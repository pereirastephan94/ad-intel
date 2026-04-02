"""
PROMPT 02: BRAND DNA ANALYZER
===============================
Extracts brand DNA from existing creatives and enforces consistency.
"""

SYSTEM_PROMPT_BRAND_DNA = """You are a brand strategist who reverse-engineers the DNA of brands from their creative outputs. You analyze text, ad copy, landing pages, and visual descriptions to extract the core brand identity.

OUTPUT FORMAT: Return ONLY valid JSON (no markdown, no preamble):

{
  "brand_name": "...",
  "brand_dna": {
    "tone": {
      "primary": "e.g. Bold & Direct",
      "secondary": "e.g. Aspirational but grounded",
      "avoid": ["e.g. Academic/formal", "Corporate jargon", "Preachy"]
    },
    "vocabulary": {
      "power_words": ["list of 10-15 words the brand uses repeatedly"],
      "banned_words": ["list of words that contradict the brand voice"],
      "signature_phrases": ["recurring phrases or tagline patterns"]
    },
    "positioning": {
      "core_promise": "One sentence: what do they promise?",
      "against": "What are they positioned AGAINST?",
      "unique_angle": "What makes them different from all competitors?",
      "proof_hierarchy": ["Ranked list of their strongest proof points"]
    },
    "visual_identity": {
      "color_palette": "Dominant colors observed",
      "imagery_style": "What kind of images/videos they use",
      "typography_feel": "Modern/traditional/bold/minimal",
      "layout_preference": "Clean/busy/card-based/editorial"
    },
    "audience_voice": {
      "speaks_like": "Who does the brand sound like? (e.g. 'a sharp startup founder on LinkedIn')",
      "speaks_to": "Who is the implied reader?",
      "relationship": "Peer-to-peer / Expert-to-novice / Friend-to-friend"
    }
  }
}
"""

USER_PROMPT_BRAND_DNA = """Analyze the following content from {brand_name} and extract their complete brand DNA:

WEBSITE COPY:
{website_copy}

AD COPY SAMPLES (if available):
{ad_samples}

SOCIAL MEDIA POSTS (if available):
{social_posts}

Extract the brand DNA following the exact JSON format specified. Be specific — use actual words and phrases from the content, not generic descriptions.
"""

# Pre-extracted SSB Brand DNA (to save time during hackathon)
SSB_BRAND_DNA = {
    "brand_name": "Scaler School of Business",
    "brand_dna": {
        "tone": {
            "primary": "Bold & Builder-oriented",
            "secondary": "Practical, proof-heavy, anti-traditional",
            "avoid": ["Academic formality", "Corporate buzzwords", "Preachy motivation", "Generic edtech language"]
        },
        "vocabulary": {
            "power_words": ["build", "ship", "launch", "real", "revenue", "funding", "AI", "practical", "hands-on", "hustle", "execution", "impact", "startup", "industry leaders", "10x"],
            "banned_words": ["holistic", "comprehensive", "world-class faculty", "state-of-the-art", "cutting-edge", "paradigm", "synergy", "ecosystem" (overused), "transform your career" (generic)],
            "signature_phrases": [
                "Build the Future. Don't Just Study It.",
                "India's only B-school built by industry leaders",
                "No fluff",
                "Real products, real customers, real money",
                "Enter without code. Exit with the capability to build real world products",
                "#CreateImpact"
            ]
        },
        "positioning": {
            "core_promise": "You will BUILD real businesses and AI products, not just study case studies",
            "against": "Traditional MBAs that are theory-heavy, slow to adopt AI, and teach through cases instead of doing",
            "unique_angle": "Only program where you get actual startup funding (₹25K-₹25L), build live businesses, and graduate AI-fluent — with a campus surrounded by incubated startups",
            "proof_hierarchy": [
                "₹25L startup funding through Hustle Program",
                "100% internship placement",
                "Backed by Deepinder Goyal, Kunal Shah, Binny Bansal",
                "D2C Challenge: ₹5L+ revenue in 6 weeks",
                "68% career pivot rate",
                "10+ startups incubated on campus",
                "150+ hours AI learning with 25+ tools",
                "Scaler placed more SDEs at Amazon than all IITs"
            ]
        },
        "visual_identity": {
            "color_palette": "Dark navy/black backgrounds, electric blue accents, white text, yellow/green highlights",
            "imagery_style": "Real student photos (not stock), campus shots, workshop moments, startup pitches",
            "typography_feel": "Modern, bold headers, clean sans-serif",
            "layout_preference": "Card-based, clean sections, heavy use of stats/numbers as visual anchors"
        },
        "audience_voice": {
            "speaks_like": "A sharp startup founder who just raised a round — direct, specific, proof-heavy",
            "speaks_to": "Ambitious 22-28 year olds who are doers, not just dreamers",
            "relationship": "Peer-to-peer (we built this, you'll build yours)"
        }
    }
}

# Brand constraint prompt to inject into generation
BRAND_CONSTRAINT_INJECTION = """
BRAND VOICE CONSTRAINTS (enforce these strictly):
- Tone: Bold, builder-oriented, anti-traditional. Sound like a startup founder's LinkedIn post, NOT a university brochure
- Power words to USE: build, ship, launch, real, revenue, funding, AI, practical, hands-on, hustle
- Words to AVOID: holistic, comprehensive, world-class, state-of-the-art, cutting-edge, paradigm, synergy, transform your career
- Always lead with proof (numbers, names, specifics) before claims
- Relationship with reader: peer-to-peer ("we built this, come build yours")
- Visual style: Dark backgrounds, bold type, real photos/stats as anchors — never stock imagery
"""
