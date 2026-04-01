import Anthropic from '@anthropic-ai/sdk'
import { NextRequest } from 'next/server'
import { scrapeAdLibraryWithPlaywright } from './scraper'

export const maxDuration = 300

// Prompt when we have pre-scraped FB Ad Library data from Playwright
function getPromptWithScrapedData(
  competitorUrl: string,
  rawAdLibraryText: string,
  adCount: number,
  yourUrl?: string
): string {
  const today = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })

  const yourBusinessSection = yourUrl ? `
STEP 2 — YOUR OWN BUSINESS ANALYSIS:
- Fetch ${yourUrl} to understand their positioning, programs, and key messaging
- Search for their own Facebook Ad Library page and browse their active ads
- Extract their ad scripts, hooks, and creative buckets

Then produce Section 6 (Gap Analysis) comparing the two.
` : ''

  const gapSection = yourUrl ? `
---

### SECTION 6 — GAP ANALYSIS: What [Competitor] does that [Your Business] doesn't

**Your business URL scraped:** ${yourUrl}

**Your current ad buckets:**
[List the buckets/hooks your business is currently using in their ads]

**What the competitor does that you do NOT:**
| Gap | Competitor Example | Why It Matters | Recommended Action |
|---|---|---|---|
| [gap] | "[verbatim copy]" | [impact] | [specific fix] |

**What YOU do that the competitor does NOT (your advantages to amplify):**
| Your Advantage | How to Use It |
|---|---|
| [advantage] | [how to feature it in ads] |

**Priority actions (ranked by impact):**
1. [highest impact gap to close first]
2. [second]
3. [third]
` : `
---

### SECTION 6 — STRATEGIC GAPS (What this competitor is NOT doing)
| Gap | Why It Matters | Opportunity |
|---|---|---|
| [gap] | [why] | [how to exploit it] |
`

  return `You are a senior McKinsey-level competitive intelligence analyst specialising in performance marketing and paid social strategy.

Today's date: ${today}

I have already scraped the Facebook Ad Library for: ${competitorUrl}
The raw page text (${adCount} ads detected) is provided below. Analyse it fully — do NOT skip any ads.
${yourUrl ? `\nFor comparison, also analyse the business at: ${yourUrl} (use web_fetch/web_search for this)` : ''}
${yourBusinessSection}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAW FACEBOOK AD LIBRARY DATA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${rawAdLibraryText}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRITICAL INSTRUCTIONS:
- Extract EVERY ad verbatim — all ${adCount} of them. Do not skip, truncate, or summarise ad copy.
- If you see multiple different products being advertised (e.g. different programs, courses, price points), treat each as a separate product line
- Library ID, start date, variant count, and full copy verbatim for every ad
- If a Library ID appears multiple times = it's a multi-variant ad — note the count

OUTPUT FORMAT — use exactly this structure:

## [Competitor Name] — Ad Intelligence Report
**Date:** ${today} | **Source:** ${competitorUrl}

---

### TLDR — What's in this report
This report covers [X] active ads across [N] distinct products from [Competitor].

**Products found:** [list each product/program with one-line description]

**What you'll see below:**
1. 📋 All [N] ad scripts verbatim, grouped by product
2. 🪣 [N] creative buckets — the strategic patterns behind every ad
3. 🗺️ Funnel map — TOFU/MOFU/BOFU breakdown
4. 🔍 Gap analysis — ${yourUrl ? "what they do that you don't (and vice versa)" : "what they're NOT doing"}

**Top 3 things to know right now:**
- [most important finding]
- [second most important]
- [third]

---

### SECTION 1 — PRODUCTS DETECTED
| Product | Description | # Ads | Target ICP | CTA |
|---|---|---|---|---|
| [product name] | [one line] | [N] | [who] | [button text → URL] |

---

### SECTION 2 — ALL AD SCRIPTS (verbatim, grouped by product)

#### PRODUCT: [Product Name 1]

**Ad [N] | Library ID: [ID] | Started: [date] | [X] variants**
Hook: [first line]
Body:
\`\`\`
[full copy verbatim — every word]
\`\`\`
CTA: [button] → [URL]
ICP signal: [who this targets based on language used]

[repeat for every ad in this product]

#### PRODUCT: [Product Name 2]
[repeat structure]

---

### SECTION 3 — CREATIVE BUCKETS

Group ALL ads across all products into 5–9 strategic themes:

**Bucket [N]: [Name]**
- What it does: [one sentence]
- Hook pattern: [how it opens]
- Body pattern: [what it says in the middle]
- CTA pattern: [how it closes]
- Products using it: [which product lines]
- # of ads: [N] ([X]% of total)
- Strongest example: "[verbatim hook]"
- Why it works: [psychology/mechanism]
- Funnel stage: TOFU / MOFU / BOFU

---

### SECTION 4 — FUNNEL MAP
| Stage | # Ads | Bucket | Hook Pattern | CTA | Landing Page |
|---|---|---|---|---|---|
| TOFU | | | | | |
| MOFU | | | | | |
| BOFU | | | | | |

---

### SECTION 5 — URL & CADENCE INTELLIGENCE
- **Landing pages:** [list all destination URLs]
- **UTM patterns:** [any visible UTM parameters]
- **Ad cadence:** [when new ads launch, how often, cluster patterns]
- **Highest-confidence creative:** [ad with most variants = their winner]
- **Newest ads:** [most recently launched — what they're testing now]

---
${gapSection}`
}

function getPrompt(competitorUrl: string, yourUrl?: string): string {
  const today = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })

  const yourBusinessSection = yourUrl ? `
STEP 5 — YOUR OWN BUSINESS ANALYSIS:
- Fetch ${yourUrl} to understand their positioning, programs, and key messaging
- Search for their own Facebook Ad Library page and browse their active ads
- Extract their ad scripts, hooks, and creative buckets

Then produce Section 6 (Gap Analysis) comparing the two.
` : ''

  const gapSection = yourUrl ? `
---

### SECTION 6 — GAP ANALYSIS: What [Competitor] does that [Your Business] doesn't

**Your business URL scraped:** ${yourUrl}

**Your current ad buckets:**
[List the buckets/hooks your business is currently using in their ads]

**What the competitor does that you do NOT:**
| Gap | Competitor Example | Why It Matters | Recommended Action |
|---|---|---|---|
| [gap] | "[verbatim copy]" | [impact] | [specific fix] |

**What YOU do that the competitor does NOT (your advantages to amplify):**
| Your Advantage | How to Use It |
|---|---|
| [advantage] | [how to feature it in ads] |

**Priority actions (ranked by impact):**
1. [highest impact gap to close first]
2. [second]
3. [third]
` : `
---

### SECTION 6 — STRATEGIC GAPS (What this competitor is NOT doing)
| Gap | Why It Matters | Opportunity |
|---|---|---|
| [gap] | [why] | [how to exploit it] |
`

  return `You are a senior McKinsey-level competitive intelligence analyst specialising in performance marketing and paid social strategy.

Today's date: ${today}

Your task: Conduct a comprehensive analysis of ALL active Facebook ads for: ${competitorUrl}
${yourUrl ? `\nFor comparison, also analyse the business at: ${yourUrl}` : ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — Find their Facebook Ad Library:
- Search for "${competitorUrl} facebook page" to find their FB page
- Find their Ad Library URL (format: facebook.com/ads/library/?view_all_page_id=XXXXX)
- Fetch the Ad Library page — sort by total impressions descending

STEP 2 — Extract ALL ads (do not stop early):
- Click/expand "See summary details" on grouped ads to see all variants
- For each ad capture: full copy verbatim, hook (first line), CTA, landing URL, start date, number of variants
- CRITICAL: If you see multiple different products being advertised (e.g. different programs, courses, price points), treat each as a separate product line and call it out

STEP 3 — Identify products:
- List every distinct product/program being advertised
- Note which ads belong to which product
- Never lump different products together

STEP 4 — Produce the report below
${yourBusinessSection}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OUTPUT FORMAT — use exactly this structure:

## [Competitor Name] — Ad Intelligence Report
**Date:** ${today} | **Source:** ${competitorUrl}

---

### TLDR — What's in this report
This report covers [X] active ads across [N] distinct products from [Competitor].

**Products found:** [list each product/program with one-line description]

**What you'll see below:**
1. 📋 All [N] ad scripts verbatim, grouped by product
2. 🪣 [N] creative buckets — the strategic patterns behind every ad
3. 🗺️ Funnel map — TOFU/MOFU/BOFU breakdown
4. 🔍 Gap analysis — ${yourUrl ? 'what they do that you don\'t (and vice versa)' : 'what they\'re NOT doing'}

**Top 3 things to know right now:**
- [most important finding]
- [second most important]
- [third]

---

### SECTION 1 — PRODUCTS DETECTED
| Product | Description | # Ads | Target ICP | CTA |
|---|---|---|---|---|
| [product name] | [one line] | [N] | [who] | [button text → URL] |

---

### SECTION 2 — ALL AD SCRIPTS (verbatim, grouped by product)

#### PRODUCT: [Product Name 1]

**Ad [N] | Library ID: [ID] | Started: [date] | [X] variants**
Hook: [first line]
Body:
\`\`\`
[full copy verbatim — every word]
\`\`\`
CTA: [button] → [URL]
ICP signal: [who this targets based on language used]

[repeat for every ad in this product]

#### PRODUCT: [Product Name 2]
[repeat structure]

---

### SECTION 3 — CREATIVE BUCKETS

Group ALL ads across all products into 5–9 strategic themes:

**Bucket [N]: [Name]**
- What it does: [one sentence]
- Hook pattern: [how it opens]
- Body pattern: [what it says in the middle]
- CTA pattern: [how it closes]
- Products using it: [which product lines]
- # of ads: [N] ([X]% of total)
- Strongest example: "[verbatim hook]"
- Why it works: [psychology/mechanism]
- Funnel stage: TOFU / MOFU / BOFU

---

### SECTION 4 — FUNNEL MAP
| Stage | # Ads | Bucket | Hook Pattern | CTA | Landing Page |
|---|---|---|---|---|---|
| TOFU | | | | | |
| MOFU | | | | | |
| BOFU | | | | | |

---

### SECTION 5 — URL & CADENCE INTELLIGENCE
- **Landing pages:** [list all destination URLs]
- **UTM patterns:** [any visible UTM parameters]
- **Ad cadence:** [when new ads launch, how often, cluster patterns]
- **Highest-confidence creative:** [ad with most variants = their winner]
- **Newest ads:** [most recently launched — what they're testing now]

---
${gapSection}`
}

async function sendToSlack(webhookUrl: string, competitorUrl: string, analysis: string): Promise<void> {
  const hostname = (() => { try { return new URL(competitorUrl).hostname.replace('www.', '') } catch { return competitorUrl } })()

  // Extract TLDR section for the Slack preview
  const tldrMatch = analysis.match(/### TLDR[^\n]*\n([\s\S]*?)(?=\n---|\n###)/i)
  const tldrText = tldrMatch ? tldrMatch[1].trim().slice(0, 1200) : analysis.slice(0, 1200)

  const totalAdsMatch = analysis.match(/Total[^\d]*(\d+)\s*ad/i)
  const productsMatch = analysis.match(/Products found[:\s]*([^\n]+)/i)
  const totalAds = totalAdsMatch?.[1] ?? '?'
  const products = productsMatch?.[1]?.trim() ?? '?'

  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `🔍 Ad Intel Report: ${hostname}`,
      blocks: [
        {
          type: 'header',
          text: { type: 'plain_text', text: `🔍 Ad Intel: ${hostname}` }
        },
        {
          type: 'section',
          fields: [
            { type: 'mrkdwn', text: `*Active Ads*\n${totalAds}` },
            { type: 'mrkdwn', text: `*Products Found*\n${products}` },
          ]
        },
        { type: 'divider' },
        {
          type: 'section',
          text: { type: 'mrkdwn', text: `*📋 TLDR*\n${tldrText}` }
        },
        { type: 'divider' },
        {
          type: 'section',
          text: { type: 'mrkdwn', text: '_Full report is streaming in your browser. Detailed breakdown follows in the next messages._' }
        },
        {
          type: 'context',
          elements: [{ type: 'mrkdwn', text: `Generated ${new Date().toLocaleString('en-IN')} · Ad Intel powered by Claude` }]
        }
      ]
    })
  })

  // Send full report in chunks
  const chunks = analysis.match(/[\s\S]{1,2800}/g) ?? []
  for (let i = 0; i < Math.min(chunks.length, 8); i++) {
    await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: chunks[i],
        blocks: [{
          type: 'section',
          text: { type: 'mrkdwn', text: '```' + chunks[i].slice(0, 2900) + '```' }
        }]
      })
    })
    // Small delay to avoid Slack rate limits
    await new Promise(r => setTimeout(r, 300))
  }
}

export async function POST(req: NextRequest) {
  const { urls, yourUrl, slackWebhook, apiKey } = await req.json()

  if (!apiKey?.trim()) return new Response('Missing Claude API key', { status: 400 })
  const validUrls: string[] = (urls ?? []).filter((u: string) => u?.trim())
  if (!validUrls.length) return new Response('No URLs provided', { status: 400 })

  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      const send = (data: object) =>
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`))

      let client: Anthropic
      try {
        client = new Anthropic({ apiKey })
      } catch {
        send({ type: 'error', url: '', message: 'Invalid API key format' })
        send({ type: 'done' })
        controller.close()
        return
      }

      for (const url of validUrls) {
        send({ type: 'status', url, message: 'Launching browser to scrape Facebook Ad Library...' })
        let fullText = ''

        try {
          // ── Try Playwright first (real browser, bypasses FB bot detection) ──
          let prompt: string
          const scrapeResult = await scrapeAdLibraryWithPlaywright(url)

          if (scrapeResult.success && scrapeResult.rawText && scrapeResult.adCount && scrapeResult.adCount > 0) {
            send({
              type: 'status', url,
              message: `✓ Scraped ${scrapeResult.adCount} ads from Facebook. Sending to Claude for analysis...`
            })
            prompt = getPromptWithScrapedData(url, scrapeResult.rawText, scrapeResult.adCount, yourUrl || undefined)
          } else {
            // Fall back to Claude's own web tools
            send({
              type: 'status', url,
              message: `Browser scrape failed (${scrapeResult.error ?? 'unknown'}). Falling back to Claude web search...`
            })
            prompt = getPrompt(url, yourUrl || undefined)
          }

          // Tools only needed for fallback (yourUrl analysis still benefits from them)
          const messageStream = client.messages.stream({
            model: 'claude-opus-4-6',
            max_tokens: 16000,
            thinking: { type: 'adaptive' },
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            tools: [
              { type: 'web_search_20260209', name: 'web_search' },
              { type: 'web_fetch_20260209', name: 'web_fetch' },
            ] as any,
            messages: [{ role: 'user', content: prompt }],
          })

          for await (const event of messageStream) {
            if (
              event.type === 'content_block_delta' &&
              'delta' in event &&
              (event.delta as { type: string }).type === 'text_delta'
            ) {
              const chunk = (event.delta as { type: string; text: string }).text
              fullText += chunk
              send({ type: 'text', url, chunk })
            }
          }

          if (slackWebhook?.trim() && fullText) {
            try {
              await sendToSlack(slackWebhook.trim(), url, fullText)
              send({ type: 'slack', url, sent: true })
            } catch (e) {
              send({ type: 'slack', url, sent: false, error: String(e) })
            }
          }

          send({ type: 'complete', url })
        } catch (err) {
          send({ type: 'error', url, message: err instanceof Error ? err.message : String(err) })
        }
      }

      send({ type: 'done' })
      controller.close()
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    }
  })
}
