"""Checks every figure used in perspectives.json against comparison.json, series.json and the ads (runbook step 6).
Usage: python3 check_figures.py   (prints each check; exits non-zero on the first failure)"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

H = Path(__file__).resolve().parent
C = json.loads((H / "comparison.json").read_text())
S = json.loads((H / "series.json").read_text())
ads = C["ads"]
fails = 0


def ok(name, got, want):
    global fails
    good = got == want
    fails += not good
    print(("ok   " if good else "FAIL ") + f"{name}: {got!r}" + ("" if good else f" (want {want!r})"))


def sel(k, **kw):
    out = []
    for l, a in ads.items():
        if a["brand"] != k:
            continue
        if all((a.get(f) if f != "cid" else a["tags"].get("concept_id")) in (v if isinstance(v, (set, list)) else {v}) for f, v in kw.items()):
            out.append(l)
    return out


def txt(a):
    return " ".join([a["headline"], a["body"], a["link_description"], a["transcript"], a["hook_text"]])


def ser(k, name):
    return next(s for s in S[k] if s["name"] == name)["ads"]


lockA, lockB = sel("A", product_key="smart_lock"), sel("B", product_key="smart_lock")
ok("Atomberg lock ads", len(lockA), 2)
ok("Atomberg lock versions", sum(int(ads[l]["versions"]) for l in lockA), 3)
ok("Atomberg lock language", {ads[l]["tags"]["language"] for l in lockA}, {"hinglish"})
ok("Atomberg lock start", {ads[l]["start_date"] for l in lockA}, {"2026-09-08"})
ok("Qubo lock ads", len(lockB), 13)
ok("Qubo lock ads all English", {ads[l]["tags"]["language"] for l in lockB}, {"english"})
ok("Lock ads with a person to camera, both", sum(1 for l in lockA + lockB if ads[l]["row"] == "V1"), 0)
ok("Qubo lock ads with unfilled brand", sum(1 for l in lockB if "{{product.brand}}" in ads[l]["body"]), 10)
ok("Qubo lock ads started in 2025", sum(1 for l in lockB if ads[l]["start_date"].startswith("2025")), 11)
cards = ser("B", "Smart lock catalogue cards")
ok("Lock catalogue set", (len(cards), sum(1 for l in cards if ads[l]["medium"] == "image"),
                          min(int(ads[l]["days"]) for l in cards), max(int(ads[l]["days"]) for l in cards)), (10, 8, 373, 605))
ok("Lock catalogue set all started 2025", {ads[l]["start_date"][:4] for l in cards}, {"2025"})
ok("Warranty 3 Years cards", len(sel("B", cid="QB-c08")), 2)
ok("Warranty 2+ Years cards", len(sel("B", cid="QB-c09")), 2)
dont = ser("B", "Don't buy X reverse-psychology lists")
ok("Don't buy series", (len(dont), max(int(ads[l]["days"]) for l in dont), sorted({ads[l]["product_key"] for l in dont})),
   (4, 154, ["air_purifier", "dashcam", "security_camera"]))
c04 = sel("B", cid="QB-c04")
ok("Four-customer film days", int(ads[c04[0]]["days"]), 620)
for q in ["The installation process was very easy", "We are able to kind of provide remote access to maids",
          "Same goes with the gardener", "And it has different logs so that's definitely makes it more secure",
          "the rose gold finish was very premium"]:
    ok(f"quote in customer film: {q[:30]}", q in ads[c04[0]]["transcript"], True)
zen = ser("A", "Zenova regional demo set")
ok("Zenova set size and Tamil or Telugu", (len(zen), sum(1 for l in zen if ads[l]["tags"]["language"].startswith("regional"))), (5, 4))
langA = Counter(ads[l]["tags"]["language"] for l in sel("A", medium="video"))
langB = Counter(ads[l]["tags"]["language"] for l in sel("B", medium="video"))
ok("Atomberg video languages", dict(langA), {"hinglish": 17, "regional:tamil": 5, "regional:telugu": 3, "english": 2, "unclear": 2})
ok("Qubo video languages", dict(langB), {"hinglish": 19, "english": 11})
ok("Image ad languages", (Counter(ads[l]["tags"]["language"] for l in sel("A", medium="image")),
                          Counter(ads[l]["tags"]["language"] for l in sel("B", medium="image"))), (Counter(english=1), Counter(english=12)))
tech = ser("A", "Technician and AMC trust (Intellon)")
ok("Technician series", (len(tech), max(int(ads[l]["days"]) for l in tech)), (4, 242))
gag = ser("A", "Gag box, then the real product")
ok("Gag series", (len(gag), max(int(ads[l]["days"]) for l in gag), len({ads[l]["product_key"] for l in gag})), (2, 178, 2))
ok("Atomberg ideas, max ads per idea", (len({ads[l]["tags"]["concept_id"] for l in sel("A")}),
                                        max(Counter(ads[l]["tags"]["concept_id"] for l in sel("A")).values())), (26, 2))
ok("Fan saving series", len(ser("A", "Rupee saving line on fans")), 6)
nowA, nowB = C["now"]["A"]["ad_ids"], C["now"]["B"]["ad_ids"]
ok("Atomberg last 30 days", (len(nowA), sorted({ads[l]["start_date"] for l in nowA}), Counter(ads[l]["product_key"] for l in nowA)),
   (5, ["2026-11-04", "2026-11-05", "2026-11-06"], Counter(ceiling_fan=3, water_purifier=2)))
ok("Qubo last 30 days", (len(nowB), Counter(ads[l]["product_key"] for l in nowB)),
   (15, Counter(air_purifier=7, security_camera=3, video_doorbell=2, dashcam=2, smart_lock=1)))
ok("Qubo lock card in last 30 days", [ads[l]["start_date"] for l in nowB if ads[l]["product_key"] == "smart_lock"], ["2026-10-21"])
cl = [c for c in C["clusters"]["B"] if c["from"] == "2026-10-27"][0]
ok("Qubo 27 Oct to 3 Nov cluster", (cl["to"], cl["n"], cl["products"].get("air_purifier")), ("2026-11-03", 9, 7))
pur = ser("B", "Purifier winter push")
ok("Purifier push size, earliest", (len(pur), min(ads[l]["start_date"] for l in pur)), (6, "2026-10-16"))
dest = lambda k: Counter("amazon" if "amazon" in (a.get("link_description") or "") else a["destination"] for a in ads.values() if a["brand"] == k)
ra = json.loads((H.parents[1] / "atomberg" / "ads.json").read_text())
rb = json.loads((H.parents[1] / "qubo" / "ads.json").read_text())
ok("Atomberg destinations", Counter("amazon.in" if "amazon.in" in a["landing_url"] else "atomberg.com" if "atomberg.com" in a["landing_url"] else "other" for a in ra.values()),
   Counter({"atomberg.com": 29, "amazon.in": 1}))
ok("Qubo destinations", Counter("quboworld.com" if "quboworld.com" in a["landing_url"] else "other" for a in rb.values()), Counter({"quboworld.com": 42}))
ok("Qubo lock landing pages", Counter(rb[l]["landing_url"].split("?")[0].rsplit("/", 1)[-1] for l in lockB), Counter({"smart-locks": 11, "smart-door-lock-select-black": 2}))
intel = sel("A", product_key="water_purifier")
ok("Intellon ads, ideas, person to camera", (len(intel), len({ads[l]["tags"]["concept_id"] for l in intel}), sum(1 for l in intel if ads[l]["row"] == "V1")), (10, 9, 4))
airp = sel("B", product_key="air_purifier")
ok("Qubo purifier ads, ideas, presenters, smoke demo", (len(airp), len({ads[l]["tags"]["concept_id"] for l in airp}),
                                                        sum(1 for l in airp if ads[l]["row"] == "V1"), len(sel("B", cid="QB-c27"))), (9, 5, 3, 5))
ok("25,000 over 8 years spoken", bool(re.search(r"25,?000|pachchis hazaar|25 thousand|पच्छिस हजार", ads["1100991832415673"]["transcript"], re.I)), True)
ok("filter saste line", "फिल्टर सबस्ते" in ads["1397233215855053"]["transcript"], True)
freeB = [l for l in sel("B") if re.search(r"free install", txt(ads[l]) + json.dumps(ads[l]["tags"]), re.I)]
ok("Qubo ads saying free installation", Counter(ads[l]["tags"]["concept_id"] for l in freeB),
   Counter({"QB-c08": 2, "QB-c09": 2, "QB-c10": 1, "QB-c11": 1, "QB-c02": 1, "QB-c03": 1}))
ok("Atomberg ads saying free installation", [l for l in sel("A") if re.search(r"free install", txt(ads[l]), re.I)], [])
ok("Creatives", (C["creatives"]["A"], C["creatives"]["B"]),
   ({"ads": 30, "versions": 35, "video_ads": 29, "videos": 27, "image_ads": 1, "images": 1},
    {"ads": 42, "versions": 54, "video_ads": 30, "videos": 23, "image_ads": 12, "images": 8}))
ok("Lock text says 6 ways", all("6 ways" in ads[l]["body"] for l in lockA), True)
ok("AI Guard free said aloud", "free" in ads["1140748798813160"]["transcript"].lower(), True)
ok("Qubo prices shown or said", sorted(["1088717086222561", "1011962618598558", "1828691691913803", "1068646366168711", "1158325139855724"]),
   sorted(sel("B", cid={"QB-c18", "QB-c10", "QB-c01", "QB-c24", "QB-c31"})))
print("failures:", fails)
sys.exit(1 if fails else 0)
