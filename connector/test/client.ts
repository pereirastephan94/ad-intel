// End-to-end test: talks to a running connector exactly like Claude would.
// Usage: MCP_URL=http://localhost:8080/mcp/<token> OUT=<folder for stills> npx tsx test/client.ts [page_id] [videos]
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js'
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const url = process.env.MCP_URL || 'http://localhost:8080/mcp/test-token'
const out = process.env.OUT || './work'
const pageId = process.argv[2] || '115513081449393'
const nVideos = Number(process.argv[3] || 3)
mkdirSync(out, { recursive: true })

const client = new Client({ name: 'test-client', version: '1.0.0' })
await client.connect(new StreamableHTTPClientTransport(new URL(url)))
const textOf = (r: any) => r.content.filter((c: any) => c.type === 'text').map((c: any) => c.text).join('\n')
const log: string[] = []
const say = (s: string) => { console.log(s); log.push(s) }

const tools = await client.listTools()
say(`Tools: ${tools.tools.map((t) => t.name).join(', ')}`)
const prompts = await client.listPrompts()
say(`Prompts: ${prompts.prompts.map((p) => p.name).join(', ')}`)

let t = Date.now()
const fa = await client.callTool({ name: 'find_advertiser', arguments: { name: 'Mesa School of Business' } }, undefined, { timeout: 300000 })
const faj = JSON.parse(textOf(fa))
say(`\nfind_advertiser (${((Date.now() - t) / 1000).toFixed(0)}s):`)
for (const c of faj.candidates) say(`  ${c.page_name} | ${c.page_id} | rough ads ${c.rough_active_ads} | in sample ${c.ads_seen_in_sample}`)

t = Date.now()
const la = await client.callTool({ name: 'list_ads', arguments: { page_id: pageId, limit: 30 } }, undefined, { timeout: 300000 })
const laj = JSON.parse(textOf(la))
writeFileSync(path.join(out, 'list_ads.json'), JSON.stringify(laj, null, 1))
say(`\nlist_ads (${((Date.now() - t) / 1000).toFixed(0)}s): ${laj.page_name}, returned ${laj.returned}, reported total ${laj.total_active_reported}, types ${JSON.stringify(laj.media_types)}`)
for (const n of laj.notes) say(`  note: ${n}`)
for (const a of laj.ads.slice(0, 8)) say(`  ${a.library_id} | ${a.media_type} | ${a.days_running}d | ${a.copies} copies | ${a.headline.slice(0, 50)} | ${a.landing_url.slice(0, 40)}`)

const vids = laj.ads.filter((a: any) => a.video_url).slice(0, nVideos)
for (const v of vids) {
  t = Date.now()
  const r: any = await client.callTool({ name: 'analyze_video', arguments: { library_id: v.library_id } }, undefined, { timeout: 600000 })
  const imgs = r.content.filter((c: any) => c.type === 'image')
  const dir = path.join(out, v.library_id)
  mkdirSync(dir, { recursive: true })
  imgs.forEach((c: any, i: number) => writeFileSync(path.join(dir, `still${String(i).padStart(2, '0')}.jpg`), Buffer.from(c.data, 'base64')))
  const head = textOf(r)
  writeFileSync(path.join(dir, 'result.txt'), head)
  say(`\nanalyze_video ${v.library_id} (${((Date.now() - t) / 1000).toFixed(0)}s): error=${!!r.isError}, ${imgs.length} images`)
  say(head.split('\n').filter((l: string) => !l.startsWith('Still at')).slice(0, 8).map((l: string) => '  ' + l.slice(0, 160)).join('\n'))
}

// Auth check: wrong token must be refused.
const bad = await fetch(url.replace(/\/mcp\/.*/, '/mcp/wrong'), { method: 'POST', headers: { 'content-type': 'application/json', accept: 'application/json, text/event-stream' }, body: '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' })
say(`\nWrong token -> HTTP ${bad.status}`)
writeFileSync(path.join(out, 'log.txt'), log.join('\n'))
await client.close()
