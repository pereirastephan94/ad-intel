"""Make a read-only view of a brand folder that holds only its written-up ads.

Usage: python3 written_up.py <research/brand> <out_dir>

Fitelo's ads.json grew from 34 to 58 ads on 23 Nov 2026 (24 image ads from one more Library view), but only
the 34 earlier ads have tags and a place in concepts.md. compute.py counts every ad in ads.json, so this
writes <out_dir>/ads.json with the written-up ads only (a video ad needs videos/<asset>/tags.json, an image
ad statics/<id>.tags.json) and links everything else back to the brand folder. The brand folder is not changed.
"""
import json
import sys
from pathlib import Path

src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
ads = json.loads((src / "ads.json").read_text())
keep, drop = {}, []
for lid, a in ads.items():
    asset = a.get("video_asset")
    tags = src / "videos" / asset / "tags.json" if asset else src / "statics" / f"{lid}.tags.json"
    (keep.__setitem__(lid, a) if tags.exists() else drop.append(lid))
(out / "ads.json").write_text(json.dumps(keep, indent=1, ensure_ascii=False))
for p in src.iterdir():
    if p.name == "ads.json":
        continue
    link = out / p.name
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(p)
print(f"{src.name}: kept {len(keep)} written-up ads, left out {len(drop)}: {' '.join(drop)}")
