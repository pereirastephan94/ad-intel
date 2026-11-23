"""Writes series.json for Scaler School of Business (A) vs Mesa (B) from concept ids, assets and ad text.
Every series follows research/<brand>/concepts.md "Series and recurring devices"; ids are listed in full here.
Usage: python3 make_series.py <out series.json>"""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]

def load(b):
    ads = json.loads((R / b / "ads.json").read_text())
    cid = {}
    for k, a in ads.items():
        f = (R / b / "videos" / a["video_asset"] / "tags.json") if a.get("video_asset") else (R / b / "statics" / f"{k}.tags.json")
        try:
            cid[k] = json.loads(f.read_text())["tags"].get("concept_id")
        except FileNotFoundError:
            cid[k] = None
    return ads, cid

A, ca = load("scaler-school-of-business")
B, cb = load("mesa")
def by_c(c, ids):
    return [k for k in sorted(c) if c[k] in ids]
def by_asset(ads, assets):
    return [k for k in sorted(ads) if ads[k].get("video_asset") in assets]

mba_down = by_c(ca, {"SSB-c01", "SSB-c04", "SSB-c05"}) + ["1150917287446121"]
early = ["954275137769376", "1123141853818596", "1406583844890391", "4572207989702796"]
series = {
 "_note": "Series and recurring devices per brand, from research/<brand>/concepts.md and extras.json, every ad id listed. Read by compute.py --series.",
 "A": [
  {"name": "Openings that run down the MBA", "ads": mba_down,
   "note": "11 of 30 ads open by calling the MBA or college outdated, dead, not enough or its graduates underused; 3 of them say \"outdated\" and \"unemployable\"."},
  {"name": "Same footage in several shapes", "ads": by_c(ca, {"SSB-c02", "SSB-c03", "SSB-c05", "SSB-c10"}),
   "note": "Four ideas run in two shapes each (16:9 with 9:16, 4:5 or square); some cuts drop or swap the first sentence."},
  {"name": "Named companies in the story", "ads": by_c(ca, {"SSB-c02", "SSB-c04", "SSB-c07", "SSB-c10"}),
   "note": "Mokobara is spoken or captioned in three ideas (8 ads); the timeline film names Sequoia, McKinsey, Zomato, Razorpay and Apple (5 ads), spoken only."},
  {"name": "50 lakh in three meanings", "ads": by_c(ca, {"SSB-c04", "SSB-c10", "SSB-c11"}),
   "note": "50 lakh is a brand's revenue, a D2C aim or a funding offer to a student, with no source or student named."},
  {"name": "One interview closing line, three scripts", "ads": by_c(ca, {"SSB-c03", "SSB-c05", "SSB-c08"}),
   "note": "\"If I was a student ... like an SSB today, I do think that exposure would have helped\" closes three scripts; none labels who speaks."},
  {"name": "Early bird date after the date", "ads": early,
   "note": "Four ads started 17 to 19 Nov still show \"Early Bird Deadline 1st November 2026\", two in the headline and two on the end card."},
 ],
 "B": [
  {"name": "The Ascend shoot, cut into six ideas", "ads": by_c(cb, {"MS-c03", "MS-c13", "MS-c15", "MS-c16", "MS-c18", "MS-c20"}),
   "note": "One interview session gives six different answers across 32 ads, each with its own headline naming Ascend, while the speech never does."},
  {"name": "Quit-your-job reassurance cards", "ads": by_c(cb, {"MS-s05", "MS-s03", "MS-s01", "MS-s31"}),
   "note": "Image ads that say you need not quit your job: \"You Don't Have to Quit Your Job to Learn to Build\" alone is 15 ads, all Ascend."},
  {"name": "The 200-person cohort call", "ads": sorted(k for k, a in B.items() if (a.get("body") or "").startswith("Mesa is selecting 200")),
   "note": "13 ads share the text \"Mesa is selecting 200 ambitious individuals\" over four videos, nine of them over the 38-second cohort call itself."},
  {"name": "One investor recording, two edits", "ads": by_c(cb, {"MS-c11", "MS-c19"}),
   "note": "An outside investor on a podcast set: one cut opens on \"200 plus startups\", the other on \"every student has to sell 5 lakhs in 8 weeks\"."},
  {"name": "Graduate outcomes, in figures or named alumni", "ads": by_c(cb, {"MS-c06", "MS-c07", "MS-c09", "MS-c12", "MS-c30", "MS-s06", "MS-s11", "MS-s14", "MS-s18", "MS-s22", "MS-s23", "MS-s26", "MS-s32"}),
   "note": "Full-time PGP ads that state a graduate outcome: 100% placements, an average salary upwards of 25 lakhs, 57.5% in early startups, 50 to 60% rises (14 videos); 71% career pivot, 58% founder-facing, 2.8x, or a named graduate's new role (16 image ads). The figures are not sourced and do not agree."},
  {"name": "Undergraduate podcast-mic set", "ads": by_c(cb, {"MS-c22", "MS-c24", "MS-c29"}),
   "note": "One speaker at a studio microphone tells three student stories; students are talked about and never speak."},
  {"name": "Founding cohort and early bird cards", "ads": by_c(cb, {"MS-s16", "MS-s25", "MS-s04"}),
   "note": "Ascend image ads that invite people to the founding online cohort; one idea names the early bird close, 26 November 2026."},
  {"name": "The borrowed-clip selfie", "ads": by_c(cb, {"MS-c02"}),
   "note": "One 105-second video with a known investor's stage clip, re-sent in four shapes under two ad texts."},
 ],
}
for k in "AB":
    for s in series[k]:
        print(k, len(s["ads"]), s["name"])
Path(sys.argv[1]).write_text(json.dumps(series, indent=1, ensure_ascii=False))
