# Night plan (20 Nov 2026, IST): head-to-head ad comparisons

Read this first if you are resuming after a restart, a usage reset (about 03:52 IST) or a context summary.
Owner is asleep. Do not ask questions. Do not create accounts or deploy servers. Never commit mp4 files, secrets or emails.
Branch `claude/yesterday-cpls-TCJO8`. Commit and push often (commit trailer rules are in the session).

## Goal by morning
Five head-to-head comparison pages for founders and growth heads, each a self-contained HTML page published as an Artifact,
plus one short index of links. Order of priority:
1. Fintech: Stable Money vs Wint Wealth (PhonePe dropped by the owner)
2. Health and fitness: Cult.fit vs Fitelo
3. Home and appliances: Atomberg vs Qubo
4. Bags: Mokobara vs DailyObjects
5. Jewellery: GIVA vs CaratLane
Fallback if a brand has under 15 ads or no page is found: fintech Upstox, Dezerv; fitness PlatinumRx; home The Sleep Company; bags none; jewellery Titan/Tanishq.

## Pipeline per brand (all in this repo)
1. Pull (slow, one company at a time, never two pulls at once, Facebook returns empty pages otherwise):
   `connector/scripts/sample-run.sh <scratch>/sample-videos "Brand 1" "Brand 2" "Brand 3"` in the background, at most 3 brands per job
   (background jobs die at 2 h). Log: `<scratch>/sample.log`. Output: `research/<slug>/` (ads.json, videos/<asset>/ with stills and
   transcript.json, images/<library_id>.jpg, page.json). scratch = /tmp/claude-0/-home-user-ad-intel/881fe6a6-b751-599d-a717-87e6df82ea58/scratchpad
   Needs `CHROME_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome`.
   If a view came back with 0 ads, rerun the same brand later (the queue in crawl-state.json keeps what is left; an empty view is
   consumed, so re-add it to the queue by hand). If page.json picked a wrong page (ads not by the brand), delete the folder and find the right page id.
2. Prepare: `python3 teardown/prepare.py research/<slug> <scratch>/sample-videos/<slug>` (metrics.json per video, per-video ads.json, lists what needs a write-up).
3. Write-ups by Sonnet sub-agents (cheap), one agent per brand, capped at the 12 most-used videos and 15 distinct images (md5 duplicates written once):
   - per video `videos/<asset>/breakdown.md` per `teardown/BREAKDOWN_BRIEF.md` and `videos/<asset>/tags.json` per `teardown/TAGGING.md`
   - per image `statics/<library_id>.md` per `teardown/STATIC_BRIEF.md` and `statics/<library_id>.tags.json`
   - tags (not full write-ups) for EVERY sampled creative, since the gap map counts all of them
   Quality checks by the lead session: read the first 5 write-ups in full, then spot-check around the 10th, 15th, 20th and at irregular points.
   Each time, note misses in `teardown/BRIEF_REVIEW_LOG.md` and tighten the briefs.
4. Compare: `teardown/compare/compute.py research/<A> research/<B> out.json`; the lead session (or an Opus sub-agent) writes
   `perspectives.json` (verdict and moves for both brands, wording rules in `teardown/COMPARE_SPEC.md`); `teardown/compare/build.py` builds the page.
5. Review the page against `teardown/RUBRIC.md` (ship at 26 of 30, gates at 2). Fix, then publish with the Artifact tool. Add the link below.

## Status (update as you go)
- Mesa full teardown: paused at 249 of ~310 ads. Page https://claude.ai/artifact/AkQYkZB3ZuVR8hV7rRyrtE . Google Doc sent. Not a priority tonight.
- Pull job 1 done: Stable Money got 30 video ads (25 videos); its "all" and "image" views came back empty. Cult.fit page not found on first try.
- LESSON: about half of all page views come back empty. slow-crawl now retries empty plain views twice; sample-run.sh takes alternate
  spellings ("Cult.fit|cultfit|Cult") and MAX_VIEWS=6.
- Pull job 2 (Stable Money remaining views, Wint Wealth, Cult.fit): started 20:32 UTC 19 Nov.
- Pull job 3 (Fitelo, Atomberg, Qubo): not started.
- Pull job 4 (Mokobara, DailyObjects, GIVA): not started.
- Pull job 5 (CaratLane + any brand that failed): not started.
- Write-ups: Sonnet pilot on 5 Stable Money videos running; review them (log in teardown/BRIEF_REVIEW_LOG.md) before releasing the other 20.
- Opus agent finished: RUBRIC v2, TAGGING.md, COMPARE_SPEC.md, compare/compute.py, compare/build.py all written and tested on dummy brands (28 of 30).
- Comparison pages published: none yet.

## Published links
(none yet)
