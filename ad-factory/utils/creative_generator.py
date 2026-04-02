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

            # Fit the entire image into the top portion of the canvas
            # — no cropping, the full photo is visible (person + background)
            # Image occupies the top ~65% of the canvas, text goes in the bottom 35%
            fit_h = int(H * 0.65)  # image fills top 65%
            fit_w = W

            img_ratio = bg.width / bg.height
            fit_ratio = fit_w / fit_h

            if img_ratio > fit_ratio:
                # Wider than slot → fit by width, image may be shorter
                nw = fit_w
                nh = int(fit_w / img_ratio)
            else:
                # Taller than slot → fit by height, image may be narrower
                nh = fit_h
                nw = int(fit_h * img_ratio)

            bg = bg.resize((nw, nh), Image.LANCZOS)
            # Center the image horizontally, top-align vertically
            x0 = (W - nw) // 2
            y0 = 0
            canvas.paste(bg, (x0, y0))

            # Soft blur on the very edges for a clean blend into dark BG
            # (only if image doesn't fill full width)
            if nw < W:
                bg_blur = bg.resize((W, nh), Image.LANCZOS).filter(ImageFilter.GaussianBlur(25))
                blur_layer = Image.new("RGB", (W, H), BG)
                blur_layer.paste(bg_blur, (0, 0))
                # Paste sharp image on top of blurred full-width version
                canvas.paste(blur_layer, (0, 0))
                canvas.paste(bg, (x0, y0))
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

    # Top fade (just enough for logo readability)
    top_alpha_max = int(min(160, 120 * grad_strength))
    for y in range(int(H*0.12)):
        od.line([(0,y),(W,y)], fill=(0,0,0, int(top_alpha_max*(1-y/(H*0.12)))))

    # Bottom fade — starts at ~55% to darken only the text zone at bottom
    bot_start = int(H * max(0.50, 0.60 - (grad_strength - 1.0) * 0.10))
    bot_alpha_min = int(min(220, 160 * grad_strength))
    bot_alpha_max = int(min(250, 240 * grad_strength))
    for y in range(bot_start, H):
        p = (y - bot_start) / (H - bot_start)
        alpha = int(bot_alpha_min + (bot_alpha_max - bot_alpha_min) * p)
        od.line([(0,y),(W,y)], fill=(10,10,26, min(255, alpha)))

    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")

    # ── 2b. Post-gradient luminance check — darken text zone if still bright ──
    post_text_lum = _region_luminance(canvas, (M, int(H*0.55), W-M, int(H*0.90)))
    if post_text_lum > 110:
        dark_ov = Image.new("RGBA", (W, H), (0,0,0,0))
        dark_d  = ImageDraw.Draw(dark_ov)
        extra_alpha = min(170, int((post_text_lum - 110) * 2.5))
        dark_d.rectangle(
            [0, int(H*0.50), W, H],
            fill=(10, 10, 26, extra_alpha)
        )
        canvas = Image.alpha_composite(canvas.convert("RGBA"), dark_ov).convert("RGB")

    draw = ImageDraw.Draw(canvas)

    # ── 3. Left accent bar (SSB green) — aligned with text block ─────────────
    bx = M - 22
    draw.rectangle([bx, int(H*0.66), bx+5, int(H*0.66)+int(H*0.14)], fill=accent)

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

    # ── 5. Headline ────────────────────────────────────────────────────────────
    TW = W - M*2
    fh  = _font(FONT_BOLD, 76 if size=="9:16" else 54)
    fhs = _font(FONT_BOLD, 60 if size=="9:16" else 44)
    lines = _wrap(headline, fh, TW, draw)
    if len(lines) > 3:
        lines, fused, lh = _wrap(headline, fhs, TW, draw), fhs, 80
    else:
        fused, lh = fh, 96

    # ── Text block at bottom 30% — maximum space for the photo subject ───────
    hy = int(H * 0.68)

    # Use smaller font if needed to keep everything in bottom 30%
    headline_font = fused
    headline_lh = lh
    if len(lines) > 2:
        headline_font = fhs
        lines = _wrap(headline, fhs, TW, draw)
        headline_lh = 72

    for ln in lines[:3]:
        _text_with_shadow(draw, (M, hy), ln, headline_font, WHITE, offset=3)
        hy += headline_lh

    # ── 6. Subheading (45 chars max) ──────────────────────────────────────────
    fbd = _font(FONT_REG, 32 if size=="9:16" else 26)
    by2 = hy + 8
    for ln in _wrap(body, fbd, TW, draw)[:2]:
        _text_with_shadow(draw, (M, by2), ln, fbd, WHITE_MED)
        by2 += 42

    # ── 7. Intake date + CTA on same row ─────────────────────────────────────
    fdate = _font(FONT_BOLD, 26)
    date_txt = "Intake 3 closes April 19"
    row_y = by2 + 16
    _text_with_shadow(draw, (M, row_y), date_txt, fdate, accent)

    fct  = _font(FONT_BOLD, 36)
    cy   = row_y + 38
    ctxt = "Apply Now"
    cb   = draw.textbbox((0,0), ctxt, font=fct)
    cw   = cb[2]-cb[0]+48
    ch   = 60
    draw.rounded_rectangle([M, cy, M+cw, cy+ch], radius=10, fill=accent)
    draw.text((M+24, cy+12), ctxt, font=fct, fill=WHITE)

    # ── 8. Footer ─────────────────────────────────────────────────────────────
    fwm = _font(FONT_LIGHT, 20)
    _text_with_shadow(draw, (M, H-36), "scaler.com/school-of-business",
                      fwm, _blend(WHITE,90,BG))

    # ── Save ───────────────────────────────────────────────────────────────────
    out = os.path.join(OUTPUT_DIR, f"{ad_id}_{size.replace(':','x')}.png")
    canvas.save(out, "PNG", quality=95)
    return out
