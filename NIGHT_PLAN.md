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
- ROOT CAUSE of empty views found 22:25 UTC: the `sort_data[mode]=total_impressions` parameter. Views without any sort come back full.
  sample-run.sh now queues {all},{video},{image} with no sort. Never add the sort back.
- Pull job 2 done: Stable Money 33 ads (25 videos, 3 images), Wint Wealth 30 ads (13 videos, 11 images). Both were pulled WITH the impressions sort (it worked after retries).
- Pull job 3 (Cult.fit page 392046674300717, Fitelo, Atomberg): started 22:27 UTC 19 Nov, default order.
- Pull job 4 (Qubo, Mokobara, DailyObjects): not started.
- Pull job 5 (GIVA, CaratLane): not started.
- Write-ups: Stable Money and Wint Wealth done (breakdown.md, tags.json, concepts.md). Hindi transcripts need `teardown/retranscribe.py` BEFORE write-ups.
  Per brand: 2 Sonnet agents (videos split in two, images with the second), then 1 Sonnet concept pass. Prompts: copy the pattern used for Wint Wealth
  (briefs + all Rulings sections; example folder research/stable-money/videos/1113897927910622).
- Comparison 1 (Stable Money vs Wint Wealth): PUBLISHED v1 https://claude.ai/artifact/MsxdvaRyVXemXciA35N7KJ . Data in research/compare/stable-money-vs-wint-wealth/. Page file: <scratch>/pages/stable-money-vs-wint-wealth/index.html (republish the same path to keep the link). An Opus agent is doing the rubric review and fixes; rebuild and republish when it reports.
- Opus agent finished: RUBRIC v2, TAGGING.md, COMPARE_SPEC.md, compare/compute.py, compare/build.py all written and tested on dummy brands (28 of 30).
- Comparison pages published: none yet.

## Published links
- Stable Money vs Wint Wealth: https://claude.ai/artifact/MsxdvaRyVXemXciA35N7KJ

## Added 23:40 UTC 19 Nov
- LESSON 2: dropping the sort did not cure empties. Real pattern: one good view of a page, then empties for roughly 10 to 15 minutes. So: one view per brand per visit, 9 to 12 minutes between any two views (`sample-run-slow.sh`, MAXV=1 NAPMIN=540).
- Round one: top 30 per brand. Job running: Atomberg, Qubo, Mokobara, DailyObjects. Next job: GIVA, CaratLane.
- Round two (owner asked "more exhaustive than 30"): after round one, top up every brand with {media: video}, {media: image}, then keyword views
  (set research/<slug>/crawl-state.json queue by hand, run sample-run-slow.sh with MAXV=1 per visit, cycling through brands so each brand rests 12+ minutes).
  Target 60 to 90 ads per brand. Then write up the new creatives, rerun concept pass, compute, build, republish at the same link.
- Cult.fit 30 ads and Fitelo 34 ads pulled; metrics and second-pass transcripts running; then write-ups (2 Sonnet agents per brand + concept pass).
- Opus agent reviewing comparison 1 against the rubric; it may add an `extras` block (product mix, contradictions, series) and RUBRIC v3.

## Added 23:45 UTC 19 Nov: PULLING NEVER STOPS (owner's instruction: keep pulling, analysis can wait)
- One job does all pulling now: `connector/scripts/rr-pull.sh <scratch>/sample-videos "Atomberg" "Qubo" "Mokobara" "DailyObjects|Daily Objects" "GIVA" "CaratLane" "Cult.fit" "Fitelo" "Stable Money" "Wint Wealth"`
  with CHROME_PATH set, in the background, 2 h timeout. It rotates through the brands, one page view each, 5 to 7 minutes apart, and ends by itself after 105 minutes ("RR END" in sample.log).
  THE MOMENT IT ENDS, START IT AGAIN with the same command. It keeps its place (research/<slug>/crawl-state.json: stage 1 = all/video/image, stage 2 = more media views, stage 3 = keyword views).
- Do not run sample-run.sh or sample-run-slow.sh any more, and never two pullers at once.
- Analysis (write-ups, concept pass, compare, publish) happens alongside and must never pause the puller. Before writing up a brand, run prepare.py and retranscribe.py on it.

## Added 23:55 UTC 19 Nov
- Comparison 1 republished as v2 after the Opus rubric review (22 -> 28 of 30; 7 wrong claims in my hand-written verdicts were fixed). RUBRIC is now v3 (17 lines, ship at 30 of 34).
  LESSON: always have an Opus agent verify every figure in perspectives.json against the tags before publishing, and fill the `extras` block
  (product mix, series, contradictions per brand from concepts.md). Use the prompt pattern of the "Rubric review of comparison 1" agent.
- The Ad Library keyword search also returns empties. Page ids looked up by hand and written to research/<slug>/page.json:
  Atomberg 761127860687721, Qubo 2142425975816266, Mokobara 877758885907009, GIVA 350941852220221, CaratLane 77179773544. DailyObjects still unknown (rr-pull keeps searching).
- Write-ups running: Cult.fit (14 videos, 2 Sonnet agents), Fitelo (21 videos + 4 images, 2 Sonnet agents). Then a concept pass each, then comparison 2.

## Added 00:00 UTC 20 Nov: pull workers on other machines
- Test running: child session session_018VFYVJ74b98dqPoxK7xT9B ("Ad pull worker: Mokobara and GIVA", Sonnet) pulls Mokobara and GIVA and pushes to branch `pull/worker-1`.
  It messages this session with full vs empty view counts. If its views come back full, spawn more workers (create_session, same prompt pattern, 2 to 3 brands each,
  own branch pull/worker-N) and take those brands out of this machine's rr-pull list. To use a worker's data: `git fetch origin pull/worker-1` and
  `git checkout origin/pull/worker-1 -- research/mokobara research/giva` (videos' mp4s stay on the worker; stills and transcripts are in the repo).
  NOTE: retranscribe.py needs the mp4s, so ask the worker to run teardown/retranscribe.py itself before its final push.
- This machine's rr-pull list is now: Atomberg, Qubo, CaratLane, DailyObjects, Cult.fit, Fitelo, Stable Money, Wint Wealth.

## Added 00:20 UTC 20 Nov: owner feedback on comparison 1 (he is awake and reading)
- He found the page not actionable. Required in every comparison from now on: (1) workhorse creatives (one idea can carry a brand: ads, versions, days live),
  (2) like-for-like by product, checked against each brand's own website, with a separate view of other products, (3) a clear action plan (focus / start / stop),
  (4) script directions for his performance content team (persona-led, founder-led, character series...), each with a full draft script.
  The Opus agent (a67a9ab4848dca893) is rebuilding spec, compute, builder, rubric v4 and the Stable Money vs Wint Wealth page on this basis.
- Website hosts for all ten brands plus www.scaler.com are now allowed in the environment (WebFetch works for them).
- He also wants "insights that Mesa does that we (Scaler School of Business) don't do": SSB's own ad page is 278591052007519, page.json written to
  research/scaler-school-of-business/. ADD "Scaler School of Business" to the rr-pull brand list at the next restart, then run SSB through the same write-up
  pipeline and build "SSB vs Mesa" with the new comparison framework (Mesa data: research/mesa, 249 ads; it has breakdowns but NOT tags.json yet: a tagging pass is needed).
- Cult.fit and Fitelo are fully written up with concepts.md and extras.json: comparison 2 waits for the v4 framework.
- Pull worker test (session_018VFYVJ74b98dqPoxK7xT9B): its first two views were empty while this machine's view was full; undecided, check its branch pull/worker-1 later.
