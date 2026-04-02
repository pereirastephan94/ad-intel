# MASTER PROMPT — SSB AI Ad Creative Factory
## For Claude Max (or any Claude session connected to this repo)
### Paste this entire file into Claude Max. It self-executes in 6 ordered steps.

---

> **What this prompt does:** Builds a complete AI-powered ad creative production system for Scaler School of Business. It generates 20 ad variants from a campaign brief, scores each on 7 dimensions, surfaces the Top 5 with reasons, and outputs everything through a Streamlit dashboard. All brand intelligence is pre-baked into the prompts — you just need to run the steps.

---

## STEP 0 — READ BEFORE STARTING

You are building the SSB AI Ad Creative Factory. The repository you are connected to contains everything:

```
ad-intel/ad-factory/
├── app.py                      ← Main Streamlit app (5-tab dashboard)
├── requirements.txt            ← Python deps (streamlit, anthropic, pandas, plotly)
├── README.md                   ← Full documentation
│
├── prompts/
│   ├── p01_generate_ads.py    ← Generation engine: brief → 20 ad variants (JSON)
│   ├── p02_brand_dna.py       ← Brand DNA: SSB voice, banned words, proof hierarchy
│   ├── p03_judge_ads.py       ← Judge: 7-dimension scoring rubric, 0-100 score
│   └── p04_competitor_and_recommend.py ← Competitor gaps + strategy recommendations
│
├── data/
│   └── sample_data.py         ← 20 pre-generated + pre-scored demo ads (works without API key)
│
└── intelligence/
    ├── SSB_Creative_Universe.md    ← MASTER BRAND BIBLE: 7 ICPs, 13 buckets, 10 hooks, USP library
    ├── SSB_Ad_Scripts_V1.md        ← 9 production-ready SSB video scripts
    └── SSB_McKinsey_Audit.md       ← Full McKinsey audit of SSB's current ad portfolio
```

**Read `intelligence/SSB_Creative_Universe.md` first.** It is the ground truth for every creative decision.

---

## STEP 1 — VERIFY REPO STATE

Check all required files exist. Report what's present vs missing. Fix any gaps before proceeding.

Required files:
- [ ] `ad-factory/app.py`
- [ ] `ad-factory/requirements.txt`
- [ ] `ad-factory/prompts/__init__.py`
- [ ] `ad-factory/prompts/p01_generate_ads.py`
- [ ] `ad-factory/prompts/p02_brand_dna.py`
- [ ] `ad-factory/prompts/p03_judge_ads.py`
- [ ] `ad-factory/prompts/p04_competitor_and_recommend.py`
- [ ] `ad-factory/data/__init__.py`
- [ ] `ad-factory/data/sample_data.py`
- [ ] `ad-factory/intelligence/SSB_Creative_Universe.md`

When complete, confirm: "Step 1 complete — all files present. Proceeding to Step 2."

---

## STEP 2 — VERIFY THE GENERATION PROMPT

Read `prompts/p01_generate_ads.py`. Confirm it:
- Has `SYSTEM_PROMPT_GENERATE` with all SSB brand facts (Deepinder Goyal, Kunal Shah, Binny Bansal, ₹50K capital, 150hrs AI, 100% placement, 68% pivot, D2C Challenge)
- Has `USER_PROMPT_GENERATE` with all required format fields
- Outputs valid JSON with the correct 11 fields: `ad_id`, `bucket`, `platform`, `audience_segment`, `hook_type`, `headline`, `primary_text`, `description`, `cta_text`, `image_prompt`, `video_script`, `key_proof_point`

If anything is missing or incorrect, fix it.

When complete, confirm: "Step 2 complete — generation prompt verified."

---

## STEP 3 — VERIFY THE JUDGE PROMPT

Read `prompts/p03_judge_ads.py`. Confirm it:
- Has `SYSTEM_PROMPT_JUDGE` with all 7 scoring dimensions and their exact weights:
  - Hook Strength: 20%
  - Proof Density: 20%
  - Audience-Message Fit: 15%
  - CTA Clarity + Urgency: 10%
  - Visual Concept Strength: 15%
  - Brand Differentiation: 10%
  - Platform-Format Fit: 10%
- Uses the formula: `CPS = ((Hook × 2) + (Proof × 2) + (Fit × 1.5) + (CTA × 1) + (Visual × 1.5) + (Diff × 1) + (Platform × 1)) / 10 × 10`
- Has verdict thresholds: LAUNCH (80-100), ITERATE (60-79), REWORK (40-59), KILL (0-39)
- Has `USER_PROMPT_JUDGE_BATCH` for scoring multiple ads at once
- Outputs the correct JSON structure per ad including `composite_score`, `verdict`, `top_strength`, `improvement_suggestion`

If anything is missing or incorrect, fix it.

When complete, confirm: "Step 3 complete — judge prompt verified."

---

## STEP 4 — VERIFY THE SAMPLE DATA

Read `data/sample_data.py`. Confirm it has:
- `SAMPLE_ADS` — array of exactly 20 ad objects, each with all required fields
- `SAMPLE_SCORES` — array of 20 scoring objects matching the ad IDs
- At least 5 ads with `verdict: "LAUNCH"` (score 80+)
- Coverage of all 7 buckets: STARTUP, OUTCOME, CURRICULUM, FACULTY, SOCIAL_PROOF, URGENCY, EMOTIONAL
- Coverage of all 3 audiences: career_pivoter, ambitious_fresher, aspiring_founder
- Coverage of all platforms: meta_feed, meta_stories, google_search, google_display, linkedin, youtube_pre_roll

If any ads are missing proof points (real names, numbers, SSB facts), fix them.

When complete, confirm: "Step 4 complete — sample data verified. X LAUNCH-ready ads out of 20."

---

## STEP 5 — VERIFY THE STREAMLIT APP

Read `app.py`. Confirm it:
- Has correct imports: `from prompts.p01_generate_ads import SYSTEM_PROMPT_GENERATE, USER_PROMPT_GENERATE`
- Has correct imports: `from prompts.p03_judge_ads import SYSTEM_PROMPT_JUDGE, USER_PROMPT_JUDGE_BATCH`
- Has correct data import: `from data.sample_data import SAMPLE_ADS, SAMPLE_SCORES`
- Has all 5 tabs: Top 5 Ads, Scoreboard, Analytics, All Ads, Recommendations
- Demo mode works WITHOUT an API key (uses `SAMPLE_ADS` and `SAMPLE_SCORES`)
- Live mode accepts Anthropic API key in sidebar, calls `generate_ads_with_api()` then `score_ads_with_api()`
- Tab 1 (Top 5) shows: rank, headline, copy, CTA, bucket tag, platform tag, verdict, composite score, per-dimension scores as progress bars, top_strength, improvement_suggestion
- Tab 2 (Scoreboard) shows: sortable dataframe with all 20 ads
- Tab 3 (Analytics) shows: 4 Plotly charts (bucket performance, verdict distribution, score histogram, platform breakdown)
- Tab 5 (Recommendations) has hard-coded strategic insights based on SSB's unique angles

Fix any bugs found. The app must be runnable with `streamlit run app.py` from the `ad-factory/` directory.

When complete, confirm: "Step 5 complete — app verified and runnable."

---

## STEP 6 — RUN A LIVE TEST

Simulate what happens when a user clicks "Generate & Score Ads" in Demo mode:

1. Load `SAMPLE_ADS` (20 ads)
2. Load `SAMPLE_SCORES` (20 scores)
3. Sort scores by `composite_score` descending
4. Identify the Top 5
5. Report them here in this format:

```
TOP 5 ADS — Demo Mode Test
===========================
#1 [AD-ID] | Score: XX | Verdict: LAUNCH | Bucket: BUCKET | Platform: platform
   Headline: "..."
   Strength: "..."
   Improve: "..."

[repeat for #2 through #5]

SUMMARY:
- Strongest bucket: X (avg score Y)
- Weakest bucket: X (avg score Y)
- LAUNCH-ready: X/20
- Recommended next: [what types of ads to generate]
```

When complete, confirm: "Step 6 complete. The factory is live. Here are your top 5 ads."

---

## RUNNING THE APP LOCALLY

After all steps complete:

```bash
cd ad-factory
pip install -r requirements.txt
streamlit run app.py
```

App opens at http://localhost:8501

**Demo mode:** Click "Generate & Score Ads" immediately — no API key needed. Uses pre-generated sample data.

**Live mode:** Enter Anthropic API key in sidebar, select audiences and platforms, click Generate. Costs ~$0.50-2 per run with claude-sonnet-4.

---

## KEY BRAND FACTS TO VERIFY ARE IN EVERY AD

Every generated ad MUST reference at least ONE of these. If it doesn't, the judge will score it below 50.

**Tier 1 (nuclear — use these first):**
- Deepinder Goyal (Zomato) + Kunal Shah (CRED) + Binny Bansal (Flipkart) as backers/faculty
- ₹50,000 startup capital from Day 1 (D2C Challenge)
- Up to ₹25L funding through Hustle Program
- ₹10Cr+ revenue generated by enrolled students

**Tier 2 (differentiating):**
- 150+ hours AI practice, 25+ tools, 3 AI products shipped
- 60 seats (not 600) — cohort scarcity
- 100% internship placement
- 68% career pivot success rate
- 18 months (not 2 years like an MBA)
- 150+ companies actively hiring from SSB

**Banned words (deduct score if found):**
immersive · holistic · world-class · transformative · journey · ecosystem · leverage · synergy · cutting-edge

---

## WHAT GOOD LOOKS LIKE

The best ads in the dataset (score 80+) all share 3 things:
1. A hook that a specific ICP would feel in their gut (not a general "are you ready to grow?")
2. A Tier 1 proof point with an exact number or named person
3. A CTA with the real deadline (April 19) or a scarcity signal

The worst ads (score below 50) all share: generic hooks, no proof points, and CTAs that don't create urgency.

The judge is calibrated to be harsh — most ads should score 40-70. Only genuinely differentiated, proof-heavy ads score 80+.

---

*This file is the complete briefing. Read it once, then execute Steps 1-6 in order.*
