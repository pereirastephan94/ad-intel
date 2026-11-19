// Slow, polite full pull of one page's active ads from the public Ad Library.
// Facebook refuses "load more", so this loads ONE ordinary page view every few minutes, each with a
// different filter (sort order, media type, start-date window), and merges the ~30 ads each view embeds.
// Each new video is downloaded once (links expire), stills + transcript are saved; mp4s stay outside the repo.
//
// Usage: node scripts/slow-crawl.mjs <page_id> <out_dir_in_repo> <video_dir_outside_repo> [minGapMin] [maxGapMin]
import fs from 'node:fs'
import path from 'node:path'
import { loadLibraryUrl } from '../dist/facebook.js'
import { downloadVideo, processFile, genericHost } from '../dist/video.js'

const [pageId, OUT, VID, gapMin = '4', gapMax = '7'] = process.argv.slice(2)
fs.mkdirSync(path.join(OUT, 'videos'), { recursive: true })
fs.mkdirSync(path.join(OUT, 'images'), { recursive: true })
fs.mkdirSync(VID, { recursive: true })
const ADS = path.join(OUT, 'ads.json')
const STATE = path.join(OUT, 'crawl-state.json')
const ads = fs.existsSync(ADS) ? JSON.parse(fs.readFileSync(ADS, 'utf8')) : {}
const state = fs.existsSync(STATE) ? JSON.parse(fs.readFileSync(STATE, 'utf8')) : { done: [], queue: null, total: null, log: [] }
const log = (m) => { const l = `${new Date().toISOString()} ${m}`; console.log(l); state.log.push(l) }
const save = () => { fs.writeFileSync(ADS, JSON.stringify(ads, null, 1)); fs.writeFileSync(STATE, JSON.stringify(state, null, 1)) }
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
const day = (d) => d.toISOString().slice(0, 10)

const base = `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&is_targeted_country=false&search_type=page&view_all_page_id=${pageId}`
function urlFor(v) {
  let u = base + `&media_type=${v.media || 'all'}`
  if (v.sort) u += `&sort_data[mode]=${v.sort}&sort_data[direction]=${v.dir || 'desc'}`
  if (v.from) u += `&start_date[min]=${v.from}`
  if (v.to) u += `&start_date[max]=${v.to}`
  if (v.q) u += `&q=${encodeURIComponent(v.q)}`
  return u
}

if (!state.queue) {
  const q = []
  for (const media of ['all', 'video', 'image', 'meme'])
    for (const [sort, dir] of [['total_impressions', 'desc'], ['total_impressions', 'asc'], ['relevancy_monthly_grouped', 'desc']])
      q.push({ media, sort, dir })
  // Start-date windows, newest first: 3-day windows for 6 weeks, then wider back to a year.
  const today = new Date()
  const back = (n) => new Date(today.getTime() - n * 86400000)
  for (let d = 0; d < 42; d += 3) q.push({ from: day(back(d + 2)), to: day(back(d)), span: 3 })
  for (let d = 42; d < 180; d += 14) q.push({ from: day(back(d + 13)), to: day(back(d)), span: 14 })
  q.push({ from: day(back(365)), to: day(back(180)), span: 185 })
  q.push({ to: day(back(366)), span: 9999 })
  state.queue = q
}

// Keyword views: the date filter turned out to match "ran during", so nearly every ad shares one window.
// A keyword inside the page view does narrow the list, so slice by words instead.
if (!state.keywordsQueued) {
  state.queue = state.queue.filter((v) => !v.from && !v.to)
  const words = ['Ascend', 'PGP', 'MBA', 'undergraduate', 'CAT', 'XAT', 'founders', 'startup', 'AI', 'placement', 'salary', 'career',
    'internship', 'cohort', 'scholarship', 'admission', 'apply', 'job', 'LPA', 'CTC', 'business', 'build', 'immersion', 'tech', 'sales',
    'marketing', 'product', 'consulting', 'finance', 'experience', 'learn', 'IIM', 'Bangalore', 'Mesa', 'school', 'year', 'work', 'why',
    'how', 'you', 'your', 'the', 'not', 'from', 'with', 'for', 'and', 'is', 'to', 'in', 'of', 'a', 'I', 'we', 'our', 'this', 'what', 'who',
    'India', 'leaders', 'students', 'class', 'program', 'programme', 'founder', 'CEO', 'real', 'world', 'batch', 'join', 'now', 'today']
  for (const q of words) state.queue.push({ q })
  state.keywordsQueued = true
}
const key = (v) => JSON.stringify([v.media || 'all', v.sort || '', v.dir || '', v.from || '', v.to || '', v.q || '', v.retry || 0])
const seenViews = new Set(state.done.map(key))

function assetId(u) {
  try { return String(JSON.parse(Buffer.from(new URL(u).searchParams.get('efg'), 'base64').toString()).xpv_asset_id) } catch { return null }
}

async function handleMedia(a) {
  if (a.video_url) {
    const asset = assetId(a.video_url) || a.library_id
    a.video_asset = asset
    const dir = path.join(OUT, 'videos', asset)
    if (fs.existsSync(path.join(dir, 'transcript.json'))) return
    try {
      const mp4 = path.join(VID, `${asset}.mp4`)
      await downloadVideo(a.video_url, mp4)
      fs.mkdirSync(dir, { recursive: true })
      const tmp = fs.mkdtempSync(path.join(VID, 'tmp-'))
      const r = await processFile(mp4, tmp, 16)
      r.stills.forEach((s, i) => fs.writeFileSync(path.join(dir, `still${String(i).padStart(2, '0')}_${s.t}s.jpg`), Buffer.from(s.jpeg_base64, 'base64')))
      fs.writeFileSync(path.join(dir, 'transcript.json'), JSON.stringify({ asset, first_seen_in: a.library_id, duration_s: r.duration_s,
        stills: r.stills.map((s) => ({ t: s.t, why: s.why })), transcript: r.transcript, transcript_error: r.transcript_error }, null, 1))
      fs.rmSync(tmp, { recursive: true, force: true })
      log(`  video ${asset} ok (${r.duration_s}s, ${r.stills.length} stills)`)
    } catch (e) { log(`  video ${asset} FAILED: ${e.message}`) }
  } else if (a.thumbnail_url) {
    const f = path.join(OUT, 'images', `${a.library_id}.jpg`)
    if (fs.existsSync(f)) return
    for (const u of [a.thumbnail_url, a.thumbnail_url.replace(/\/\/scontent[^/]*\.fbcdn\.net/, '//scontent.xx.fbcdn.net')]) {
      try {
        const r = await fetch(u); if (!r.ok) continue
        fs.writeFileSync(f, Buffer.from(await r.arrayBuffer())); break
      } catch { /* try next host */ }
    }
  }
}

let emptyStreak = 0
let views = 0
const MAX_VIEWS = Number(process.env.MAX_VIEWS || 0) // 0 = no limit
while (state.queue.length) {
  const v = state.queue.shift()
  if (seenViews.has(key(v))) continue
  seenViews.add(key(v))
  let res
  try { res = await loadLibraryUrl(urlFor(v)) } catch (e) { log(`load error ${e.message}`); res = { raw: [], ads: [], total: null } }
  if (res.total > 0 && !v.from && !v.to && !v.q && (v.media || 'all') === 'all') state.total = Math.max(state.total || 0, res.total)
  let fresh = 0
  for (let i = 0; i < res.ads.length; i++) {
    const a = res.ads[i]
    if (String(a.page_id) !== String(pageId)) continue
    if (!ads[a.library_id]) { fresh++; ads[a.library_id] = { ...a, extra: { cards: res.raw[i].snapshot?.cards?.length || 0, display_format: res.raw[i].snapshot?.display_format, categories: res.raw[i].snapshot?.page_categories } } }
    else { ads[a.library_id].video_url = a.video_url; ads[a.library_id].thumbnail_url = a.thumbnail_url }
    await handleMedia(ads[a.library_id])
  }
  log(`view ${JSON.stringify(v)} -> ${res.ads.length} ads (window total ${res.total}), ${fresh} new, ${Object.keys(ads).length} unique of ~${state.total}`)
  // A keyword view that still hides ads and is still finding new ones: narrow it by media type and sort.
  if (v.q && fresh > 0 && res.total > res.ads.length) {
    const more = []
    if (!v.media) for (const media of ['video', 'meme', 'image']) more.push({ q: v.q, media })
    if (!v.sort) more.push({ ...v, sort: 'relevancy_monthly_grouped', dir: 'desc' })
    state.queue.unshift(...more.filter((m) => !seenViews.has(key(m))))
  }
  // Facebook sometimes answers a keyword view with nothing even when ads match; try each such view once more, later.
  if (v.q && !res.ads.length && !v.retry) state.queue.push({ ...v, retry: 1 })
  state.done.push(v)
  save()
  emptyStreak = res.ads.length === 0 && res.total == null ? emptyStreak + 1 : 0
  if (emptyStreak >= 3) { log('three empty views in a row: Facebook may be refusing us. Pausing 45 min.'); await sleep(45 * 60000); emptyStreak = 0 }
  if (state.total && Object.keys(ads).length >= state.total) { log('all reported ads collected'); break }
  if (MAX_VIEWS && ++views >= MAX_VIEWS) { log(`stopping after ${views} view(s) as asked`); break }
  await sleep((Number(gapMin) + Math.random() * (Number(gapMax) - Number(gapMin))) * 60000)
}
log(`${state.queue.length ? 'PAUSED' : 'DONE'}: ${Object.keys(ads).length} unique ads of ~${state.total}`)
save()
