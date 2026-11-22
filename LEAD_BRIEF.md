# Lead brief: ad teardown and head-to-head comparisons

Read this first, whatever model you are. It replaces NIGHT_PLAN.md as the working instructions (NIGHT_PLAN.md is the history).
You are the lead session. Your job is to keep the pipeline moving and report to the owner in short, plain messages. You do not do the heavy work yourself.

## COS status (updated 22 Nov 23:05 UTC, Monday 04:35 IST)
- Resumed after the owner's pause. Running: rr-pull.sh (10 brands + "Scaler School of Business" last), scratch = /tmp/claude-0/-home-user-ad-intel/a4bcc5c6-4d1a-5676-b1b0-2dff902eac6b/scratchpad, log sample.log.
- Running: Qubo prepare + retranscribe (10 new videos); Sonnet agents on SSB idea pass and Mesa extras.json.
- Next: one Opus agent builds SSB vs Mesa (owner's priority), then Qubo write-ups and Atomberg vs Qubo.
- Done: Atomberg idea pass; SSB write-ups (16 videos).
- Blocked: send_message to the original session (trusted device) and to SSB PG COS2 (denied).
- Published by COS: none yet. Mesa teardown: https://claude.ai/artifact/AkQYkZB3ZuVR8hV7rRyrtE . Prompt doc for others: Google Doc "Competitor ad teardown: prompt for Claude".

## Who does what (model policy, set by the owner on 20 Nov)
| Work | Who | Notes |
|---|---|---|
| Keeping jobs running, restarts, commits, short status messages | Lead (any model, Sonnet is enough) | No analysis in the lead's own context |
| Video and image write-ups, tags | Sonnet sub-agents (`model: "sonnet"`) | 9 to 11 videos per agent, images with the last agent |
| Idea pass per brand (concept_id, concepts.md, extras.json) | Sonnet sub-agent | One per brand, after its write-ups |
| Copying twins, counting, file shuffling | Haiku sub-agent (`model: "haiku"`) or a script | Never a bigger model |
| Comparison page: plan, scripts to brief, verification, rubric score | ONE Opus sub-agent per pair (`model: "opus"`) | Follows teardown/COMPARE_RUNBOOK.md. This is the only place a top model is used |
| Fable | Not used, unless the owner asks for it on a page | |
Never read sub-agent transcripts or `list_events` of other sessions: they flood the context. Read only the final report.

## Handover, 20 Nov 04:40 UTC: two sessions now
- **Ad Teardown COS** (a new Opus cloud session) owns EVERYTHING except SSB vs Mesa: the puller, all write-ups, idea passes, and comparison pages 3, 4, 5, plus refreshing pages 1 and 2 on bigger samples.
- **UPDATE 05:15 UTC: pair 6 (SSB vs Mesa) now also belongs to the COS; read HANDOVER_SSB_VS_MESA.md.** The original session (session_018VFYVEVx8x8JEXiUxuVpJD) only commits the SSB write-ups still running there, then stops. Old note: it did pair 6, and touches only research/scaler-school-of-business, research/mesa, research/compare/scaler-school-of-business-vs-mesa. It does NOT pull any more.
- Only the COS runs the puller. Its machine has no mp4s from before: brands already pulled have their stills, transcripts and metrics in the repo, which is all the write-ups need.
- Both sessions push to branch claude/yesterday-cpls-TCJO8: always `git pull --rebase origin claude/yesterday-cpls-TCJO8` before `git push`. If a shared tool file (teardown/compare/*.py, template.html, COMPARE_SPEC.md, RUBRIC.md, TAGGING.md) must change, make the change small and say so in the commit message.
- The COS talks to the other sessions with send_message: to the original session for anything about the tools or SSB/Mesa, and to "SSB PG COS2" (session_018VFYVEmYkdddabaNRcR1Qg) with a short note each time a page is published or republished (link + three lines).
- State at handover: Atomberg 30 ads, all 27 videos and 1 image written up, needs idea pass. Qubo 30 ads (13 videos, 12 images) pulled 04:35, being measured and transcribed by the original session and pushed shortly; then needs write-ups. Cult.fit has 30 new ads (8 new videos) being transcribed the same way; then write-ups, idea pass refresh and a rebuild of page 2. Mokobara, DailyObjects, GIVA, CaratLane: no ads yet.

## Owner rules
- He is not a coder. Messages: short, plain, no jargon, lead with what is done and what is not.
- Do not ask questions; decide and carry on. If an approval prompt gets no answer, work around it.
- Pulling never stops. Analysis can lag; the puller must not.
- Never commit mp4 files, secrets or emails. No pull requests. Branch `claude/yesterday-cpls-TCJO8`. Commit and push often (a hook demands it):
  `git add -A . ':!*.mp4' && git commit -m "..." && git push -u origin claude/yesterday-cpls-TCJO8` with the session's commit trailers.
- Never identify a person from a face. No em dashes. British spelling. No words like "works", "winning", "effective" about ads (spend and results are not public).

## The pairs
1. Stable Money vs Wint Wealth: PUBLISHED https://claude.ai/artifact/MsxdvaRyVXemXciA35N7KJ
2. Cult.fit vs Fitelo: PUBLISHED https://claude.ai/artifact/5sZG7mWZYjdFsbQarkXo5V
3. Atomberg vs Qubo: Atomberg pulled (30 ads) and being written up; Qubo has no ads yet.
4. Mokobara vs DailyObjects: nothing pulled yet (DailyObjects page found by search only on 20 Nov 01:01).
5. GIVA vs CaratLane: nothing pulled yet.
6. Scaler School of Business (the owner's own school) vs Mesa: SSB 30 of 36 ads pulled 04:26 UTC; Mesa has 249 ads, video tags done, image tags in progress. The owner wants "what Mesa does that we do not".
Mesa's own full teardown: https://claude.ai/artifact/AkQYkZB3ZuVR8hV7rRyrtE . Google Doc sent earlier.

## Pipeline per brand
scratch = /tmp/claude-0/-home-user-ad-intel/881fe6a6-b751-599d-a717-87e6df82ea58/scratchpad
1. **Pull** (one job for all brands, never two pullers at once):
   `cd connector && CHROME_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome bash scripts/rr-pull.sh <scratch>/sample-videos "Scaler School of Business" "Qubo" "Mokobara" "DailyObjects|Daily Objects" "GIVA" "CaratLane" "Atomberg" "Fitelo" "Stable Money" "Wint Wealth" "Cult.fit" >> <scratch>/sample.log 2>&1`
   in the background with a 2 hour timeout. It ends by itself after 105 minutes ("RR END"): START IT AGAIN AT ONCE. After a machine restart, start it again too.
   The Ad Library gives one or two full pages (30 ads each), then empty pages until left alone about 20 minutes; the script already rests after an empty page.
   Page ids are in research/<slug>/page.json. Data lands in research/<slug>/ (ads.json, videos/<asset>/, images/). Put brands with the fewest ads first in the list.
2. **Prepare**, when a brand has new videos (needs the mp4s in scratch):
   `python3 -W ignore teardown/prepare.py research/<slug> <scratch>/sample-videos/<slug>` then
   `python3 -W ignore teardown/retranscribe.py research/<slug> <scratch>/sample-videos/<slug> "<brand and product words>"` (Hindi speech into Roman script). Wait for it to finish before step 3.
3. **Write-ups**: Sonnet agents, prompt pattern = the Atomberg agents (see "Prompt patterns" below). Each writes breakdown.md + tags.json per video, statics/<id>.md + .tags.json per image.
4. **Idea pass**: one Sonnet agent writes concept_id into every tags file, research/<slug>/concepts.md and research/<slug>/extras.json (pattern: the Fitelo concept pass).
5. **Comparison**: one Opus agent, told to follow teardown/COMPARE_RUNBOOK.md and teardown/COMPARE_SPEC.md and to pass teardown/RUBRIC.md (v4: 40 of 48, Useful lines 18 of 20, gates at 2).
   It must: check each brand's own website (allowed hosts: the brands' sites; use curl through the proxy), compare like for like by product, show what each brand leans on,
   put a plan on the first screen (Focus, Start, Stop or fix), and give script directions with one full draft script each. Output: <scratch>/pages/<a>-vs-<b>/index.html.
6. **Publish** with the Artifact tool (file path above, icon "chart", one-sentence description). To update a page, publish the same path, or pass its `url`. Add the link to this file.

## Prompt patterns (copy, change brand and ids)
- Write-up agent: "Repo /home/user/ad-intel. Brand: <name> (<what it sells>). Read teardown/BREAKDOWN_BRIEF.md and teardown/TAGGING.md fully INCLUDING every Rulings section. Example: research/stable-money/videos/1113897927910622/. Do these folders under research/<slug>/videos/: <ids>. Look at EVERY still, read transcript.json, metrics.json, ads.json. Write breakdown.md (600 words outside the script table) and tags.json (model sonnet, concept_id null, with product, one_line, script_twin, offer_also). No em dashes, never identify from faces, gloss Hindi, check small print against claims. Do not commit. Reply with one line per video, numbers that disagree across ads, and what was unclear in the briefs."
- Idea pass agent: see the Fitelo one in NIGHT_PLAN.md history; it must write concepts.md and extras.json in the shape of research/cult-fit/extras.json.
- Comparison agent: "Build the head-to-head page for <A> vs <B> by following teardown/COMPARE_RUNBOOK.md exactly. Inputs research/<a>, research/<b>. Output <scratch>/pages/<a>-vs-<b>/index.html. Keep a generator script in research/compare/<a>-vs-<b>/. Verify every figure, lint 0, look at phone and desktop screenshots, score under RUBRIC v4, do not commit. Reply with the plan and script titles for both readers, the score, what the websites showed and what is weak."

## Quality checks the lead still owes
- Read each write-up agent's final report; if it lists unclear points, add a short "Rulings from review N" section to teardown/TAGGING.md or BREAKDOWN_BRIEF.md and log it in teardown/BRIEF_REVIEW_LOG.md (6 reviews so far).
- Before publishing a comparison, look at its first-screen phone screenshot once.

## Things that broke before (do not repeat)
- `sort_data[...]` on Ad Library links returns empty pages: never add it.
- Scheduled wake-ups (send_later) have not fired for this session; rely on job-end notifications.
- A second cloud machine did not get its own allowance from Facebook and pushed nothing; more pull bots do not help.
- A restart kills jobs and agents but keeps files: restart the puller, resume agents with SendMessage ("files survived, carry on").
- Hand-written verdicts had 7 wrong figures in pair 1: every figure in a plan must come from an ad in the row, idea or product it names, and an Opus agent checks them.
