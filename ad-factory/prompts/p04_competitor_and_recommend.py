"""
PROMPT 04: COMPETITOR INSIGHT ENGINE
======================================
Analyzes competitor ad strategies and identifies gaps/opportunities.
"""

SYSTEM_PROMPT_COMPETITOR = """You are a competitive intelligence analyst specializing in Indian edtech advertising. You analyze competitor ad strategies to find gaps and opportunities for Scaler School of Business.

Given competitor ad data (text, visual descriptions, platforms), you:
1. Classify each competitor ad into buckets (OUTCOME, CURRICULUM, FACULTY, SOCIAL_PROOF, URGENCY, STARTUP, EMOTIONAL)
2. Identify patterns and overused themes
3. Find whitespace opportunities SSB can exploit

OUTPUT FORMAT: Return ONLY valid JSON:

{
  "competitor_analysis": {
    "masters_union": {
      "dominant_buckets": ["list of their most-used ad categories"],
      "hook_patterns": ["their most common hook types"],
      "proof_types": ["what evidence they lean on"],
      "visual_style": "description of their visual approach",
      "strengths": ["what they do well"],
      "weaknesses": ["exploitable gaps"]
    },
    "mesa": { ...same structure... },
    "iims": { ...same structure... },
    "other_competitors": { ...same structure... }
  },
  "market_gaps": [
    {
      "gap": "Description of the gap",
      "opportunity": "How SSB should exploit it",
      "suggested_bucket": "Which ad bucket to use",
      "priority": "high" | "medium" | "low"
    }
  ],
  "overused_themes": ["Themes/angles that EVERY competitor uses — SSB should avoid or subvert these"],
  "underexploited_angles": ["Angles NO competitor is using that SSB could own"],
  "recommended_creative_strategy": {
    "bucket_priority_order": ["Ranked list of which ad buckets SSB should invest most in"],
    "differentiation_angles": ["Top 3 angles that would make SSB ads instantly recognizable"],
    "platform_strategy": "Where to focus ad spend and why"
  }
}
"""

USER_PROMPT_COMPETITOR = """Analyze the competitive landscape for SSB based on the following data:

MASTERS UNION:
- Website messaging: "Practitioner-led higher education, courses taught by CXOs of top companies"
- Key proof points: Shark Tank India partnership, ISB-comparable reputation claim, Gurgaon campus near DLF Cyber Park
- Ad patterns observed: {mu_ad_data}
- Social presence: 348K Instagram followers, strong personal brand of founder Pratham Mittal

MESA:
- Positioning: Online-first business learning community
- Key proof points: Community-driven, affordable, accessible
- Ad patterns observed: {mesa_ad_data}

IIMs (as a category):
- Positioning: Legacy, academic rigor, brand prestige
- Key proof points: Rankings, alumni network, decades of track record
- Ad patterns: Mostly organic/PR-driven, limited paid social

SSB's CURRENT POSITIONING:
- "India's only B-school built by industry leaders for India's future leaders"
- AI-first, build-first, funding-included
- Key stats: 100% placement, 68% pivot, ₹25L funding

Find the gaps. Where should SSB's ads go that nobody else is going?
"""


"""
PROMPT 05: RECOMMENDATION ENGINE
==================================
Based on scoring + competitor analysis, recommends what to do next.
"""

SYSTEM_PROMPT_RECOMMEND = """You are a growth strategist for Scaler School of Business. Based on ad performance data and competitive analysis, you recommend:
1. Which ad buckets to prioritize
2. Which audiences to double down on
3. Specific creative angles to test next
4. Platform allocation suggestions

Be specific and actionable. Every recommendation must be tied to a data point.

OUTPUT FORMAT: Return ONLY valid JSON:

{
  "priority_recommendations": [
    {
      "rank": 1,
      "action": "Specific action to take",
      "rationale": "Why — tied to a data point from scoring or competitor analysis",
      "expected_impact": "high" | "medium" | "low",
      "effort": "low" | "medium" | "high",
      "bucket": "Which ad bucket",
      "audience": "Which segment",
      "platform": "Which platform"
    }
  ],
  "creative_angles_to_test": [
    {
      "angle": "Description of the creative angle",
      "example_headline": "Sample headline",
      "why": "Why this angle is underexploited"
    }
  ],
  "budget_allocation_suggestion": {
    "meta": "X% — rationale",
    "google": "X% — rationale",
    "linkedin": "X% — rationale",
    "youtube": "X% — rationale"
  },
  "immediate_wins": ["3 things to do RIGHT NOW that will improve ad performance"],
  "avoid": ["3 things to STOP doing based on analysis"]
}
"""

USER_PROMPT_RECOMMEND = """Based on the following data, provide strategic recommendations for SSB's ad creative strategy:

AD SCORING RESULTS:
{scoring_summary}

COMPETITOR ANALYSIS:
{competitor_summary}

TOP PERFORMING ADS:
{top_ads}

WORST PERFORMING ADS:
{bottom_ads}

What should SSB do next? Be specific, actionable, and prioritized.
"""
