// Picks a Chrome/Chromium for Playwright. Import this before calling anything in ../dist/facebook.js.
// facebook.js launches with executablePath = process.env.CHROME_PATH, or Playwright's own download if that is unset.
// Here: keep CHROME_PATH if it points at a real file; otherwise look in the usual places; otherwise leave it unset
// so Playwright uses its own browser (installed with `npx playwright install chromium`).
import fs from 'node:fs'
import path from 'node:path'

function candidates() {
  const c = []
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH
  if (root && fs.existsSync(root)) {
    c.push(path.join(root, 'chromium'))
    for (const d of fs.readdirSync(root).filter((n) => /^chromium-\d+$/.test(n)).sort().reverse())
      for (const sub of ['chrome-linux64/chrome', 'chrome-linux/chrome', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium'])
        c.push(path.join(root, d, sub))
  }
  c.push('/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
  return c
}

export function pickChrome() {
  const set = process.env.CHROME_PATH
  if (set && fs.existsSync(set)) return set
  delete process.env.CHROME_PATH
  // Playwright's own matching download wins if it is there.
  try {
    const own = path.join(process.env.PLAYWRIGHT_BROWSERS_PATH || path.join(process.env.HOME || '', '.cache', 'ms-playwright'))
    const want = JSON.parse(fs.readFileSync(new URL('../node_modules/playwright-core/browsers.json', import.meta.url), 'utf8'))
      .browsers.find((b) => b.name === 'chromium').revision
    if (fs.existsSync(path.join(own, `chromium-${want}`))) return null
  } catch { /* fall through to the list */ }
  for (const p of candidates()) if (fs.existsSync(p)) { process.env.CHROME_PATH = p; return p }
  return null
}
pickChrome()
