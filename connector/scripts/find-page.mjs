// Find the Facebook page(s) that match a company name in the public Ad Library.
// Usage: node scripts/find-page.mjs "<name>" [country=IN] [--exact]
// Step 1 (one page view): findAdvertiser, a loose keyword search. Facebook sometimes answers it with unrelated pages.
// Step 2 (only if step 1 found no page whose name matches; waits 75 s first, one more page view): an exact-phrase
//         search for the name, reading the pages off the ads that come back. --exact skips step 1.
// Prints JSON: { query, country, candidates: [{ page_id, page_name, name_match, rough_active_ads, ads_seen_in_sample,
//               likes, categories, page_url, ads_library_link }], note }
import './chrome.mjs'
import { findAdvertiser, loadLibraryUrl } from '../dist/facebook.js'

const args = process.argv.slice(2)
const exactOnly = args.includes('--exact')
const [name, country = 'IN'] = args.filter((a) => a !== '--exact')
if (!name) { console.error('Usage: node scripts/find-page.mjs "<name>" [country=IN] [--exact]'); process.exit(2) }
const CC = country.toUpperCase()
const LIB = 'https://www.facebook.com/ads/library/'
const words = (s) => (s || '').toLowerCase().split(/[^\p{L}\p{N}]+/u).filter(Boolean)
const q = words(name)
function match(pageName) {
  const p = words(pageName)
  if (p.join(' ') === q.join(' ')) return 'exact'
  return q.every((w) => p.includes(w)) || (p.length && p.every((w) => q.includes(w))) ? 'partial' : 'no'
}
const rank = (c) => ({ exact: 2, partial: 1, no: 0 })[c.name_match] * 1000 + (c.rough_active_ads === '100+' ? 100 : Number(c.rough_active_ads) || 0) + c.ads_seen_in_sample
const link = (id) => `${LIB}?active_status=active&ad_type=all&country=${CC}&view_all_page_id=${id}&search_type=page`

async function exactPhrase() {
  const res = await loadLibraryUrl(`${LIB}?active_status=active&ad_type=all&country=${CC}&is_targeted_country=false&media_type=all` +
    `&search_type=keyword_exact_phrase&q=${encodeURIComponent(`"${name}"`)}`)
  const by = new Map()
  for (const raw of res.raw) {
    const id = String(raw.page_id)
    const c = by.get(id) || { page_id: id, page_name: raw.page_name || raw.snapshot?.page_name, rough_active_ads: 'unknown', ads_seen_in_sample: 0, likes: null, categories: null, page_url: null }
    c.ads_seen_in_sample++
    c.likes = raw.snapshot?.page_like_count ?? c.likes
    c.categories = raw.snapshot?.page_categories ?? c.categories
    c.page_url = raw.snapshot?.page_profile_uri ?? c.page_url
    by.set(id, c)
  }
  return [...by.values()]
}

try {
  const by = new Map()
  const steps = []
  if (!exactOnly) {
    const r = await findAdvertiser(name, CC)
    for (const c of r.candidates) by.set(c.page_id, c)
    steps.push('keyword search')
  }
  if (![...by.values()].some((c) => match(c.page_name) !== 'no')) {
    if (!exactOnly) await new Promise((r) => setTimeout(r, 75000))
    for (const c of await exactPhrase()) by.set(c.page_id, { ...(by.get(c.page_id) || {}), ...c })
    steps.push('exact-phrase search')
  }
  const candidates = [...by.values()]
    .map((c) => ({ page_id: c.page_id, page_name: c.page_name, name_match: match(c.page_name), rough_active_ads: c.rough_active_ads, ads_seen_in_sample: c.ads_seen_in_sample,
      likes: c.likes ?? null, categories: c.categories ?? null, page_url: c.page_url ?? null, ads_library_link: link(c.page_id) }))
    .sort((a, b) => rank(b) - rank(a))
  const good = candidates.filter((c) => c.name_match !== 'no')
  console.log(JSON.stringify({
    query: name, country: CC, searched_with: steps, plausible_matches: good.length, candidates,
    note: good.length === 1 ? 'One page matches the name. Use it, and tell the user which page it is.'
      : good.length > 1 ? 'More than one page matches the name. Ask the user which one (show name, likes and the link).'
      : candidates.length ? 'No page name matches the search. Show the user the closest ones, or ask them to paste the page link from facebook.com/ads/library (the number after view_all_page_id is the page id).'
      : 'Nothing came back. Try a shorter or different spelling or another country code, once, after a few minutes. Or ask the user to paste the page link from facebook.com/ads/library.',
  }, null, 1))
  process.exit(0)
} catch (e) {
  console.error(`find-page failed: ${e.message}`)
  process.exit(1)
}
