'use client'

import { useState, useRef } from 'react'

type StreamEvent =
  | { type: 'status'; url: string; message: string }
  | { type: 'text'; url: string; chunk: string }
  | { type: 'slack'; url: string; sent: boolean; error?: string }
  | { type: 'complete'; url: string }
  | { type: 'error'; url: string; message: string }
  | { type: 'done' }

interface Result {
  text: string
  status: string
  done: boolean
  error?: string
  slackSent?: boolean
}

export default function Home() {
  const [urls, setUrls] = useState<string[]>([''])
  const [yourUrl, setYourUrl] = useState('')
  const [slackWebhook, setSlackWebhook] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [results, setResults] = useState<Record<string, Result>>({})
  const [loading, setLoading] = useState(false)
  const [globalDone, setGlobalDone] = useState(false)
  const resultsRef = useRef<HTMLDivElement>(null)

  const addUrl = () => { if (urls.length < 5) setUrls([...urls, '']) }
  const removeUrl = (i: number) => setUrls(urls.filter((_, j) => j !== i))
  const updateUrl = (i: number, val: string) => {
    const next = [...urls]; next[i] = val; setUrls(next)
  }

  const validUrls = urls.filter(u => u.trim())

  const analyze = async () => {
    if (!validUrls.length || !apiKey.trim()) return
    setLoading(true)
    setGlobalDone(false)
    setResults({})
    setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth' }), 300)

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          urls: validUrls,
          yourUrl: yourUrl.trim(),
          slackWebhook: slackWebhook.trim(),
          apiKey: apiKey.trim(),
        }),
      })

      if (!res.ok) throw new Error(await res.text())

      const reader = res.body!.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          try { handleEvent(JSON.parse(line.slice(6)) as StreamEvent) } catch {}
        }
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const handleEvent = (event: StreamEvent) => {
    if (event.type === 'done') { setGlobalDone(true); setLoading(false); return }
    if (event.type === 'status') {
      setResults(prev => ({ ...prev, [event.url]: { text: prev[event.url]?.text ?? '', status: event.message, done: false } }))
    } else if (event.type === 'text') {
      setResults(prev => ({ ...prev, [event.url]: { ...prev[event.url], text: (prev[event.url]?.text ?? '') + event.chunk, status: 'Analyzing...', done: false } }))
    } else if (event.type === 'slack') {
      setResults(prev => ({ ...prev, [event.url]: { ...prev[event.url], slackSent: event.sent } }))
    } else if (event.type === 'complete') {
      setResults(prev => ({ ...prev, [event.url]: { ...prev[event.url], status: 'Complete', done: true } }))
    } else if (event.type === 'error') {
      setResults(prev => ({ ...prev, [event.url]: { text: '', status: 'Error', done: true, error: event.message } }))
    }
  }

  const hostname = (url: string) => { try { return new URL(url).hostname.replace('www.', '') } catch { return url } }

  return (
    <div className="min-h-screen bg-[#080808]">
      {/* Header */}
      <header className="border-b border-white/5 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm">A</div>
          <span className="text-white font-semibold text-sm">Ad Intel</span>
          <span className="text-white/20 mx-1">—</span>
          <span className="text-white/40 text-sm">Powered by Claude</span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-12">
        {/* Hero */}
        <div className="mb-10">
          <h1 className="text-4xl font-bold text-white mb-3 tracking-tight">Competitor Ad Intelligence</h1>
          <p className="text-white/50 text-lg max-w-xl">
            Every script your competitor is running. Every hook. Every gap. Compared against your own ads. Straight to Slack.
          </p>
        </div>

        {/* Form */}
        <div className="bg-white/[0.03] border border-white/[0.08] rounded-2xl p-8 mb-8">

          {/* YOUR website */}
          <div className="mb-7">
            <label className="block text-sm font-medium text-white/70 mb-1.5">
              Your website URL
              <span className="text-white/30 font-normal ml-2">optional — enables gap analysis against your own ads</span>
            </label>
            <input
              type="text"
              value={yourUrl}
              onChange={e => setYourUrl(e.target.value)}
              placeholder="https://scaler.com/school-of-business"
              className="w-full bg-white/[0.05] border border-indigo-500/30 rounded-xl px-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-indigo-500/60 transition-all text-sm"
            />
            <p className="text-xs text-white/25 mt-1.5">Claude will scrape your site + your own ads and add a "what they do that you don't" section</p>
          </div>

          <div className="border-t border-white/5 mb-7" />

          {/* Competitor URLs */}
          <div className="mb-7">
            <label className="block text-sm font-medium text-white/70 mb-3">
              Competitor URLs
              <span className="text-white/30 font-normal ml-2">up to 5</span>
            </label>
            <div className="space-y-2.5">
              {urls.map((url, i) => (
                <div key={i} className="flex gap-2 items-center">
                  <input
                    type="text"
                    value={url}
                    onChange={e => updateUrl(i, e.target.value)}
                    onKeyDown={e => { if (e.key === 'Enter' && i === urls.length - 1) addUrl() }}
                    placeholder={i === 0 ? 'https://mesaschool.co' : 'https://competitor.com'}
                    className="flex-1 bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-indigo-500/60 transition-all text-sm"
                  />
                  {urls.length > 1 && (
                    <button onClick={() => removeUrl(i)} className="w-9 h-9 flex items-center justify-center text-white/20 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-all">×</button>
                  )}
                </div>
              ))}
            </div>
            {urls.length < 5 && (
              <button onClick={addUrl} className="mt-3 text-xs text-indigo-400/70 hover:text-indigo-400 flex items-center gap-1.5 transition-colors">
                <span className="text-base leading-none">+</span> Add another competitor
              </button>
            )}
          </div>

          <div className="border-t border-white/5 mb-7" />

          {/* Slack + API Key */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-7">
            <div>
              <label className="block text-sm font-medium text-white/70 mb-2">
                Slack Webhook URL <span className="text-white/30 font-normal ml-1">optional</span>
              </label>
              <input type="text" value={slackWebhook} onChange={e => setSlackWebhook(e.target.value)}
                placeholder="https://hooks.slack.com/services/..."
                className="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-indigo-500/60 transition-all text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-white/70 mb-2">
                Claude API Key <span className="text-red-400/60 ml-1">*</span>
              </label>
              <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)}
                placeholder="sk-ant-api03-..."
                className="w-full bg-white/[0.05] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-indigo-500/60 transition-all text-sm" />
              <p className="text-xs text-white/25 mt-1.5">Used per-request. Never stored.</p>
            </div>
          </div>

          {/* CTA */}
          <button onClick={analyze} disabled={loading || !validUrls.length || !apiKey.trim()}
            className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl font-semibold text-white transition-all text-sm flex items-center justify-center gap-2">
            {loading ? (
              <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Analyzing competitor ads...</>
            ) : (
              <><svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>Analyze All Ads</>
            )}
          </button>

          <div className="mt-5 flex flex-wrap gap-x-6 gap-y-1.5">
            {['Detects multiple products per competitor', 'Full scripts verbatim', 'Buckets + funnel map', 'Gaps vs your own ads', 'Posts to Slack'].map(s => (
              <span key={s} className="text-xs text-white/25 flex items-center gap-1.5"><span className="text-indigo-500/60">✓</span>{s}</span>
            ))}
          </div>
        </div>

        {/* Results */}
        <div ref={resultsRef}>
          {Object.entries(results).map(([url, result]) => (
            <div key={url} className="bg-white/[0.03] border border-white/[0.08] rounded-2xl mb-6 overflow-hidden">
              <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${result.done && !result.error ? 'bg-green-400' : result.error ? 'bg-red-400' : 'bg-indigo-400 animate-pulse'}`} />
                  <span className="font-medium text-white text-sm">{hostname(url)}</span>
                  <span className="text-white/30 text-xs">{result.status}</span>
                  {result.slackSent && <span className="text-xs bg-green-500/10 text-green-400 border border-green-500/20 px-2 py-0.5 rounded-full">Sent to Slack ✓</span>}
                </div>
                {result.text && (
                  <button onClick={() => navigator.clipboard.writeText(result.text)}
                    className="text-xs text-white/30 hover:text-white/70 transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-white/5">
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                    Copy
                  </button>
                )}
              </div>
              <div className="p-6">
                {result.error
                  ? <div className="text-red-400/80 text-sm bg-red-400/5 border border-red-400/10 rounded-xl p-4">{result.error}</div>
                  : <pre className={`whitespace-pre-wrap text-sm text-white/70 font-mono leading-relaxed ${!result.done && result.text ? 'cursor' : ''}`}>
                      {result.text || <span className="text-white/20 italic">Browsing Facebook Ad Library...</span>}
                    </pre>
                }
              </div>
            </div>
          ))}

          {loading && !Object.keys(results).length && (
            <div className="text-center py-16">
              <div className="w-10 h-10 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mx-auto mb-4" />
              <p className="text-white/30 text-sm">Finding ads on Facebook Ad Library...</p>
            </div>
          )}

          {globalDone && Object.keys(results).length > 0 && (
            <div className="text-center py-4">
              <p className="text-white/20 text-xs">Analysis complete — {Object.keys(results).length} competitor{Object.keys(results).length > 1 ? 's' : ''} analyzed</p>
            </div>
          )}
        </div>
      </main>

      <footer className="border-t border-white/5 mt-12 px-6 py-5">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <p className="text-white/20 text-xs">Your API key is used directly and never stored.</p>
          <p className="text-white/20 text-xs">Built with Claude Opus 4.6</p>
        </div>
      </footer>
    </div>
  )
}
