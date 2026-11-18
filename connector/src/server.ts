// Ad Audit connector: a remote MCP server (Streamable HTTP) that Claude calls.
// Claude does the thinking; this server only fetches public Ad Library data and processes video.

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js'
import { createMcpExpressApp } from '@modelcontextprotocol/sdk/server/express.js'
import type { Request, Response } from 'express'
import { timingSafeEqual } from 'node:crypto'
import * as z from 'zod/v4'
import { findAdvertiser, listAds, getAd, closeBrowser } from './facebook.js'
import { analyzeVideo } from './video.js'
import { AUDIT_GUIDE, auditPrompt } from './prompt.js'

const PORT = Number(process.env.PORT || 8080)
const TOKEN = process.env.ACCESS_TOKEN || ''
if (!TOKEN && process.env.ALLOW_NO_TOKEN !== '1') {
  console.error('ACCESS_TOKEN is not set. Set it to a long random string (see README). Refusing to start.')
  process.exit(1)
}

// One heavy job (browser page or video) at a time keeps a small machine alive.
let queue: Promise<unknown> = Promise.resolve()
function oneAtATime<T>(fn: () => Promise<T>): Promise<T> {
  const p = queue.then(fn, fn)
  queue = p.catch(() => {})
  return p
}

const text = (t: string) => ({ type: 'text' as const, text: t })
const fail = (t: string) => ({ content: [text(t)], isError: true })

function buildServer() {
  const server = new McpServer(
    { name: 'ad-audit', version: '1.0.0' },
    { instructions: AUDIT_GUIDE },
  )

  server.registerTool(
    'find_advertiser',
    {
      title: 'Find advertiser',
      description:
        'Search the public Facebook Ad Library for a business name and return candidate Facebook pages ' +
        '(page name, page ID, rough number of active ads). Show these to the user and confirm the right page before listing ads.',
      inputSchema: {
        name: z.string().min(2).describe('Business or brand name, e.g. "Mesa School of Business"'),
        country: z.string().length(2).default('IN').describe('Two-letter country code for the Ad Library. Default IN.'),
      },
      annotations: { readOnlyHint: true, openWorldHint: true },
    },
    async ({ name, country }) => {
      try {
        const r = await oneAtATime(() => findAdvertiser(name, country.toUpperCase()))
        return { content: [text(JSON.stringify(r, null, 1))] }
      } catch (e: any) {
        return fail(`Search failed: ${e.message}`)
      }
    },
  )

  server.registerTool(
    'list_ads',
    {
      title: 'List active ads',
      description:
        "List a page's active ads from the Ad Library, longest-running first (long-running ads are usually the ones that work), " +
        'then by number of copies. Per ad: Library ID and link, start date, days running, text, headline, CTA, landing URL, ' +
        'media type, video URL, thumbnail, copies. Facebook rate-limits paging, so you may get only ~30; the notes say so.',
      inputSchema: {
        page_id: z.string().regex(/^\d+$/).describe('Facebook page ID from find_advertiser'),
        limit: z.number().int().min(1).max(100).default(30).describe('Max ads to return (default 30)'),
        country: z.string().length(2).default('IN').describe('Two-letter country code. Default IN.'),
      },
      annotations: { readOnlyHint: true, openWorldHint: true },
    },
    async ({ page_id, limit, country }) => {
      try {
        const r = await oneAtATime(() => listAds(page_id, limit, country.toUpperCase()))
        return { content: [text(JSON.stringify(r, null, 1))] }
      } catch (e: any) {
        return fail(`Could not load ads: ${e.message}`)
      }
    },
  )

  server.registerTool(
    'analyze_video',
    {
      title: 'Analyse a video ad',
      description:
        'Download one video ad, return its transcript with timestamps plus up to 12 still frames as images ' +
        '(0, 0.5, 1, 2, 3 s, scene changes, last frame). Look at the stills: on-screen text often holds the real claims, ' +
        'and fixes transcript errors. Give a library_id from list_ads (preferred) or a video_url. Takes 30-90 seconds.',
      inputSchema: {
        library_id: z.string().regex(/^\d+$/).optional().describe('Ad Library ID from list_ads'),
        video_url: z.string().url().optional().describe('Direct video URL from list_ads, if no library_id'),
      },
      annotations: { readOnlyHint: true, openWorldHint: true },
    },
    async ({ library_id, video_url }) => {
      if (!library_id && !video_url) return fail('Give a library_id or a video_url.')
      try {
        let url = video_url
        let ad = null
        if (library_id) {
          ad = await oneAtATime(() => getAd(library_id))
          if (!ad) return fail(`Ad ${library_id} was not found in the Ad Library (it may have stopped running).`)
          if (!ad.video_url) return fail(`Ad ${library_id} is a ${ad.media_type} ad, not a video. Its image: ${ad.thumbnail_url}`)
          url = ad.video_url
        }
        if (url && !/^https:\/\/[^/]+\.fbcdn\.net\//.test(url)) return fail('Only Facebook video links (fbcdn.net) are accepted.')
        const v = await oneAtATime(() => analyzeVideo(url!))
        const head = [
          library_id ? `Ad ${library_id}: https://www.facebook.com/ads/library/?id=${library_id}` : `Video: ${url}`,
          ad ? `Started ${ad.start_date}, ${ad.days_running} days running, ${ad.copies} copies. Headline: ${ad.headline}. CTA: ${ad.cta}.` : '',
          `Length: ${v.duration_s}s. Stills: ${v.stills.length}.`,
          v.transcript
            ? `Transcript (language: ${v.transcript.language}; machine transcription, check names and numbers against the stills):\n` +
              v.transcript.segments.map((s) => `[${s.start.toFixed(1)}-${s.end.toFixed(1)}s] ${s.text}`).join('\n')
            : `No transcript. ${v.transcript_error || ''}`,
        ]
          .filter(Boolean)
          .join('\n')
        const content: any[] = [text(head)]
        for (const s of v.stills) {
          content.push(text(`Still at ${s.t}s (${s.why})`))
          content.push({ type: 'image', data: s.jpeg_base64, mimeType: 'image/jpeg' })
        }
        return { content }
      } catch (e: any) {
        return fail(`Video analysis failed: ${e.message}`)
      }
    },
  )

  server.registerPrompt(
    'audit',
    {
      title: 'Audit an advertiser',
      description: "Full audit of a competitor's Facebook and Instagram ads, video included",
      argsSchema: {
        advertiser: z.string().describe('Business to audit, e.g. "Mesa School of Business"'),
        my_business: z.string().optional().describe('Your own business, so the audit says what to run against them'),
      },
    },
    ({ advertiser, my_business }) => ({
      messages: [{ role: 'user', content: { type: 'text', text: auditPrompt(advertiser, my_business) } }],
    }),
  )

  return server
}

function tokenOk(req: Request): boolean {
  const given = (req.params.token as string) || (req.headers.authorization || '').replace(/^Bearer\s+/i, '')
  if (!TOKEN) return true
  const a = Buffer.from(given || '')
  const b = Buffer.from(TOKEN)
  return a.length === b.length && timingSafeEqual(a, b)
}

const app = createMcpExpressApp({ host: '0.0.0.0' })

app.get('/health', (_req: Request, res: Response) => {
  res.json({ ok: true })
})

async function handle(req: Request, res: Response) {
  if (!tokenOk(req)) {
    res.status(401).json({ jsonrpc: '2.0', error: { code: -32001, message: 'Unauthorized' }, id: null })
    return
  }
  if (req.method !== 'POST') {
    res.status(405).json({ jsonrpc: '2.0', error: { code: -32000, message: 'Method not allowed.' }, id: null })
    return
  }
  const server = buildServer()
  try {
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined })
    res.on('close', () => {
      transport.close()
      server.close()
    })
    await server.connect(transport)
    await transport.handleRequest(req, res, req.body)
  } catch (e) {
    console.error('MCP error', e)
    if (!res.headersSent)
      res.status(500).json({ jsonrpc: '2.0', error: { code: -32603, message: 'Internal server error' }, id: null })
  }
}

// Secret in the path (for claude.ai custom connectors) or in an Authorization: Bearer header.
app.all('/mcp/:token', handle)
app.all('/mcp', handle)

app.listen(PORT, () => {
  console.log(`Ad Audit connector listening on port ${PORT}. MCP endpoint: /mcp/<ACCESS_TOKEN>`)
})

for (const sig of ['SIGINT', 'SIGTERM'])
  process.on(sig, async () => {
    await closeBrowser()
    process.exit(0)
  })
