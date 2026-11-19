---
name: ad-teardown
description: Collect and take apart every live Facebook and Instagram ad of one company from the public Meta Ad Library, and publish the result as one page (every video script, a breakdown of every video and image, patterns, counts). Use when the user asks to audit, tear down, analyse or review a company's ads, asks about a competitor's ads or "competitor ads", mentions the "ad library", or types "/ad-teardown <company>".
---

# Ad teardown

You are running a slow, polite pull of one company's live ads from the public Ad Library, then writing them up.
Everything runs inside this Claude Code session: no API key, no server, nothing to deploy.
The user is usually not a coder. Keep every message to them short and in plain words. No em dashes. British spelling.

The argument is the company name (for example `/ad-teardown Nike`). An optional two-letter country may follow
(default `IN`). If the user pastes an Ad Library link instead, the number after `view_all_page_id=` is the page id and you can skip step 1.

Paths used below:

- `SLUG`: the company name in lower case with hyphens (`nike`, `mesa-school-of-business`).
- `RESEARCH=research/<SLUG>` (in the repo; this is what gets committed).
- `SCRATCH`: a folder OUTSIDE the repo for mp4 files, logs and the built page. Use the session scratchpad directory if you have one, otherwise `/tmp/ad-teardown`. `VIDEOS=$SCRATCH/<SLUG>-videos`, `DOC=$SCRATCH/<SLUG>-doc`.

If `research/<SLUG>/ads.json` already exists, this is a pull that was started earlier. Do not start again: skip to step 3 and carry on (the pull remembers where it stopped).

## Hard rules

- **Go slowly.** Never load the Ad Library in a loop or in parallel. `find-page.mjs` and `estimate.mjs` cost one page view each (two at most); leave at least a minute between them. All other loading is done by `slow-crawl.mjs`, one batch at a time. Never run two crawls at once, for the same or different companies.
- **People.** Never identify anyone from their face. Use a name only when it is spoken, captioned, printed on the creative or written in the ad text.
- **Quotes.** Scripts, captions and ad text are quoted word for word. Do not tidy or invent lines.
- **Measured versus seen.** Cuts, tempo, words per minute and the music-bed guess are measured by software; the track and genre cannot be named. Say this plainly wherever those numbers appear. Everything else is what was seen in the frames.
- **Not public.** Spend, reach and results are not in the Ad Library. Never imply that an ad "works"; say what the company is betting on (copies, reuse, how long it has run).
- **Privacy.** Do not send the user's name, employer or project to any outside service (search queries, fetched URLs, headers). Only the advertiser's own public pages are fetched.
- **Never commit mp4 files.** They stay in `SCRATCH`.
- **Background jobs die after 2 hours.** Never start an unbounded crawl. Always use `MAX_VIEWS=14` and a 2 hour timeout.

## 0. Setup (once per machine or container)

Check first; only install what is missing.

```bash
test -f connector/dist/facebook.js && test -d connector/node_modules/playwright || (cd connector && npm install && npx tsc)
python3 -c "import whisper, librosa, numpy, markdown, PIL" || pip install markdown pillow librosa numpy openai-whisper
which ffmpeg ffprobe || echo "install ffmpeg (apt-get install -y ffmpeg, or brew install ffmpeg)"
```

- Whisper needs PyTorch. `pip install openai-whisper` pulls it in; on a small machine install the CPU build first: `pip install torch --index-url https://download.pytorch.org/whl/cpu`. The first transcript downloads the `base` model (about 140 MB) from `openaipublic.azureedge.net`. If that host is blocked, videos still get frames and metrics but no script; say so in the page.
- Browser: the scripts find Chrome by themselves (`connector/scripts/chrome.mjs`: `CHROME_PATH` if it points at a real file, then a Chromium under `PLAYWRIGHT_BROWSERS_PATH`, then the usual system paths, then Playwright's own). If launching fails with "Executable doesn't exist", run `cd connector && npx playwright install chromium`.
- The crawl needs about 2 GB of free memory (browser, then Whisper, never both at once).

## 1. Find the page

```bash
cd connector && node scripts/find-page.mjs "<company name>" [COUNTRY]
```

Allow 2 minutes (if the first search returns unrelated pages it waits 75 seconds and tries an exact-phrase search). Read `candidates` and `note`:

- One page with `name_match: "exact"` and nothing else plausible: use it and tell the user which page it is.
- More than one plausible page (sub-brands, regional pages, look-alikes): ask the user which one, showing name, likes and the Ad Library link for each. One teardown covers one page.
- Nothing plausible: ask the user to open facebook.com/ads/library, search for the company, click it, and paste the link. Do not keep retrying.

## 2. Estimate, and tell the user before starting

Wait at least a minute after step 1, then:

```bash
cd connector && node scripts/estimate.mjs <page_id> [COUNTRY]
```

Allow 7 minutes (on an empty answer it waits 5 minutes and tries once more). It prints `total`, a `sentence` with the time estimate, and `suggested_extra_words`.
If `total` is null after that, wait 10 minutes and run it once more; if it is still null, start anyway and say the size is unknown (about 2 hours per 100 ads).

**Before starting the pull, send the user one short message that says all of this, in plain words:**

1. Which page you found and how many live ads it has.
2. This is a slow, background pull on purpose: one ordinary page view every 4 to 7 minutes, so it does not hammer the Ad Library (Facebook blocks anything faster).
3. The estimated time for this company (use the `sentence` from estimate.mjs). Rough guide: up to 30 ads about 10 minutes; about 100 ads about 2 hours; about 300 ads 10 to 14 hours.
4. They can close the chat and come back; the work carries on in the background and nothing is lost if it stops, it picks up where it left off.
5. A first version of the document arrives after the first batch (about an hour and a half on a big account) and the same link is updated as more ads come in.
6. On big accounts expect about 80% of the ads, not all of them.
7. Spend and results are not public, so the document shows what the company is running, not what is working.

Then start. Do not wait for a reply unless you asked which page to use.

## 3. Pull in batches

Pick `EXTRA_WORDS` once, before the first batch: 5 to 15 words that appear in this company's own ads (product and programme names, brand name, offer words). Start from `suggested_extra_words` and add product names you saw in step 2. They are only used when the search list is first built, so set them on the first run. (The built-in list is general English plus business-school words; it is harmless for other companies.)

Run each batch with the Bash tool in the background (`run_in_background: true`, `timeout: 7200000`):

```bash
cd connector && MAX_VIEWS=14 COUNTRY=<CC> EXTRA_WORDS="<a,b,c>" node scripts/slow-crawl.mjs <page_id> ../research/<SLUG> <VIDEOS> 4 7 >> <SCRATCH>/<SLUG>-crawl.log 2>&1
```

- A batch is 14 page views, about 75 to 100 minutes including video downloads and transcripts. Do not poll it; you are told when it exits.
- When it exits, read the last line of the log: `PAUSED: N unique ads of ~T` or `DONE: N unique ads of ~T`. Note N.
- **Stop pulling** when the line says `DONE`, or when two batches in a row each added fewer than 3 new ads. Otherwise start the next batch straight away (same command), and do step 4 for the batch that just finished while the next one runs.
- If the log says "three empty views in a row", Facebook is refusing for now. The script pauses itself for 45 minutes; let it. Do not add retries of your own.
- If the session was restarted and the mp4 folder is gone, carry on: videos already transcribed are not downloaded again.

## 4. After every batch: write up, build, publish, save

**a. Prepare.**

```bash
python3 teardown/prepare.py research/<SLUG> <VIDEOS>
```

It adds `metrics.json` to new videos, refreshes each video folder's `ads.json`, and prints what still needs writing: `videos_needing_breakdown`, `images_needing_writeup`, `images_that_are_exact_duplicates`. If a video is in `metrics_failed`, its breakdown should say the pacing and music were not measured.

**b. Write-ups, by sub-agents in parallel** (if you have no sub-agent tool, do them yourself in the same way):

- Videos: about 4 per sub-agent. Prompt: "Read teardown/BREAKDOWN_BRIEF.md and follow it exactly. Research folder: research/<SLUG>. Your videos: <asset ids>."
- Images: about 10 per sub-agent. Prompt: "Read teardown/STATIC_BRIEF.md and follow it exactly. Research folder: research/<SLUG>. Your images: <library ids>."
- Exact duplicates: do not write them again. Once the twin is written, copy `statics/<copy_from>.md` to `statics/<id>.md`, then correct the title line, the Facts (library id, link, start date, copies, landing page, utm values) and the Ad text from that id's own record in `ads.json`, and add the twin under "Same creative as".
- Check that every assigned file now exists (run prepare.py again; the lists should be empty). Re-assign anything missing once.

**c. The hand-written sections** in `research/<SLUG>/doc/`. Write them after the first batch and refresh them after each later batch (update the counts, add what is new; do not rewrite from scratch unless the picture changed). Read `research/mesa/doc/*.md` once for the shape and tone. Use `###` for headings inside a section, short bullets, real counts ("12 of 35 videos"), and quote creatives by a short title. Each file starts with one bold "short version" sentence.

- `summary.md`: the picture in one paragraph, "The ten things to know" (fewer on a small account), and "What is not known" (spend and results are not public; how many of the reported ads were collected; music is measured by software).
- `how-ads-run.md`: how recently the ads started, product lines, audiences and naming read from the utm tags in the links, formats, reuse of the same creative across ads, buttons and landing pages.
- `patterns.md`: read ALL the breakdowns first (use sub-agents to tally if there are many). Creative families, hooks and first 3 seconds, people and clothing, setting and camera, captions and logos, sound and pacing (from the metrics, labelled as measured), script structure, claims and proof, offers and calls to action, the image ads, weak spots.
- `website.md`: once only. Fetch the distinct landing pages the ads point to (strip the utm tags; 10 pages at most), save the text of each to `research/<SLUG>/site/<name>.txt`, and write what each page promises, prices and offers, proof shown, and where the page and the ads disagree.
- `method.md`: source (public Ad Library, country, page name, no login), pace, how videos were processed, the music caveat, the people rule, limits (coverage reached, spend not public, transcripts can mishear names).
- Optional `insights.md` ("What it means for you"): only if the user has said who they are comparing against or what they want to learn. Leave it out otherwise.

A section with no file is simply left out of the page.

**d. Build and publish.**

```bash
python3 teardown/build.py research/<SLUG> <DOC> "<Company name as on the page>"
```

It prints the counts and writes `<DOC>/index.html` (one file, images inside; several MB). Publish that file with the Artifact tool. Always publish the same file path so the link stays the same; the first time, save the link in `research/<SLUG>/doc/artifact-url.txt`, and in a later session pass that link as `url` so the same page is updated. If there is no Artifact tool, tell the user where the file is.

**e. Save.** Commit and push `research/<SLUG>` on the current branch (`git add research/<SLUG>`; check `git status` shows no mp4). One short commit message, for example "Nike teardown: 96 ads".

**f. Tell the user**, in three or four plain lines: the link, how many ads are in so far out of how many, what is new in this version (one or two findings), and whether more is coming or it is finished.

## 5. Finish

When the pull has stopped (step 3), do step 4 one last time, then send a final short message: the link, the final counts (ads collected of ads reported, videos, images), the three most useful findings, and the limits in one line (coverage, spend not public). No file paths, no commands, no jargon.

## Files

- `connector/scripts/find-page.mjs`, `estimate.mjs`, `slow-crawl.mjs`, `video-metrics.py`, `chrome.mjs`: the pull.
- `teardown/prepare.py`, `build.py`, `template.html`, `BREAKDOWN_BRIEF.md`, `STATIC_BRIEF.md`: the write-up and the page.
- `research/mesa/`: a finished example (it has its own older `doc/build.py`; leave that alone).
