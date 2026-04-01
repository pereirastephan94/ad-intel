import { chromium } from 'playwright'

export interface ScrapeResult {
  success: boolean
  rawText?: string
  adCount?: number
  pageId?: string
  error?: string
}

/**
 * Scrapes Facebook Ad Library for a given competitor URL using a real Chromium browser.
 * Bypasses bot detection that blocks server-side HTTP fetchers.
 */
export async function scrapeAdLibraryWithPlaywright(competitorUrl: string): Promise<ScrapeResult> {
  let browser = null

  try {
    // Extract company name / domain from URL for search
    const domain = (() => {
      try { return new URL(competitorUrl).hostname.replace('www.', '') }
      catch { return competitorUrl }
    })()
    const companyName = domain.split('.')[0]

    browser = await chromium.launch({ headless: true })
    const context = await browser.newContext({
      userAgent:
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
        '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      locale: 'en-US',
      viewport: { width: 1280, height: 900 },
    })
    const page = await context.newPage()

    // ── STEP 1: Search Ad Library by keyword to find the page ─────────────────
    const searchUrl =
      `https://www.facebook.com/ads/library/?active_status=active&ad_type=all` +
      `&country=IN&is_targeted_country=false&media_type=all` +
      `&q=${encodeURIComponent(companyName)}&search_type=keyword_unordered`

    await page.goto(searchUrl, { waitUntil: 'networkidle', timeout: 30000 })
    await page.waitForTimeout(4000)

    // ── STEP 2: Try to find "See all ads from this page" link → extract page ID
    let pageId: string | undefined
    let pageSpecificUrl: string | undefined

    // Look for links containing view_all_page_id in the rendered page
    const links = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('a[href*="view_all_page_id"]'))
        .map(a => (a as HTMLAnchorElement).href)
    })

    if (links.length > 0) {
      const match = links[0].match(/view_all_page_id=(\d+)/)
      if (match) {
        pageId = match[1]
        pageSpecificUrl =
          `https://www.facebook.com/ads/library/?active_status=active&ad_type=all` +
          `&country=IN&is_targeted_country=false&media_type=all&search_type=page` +
          `&sort_data[mode]=total_impressions&sort_data[direction]=desc` +
          `&view_all_page_id=${pageId}`
      }
    }

    // ── STEP 3: If page ID found, navigate to page-specific Ad Library ────────
    if (pageSpecificUrl) {
      await page.goto(pageSpecificUrl, { waitUntil: 'networkidle', timeout: 30000 })
      await page.waitForTimeout(4000)
    }

    // ── STEP 4: Scroll to load all ads ────────────────────────────────────────
    for (let i = 0; i < 6; i++) {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
      await page.waitForTimeout(2500)
    }

    // Expand any "See more" / "See full ad" buttons
    const expandButtons = await page.$$('div[role="button"]')
    for (const btn of expandButtons.slice(0, 40)) {
      try {
        const text = await btn.textContent()
        if (text && (text.includes('See more') || text.includes('See full ad'))) {
          await btn.click()
          await page.waitForTimeout(300)
        }
      } catch { /* ignore click errors */ }
    }

    // ── STEP 5: Extract raw page text ─────────────────────────────────────────
    const rawText = await page.innerText('body')

    // Count library IDs as a proxy for ad count
    const libIdMatches = rawText.match(/Library ID[:\s]*\d{10,}/g) ?? []
    const adCount = libIdMatches.length

    await browser.close()

    if (!rawText || rawText.length < 500) {
      return { success: false, error: 'Page returned too little content — likely blocked or empty' }
    }

    // Cap at 80k chars to stay within Claude context limits
    return {
      success: true,
      rawText: rawText.slice(0, 80000),
      adCount,
      pageId,
    }
  } catch (err) {
    if (browser) {
      try { await browser.close() } catch { /* ignore */ }
    }
    return {
      success: false,
      error: err instanceof Error ? err.message : String(err),
    }
  }
}
