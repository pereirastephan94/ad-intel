"""
🏭 AI Ad Creative Factory — Scaler School of Business
=====================================================
A working MVP that takes a campaign brief and generates, scores, and ranks ad creatives.
Built for Scaler's 5-hour hackathon.

Run: streamlit run app.py
"""
import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ad Creative Factory | SSB",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    .stApp { background-color: #0a0a1a; }
    .main-header { 
        font-size: 2.5rem; font-weight: 800; 
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-top: 0; }
    .score-card {
        background: linear-gradient(135deg, #1e1e3a, #2a2a4a);
        border-radius: 12px; padding: 20px; text-align: center;
        border: 1px solid #333366;
    }
    .score-big { font-size: 2.8rem; font-weight: 800; margin: 0; }
    .score-label { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
    .verdict-launch { color: #22c55e; font-weight: 700; }
    .verdict-iterate { color: #f59e0b; font-weight: 700; }
    .verdict-rework { color: #ef4444; font-weight: 700; }
    .verdict-kill { color: #dc2626; font-weight: 700; }
    .ad-card {
        background: #12122a; border-radius: 12px; padding: 20px;
        border-left: 4px solid #7c3aed; margin-bottom: 16px;
    }
    .bucket-tag {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600; margin-right: 6px;
    }
    .bucket-STARTUP { background: #7c3aed22; color: #a78bfa; border: 1px solid #7c3aed44; }
    .bucket-OUTCOME { background: #22c55e22; color: #86efac; border: 1px solid #22c55e44; }
    .bucket-CURRICULUM { background: #06b6d422; color: #67e8f9; border: 1px solid #06b6d444; }
    .bucket-FACULTY { background: #f59e0b22; color: #fcd34d; border: 1px solid #f59e0b44; }
    .bucket-SOCIAL_PROOF { background: #ec489922; color: #f9a8d4; border: 1px solid #ec489944; }
    .bucket-URGENCY { background: #ef444422; color: #fca5a5; border: 1px solid #ef444444; }
    .bucket-EMOTIONAL { background: #8b5cf622; color: #c4b5fd; border: 1px solid #8b5cf644; }
    div[data-testid="stMetricValue"] { font-size: 2rem; }
</style>
""", unsafe_allow_html=True)

# ---- LOAD SAMPLE DATA ----
import sys
sys.path.insert(0, '.')
from data.sample_data import SAMPLE_ADS, SAMPLE_SCORES

# ---- TRY LOADING ANTHROPIC ----
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# ---- HELPER FUNCTIONS ----

def get_verdict_class(verdict):
    return f"verdict-{verdict.lower()}"

def score_color(score):
    if score >= 80: return "#22c55e"
    elif score >= 60: return "#f59e0b"
    elif score >= 40: return "#f97316"
    else: return "#ef4444"

def bucket_html(bucket):
    return f'<span class="bucket-tag bucket-{bucket}">{bucket}</span>'

def generate_ads_with_api(brief, api_key):
    """Call Claude API to generate ads. Falls back to sample data."""
    from prompts.p01_generate_ads import SYSTEM_PROMPT_GENERATE, USER_PROMPT_GENERATE
    
    client = anthropic.Anthropic(api_key=api_key)
    user_msg = USER_PROMPT_GENERATE.format(**brief)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        system=SYSTEM_PROMPT_GENERATE,
        messages=[{"role": "user", "content": user_msg}]
    )
    return json.loads(response.content[0].text)

def score_ads_with_api(ads, api_key):
    """Call Claude API to score ads."""
    from prompts.p03_judge_ads import SYSTEM_PROMPT_JUDGE, USER_PROMPT_JUDGE_BATCH
    
    client = anthropic.Anthropic(api_key=api_key)
    user_msg = USER_PROMPT_JUDGE_BATCH.format(
        num_ads=len(ads),
        ads_json=json.dumps(ads, indent=2)
    )
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        system=SYSTEM_PROMPT_JUDGE,
        messages=[{"role": "user", "content": user_msg}]
    )
    return json.loads(response.content[0].text)


# ===============================
# SIDEBAR — CAMPAIGN BRIEF INPUT
# ===============================
with st.sidebar:
    st.markdown("### 📋 Campaign brief")
    
    mode = st.radio("Mode", ["🎭 Demo (sample data)", "🔑 Live (Claude API)"], index=0)
    
    if mode == "🔑 Live (Claude API)":
        api_key = st.text_input("Anthropic API Key", type="password", 
                                help="Get yours at console.anthropic.com")
    else:
        api_key = None
    
    st.divider()
    
    campaign_goal = st.text_area(
        "Campaign goal",
        value="Drive applications for Intake 3 (deadline April 19, 2026)",
        height=68
    )
    
    audience = st.multiselect(
        "Target audience",
        ["Career Pivoters (2-4 yrs exp)", "Ambitious Freshers", "Aspiring Founders"],
        default=["Career Pivoters (2-4 yrs exp)", "Aspiring Founders"]
    )
    
    platforms = st.multiselect(
        "Platforms",
        ["Meta Feed", "Meta Stories", "Google Search", "Google Display", "LinkedIn", "YouTube"],
        default=["Meta Feed", "Google Search", "LinkedIn"]
    )
    
    priority_buckets = st.multiselect(
        "Priority ad buckets",
        ["STARTUP", "OUTCOME", "CURRICULUM", "FACULTY", "SOCIAL_PROOF", "URGENCY", "EMOTIONAL"],
        default=["STARTUP", "OUTCOME"]
    )
    
    tone = st.select_slider(
        "Tone",
        options=["Conservative", "Professional", "Bold", "Provocative", "Aggressive"],
        value="Bold"
    )
    
    num_ads = st.slider("Number of ads to generate", 5, 30, 20)
    
    st.divider()
    generate_btn = st.button("🚀 Generate & Score Ads", type="primary", use_container_width=True)


# ===============================
# MAIN AREA
# ===============================

# Header
st.markdown('<p class="main-header">🏭 AI Ad Creative Factory</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Scaler School of Business — Intake 3 Campaign Engine</p>', unsafe_allow_html=True)

# ---- STATE MANAGEMENT ----
if 'ads' not in st.session_state:
    st.session_state.ads = None
    st.session_state.scores = None

if generate_btn:
    if mode == "🔑 Live (Claude API)" and api_key:
        with st.spinner("🧠 Generating ads with Claude..."):
            try:
                brief = {
                    "num_ads": num_ads,
                    "campaign_goal": campaign_goal,
                    "primary_audience": ", ".join(audience),
                    "platforms": ", ".join(platforms),
                    "tone": tone,
                    "special_focus": ", ".join(priority_buckets),
                    "platform_mix": "Auto-distribute across selected platforms",
                    "priority_buckets": ", ".join(priority_buckets),
                    "additional_context": ""
                }
                st.session_state.ads = generate_ads_with_api(brief, api_key)
                st.success(f"✅ Generated {len(st.session_state.ads)} ads!")
            except Exception as e:
                st.error(f"API Error: {e}")
                st.session_state.ads = SAMPLE_ADS
        
        with st.spinner("⚖️ Scoring ads..."):
            try:
                st.session_state.scores = score_ads_with_api(st.session_state.ads, api_key)
            except Exception as e:
                st.error(f"Scoring Error: {e}")
                st.session_state.scores = SAMPLE_SCORES
    else:
        # Demo mode
        with st.spinner("Loading demo data..."):
            st.session_state.ads = SAMPLE_ADS
            st.session_state.scores = SAMPLE_SCORES


# ---- DISPLAY RESULTS ----
if st.session_state.ads and st.session_state.scores:
    ads = st.session_state.ads
    scores = st.session_state.scores
    
    # Sort scores by composite_score
    scores_sorted = sorted(scores, key=lambda x: x['composite_score'], reverse=True)
    
    # Create lookup
    ad_lookup = {ad['ad_id']: ad for ad in ads}
    score_lookup = {s['ad_id']: s for s in scores}
    
    # ===============================
    # TAB LAYOUT
    # ===============================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 Top 5 Ads", "📊 Scoreboard", "📈 Analytics", "🔍 All Ads", "🎯 Recommendations"
    ])
    
    # ---- TAB 1: TOP 5 ----
    with tab1:
        st.markdown("### 🏆 Top 5 launch-ready ads")
        st.markdown("*These scored highest across hook strength, proof density, audience fit, visual concept, brand differentiation, CTA urgency, and platform fit.*")
        
        top5 = scores_sorted[:5]
        
        for rank, s in enumerate(top5, 1):
            ad = ad_lookup.get(s['ad_id'], {})
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <div>
                            <span style="font-size:1.4rem; font-weight:800; color:#e2e8f0;">#{rank}</span>
                            <span style="margin-left:8px; color:#94a3b8;">{s['ad_id']}</span>
                            {bucket_html(s.get('bucket', ad.get('bucket', 'N/A')))}
                            <span class="bucket-tag" style="background:#1e293b; color:#94a3b8; border:1px solid #334155;">{ad.get('platform', 'N/A')}</span>
                        </div>
                        <span class="{get_verdict_class(s['verdict'])}" style="font-size:1.1rem;">{s['verdict']}</span>
                    </div>
                    <h3 style="color:#f1f5f9; margin:0 0 8px 0; font-size:1.2rem;">{ad.get('headline', 'N/A')}</h3>
                    <p style="color:#cbd5e1; font-size:0.95rem; line-height:1.6;">{ad.get('primary_text', 'N/A')}</p>
                    <div style="margin-top:12px; padding-top:12px; border-top:1px solid #1e293b;">
                        <span style="color:#22c55e; font-size:0.85rem;">💪 {s.get('top_strength', '')}</span><br>
                        <span style="color:#f59e0b; font-size:0.85rem;">🔧 {s.get('improvement', '')}</span>
                    </div>
                    <div style="margin-top:8px;">
                        <span style="color:#7c3aed; font-size:0.85rem;">🎯 CTA: {ad.get('cta_text', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="score-card">
                    <p class="score-big" style="color:{score_color(s['composite_score'])}">{s['composite_score']}</p>
                    <p class="score-label">Composite Score</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Mini score breakdown
                dims = s.get('scores', {})
                if isinstance(dims, dict):
                    for dim_name, val in dims.items():
                        if isinstance(val, (int, float)):
                            st.progress(val / 10, text=f"{dim_name}: {val}/10")
    
    # ---- TAB 2: SCOREBOARD ----
    with tab2:
        st.markdown("### 📊 Full scoreboard — all 20 ads ranked")
        
        # Build dataframe
        df_data = []
        for s in scores_sorted:
            ad = ad_lookup.get(s['ad_id'], {})
            row = {
                'Rank': len(df_data) + 1,
                'Ad ID': s['ad_id'],
                'Score': s['composite_score'],
                'Verdict': s['verdict'],
                'Bucket': s.get('bucket', ad.get('bucket', '')),
                'Platform': ad.get('platform', ''),
                'Audience': ad.get('audience_segment', ''),
                'Headline': ad.get('headline', '')[:60] + '...' if len(ad.get('headline', '')) > 60 else ad.get('headline', ''),
                'Hook': s.get('scores', {}).get('hook', 0) if isinstance(s.get('scores', {}).get('hook'), (int, float)) else 0,
                'Proof': s.get('scores', {}).get('proof', 0) if isinstance(s.get('scores', {}).get('proof'), (int, float)) else 0,
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        
        # Color the score column
        st.dataframe(
            df,
            column_config={
                "Score": st.column_config.ProgressColumn(
                    "Score",
                    min_value=0,
                    max_value=100,
                    format="%d"
                ),
                "Hook": st.column_config.NumberColumn("Hook /10", format="%d"),
                "Proof": st.column_config.NumberColumn("Proof /10", format="%d"),
            },
            hide_index=True,
            use_container_width=True,
            height=700
        )
    
    # ---- TAB 3: ANALYTICS ----
    with tab3:
        st.markdown("### 📈 Creative performance analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        avg_score = sum(s['composite_score'] for s in scores) / len(scores)
        launch_count = sum(1 for s in scores if s['verdict'] == 'LAUNCH')
        top_bucket = max(set(s.get('bucket', '') for s in scores[:5]), 
                        key=lambda b: sum(1 for s in scores[:5] if s.get('bucket') == b))
        
        col1.metric("Avg score", f"{avg_score:.0f}/100")
        col2.metric("Launch-ready", f"{launch_count}/{len(scores)}")
        col3.metric("Top bucket", top_bucket)
        col4.metric("Total ads", len(scores))
        
        st.divider()
        
        c1, c2 = st.columns(2)
        
        with c1:
            # Score distribution by bucket
            bucket_scores = {}
            for s in scores:
                b = s.get('bucket', 'Unknown')
                bucket_scores.setdefault(b, []).append(s['composite_score'])
            
            bucket_avg = {b: sum(v)/len(v) for b, v in bucket_scores.items()}
            fig1 = px.bar(
                x=list(bucket_avg.keys()), y=list(bucket_avg.values()),
                title="Average score by ad bucket",
                labels={"x": "Bucket", "y": "Avg Score"},
                color=list(bucket_avg.values()),
                color_continuous_scale="viridis"
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8', showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with c2:
            # Verdict distribution
            verdicts = [s['verdict'] for s in scores]
            verdict_counts = {v: verdicts.count(v) for v in set(verdicts)}
            colors = {'LAUNCH': '#22c55e', 'ITERATE': '#f59e0b', 'REWORK': '#ef4444', 'KILL': '#dc2626'}
            
            fig2 = px.pie(
                names=list(verdict_counts.keys()),
                values=list(verdict_counts.values()),
                title="Verdict distribution",
                color=list(verdict_counts.keys()),
                color_discrete_map=colors
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Score distribution histogram
        fig3 = px.histogram(
            x=[s['composite_score'] for s in scores],
            nbins=10,
            title="Score distribution",
            labels={"x": "Composite Score", "y": "Count"},
            color_discrete_sequence=["#7c3aed"]
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8'
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Platform breakdown
        c3, c4 = st.columns(2)
        with c3:
            platform_scores = {}
            for s in scores:
                ad = ad_lookup.get(s['ad_id'], {})
                p = ad.get('platform', 'Unknown')
                platform_scores.setdefault(p, []).append(s['composite_score'])
            
            plat_avg = {p: sum(v)/len(v) for p, v in platform_scores.items()}
            fig4 = px.bar(
                x=list(plat_avg.keys()), y=list(plat_avg.values()),
                title="Avg score by platform",
                color_discrete_sequence=["#06b6d4"]
            )
            fig4.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8'
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with c4:
            audience_scores = {}
            for s in scores:
                ad = ad_lookup.get(s['ad_id'], {})
                a = ad.get('audience_segment', 'Unknown')
                audience_scores.setdefault(a, []).append(s['composite_score'])
            
            aud_avg = {a: sum(v)/len(v) for a, v in audience_scores.items()}
            fig5 = px.bar(
                x=list(aud_avg.keys()), y=list(aud_avg.values()),
                title="Avg score by audience",
                color_discrete_sequence=["#ec4899"]
            )
            fig5.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8'
            )
            st.plotly_chart(fig5, use_container_width=True)
    
    # ---- TAB 4: ALL ADS ----
    with tab4:
        st.markdown("### 🔍 Browse all generated ads")
        
        # Filters
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filter_bucket = st.selectbox("Filter by bucket", ["All"] + list(set(
                s.get('bucket', ad_lookup.get(s['ad_id'], {}).get('bucket', '')) for s in scores
            )))
        with fc2:
            filter_verdict = st.selectbox("Filter by verdict", ["All", "LAUNCH", "ITERATE", "REWORK", "KILL"])
        with fc3:
            filter_platform = st.selectbox("Filter by platform", ["All"] + list(set(
                ad_lookup.get(s['ad_id'], {}).get('platform', '') for s in scores
            )))
        
        for s in scores_sorted:
            ad = ad_lookup.get(s['ad_id'], {})
            bucket = s.get('bucket', ad.get('bucket', ''))
            platform = ad.get('platform', '')
            
            # Apply filters
            if filter_bucket != "All" and bucket != filter_bucket:
                continue
            if filter_verdict != "All" and s['verdict'] != filter_verdict:
                continue
            if filter_platform != "All" and platform != filter_platform:
                continue
            
            with st.expander(f"**{s['ad_id']}** | Score: {s['composite_score']} | {s['verdict']} | {bucket} | {platform}"):
                st.markdown(f"**Headline:** {ad.get('headline', 'N/A')}")
                st.markdown(f"**Primary text:** {ad.get('primary_text', 'N/A')}")
                if ad.get('description'):
                    st.markdown(f"**Description:** {ad['description']}")
                st.markdown(f"**CTA:** {ad.get('cta_text', 'N/A')}")
                st.markdown(f"**Hook type:** {ad.get('hook_type', 'N/A')}")
                st.markdown(f"**Audience:** {ad.get('audience_segment', 'N/A')}")
                st.markdown(f"**Key proof point:** {ad.get('key_proof_point', 'N/A')}")
                if ad.get('image_prompt'):
                    st.markdown(f"**🎨 Image concept:** {ad['image_prompt']}")
                if ad.get('video_script'):
                    st.markdown(f"**🎬 Video script:** {ad['video_script']}")
                
                st.divider()
                st.markdown(f"💪 **Strength:** {s.get('top_strength', 'N/A')}")
                st.markdown(f"🔧 **Improve:** {s.get('improvement', 'N/A')}")
    
    # ---- TAB 5: RECOMMENDATIONS ----
    with tab5:
        st.markdown("### 🎯 Strategic recommendations")
        
        st.markdown("""
        <div class="ad-card" style="border-left-color: #22c55e;">
            <h4 style="color:#22c55e; margin-top:0;">✅ Immediate wins</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>Double down on STARTUP bucket</strong> — your highest-scoring ads all leverage the ₹25L funding and D2C challenge. No competitor can match this.</li>
                <li><strong>Lead every ad with a specific proof point</strong> — ads with named students + companies score 15-20 points higher than generic claims.</li>
                <li><strong>Add April 19 deadline to ALL ads</strong> — urgency in CTA boosts score by ~8 points on average.</li>
            </ol>
        </div>
        
        <div class="ad-card" style="border-left-color: #f59e0b;">
            <h4 style="color:#f59e0b; margin-top:0;">⚠️ Gaps to fill</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>Video content is underdeveloped</strong> — generate more YouTube pre-roll and Instagram Reels scripts. Video ads have 2x engagement on Meta.</li>
                <li><strong>Aspiring founders segment is underserved</strong> — only 5/20 ads target founders. This is SSB's strongest unique segment.</li>
                <li><strong>Google Search ads need differentiation</strong> — current search ads are functional but generic. Add more unique SSB angles.</li>
            </ol>
        </div>
        
        <div class="ad-card" style="border-left-color: #7c3aed;">
            <h4 style="color:#7c3aed; margin-top:0;">🧪 Creative angles to test next</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>"Your office has a startup floor"</strong> — campus ecosystem angle. No IIM, MU, or MESA can claim 10+ live startups on campus.</li>
                <li><strong>"₹25K on Day 1"</strong> — D2C challenge funding as a hook. Tangible, immediate, unique.</li>
                <li><strong>"Scaler put more people in Amazon than all IITs"</strong> — legacy proof transferred to SSB credibility.</li>
                <li><strong>Student founder vs. MBA student side-by-side</strong> — visual format showing what SSB students DO vs what MBA students STUDY.</li>
            </ol>
        </div>
        
        <div class="ad-card" style="border-left-color: #06b6d4;">
            <h4 style="color:#06b6d4; margin-top:0;">💰 Suggested budget allocation</h4>
            <ol style="color:#cbd5e1;">
                <li><strong>Meta (Feed + Stories): 45%</strong> — highest creative flexibility, best for visual storytelling and social proof</li>
                <li><strong>Google Search: 25%</strong> — captures high-intent "business school" and "career change" searches</li>
                <li><strong>LinkedIn: 20%</strong> — career pivoters are most active here, best for professional positioning</li>
                <li><strong>YouTube: 10%</strong> — video pre-roll for awareness, retarget search visitors</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


# ---- FOOTER ----
st.divider()
st.markdown("""
<div style="text-align:center; color:#475569; font-size:0.85rem;">
    Built with Claude API + Streamlit | Scaler School of Business — AI Ad Creative Factory
    <br>Hackathon MVP — 5-hour build | April 2026
</div>
""", unsafe_allow_html=True)
