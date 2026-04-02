"""
Creative Generator — renders a 1080x1920 (9:16) ad creative
using real SSB background images + copy overlay.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, glob

# ── Fonts ─────────────────────────────────────────────────────────────────────
_HEL     = "/System/Library/Fonts/Helvetica.ttc"
FONT_REG   = (_HEL, 0)
FONT_BOLD  = (_HEL, 1)
FONT_LIGHT = (_HEL, 4)

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = (10,  10,  26)
WHITE     = (255, 255, 255)
WHITE_DIM = (180, 180, 190)
WHITE_MED = (220, 220, 225)

BUCKET_COLORS = {
    "STARTUP":      (124,  58, 237),
    "OUTCOME":      ( 34, 197,  94),
    "CURRICULUM":   (  6, 182, 212),
    "FACULTY":      (245, 158,  11),
    "SOCIAL_PROOF": (236,  72, 153),
    "URGENCY":      (239,  68,  68),
    "EMOTIONAL":    (139,  92, 246),
}

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../assets/ssb_images")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _font(spec, size):
    try:
        return ImageFont.truetype(spec[0], size, index=spec[1]) if isinstance(spec, tuple) \
               else ImageFont.truetype(spec, size)
    except Exception:
        return ImageFont.load_default()


def _clean(text):
    """Replace glyphs Helvetica can't render."""
    return (text.replace("→",">").replace("←","<").replace("—","-")
                .replace("\u2019","'").replace("\u201c",'"').replace("\u201d",'"'))


def _blend(color, alpha, bg=BG):
    """Simulate alpha-blend of color over bg (all solid RGB)."""
    a = alpha / 255.0
    return tuple(int(c * a + b * (1 - a)) for c, b in zip(color, bg))


def _wrap(text, font, max_w, draw):
    words, lines, cur = text.split(), [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textbbox((0,0), test, font=font)[2] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines


def pick_best_image(bucket=None):
    # CLEAN images only — ssb_5/6/7 have pre-printed text that clashes with our overlay
    MAP = {
        "STARTUP":      ["ssb_17.webp","ssb_19.webp","ssb_20.webp"],
        "OUTCOME":      ["ssb_19.webp","ssb_20.webp","ssb_17.webp"],
        "FACULTY":      ["ssb_19.webp","ssb_20.webp","ssb_3.webp"],
        "SOCIAL_PROOF": ["ssb_3.webp","ssb_17.webp","ssb_20.webp"],
        "CURRICULUM":   ["ssb_19.webp","ssb_20.webp","ssb_17.webp"],
        "URGENCY":      ["ssb_20.webp","ssb_19.webp","ssb_17.webp"],
        "EMOTIONAL":    ["ssb_17.webp","ssb_3.webp","ssb_19.webp"],
    }
    for name in MAP.get(bucket, ["ssb_19.webp","ssb_17.webp","ssb_20.webp"]):
        p = os.path.join(ASSETS_DIR, name)
        if os.path.exists(p): return p
    # Fallback: any clean image (exclude known text-heavy ones)
    AVOID = {"ssb_5.webp", "ssb_6.webp", "ssb_7.webp"}
    all_ = glob.glob(os.path.join(ASSETS_DIR, "ssb_*.webp"))
    clean = [x for x in all_ if os.path.basename(x) not in AVOID]
    return clean[0] if clean else (all_[0] if all_ else None)


def generate_creative(ad: dict, image_path: str = None, size: str = "9:16") -> str:
    W, H = {"9:16":(1080,1920),"1:1":(1080,1080),"16:9":(1920,1080)}.get(size,(1080,1920))
    M = 76

    ad_id    = ad.get("ad_id", "AD")
    bucket   = ad.get("bucket", "STARTUP")
    headline = _clean(ad.get("headline", ""))
    body     = _clean(ad.get("primary_text", ""))
    cta      = _clean(ad.get("cta_text", "Apply Now >"))
    accent   = BUCKET_COLORS.get(bucket, (0, 212, 255))

    # Pre-blended colour variants
    accent_dim  = _blend(accent, 190, BG)
    accent_soft = _blend(accent, 90,  BG)

    # ── 1. Background photo ────────────────────────────────────────────────────
    if not image_path:
        image_path = pick_best_image(bucket)

    canvas = Image.new("RGB", (W, H), BG)
    if image_path and os.path.exists(image_path):
        try:
            bg = Image.open(image_path).convert("RGB")
            r  = bg.width / bg.height
            if r > W/H:  nw, nh = int(H*r), H
            else:         nw, nh = W, int(W/r)
            bg = bg.resize((nw, nh), Image.LANCZOS)
            bg = bg.crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H))
            bg = bg.filter(ImageFilter.GaussianBlur(1.2))
            canvas.paste(bg, (0,0))
        except Exception:
            pass

    # ── 2. Gradient overlay (composited via RGBA layer) ────────────────────────
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    od = ImageDraw.Draw(ov)
    for y in range(int(H*0.22)):
        od.line([(0,y),(W,y)], fill=(0,0,0, int(155*(1-y/(H*0.22)))))
    fs = int(H*0.46)
    for y in range(fs, H):
        p = (y-fs)/(H-fs)
        od.line([(0,y),(W,y)], fill=(10,10,26, int(178+77*p)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")

    draw = ImageDraw.Draw(canvas)

    # ── 3. Left accent bar ─────────────────────────────────────────────────────
    bx = M - 22
    draw.rectangle([bx, int(H*0.355), bx+6, int(H*0.355)+int(H*0.32)], fill=accent)

    # ── 4. Brand header ────────────────────────────────────────────────────────
    fb  = _font(FONT_BOLD,  34)
    fl  = _font(FONT_LIGHT, 27)
    draw.text((M, 52), "SCALER SCHOOL", font=fb, fill=accent_dim)
    draw.text((M, 92), "OF BUSINESS",   font=fl, fill=(150,155,165))

    # Intake badge
    fbg = _font(FONT_BOLD, 27)
    btx = "INTAKE 3  APR 19"
    bb  = draw.textbbox((0,0), btx, font=fbg)
    bw2, bh2 = bb[2]-bb[0]+26, bb[3]-bb[1]+18
    bx2 = W-M-bw2
    draw.rounded_rectangle([bx2,54,bx2+bw2,54+bh2], radius=7,
                            fill=accent_soft, outline=accent_dim, width=1)
    draw.text((bx2+13, 62), btx, font=fbg, fill=accent_dim)

    # ── 5. Headline ────────────────────────────────────────────────────────────
    TW = W - M*2
    fh  = _font(FONT_BOLD, 76 if size=="9:16" else 54)
    fhs = _font(FONT_BOLD, 60 if size=="9:16" else 44)
    lines = _wrap(headline, fh, TW, draw)
    if len(lines) > 3:
        lines, fused, lh = _wrap(headline, fhs, TW, draw), fhs, 80
    else:
        fused, lh = fh, 96

    hy = int(H*0.375)
    for ln in lines[:4]:
        draw.text((M, hy), ln, font=fused, fill=WHITE)
        hy += lh

    # ── 6. Body ────────────────────────────────────────────────────────────────
    fbd = _font(FONT_REG, 37 if size=="9:16" else 30)
    bdy = (body[:150]+"...") if len(body)>150 else body
    by2 = hy+30
    for ln in _wrap(bdy, fbd, TW, draw)[:4]:
        draw.text((M, by2), ln, font=fbd, fill=WHITE_MED)
        by2 += 52

    # ── 7. Proof pills ─────────────────────────────────────────────────────────
    fpf   = _font(FONT_BOLD, 28)
    pills = ["100% PLACED", "68% PIVOTS", "Rs.50K DAY 1"]
    py    = int(H*0.735)
    px    = M
    PILL_BG      = _blend(WHITE, 25, BG)    # very dark near-BG tint
    PILL_OUTLINE = _blend(WHITE, 85, BG)    # slightly lighter
    for pill in pills:
        pb  = draw.textbbox((0,0), pill, font=fpf)
        pw  = pb[2]-pb[0]+24
        pht = pb[3]-pb[1]+16
        draw.rounded_rectangle([px, py, px+pw, py+pht], radius=6,
                                fill=PILL_BG, outline=PILL_OUTLINE, width=1)
        draw.text((px+12, py+8), pill, font=fpf, fill=WHITE_MED)
        px += pw+12

    # ── 8. Divider ─────────────────────────────────────────────────────────────
    dy = int(H*0.735)+58
    draw.line([(M,dy),(W-M,dy)], fill=_blend(WHITE,55,BG), width=1)

    # ── 9. CTA button ──────────────────────────────────────────────────────────
    fct  = _font(FONT_BOLD, 46)
    cy   = dy+36
    ctxt = cta[:38]+("..." if len(cta)>38 else "")
    cb   = draw.textbbox((0,0), ctxt, font=fct)
    cw   = min(cb[2]-cb[0]+64, W-M*2)
    ch   = 80
    draw.rounded_rectangle([M,cy,M+cw,cy+ch], radius=14, fill=accent)
    draw.text((M+32, cy+17), ctxt, font=fct, fill=BG)

    # ── 10. Footer ─────────────────────────────────────────────────────────────
    fwm = _font(FONT_LIGHT, 25)
    draw.text((M, H-50), "scaler.com/school-of-business",
              font=fwm, fill=_blend(WHITE,90,BG))
    fbk = _font(FONT_BOLD, 25)
    blt = f"#{bucket}"
    blb = draw.textbbox((0,0), blt, font=fbk)
    draw.text((W-M-(blb[2]-blb[0]), H-50), blt, font=fbk,
              fill=_blend(accent,160,BG))

    # ── Save ───────────────────────────────────────────────────────────────────
    out = os.path.join(OUTPUT_DIR, f"{ad_id}_{size.replace(':','x')}.png")
    canvas.save(out, "PNG", quality=95)
    return out
