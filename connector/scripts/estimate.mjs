// How big is this advertiser, and how long will a slow pull take? Costs ONE page view.
// Usage: node scripts/estimate.mjs <page_id> [country=IN]
//        node scripts/estimate.mjs --total <n> [video_share 0..1]     (no page view; just the arithmetic)
// Prints JSON; the "sentence" field is plain English to show the user.
import './chrome.mjs'
import { pathToFileURL } from 'node:url'

const MIN_PER_VIEW = 5.5 // one page view every 4 to 7 minutes
const hrs = (h) => (h < 0.75 ? `${Math.max(10, Math.round((h * 60) / 5) * 5)} minutes` : Math.round(h) <= 1 ? '1 hour' : `${Math.round(h)} hours`)

/**
 * The whole estimate lives here. Measured on one ~310-ad account (Mesa School of Business), one view per ~5.5 min,
 * 30 ads at most per view, many views repeating ads already seen:
 *   89 ads after 1.4 h, 148 after 2.75 h, 163 after 5.5 h, 221 after 8.3 h, 249 after 10.5 h (about 80%).
 * So: up to 30 ads is one or two views (about 10 minutes); about 100 ads is about 2 hours;
 * about 300 ads is 10 to 14 hours for roughly 80% of them. Linear between and beyond those points.
 * Write-ups: 1 to 2 minutes per new video, 30 to 60 seconds per new image.
 */
export function estimate(total, videoShare = 0.4) {
  if (!total || total < 0) return { total: null, sentence: 'The Ad Library did not report how many live ads this page has, so there is no time estimate. Expect about 2 hours per 100 ads.' }
  let lo, hi, coverage
  if (total <= 30) { lo = hi = 10 / 60; coverage = 100 }
  else if (total <= 100) { lo = 10 / 60 + ((total - 30) / 70) * (2 - 10 / 60); hi = lo * 1.2; coverage = 90 }
  else { lo = 2 + ((total - 100) / 200) * 8; hi = lo * 1.4; coverage = 80 }
  const expected = Math.round((total * coverage) / 100)
  // On Mesa about half of the video ads reused a video already seen; image ads were mostly one image each.
  const videos = Math.round(expected * videoShare * 0.5)
  const images = Math.round(expected * (1 - videoShare))
  const wLo = (videos * 1 + images * 0.5) / 60, wHi = (videos * 2 + images * 1) / 60
  const pull = lo === hi ? `about ${hrs(lo)}` : hrs(lo) === hrs(hi) ? `about ${hrs(lo)}` : `about ${hrs(lo).replace(/ hours?$/, '')} to ${hrs(hi)}`
  const write = hrs(wLo) === hrs(wHi) ? `about ${hrs(wHi)}` : `${hrs(wLo)} to ${hrs(wHi)}`
  const sentence =
    `This page has about ${total} live ads. ` +
    (total <= 30
      ? `That fits in one or two page views, so collecting them takes ${pull} and should get all of them. `
      : `Collecting them slowly (one ordinary page view every 4 to 7 minutes) will take ${pull}, and should reach roughly ${coverage}% of them (about ${expected} ads), not all. `) +
    `Writing up the creatives (about ${videos} different videos and ${images} images, at 1 to 2 minutes per video and under a minute per image) adds ${write}, spread across the batches.`
  return {
    total, expected_coverage_pct: coverage, expected_ads: expected,
    pull_hours_low: +lo.toFixed(1), pull_hours_high: +hi.toFixed(1), page_views_low: Math.ceil((lo * 60) / MIN_PER_VIEW), page_views_high: Math.ceil((hi * 60) / MIN_PER_VIEW),
    est_new_videos: videos, est_new_images: images, writeup_hours_low: +wLo.toFixed(1), writeup_hours_high: +wHi.toFixed(1),
    sentence,
  }
}

const STOP = new Set(('the and for you your with from that this what have will not are our can how why who now get all more just into than then them they their about ' +
  'been was has out one new its his her here there when where which while also only over most make made like know want need take every each much many some very ' +
  'http https www com apply learn more sign book shop today').split(' '))
/** Words that are common in this advertiser's own ad text: good extra search words for the slow pull. */
export function suggestWords(ads, max = 15) {
  const n = new Map()
  for (const a of ads) {
    const seen = new Set()
    for (const w of `${a.headline} ${a.link_description} ${a.body}`.split(/[^\p{L}\p{N}]+/u)) {
      const k = w.toLowerCase()
      if (k.length < 3 || STOP.has(k) || /^\d+$/.test(k) || seen.has(k)) continue
      seen.add(k); n.set(k, (n.get(k) || 0) + 1)
    }
  }
  return [...n.entries()].filter(([, c]) => c >= 2).sort((a, b) => b[1] - a[1]).slice(0, max).map(([w]) => w)
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const args = process.argv.slice(2)
  if (args[0] === '--total') { console.log(JSON.stringify(estimate(Number(args[1]), args[2] ? Number(args[2]) : undefined), null, 1)); process.exit(0) }
  const [pageId, country = 'IN'] = args
  if (!pageId) { console.error('Usage: node scripts/estimate.mjs <page_id> [country=IN]'); process.exit(2) }
  try {
    const { loadLibraryUrl } = await import('../dist/facebook.js')
    const url = `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=${country.toUpperCase()}&is_targeted_country=false&media_type=all` +
      `&search_type=page&sort_data[mode]=total_impressions&sort_data[direction]=desc&view_all_page_id=${pageId}`
    const res = await loadLibraryUrl(url)
    const mine = res.ads.filter((a) => String(a.page_id) === String(pageId))
    const videoShare = mine.length ? mine.filter((a) => a.video_url).length / mine.length : undefined
    // If Facebook gives no total but the view is not full, the view is the whole account.
    const total = res.total ?? (mine.length && mine.length < 30 ? mine.length : null)
    const e = estimate(total, videoShare)
    console.log(JSON.stringify({
      page_id: pageId, country: country.toUpperCase(), page_name: mine[0]?.page_name || null,
      total_live_ads_reported: res.total, ads_in_this_view: mine.length,
      video_share_in_view: videoShare == null ? null : +videoShare.toFixed(2),
      oldest_start_in_view: mine.map((a) => a.start_date).filter(Boolean).sort()[0] || null,
      landing_sites_in_view: [...new Set(mine.map((a) => { try { return new URL(a.landing_url).hostname } catch { return null } }).filter(Boolean))],
      suggested_extra_words: suggestWords(mine),
      ...e,
      note: mine.length ? undefined : 'No ads came back for this page. Check the page id and country, and wait a few minutes before trying again.',
    }, null, 1))
    process.exit(0)
  } catch (e) {
    console.error(`estimate failed: ${e.message}`)
    process.exit(1)
  }
}
