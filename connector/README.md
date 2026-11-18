# Ad Audit connector

A small server that lets **your own Claude chat** audit any company's Facebook and Instagram ads,
videos included. You add it to claude.ai as a custom connector. Claude does the thinking on your
own Claude plan; this server only fetches the public Ad Library and processes the videos.
No API key is needed.

What Claude gets from it:

| Tool | What it does |
|---|---|
| `find_advertiser` | Searches the Ad Library for a name and lists matching Facebook pages, so you can pick the right one |
| `list_ads` | Lists a page's active ads, longest-running first: text, headline, button, landing page, video, copies |
| `analyze_video` | Downloads one video ad and returns up to 12 stills (which Claude can see) and a timestamped transcript |
| `audit` prompt | Tells Claude how to write the audit (hook, presenter, format, beats, claims and proof, offer, CTA, patterns, what to run against them, with a link for every ad) |

Test results are in [TEST_RESULTS.md](TEST_RESULTS.md).

---

## Try it first on your Mac (free, about 15 minutes)

This runs the tool on your own Mac and gives claude.ai a temporary link to it through a free
Cloudflare tunnel (no account needed). It only works while the Terminal window is open.

1. Install Homebrew from brew.sh if you don't have it (copy the one line on that page into Terminal).
2. Download this branch from GitHub (**Code → Download ZIP**) and unzip it.
3. In Terminal, go into the `connector` folder, e.g.
   `cd ~/Downloads/ad-intel-claude-yesterday-cpls-TCJO8/connector`
4. Run: `bash start-mac.sh`
   The first run installs what it needs (about 10 minutes). Later runs take seconds.
5. It prints a **connector link**. In claude.ai go to **Settings → Connectors → Add custom connector**,
   name it `Ad Audit (test)`, paste the link, and click Add.
6. Start a new chat, switch on **Ad Audit (test)** in the tools menu, and type **Audit Mesa's ads**.
7. Press **Ctrl+C** in Terminal to stop it. The link changes each run, so update the connector's URL
   next time.

If you use Claude Code on your Mac, the script also prints a one-line command that adds the tool
there directly, with no tunnel.

Once you're happy with it, put it online permanently (below) so it works without your Mac.

## Which host? Fly.io

The server needs about **2 GB of memory**: the browser uses about 0.4 GB and the speech-to-text
(Whisper) about 1 GB.

| | Render | Fly.io |
|---|---|---|
| Plan with 2 GB | Standard: **$25 a month** | shared-cpu-1x with 2 GB: about **$12–13 a month** if always on |
| Cheaper plans | Free and Starter have only 512 MB, so they **will crash** | — |
| When nobody is using it | Free plan sleeps after 15 minutes; paid plans stay on and you pay the full month | **Stops by itself and wakes on the next request in a few seconds.** You pay only while it runs. |
| Light use (a few audits a week) | $25 | **about $1–3 a month** (running time plus a little storage) |
| Needs a card | Only for paid plans | Yes |

**Use Fly.io.** It is the only one with 2 GB that you don't pay for while it sleeps. The `fly.toml`
file in this folder already sets 2 GB and auto-sleep. Prices are from the providers' pages and
reviews in November 2026; check fly.io/pricing before you sign up.

---

## A. Put it online (about 20 minutes, once)

You type these into the **Terminal** app on your Mac. Copy each line exactly.

1. **Make a Fly.io account** at fly.io and add a card.
2. **Install Fly's tool:**
   `curl -L https://fly.io/install.sh | sh`
   Then close Terminal and open it again.
3. **Log in:** `fly auth login` (a browser window opens; click to confirm).
4. **Get this folder onto your Mac.** On GitHub, open the `ad-intel` repo, switch to the branch
   `claude/yesterday-cpls-TCJO8`, click **Code → Download ZIP**, and unzip it. Then in Terminal:
   `cd ~/Downloads/ad-intel-claude-yesterday-cpls-TCJO8/connector`
   (adjust if your folder has a different name).
5. **Create the app:** `fly launch --no-deploy --copy-config --name ad-audit-stephan`
   If it says the name is taken, add a number, e.g. `ad-audit-stephan-7`. Say **No** to any
   question about databases or Redis.
6. **Make your secret password** (this stops strangers using your server):
   `openssl rand -hex 24`
   Copy the long string it prints. Keep it private, like a password. Then:
   `fly secrets set ACCESS_TOKEN=paste-the-string-here`
7. **Deploy:** `fly deploy`
   The first time takes 5–10 minutes. It ends by showing your address, like
   `https://ad-audit-stephan.fly.dev`.
8. **Check it:** open `https://ad-audit-stephan.fly.dev/health` in your browser. You should see
   `{"ok":true}`.

Your connector link is your address + `/mcp/` + your secret:

`https://ad-audit-stephan.fly.dev/mcp/your-secret-string`

Anyone with this full link can use your server, so don't share it.

## B. Add it to Claude

1. Go to **claude.ai → Settings → Connectors → Add custom connector**.
2. Name: `Ad Audit`. URL: your connector link from step A. Click **Add**.
3. Start a new chat. In the chat's tools menu, make sure **Ad Audit** is switched on.
4. Type: **Audit Mesa's ads**
   Claude will find the page, ask you to confirm it, list the ads, watch the top videos and write
   the audit. To make it specific to you, add: "My business is …, tell me what to run against them."

The first message after a quiet spell can take 10–20 seconds while the server wakes up.

---

## Good to know

- **About 30 ads per company.** Facebook blocks "load more" with "Rate limit exceeded". The tool
  stops and tells Claude. Trying again hours later may get more.
- **Videos take 10–60 seconds each.** Claude is told to do the top 3–5 unless you ask for more.
- **Video links expire after a few hours.** If a video fails, ask Claude to list the ads again.
- **Facebook may block servers.** It worked from a cloud machine in testing, but Facebook could
  start refusing Fly's addresses. If every search comes back empty, that is the likely cause.
- **Legal:** Meta's terms forbid automated collection. Get a lawyer's view before charging anyone.
- **Your method is visible to Claude.** The audit instructions live in `src/prompt.ts` and are sent
  to whoever's Claude uses the connector. Fine for you alone; think about it before sharing the link.
- **Nothing is stored.** Videos are deleted as soon as each one is processed.
- **To stop paying:** `fly apps destroy ad-audit-stephan`

## For a developer

- Node 22, TypeScript, `@modelcontextprotocol/sdk` (Streamable HTTP, stateless), Playwright
  Chromium, ffmpeg, Python `openai-whisper` (CPU).
- Endpoint: `POST /mcp/<ACCESS_TOKEN>`, or `POST /mcp` with `Authorization: Bearer <ACCESS_TOKEN>`.
  `GET /health` is open.
- Settings (environment variables): `ACCESS_TOKEN` (required), `PORT` (8080), `WHISPER_MODEL`
  (`base`, or `tiny` for less memory), `CHROME_PATH` (only if Playwright can't find Chromium),
  `PYTHON`.
- Local run: `npm ci && npm run build && ACCESS_TOKEN=test-token npm start`, then
  `MCP_URL=http://localhost:8080/mcp/test-token OUT=/tmp/out npm test -- 115513081449393 3`.
- Ad data comes from the JSON the Ad Library page loads (embedded `application/json` scripts and
  `/api/graphql/` responses), not from page text.
