#!/usr/bin/env python3
"""Draft research/compare/<pair>/products.json: one product_key per sampled ad.

Usage:
  products.py <research_dir_A> <research_dir_B> <out products.json> [--rules rules.json]

Each ad's key is taken from its tags ("product", then "one_line", then the ad's headline and body),
matched against keyword rules in order (first match wins). Rules are {"product_key": ["keyword", ...]},
case-insensitive, whole words where the keyword is short. The default rules cover Indian retail finance;
pass --rules for another category (for example gym_pass, sports_pass, diet_plan).

Ads that match no rule get "unclear" and are printed. Edit the file by hand afterwards; compute.py reads it.
If <out> already exists, its "labels" and "site" blocks are kept and only "ads" is redrafted.
The "site" block (what each brand sells on its own website) is written by hand from research/<brand>/site.md.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_RULES = {
    "fd_backed_card": ["credit card", "fd card", "lounge"],
    "recurring_deposit": ["recurring deposit", "rd"],
    "bonds": ["bond", "bonds"],
    "fixed_deposit": ["fixed deposit", "fd", "fds"],
    "mutual_funds": ["mutual fund", "sip"],
    "gold": ["gold"],
}
DEFAULT_LABELS = {
    "fd_backed_card": "FD-backed credit card", "recurring_deposit": "Recurring deposit", "bonds": "Bonds",
    "fixed_deposit": "Fixed deposits", "mutual_funds": "Mutual funds", "gold": "Gold",
}


def load(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def tags_for(rdir, lid, ad):
    asset = ad.get("video_asset")
    if asset:
        return (load(rdir / "videos" / asset / "tags.json", {}) or {}).get("tags", {})
    return (load(rdir / "statics" / f"{lid}.tags.json", {}) or {}).get("tags", {})


def match(text, rules):
    t = (text or "").lower()
    for key, words in rules.items():
        for w in words:
            pat = rf"(?<![a-z]){re.escape(w.lower())}(?![a-z])"
            if re.search(pat, t):
                return key
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir_a")
    ap.add_argument("dir_b")
    ap.add_argument("out")
    ap.add_argument("--rules")
    args = ap.parse_args()
    rules = load(args.rules) if args.rules else DEFAULT_RULES
    prev = load(args.out, {}) or {}
    out = {"labels": prev.get("labels") or {k: DEFAULT_LABELS.get(k, k.replace("_", " ").capitalize()) for k in rules},
           "site": prev.get("site") or {"A": [], "B": []}, "ads": {}}
    for d in (args.dir_a, args.dir_b):
        rdir = Path(d)
        for lid, ad in (load(rdir / "ads.json", {}) or {}).items():
            t = tags_for(rdir, lid, ad)
            key = None
            for src in (t.get("product"), t.get("one_line"), ad.get("headline"), ad.get("body")):
                key = match(src, rules)
                if key:
                    break
            out["ads"][lid] = key or "unclear"
            if not key:
                print(f"unclear: {rdir.name} {lid} product={t.get('product')!r}", file=sys.stderr)
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    from collections import Counter
    print(f"wrote {args.out}:", dict(Counter(out["ads"].values())))


if __name__ == "__main__":
    main()
