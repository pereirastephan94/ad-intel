#!/usr/bin/env python3
"""Compute the head-to-head comparison data for two brands.

Usage:
  compute.py <research_dir_A> <research_dir_B> <out.json> [--snapshot YYYY-MM-DD] [--country IN] [--previous old.json]

Reads per brand: ads.json, videos/<asset>/tags.json, videos/<asset>/metrics.json,
videos/<asset>/transcript.json, statics/<library_id>.tags.json, optional tag_check.json.
Writes everything the page needs except the verdict and moves (perspectives.json).
Rules are in ../COMPARE_SPEC.md; keep the two in step.
"""
import argparse
import datetime as dt
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROWS = [
    ("V1", "Person to camera", "video"),
    ("V2", "Scene or story", "video"),
    ("V3", "Product or app demo", "video"),
    ("V4", "Text and motion", "video"),
    ("I1", "Offer-led", "image"),
    ("I2", "Product or people", "image"),
    ("I3", "Proof", "image"),
]
ROW_IDS = {r[0] for r in ROWS}
PRESENT = 3          # ads needed for a brand to be present in a row
LEAD_RATIO = 2       # share ratio for "Nx"
STRONG_ADS, STRONG_IDEAS = 8, 3
THIN_ADS = 4         # under this, or a single idea, is thin
NOW_DAYS = 30
SAMPLE_RULE = ("Per brand, three Ad Library views, each sorted by the Library's total impressions, high to low: "
               "all ads, video only and image only, about 30 each, overlapping. The sample is the ads the Library "
               "ranks highest by impressions, with video and image each guaranteed a look.")


def load_json(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def median(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 2) if xs else None


def destination(url, cta):
    if not url:
        return "lead_form" if (cta or "").lower() in ("sign up", "get quote", "apply now", "subscribe") else "other"
    host = (urlparse(url).netloc or "").lower()
    if any(h in host for h in ("play.google.com", "apps.apple.com", "itunes.apple.com", "onelink.me",
                               "app.link", "adj.st", "adjust.com", "appsflyer", "branch.io")):
        return "app"
    if any(h in host for h in ("wa.me", "whatsapp.com")):
        return "whatsapp"
    if "facebook.com" in host or "fb.me" in host:
        return "lead_form"
    return "web"


def campaign_tag(url):
    if not url:
        return None
    q = parse_qs(urlparse(url).query)
    v = (q.get("utm_campaign") or [None])[0]
    return v or None


def still_files(vdir):
    return sorted(p.name for p in vdir.glob("still*.jpg"))


def pick_still(vdir, transcript):
    """The opening still at about 1 second, else the first."""
    files = still_files(vdir)
    if not files:
        return None
    stills = (transcript or {}).get("stills") or []
    for i, s in enumerate(stills):
        if s.get("t", 0) >= 1 and i < len(files):
            return files[i]
    return files[min(1, len(files) - 1)]


def first_line(transcript):
    segs = ((transcript or {}).get("transcript") or {}).get("segments") or []
    return segs[0]["text"].strip() if segs else ""


def load_brand(rdir, key):
    rdir = Path(rdir)
    ads = load_json(rdir / "ads.json", {})
    if not ads:
        sys.exit(f"no ads.json in {rdir}")
    out = {}
    unique_videos = {}
    for lid, a in ads.items():
        asset = a.get("video_asset")
        medium = "video" if (a.get("media_type") == "VIDEO" or asset) else "image"
        tags, tagging, metrics, transcript, still = {}, {}, None, None, None
        if medium == "video" and asset:
            vdir = rdir / "videos" / asset
            tf = load_json(vdir / "tags.json", {}) or {}
            metrics = load_json(vdir / "metrics.json")
            transcript = load_json(vdir / "transcript.json")
            s = pick_still(vdir, transcript)
            still = f"videos/{asset}/{s}" if s else None
            unique_videos[asset] = metrics
        else:
            tf = load_json(rdir / "statics" / f"{lid}.tags.json", {}) or {}
            for ext in ("jpg", "png", "webp"):
                if (rdir / "images" / f"{lid}.{ext}").exists():
                    still = f"images/{lid}.{ext}"
                    break
        tags = tf.get("tags", {}) or {}
        tagging = tf.get("tagging", {}) or {}
        row = tags.get("row")
        if row not in ROW_IDS or (row[0] == "V") != (medium == "video"):
            row = None
        hook_text = tags.get("hook_text") or first_line(transcript) or a.get("headline") or ""
        out[lid] = {
            "brand": key, "medium": medium, "row": row, "tags": tags, "tagging": tagging,
            "days": a.get("days_running"), "versions": a.get("copies") or 1,
            "start_date": a.get("start_date"), "link": a.get("link"), "still": still,
            "hook_text": hook_text, "headline": a.get("headline") or "", "body": a.get("body") or "",
            "link_description": a.get("link_description") or "", "cta": a.get("cta") or "",
            "destination": destination(a.get("landing_url"), a.get("cta")),
            "campaign_tag": campaign_tag(a.get("landing_url")),
            "transcript": (((transcript or {}).get("transcript")) or {}).get("text", ""),
            "asset": asset, "metrics": metrics, "sample_views": a.get("sample_views"),
            "page_name": a.get("page_name"),
        }
    return out, unique_videos, load_json(rdir / "tag_check.json")


def row_stats(ads, rid, n_medium):
    sel = [a for a in ads.values() if a["row"] == rid]
    ideas = {a["tags"].get("concept_id") or f"solo-{id(a)}" for a in sel}
    return {
        "n": len(sel),
        "share": round(len(sel) / n_medium, 4) if n_medium else 0,
        "ideas": len(ideas),
        "median_days": median([a["days"] for a in sel]),
        "versions": sum(a["versions"] for a in sel),
        "founder": sum(1 for a in sel if a["tags"].get("face") == "founder_declared"),
        "ad_ids": [k for k, _ in sorted(((k, a) for k, a in ads.items() if a["row"] == rid),
                                       key=lambda kv: (-(kv[1]["days"] or 0), -kv[1]["versions"]))],
    }


def status_for(a, b):
    pa, pb = a["n"] >= PRESENT, b["n"] >= PRESENT
    if pa and pb:
        hi, lo, lead = (a, b, "A") if a["share"] >= b["share"] else (b, a, "B")
        ratio = hi["share"] / lo["share"] if lo["share"] else None
        if ratio and ratio >= LEAD_RATIO:
            return f"{lead}_lead", lead, int(ratio)
        return "even", None, round(ratio, 2) if ratio else None
    if pa:
        return "only_A", "A", None
    if pb:
        return "only_B", "B", None
    return "neither", None, None


def evidence_for(a, b):
    side = a if a["n"] >= b["n"] else b
    if side["n"] >= STRONG_ADS and side["ideas"] >= STRONG_IDEAS:
        return "strong"
    if side["n"] < THIN_ADS or side["ideas"] <= 1:
        return "thin"
    return "moderate"


def cards_for(ads, ad_ids, k=2):
    seen, out = set(), []
    for lid in ad_ids:
        idea = ads[lid]["tags"].get("concept_id") or lid
        if idea in seen:
            continue
        seen.add(idea)
        out.append(lid)
        if len(out) == k:
            break
    return out


def counter_by(ads, field, split_medium=False):
    if split_medium:
        res = {"video": Counter(), "image": Counter()}
        for a in ads.values():
            v = a["tags"].get(field)
            if v:
                res[a["medium"]][v] += 1
        return {m: dict(c.most_common()) for m, c in res.items()}
    c = Counter()
    for a in ads.values():
        v = a["tags"].get(field) if field not in ("destination",) else a[field]
        if v:
            c[v] += 1
    return dict(c.most_common())


def pacing(ads, unique_videos):
    def agg(assets):
        ms = [unique_videos[x] for x in assets if unique_videos.get(x)]
        return {
            "videos": len(ms),
            "duration_s": median([m.get("duration_s") for m in ms]),
            "cuts_per_10s": median([m.get("cuts_per_10s") for m in ms]),
            "wpm": median([m.get("words_per_min") for m in ms if m.get("has_audio", True)]),
            "first_cut_s": median([m.get("first_cut_s") for m in ms]),
        }
    by_row = defaultdict(set)
    for a in ads.values():
        if a["asset"] and a["row"]:
            by_row[a["row"]].add(a["asset"])
    return {"all": agg(set(unique_videos)), "by_row": {r: agg(s) for r, s in sorted(by_row.items())}}


def frames_for(rdir, ad):
    if not ad["asset"]:
        return [{"t": None, "still": ad["still"], "spoken": ""}]
    vdir = Path(rdir) / "videos" / ad["asset"]
    files = still_files(vdir)
    tr = load_json(vdir / "transcript.json", {}) or {}
    stills = tr.get("stills") or []
    segs = (tr.get("transcript") or {}).get("segments") or []
    frames = []
    for i, f in enumerate(files):
        t = stills[i]["t"] if i < len(stills) else None
        if t is None:
            m = re.search(r"_([\d.]+)s\.jpg$", f)
            t = float(m.group(1)) if m else None
        spoken = ""
        if t is not None:
            for s in segs:
                if s["start"] <= t < s["end"]:
                    spoken = s["text"].strip()
                    break
        frames.append({"t": t, "still": f"videos/{ad['asset']}/{f}", "spoken": spoken})
    # drop repeated spoken lines on consecutive frames for readability
    for i in range(1, len(frames)):
        if frames[i]["spoken"] and frames[i]["spoken"] == frames[i - 1]["spoken"]:
            frames[i]["spoken_repeat"] = True
    return frames


def standouts(key, other, rows, ads, rdir, k=2):
    cand = []
    for r in rows:
        me, them = r[key], r[other]
        if me["n"] < PRESENT:
            continue
        cand.append((me["share"] - them["share"], r["medium"] == "video", r))
    cand.sort(key=lambda c: -c[0])
    chosen = cand[:k]
    if chosen and not any(c[1] for c in chosen):
        vids = [c for c in cand if c[1]]
        if vids:
            chosen = chosen[:k - 1] + [vids[0]]
    out = []
    for diff, _, r in chosen:
        lid = r[key]["ad_ids"][0]
        a = ads[lid]
        out.append({
            "ad_id": lid, "row": r["id"], "idea": a["tags"].get("concept_id"),
            "why": (f"{r['label']} is where this brand differs most from the other "
                    f"({round(r[key]['share'] * 100)}% against {round(r[other]['share'] * 100)}%); "
                    f"this is the idea in that row with the most days live ({a['days']} days, {a['versions']} versions)."),
            "frames": frames_for(rdir, a),
        })
    return out


def snapshot_of(ads):
    c = Counter()
    for a in ads.values():
        if a["start_date"] and a["days"] is not None:
            d = dt.date.fromisoformat(a["start_date"]) + dt.timedelta(days=a["days"])
            c[d.isoformat()] += 1
    return c.most_common(1)[0][0] if c else dt.date.today().isoformat()


def rerun_diff(prev, ads_all):
    out = {}
    for key in ("A", "B"):
        old = {k for k, a in prev.get("ads", {}).items() if a["brand"] == key}
        new = {k for k, a in ads_all.items() if a["brand"] == key}
        def by_row(ids, src):
            c = Counter(src[i]["row"] or "unclear" for i in ids)
            return dict(c)
        old_ideas = {a["tags"].get("concept_id") for k, a in prev["ads"].items() if a["brand"] == key}
        new_ideas = {a["tags"].get("concept_id") for k, a in ads_all.items() if a["brand"] == key}
        out[key] = {
            "previous_snapshot": prev["meta"]["snapshot_date"],
            "kept": sorted(old & new), "gone": sorted(old - new), "new": sorted(new - old),
            "kept_by_row": by_row(old & new, ads_all), "gone_by_row": by_row(old - new, prev["ads"]),
            "new_by_row": by_row(new - old, ads_all),
            "ideas": {"kept": len(old_ideas & new_ideas), "gone": len(old_ideas - new_ideas),
                      "new": len(new_ideas - old_ideas)},
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir_a")
    ap.add_argument("dir_b")
    ap.add_argument("out")
    ap.add_argument("--snapshot")
    ap.add_argument("--country", default="IN")
    ap.add_argument("--previous")
    args = ap.parse_args()

    brands, ads_all, uv, checks = {}, {}, {}, {}
    for key, d in (("A", args.dir_a), ("B", args.dir_b)):
        ads, unique_videos, check = load_brand(d, key)
        brands[key] = ads
        uv[key] = unique_videos
        checks[key] = check
        ads_all.update(ads)

    snapshot = args.snapshot or snapshot_of(ads_all)
    snap_date = dt.date.fromisoformat(snapshot)

    meta_brands = {}
    for key, d in (("A", args.dir_a), ("B", args.dir_b)):
        ads = brands[key]
        page = load_json(Path(d) / "page.json", {}) or {}
        name = page.get("name") or next((a["page_name"] for a in ads.values() if a.get("page_name")), key)
        nv = sum(1 for a in ads.values() if a["medium"] == "video")
        ni = len(ads) - nv
        top = [a for a in ads.values() if a["sample_views"] and a["sample_views"].get("all")]
        top30 = None
        if top:
            top = sorted(top, key=lambda a: a["sample_views"]["all"])[:30]
            top30 = {"video": sum(1 for a in top if a["medium"] == "video"),
                     "image": sum(1 for a in top if a["medium"] == "image"), "n": len(top)}
        meta_brands[key] = {
            "name": name, "dir": str(d), "n": len(ads), "n_video": nv, "n_image": ni,
            "unique_videos": len(uv[key]),
            "unclear": {"video": sum(1 for a in ads.values() if a["medium"] == "video" and not a["row"]),
                        "image": sum(1 for a in ads.values() if a["medium"] == "image" and not a["row"])},
            "top30_all": top30,
        }

    rows = []
    for rid, label, medium in ROWS:
        a = row_stats(brands["A"], rid, meta_brands["A"][f"n_{medium}"])
        b = row_stats(brands["B"], rid, meta_brands["B"][f"n_{medium}"])
        status, lead, ratio = status_for(a, b)
        rows.append({
            "id": rid, "label": label, "medium": medium, "A": a, "B": b,
            "status": status, "lead": lead, "ratio": ratio, "evidence": evidence_for(a, b),
            "cards": {"A": cards_for(brands["A"], a["ad_ids"]), "B": cards_for(brands["B"], b["ad_ids"])},
        })

    now, launches = {}, {}
    for key in ("A", "B"):
        recent = [k for k, a in brands[key].items() if a["start_date"]
                  and (snap_date - dt.date.fromisoformat(a["start_date"])).days <= NOW_DAYS]
        recent.sort(key=lambda k: brands[key][k]["start_date"], reverse=True)
        now[key] = {"n": len(recent), "ad_ids": recent,
                    "by_row": dict(Counter(brands[key][k]["row"] or "unclear" for k in recent))}
        launches[key] = dict(sorted(Counter(a["start_date"][:7] for a in brands[key].values()
                                            if a["start_date"]).items()))

    breakdowns = {}
    for f in ("hook",):
        breakdowns[f] = {k: counter_by(brands[k], f, split_medium=True) for k in ("A", "B")}
    for f in ("offer", "angle", "language", "production", "face"):
        breakdowns[f] = {k: counter_by(brands[k], f) for k in ("A", "B")}
    breakdowns["destination"] = {k: counter_by(brands[k], "destination") for k in ("A", "B")}
    breakdowns["deadline"] = {k: sum(1 for a in brands[k].values() if a["tags"].get("deadline")) for k in ("A", "B")}
    breakdowns["campaign_tags"] = {k: Counter(a["campaign_tag"] for a in brands[k].values()
                                              if a["campaign_tag"]).most_common(5) for k in ("A", "B")}

    comp = {
        "meta": {
            "snapshot_date": snapshot, "country": args.country, "rules_version": "rows-v1",
            "sample_rule": SAMPLE_RULE, "brands": meta_brands,
            "tag_check": {"A": checks["A"], "B": checks["B"]},
            "thresholds": {"present": PRESENT, "lead_ratio": LEAD_RATIO, "strong_ads": STRONG_ADS,
                           "strong_ideas": STRONG_IDEAS, "thin_ads": THIN_ADS, "now_days": NOW_DAYS},
        },
        "rows": rows,
        "table_stakes": [r["id"] for r in rows if r["status"] == "even"],
        "now": now,
        "launches": launches,
        "breakdowns": breakdowns,
        "pacing": {k: pacing(brands[k], uv[k]) for k in ("A", "B")},
        "standouts": {
            "A": standouts("A", "B", rows, brands["A"], args.dir_a),
            "B": standouts("B", "A", rows, brands["B"], args.dir_b),
        },
        "ads": {k: {f: v for f, v in a.items() if f not in ("metrics", "page_name")} for k, a in ads_all.items()},
        "rerun": None,
    }
    if args.previous:
        comp["rerun"] = rerun_diff(load_json(args.previous), ads_all)

    Path(args.out).write_text(json.dumps(comp, indent=1, ensure_ascii=False))
    print(f"wrote {args.out}: A {meta_brands['A']['n']} ads, B {meta_brands['B']['n']} ads, snapshot {snapshot}")
    for r in rows:
        print(f"  {r['id']} {r['label']:<20} A {r['A']['n']:>2} ({r['A']['share']:.0%})  "
              f"B {r['B']['n']:>2} ({r['B']['share']:.0%})  {r['status']:<8} {r['evidence']}")


if __name__ == "__main__":
    main()
