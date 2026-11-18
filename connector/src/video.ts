// Download an ad video, take stills, transcribe it. Files live in a temp folder that is
// deleted after each call; nothing is stored.

import { execFile } from 'node:child_process'
import { promisify } from 'node:util'
import { mkdtemp, readFile, rm, writeFile, stat } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const run = promisify(execFile)
const HERE = path.dirname(fileURLToPath(import.meta.url))
const TRANSCRIBE = process.env.TRANSCRIBE_SCRIPT || path.resolve(HERE, '..', 'transcribe.py')
const PYTHON = process.env.PYTHON || 'python3'
const MAX_BYTES = 200 * 1024 * 1024

const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

/** video-ord5-1.xx.fbcdn.net -> video.xx.fbcdn.net (regional hosts are sometimes refused). */
export function genericHost(u: string): string {
  try {
    const url = new URL(u)
    if (/^video-[a-z0-9-]+\.xx\.fbcdn\.net$/.test(url.hostname)) {
      url.hostname = 'video.xx.fbcdn.net'
      return url.toString()
    }
  } catch {
    /* ignore */
  }
  return u
}

async function download(u: string, file: string): Promise<string> {
  const tries = [u, genericHost(u)].filter((x, i, a) => a.indexOf(x) === i)
  let lastErr = ''
  for (const t of tries) {
    try {
      const r = await fetch(t, { headers: { 'User-Agent': UA, Referer: 'https://www.facebook.com/' } })
      if (!r.ok) {
        lastErr = `${new URL(t).hostname} answered ${r.status}`
        continue
      }
      const buf = Buffer.from(await r.arrayBuffer())
      if (buf.length > MAX_BYTES) throw new Error('video is larger than 200 MB')
      await writeFile(file, buf)
      return new URL(t).hostname
    } catch (e: any) {
      lastErr = `${(() => { try { return new URL(t).hostname } catch { return t } })()}: ${e.message}`
    }
  }
  throw new Error(`Could not download the video (${lastErr}). Facebook video links expire after a few hours; call list_ads again for a fresh link.`)
}

async function duration(file: string): Promise<number> {
  const { stdout } = await run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file])
  return parseFloat(stdout.trim()) || 0
}

async function sceneChanges(file: string): Promise<number[]> {
  // showinfo prints pts_time for each frame the scene filter keeps.
  const { stderr } = await run(
    'ffmpeg',
    ['-hide_banner', '-i', file, '-an', '-vf', "select='gt(scene,0.3)',showinfo", '-f', 'null', '-'],
    { maxBuffer: 50 * 1024 * 1024 },
  )
  const times: number[] = []
  for (const m of stderr.matchAll(/pts_time:([0-9.]+)/g)) times.push(parseFloat(m[1]))
  return times
}

function pickTimes(dur: number, scenes: number[], cap = 12): { t: number; why: string }[] {
  const fixed = [0, 0.5, 1, 2, 3].filter((t) => t < dur).map((t) => ({ t, why: 'opening' }))
  const out = [...fixed]
  const endT = Math.max(0, dur - 0.3)
  const later = scenes.filter((t) => t > 3.2 && t < endT - 0.5)
  const room = cap - out.length - (dur > 4 ? 1 : 0)
  // Spread the scene changes evenly if there are too many.
  const chosen =
    later.length <= room ? later : Array.from({ length: room }, (_, i) => later[Math.floor((i * later.length) / room)])
  for (const t of chosen) out.push({ t, why: 'scene change' })
  if (dur > 4) out.push({ t: endT, why: 'last frame' })
  return out.slice(0, cap)
}

async function still(file: string, t: number, out: string) {
  await run('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-ss', t.toFixed(2), '-i', file, '-frames:v', '1',
    '-vf', 'scale=480:-2', '-q:v', '5', '-y', out])
}

export interface VideoResult {
  duration_s: number
  downloaded_from: string
  stills: { t: number; why: string; jpeg_base64: string }[]
  transcript: { language: string | null; text: string; segments: { start: number; end: number; text: string }[] } | null
  transcript_error?: string
}

export async function analyzeVideo(videoUrl: string): Promise<VideoResult> {
  const dir = await mkdtemp(path.join(tmpdir(), 'adv-'))
  try {
    const mp4 = path.join(dir, 'v.mp4')
    const host = await download(videoUrl, mp4)
    if ((await stat(mp4)).size < 1000) throw new Error('downloaded file is empty')
    const dur = await duration(mp4)
    const scenes = await sceneChanges(mp4).catch(() => [])
    const times = pickTimes(dur, scenes)

    const stills: VideoResult['stills'] = []
    for (const [i, s] of times.entries()) {
      const f = path.join(dir, `s${i}.jpg`)
      try {
        await still(mp4, s.t, f)
        stills.push({ t: Math.round(s.t * 10) / 10, why: s.why, jpeg_base64: (await readFile(f)).toString('base64') })
      } catch {
        /* skip a bad frame */
      }
    }

    let transcript: VideoResult['transcript'] = null
    let transcript_error: string | undefined
    const wav = path.join(dir, 'a.wav')
    try {
      await run('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-i', mp4, '-vn', '-ac', '1', '-ar', '16000', '-y', wav])
      const { stdout } = await run(PYTHON, [TRANSCRIBE, wav], { maxBuffer: 20 * 1024 * 1024, timeout: 10 * 60 * 1000 })
      transcript = JSON.parse(stdout.trim().split('\n').pop() || '{}')
    } catch (e: any) {
      transcript_error = /does not contain any stream|Output file .* does not contain/i.test(String(e.stderr || e.message))
        ? 'This video has no audio track.'
        : `Transcription failed: ${String(e.stderr || e.message).slice(-400)}`
    }
    return { duration_s: Math.round(dur * 10) / 10, downloaded_from: host, stills, transcript, transcript_error }
  } finally {
    await rm(dir, { recursive: true, force: true })
  }
}
