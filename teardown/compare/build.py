#!/usr/bin/env python3
"""Build the head-to-head comparison page.

Usage:
  build.py <comparison.json> <perspectives.json> <research_dir_A> <research_dir_B> <out_dir>

Writes <out_dir>/index.html: one self-contained file (images inlined, downscaled). The only external
request is the Google Fonts stylesheet. Prints a lint report (banned words, jargon, dashes, lengths).
Layout and wording rules: ../COMPARE_SPEC.md.
"""
import base64
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
E = html.escape

BANNED = ["works", "winning", "winner", "winners", "best-performing", "top-performing", "converts",
          "effective", "successful", "profitable", "ROI", "ROAS", "scaling"]
JARGON = ["DCO", "UTM", "utm_", "tercile", "concept_id", "concept", "WPM", "Entity ID", "copies"]

STATUS_TEXT = {  # (status, reader) -> label
    ("only_A", "A"): "Only you", ("only_A", "B"): "Only them",
    ("only_B", "A"): "Only them", ("only_B", "B"): "Only you",
    ("even", "A"): "Even", ("even", "B"): "Even",
    ("neither", "A"): "Neither", ("neither", "B"): "Neither",
}
NICE = {
    "founder_declared": "founder (the ad says so)", "expert_or_staff": "expert or staff", "creator": "creator",
    "celebrity_named": "named celebrity", "customer": "customer", "presenter": "unnamed presenter",
    "actor_model": "actor or model", "none": "none",
    "offer": "offer", "number_claim": "number or claim", "social_proof": "social proof", "question": "question",
    "problem": "problem", "callout": "calls out an audience", "story_open": "story opening", "visual_only": "visual only",
    "discount": "discount", "cashback": "cashback", "free": "free item or trial", "rate_return": "rate or return",
    "emi_or_bundle": "EMI or bundle", "other": "other",
    "price_value": "price or value", "trust_safety": "trust or safety", "convenience_speed": "convenience or speed",
    "quality_design": "quality or design", "outcome": "outcome for the user", "popularity": "popularity",
    "feature": "one feature", "identity": "identity",
    "english": "English", "hindi": "Hindi", "hinglish": "Hinglish",
    "phone_lofi": "phone, lo-fi", "studio": "studio", "high_film": "high-end film", "designed_static": "designed graphic",
    "ai_or_stock": "AI or stock",
    "app": "app store", "web": "website", "whatsapp": "WhatsApp", "lead_form": "lead form on Facebook",
    "unclear": "unclear",
}


def nice(v):
    if v is None:
        return "untagged"
    if isinstance(v, str) and v.startswith("regional:"):
        return v.split(":", 1)[1].title()
    return NICE.get(v, str(v).replace("_", " "))


def pct(x):
    return f"{round(x * 100)}%"


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


class Images:
    def __init__(self, dirs):
        self.dirs = dirs
        self.cache = {}
        self.bytes = 0

    def uri(self, brand, rel, width=360):
        if not rel:
            return None
        key = (brand, rel, width)
        if key in self.cache:
            return self.cache[key]
        p = Path(self.dirs[brand]) / rel
        if not p.exists():
            self.cache[key] = None
            return None
        im = Image.open(p).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=70, optimize=True, progressive=True)
        data = buf.getvalue()
        self.bytes += len(data)
        uri = "data:image/jpeg;base64," + base64.b64encode(data).decode()
        self.cache[key] = uri
        return uri


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", str(t).lower()).strip("-")[:40]


def lean_evidence(g):
    """Evidence for an idea or series: strong at 5 ads, or 120 days live with 2 ads; moderate at 2 ads or 90 days."""
    n, d = g.get("n", 0), g.get("longest_days", 0)
    if n >= 5 or (d >= 120 and n >= 2):
        return "strong"
    if n >= 2 or d >= 90:
        return "moderate"
    return "thin"


def thin_frames(frames):
    """Drop stills that repeat the opening line inside the first 3 seconds, keeping the first and the one nearest 3 s."""
    early = [f for f in frames if f.get("t") is not None and f["t"] <= 3]
    keep_early = {id(early[0]), id(early[-1])} if early else set()
    return [f for f in frames if f.get("t") is None or f["t"] > 3 or id(f) in keep_early or not f.get("spoken_repeat")]


def lowfirst(t):
    """Lower-case a leading capital for use mid-sentence, leaving acronyms such as FD alone."""
    return t[:1].lower() + t[1:] if len(t) > 1 and t[1].islower() else t


def launch_fill(k, v, mx):
    return f'<div class="fill {k}" style="width:{v / mx * 100:.1f}%"></div>' if v else ""


def img_tag(uri, alt, cls=""):
    """cls "fit" shows the whole image (static ads); default crops to fill (video stills)."""
    if not uri:
        return f'<div class="{cls}" role="img" aria-label="no still" style="aspect-ratio:4/5;background:var(--line-2)"></div>'
    return f'<img src="{uri}" alt="{E(alt)}" decoding="async"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'


SMALL_BASE = 10  # a medium total under this on either side shows counts, not shares, and a small-base note


def heat(share):
    return "h0" if share < 0.10 else "h1" if share < 0.25 else "h2" if share < 0.40 else "h3"


def status_label(r, me):
    s = r["status"]
    if s.endswith("_lead"):
        lead = s[0]
        return f"{'You' if lead == me else 'Them'} {r['ratio']}x"
    return STATUS_TEXT[(s, me)]


class Page:
    def __init__(self, comp, persp, dirs):
        self.c = comp
        self.p = persp
        self.img = Images(dirs)
        self.names = {k: comp["meta"]["brands"][k]["name"] for k in ("A", "B")}
        self.rows = {r["id"]: r for r in comp["rows"]}
        self.extras = persp.get("extras") or {}
        # v4 layout (plan, workhorses, products, scripts) whenever a focus product is set or a plan is written;
        # with a plan but no focus product (the brands share no product) the full-sample map is the main map.
        self.v4 = bool(comp.get("focus")) or any((persp.get(k) or {}).get("plan") for k in ("A", "B"))
        self.by_impr = comp["meta"].get("sample_order", "impressions") == "impressions"

    # ---------- helpers
    def other(self, k):
        return "B" if k == "A" else "A"

    def ad(self, lid):
        return self.c["ads"][lid]

    def nmed(self, k, medium, scope="focus"):
        f = self.c.get("focus")
        if scope == "focus" and f:
            return f["brands"][k][f"n_{medium}"]
        return self.c["meta"]["brands"][k][f"n_{medium}"]

    def flabel(self):
        f = self.c.get("focus")
        return f["label"] if f else None

    def idea_name(self, k, idea):
        n = (self.c.get("idea_names") or {}).get(k, {}).get(idea)
        if not n:
            return "Untitled idea"
        n = n.strip('"')
        return re.sub(r"^Static:\s*", "Image ad: ", n)

    def plabel(self, key):
        labels = ((self.c.get("products") or {}).get("labels") or {})
        return labels.get(key, (key or "unclear").replace("_", " ").capitalize())

    def card(self, lid):
        a = self.ad(lid)
        uri = self.img.uri(a["brand"], a["still"], 320)
        line = a["hook_text"] or a["headline"]
        return (f'<article class="card">{img_tag(uri, "Still from the ad", "" if a["medium"] == "video" else "fit")}'
                f'<div class="cb"><div class="q">&ldquo;{E(line)}&rdquo;</div>'
                f'<div class="meta num">{a["days"]} days live, {plural(a["versions"], "version")}<br>'
                f'<a href="{E(a["link"])}" target="_blank" rel="noopener">Open in Ad Library</a></div></div></article>')

    # ---------- first screen
    def header(self):
        m = self.c["meta"]
        A, B = m["brands"]["A"], m["brands"]["B"]
        country = {"IN": "India"}.get(m["country"], m["country"])
        return f"""
<header class="top wrap">
  <h1>{E(self.names['A'])} <span class="vs">vs</span> {E(self.names['B'])}</h1>
  <p class="sample">Meta ads in {E(country)}, snapshot {fmt_date(m['snapshot_date'], short=True)} {m['snapshot_date'][:4]}. <b>{E(self.names['A'])} {A['n']} ads, {E(self.names['B'])} {B['n']}</b>:
  {E(m.get("sample_short") or "the ones the Ad Library ranks highest by impressions")}. <b>No spend or results are public.</b></p>{self.products_note()}
  <div class="controls"><div class="seg" role="group" aria-label="Read this page as">
    <button type="button" data-set-me="A" aria-pressed="true">I am {E(self.names['A'])}</button>
    <button type="button" data-set-me="B" aria-pressed="false">I am {E(self.names['B'])}</button></div>
  <button class="theme" type="button" data-theme-toggle aria-label="Switch colour theme">Theme</button></div>
</header>"""

    def products_note(self):
        """First-screen line when the two brands share no advertised product (v4 without a focus product)."""
        if not self.v4 or self.c.get("focus") or not (self.c.get("products") or {}).get("counts"):
            return ""
        note = self.extras.get("products_note")
        if not note:
            cnt = self.c["products"]["counts"]
            def sells(k):
                return ", ".join(f"{lowfirst(self.plabel(x))} {n}" for x, n in cnt[k].items() if x != "unclear")
            note = (f"No product is shared. Ads per product: {self.names['A']}, {sells('A')}; "
                    f"{self.names['B']}, {sells('B')}. The map covers each whole sample.")
        return f'<p class="sample prodnote"><b>{E(note)}</b> <a href="#products" data-fold="products">What each sells</a></p>'

    def verdict_and_moves(self, me):
        p = self.p.get(me, {})
        out = [f'<div class="only-{me}">']
        out.append(f'<p class="verdict">{E(p.get("verdict", "Verdict not written yet."))}</p>')
        out.append('<ol class="moves">')
        for mv in sorted(p.get("moves", []), key=lambda m: m.get("rank", 9)):
            ev = mv.get("evidence", "thin")
            out.append(f'<li>{E(mv["text"])} <span class="test"><b>First test:</b> {E(mv["first_test"])}</span>'
                       f'<span class="chips"><span class="chip">Effort {E(mv["effort"].lower())}</span>'
                       f'<span class="chip ev-{E(ev)}">Evidence {E(ev)}</span>'
                       f'<button type="button" class="chip seeads testbtn" data-test-toggle aria-expanded="false">First test</button>'
                       f'<a class="chip seeads" href="#row-{E(mv["row"])}" data-fold="row-{E(mv["row"])}">See the ads</a></span></li>')
        out.append('</ol>')
        out.append('</div>')
        return "".join(out)

    def map(self, me, rows=None, scope="focus", folds=True):
        th = self.other(me)
        rows = rows or self.c["rows"]
        nm = lambda k, m: self.nmed(k, m, scope)
        out = [f'<div class="map only-{me}" aria-label="Gap map">']
        anysmall = any(min(nm(me, m), nm(th, m)) < SMALL_BASE for m in ("video", "image"))
        if scope != "focus" and not anysmall:
            out.append(self.top30_line(me))
        out.append(f'<div class="mhead"><div></div><div class="who"><b>You</b><br><span>{E(self.names[me])}</span></div>'
                   f'<div class="who"><b>Them</b><br><span>{E(self.names[th])}</span></div><div>Status<br>evidence</div></div>')
        for medium, title in (("video", "Video"), ("image", "Image")):
            small = min(nm(me, medium), nm(th, medium)) < SMALL_BASE
            out.append(f'<div class="mgroup"><span>{title}</span><span class="num">you {nm(me, medium)}, '
                       f'them {nm(th, medium)} sampled</span></div>')
            if small:
                zero = [self.names[k] for k in (me, th) if nm(k, medium) == 0]
                extra = (f'{" and ".join(zero)} {"has" if len(zero) == 1 else "have"} no {medium} ads here. ' if zero else "")
                out.append(f'<p class="smallbase">Small base: with under {SMALL_BASE} {medium} ads on one side, '
                           f'cells show counts, and evidence is at most moderate. {E(extra)}'
                           f'{self.top30_line(me, bare=True) if scope != "focus" else ""}</p>')
            for r in rows:
                if r["medium"] != medium:
                    continue
                cells = []
                for k in (me, th):
                    s = r[k]
                    N = nm(k, medium)
                    big = f'{s["n"]} of {N}' if small else pct(s["share"])
                    if N == 0:
                        cells.append(f'<div class="cell {k} h0 zero"><span class="pct">none</span>'
                                     f'<span class="sub">no {medium} ads</span></div>')
                        continue
                    if s["n"] == 0:
                        cells.append(f'<div class="cell {k} h0 zero"><span class="pct num{" cnt" if small else ""}">{big}</span>'
                                     f'<span class="sub">no ads</span></div>')
                        continue
                    d = f'{s["median_days"]:.0f}d' if s["median_days"] is not None else ""
                    sub = f'median {d}' if small else f'{s["n"]} ad{"" if s["n"] == 1 else "s"}, {d}'
                    cells.append(f'<div class="cell {k} {"h0" if small else heat(s["share"])}"><span class="pct num{" cnt" if small else ""}">{big}</span>'
                                 f'<span class="sub num">{sub}</span></div>')
                lead = r["lead"] or ""
                tag, attrs = ("a", f' href="#row-{r["id"]}" data-fold="row-{r["id"]}" title="{E(r["label"])}: open the evidence"') if folds else ("div", "")
                out.append(f'<{tag} class="mrow"{attrs}>'
                           f'<div class="mlabel">{E(r["label"])}</div>{"".join(cells)}'
                           f'<div class="st lead-{lead}"><span class="s">{status_label(r, me)}</span>'
                           f'<span class="e">{r["evidence"]}</span></div></{tag}>')
        fa = sum(r[me]["founder"] for r in rows)
        fb = sum(r[th]["founder"] for r in rows)
        where = [r["label"] for r in rows if r[th]["founder"] or r[me]["founder"]]
        out.append(f'<p class="founder num">Founder says so on screen: you {fa}, them {fb}'
                   f'{" (" + ", ".join(where) + ")" if where else ""}. Counted only where the ad itself says founder.</p>')
        out.append('<p class="maplegend">Share is of each brand\'s sampled ads of that medium'
                   f'{" for this product" if scope == "focus" and self.c.get("focus") else ""}; "d" is median days live so far.'
                   f'{" Tap a row for the ads." if folds else ""}</p></div>')
        return "".join(out)

    def top30_line(self, me, bare=False):
        t = self.c["meta"]["brands"]
        ta, tb = t[me]["top30_all"], t[self.other(me)]["top30_all"]
        if ta and tb:
            head = (f'Top {max(ta["n"], tb["n"])} by Library impressions' if self.by_impr
                    else f'First {max(ta["n"], tb["n"])} in the Library\'s default order')
            line = (f'{head}: you {ta["video"]} video, '
                    f'{ta["image"]} image; {E(self.names[self.other(me)])} {tb["video"]} video, {tb["image"]} image.')
        elif ta or tb:
            k = me if ta else self.other(me)
            t = ta or tb
            who = "you" if k == me else E(self.names[k])
            head = "top 30 by Library impressions" if self.by_impr else "first 30 in the Library's all-ads view"
            line = (f'Video and image lean, {head}: {who} {t["video"]} video, {t["image"]} image; '
                    f'not recorded for {"you" if k != me else E(self.names[self.other(me)])}.')
        else:
            line = 'Overall video and image lean: not recorded for this sample.'
        return line if bare else f'<p class="top30 num">{line}</p>'

    def product_line(self, me):
        pm = self.extras.get("product_mix")
        if not pm:
            return ""
        th = self.other(me)
        def one(k):
            items = pm.get(k, {}).get("items", [])
            return ", ".join(f"{E(lowfirst(n))} {c}" for n, c in items) if items else "not read"
        return (f'<p class="top30 num">What they sell, ads per product: you, {one(me)}; '
                f'{E(self.names[th])}, {one(th)}. <a href="#extras" data-fold="extras">More</a></p>')


    # ---------- action plan (v4)
    def plan_issues(self):
        """Plan evidence labels must match the rule for their basis; every anchor must exist."""
        out = []
        for k in ("A", "B"):
            pl = (self.p.get(k) or {}).get("plan")
            if not pl:
                continue
            for it in [pl.get("focus")] + pl.get("start", []) + pl.get("stop", []):
                anchor, ids, ev = self.basis_info(it.get("basis"))
                if it.get("basis") and ev is None:
                    out.append(f"plan {k}: basis '{it.get('basis')}' not found")
                elif ev not in (None, "seen") and it.get("evidence") != ev:
                    out.append(f"plan {k}: '{it['title']}' says evidence {it.get('evidence')} but its basis is {ev}")
            n = len(self.p[k].get("scripts") or [])
            for it in [pl.get("focus")] + pl.get("start", []) + pl.get("stop", []):
                if it.get("script") and not 1 <= it["script"] <= n:
                    out.append(f"plan {k}: '{it['title']}' points to script {it['script']}, which does not exist")
        return out

    def basis_info(self, basis):
        """(anchor or None, list of ad ids, computed evidence label or None) for a plan item's basis."""
        if not basis:
            return None, [], None
        kind, _, rest = basis.partition(":")
        if kind == "row":
            r = self.rows.get(rest)
            return (f"row-{rest}", [], r["evidence"] if r else None)
        if kind in ("idea", "series"):
            k, _, name = rest.partition(":")
            g = self.lean_group(k, kind, name)
            if not g:
                return None, [], None
            anchor = f"{kind}-{k}-{slug(name)}"
            return anchor, g["ad_ids"], lean_evidence(g)
        if kind == "contradictions":
            ids = [i for it in (self.extras.get("contradictions") or {}).get(rest, []) for i in it.get("ads", [])]
            return "disagree", ids, "seen"
        if kind == "ads":
            return None, [i for i in rest.split(",") if i], "seen"
        return None, [], None

    def lean_group(self, k, kind, name):
        lean = (self.c.get("lean") or {}).get(k, {}).get("all") or {}
        if kind == "idea":
            for x in lean.get("top", []):
                if x["idea"] == name:
                    return x
            # an idea outside the listed top: rebuild from the ads
            ids = [l for l, a in self.c["ads"].items() if a["brand"] == k and a["tags"].get("concept_id") == name]
            if not ids:
                return None
            sel = [self.ad(l) for l in ids]
            return {"idea": name, "ad_ids": ids, "n": len(ids), "versions": sum(a["versions"] for a in sel),
                    "longest_days": max(a["days"] or 0 for a in sel), "products": sorted({a.get("product_key") or "unclear" for a in sel})}
        for x in lean.get("series", []):
            if x["name"] == name:
                return x
        return None

    def plan_item(self, me, it, cls, n=None):
        anchor, ids, ev = self.basis_info(it.get("basis"))
        if ev == "seen":
            chip_ev = f'<span class="chip">In {plural(len(set(ids)), "ad")}</span>' if ids else ""
        else:
            ev = it.get("evidence", ev or "thin")
            eff_t = f', {E(it["effort"].lower())} effort' if it.get("effort") else ""
            chip_ev = f'<span class="chip ev-{E(ev)}">{E(ev.capitalize())} evidence{eff_t}</span>'
        eff = ""
        links = []
        if anchor:
            links.append(f'<a class="chip seeads" href="#{anchor}" data-fold="{anchor}">Ads</a>')
        elif ids:
            a = self.c["ads"].get(ids[0])
            if a:
                links.append(f'<a class="chip seeads" href="{E(a["link"])}" target="_blank" rel="noopener">Ad</a>')
        if it.get("script"):
            sid = f"script-{me}-{it['script']}"
            links.append(f'<a class="chip seeads" href="#{sid}" data-fold="{sid}">Script</a>')
        num = f'<span class="pn">{n}</span>' if n else ""
        return (f'<li class="pi {cls}">{num}<div class="pt">{E(it["title"])}</div>'
                f'<div class="pw">{E(it.get("why", ""))}</div>'
                f'<div class="ptest"><b>First test:</b> {E(it.get("first_test", ""))}</div>'
                f'<span class="chips">{chip_ev}{eff}'
                f'<button type="button" class="chip seeads testbtn" data-test-toggle aria-expanded="false">Why and test</button>'
                f'{"".join(links)}</span></li>')

    def plan(self, me):
        p = self.p.get(me, {})
        pl = p.get("plan")
        out = [f'<div class="only-{me}">', f'<p class="verdict">{E(p.get("verdict", "Verdict not written yet."))}</p>']
        if not pl:
            out.append('</div>')
            return "".join(out) + self.verdict_and_moves(me).replace(f'<p class="verdict">{E(p.get("verdict", ""))}</p>', "", 1)
        out.append('<div class="plan" aria-label="What to do on Monday">')
        out.append('<div class="plabel">Focus</div><ol class="pl focus">' + self.plan_item(me, pl["focus"], "f") + '</ol>')
        out.append('<div class="plabel">Start</div><ol class="pl">' +
                   "".join(self.plan_item(me, it, "s", i) for i, it in enumerate(pl.get("start", []), 1)) + '</ol>')
        out.append('<div class="plabel">Stop or fix</div><ol class="pl">' +
                   "".join(self.plan_item(me, it, "x", i) for i, it in enumerate(pl.get("stop", []), 1)) + '</ol>')
        out.append('</div></div>')
        return "".join(out)

    # ---------- what they lean on (workhorses)
    def lean_rule_text(self):
        r = self.c.get("lean_rule") or {}
        return (f"Leaning score = ads using the idea + half a point per extra version + one point per {r.get('days_per_point', 30)} days "
                f"of its longest-running ad + {r.get('recut_points', 2)} points per extra product, city or centre it is re-cut for "
                "(places as named in each ad's text). "
                "Long life and many versions are the nearest public sign that a brand keeps paying for an idea. "
                "They do not show that it performs: the Library publishes no spend or results.")

    def idea_card(self, k, x, big=False):
        a = self.ad(x["lead_ad"] if x.get("lead_ad") else x["ad_ids"][0])
        uri = self.img.uri(k, a["still"], 240 if big else 160)
        prods = ", ".join(lowfirst(self.plabel(p)) for p in x.get("products", []))
        anchor = f'idea-{k}-{slug(x["idea"])}'
        return (f'<div class="wh" id="{anchor}">{img_tag(uri, "Still from the ad", "" if a["medium"] == "video" else "fit")}'
                f'<div><div class="whn">{E(self.idea_name(k, x["idea"]))}</div>'
                f'<div class="q whq">&ldquo;{E(a["hook_text"] or a["headline"])}&rdquo;</div>'
                f'<div class="whs num">{plural(x["n"], "ad")}, {plural(x["versions"], "version")}, longest {x["longest_days"]} days live'
                f'{", " + E(prods) if prods else ""}{self.places(x)}. Score {x.get("score", "")}.</div>'
                f'<div class="adlinks">{self.ad_links(x["ad_ids"]).strip()}</div></div></div>')

    def series_card(self, k, x):
        anchor = f'series-{k}-{slug(x["name"])}'
        seen, stills = set(), []
        for l in x["ad_ids"]:
            a = self.ad(l)
            idea = a["tags"].get("concept_id")
            if idea in seen:
                continue
            seen.add(idea)
            stills.append(f'<div class="mini">{img_tag(self.img.uri(k, a["still"], 160), "Still", "" if a["medium"] == "video" else "fit")}'
                          f'{E(self.plabel(a.get("product_key")))}</div>')
        prods = ", ".join(self.plabel(p) for p in x.get("products", []))
        n_brand = self.c["meta"]["brands"][k]["n"]
        return (f'<div class="series" id="{anchor}"><div class="whn">{E(x["name"])}</div>'
                f'<div class="whs num">{x["n"]} of {n_brand} ads, {plural(x["ideas"], "idea")}, {plural(x["versions"], "version")}, '
                f'longest {x["longest_days"]} days live; products: {E(prods)}{self.places(x)}. Score {x["score"]}.</div>'
                f'<p class="small">{E(x.get("note", ""))}</p><div class="strip">{"".join(stills[:6])}</div>'
                f'<div class="adlinks">{self.ad_links(x["ad_ids"]).strip()}</div></div>')

    def lean_compact(self, me):
        """First-screen summary: each brand's top series (or idea) with one still."""
        out = [f'<div class="leanmini only-{me}"><div class="plabel">What they lean on</div>']
        for k in (me, self.other(me)):
            lean = (self.c.get("lean") or {}).get(k, {}).get("all")
            if not lean:
                continue
            top = lean["top"][0] if lean["top"] else None
            ser = lean["series"][0] if lean.get("series") else None
            who = "You" if k == me else E(self.names[k])
            if ser:
                a = self.ad(ser["lead_ad"])
                line = (f'<b>{E(ser["name"])}</b>: {ser["n"]} of {lean["n"]} ads, {ser["versions"]} versions, '
                        f'longest {ser["longest_days"]} days, {plural(len(ser["products"]), "product")}{self.places(ser)}.')
                anchor = f'series-{k}-{slug(ser["name"])}'
            else:
                a = self.ad(top["lead_ad"])
                line = (f'<b>{E(self.idea_name(k, top["idea"]))}</b>: {top["n"]} of {lean["n"]} ads, {top["versions"]} versions, '
                        f'longest {top["longest_days"]} days.')
                anchor = f'idea-{k}-{slug(top["idea"])}'
            out.append(f'<a class="lm" href="#{anchor}" data-fold="{anchor}">{img_tag(self.img.uri(k, a["still"], 120), "Still", "" if a["medium"] == "video" else "fit")}'
                       f'<div><div class="lmw"><span class="sw {k}"></span>{who}</div><div class="small num">{line}</div>'
                       f'<div class="q small muted">&ldquo;{E(a["hook_text"])}&rdquo;</div></div></a>')
        out.append('<p class="small muted" style="margin:6px 0 0">Long life and many versions show an idea is kept running, '
                   'the nearest public sign a brand keeps paying for it; not that it performs.</p></div>')
        return "".join(out)

    def places(self, x):
        n = x.get("cities") or 0
        return f", re-sent for {n} named places" if n > 1 else ""

    def lean_section(self):
        if not self.c.get("lean"):
            return ""
        parts = []
        for me in ("A", "B"):
            p = self.p.get(me, {})
            if p.get("workhorse_read"):
                parts.append(f'<p class="read only-{me}">{E(p["workhorse_read"])}</p>')
        for me in ("A", "B"):
            cols = []
            for k in (me, self.other(me)):
                lean = self.c["lean"][k]["all"]
                c = lean["concentration"]
                head = (f'<h3 class="bh"><span class="sw {k}"></span>{E(self.names[k])}{" (you)" if k == me else ""}</h3>'
                        f'<p class="small num">{lean["n"]} ads, {lean["ideas_total"]} ideas. The highest-scoring idea carries {c["top1_n"]} of {lean["n"]} ads '
                        f'({pct(c["top1"])}); the three highest, {c["top3_n"]} of {lean["n"]} ({pct(c["top3"])}).'
                        + (f' Its biggest series or recurring line carries {lean["series"][0]["n"]} of {lean["n"]} '
                           f'({pct(lean["series"][0]["share"])}).' if lean.get("series") else "") + '</p>')
                ser = "".join(self.series_card(k, x) for x in lean.get("series", []))
                ideas = "".join(self.idea_card(k, x) for x in lean["top"])
                cols.append(f'<div>{head}{f"<h4 class={chr(34)}xh{chr(34)}>Series and recurring lines</h4>" + ser if ser else ""}'
                            f'<h4 class="xh">Ideas ranked by leaning score</h4>{ideas}</div>')
            parts.append(f'<div class="only-{me}"><div class="pair">{"".join(cols)}</div></div>')
        parts.append(f'<p class="note">{E(self.lean_rule_text())}</p>')
        return self.section("lean", "Workhorses", "What they lean on", "".join(parts),
                            "Counting ads per row hides that one idea or one series can carry a brand. Here are the ideas each brand keeps re-running. "
                            "Long life and many versions are a sign a brand keeps paying for an idea, not that it performs.")

    # ---------- products: like for like, and the rest
    def products_section(self):
        pr = self.c.get("products")
        if not pr or not pr.get("counts"):
            return ""
        f = self.c.get("focus")
        site = pr.get("site") or {}
        counts = pr["counts"]
        keys = []
        for k in ("A", "B"):
            for x in list(counts[k]) + [e["key"] for e in site.get(k, [])]:
                if x not in keys and x != "unclear":
                    keys.append(x)
        rows = []
        for key in keys:
            cells = []
            for k in ("A", "B"):
                n = counts[k].get(key, 0)
                se = next((e for e in site.get(k, []) if e["key"] == key), None)
                st = (se or {}).get("status")
                on_site = ("not on the site" if not se else "unclear on the site" if st == "unclear"
                           else "registration only" if st == "registration_only"
                           else "on the site, page not readable" if st == "not_read" else "on the site")
                cells.append(f'<td class="n" data-l="{E(self.names[k])} ads">{n} of {self.c["meta"]["brands"][k]["n"]}</td>'
                             f'<td class="small" data-l="{E(self.names[k])} site">{E(on_site)}'
                             f'{": " + E(lowfirst(se["claim"])) if se else ""}</td>')
            focus_mark = ' class="focusrow"' if f and key == f["key"] else ""
            rows.append(f'<tr{focus_mark}><td class="pname"><b>{E(self.plabel(key))}</b></td>{"".join(cells)}</tr>')
        table = (f'<div class="tablewrap"><table class="t prod"><tr><th>Product</th><th class="n">{E(self.names["A"])} ads</th>'
                 f'<th>{E(self.names["A"])} site</th><th class="n">{E(self.names["B"])} ads</th><th>{E(self.names["B"])} site</th></tr>'
                 f'{"".join(rows)}</table></div>')
        fetched = site.get("fetched")
        lede = ("What each company sells, from its own website" + (f" (read {fmt_date(fetched)})" if fetched else "") +
                ", against what its sampled ads sell. " +
                ("The map compares only the product both advertise." if f else
                 "No product appears in both brands' ads, so there is no single-product map; the map above covers each whole sample."))
        # what else each advertises
        other = []
        for k in ("A", "B"):
            items = []
            for key, wh in ((self.c.get("lean") or {}).get(k, {}).get("by_product") or {}).items():
                if key == "unclear" or not wh["top"]:
                    continue
                x = wh["top"][0]
                items.append(f'<div class="op"><div class="whn">{E(self.plabel(key))}: <span class="num">{wh["n"]} ads, '
                             f'{plural(wh["ideas_total"], "idea")}</span></div><div class="small muted">Leans on:</div>'
                             f'{self.idea_card(k, x)}</div>')
            body = "".join(items) or f'<p class="small">Every sampled ad sells {E((f or {}).get("label", "one product").lower())}.</p>'
            absent = [e for e in site.get(k, []) if counts[k].get(e["key"], 0) == 0]
            if absent:
                body += ('<p class="small"><b>On the site but in none of the sampled ads:</b> ' +
                         "; ".join(f'{E(self.plabel(e["key"]))} ({E(e["claim"])})' for e in absent) + '.</p>')
            other.append(f'<div><h3 class="bh"><span class="sw {k}"></span>{E(self.names[k])}</h3>{body}</div>')
        return self.section("products", "Like for like", "What each one sells", table +
                            f'<h3 class="xh" style="margin-top:22px">{"What else each one advertises" if f else "What each one advertises, product by product"}</h3>'
                            f'<div class="pair">{"".join(other)}</div>', lede)

    def focus_map_section(self):
        f = self.c.get("focus")
        if not f:
            return ""
        b = f["brands"]
        parts = [self.map("A") + self.map("B")]
        if self.c.get("rows_all"):
            parts.append(f'<details class="fold allmap"><summary><span class="sumlabel">All products together</span>'
                         f'<span class="sumstat">The same map over the whole sample: {E(self.names["A"])} {self.c["meta"]["brands"]["A"]["n"]} ads, '
                         f'{E(self.names["B"])} {self.c["meta"]["brands"]["B"]["n"]}. It mixes products, so read it as context only.</span></summary>'
                         f'<div class="foldbody">{self.map("A", self.c["rows_all"], "all", False)}{self.map("B", self.c["rows_all"], "all", False)}</div></details>')
        title = f'{f["label"]} against {f["label"].lower()}'
        lede = (f'Only the ads that sell {E(f["label"].lower())}: {E(self.names["A"])} {b["A"]["n"]} ads ({b["A"]["ideas"]} ideas), '
                f'{E(self.names["B"])} {b["B"]["n"]} ({b["B"]["ideas"]} ideas).')
        return self.section("bonds", "Like for like", title, "".join(parts), lede)

    def whole_map_section(self):
        """v4 without a focus product: the full-sample map is the main map, under a plain no-shared-product note."""
        n = self.c["meta"]["brands"]
        note = self.extras.get("map_note") or (
            "These two sell different things, so this map compares each brand's whole sample, not one product. "
            "Read it as how each one makes ads, and see What each one sells and What is comparable below.")
        lede = (f'{E(note)} {E(self.names["A"])} {n["A"]["n"]} ads, {E(self.names["B"])} {n["B"]["n"]}.')
        return self.section("wholemap", "No shared product", "The whole sample, side by side",
                            self.map("A", scope="all") + self.map("B", scope="all"), lede)

    def comparable_section(self):
        """extras.comparable: the things two brands with different products can be compared on, reader first."""
        cp = self.extras.get("comparable")
        if not cp:
            return ""
        parts = []
        for me in ("A", "B"):
            th = self.other(me)
            rows = []
            for r in cp.get("rows", []):
                cells = "".join(
                    f'<div><div class="cmpw"><span class="sw {k}"></span>{"You" if k == me else E(self.names[k])}</div>'
                    f'<p class="small">{E((r.get(k) or {}).get("text", ""))}{self.ad_links((r.get(k) or {}).get("ads"))}</p></div>'
                    for k in (me, th))
                rows.append(f'<div class="cmprow"><h3 class="xh">{E(r["label"])}</h3><div class="pair">{cells}</div></div>')
            parts.append(f'<div class="only-{me}">{"".join(rows)}</div>')
        return self.section("comparable", "Like for like", cp.get("title", "What is comparable"), "".join(parts),
                            E(cp.get("lede", "")))

    # ---------- scripts to brief
    def brief_text(self, me, i, d):
        lines = [f"SCRIPT DIRECTION {i}: {d['title']}"]
        if d.get("label"):
            lines.append(d["label"])
        lines += [f"Who it talks to: {d['persona']}", f"Why: {d['why']}",
                  f"Format: {d['format']}, {d['length']}, {d.get('language', '')}", "", "First 3 seconds, options:"]
        lines += [f"- {o}" for o in d.get("openings", [])]
        lines += ["", "Beats:"] + [f"- {b['t']} {b['beat']}: {b['note']}" for b in d.get("beats", [])]
        lines += ["", "Draft script:"] + [f"{r['t']} | VO: {r['voice']} | ON SCREEN: {r['screen']}" for r in d.get("script", [])]
        lines += ["", f"On-screen notes: {d.get('on_screen', '')}", f"End card: {d.get('end_card', '')}", "", "Compliance watch-outs:"]
        lines += [f"- {c}" for c in d.get("compliance", [])]
        lines += ["", "What to measure:"] + [f"- {m}" for m in d.get("measure", [])]
        return "\n".join(lines)

    def scripts_section(self):
        parts = []
        any_ = False
        for me in ("A", "B"):
            ds = self.p.get(me, {}).get("scripts") or []
            if not ds:
                continue
            any_ = True
            items = []
            for i, d in enumerate(ds, 1):
                sid = f"script-{me}-{i}"
                ev = self.ad_links(d.get("evidence_ads"))
                label = f'<p class="reco">{E(d["label"])}</p>' if d.get("label") else ""
                beats = "".join(f'<tr><td class="tc num">{E(b["t"])}</td><td><b>{E(b["beat"])}</b></td><td>{E(b["note"])}</td></tr>'
                                for b in d.get("beats", []))
                script = "".join(f'<tr><td class="tc num">{E(r["t"])}</td><td class="vo">{E(r["voice"])}</td><td class="os">{E(r["screen"])}</td></tr>'
                                 for r in d.get("script", []))
                opens = "".join(f'<li class="vo">{E(o)}</li>' for o in d.get("openings", []))
                comp = "".join(f"<li>{E(c)}</li>" for c in d.get("compliance", []))
                meas = "".join(f"<li>{E(m)}</li>" for m in d.get("measure", []))
                items.append(
                    f'<details class="brief fold" id="{sid}"{" open" if i == 1 else ""}><summary><span class="bn num">{i}</span>'
                    f'<span class="sumlabel">{E(d["title"])}</span><span class="sumstat">{E(d["format"])}; {E(d["length"])}; {E(d.get("language", ""))}</span></summary>'
                    f'<div class="foldbody">{label}'
                    f'<p><b>Who it talks to.</b> {E(d["persona"])}</p><p><b>Why.</b> {E(d["why"])}{ev}</p>'
                    f'<h4 class="xh">First 3 seconds, options</h4><ul class="opens">{opens}</ul>'
                    f'<h4 class="xh">Beats</h4><div class="tablewrap"><table class="t beats">{beats}</table></div>'
                    f'<h4 class="xh">Draft script</h4><div class="tablewrap"><table class="t script"><tr><th>Time</th><th>Voice</th><th>On screen</th></tr>{script}</table></div>'
                    f'<p><b>On-screen notes.</b> {E(d.get("on_screen", ""))}</p><p><b>End card.</b> {E(d.get("end_card", ""))}</p>'
                    f'<div class="pair"><div><h4 class="xh">Compliance watch-outs</h4><ul class="facts small">{comp}</ul></div>'
                    f'<div><h4 class="xh">What to measure</h4><ul class="facts small">{meas}</ul></div></div>'
                    f'<textarea class="briefsrc" hidden readonly>{E(self.brief_text(me, i, d))}</textarea>'
                    f'<button type="button" class="copy" data-copy>Copy this brief</button></div></details>')
            parts.append(f'<div class="only-{me}">{"".join(items)}</div>')
        if not any_:
            return ""
        return self.section("scripts", "For the content team", "Scripts to brief", "".join(parts),
                            "Each direction is one line you can say to the team, then the detail to brief it. Figures in [brackets] are yours to fill "
                            "from the live product on the day of the edit; every other fact is taken from the brands' own ads or sites.")

    def disagree_section(self):
        co = (self.extras or {}).get("contradictions")
        if not co:
            return ""
        parts = []
        for me in ("A", "B"):
            th = self.other(me)
            cols = []
            for k, who in ((me, "Your ads"), (th, f"{self.names[th]}'s ads")):
                items = "".join(f'<li>{E(it["text"])}{self.ad_links(it.get("ads"))}</li>' for it in co.get(k, []))
                cols.append(f'<div><h4 class="bh"><span class="sw {k}"></span>{E(who)}</h4>'
                            f'<ul class="facts">{items or "<li>None found.</li>"}</ul></div>')
            parts.append(f'<div class="only-{me}"><div class="pair">{"".join(cols)}</div></div>')
        return self.section("disagree", "Fix first", "Where their own ads disagree", "".join(parts),
                            "Figures that differ between ads of one brand, or inside one ad. A viewer who sees two of them sees both numbers.")

    def first_screen(self):
        if self.v4:
            left = self.plan("A") + self.plan("B")
            right = self.lean_compact("A") + self.lean_compact("B")
            return f'{self.header()}<div class="wrap"><div class="hero"><div>{left}</div><div>{right}</div></div></div>'
        left = self.verdict_and_moves("A") + self.verdict_and_moves("B")
        right = self.map("A") + self.map("B")
        return f'{self.header()}<div class="wrap"><div class="hero"><div>{left}</div><div>{right}</div></div></div>'

    # ---------- sections
    def section(self, sid, kicker, title, body, lede=""):
        return (f'<section id="{sid}" class="wrap"><div class="kicker">{E(kicker)}</div><h2>{E(title)}</h2>'
                f'{f"<p class={chr(34)}lede prose{chr(34)}>{lede}</p>" if lede else ""}{body}</section>')

    def folds(self):
        out = []
        for r in self.c["rows"]:
            sides = []
            for k in ("A", "B"):
                s = r[k]
                d = f'median {s["median_days"]:.0f} days live' if s["median_days"] is not None else "no ads"
                fl = f'{self.flabel().lower()} ' if self.flabel() else ""
                if self.nmed(k, r["medium"]) == 0:
                    stat = f'No {fl}{r["medium"]} ads in the sample.'
                    sides.append(f'<div class="side"><h4><span class="sw {k}"></span>{E(self.names[k])}</h4>'
                                 f'<p class="stat num">{stat}</p></div>')
                    continue
                stat = (f'{s["n"]} of {self.nmed(k, r["medium"])} {fl}{r["medium"]} ads ({pct(s["share"])}), '
                        f'{plural(s["ideas"], "idea")}, {plural(s["versions"], "version")}, {d}.')
                if s["founder"]:
                    stat += f' {s["founder"]} say a founder is speaking (counted only where the ad says so).'
                cards = "".join(self.card(l) for l in r["cards"][k]) or '<div class="empty">No ads in this row.</div>'
                sides.append(f'<div class="side"><h4><span class="sw {k}"></span>{E(self.names[k])}</h4>'
                             f'<p class="stat num">{stat}</p><div class="cards">{cards}</div></div>')
            lead = r["lead"]
            summ = {"even": "both run it", "neither": "neither runs it enough to count"}.get(
                r["status"], f'{E(self.names[lead])} {"only" if r["status"].startswith("only") else "leads " + str(r["ratio"]) + "x"}' if lead else "")
            out.append(f'<details class="fold" id="row-{r["id"]}"><summary><span class="sumlabel">{E(r["label"])}</span>'
                       f'<span class="sumstat">{r["medium"]}: {summ}; evidence {r["evidence"]}</span></summary>'
                       f'<div class="foldbody"><div class="pair">{"".join(sides)}</div>'
                       f'<p class="note">Cards: one per idea, longest-running first.</p></div></details>')
        return self.section("map", "Evidence", "The map, row by row", "".join(out),
                            "Each row opens to the ads behind it. An idea is one message with one main visual; "
                            "versions are near-duplicates of it that differ only in crop, caption or button.")

    def ad_links(self, ids):
        out = []
        for i, l in enumerate(ids or [], 1):
            a = self.c["ads"].get(l)
            if a:
                out.append(f'<a href="{E(a["link"])}" target="_blank" rel="noopener">ad {i}</a>')
        return f' <span class="adlinks">{", ".join(out)}</span>' if out else ""

    def extras_section(self):
        x = self.extras
        if not x:
            return ""
        parts = []
        pm = x.get("product_mix")
        if pm:
            cols = []
            for k in ("A", "B"):
                d = pm.get(k) or {}
                items = d.get("items", [])
                tot = sum(c for _, c in items) or 1
                bars = "".join(
                    f'<div class="brow"><div class="bl">{E(n)}</div><div class="bars"><div class="bar">'
                    f'<div class="track"><div class="fill {k}" style="width:{c / tot * 100:.1f}%"></div></div>'
                    f'<span class="v num">{c} of {self.c["meta"]["brands"][k]["n"]}</span></div></div></div>' for n, c in items)
                note = f'<p class="small muted">{E(d["note"])}</p>' if d.get("note") else ""
                cols.append(f'<div><h4 class="bh"><span class="sw {k}"></span>{E(self.names[k])}</h4>{bars}{note}</div>')
            parts.append(f'<h3 class="xh">What they sell</h3><div class="pair">{"".join(cols)}</div>')
        se = x.get("series")
        if se:
            cols = []
            for k in ("A", "B"):
                items = "".join(f'<li><b>{E(it["name"])}</b> <span class="num">({plural(len(it.get("ads", [])), "ad")})</span>: '
                                f'{E(it.get("note", ""))}{self.ad_links(it.get("ads"))}</li>' for it in se.get(k, []))
                cols.append(f'<div><h4 class="bh"><span class="sw {k}"></span>{E(self.names[k])}</h4>'
                            f'<ul class="facts">{items or "<li>None found.</li>"}</ul></div>')
            parts.append(f'<h3 class="xh">Series and recurring lines</h3><div class="pair">{"".join(cols)}</div>')
        co = x.get("contradictions")
        if co:
            for me in ("A", "B"):
                th = self.other(me)
                cols = []
                for k, who in ((me, "Your ads"), (th, f"{self.names[th]}'s ads")):
                    items = "".join(f'<li>{E(it["text"])}{self.ad_links(it.get("ads"))}</li>' for it in co.get(k, []))
                    cols.append(f'<div><h4 class="bh"><span class="sw {k}"></span>{E(who)}</h4>'
                                f'<ul class="facts">{items or "<li>None found.</li>"}</ul></div>')
                parts.append(f'<div class="only-{me}"><h3 class="xh">Where their own ads disagree</h3>'
                             f'<p class="small muted">Figures that differ between ads of one brand, or within one ad. '
                             f'A viewer who sees two of them sees both numbers.</p><div class="pair">{"".join(cols)}</div></div>')
        lede = E(x.get("source", ""))
        return self.section("extras", "Beyond the map", "What they sell and what they say", "".join(parts), lede)

    def lead_section(self):
        out = []
        for me in ("A", "B"):
            th = self.other(me)
            rows = [r for r in self.c["rows"] if r["lead"] == me]
            items = []
            for r in rows:
                s, o = r[me], r[th]
                items.append(f'<li><b>{E(r["label"])}</b> <span class="num">({r["medium"]}): you {s["n"]} of '
                             f'{self.nmed(me, r["medium"])} ({pct(s["share"])}), {plural(s["ideas"], "idea")}; '
                             f'{E(self.names[th])} ' + (f'{o["n"]} of {self.nmed(th, r["medium"])}' if self.nmed(th, r["medium"]) else f'no {r["medium"]} ads')
                             + f'. Evidence {r["evidence"]}.</span></li>')
            body = f'<ul class="facts">{"".join(items)}</ul>' if items else '<p>We found no row where you lead.</p>'
            out.append(f'<div class="only-{me}">{body}</div>')
        scope = f" in {self.flabel().lower()}" if self.flabel() else ""
        return self.section("lead", "Fair both ways", f"Where you lead{scope}", "".join(out),
                            "The same rules as the gaps: present at 3 ads, a lead at twice the rival's share.")

    def stakes_section(self):
        even = [self.rows[i] for i in self.c["table_stakes"]]
        neither = [r for r in self.c["rows"] if r["status"] == "neither"]
        items = []
        for r in even:
            items.append(f'<li><b>{E(r["label"])}</b> <span class="num">({r["medium"]}): {E(self.names["A"])} '
                         f'{r["A"]["n"]} of {self.nmed("A", r["medium"])}, {E(self.names["B"])} {r["B"]["n"]} of '
                         f'{self.nmed("B", r["medium"])}.</span> Both of you do this, so stand out inside it rather than copy it.</li>')
        for r in neither:
            items.append(f'<li><b>{E(r["label"])}</b> <span class="num">({r["medium"]}): {E(self.names["A"])} {r["A"]["n"]}, '
                         f'{E(self.names["B"])} {r["B"]["n"]}.</span> Neither of you runs it enough to count. Open ground, '
                         f'but with no evidence either way.</li>')
        scope = f" in {self.flabel().lower()}" if self.flabel() else ""
        return self.section("stakes", "Context", f"Table stakes and open ground{scope}",
                            f'<ul class="facts">{"".join(items) or "<li>None.</li>"}</ul>')

    def now_section(self):
        now = self.c["now"]
        days = self.c["meta"]["thresholds"]["now_days"]
        parts = []
        for me in ("A", "B"):
            r = self.p.get(me, {}).get("now_read")
            if r:
                parts.append(f'<p class="read only-{me}">{E(r)}</p>')
        for k in ("A", "B"):
            n = now[k]
            by = ", ".join(f'{self.rows[x]["label"] if x in self.rows else "unclear"} {v}'
                           for x, v in sorted(n["by_row"].items(), key=lambda kv: -kv[1]))
            minis = "".join(
                f'<div class="mini">{img_tag(self.img.uri(k, self.ad(l)["still"], 200), "Still", "" if self.ad(l)["medium"] == "video" else "fit")}'
                f'{E(self.rows[self.ad(l)["row"]]["label"]) if self.ad(l)["row"] else "unclear"}<br>'
                f'<span class="num">from {fmt_date(self.ad(l)["start_date"], short=True)}</span></div>'
                for l in n["ad_ids"][:12])
            parts.append(f'<h3><span class="sw {k}"></span> {E(self.names[k])}: {n["n"]} of {self.c["meta"]["brands"][k]["n"]} '
                         f'sampled ads launched in the last {days} days</h3>'
                         f'<p class="small muted num">{E(by) or "none"}</p><div class="strip">{minis}</div>')
        months = sorted(set(self.c["launches"]["A"]) | set(self.c["launches"]["B"]))
        mx = max([v for k in "AB" for v in self.c["launches"][k].values()] or [1])
        rows = []
        for mth in months:
            bars = "".join(
                f'<div class="bar" title="{E(self.names[k])}: {self.c["launches"][k].get(mth, 0)} ads started in {fmt_month(mth)}">'
                f'<div class="track">{launch_fill(k, self.c["launches"][k].get(mth, 0), mx)}</div>'
                f'<span class="v num">{self.c["launches"][k].get(mth, 0)}</span></div>' for k in ("A", "B"))
            rows.append(f'<div class="brow"><div class="bl">{fmt_month(mth)}</div><div class="bars">{bars}</div></div>')
        sub = ("Ads still in the sample, by start month. Impressions add up over time, so older months are favoured." if self.by_impr
               else "Ads still in the sample, by start month. The sample follows the Library's default order, not impressions.")
        parts.append(f'<div class="chart" style="margin-top:18px"><h3>When the sampled ads started</h3>'
                     f'<p class="sub">{sub}</p>'
                     f'{self.legend()}{"".join(rows)}</div>')
        return self.section("now", "Now vs always", "What is new, and what has stayed", "".join(parts),
                            "Ads launched recently that already made a sample ranked by lifetime impressions are carrying real weight." if self.by_impr
                            else "Ads launched in the last 30 days, and the months the rest started. This sample is the Library's default order, "
                                 "so a recent ad here shows what the brand runs now, not what it pays most for.")

    def legend(self):
        return (f'<div class="legend"><span><i class="sw A"></i>{E(self.names["A"])}</span>'
                f'<span><i class="sw B"></i>{E(self.names["B"])}</span></div>')

    def paired_chart(self, title, sub, data, denom):
        allc = set(data["A"]) | set(data["B"])
        if len(allc) == 1:
            c = next(iter(allc))
            if all(data[k].get(c, 0) == denom[k] for k in "AB"):
                return (f'<div class="chart"><h3>{E(title)}</h3><p class="sub">{E(sub)}</p>'
                        f'<p class="small">Both brands: {E(nice(c))} for every sampled ad '
                        f'(<span class="num">{denom["A"]} of {denom["A"]} and {denom["B"]} of {denom["B"]}</span>).</p></div>')
        cats = []
        for k in ("A", "B"):
            for c in data[k]:
                if c not in cats:
                    cats.append(c)
        cats.sort(key=lambda c: -max(data["A"].get(c, 0) / max(denom["A"], 1), data["B"].get(c, 0) / max(denom["B"], 1)))
        rows = []
        for c in cats:
            bars = ""
            for k in ("A", "B"):
                v = data[k].get(c, 0)
                share = v / denom[k] if denom[k] else 0
                fill = f'<div class="fill {k}" style="width:{share * 100:.1f}%"></div>' if v else ""
                bars += (f'<div class="bar" title="{E(self.names[k])}: {v} of {denom[k]}">'
                         f'<div class="track">{fill}</div>'
                         f'<span class="v num">{v} of {denom[k]}</span></div>')
            rows.append(f'<div class="brow"><div class="bl">{E(nice(c)[:1].upper() + nice(c)[1:])}</div><div class="bars">{bars}</div></div>')
        return f'<div class="chart"><h3>{E(title)}</h3><p class="sub">{E(sub)}</p>{"".join(rows)}</div>'

    def mix_section(self):
        b = self.c["breakdowns"]
        mb = self.c["meta"]["brands"]
        tot = {k: mb[k]["n"] for k in "AB"}
        vid = {k: mb[k]["n_video"] for k in "AB"}
        imgn = {k: mb[k]["n_image"] for k in "AB"}
        parts = []
        for me in ("A", "B"):
            lines = self.p.get(me, {}).get("india_read") or []
            if lines:
                parts.append(f'<div class="india only-{me}"><div class="kicker">India read</div>'
                             + "".join(f"<p>{E(l)}</p>" for l in lines) + '</div>')
        parts.append(self.legend())
        charts = [
            self.paired_chart("How videos open", "First 3 seconds, share of each brand's sampled videos.",
                              {k: b["hook"][k]["video"] for k in "AB"}, vid),
            self.paired_chart("How image ads open", "Largest text, share of each brand's sampled image ads.",
                              {k: b["hook"][k]["image"] for k in "AB"}, imgn),
            self.paired_chart("Offers", "Only concrete incentives stated in the ad.", {k: b["offer"][k] for k in "AB"}, tot),
            self.paired_chart("Main reason to buy", "The first claim each ad makes.", {k: b["angle"][k] for k in "AB"}, tot),
            self.paired_chart("Who is on screen", "Founder only where the ad itself says so. Nobody is identified from a face.",
                              {k: b["face"][k] for k in "AB"}, tot),
            self.paired_chart("Language", "Spoken language, else on-screen text.", {k: b["language"][k] for k in "AB"}, tot),
            self.paired_chart("Where the button goes", "Read from the link and button only; pages were not opened.",
                              {k: b["destination"][k] for k in "AB"}, tot),
            self.paired_chart("How it is made", "Production level.", {k: b["production"][k] for k in "AB"}, tot),
        ]
        parts.append(f'<div class="charts">{"".join(charts)}</div>')
        ct = []
        if not any(b["campaign_tags"][k] for k in "AB") and not any(b["deadline"][k] for k in "AB"):
            parts.append('<p class="small muted" style="margin-top:22px">Neither brand puts campaign tags in its links, '
                         'and no sampled ad states a deadline.</p>')
            return self.section("mix", "Detail", "Hooks, offers and destination", "".join(parts))
        for k in "AB":
            tags = "".join(f'<span class="tag num">{E(t)} ({n})</span>' for t, n in b["campaign_tags"][k]) or '<span class="muted small">none in the links</span>'
            ct.append(f'<div><h4 style="margin:0;font:600 13px var(--sans);display:flex;gap:6px;align-items:center">'
                      f'<span class="sw {k}"></span>{E(self.names[k])}</h4><div class="tags">{tags}</div>'
                      f'<p class="small muted num" style="margin:6px 0 0">{b["deadline"][k]} of {tot[k]} ads state a deadline.</p></div>')
        parts.append(f'<div style="margin-top:26px"><h3 style="font:600 13.5px var(--sans)">Campaign tags in the links</h3>'
                     f'<p class="small muted" style="margin:2px 0 8px">The names each brand gives its campaigns, from the tracking tags in its links, with ad counts.</p>'
                     f'<div class="pair">{"".join(ct)}</div></div>')
        return self.section("mix", "Detail", "Hooks, offers and destination", "".join(parts))

    def pacing_section(self):
        pa = self.c["pacing"]
        def f(v, unit="", dp=0):
            return "n/a" if v is None else f"{round(v, dp):g}{unit}"
        rows = [("Distinct videos", "videos", "", 0), ("Length", "duration_s", " s", 0), ("Cuts per 10 seconds", "cuts_per_10s", "", 1),
                ("Words a minute", "wpm", "", 0), ("First cut at", "first_cut_s", " s", 1)]
        head = f'<tr><th></th><th class="n">{E(self.names["A"])}</th><th class="n">{E(self.names["B"])}</th></tr>'
        body = "".join(f'<tr><td>{lab}</td><td class="n">{f(pa["A"]["all"][key], u, dp)}</td>'
                       f'<td class="n">{f(pa["B"]["all"][key], u, dp)}</td></tr>' for lab, key, u, dp in rows)
        t1 = f'<div class="tablewrap"><table class="t">{head}{body}</table></div>'
        rws = []
        for r in self.c["rows"]:
            if r["medium"] != "video":
                continue
            ra, rb = pa["A"]["by_row"].get(r["id"]), pa["B"]["by_row"].get(r["id"])
            def cell(x):
                if not x or not x["videos"]:
                    return "n/a"
                return f'{plural(x["videos"], "video")}, {f(x["duration_s"], " s")}, {f(x["cuts_per_10s"], "", 1)} cuts, {f(x["wpm"])} words'
            rws.append(f'<tr><td>{E(r["label"])}</td><td>{cell(ra)}</td><td>{cell(rb)}</td></tr>')
        t2 = (f'<h3 style="margin-top:20px;font:600 13.5px var(--sans)">By row (medians: length, cuts per 10 s, words a minute)</h3>'
              f'<div class="tablewrap"><table class="t"><tr><th>Row</th><th>{E(self.names["A"])}</th><th>{E(self.names["B"])}</th></tr>'
              f'{"".join(rws)}</table></div>')
        return self.section("pacing", "Craft", "Pacing", t1 + t2,
                            "Medians over distinct videos, not ads, so one video run in many versions counts once.")

    def standouts_section(self):
        rule = ("Rule: for each brand, its two video ideas with the highest leaning score"
                + (f" among its {self.flabel().lower()} ads" if self.flabel() else "") + " (see What they lean on)."
                if self.c.get("lean") else
                "Rule: for each brand, its two rows where its share is furthest above the other brand's "
                "(at least one video row when it has one), and in each row the idea with the most days live, ties broken by versions.")
        parts = [f'<p class="lede prose">{E(rule)}</p>']
        for k in ("A", "B"):
            parts.append(f'<h3 style="margin:18px 0 6px;display:flex;gap:8px;align-items:center"><span class="sw {k}"></span>{E(self.names[k])}</h3>')
            for i, s in enumerate(self.c["standouts"][k]):
                a = self.ad(s["ad_id"])
                head = (f'<div class="kicker">{E(self.rows[s["row"]]["label"])}</div>'
                        f'<h3>&ldquo;{E(a["hook_text"] or a["headline"])}&rdquo;</h3><p class="why">{E(self.why(k, s, i))} '
                        f'<a href="{E(a["link"])}" target="_blank" rel="noopener">Open in Ad Library</a></p>')
                if a["medium"] == "video":
                    fr = []
                    for f in thin_frames(s["frames"]):
                        sp = "" if f.get("spoken_repeat") else f["spoken"]
                        fr.append(f'<div class="frame">{img_tag(self.img.uri(k, f["still"], 240), "Frame")}'
                                  f'<div class="tc">{f["t"]:g} s</div><div class="sp q">{E(sp)}</div></div>')
                    body = f'<div class="frames">{"".join(fr)}</div>'
                    if a["transcript"]:
                        body += f'<details style="margin-top:10px"><summary class="small">Full script</summary><p class="txt q small" style="white-space:pre-wrap">{E(a["transcript"])}</p></details>'
                else:
                    body = (f'<div class="single">{img_tag(self.img.uri(k, a["still"], 480), "The ad")}'
                            f'<div><p class="q" style="margin:0 0 6px"><b>{E(a["headline"])}</b></p>'
                            f'<p class="q small" style="white-space:pre-wrap;margin:0">{E(a["body"])}</p></div></div>')
                parts.append(f'<div class="standout">{head}{body}</div>')
        return self.section("standouts", "Craft", "Standouts, frame by frame", "".join(parts))

    def why(self, k, s, i):
        """Selection reason built from the rows, so it never claims a lead the numbers do not show."""
        if s.get("score") is not None:
            a = self.ad(s["ad_id"])
            g = self.lean_group(k, "idea", s["idea"]) or {}
            scope = f' {self.flabel().lower()}' if self.flabel() else ""
            return (f'{"Its highest" if i == 0 else "Its second highest"}-scoring{scope} video idea by leaning score ({s["score"]}): '
                    f'{plural(g.get("n", 1), "ad")}, {plural(g.get("versions", a["versions"]), "version")}, longest {g.get("longest_days", a["days"])} days live.')
        r = self.rows[s["row"]]
        th = self.other(k)
        mine, theirs = r[k]["share"], r[th]["share"]
        a = self.ad(s["ad_id"])
        def fig(x):
            N = self.nmed(x, r["medium"])
            small = min(self.nmed("A", r["medium"]), self.nmed("B", r["medium"])) < SMALL_BASE
            return f'{r[x]["n"]} of {N}' if small else pct(r[x]["share"])
        pair = f'{fig(k)} against {fig(th)}'
        nth = "widest" if i == 0 else "second widest"
        if mine > theirs:
            lead = f'{r["label"]} is {self.names[k]}\'s {nth} gap over {self.names[th]} ({pair}).'
        else:
            lead = (f'{r["label"]} is {self.names[k]}\'s other present row; here it trails {self.names[th]} '
                    f'({pair}).')
        return (f'{lead} This is the idea in that row with the most days live '
                f'({a["days"]} days, {plural(a["versions"], "version")}).')

    def rerun_section(self):
        rr = self.c.get("rerun")
        if not rr:
            return ""
        parts = []
        for k in ("A", "B"):
            x = rr[k]
            rows = "".join(
                f'<tr><td>{E(self.rows[r]["label"]) if r in self.rows else "unclear"}</td>'
                f'<td class="n">{x["kept_by_row"].get(r, 0)}</td><td class="n">{x["gone_by_row"].get(r, 0)}</td>'
                f'<td class="n">{x["new_by_row"].get(r, 0)}</td></tr>' for r in list(self.rows) + ["unclear"]
                if any(x[f"{s}_by_row"].get(r) for s in ("kept", "gone", "new")))
            parts.append(f'<h3 style="margin:14px 0 6px">{E(self.names[k])}, since {fmt_date(x["previous_snapshot"])}</h3>'
                         f'<p class="small muted num">Ideas: {x["ideas"]["kept"]} kept, {x["ideas"]["gone"]} gone, {x["ideas"]["new"]} new.</p>'
                         f'<div class="tablewrap"><table class="t"><tr><th>Row</th><th class="n">Kept</th><th class="n">Gone</th>'
                         f'<th class="n">New</th></tr>{rows}</table></div>')
        return self.section("rerun", "Thirty days on", "Kept, gone, new", "".join(parts),
                            "Gone means stopped, or fell out of the top by impressions; the Library sample cannot tell which.")

    def shares_line(self):
        mb = self.c["meta"]["brands"]
        if not self.by_impr:
            return ("<b>Shares.</b> Video rows are shares of a brand's sampled video ads, image rows of its sampled image ads. "
                    "The views were taken in the Library's default order, so the video and image split is whatever those views returned; "
                    f"a medium with under {SMALL_BASE} ads on a side shows counts, not shares, and a side with none reads \"none\".")
        base = "<b>Shares.</b> Video rows are shares of a brand's sampled video ads, image rows of its sampled image ads. "
        only_top = [k for k in "AB" if mb[k].get("top30_all") and mb[k]["n_image"] <= mb[k]["top30_all"]["image"]]
        if only_top:
            who = " and ".join(E(self.names[k]) for k in only_top)
            return (base + f"No extra image ads were collected for {who}: its image ads are only those inside its top 30, "
                    f"so image rows on a small base say more about whether a brand runs image ads than which kind. "
                    f"Image rows with under {SMALL_BASE} ads on a side show counts, not shares.")
        return (base + "The sample gives video and image a guaranteed look each, so the video and image split of the sample is "
                "not the brand's real split; the overall lean comes only from its top 30 across both.")

    def method_section(self):
        m = self.c["meta"]
        th = m["thresholds"]
        lines = [f"<b>Sample.</b> {E(m['sample_rule'])}",
                 f"<b>Snapshot.</b> {fmt_date(m['snapshot_date'])}. Ads live on that day only."]
        for k in "AB":
            b = m["brands"][k]
            unc = b["unclear"]["video"] + b["unclear"]["image"]
            lines.append(f"<b>{E(self.names[k])}.</b> {b['n']} ads: {b['n_video']} video ({b['unique_videos']} distinct videos), "
                         f"{b['n_image']} image. {unc} could not be placed in a row; they count in the totals but in no row.")
        lines += [
            "<b>No spend or results.</b> The Ad Library does not publish spend, reach or results for these ads. " +
            ("We use what is public: whether the Library ranks an ad highest by impressions, how long it has run, and how many versions run."
             if self.by_impr else
             "We use what is public: which ads the Library shows first, how long each has run, and how many versions run. "
             "The default order is the Library's own and is not documented, so it is not a ranking by impressions or spend."),
            self.shares_line(),
            "<b>Days live</b> are days so far: ads still running are counted to the snapshot date.",
            "<b>Versions</b> are the Library's count of ads that share a creative. Mixed-format set-ups, where Meta combines images, videos and text, "
            "inflate it, so we lean on ideas, not versions.",
            f"<b>Status rules.</b> A brand is present in a row at {th['present']} ads. Only: one side present. "
            f"Leads: both present and a share at least {th['lead_ratio']} times the other's. Even: both present, under that. "
            f"Evidence is strong at {th['strong_ads']} ads across {th['strong_ideas']} ideas, thin under {th['thin_ads']} ads or a single idea, "
            "moderate otherwise.",
            "<b>Founders.</b> Counted only where the ad itself says founder, co-founder or CEO. Nobody is identified from a face.",
        ]
        tc = m.get("tag_check") or {}
        for k in "AB":
            c = tc.get(k)
            if c:
                ag = ", ".join(f"{('idea' if f == 'concept_id' else f)} {round(v * 100)}%" for f, v in c["agreement"].items())
                lines.append(f"<b>Tag check, {E(self.names[k])}.</b> {c['n_checked']} ads tagged twice, once by hand: agreement {ag}.")
            else:
                lines.append(f"<b>Tag check, {E(self.names[k])}.</b> Not done yet.")
        lines.append("<b>Scripts</b> are typed by software and can mishear names and non-English words.")
        return self.section("method", "Method", "Method and limits",
                            '<ul class="facts prose">' + "".join(f"<li>{l}</li>" for l in lines) + "</ul>")

    def appendix(self):
        parts = []
        for k in ("A", "B"):
            ids = sorted((l for l, a in self.c["ads"].items() if a["brand"] == k),
                         key=lambda l: (self.ad(l)["medium"], self.ad(l)["row"] or "Z", -(self.ad(l)["days"] or 0)))
            items = []
            for l in ids:
                a = self.ad(l)
                t = a["tags"]
                row = self.rows[a["row"]]["label"] if a["row"] else "unclear"
                meta = (f'{a["medium"].title()} ad, {row.lower() if a["row"] else row}. {a["days"]} days live from '
                        f'{fmt_date(a["start_date"], short=True)}, {plural(a["versions"], "version")}. '
                        f'Opens with: {nice(t.get("hook"))}. Offer: {nice(t.get("offer"))}. On screen: {nice(t.get("face"))}. '
                        f'Language: {nice(t.get("language"))}. Button goes to: {nice(a["destination"])}.')
                text = "\n\n".join(x for x in (a["headline"], a["body"]) if x)
                more = f'<details><summary>Ad text{" and script" if a["transcript"] else ""}</summary><p class="txt q">{E(text)}'
                if a["transcript"]:
                    more += f'\n\nScript: {E(a["transcript"])}'
                more += f'</p></details>'
                items.append(f'<div class="ad">{img_tag(self.img.uri(k, a["still"], 160), "Still", "" if a["medium"] == "video" else "fit")}<div>'
                             f'<div class="h q">&ldquo;{E(a["hook_text"] or a["headline"])}&rdquo;</div>'
                             f'<div class="m num">{E(meta)} <a href="{E(a["link"])}" target="_blank" rel="noopener">Ad Library</a></div>'
                             f'{more}</div></div>')
            parts.append(f'<details class="fold"><summary><span class="sumlabel">{E(self.names[k])}</span>'
                         f'<span class="sumstat num">{len(ids)} ads</span></summary><div class="adlist">{"".join(items)}</div></details>')
        return self.section("appendix", "Appendix", "Every ad", "".join(parts))

    def build(self):
        if self.v4 and not self.c.get("focus"):
            body = [self.first_screen(), self.lean_section(), self.whole_map_section(), self.products_section(),
                    self.comparable_section(), self.folds(), self.scripts_section(), self.disagree_section(),
                    self.lead_section(), self.stakes_section(), self.now_section(), self.mix_section(), self.pacing_section(),
                    self.standouts_section(), self.rerun_section(), self.method_section(), self.appendix(),
                    f'<footer class="wrap">Built from the public Meta Ad Library on {fmt_date(self.c["meta"]["snapshot_date"])}. '
                    f'Rules version {E(self.c["meta"]["rules_version"])}.</footer>']
            return "\n".join(body)
        if self.c.get("focus"):
            body = [self.first_screen(), self.lean_section(), self.focus_map_section(), self.folds(), self.products_section(),
                    self.scripts_section(), self.disagree_section(), self.lead_section(), self.stakes_section(), self.now_section(),
                    self.mix_section(), self.pacing_section(), self.standouts_section(), self.rerun_section(),
                    self.method_section(), self.appendix(),
                    f'<footer class="wrap">Built from the public Meta Ad Library on {fmt_date(self.c["meta"]["snapshot_date"])}. '
                    f'Rules version {E(self.c["meta"]["rules_version"])}.</footer>']
            return "\n".join(body)
        body = [self.first_screen(), self.extras_section(), self.folds(), self.lead_section(), self.stakes_section(), self.now_section(),
                self.mix_section(), self.pacing_section(), self.standouts_section(), self.rerun_section(),
                self.method_section(), self.appendix(),
                f'<footer class="wrap">Built from the public Meta Ad Library on {fmt_date(self.c["meta"]["snapshot_date"])}. '
                f'Rules version {E(self.c["meta"]["rules_version"])}.</footer>']
        return "\n".join(body)


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def fmt_date(s, short=False):
    if not s:
        return "unknown"
    y, m, d = s.split("-")
    mon = MONTHS[int(m) - 1]
    return f"{int(d)} {mon[:3]}" if short else f"{int(d)} {mon} {y}"


def fmt_month(s):
    y, m = s.split("-")
    return f"{MONTHS[int(m) - 1][:3]} {y}"


def lint(html_text, persp, comp=None):
    issues = []
    rows = {r["id"]: r for r in (comp or {}).get("rows", [])}
    persp = {k: v for k, v in persp.items() if k in ("A", "B")}
    for k, p in persp.items():
        for mv in p.get("moves", []):
            r = rows.get(mv.get("row"))
            if not r:
                issues.append(f"move {k}{mv.get('rank')} names unknown row {mv.get('row')}")
            elif r["evidence"] != mv.get("evidence"):
                issues.append(f"move {k}{mv.get('rank')} says evidence {mv.get('evidence')} but row {r['id']} is {r['evidence']}")
    # visible text only, without quoted ad content (class q) and without attributes
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html_text, flags=re.S)
    t = re.sub(r'<(\w+)[^>]*class="[^"]*\bq\b[^"]*"[^>]*>.*?</\1>', " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    for w in BANNED:
        for m in re.finditer(rf"(?<![\w-]){re.escape(w)}(?![\w-])", t, flags=re.I):
            issues.append(f"banned word '{w}': ...{t[max(0, m.start() - 40):m.end() + 40].strip()}...")
    for m in re.finditer(r"\btop\b(?! \d| by)", t, flags=re.I):
        issues.append(f"'top' without 'top 30' or 'top by': ...{t[max(0, m.start() - 40):m.end() + 40].strip()}...")
    for w in JARGON:
        for m in re.finditer(rf"\b{re.escape(w)}", t, flags=re.I if w.islower() else 0):
            issues.append(f"jargon '{w}': ...{t[max(0, m.start() - 40):m.end() + 40].strip()}...")
    if "\u2014" in html_text or "\u2013" in html_text:
        issues.append("em or en dash present")
    for k, p in persp.items():
        n = len(p.get("verdict", "").split())
        if n > 30:
            issues.append(f"verdict {k} is {n} words (max 30)")
        if p.get("plan"):
            issues += lint_plan(k, p)
            continue
        moves = p.get("moves", [])
        if not 2 <= len(moves) <= 4:
            issues.append(f"perspective {k} has {len(moves)} moves (2 to 4)")
        for mv in moves:
            if len(mv["text"].split()) > 35:
                issues.append(f"move {k}{mv.get('rank')} text over 35 words")
            if len(mv["first_test"].split()) > 25:
                issues.append(f"move {k}{mv.get('rank')} first test over 25 words")
        if moves and sorted(moves, key=lambda m: m.get("rank", 9))[0].get("evidence") == "thin":
            issues.append(f"perspective {k}: move 1 rests on thin evidence")
    return issues


def words(t):
    return len((t or "").split())


def lint_plan(k, p):
    out = []
    pl = p["plan"]
    if not pl.get("focus"):
        out.append(f"plan {k}: no focus")
    elif pl["focus"].get("evidence") == "thin":
        out.append(f"plan {k}: focus rests on thin evidence")
    if not 2 <= len(pl.get("start", [])) <= 3:
        out.append(f"plan {k}: {len(pl.get('start', []))} start items (2 to 3)")
    if not 1 <= len(pl.get("stop", [])) <= 2:
        out.append(f"plan {k}: {len(pl.get('stop', []))} stop items (1 to 2)")
    for it in [pl.get("focus") or {}] + pl.get("start", []) + pl.get("stop", []):
        t = it.get("title", "")
        if words(t) > 14:
            out.append(f"plan {k}: title over 14 words: {t}")
        if words(it.get("why")) > 40:
            out.append(f"plan {k}: why over 40 words: {t}")
        if words(it.get("first_test")) > 25:
            out.append(f"plan {k}: first test over 25 words: {t}")
        if not it.get("first_test"):
            out.append(f"plan {k}: no first test: {t}")
    ds = p.get("scripts") or []
    if not 4 <= len(ds) <= 6:
        out.append(f"scripts {k}: {len(ds)} directions (4 to 6)")
    for d in ds:
        t = d.get("title", "")
        if words(t) > 20:
            out.append(f"script {k}: title over 20 words: {t}")
        for f in ("persona", "why", "format", "length", "on_screen", "end_card"):
            if not d.get(f):
                out.append(f"script {k}: '{t}' lacks {f}")
        if len(d.get("openings", [])) < 2:
            out.append(f"script {k}: '{t}' needs 2 or more opening lines")
        if len(d.get("beats", [])) < 5:
            out.append(f"script {k}: '{t}' needs 5 or more beats")
        if not d.get("compliance") or not d.get("measure"):
            out.append(f"script {k}: '{t}' lacks compliance or measures")
        rows = d.get("script", [])
        end = None
        if rows:
            m = re.search(r"(\d+)\s*s\s*$", rows[-1].get("t", ""))
            end = int(m.group(1)) if m else None
        if end is None or not 30 <= end <= 45:
            out.append(f"script {k}: '{t}' full script runs {end} s (30 to 45)")
        if re.search(r"\bfounder\b", t + d.get("format", ""), re.I) and not d.get("label"):
            out.append(f"script {k}: '{t}' is founder-led but not labelled a recommendation")
    return out


def main():
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    comp = json.loads(Path(sys.argv[1]).read_text())
    persp = json.loads(Path(sys.argv[2]).read_text())
    dirs = {"A": sys.argv[3], "B": sys.argv[4]}
    out = Path(sys.argv[5])
    out.mkdir(parents=True, exist_ok=True)
    page = Page(comp, persp, dirs)
    body = page.build()
    names = page.names
    title = f"{names['A']} vs {names['B']}"
    if len(title.split()) > 4:
        wa, wb = names["A"].split(), names["B"].split()
        if wa[0] == wb[0] and len(wb) > 1:      # "Brand A vs B"
            title = f"{names['A']} vs {' '.join(wb[1:])}"
        if len(title.split()) > 4 or wa[0] != wb[0]:
            title = f"{wa[0]} vs {wb[0]}"
    desc = (f"Head-to-head of the live Meta ads of {names['A']} and {names['B']}: where each is missing out in video "
            f"and image ads, and what to test next.")
    tpl = (HERE / "template.html").read_text()
    doc = tpl.replace("{{TITLE}}", E(title)).replace("{{DESCRIPTION}}", E(desc)).replace("{{BODY}}", body)
    doc = doc.replace('\ufffd', '')
    doc = doc.replace('\u2014', ' - ').replace('\u2013', '-')  # quoted ad text often carries long dashes
    (out / "index.html").write_text(doc)
    size = len(doc.encode())
    print(f"wrote {out / 'index.html'}: {size / 1e6:.2f} MB ({page.img.bytes / 1e6:.2f} MB images)")
    issues = lint(doc, persp, comp) + page.plan_issues()
    print(f"lint: {len(issues)} issue(s)")
    for i in issues:
        print("  -", i)


if __name__ == "__main__":
    main()
