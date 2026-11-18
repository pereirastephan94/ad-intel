// Reads the public Facebook Ad Library, logged out, with a real browser.
// Data comes from the JSON the page itself loads (embedded <script type="application/json">
// blocks in the first page load, and /api/graphql/ responses when it pages), never page text.

import { chromium, type Browser, type BrowserContext } from 'playwright'

const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
const LIB = 'https://www.facebook.com/ads/library/'

export interface Ad {
  library_id: string
  link: string
  page_id: string
  page_name: string
  is_active: boolean
  start_date: string | null
  days_running: number | null
  media_type: string
  body: string
  headline: string
  link_description: string
  cta: string
  landing_url: string
  video_url: string | null
  thumbnail_url: string | null
  copies: number
  platforms: string[]
}

export interface Candidate {
  page_id: string
  page_name: string
  rough_active_ads: string
  ads_seen_in_sample: number
  likes: number | null
  page_url: string | null
}

let browserP: Promise<Browser> | null = null
function browser(): Promise<Browser> {
  if (!browserP) {
    browserP = chromium
      .launch({
        headless: true,
        executablePath: process.env.CHROME_PATH || undefined,
        args: ['--no-sandbox', '--disable-dev-shm-usage'],
      })
      .catch((e) => {
        browserP = null
        throw e
      })
  }
  return browserP
}

async function newContext(): Promise<BrowserContext> {
  const b = await browser()
  return b.newContext({ userAgent: UA, locale: 'en-US', viewport: { width: 1280, height: 900 } })
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

// ---------- JSON extraction ----------

function walk(o: unknown, found: { ads: any[]; pages: any[]; total?: number }) {
  if (!o || typeof o !== 'object') return
  if (Array.isArray(o)) {
    for (const x of o) walk(x, found)
    return
  }
  const r = o as Record<string, any>
  if (r.ad_archive_id && r.snapshot) {
    found.ads.push(r)
    return
  }
  if (r.dynamic_filter_options?.pages) found.pages.push(...r.dynamic_filter_options.pages)
  if (r.search_results_connection && typeof r.search_results_connection.count === 'number')
    found.total = r.search_results_connection.count
  for (const k in r) walk(r[k], found)
}

/** Pull every JSON object out of an HTML document or a (possibly multi-line) graphql body. */
export function extractFromText(text: string, found: { ads: any[]; pages: any[]; total?: number; rateLimited?: boolean }) {
  if (text.includes('Rate limit exceeded')) found.rateLimited = true
  const blocks: string[] = []
  if (text.trimStart().startsWith('<')) {
    const re = /<script type="application\/json"[^>]*>([\s\S]*?)<\/script>/g
    let m
    while ((m = re.exec(text))) blocks.push(m[1])
  } else {
    blocks.push(...text.replace(/^for \(;;\);/, '').split('\n'))
  }
  for (const b of blocks) {
    if (!b.includes('ad_archive_id') && !b.includes('dynamic_filter_options') && !b.includes('search_results_connection'))
      continue
    try {
      walk(JSON.parse(b), found)
    } catch {
      /* not JSON */
    }
  }
}

function decodeLanding(u: string | null | undefined): string {
  if (!u) return ''
  try {
    const url = new URL(u)
    if (url.hostname.startsWith('l.facebook.com') || url.hostname.startsWith('lm.facebook.com')) {
      return url.searchParams.get('u') || u
    }
  } catch {
    /* keep as is */
  }
  return u
}

function clean(s: unknown): string {
  if (typeof s !== 'string') return ''
  // Dynamic-creative placeholders like {{product.brand}} are not useful text.
  return s.trim()
}

export function normalise(raw: any): Ad {
  const s = raw.snapshot || {}
  const card = (s.cards && s.cards[0]) || {}
  const vid = (s.videos && s.videos[0]) || {}
  const img = (s.images && s.images[0]) || {}
  const start = typeof raw.start_date === 'number' ? raw.start_date * 1000 : null
  const end = !raw.is_active && typeof raw.end_date === 'number' ? raw.end_date * 1000 : Date.now()
  const video = vid.video_hd_url || vid.video_sd_url || card.video_hd_url || card.video_sd_url || null
  return {
    library_id: String(raw.ad_archive_id),
    link: `https://www.facebook.com/ads/library/?id=${raw.ad_archive_id}`,
    page_id: String(raw.page_id || s.page_id || ''),
    page_name: raw.page_name || s.page_name || '',
    is_active: !!raw.is_active,
    start_date: start ? new Date(start).toISOString().slice(0, 10) : null,
    days_running: start ? Math.max(1, Math.round((end - start) / 86400000)) : null,
    media_type: video ? 'VIDEO' : String(s.display_format || (img.original_image_url ? 'IMAGE' : 'UNKNOWN')),
    body: clean(s.body?.text) || clean(card.body),
    headline: clean(s.title) || clean(card.title),
    link_description: clean(s.link_description) || clean(card.link_description),
    cta: clean(s.cta_text) || clean(card.cta_text),
    landing_url: decodeLanding(s.link_url || card.link_url),
    video_url: video,
    thumbnail_url:
      vid.video_preview_image_url ||
      card.video_preview_image_url ||
      img.original_image_url ||
      img.resized_image_url ||
      card.original_image_url ||
      card.resized_image_url ||
      null,
    copies: typeof raw.collation_count === 'number' ? raw.collation_count : 1,
    platforms: raw.publisher_platform || [],
  }
}

// Ads seen recently, so analyze_video can work from a Library ID.
export const adCache = new Map<string, Ad>()

// ---------- Tools ----------

export async function findAdvertiser(name: string, country = 'IN') {
  const ctx = await newContext()
  const found: { ads: any[]; pages: any[]; total?: number; rateLimited?: boolean } = { ads: [], pages: [] }
  try {
    const page = await ctx.newPage()
    page.on('response', async (r) => {
      const u = r.url()
      if (!u.includes('/api/graphql') && !u.startsWith(LIB)) return
      try {
        extractFromText(await r.text(), found)
      } catch {
        /* body gone */
      }
    })
    const url =
      `${LIB}?active_status=active&ad_type=all&country=${country}&is_targeted_country=false` +
      `&media_type=all&search_type=keyword_unordered&q=${encodeURIComponent(name)}`
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
    await page.waitForTimeout(7000)
  } finally {
    await ctx.close()
    await closeBrowser() // free ~400 MB before any Whisper run
  }

  const byId = new Map<string, Candidate>()
  for (const p of found.pages) {
    byId.set(String(p.key), {
      page_id: String(p.key),
      page_name: p.display_name,
      rough_active_ads: p.count >= 100 ? '100+' : String(p.count),
      ads_seen_in_sample: 0,
      likes: null,
      page_url: null,
    })
  }
  for (const raw of found.ads) {
    const id = String(raw.page_id)
    const c =
      byId.get(id) ||
      ({
        page_id: id,
        page_name: raw.page_name,
        rough_active_ads: 'unknown',
        ads_seen_in_sample: 0,
        likes: null,
        page_url: null,
      } as Candidate)
    c.ads_seen_in_sample++
    c.likes = raw.snapshot?.page_like_count ?? c.likes
    c.page_url = raw.snapshot?.page_profile_uri ?? c.page_url
    byId.set(id, c)
  }
  const candidates = [...byId.values()].sort(
    (a, b) =>
      (b.rough_active_ads === '100+' ? 100 : Number(b.rough_active_ads) || 0) +
      b.ads_seen_in_sample -
      ((a.rough_active_ads === '100+' ? 100 : Number(a.rough_active_ads) || 0) + a.ads_seen_in_sample),
  )
  return {
    query: name,
    country,
    candidates: candidates.map((c) => ({
      ...c,
      ads_library_link: `${LIB}?active_status=active&ad_type=all&country=${country}&view_all_page_id=${c.page_id}&search_type=page`,
    })),
    note:
      'Counts are rough: "rough_active_ads" comes from the Ad Library filter (it caps at 100+), ' +
      '"ads_seen_in_sample" is how many of the first ~30 keyword results came from that page. ' +
      'Ask the user to confirm the right page before calling list_ads.',
  }
}

export async function listAds(pageId: string, limit = 30, country = 'IN') {
  const ctx = await newContext()
  const found: { ads: any[]; pages: any[]; total?: number; rateLimited?: boolean } = { ads: [], pages: [] }
  const notes: string[] = []
  try {
    const page = await ctx.newPage()
    page.on('response', async (r) => {
      const u = r.url()
      if (!u.includes('/api/graphql') && !u.startsWith(LIB)) return
      try {
        extractFromText(await r.text(), found)
      } catch {
        /* body gone */
      }
    })
    const url =
      `${LIB}?active_status=active&ad_type=all&country=${country}&is_targeted_country=false&media_type=all` +
      `&search_type=page&sort_data[mode]=total_impressions&sort_data[direction]=desc&view_all_page_id=${pageId}`
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
    await page.waitForTimeout(6000)

    // Page gently for more, one scroll at a time, and stop at the first rate-limit.
    let lastCount = -1
    for (let i = 0; i < 20 && uniq(found.ads).length < limit; i++) {
      if (found.rateLimited) break
      const n = uniq(found.ads).length
      if (n === lastCount && i > 2) break
      lastCount = n
      await page.mouse.wheel(0, 6000)
      await page.waitForTimeout(3500 + Math.random() * 2000)
    }
  } finally {
    await ctx.close()
    await closeBrowser() // free ~400 MB before any Whisper run
  }

  const ads = uniq(found.ads).map(normalise)
  for (const a of ads) adCache.set(a.library_id, a)
  ads.sort((a, b) => (b.days_running ?? 0) - (a.days_running ?? 0) || b.copies - a.copies)
  const out = ads.slice(0, limit)

  if (found.rateLimited)
    notes.push(
      `Facebook said "Rate limit exceeded" when asked for more ads, so this is only the first ${ads.length}. ` +
        'Try again later for more; do not retry straight away.',
    )
  if (found.total != null) notes.push(`The Ad Library reports about ${found.total} active ads for this page in total.`)
  if (!ads.length) notes.push('No ads came back. Check the page ID with find_advertiser, or try a different country.')

  const counts: Record<string, number> = {}
  for (const a of out) counts[a.media_type] = (counts[a.media_type] || 0) + 1
  return {
    page_id: pageId,
    page_name: out[0]?.page_name || null,
    total_active_reported: found.total ?? null,
    returned: out.length,
    media_types: counts,
    notes,
    ads: out,
  }
}

function uniq(raw: any[]): any[] {
  const m = new Map<string, any>()
  for (const r of raw) if (!m.has(String(r.ad_archive_id))) m.set(String(r.ad_archive_id), r)
  return [...m.values()]
}

/** Look up one ad by Library ID (used when analyze_video is called cold). */
export async function getAd(libraryId: string): Promise<Ad | null> {
  if (adCache.has(libraryId)) return adCache.get(libraryId)!
  const ctx = await newContext()
  const found: { ads: any[]; pages: any[]; total?: number; rateLimited?: boolean } = { ads: [], pages: [] }
  try {
    const page = await ctx.newPage()
    page.on('response', async (r) => {
      const u = r.url()
      if (!u.includes('/api/graphql') && !u.startsWith(LIB)) return
      try {
        extractFromText(await r.text(), found)
      } catch {
        /* body gone */
      }
    })
    await page.goto(`${LIB}?id=${libraryId}`, { waitUntil: 'domcontentloaded', timeout: 60000 })
    await page.waitForTimeout(6000)
  } finally {
    await ctx.close()
    await closeBrowser() // free ~400 MB before any Whisper run
  }
  for (const raw of uniq(found.ads)) adCache.set(String(raw.ad_archive_id), normalise(raw))
  return adCache.get(libraryId) || null
}

/** Load one Ad Library URL once (no scrolling, so no "load more" requests) and return what it embeds. */
export async function loadLibraryUrl(url: string) {
  const ctx = await newContext()
  const found: { ads: any[]; pages: any[]; total?: number; rateLimited?: boolean } = { ads: [], pages: [] }
  try {
    const page = await ctx.newPage()
    page.on('response', async (r) => {
      if (!r.url().startsWith(LIB)) return
      try {
        extractFromText(await r.text(), found)
      } catch {
        /* body gone */
      }
    })
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 })
    await page.waitForTimeout(5000)
  } finally {
    await ctx.close()
    await closeBrowser()
  }
  return { raw: uniq(found.ads), ads: uniq(found.ads).map(normalise), total: found.total ?? null }
}

export async function closeBrowser() {
  if (browserP) await (await browserP).close().catch(() => {})
  browserP = null
}

export { sleep }
