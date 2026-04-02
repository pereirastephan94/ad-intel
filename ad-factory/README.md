# 🏭 AI Ad Creative Factory — Scaler School of Business

> Take one campaign brief → Generate 20 ad variants → Score & rank them with AI → Ship the top 5.

Built for Scaler's 5-hour hackathon. Theme: AI Ad Creative Factory.

---

## ⚡ Quick Start (2 minutes)

```bash
# 1. Clone and enter
git clone <your-repo-url>
cd ad-factory

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

**Demo mode works without any API key.** The app ships with 20 pre-generated, pre-scored sample ads for SSB.

To use **live mode**, get a Claude API key from [console.anthropic.com](https://console.anthropic.com) and enter it in the sidebar.

---

## 🏗 System Architecture

```
┌──────────────────────────────────────────────────┐
│                 CAMPAIGN BRIEF                    │
│   (Goal, Audience, Platform, Tone, Buckets)       │
└────────────────────┬─────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  BRAND DNA      │   │  AD BUCKETING   │
│  Analyzer       │   │  Classifier     │
│  (tone, vocab,  │   │  (7 categories) │
│   constraints)  │   │                 │
└────────┬────────┘   └────────┬────────┘
         └──────────┬──────────┘
                    ▼
┌──────────────────────────────────────────────────┐
│            GENERATION ENGINE (Claude API)          │
│  ┌──────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Copy │ │ Img      │ │ Video    │ │ CTA     │ │
│  │ Gen  │ │ Prompts  │ │ Scripts  │ │ Bank    │ │
│  └──────┘ └──────────┘ └──────────┘ └─────────┘ │
│              → 20 ad variants                     │
└────────────────────┬─────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  Image Gen      │   │  AI JUDGE       │
│  (Ideogram /    │   │  (7-dimension   │
│   DALL-E /      │   │   scoring, 0-100│
│   Canva)        │   │   composite)    │
└─────────────────┘   └────────┬────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌─────────────────┐   ┌─────────────────┐
          │  Competitor     │   │  Recommendation │
          │  Insight Engine │   │  Engine         │
          └────────┬────────┘   └────────┬────────┘
                   └──────────┬──────────┘
                              ▼
              ┌───────────────────────────┐
              │    STREAMLIT DASHBOARD    │
              │  Top 5 + Scores + Charts  │
              │  + Recommendations        │
              └───────────────────────────┘
```

---

## 📁 Folder Structure

```
ad-factory/
├── app.py                          # Main Streamlit app (the MVP)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── prompts/                        # All LLM prompts (copy-paste ready)
│   ├── 01_generate_ads.py         # Ad generation master prompt
│   ├── 02_brand_dna.py            # Brand DNA extraction + constraints
│   ├── 03_judge_ads.py            # AI creative scoring rubric
│   └── 04_competitor_and_recommend.py  # Competitor analysis + recommendations
│
├── data/                           # Sample data for demo mode
│   └── sample_data.py             # 20 pre-generated ads + scores
│
├── utils/                          # Helper functions (if needed)
│   └── (optional api wrappers)
│
├── outputs/                        # Generated outputs (gitignored)
│   └── (generated ads, scores, images)
│
└── assets/                         # Static assets
    └── (logos, screenshots)
```

---

## ⏱ Hour-by-Hour Build Plan

### Hour 1 (10:00–11:00): Foundation
| Who | What |
|-----|------|
| **Builder** | Set up repo, install deps, get Streamlit hello-world running |
| **Prompt Engineer** | Test generation prompt in Claude.ai manually, iterate on quality |
| **Scorer** | Test judge prompt in Claude.ai, calibrate scoring (is 80 hard enough to hit?) |
| **Creative Director** | Study SSB website, extract brand DNA, compile proof points |
| **Demo Lead** | Set up Google Sheet as backup output, outline demo narrative |

**Checkpoint:** Generation prompt produces 5+ good ads. Judge prompt returns meaningful scores.

### Hour 2 (11:00–12:00): Generation Engine
| Who | What |
|-----|------|
| **Builder** | Wire Claude API into Streamlit sidebar → generation call → display results |
| **Prompt Engineer** | Generate full batch of 20 ads. QA each one. Iterate prompt if >3 are weak |
| **Scorer** | Score all 20 ads with judge prompt. Build leaderboard in Google Sheets |
| **Creative Director** | Run top 5 image prompts through Ideogram/Canva. Get visual mockups |
| **Demo Lead** | Start capturing screenshots for the presentation |

**Checkpoint:** 20 ads generated and scored. Top 5 identified with scores.

### Hour 3 (12:00–1:00): Scoring + Analytics
| Who | What |
|-----|------|
| **Builder** | Add scoring display, analytics charts (Plotly), tab navigation |
| **Prompt Engineer** | Run competitor analysis prompt. Feed insights into recommendation engine |
| **Scorer** | QA scores — do the rankings feel right? Recalibrate rubric if needed |
| **Creative Director** | Create 2-3 visual mockups of top ads as they'd appear on Meta/Google |
| **Demo Lead** | Build demo flow: Brief → Generate → Score → Top 5 → Recommendations |

**Checkpoint:** App shows all 5 tabs. Scores feel right. Visual mockups exist.

### Hour 4 (1:00–2:00): Polish + Integration
| Who | What |
|-----|------|
| **Builder** | Polish UI (dark theme, cards, progress bars). Fix bugs. Add filters. |
| **Prompt Engineer** | Generate a "live" batch during demo prep — test end-to-end |
| **Scorer** | Fill in recommendations tab with real insights from scoring data |
| **Creative Director** | Final visual mockups. Create a "before vs after" comparison (current SSB ads vs AI-generated) |
| **Demo Lead** | Rehearse demo. Time it to 5 minutes. Identify the "wow" moments. |

**Checkpoint:** App is demo-ready. All tabs work. Visual mockups ready.

### Hour 5 (2:00–3:00): Demo Prep + Buffer
| Who | What |
|-----|------|
| **Everyone** | Rehearse demo 2-3 times. Fix last-minute bugs. |
| **Demo Lead** | Final narrative: Problem → Solution → Demo → Impact → Future |
| **Builder** | Deploy to Streamlit Cloud (or have localhost ready with backup) |

---

## 🎯 Scoring Rubric (7 dimensions)

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Hook Strength | 20% | Does the first line stop a scroll? |
| Proof Density | 20% | How many verifiable facts? |
| Audience-Message Fit | 15% | Is it laser-targeted to ONE segment? |
| CTA Clarity + Urgency | 10% | Clear next step + time pressure? |
| Visual Concept | 15% | Does the image/video ADD information? |
| Brand Differentiation | 10% | Could this work for Masters Union with a logo swap? |
| Platform-Format Fit | 10% | Is it designed for where it'll run? |

**Composite Score = weighted average × 10, scaled to 0-100**

| Score | Verdict | Action |
|-------|---------|--------|
| 80-100 | LAUNCH | Ready to run. Minor polish only. |
| 60-79 | ITERATE | Strong foundation, needs specific fixes. |
| 40-59 | REWORK | Core concept may work, execution needs overhaul. |
| 0-39 | KILL | Scrap and start over. |

---

## 🧩 Ad Bucket Taxonomy

| Bucket | What it covers | When to use |
|--------|---------------|-------------|
| OUTCOME | Placements, salary, career pivots, company logos | TOFU awareness, high-intent search |
| CURRICULUM | AI tools, pedagogy, projects, what you'll learn | Mid-funnel consideration |
| FACULTY | Who teaches, credibility, practitioner-led | Trust-building, LinkedIn |
| SOCIAL_PROOF | Student stories, testimonials, before/after | Retargeting, social feeds |
| URGENCY | Deadlines, limited seats, application closing | BOFU conversion push |
| STARTUP | D2C challenge, hustle program, funding | Founders, differentiation |
| EMOTIONAL | Aspiration, FOMO, transformation narrative | Awareness, video |

---

## 💡 Tips to Impress Judges

1. **Lead with the output, not the tech.** Show the top 5 ads FIRST. Let judges react to the quality. Then explain how you got there.

2. **"Could this actually run?"** Have 2-3 visual mockups showing how the top ad would look on an actual Instagram feed or Google search results page.

3. **Show the scoring in action.** Pick one mediocre ad and one great ad. Show the score breakdown side-by-side. Explain WHY one is better.

4. **The competitor angle.** Show what Masters Union and MESA are currently doing (screenshots). Then show your AI-generated alternatives. The contrast is the wow moment.

5. **The "10x" claim.** "This system generates and scores 20 ads in 45 seconds. A creative team takes 2 weeks and produces 5. That's 40x more creative volume at 1/100th the cost."

6. **Future vision (30 seconds).** "Imagine this plugged into Meta's API — auto-uploading the top 5, running A/B tests, feeding performance data back into the scoring model. That's the full loop."

7. **The one thing to remember:** Judges care about IMPACT, not INFRASTRUCTURE. Don't spend 3 minutes explaining your API calls. Spend 3 minutes showing that your ads are genuinely better than what's currently running.

---

## 🔧 Tool Stack

| Component | Tool | Cost |
|-----------|------|------|
| LLM (generation + scoring) | Claude API (Sonnet) | ~$2-5 per full run |
| Frontend | Streamlit | Free |
| Image generation | Ideogram 3.0 / Canva AI | Free tier |
| Video scripts | Generated by Claude (text-only MVP) | Free |
| Charts | Plotly | Free |
| Backup output | Google Sheets | Free |
| Deployment | Streamlit Cloud | Free |

**Total cost: $0-5**

---

## 🚀 Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Set `app.py` as the main file
5. Add `ANTHROPIC_API_KEY` as a secret (optional — demo mode works without it)
6. Deploy!

---

*Built for Scaler School of Business hackathon — April 2026*
