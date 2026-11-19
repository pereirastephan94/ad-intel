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


def img_tag(uri, alt, cls=""):
    """cls "fit" shows the whole image (static ads); default crops to fill (video stills)."""
    if not uri:
        return f'<div class="{cls}" role="img" aria-label="no still" style="aspect-ratio:4/5;background:var(--line-2)"></div>'
    return f'<img src="{uri}" alt="{E(alt)}" decoding="async"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'


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

    # ---------- helpers
    def other(self, k):
        return "B" if k == "A" else "A"

    def ad(self, lid):
        return self.c["ads"][lid]

    def nmed(self, k, medium):
        return self.c["meta"]["brands"][k][f"n_{medium}"]

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
  the ones the Ad Library ranks highest by impressions. <b>No spend or results are public.</b></p>
  <div class="controls"><div class="seg" role="group" aria-label="Read this page as">
    <button type="button" data-set-me="A" aria-pressed="true">I am {E(self.names['A'])}</button>
    <button type="button" data-set-me="B" aria-pressed="false">I am {E(self.names['B'])}</button></div>
  <button class="theme" type="button" data-theme-toggle aria-label="Switch colour theme">Theme</button></div>
</header>"""

    def verdict_and_moves(self, me):
        p = self.p.get(me, {})
        out = [f'<div class="only-{me}">']
        out.append(f'<p class="verdict">{E(p.get("verdict", "Verdict not written yet."))}</p>')
        out.append('<ol class="moves">')
        for mv in sorted(p.get("moves", []), key=lambda m: m.get("rank", 9)):
            ev = mv.get("evidence", "thin")
            out.append(f'<li>{E(mv["text"])} <span class="test"><b>First test:</b> {E(mv["first_test"])}</span>'
                       f'<span class="chips"><span class="chip">Effort {E(mv["effort"])}</span>'
                       f'<span class="chip ev-{E(ev)}">Evidence {E(ev)}</span>'
                       f'<a class="chip seeads" href="#row-{E(mv["row"])}" data-fold="row-{E(mv["row"])}">See the ads</a></span></li>')
        out.append('</ol>')
        out.append('</div>')
        return "".join(out)

    def map(self, me):
        th = self.other(me)
        out = [f'<div class="map only-{me}" aria-label="Gap map">']
        out.append(f'<div class="mhead"><div></div><div class="who">{E(self.names[me])}<br><span class="muted">you</span></div>'
                   f'<div class="who">{E(self.names[th])}<br><span class="muted">them</span></div><div>Status<br>evidence</div></div>')
        for medium, title in (("video", "Video"), ("image", "Image")):
            out.append(f'<div class="mgroup"><span>{title}</span><span class="num">you {self.nmed(me, medium)}, '
                       f'them {self.nmed(th, medium)} sampled</span></div>')
            for r in self.c["rows"]:
                if r["medium"] != medium:
                    continue
                cells = []
                for k in (me, th):
                    s = r[k]
                    d = f'{s["median_days"]:.0f}d' if s["median_days"] is not None else "0d"
                    cells.append(f'<div class="cell {k} {heat(s["share"])}"><span class="pct num">{pct(s["share"])}</span>'
                                 f'<span class="sub num">{s["n"]} ad{"" if s["n"] == 1 else "s"}, {d}</span></div>')
                lead = r["lead"] or ""
                out.append(f'<a class="mrow" href="#row-{r["id"]}" data-fold="row-{r["id"]}"'
                           f' title="{E(r["label"])}: open the evidence">'
                           f'<div class="mlabel">{E(r["label"])}</div>{"".join(cells)}'
                           f'<div class="st lead-{lead}"><span class="s">{status_label(r, me)}</span>'
                           f'<span class="e">{r["evidence"]}</span></div></a>')
        fa = sum(r[me]["founder"] for r in self.c["rows"])
        fb = sum(r[th]["founder"] for r in self.c["rows"])
        where = [r["label"] for r in self.c["rows"] if r[th]["founder"] or r[me]["founder"]]
        out.append(f'<p class="founder num">Founder says so on screen: you {fa}, them {fb}'
                   f'{" (" + ", ".join(where) + ")" if where else ""}. Counted only where the ad itself says founder.</p>')
        t = self.c["meta"]["brands"]
        ta, tb = t[me]["top30_all"], t[self.other(me)]["top30_all"]
        if ta and tb:
            out.append(f'<p class="top30 num">In the overall top {max(ta["n"], tb["n"])} by impressions: you {ta["video"]} video, '
                       f'{ta["image"]} image; {E(self.names[self.other(me)])} {tb["video"]} video, {tb["image"]} image.</p>')
        else:
            out.append('<p class="top30">Overall video and image lean: not recorded for this sample.</p>')
        out.append('<p class="maplegend">Share is of each brand\'s sampled ads of that medium; "d" is median days live so far. '
                   'Tap a row for the ads.</p></div>')
        return "".join(out)

    def first_screen(self):
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
                stat = (f'{s["n"]} of {self.nmed(k, r["medium"])} {r["medium"]} ads ({pct(s["share"])}), '
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
                             f'{E(self.names[th])} {o["n"]} of {self.nmed(th, r["medium"])}. Evidence {r["evidence"]}.</span></li>')
            body = f'<ul class="facts">{"".join(items)}</ul>' if items else '<p>We found no row where you lead.</p>'
            out.append(f'<div class="only-{me}">{body}</div>')
        return self.section("lead", "Fair both ways", "Where you lead", "".join(out),
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
        return self.section("stakes", "Context", "Table stakes and open ground",
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
                f'<div class="track"><div class="fill {k}" style="width:{self.c["launches"][k].get(mth, 0) / mx * 100:.1f}%"></div></div>'
                f'<span class="v num">{self.c["launches"][k].get(mth, 0)}</span></div>' for k in ("A", "B"))
            rows.append(f'<div class="brow"><div class="bl">{fmt_month(mth)}</div><div class="bars">{bars}</div></div>')
        parts.append(f'<div class="chart" style="margin-top:18px"><h3>When the sampled ads started</h3>'
                     f'<p class="sub">Ads still in the sample, by start month. Impressions add up over time, so older months are favoured.</p>'
                     f'{self.legend()}{"".join(rows)}</div>')
        return self.section("now", "Now vs always", "What is new, and what has stayed", "".join(parts),
                            "Ads launched recently that already made a sample ranked by lifetime impressions are carrying real weight.")

    def legend(self):
        return (f'<div class="legend"><span><i class="sw A"></i>{E(self.names["A"])}</span>'
                f'<span><i class="sw B"></i>{E(self.names["B"])}</span></div>')

    def paired_chart(self, title, sub, data, denom):
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
                bars += (f'<div class="bar" title="{E(self.names[k])}: {v} of {denom[k]}">'
                         f'<div class="track"><div class="fill {k}" style="width:{share * 100:.1f}%"></div></div>'
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
        parts = ['<p class="lede prose">Rule: for each brand, its two rows where its share is furthest above the other brand\'s '
                 '(at least one video row when it has one), and in each row the idea with the most days live, ties broken by versions.</p>']
        for k in ("A", "B"):
            parts.append(f'<h3 style="margin:18px 0 6px;display:flex;gap:8px;align-items:center"><span class="sw {k}"></span>{E(self.names[k])}</h3>')
            for s in self.c["standouts"][k]:
                a = self.ad(s["ad_id"])
                head = (f'<div class="kicker">{E(self.rows[s["row"]]["label"])}</div>'
                        f'<h3>&ldquo;{E(a["hook_text"] or a["headline"])}&rdquo;</h3><p class="why">{E(s["why"])} '
                        f'<a href="{E(a["link"])}" target="_blank" rel="noopener">Open in Ad Library</a></p>')
                if a["medium"] == "video":
                    fr = []
                    for f in s["frames"]:
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
            "<b>No spend or results.</b> The Ad Library does not publish spend, reach or results for these ads. "
            "We use what is public: whether the Library ranks an ad highest by impressions, how long it has run, and how many versions run.",
            "<b>Shares.</b> Video rows are shares of a brand's sampled video ads, image rows of its sampled image ads. "
            "The sample gives video and image a guaranteed look each, so the video and image split of the sample is not the brand's real split; "
            "the overall lean comes only from its top 30 across both.",
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
        body = [self.first_screen(), self.folds(), self.lead_section(), self.stakes_section(), self.now_section(),
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
    issues = lint(doc, persp, comp)
    print(f"lint: {len(issues)} issue(s)")
    for i in issues:
        print("  -", i)


if __name__ == "__main__":
    main()
