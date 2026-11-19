#!/usr/bin/env python3
"""Write two invented brand folders (brand-a, brand-b) shaped like research/<brand>/ for testing.

Usage: make_dummy.py [out_dir]   (default: this folder)
Everything here is made up: brands, ads, people, numbers. Stills are flat colour cards drawn with PIL.
"""
import datetime as dt
import json
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
SNAP = dt.date(2026, 11, 19)
rng = random.Random(7)

FONT_PATHS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]


def font(size):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(path, size, bg, fg, title, sub, tag):
    img = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(img)
    w, h = size
    d.rectangle([0, 0, w, 54], fill=tuple(max(0, c - 30) for c in bg))
    d.text((20, 16), tag, font=font(20), fill=fg)
    f = font(int(w / 11))
    y = h * 0.32
    for line in wrap(d, title, f, w - 40)[:5]:
        d.text((20, y), line, font=f, fill=fg)
        y += f.size * 1.2
    d.text((20, h - 60), sub, font=font(18), fill=fg)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=82)


# Ideas per brand: (row, idea, n_ads, hook, hook_type, face, offer, angle, language, production, script lines)
BRANDS = {
    "brand-a": {
        "name": "Brand A", "letter": "A", "colours": [(32, 84, 140), (20, 110, 100), (120, 60, 140), (170, 90, 30)],
        "ideas": [
            ("V1", 1, 2, "I check my savings every morning. Here's why.", "story_open", "presenter", "none", "trust_safety", "english", "phone_lofi"),
            ("V2", 2, 2, "Diwali bonus aaya? Usse sota mat chhodo.", "callout", "actor_model", "none", "outcome", "hinglish", "high_film"),
            ("V2", 3, 2, "Two friends, one bet: who saves more by March?", "story_open", "actor_model", "none", "identity", "english", "studio"),
            ("V2", 4, 1, "Maa ne kaha, pehle bachao, phir kharcho.", "story_open", "actor_model", "none", "identity", "hinglish", "high_film"),
            ("V3", 5, 2, "Open a deposit in three taps.", "number_claim", "none", "none", "convenience_speed", "english", "studio"),
            ("V3", 6, 2, "Watch 10,000 rupees grow in 12 months.", "number_claim", "none", "rate_return", "outcome", "english", "studio"),
            ("V3", 7, 1, "No branch. No paperwork. Just this screen.", "problem", "none", "none", "convenience_speed", "hinglish", "studio"),
            ("V4", 8, 2, "9.1% a year. Insured up to 5 lakh.", "offer", "none", "rate_return", "trust_safety", "english", "designed_static"),
            ("I1", 9, 5, "9.1% p.a. on fixed deposits", "offer", "none", "rate_return", "outcome", "english", "designed_static"),
            ("I1", 10, 3, "Get 500 cashback on your first deposit", "offer", "none", "cashback", "price_value", "english", "designed_static"),
            ("I2", 11, 2, "Your savings, finally in one place", "visual_only", "actor_model", "none", "convenience_speed", "english", "designed_static"),
            ("I2", 12, 2, "Made for people who plan ahead", "callout", "actor_model", "none", "identity", "english", "designed_static"),
            ("I2", 13, 1, "Safe. Simple. Yours.", "visual_only", "none", "none", "trust_safety", "english", "designed_static"),
            ("I3", 14, 1, "Rated 4.6 by 2 lakh savers", "social_proof", "none", "none", "popularity", "english", "designed_static"),
        ],
    },
    "brand-b": {
        "name": "Brand B", "letter": "B", "colours": [(150, 50, 40), (60, 60, 60), (40, 100, 60), (90, 70, 140)],
        "ideas": [
            ("V1", 1, 3, "Main Ravi hoon, Brand B ka co-founder. Ek sawaal.", "question", "founder_declared", "none", "trust_safety", "hindi", "phone_lofi"),
            ("V1", 2, 2, "Is your FD beating inflation? Mine wasn't.", "question", "presenter", "none", "outcome", "hinglish", "phone_lofi"),
            ("V1", 3, 2, "Main CA hoon. Yeh galti mat karna.", "problem", "expert_or_staff", "none", "trust_safety", "hinglish", "phone_lofi"),
            ("V1", 4, 1, "I moved my emergency fund. Here's what happened.", "story_open", "creator", "none", "outcome", "english", "phone_lofi"),
            ("V2", 5, 3, "Shaadi ka kharcha, ek saal pehle se.", "story_open", "actor_model", "none", "outcome", "hindi", "high_film"),
            ("V3", 6, 2, "Dekho, 2 minute mein account khul gaya.", "number_claim", "none", "none", "convenience_speed", "hindi", "phone_lofi"),
            ("V3", 7, 2, "Every rupee, tracked. Here's the screen.", "visual_only", "none", "none", "feature", "english", "studio"),
            ("V4", 8, 1, "Interest rates are changing. Are you?", "question", "none", "none", "outcome", "english", "ai_or_stock"),
            ("I1", 9, 2, "Flat 250 off your first SIP. Ends Sunday.", "offer", "none", "discount", "price_value", "english", "designed_static"),
            ("I2", 10, 3, "Plan the big day without the big loan", "callout", "actor_model", "none", "outcome", "english", "designed_static"),
            ("I2", 11, 3, "Your money. Your rules.", "visual_only", "actor_model", "none", "identity", "hinglish", "designed_static"),
            ("I3", 12, 2, "\"Saved 40,000 for my sister's wedding\": Priya, Pune", "social_proof", "customer", "none", "outcome", "english", "designed_static"),
            ("I3", 13, 2, "Rated 4.7 on Play Store by 3 lakh users", "social_proof", "none", "none", "popularity", "english", "designed_static"),
            ("I3", 14, 2, "As featured in five national dailies", "social_proof", "none", "none", "trust_safety", "english", "designed_static"),
        ],
    },
}

SCRIPT_TAIL = [
    "Most people leave their savings in an account that barely moves.",
    "With us, you pick a term, pick an amount, and you're done.",
    "Your deposit is insured, and you can see every rupee in the app.",
    "Thousands of people moved their money this month.",
    "Download the app and start with as little as 1,000 rupees.",
]


def main():
    for slug, b in BRANDS.items():
        root = OUT / slug
        (root / "videos").mkdir(parents=True, exist_ok=True)
        (root / "statics").mkdir(exist_ok=True)
        (root / "images").mkdir(exist_ok=True)
        ads, lid_n = {}, 0
        all_rank = 0
        for (row, idea, n_ads, hook, hook_type, face, offer, angle, lang, prod) in b["ideas"]:
            concept = f"{b['letter']}-c{idea:02d}"
            colour = b["colours"][idea % len(b["colours"])]
            base_days = rng.randint(8, 110)
            is_video = row.startswith("V")
            asset = None
            if is_video:
                asset = f"{b['letter'].lower()}{idea:02d}000{rng.randint(100000, 999999)}"
                vdir = root / "videos" / asset
                dur = round(rng.uniform(14, 45), 1)
                times = [0, 0.5, 1, 2, 3] + sorted(round(rng.uniform(4, dur - 1), 1) for _ in range(3))
                lines = [hook] + rng.sample(SCRIPT_TAIL, 4)
                seg_len = dur / len(lines)
                segs = [{"start": round(i * seg_len, 2), "end": round((i + 1) * seg_len, 2), "text": l}
                        for i, l in enumerate(lines)]
                for i, t in enumerate(times):
                    shade = tuple(min(255, c + i * 6) for c in colour)
                    title = hook if t < 3 else lines[min(len(lines) - 1, int(t / seg_len))]
                    label = {"V1": "Person to camera", "V2": "Scene", "V3": "App screen", "V4": "Text and motion"}[row]
                    card(vdir / f"still{i:02d}_{t:g}s.jpg", (360, 640), shade, (255, 255, 255),
                         title, f"{b['name']}  {t:g}s", f"{label}  (placeholder)")
                cuts = sorted(round(rng.uniform(1, dur), 2) for _ in range(rng.randint(4, 16)))
                words = int(sum(len(l.split()) for l in lines))
                (vdir / "metrics.json").write_text(json.dumps({
                    "duration_s": dur, "width": 720, "height": 1280, "cuts": len(cuts),
                    "cuts_per_10s": round(len(cuts) / dur * 10, 2), "first_cut_s": cuts[0],
                    "cut_times": cuts, "has_audio": True, "speech_share": 0.8, "words": words,
                    "words_per_min": int(words / dur * 60 * rng.uniform(1.6, 2.4)), "first_speech_s": 0}, indent=1))
                (vdir / "transcript.json").write_text(json.dumps({
                    "asset": asset, "duration_s": dur,
                    "stills": [{"t": t, "why": "opening" if t <= 3 else "scene change"} for t in times],
                    "transcript": {"language": "hi" if lang == "hindi" else "en",
                                   "text": " ".join(lines), "segments": segs}}, indent=1, ensure_ascii=False))
                tags = {"row": row, "face": face, "hook": hook_type, "hook_text": hook, "offer": offer,
                        "deadline": False, "angle": angle, "language": lang, "production": prod,
                        "concept_id": concept,
                        "founder_evidence": "spoken: Main Ravi hoon, Brand B ka co-founder" if face == "founder_declared" else ""}
                (vdir / "tags.json").write_text(json.dumps(
                    {"tags": tags, "tagging": {"model": "dummy", "unsure": [], "human_checked": False}},
                    indent=1, ensure_ascii=False))
            for k in range(n_ads):
                lid_n += 1
                lid = f"9{b['letter'] == 'A' and 1 or 2}{lid_n:04d}{rng.randint(100000, 999999)}"
                days = max(1, base_days - k * rng.randint(3, 20))
                start = SNAP - dt.timedelta(days=days)
                if b["letter"] == "A":
                    url = rng.choice(["https://play.google.com/store/apps/details?id=example.brand.a",
                                      "https://brand-a.example/deposits?utm_campaign=fd_rates_q4"])
                else:
                    url = rng.choice(["https://brand-b.example/?utm_campaign=wedding_goals",
                                      "https://brand-b.example/?utm_campaign=trust_founder",
                                      "https://wa.me/910000000000"])
                views = {}
                if rng.random() < 0.7:
                    all_rank += 1
                    views["all"] = all_rank
                views["video" if is_video else "image"] = rng.randint(1, 30)
                ad = {
                    "library_id": lid, "link": f"https://www.facebook.com/ads/library/?id={lid}",
                    "page_id": "0", "page_name": b["name"], "is_active": True,
                    "start_date": start.isoformat(), "days_running": days,
                    "media_type": "VIDEO" if is_video else "IMAGE",
                    "body": f"{hook} {SCRIPT_TAIL[k % len(SCRIPT_TAIL)]}",
                    "headline": hook if not is_video else SCRIPT_TAIL[(k + 2) % len(SCRIPT_TAIL)][:48],
                    "link_description": "Invented ad for testing", "cta": "Install now" if "play.google" in url else "Learn more",
                    "landing_url": url, "copies": rng.choice([1, 1, 2, 3, 4, 6, 8]),
                    "platforms": ["FACEBOOK", "INSTAGRAM"],
                    "extra": {"cards": 0, "display_format": "VIDEO" if is_video else "IMAGE", "categories": []},
                    "sample_views": views,
                }
                if is_video:
                    ad["video_asset"] = asset
                else:
                    card(root / "images" / f"{lid}.jpg", (480, 480), colour, (255, 255, 255), hook,
                         f"{b['name']}  version {k + 1}", {"I1": "Offer", "I2": "Product or people", "I3": "Proof"}[row] + "  (placeholder)")
                    tags = {"row": row, "face": face, "hook": hook_type, "hook_text": hook, "offer": offer,
                            "deadline": "Ends" in hook, "angle": angle, "language": lang, "production": prod,
                            "concept_id": concept, "founder_evidence": ""}
                    (root / "statics" / f"{lid}.tags.json").write_text(json.dumps(
                        {"tags": tags, "tagging": {"model": "dummy", "unsure": [], "human_checked": False}},
                        indent=1, ensure_ascii=False))
                ads[lid] = ad
        (root / "ads.json").write_text(json.dumps(ads, indent=1, ensure_ascii=False))
        (root / "page.json").write_text(json.dumps({"name": b["name"], "page_id": "0", "country": "IN"}))
        (root / "tag_check.json").write_text(json.dumps(
            {"n_checked": 6, "agreement": {"row": 0.83, "face": 0.83, "concept_id": 0.67}}))
        print(f"{slug}: {len(ads)} ads")


if __name__ == "__main__":
    main()
