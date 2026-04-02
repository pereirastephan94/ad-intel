"""
Creative Generator — renders a 1080x1920 (9:16) ad creative
using real SSB background images + copy overlay.

Design principles enforced:
  • Adaptive gradient: bright backgrounds get heavier darkening
  • Text shadow on all copy for legibility safety net
  • Pill/badge backgrounds adapt to sampled local brightness
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
BLACK     = (0, 0, 0)
SHADOW    = (5, 5, 15)

# SSB brand green — extracted from official logo (#1a8452)
SSB_GREEN = (26, 132, 82)

# Max 2 colours per creative: SSB_GREEN + WHITE
# All buckets use the same brand green — no random colours
BUCKET_COLORS = {
    "STARTUP":      SSB_GREEN,
    "OUTCOME":      SSB_GREEN,
    "CURRICULUM":   SSB_GREEN,
    "FACULTY":      SSB_GREEN,
    "SOCIAL_PROOF": SSB_GREEN,
    "URGENCY":      SSB_GREEN,
    "EMOTIONAL":    SSB_GREEN,
}

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../assets/ssb_images")
LOGOS_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../assets/logos")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Pre-load logo (white version for dark backgrounds)
_LOGO_WHITE_PATH = os.path.join(LOGOS_DIR, "ssb_logo_white.png")
_LOGO_GREEN_PATH = os.path.join(LOGOS_DIR, "ssb_logo_green.png")


def _font(spec, size):
    try:
        return ImageFont.truetype(spec[0], size, index=spec[1]) if isinstance(spec, tuple) \
               else ImageFont.truetype(spec, size)
    except Exception:
        return ImageFont.load_default()


def _clean(text):
    """Replace glyphs Helvetica can't render."""
    return (text.replace("\u2192",">").replace("\u2190","<").replace("\u2014","-")
                .replace("\u2019","'").replace("\u201c",'"').replace("\u201d",'"')
                .replace("\u2018","'"))


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


# ── Brightness analysis ───────────────────────────────────────────────────────

def _region_luminance(img, box):
    """Average perceived luminance (0-255) of a rectangular region.
    box = (x0, y0, x1, y1).  Uses ITU-R BT.601 weights."""
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(img.width, x1), min(img.height, y1)
    if x1 <= x0 or y1 <= y0:
        return 30  # assume dark
    region = img.crop((x0, y0, x1, y1)).resize((64, 64), Image.BILINEAR)
    pixels = list(region.getdata())
    total = sum(0.299*r + 0.587*g + 0.114*b for r, g, b in pixels)
    return total / len(pixels)


def _text_with_shadow(draw, pos, text, font, fill, shadow_color=SHADOW, offset=2):
    """Draw text with a dark shadow for legibility on any background."""
    x, y = pos
    draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)


# ── Image selection ───────────────────────────────────────────────────────────

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
    AVOID = {"ssb_5.webp", "ssb_6.webp", "ssb_7.webp"}
    all_ = glob.glob(os.path.join(ASSETS_DIR, "ssb_*.webp"))
    clean = [x for x in all_ if os.path.basename(x) not in AVOID]
    return clean[0] if clean else (all_[0] if all_ else None)


# ── Main generator ────────────────────────────────────────────────────────────

def generate_creative(ad: dict, image_path: str = None, size: str = "9:16") -> str:
    W, H = {"9:16":(1080,1920),"1:1":(1080,1080),"16:9":(1920,1080)}.get(size,(1080,1920))
    M = 76

    ad_id    = ad.get("ad_id", "AD")
    bucket   = ad.get("bucket", "STARTUP")
    headline = _clean(ad.get("headline", ""))
    body     = _clean(ad.get("primary_text", ""))
    cta      = _clean(ad.get("cta_text", "Apply Now >"))
    accent   = BUCKET_COLORS.get(bucket, (0, 212, 255))

    # Subheader: 45 char limit (design constraint). Truncate at word boundary.
    if len(body) > 45:
        trunc = body[:45]
        last_space = trunc.rfind(" ")
        if last_space > 25:
            body = trunc[:last_space]
        else:
            body = trunc

    # Pre-blended colour variants (will be recalculated if bg is bright)
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

    # ── 1b. Analyze brightness at key text zones BEFORE gradient ───────────────
    # Sample 3 horizontal bands where text will be drawn
    header_lum   = _region_luminance(canvas, (0, 0, W, int(H*0.15)))           # brand header
    headline_lum = _region_luminance(canvas, (0, int(H*0.35), W, int(H*0.60))) # headline+body
    bottom_lum   = _region_luminance(canvas, (0, int(H*0.70), W, H))           # pills+CTA+footer

    # Compute adaptive gradient strength
    # Higher values = more darkening.  Range: 0.6 (dark bg) to 1.4 (bright bg)
    avg_lum = (header_lum + headline_lum * 2 + bottom_lum) / 4
    if avg_lum > 170:       grad_strength = 1.4   # very bright photo
    elif avg_lum > 130:     grad_strength = 1.2   # medium-bright
    elif avg_lum > 80:      grad_strength = 1.0   # medium (current default)
    else:                   grad_strength = 0.7   # already dark — go lighter

    # ── 2. Adaptive gradient overlay ───────────────────────────────────────────
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    od = ImageDraw.Draw(ov)

    # Top fade (brand header area)
    top_alpha_max = int(min(200, 155 * grad_strength))
    for y in range(int(H*0.22)):
        od.line([(0,y),(W,y)], fill=(0,0,0, int(top_alpha_max*(1-y/(H*0.22)))))

    # Bottom fade (headline → footer)
    bot_start = int(H * max(0.30, 0.46 - (grad_strength - 1.0) * 0.16))  # starts higher when bright
    bot_alpha_min = int(min(240, 178 * grad_strength))
    bot_alpha_max = int(min(255, 255 * grad_strength))
    for y in range(bot_start, H):
        p = (y - bot_start) / (H - bot_start)
        alpha = int(bot_alpha_min + (bot_alpha_max - bot_alpha_min) * p)
        od.line([(0,y),(W,y)], fill=(10,10,26, min(255, alpha)))

    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")

    # ── 2b. Post-gradient luminance check — add local darkening if needed ──────
    post_headline_lum = _region_luminance(canvas, (M, int(H*0.35), W-M, int(H*0.60)))
    if post_headline_lum > 120:
        # Still too bright after gradient — add a semi-transparent dark rectangle
        dark_ov = Image.new("RGBA", (W, H), (0,0,0,0))
        dark_d  = ImageDraw.Draw(dark_ov)
        extra_alpha = min(180, int((post_headline_lum - 120) * 2.5))
        dark_d.rectangle(
            [0, int(H*0.33), W, int(H*0.72)],
            fill=(10, 10, 26, extra_alpha)
        )
        canvas = Image.alpha_composite(canvas.convert("RGBA"), dark_ov).convert("RGB")

    draw = ImageDraw.Draw(canvas)

    # ── 3. Left accent bar ─────────────────────────────────────────────────────
    bx = M - 22
    draw.rectangle([bx, int(H*0.355), bx+6, int(H*0.355)+int(H*0.32)], fill=accent)

    # ── 4. Brand logo (top-left, small) ───────────────────────────────────────
    logo_path = _LOGO_WHITE_PATH  # white logo for dark/photo backgrounds
    LOGO_H = 55  # target logo height in pixels (small, top-left)
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo_aspect = logo.width / logo.height
        logo_w = int(LOGO_H * logo_aspect)
        logo = logo.resize((logo_w, LOGO_H), Image.LANCZOS)
        # Paste with transparency onto canvas (need RGBA composite)
        logo_layer = Image.new("RGBA", canvas.size, (0,0,0,0))
        logo_layer.paste(logo, (M, 42))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), logo_layer).convert("RGB")
        draw = ImageDraw.Draw(canvas)  # re-create draw after composite
    except Exception:
        # Fallback: text header if logo file missing
        fb  = _font(FONT_BOLD,  34)
        fl  = _font(FONT_LIGHT, 27)
        _text_with_shadow(draw, (M, 52), "SCALER SCHOOL", fb, accent_dim)
        _text_with_shadow(draw, (M, 92), "OF BUSINESS",   fl, (150,155,165))

    # Intake badge
    fbg = _font(FONT_BOLD, 27)
    btx = "INTAKE 3  APR 19"
    bb  = draw.textbbox((0,0), btx, font=fbg)
    bw2, bh2 = bb[2]-bb[0]+26, bb[3]-bb[1]+18
    bx2 = W-M-bw2
    draw.rounded_rectangle([bx2,54,bx2+bw2,54+bh2], radius=7,
                            fill=accent_soft, outline=accent_dim, width=1)
    _text_with_shadow(draw, (bx2+13, 62), btx, fbg, accent_dim)

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
        _text_with_shadow(draw, (M, hy), ln, fused, WHITE, offset=3)
        hy += lh

    # ── 6. Body ────────────────────────────────────────────────────────────────
    fbd = _font(FONT_REG, 37 if size=="9:16" else 30)
    bdy = (body[:150]+"...") if len(body)>150 else body
    by2 = hy+30
    for ln in _wrap(bdy, fbd, TW, draw)[:4]:
        _text_with_shadow(draw, (M, by2), ln, fbd, WHITE_MED)
        by2 += 52

    # ── 7. Proof pills ────────────────────────────────────────────────────────
    fpf   = _font(FONT_BOLD, 28)
    pills = ["100% PLACED", "68% PIVOTS", "Rs.50K DAY 1"]
    py    = int(H*0.735)
    px    = M

    # Adaptive pill colors — sample local background brightness
    pill_zone_lum = _region_luminance(canvas, (M, py-5, W-M, py+45))
    if pill_zone_lum > 120:
        # Light background → dark pills
        PILL_BG      = (20, 20, 36)
        PILL_OUTLINE = (60, 60, 80)
        PILL_TEXT    = WHITE
    else:
        # Dark background → keep translucent look
        PILL_BG      = _blend(WHITE, 30, BG)
        PILL_OUTLINE = _blend(WHITE, 85, BG)
        PILL_TEXT    = WHITE_MED

    for pill in pills:
        pb  = draw.textbbox((0,0), pill, font=fpf)
        pw  = pb[2]-pb[0]+24
        pht = pb[3]-pb[1]+16
        draw.rounded_rectangle([px, py, px+pw, py+pht], radius=6,
                                fill=PILL_BG, outline=PILL_OUTLINE, width=1)
        draw.text((px+12, py+8), pill, font=fpf, fill=PILL_TEXT)
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
    _text_with_shadow(draw, (M, H-50), "scaler.com/school-of-business",
                      fwm, _blend(WHITE,120,BG))
    fbk = _font(FONT_BOLD, 25)
    blt = f"#{bucket}"
    blb = draw.textbbox((0,0), blt, font=fbk)
    _text_with_shadow(draw, (W-M-(blb[2]-blb[0]), H-50), blt,
                      fbk, _blend(accent,180,BG))

    # ── Save ───────────────────────────────────────────────────────────────────
    out = os.path.join(OUTPUT_DIR, f"{ad_id}_{size.replace(':','x')}.png")
    canvas.save(out, "PNG", quality=95)
    return out
