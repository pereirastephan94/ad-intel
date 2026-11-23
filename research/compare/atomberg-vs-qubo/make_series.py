"""Writes series.json for Atomberg (A) vs Qubo (B) from concept ids and ad text.
Every series follows research/<brand>/concepts.md "Series and recurring devices"; ids are listed in full here,
and each count is checked against the figure concepts.md gives (the script stops if one differs).
Usage: python3 make_series.py <out series.json>"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]


def load(b):
    ads = json.loads((R / b / "ads.json").read_text())
    cid = {}
    for k, a in ads.items():
        f = (R / b / "videos" / a["video_asset"] / "tags.json") if a.get("video_asset") else (R / b / "statics" / f"{k}.tags.json")
        cid[k] = json.loads(f.read_text())["tags"].get("concept_id")
    return ads, cid


A, ca = load("atomberg")
B, cb = load("qubo")


def by_c(c, prefix, nums):
    want = {f"{prefix}-c{n:02d}" for n in nums}
    return [k for k in sorted(c) if c[k] in want]


def text(a):
    return " ".join(str(a.get(f) or "") for f in ("headline", "link_description", "body"))


upgrade = [k for k in sorted(A) if re.search(r"upgrade", text(A[k]), re.I)]
assert len(upgrade) == 16  # a shared word, not an idea: read in a line, kept out of the leaning score

series = {
    "_note": "Series and recurring devices per brand, from research/<brand>/concepts.md and extras.json, every ad id listed. Read by compute.py --series.",
    "A": [
        {"name": "Technician and AMC trust (Intellon)", "ads": by_c(ca, "AT", [11, 12, 18]),
         "note": "Four Intellon ads built on distrust of RO service visits and bills, all showing the filter-health app; live 14 to 242 days."},
        {"name": "Zenova regional demo set", "ads": by_c(ca, "AT", [21, 22, 23, 24]),
         "note": "Five mixer ads with one headline and one long ad text, started 2 to 10 August 2026; four in Tamil or Telugu, none with a price."},
        {"name": "Rupee saving line on fans", "ads": by_c(ca, "AT", [3, 5, 6, 7, 8, 9]),
         "note": "Six of the ten fan ads give a saving: ₹1,500 a year on ceiling fans or ₹400 a summer on the pedestal fan, worded differently in speech, card and ad text."},
        {"name": "Gag box, then the real product", "ads": by_c(ca, "AT", [17, 25]),
         "note": "A fake product box is pitched as a joke (AutoMatka for the purifier, AutoSilbatta for the mixer) before the real Atomberg product appears."},
    ],
    "B": [
        {"name": "Doesn't just record. It protects.", "ads": by_c(cb, "QB", [12, 13, 14, 15, 17]),
         "note": "Six camera ads use the line in an end card, headline or ad text; two reuse one night parking clip under different hooks."},
        {"name": "Smart lock catalogue cards", "ads": by_c(cb, "QB", [5, 6, 7, 8, 9]),
         "note": "Ten lock ads from the product catalogue with an unfilled brand field and a Hero Group headline, live 373 to 605 days."},
        {"name": "Don't buy X reverse-psychology lists", "ads": by_c(cb, "QB", [16, 21, 29]),
         "note": "A man sarcastically lists three reasons not to buy a camera, a dashcam or a purifier, in Hinglish; live 59 to 154 days."},
        {"name": "India's #1 brand of dashcams end line", "ads": by_c(cb, "QB", [21, 22, 23, 24, 25, 26]),
         "note": "All six dashcam ads end on the same rank line, with no source or year; four are presenters, two silent road clips."},
        {"name": "Purifier winter push", "ads": by_c(cb, "QB", [27, 28]),
         "note": "Six purifier ads with the See details button and one collection page, started 16 October to 3 November 2026; five run the smoke demo."},
        {"name": "October 2026 lock and camera images", "ads": by_c(cb, "QB", [10, 11, 19, 20]),
         "note": "Four plain image ads started 16 to 21 October 2026, the only image ads outside the catalogue: two lock cards and two camera cards."},
        {"name": "November doorbell pair", "ads": by_c(cb, "QB", [2, 3]),
         "note": "Two doorbell ads started 11 November 2026 share a rating and free installation line that neither video shows."},
        {"name": "Q1000 living-room pair", "ads": by_c(cb, "QB", [30, 31]),
         "note": "Two Q1000 presenter ads started 27 October 2026 share one headline and ad text over two different scripts."},
    ],
}

expect = {"Technician and AMC trust (Intellon)": 4, "Zenova regional demo set": 5, "Rupee saving line on fans": 6,
          "Gag box, then the real product": 2,
          "Doesn't just record. It protects.": 6, "Smart lock catalogue cards": 10, "Don't buy X reverse-psychology lists": 4,
          "India's #1 brand of dashcams end line": 6, "Purifier winter push": 6, "October 2026 lock and camera images": 4,
          "November doorbell pair": 2, "Q1000 living-room pair": 2}
for side in ("A", "B"):
    for s in series[side]:
        n = len(s["ads"])
        assert n == expect[s["name"]], (s["name"], n)
        print(side, s["name"], n)
Path(sys.argv[1]).write_text(json.dumps(series, indent=1, ensure_ascii=False))
print("wrote", sys.argv[1])
