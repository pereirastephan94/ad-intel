# Handoff: Ad Intel, CPL 1 to CPL 2

Written 16 Nov 2026 by CPL 1 (session "Yesterday's CPLs"). Read this file first; do not reread CPL 1's transcript.

Stephan is not a coder. Give him plain, short answers, and keep usage low.

## The goal
1. Analyse competitors' **video ads** from the public Facebook Ad Library: download each video, take stills, transcribe it, and break it down. This was proven on Mesa on 14 Nov.
2. Build a **public website**: a visitor types a company and gets a full audit of its ads, with video.

## Decisions Stephan has made
- **No free audits paid for by him.** Visitors use their own paid AI (Claude, Gemini or ChatGPT), and Stephan pays nothing per audit.
- **He does not want to give away his method** (the prompts and analysis framework). This conflicts with some ways of using the visitor's AI; see open question A.
- **Analysis is built for each visitor's business**, not from SSB's intelligence. SSB is only the test case.
- **Video comes first, Mesa first.** The website comes later.

## What exists
- **This repo.**
  - Next.js app: `app/api/analyze/route.ts` and `scraper.ts`. Text only; it reads `page.innerText` and never touches video.
  - `ad-factory/`: Streamlit app hard-wired to SSB.
- **Cloud environment "ad-intel"** (`env_01TUY3kWy7WcFucege5kvusD`). It allows `www.facebook.com`, `static.xx.fbcdn.net`, `scontent.xx.fbcdn.net`, `video.xx.fbcdn.net`, `huggingface.co` and `openaipublic.azureedge.net`. Use it for any session that touches Facebook; the default environment blocks it.
- **Brief for Stephan's friend:** https://claude.ai/artifact/SoFHUdJxXZKvbzUKGhxTno. It is **wrong and incomplete**: it says video is not handled, covers only this repo, and has a wrong hosting note. Fix it before anyone shares it.
- **On Stephan's Mac** (`/Users/apple/Claude Code /Performance Research/`), not in this repo:
  - `mesa_monitor.py` with a log of 520 Mesa ads since March. It failed silently from 21 Oct to 6 Nov. It contains a hard-coded Slack webhook, which must be removed before the file is shared.
  - `ssb-os/`: Head of Copy principles and the copy rules.
  - 20 Mesa video transcripts made before this work.

## Video proof, 14 Nov: what worked
Session `session_018VFYVFMCK43rsWuhbLWSYv`, run on Fable for about $4.90 of usage.

**Result:** 10 of 10 Mesa videos were downloaded, transcribed and broken down. Facebook was reached logged out, with no login wall.

**Method:**
1. Playwright, logged out, on the page ID 115513081449393, which was confirmed to be Mesa School of Business.
2. Read the JSON responses the page loads, not the page text. These give the Library ID, start date, text, headline, CTA, landing URL, video URL, thumbnail and copy count.
3. Download each video at once, because the links expire. Regional hosts such as `video-ord5-1.xx.fbcdn.net` were refused; the same path and query string on `video.xx.fbcdn.net` worked.
4. ffmpeg stills at 0, 0.5, 1, 2 and 3 seconds plus each scene change, and the audio saved as 16 kHz WAV.
5. Local Whisper from the openai-whisper package. Hugging Face's file hosts were refused.
6. Claude reads the stills and the transcript and fills in the breakdown, using on-screen captions to fix the transcript.

**Findings:**
- **The proof sits inside the videos, not the captions.** Examples: ₹26.5L average CTC shown on screen and never spoken, 100% placements, a 50–60% first-year salary jump, under 5% acceptance, and Zomato, Zepto and Swiggy named.
- **One formula.** Nine of ten open with a presenter on a number or a student story, use word-by-word captions and student clips, and close on a silent end card colour-coded by programme. Several attack "other BBA programs".
- **They are testing presenters and numbers.** The same script appears with "200" and "150 special people", and one student's monthly revenue is given as "20 lakh" in one ad and "25 lakh" in another.

## Not working or not yet proven (exhaustive)
1. **The proof files are probably lost.** `REPORT.md`, `results.json` and `scripts/` were left uncommitted in that session's temporary container. Their contents survive in that session's transcript as Write tool calls: recover them from there, then commit them under `proof/mesa-video/`.
2. **Only 30 of about 240 active Mesa ads were captured.** Every "load more" request returned "Rate limit exceeded". A full pull needs slower paging over time, several sessions, or a paid data service.
3. **Hindi and Hinglish are untested.** All 10 videos were English; English errors were names and slang, fixed from captions.
4. **Static image ads have never been analysed.**
5. **Only Mesa has been tested.** SSB and Masters' Union have not; Masters' Union advertises from three pages, and the fourth competitor is unclear: ATLAS SkillTech or Altera (Digiaccel).
6. **No history.** The Library shows only live ads, and nothing saves daily snapshots, so ads that start and stop between pulls are missed.
7. **No performance data.** The Meta Ads connector is not authorised, so there is no CPL for SSB's own ads.
8. **The business-profile builder** (an automatic profile of the visitor's business from its website and ads) is not built.
9. **The website and the bring-your-own-AI design** are not built.
10. **Legal.** Meta's terms forbid automated collection. A 2024 US ruling (Meta v. Bright Data) favoured logged-out scraping of public data, but Meta may have changed its terms since. Get a lawyer's view before charging.
11. **Unverified figures.** Third-party data-service, transcription and competitor-product prices came from search summaries, not the pages themselves.
12. **The friend's brief is wrong** (see above).
13. **The Mac's `mesa_monitor.py`** has a silent gap from 21 Oct to 6 Nov and needs an alert when it fails.

## Open questions for Stephan
- **A. Bring your own AI without giving away the method.**
  - **Pasted API key:** the method stays on Stephan's server and costs him nothing per audit. But ChatGPT Plus, Claude Pro and Gemini Advanced subscriptions are not API keys, so the visitor needs a developer account.
  - **Connector added to the visitor's own Claude or ChatGPT:** uses their subscription with no key, but their AI must be sent the instructions, so the method is partly exposed.
  - **Claude sign-in on a third-party site:** not allowed by Anthropic without approval.
  - **Possible saving:** with a visitor's Gemini key, video goes straight to Gemini, so transcription runs on their key.
- **B. Server costs.** Hosting, scraping and video storage cost something even if the AI is the visitor's. Who pays?

## Next steps, in order
1. Recover the proof files from the transcript and commit them.
2. Pull all of Mesa's roughly 240 ads, slowly, and report coverage.
3. Run a Hinglish test on 5 videos from an advertiser who uses it.
4. Answer open question A with Stephan, then prototype that one path.
5. Build the business-profile builder; test it on SSB against the hand-built SSB files in `ad-factory/intelligence/`.
6. Fix the friend's brief.

## Usage rules for every session
- **Use Opus 5.5 for routine work.** Fable costs twice as much per token.
- **Start a new session per step.** Write a handoff file before context passes about 40%.
- **Extract only what you need** from other sessions' transcripts; never read them whole.
- **Check background sessions rarely**, for example every 30 minutes, not every 15.
