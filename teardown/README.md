# Ad teardown

Type a company name, get one page that takes apart every live Facebook and Instagram ad it is running:
every video script word for word, a breakdown of every video and every image ad, the patterns across them,
and the counts. It reads the public Meta Ad Library. No login, no API key, no server.

## How to use it

1. Open a Claude Code session on this repo (branch `claude/yesterday-cpls-TCJO8`).
2. Type `/ad-teardown <company>`, for example `/ad-teardown Nike`. Add a country code if it is not India: `/ad-teardown Nike GB`.
3. Claude finds the page (and asks you which one if there are several), tells you how long it will take, and starts.
4. You get a link to the page after the first batch. The same link is updated as more ads come in.

It runs on your normal Claude plan, inside the session.

## It is slow on purpose

Facebook blocks anything that loads the Ad Library quickly. So this loads one ordinary page view every 4 to 7 minutes,
each showing at most 30 ads, and many views repeat ads already seen. You can close the chat and come back.

| Live ads on the page | Time to collect | What you get |
|---|---|---|
| up to 30 | about 10 minutes | all of them |
| about 100 | about 2 hours | most of them |
| about 300 | 10 to 14 hours | roughly 80% of them |

Writing up the creatives adds roughly 1 to 2 minutes per different video and under a minute per image.
These figures come from one measured pull of a 310-ad account: 89 ads after 1.4 hours, 148 after 2.75,
163 after 5.5, 221 after 8.3 and 249 after 10.5.

## Limits

- Spend, reach and results are not public. The page shows what a company is running, not what is working.
- Big accounts: expect about 80% of the ads, not all.
- One Facebook page per teardown. Sub-brands with their own page need their own run.
- Only ads that are live now, in one country.
- Scripts are typed by software and can mishear names and non-English words.
- Music is measured by software (is there a music bed, what tempo). It cannot name a track or genre.
- Nobody is identified from their face. Names appear only when spoken, captioned or printed.
- Videos (mp4) are kept outside the repo and never committed.
- Facebook sometimes answers with an empty page. The tools wait and try once more; they never hammer it.

## What is in here

| File | What it does |
|---|---|
| `../.claude/skills/ad-teardown/SKILL.md` | The steps Claude follows |
| `../connector/scripts/find-page.mjs "<name>" [country]` | Finds the Facebook page |
| `../connector/scripts/estimate.mjs <page_id> [country]` | Counts live ads and estimates the time |
| `../connector/scripts/slow-crawl.mjs <page_id> <research_dir> <video_dir>` | The slow pull (env `MAX_VIEWS`, `COUNTRY`, `EXTRA_WORDS`) |
| `prepare.py <research_dir> <video_dir>` | Measures new videos and lists what still needs a write-up |
| `BREAKDOWN_BRIEF.md`, `STATIC_BRIEF.md` | Instructions for the per-video and per-image write-ups |
| `build.py <research_dir> <out_dir> "<Company name>"` | Builds the page from `template.html` |

Results live in `research/<company>/`. `research/mesa/` is a finished example.

## Setup (once)

```bash
cd connector && npm install && npx tsc
pip install markdown pillow librosa numpy openai-whisper
# plus ffmpeg (apt-get install -y ffmpeg, or brew install ffmpeg)
# and, if no Chrome is found: cd connector && npx playwright install chromium
```
