"""
🏭 AI Ad Creative Factory — Scaler School of Business
=====================================================
Start with a plain-English brief → Get 20 scored ad copies →
Pick the ones you like → Generate the actual 1080×1920 PNG creative.

Run: streamlit run app.py
"""
import streamlit as st
import json
import os
import sys
import base64
import pandas as pd
import plotly.express as px

sys.path.insert(0, '.')
from data.sample_data import SAMPLE_ADS, SAMPLE_SCORES

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ad Creative Factory | SSB",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0a0a1a; }
    .main-header {
        font-size: 2.4rem; font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header { color: #94a3b8; font-size: 1rem; margin-top: 0; }
    .score-card {
        background: linear-gradient(135deg, #1e1e3a, #2a2a4a);
        border-radius: 12px; padding: 16px; text-align: center;
        border: 1px solid #333366;
    }
    .score-big { font-size: 2.6rem; font-weight: 800; margin: 0; }
    .score-label { color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
    .verdict-launch { color: #22c55e; font-weight: 700; }
    .verdict-iterate { color: #f59e0b; font-weight: 700; }
    .verdict-rework { color: #f97316; font-weight: 700; }
    .verdict-kill   { color: #ef4444; font-weight: 700; }
    .ad-card {
        background: #12122a; border-radius: 12px; padding: 20px;
        border-left: 4px solid #7c3aed; margin-bottom: 16px;
    }
    .bucket-tag {
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 600; margin-right: 5px;
    }
    .bucket-STARTUP      { background:#7c3aed22; color:#a78bfa; border:1px solid #7c3aed44; }
    .bucket-OUTCOME      { background:#22c55e22; color:#86efac; border:1px solid #22c55e44; }
    .bucket-CURRICULUM   { background:#06b6d422; color:#67e8f9; border:1px solid #06b6d444; }
    .bucket-FACULTY      { background:#f59e0b22; color:#fcd34d; border:1px solid #f59e0b44; }
    .bucket-SOCIAL_PROOF { background:#ec489922; color:#f9a8d4; border:1px solid #ec489944; }
    .bucket-URGENCY      { background:#ef444422; color:#fca5a5; border:1px solid #ef444444; }
    .bucket-EMOTIONAL    { background:#8b5cf622; color:#c4b5fd; border:1px solid #8b5cf644; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
    .brief-box {
        background: #12122a; border-radius: 14px; padding: 28px;
        border: 1px solid #2a2a4a; margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def score_color(s):
    if s >= 80: return "#22c55e"
    elif s >= 60: return "#f59e0b"
    elif s >= 40: return "#f97316"
    return "#ef4444"


def bucket_html(b):
    return f'<span class="bucket-tag bucket-{b}">{b}</span>'


def parse_prompt_to_brief(prompt: str) -> dict:
    """Keyword-based brief parser — no API needed."""
    p = prompt.lower()

    audience = []
    if any(x in p for x in ["fresher", "graduate", "college", "first job", "entry level"]):
        audience.append("Ambitious Freshers")
    if any(x in p for x in ["professional", "career", "pivot", "switch", "corporate", "job change"]):
        audience.append("Career Pivoters (2-4 yrs exp)")
    if any(x in p for x in ["founder", "startup", "build", "entrepreneur", "venture", "d2c"]):
        audience.append("Aspiring Founders")
    if not audience:
        audience = ["Career Pivoters (2-4 yrs exp)", "Aspiring Founders"]

    buckets = []
    if any(x in p for x in ["startup", "d2c", "fund", "hustle", "capital", "₹50k", "50,000"]):
        buckets.append("STARTUP")
    if any(x in p for x in ["placement", "salary", "outcome", "hired", "job", "revenue", "20l", "crore"]):
        buckets.append("OUTCOME")
    if any(x in p for x in ["curriculum", "ai", "tools", "learn", "course", "150 hours", "product"]):
        buckets.append("CURRICULUM")
    if any(x in p for x in ["faculty", "mentor", "deepinder", "kunal", "binny", "founder teach"]):
        buckets.append("FACULTY")
    if any(x in p for x in ["student", "alumni", "story", "testimonial", "social proof", "real"]):
        buckets.append("SOCIAL_PROOF")
    if any(x in p for x in ["urgent", "deadline", "april 19", "last", "closing", "limited seats"]):
        buckets.append("URGENCY")
    if any(x in p for x in ["dream", "transform", "aspire", "future", "inspire", "emotional"]):
        buckets.append("EMOTIONAL")
    if not buckets:
        buckets = ["STARTUP", "OUTCOME", "SOCIAL_PROOF"]

    platforms = []
    if any(x in p for x in ["meta", "facebook", "instagram", "reel", "story", "feed"]):
        platforms += ["Meta Feed", "Meta Stories"]
    if any(x in p for x in ["google", "search", "display"]):
        platforms += ["Google Search", "Google Display"]
    if any(x in p for x in ["linkedin"]):
        platforms.append("LinkedIn")
    if any(x in p for x in ["youtube", "video", "pre-roll"]):
        platforms.append("YouTube")
    if not platforms:
        platforms = ["Meta Feed", "Google Search", "LinkedIn"]

    tone = "Bold"
    if any(x in p for x in ["professional", "serious", "formal"]):
        tone = "Professional"
    elif any(x in p for x in ["aggressive", "hard", "urgent"]):
        tone = "Aggressive"
    elif any(x in p for x in ["provocative", "controversial"]):
        tone = "Provocative"

    return {
        "num_ads": 20,
        "campaign_goal": prompt,
        "primary_audience": ", ".join(audience),
        "platforms": ", ".join(platforms),
        "tone": tone,
        "special_focus": ", ".join(buckets),
        "platform_mix": "Distribute evenly across selected platforms",
        "priority_buckets": ", ".join(buckets),
        "additional_context": "",
    }


def generate_ads_with_api(brief: dict, api_key: str):
    from prompts.p01_generate_ads import SYSTEM_PROMPT_GENERATE, USER_PROMPT_GENERATE
    client = anthropic.Anthropic(api_key=api_key)
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=8000,
        system=SYSTEM_PROMPT_GENERATE,
        messages=[{"role": "user", "content": USER_PROMPT_GENERATE.format(**brief)}]
    )
    return json.loads(r.content[0].text)


def score_ads_with_api(ads, api_key: str):
    from prompts.p03_judge_ads import SYSTEM_PROMPT_JUDGE, USER_PROMPT_JUDGE_BATCH
    client = anthropic.Anthropic(api_key=api_key)
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=8000,
        system=SYSTEM_PROMPT_JUDGE,
        messages=[{"role": "user", "content": USER_PROMPT_JUDGE_BATCH.format(
            num_ads=len(ads), ads_json=json.dumps(ads, indent=2)
        )}]
    )
    return json.loads(r.content[0].text)


def render_creative(ad: dict, size: str = "9:16", bg_image: str = None) -> str | None:
    """Call creative_generator and return path to PNG, or None on error."""
    try:
        from utils.creative_generator import generate_creative, pick_best_image
        img_path = bg_image if bg_image else pick_best_image(ad.get("bucket"))
        return generate_creative(ad, image_path=img_path, size=size)
    except Exception as e:
        st.error(f"Creative render failed: {e}")
        return None


def img_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ── Design Principles Prompt (7 principles, pick max 2) ───────────────────────
DESIGN_STRATEGIST_PROMPT = """You are a high-performance creative strategist and visual designer.

Your task is to generate a creative direction for a marketing ad background image using:
1. The uploaded photo (described below)
2. The ad copy/message
3. The target audience

### DESIGN PRINCIPLES (pick MAXIMUM 2):
- Balance: Distributes elements for a stable, structured layout
- Repetition: Repeats elements for consistency and flow
- Contrast: Uses differences to highlight key elements
- Proportion: Scales elements for balance and focus
- Emphasis: Draws attention to important details
- Unity: Ensures a cohesive, harmonious look
- Movement: Guides the eye through the design

### HARD RULES:
- Do NOT overload the creative
- Do NOT use more than 2 principles
- Prioritise clarity > aesthetics
- Design for mobile-first (9:16 portrait)
- The output image must have NO text, NO logos — just the enhanced photo as ad background

### YOUR TASK:
1. Pick the 2 best design principles for this audience + message
2. Write a single image generation prompt (max 80 words) that describes
   how to recreate this photo as a professional ad background following
   those 2 principles. Include: the scene, people, lighting, mood, color grading,
   and how the 2 chosen principles shape the composition.

Return ONLY the image generation prompt, nothing else."""


# ── Grok image pipeline ──────────────────────────────────────────────────────

def _grok_headers(api_key: str) -> dict:
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _grok_describe_photo(photo_path: str, api_key: str) -> str:
    """Use Grok vision to describe an uploaded photo."""
    import base64, requests
    with open(photo_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = photo_path.rsplit(".", 1)[-1].lower()
    mime = {"jpg":"jpeg","jpeg":"jpeg","png":"png","webp":"webp"}.get(ext, "jpeg")
    resp = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers=_grok_headers(api_key),
        json={
            "model": "grok-4-fast-non-reasoning",
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/{mime};base64,{b64}"}},
                {"type": "text", "text": (
                    "Describe this photo in 2 sentences. Focus on the people, their activity, "
                    "the setting, lighting, colors, and mood. Be specific and visual."
                )}
            ]}],
            "max_tokens": 200
        },
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _grok_design_direction(photo_desc: str, ad: dict, api_key: str) -> str:
    """Use Grok strategist to pick 2 design principles and write an image prompt."""
    import requests
    audience = ad.get("audience_segment", "career pivoters and aspiring founders")
    headline = ad.get("headline", "")
    bucket   = ad.get("bucket", "STARTUP")
    resp = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers=_grok_headers(api_key),
        json={
            "model": "grok-4-fast-non-reasoning",
            "messages": [
                {"role": "system", "content": DESIGN_STRATEGIST_PROMPT},
                {"role": "user", "content": (
                    f"PHOTO DESCRIPTION: {photo_desc}\n\n"
                    f"AD HEADLINE: {headline}\n"
                    f"BUCKET: {bucket}\n"
                    f"TARGET AUDIENCE: {audience}\n"
                    f"OBJECTIVE: Lead generation for Scaler School of Business\n\n"
                    f"Write the image generation prompt."
                )}
            ],
            "max_tokens": 200
        },
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _grok_generate_image(prompt: str, api_key: str, slug: str) -> str | None:
    """Generate an image with grok-imagine-image and save it."""
    import requests
    out_dir = os.path.join(os.path.dirname(__file__), "assets", "ssb_images", "enhanced")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slug}.jpg")
    if os.path.exists(out_path):
        return out_path

    resp = requests.post(
        "https://api.x.ai/v1/images/generations",
        headers=_grok_headers(api_key),
        json={"model": "grok-imagine-image", "prompt": prompt, "response_format": "url"},
        timeout=90
    )
    resp.raise_for_status()
    url = resp.json()["data"][0]["url"]
    img_data = requests.get(url, timeout=30).content
    with open(out_path, "wb") as f:
        f.write(img_data)
    return out_path


def enhance_photo_with_grok(photo_path: str, ad: dict, api_key: str) -> str | None:
    """
    Full Grok pipeline:
    1. Vision describes the uploaded photo
    2. Strategist picks 2 design principles + writes image prompt
    3. Imagine generates the enhanced ad-ready background
    Returns path to enhanced image, or None on failure.
    """
    import hashlib
    try:
        slug = hashlib.md5(f"{photo_path}_{ad.get('ad_id','')}".encode()).hexdigest()[:10]

        # Check cache
        cached = os.path.join(os.path.dirname(__file__), "assets", "ssb_images", "enhanced", f"{slug}.jpg")
        if os.path.exists(cached):
            return cached

        # Step 1: Describe photo
        desc = _grok_describe_photo(photo_path, api_key)

        # Step 2: Design direction (picks 2 principles, writes image prompt)
        img_prompt = _grok_design_direction(desc, ad, api_key)

        # Step 3: Generate enhanced background
        return _grok_generate_image(img_prompt, api_key, slug)

    except Exception as e:
        st.warning(f"Grok enhancement failed: {e}")
        return None


def generate_ai_background(prompt: str, api_key: str) -> str | None:
    """Generate an image from scratch with Grok (when no uploaded photo)."""
    import hashlib, requests
    slug = hashlib.md5(prompt.encode()).hexdigest()[:8]
    out_dir = os.path.join(os.path.dirname(__file__), "assets", "ssb_images")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"ai_bg_{slug}.jpg")
    if os.path.exists(out_path):
        return out_path
    try:
        resp = requests.post(
            "https://api.x.ai/v1/images/generations",
            headers=_grok_headers(api_key),
            json={"model": "grok-imagine-image", "prompt": prompt, "response_format": "url"},
            timeout=90
        )
        resp.raise_for_status()
        url = resp.json()["data"][0]["url"]
        img_data = requests.get(url, timeout=30).content
        with open(out_path, "wb") as f:
            f.write(img_data)
        return out_path
    except Exception as e:
        st.warning(f"Grok image generation failed: {e}")
        return None


def _save_uploaded_images(uploaded_files, ad_id: str) -> list[str]:
    """Save uploaded files to disk and return list of paths."""
    import hashlib
    out_dir = os.path.join(os.path.dirname(__file__), "assets", "ssb_images", "uploads")
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, uf in enumerate(uploaded_files):
        ext = os.path.splitext(uf.name)[1] or ".jpg"
        slug = hashlib.md5(uf.getvalue()[:1024]).hexdigest()[:6]
        path = os.path.join(out_dir, f"{ad_id}_{slug}{ext}")
        with open(path, "wb") as f:
            f.write(uf.getbuffer())
        paths.append(path)
    return paths


# ── Session state init ─────────────────────────────────────────────────────────
for key in ["ads", "scores", "generated_creatives"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "generated_creatives" else {}


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="main-header">🏭 AI Ad Creative Factory</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Scaler School of Business — Intake 3 | Type a brief → get 20 scored copies → pick the best → generate the PNG</p>',
            unsafe_allow_html=True)

st.divider()


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — BRIEF
# ══════════════════════════════════════════════════════════════════════════════
with st.container():
    st.markdown("### Step 1 — Describe what you want")

    col_brief, col_opts = st.columns([3, 1])

    with col_brief:
        user_prompt = st.text_area(
            "Your campaign brief",
            height=100,
            placeholder=(
                "e.g.  Create a Meta campaign around how our students built a D2C brand "
                "to ₹20L revenue. Real student photos in the background for authenticity. "
                "Target career pivoters and aspiring founders. Deadline: April 19."
            ),
            label_visibility="collapsed",
        )

    with col_opts:
        mode = st.radio("Mode", ["🎭 Demo", "🔑 Live (Claude API)"], index=0)
        api_key = None
        if mode == "🔑 Live (Claude API)":
            api_key = st.text_input("Anthropic API key", type="password")

    generate_btn = st.button("🚀 Generate Ad Copies", type="primary", use_container_width=False)

    # Grok API key — primary image tool
    with st.expander("🎨 Grok Image Settings", expanded=False):
        st.caption(
            "Grok enhances your uploaded photos into ad-ready backgrounds using design principles "
            "(Balance, Contrast, Emphasis, etc.). Upload photos per ad card below."
        )
        grok_api_key = st.text_input(
            "Grok API key (xAI)", type="password",
            help="Get yours at console.x.ai",
        )


# ── Generate on button click ──────────────────────────────────────────────────
if generate_btn:
    if mode == "🎭 Demo":
        with st.spinner("Loading demo data…"):
            st.session_state.ads    = SAMPLE_ADS
            st.session_state.scores = SAMPLE_SCORES
        st.success("✅ Loaded 20 demo ads — scroll down to browse and generate creatives!")
    else:
        if not api_key:
            st.error("Add your Anthropic API key to use live mode.")
        else:
            brief = parse_prompt_to_brief(user_prompt or "Drive Intake 3 applications — April 19 deadline")
            with st.spinner("🧠 Generating 20 ad copies with Claude…"):
                try:
                    st.session_state.ads = generate_ads_with_api(brief, api_key)
                except Exception as e:
                    st.error(f"Generation error: {e}")
                    st.session_state.ads = SAMPLE_ADS

            with st.spinner("⚖️ Scoring all 20 ads…"):
                try:
                    st.session_state.scores = score_ads_with_api(st.session_state.ads, api_key)
                except Exception as e:
                    st.error(f"Scoring error: {e}")
                    st.session_state.scores = SAMPLE_SCORES

            st.success(f"✅ {len(st.session_state.ads)} ads generated and scored!")


# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.ads and st.session_state.scores:
    ads    = st.session_state.ads
    scores = st.session_state.scores

    scores_sorted = sorted(scores, key=lambda x: x["composite_score"], reverse=True)
    ad_lookup     = {a["ad_id"]: a for a in ads}
    score_lookup  = {s["ad_id"]: s for s in scores}

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 Top 5 Ads", "📊 Scoreboard", "📈 Analytics", "🔍 All Ads", "🎯 Recommendations"
    ])


    # ── helper: creative card with "Generate Creative" button ─────────────────
    def creative_card(rank_label, s, ad, key_prefix):
        bucket  = s.get("bucket", ad.get("bucket", "STARTUP"))
        score   = s["composite_score"]
        verdict = s["verdict"]

        col_copy, col_score = st.columns([3, 1])

        with col_copy:
            st.markdown(f"""
            <div class="ad-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <div>
                        <span style="font-size:1.3rem;font-weight:800;color:#e2e8f0;">{rank_label}</span>
                        <span style="margin-left:8px;color:#94a3b8;font-size:0.8rem;">{s['ad_id']}</span>
                        {bucket_html(bucket)}
                        <span class="bucket-tag" style="background:#1e293b;color:#94a3b8;border:1px solid #334155;">{ad.get('platform','')}</span>
                    </div>
                    <span class="verdict-{verdict.lower()}" style="font-size:1rem;">{verdict}</span>
                </div>
                <h3 style="color:#f1f5f9;margin:0 0 8px 0;font-size:1.15rem;">{ad.get('headline','')}</h3>
                <p style="color:#cbd5e1;font-size:0.92rem;line-height:1.6;margin:0 0 10px 0;">{ad.get('primary_text','')}</p>
                <div style="border-top:1px solid #1e293b;padding-top:8px;">
                    <span style="color:#22c55e;font-size:0.82rem;">💪 {s.get('top_strength','')}</span><br>
                    <span style="color:#f59e0b;font-size:0.82rem;">🔧 {s.get('improvement','')}</span>
                </div>
                <div style="margin-top:8px;">
                    <span style="color:#7c3aed;font-size:0.82rem;">🎯 CTA: <strong>{ad.get('cta_text','')}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_score:
            st.markdown(f"""
            <div class="score-card">
                <p class="score-big" style="color:{score_color(score)}">{score}</p>
                <p class="score-label">Composite Score</p>
            </div>
            """, unsafe_allow_html=True)

            dims = s.get("scores", {})
            if isinstance(dims, dict):
                for dim, val in dims.items():
                    if isinstance(val, (int, float)):
                        st.progress(val / 10, text=f"{dim}: {val}/10")

        # ── Image upload + Generate Creative ─────────────────────────────────────
        with st.container():
            g_col1, g_col2, g_col3 = st.columns([1, 1, 2])
            with g_col1:
                size_choice = st.selectbox(
                    "Format", ["9:16 (Meta/Reels)", "1:1 (Square)", "16:9 (YouTube)"],
                    key=f"size_{key_prefix}", label_visibility="collapsed"
                )
            with g_col2:
                gen_btn = st.button(
                    "🎨 Generate Creative",
                    key=f"gen_{key_prefix}",
                    help="Renders one PNG per uploaded image, or one using the default/AI background"
                )

            # Image upload — 1 to 10 custom background images
            uploaded_imgs = st.file_uploader(
                "Upload background images (1-10)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
                key=f"upload_{key_prefix}",
                help="Drop your own photos here. One creative will be generated per image."
            )

            size_code = size_choice.split()[0]  # "9:16", "1:1", or "16:9"

            if gen_btn:
                ad_id = s["ad_id"]

                if uploaded_imgs:
                    # ── Batch: one creative per uploaded image ─────────────────
                    saved = _save_uploaded_images(uploaded_imgs[:10], ad_id)
                    results = []
                    total_steps = len(saved) * (2 if grok_api_key else 1)
                    progress = st.progress(0, text="Processing…")
                    step = 0

                    for idx, img_path in enumerate(saved):
                        bg = img_path  # default: use raw upload

                        # Grok enhancement: vision → design principles → regenerate
                        if grok_api_key:
                            progress.progress(
                                (step + 1) / total_steps,
                                text=f"🧠 Grok analyzing photo {idx+1}/{len(saved)} (picking design principles)…"
                            )
                            enhanced = enhance_photo_with_grok(img_path, ad, grok_api_key)
                            if enhanced:
                                bg = enhanced
                            step += 1

                        progress.progress(
                            (step + 1) / total_steps,
                            text=f"🎨 Rendering creative {idx+1}/{len(saved)}…"
                        )
                        path = render_creative(ad, size=size_code, bg_image=bg)
                        if path:
                            results.append(path)
                        step += 1

                    progress.empty()

                    for i, p in enumerate(results):
                        st.session_state.generated_creatives[f"{ad_id}_{size_code}_u{i}"] = p
                    if results:
                        st.success(f"✅ {len(results)} creative(s) rendered with design principles!")

                else:
                    # ── No uploads: Grok generates from scratch or use SSB photo ──
                    bg_img = None
                    if grok_api_key:
                        bg_prompt = (
                            f"Young Indian business students {ad.get('image_prompt', 'in a modern classroom setting')}, "
                            "photorealistic, cinematic warm natural light, shallow depth of field, "
                            "professional ad background, portrait 9:16, authentic, no text overlay"
                        )
                        with st.spinner("🖼️ Grok generating background…"):
                            bg_img = generate_ai_background(bg_prompt, grok_api_key)

                    with st.spinner(f"Rendering {size_code} creative for {ad_id}…"):
                        path = render_creative(ad, size=size_code, bg_image=bg_img)

                    if path:
                        st.session_state.generated_creatives[f"{ad_id}_{size_code}"] = path

            # ── Show generated creatives (gallery) ────────────────────────────
            ad_id_for_cache = s["ad_id"]
            # Collect all cached creatives for this ad+size (single + batch)
            matching = [(k, v) for k, v in st.session_state.generated_creatives.items()
                        if k.startswith(f"{ad_id_for_cache}_{size_code}") and os.path.exists(v)]

            if matching:
                cols = st.columns(min(len(matching), 3))
                for idx, (cache_key, img_path) in enumerate(matching):
                    with cols[idx % 3]:
                        st.image(img_path, caption=f"v{idx+1}", width=280)
                        with open(img_path, "rb") as f:
                            st.download_button(
                                f"⬇️ v{idx+1}",
                                data=f,
                                file_name=os.path.basename(img_path),
                                mime="image/png",
                                key=f"dl_{key_prefix}_{idx}",
                            )

        st.divider()


    # ── TAB 1: TOP 5 ──────────────────────────────────────────────────────────
    with tab1:
        st.markdown("### 🏆 Top 5 launch-ready ads")
        st.caption("Highest-scoring across hook strength, proof density, audience fit, visual concept, brand differentiation, CTA urgency, and platform fit.")

        for rank, s in enumerate(scores_sorted[:5], 1):
            ad = ad_lookup.get(s["ad_id"], {})
            creative_card(f"#{rank}", s, ad, key_prefix=f"top{rank}")


    # ── TAB 2: SCOREBOARD ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("### 📊 Full scoreboard — all ads ranked")

        df_data = []
        for s in scores_sorted:
            ad = ad_lookup.get(s["ad_id"], {})
            hl = ad.get("headline", "")
            df_data.append({
                "Rank":     len(df_data) + 1,
                "Ad ID":    s["ad_id"],
                "Score":    s["composite_score"],
                "Verdict":  s["verdict"],
                "Bucket":   s.get("bucket", ad.get("bucket", "")),
                "Platform": ad.get("platform", ""),
                "Audience": ad.get("audience_segment", ""),
                "Headline": hl[:60] + ("…" if len(hl) > 60 else ""),
            })

        df = pd.DataFrame(df_data)
        st.dataframe(
            df,
            column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d")},
            hide_index=True, use_container_width=True, height=700
        )


    # ── TAB 3: ANALYTICS ──────────────────────────────────────────────────────
    with tab3:
        st.markdown("### 📈 Creative performance analytics")

        avg_score    = sum(s["composite_score"] for s in scores) / len(scores)
        launch_count = sum(1 for s in scores if s["verdict"] == "LAUNCH")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Avg score",     f"{avg_score:.0f}/100")
        m2.metric("Launch-ready",  f"{launch_count}/{len(scores)}")
        m3.metric("Total ads",     len(scores))
        m4.metric("Top score",     scores_sorted[0]["composite_score"])

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            bucket_scores = {}
            for s in scores:
                b = s.get("bucket", "?")
                bucket_scores.setdefault(b, []).append(s["composite_score"])
            ba = {b: sum(v)/len(v) for b, v in bucket_scores.items()}
            fig1 = px.bar(x=list(ba.keys()), y=list(ba.values()),
                          title="Avg score by bucket", labels={"x":"Bucket","y":"Avg Score"},
                          color=list(ba.values()), color_continuous_scale="viridis")
            fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#94a3b8", showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            verdicts = [s["verdict"] for s in scores]
            vc = {v: verdicts.count(v) for v in set(verdicts)}
            colors = {"LAUNCH":"#22c55e","ITERATE":"#f59e0b","REWORK":"#f97316","KILL":"#ef4444"}
            fig2 = px.pie(names=list(vc.keys()), values=list(vc.values()),
                          title="Verdict distribution",
                          color=list(vc.keys()), color_discrete_map=colors)
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#94a3b8")
            st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.histogram(x=[s["composite_score"] for s in scores], nbins=10,
                            title="Score distribution", labels={"x":"Score","y":"Count"},
                            color_discrete_sequence=["#7c3aed"])
        fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           font_color="#94a3b8")
        st.plotly_chart(fig3, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            ps = {}
            for s in scores:
                ad = ad_lookup.get(s["ad_id"], {})
                ps.setdefault(ad.get("platform","?"), []).append(s["composite_score"])
            pa = {p: sum(v)/len(v) for p, v in ps.items()}
            fig4 = px.bar(x=list(pa.keys()), y=list(pa.values()),
                          title="Avg score by platform", color_discrete_sequence=["#06b6d4"])
            fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#94a3b8")
            st.plotly_chart(fig4, use_container_width=True)

        with c4:
            aus = {}
            for s in scores:
                ad = ad_lookup.get(s["ad_id"], {})
                aus.setdefault(ad.get("audience_segment","?"), []).append(s["composite_score"])
            aa = {a: sum(v)/len(v) for a, v in aus.items()}
            fig5 = px.bar(x=list(aa.keys()), y=list(aa.values()),
                          title="Avg score by audience", color_discrete_sequence=["#ec4899"])
            fig5.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               font_color="#94a3b8")
            st.plotly_chart(fig5, use_container_width=True)


    # ── TAB 4: ALL ADS ────────────────────────────────────────────────────────
    with tab4:
        st.markdown("### 🔍 Browse all generated ads")
        st.caption("Use the 'Generate Creative' button on any ad to render the actual PNG.")

        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filter_bucket = st.selectbox("Bucket", ["All"] + sorted(set(
                s.get("bucket", ad_lookup.get(s["ad_id"], {}).get("bucket", "")) for s in scores
            )))
        with fc2:
            filter_verdict = st.selectbox("Verdict", ["All", "LAUNCH", "ITERATE", "REWORK", "KILL"])
        with fc3:
            filter_platform = st.selectbox("Platform", ["All"] + sorted(set(
                ad_lookup.get(s["ad_id"], {}).get("platform", "") for s in scores
            )))

        shown = 0
        for i, s in enumerate(scores_sorted):
            ad = ad_lookup.get(s["ad_id"], {})
            bucket   = s.get("bucket", ad.get("bucket", ""))
            platform = ad.get("platform", "")

            if filter_bucket  != "All" and bucket   != filter_bucket:  continue
            if filter_verdict != "All" and s["verdict"] != filter_verdict: continue
            if filter_platform != "All" and platform != filter_platform: continue

            with st.expander(
                f"**{s['ad_id']}** | {s['composite_score']}/100 | {s['verdict']} | {bucket} | {platform}"
            ):
                creative_card("", s, ad, key_prefix=f"all{i}")
                with st.container():
                    st.markdown(f"**Audience:** {ad.get('audience_segment','')}")
                    st.markdown(f"**Hook type:** {ad.get('hook_type','')}")
                    st.markdown(f"**Key proof point:** {ad.get('key_proof_point','')}")
                    if ad.get("image_prompt"):
                        st.markdown(f"🎨 **Image concept:** {ad['image_prompt']}")
                    if ad.get("video_script"):
                        st.markdown(f"🎬 **Video script:** {ad['video_script']}")
            shown += 1

        if shown == 0:
            st.info("No ads match the current filters.")


    # ── TAB 5: RECOMMENDATIONS ────────────────────────────────────────────────
    with tab5:
        st.markdown("### 🎯 Strategic recommendations")

        st.markdown("""
        <div class="ad-card" style="border-left-color:#22c55e;">
            <h4 style="color:#22c55e;margin-top:0;">✅ Immediate wins</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>Double down on STARTUP bucket</strong> — top-scoring ads all leverage the ₹25L Hustle Program + D2C Challenge. No competitor can match this.</li>
                <li><strong>Lead every ad with a specific proof point</strong> — named students + company logos score 15–20 pts higher than generic claims.</li>
                <li><strong>Add "April 19" to ALL ads</strong> — urgency in CTA lifts score ~8 pts on average.</li>
            </ol>
        </div>
        <div class="ad-card" style="border-left-color:#f59e0b;">
            <h4 style="color:#f59e0b;margin-top:0;">⚠️ Gaps to fill</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>Video is underdeveloped</strong> — generate more YouTube pre-roll + Instagram Reels scripts. Video has 2× engagement on Meta.</li>
                <li><strong>Founders segment is underserved</strong> — only 5/20 ads target aspiring founders. This is SSB's strongest unique angle.</li>
                <li><strong>Google Search lacks differentiation</strong> — current search ads are functional but generic. Add more SSB-specific angles.</li>
            </ol>
        </div>
        <div class="ad-card" style="border-left-color:#7c3aed;">
            <h4 style="color:#7c3aed;margin-top:0;">🧪 Creative angles to test next</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>"Your office has a startup floor"</strong> — campus ecosystem angle. No IIM, MU, or MESA can claim 10+ live startups on campus.</li>
                <li><strong>"₹50K on Day 1"</strong> — D2C challenge funding as a hook. Tangible, immediate, unique.</li>
                <li><strong>"Scaler placed more people in Amazon than all IITs"</strong> — legacy proof transferred to SSB credibility.</li>
                <li><strong>Student founder vs. MBA student side-by-side</strong> — visual showing what SSB students DO vs what MBA students STUDY.</li>
            </ol>
        </div>
        <div class="ad-card" style="border-left-color:#06b6d4;">
            <h4 style="color:#06b6d4;margin-top:0;">💰 Suggested budget split</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>Meta (Feed + Stories): 45%</strong> — highest creative flexibility, best for visual storytelling and social proof</li>
                <li><strong>Google Search: 25%</strong> — high-intent "business school" and "career change" traffic</li>
                <li><strong>LinkedIn: 20%</strong> — career pivoters most active here</li>
                <li><strong>YouTube: 10%</strong> — video pre-roll for awareness; retarget search visitors</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#475569;font-size:0.82rem;">
    🏭 AI Ad Creative Factory — Scaler School of Business &nbsp;|&nbsp;
    Claude API + Streamlit + Pillow &nbsp;|&nbsp; Intake 3 — April 2026
</div>
""", unsafe_allow_html=True)
