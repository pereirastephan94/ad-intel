# Handover: Scaler School of Business vs Mesa (pair 6)

Owner's ask, in his words: "tell me from it what the insights are based on Scaler School of Business's documentation ... improve this iterative process by even finding insights that mesa does that we don't do." Then write scripts and copies for SSB's performance videos (he will send a brief), and hand the result to "SSB PG COS2" (session_018VFYVEmYkdddabaNRcR1Qg) with very deep, clear insights.
SSB is the owner's own school. Read as SSB first; the Mesa reader view is secondary.

## Status at handover (20 Nov, about 05:15 UTC)
- **SSB**: 30 of its 36 live ads pulled (all video, 16 distinct videos, started 6 to 19 Nov, one landing page scaler.com/school-of-business/minimal-landing/).
  Metrics and Roman-script transcripts are done. Two Sonnet write-up agents were started from the original session at 05:00 on the 16 videos;
  their breakdown.md + tags.json files will be committed to the branch by the original session when they finish (check `ls research/scaler-school-of-business/videos/*/tags.json | wc -l` = 16).
  If any are missing an hour from now, write them yourself with a Sonnet agent (prompt pattern in LEAD_BRIEF.md; ask for: how each speaker is labelled, first 3 seconds, text by 0.5 s, every number and its source, when the school is named aloud, spoken call to action, end card).
  The last 6 SSB ads: one more full page view of page 278591052007519 would get them; add "Scaler School of Business" back to the end of your rr-pull list.
- **Mesa**: 249 ads (126 video ads over 44 videos, 115 image ads tagged; 2 ids without records). All 44 videos have breakdown.md + tags.json; 115 image ads have .tags.json.
  research/mesa/concepts.md lists 30 video ideas (MS-c01..c30) and 33 image ideas (MS-s01..s33), series, and numbers that disagree.
  Mesa has NO extras.json yet: write it (shape of research/cult-fit/extras.json) from concepts.md.
- **Still to do**: SSB idea pass (concepts.md + extras.json, Sonnet), then ONE Opus agent builds the page by teardown/COMPARE_RUNBOOK.md, then publish, then send to SSB PG COS2.

## What is different about this pair
- **Like for like by programme, not product.** Mesa: PGP (full-time), Ascend (part-time, 25 to 38, "keep your job"), Undergraduate. SSB: read scaler.com/school-of-business (allowed host www.scaler.com) for its programmes and claims, and record research/scaler-school-of-business/site.md.
  Mesa's site text is already in research/mesa/site/*.txt. Compare SSB's flagship against Mesa PGP first; give Mesa's Ascend and Undergraduate their own short view ("what else Mesa advertises").
- **Sample sizes differ a lot** (SSB 30 to 36, nearly all its live ads; Mesa 249 of about 310). Say so; use shares, not raw counts; Mesa's sample was pulled in many views, not one ranked view.
- **SSB's own script rules** (from the owner's skill "ssb-creator-scripts"; use them to judge SSB's ads and to write the scripts): a 7-beat structure of about 250 words; one number every 25 to 31 words; named companies (for example Practo, Mokobara); operators as faculty; "1,200+ hiring partners"; "10 years in education"; a call to action with scarcity (seats), a deadline and "scholarships up to 100%"; never "MBAs are broken" with MBA aspirants (it backfires); short dashes; British English. Do not invent SSB facts: anything not in SSB's ads or site goes in [brackets].
- **Already written about Mesa** (reuse, check against the new tags): research/mesa/doc/patterns.md (8,000 words: hooks, first 3 seconds, people and clothing, framing, captions, sound and pacing, structure, claims, offers, weak spots), research/mesa/doc/ssb-insights.md, research/mesa/HANDOVER_SSB.md, research/mesa/doc/summary.md.
  Key Mesa facts: text on screen by 0.5 s in 30 of 35 videos; median 60.8 s, 171 words a minute; polo shirts in 23 of 35; 20 of 35 never look at the lens; 22 of 35 have no spoken call to action; Mesa named aloud late or never in many; speakers named on screen in 2 of 35; numbers unsourced and conflicting (startups 100/150/500; a student brand at 20 vs 25 lakh a month); workhorses: "average of the 5 people around you" (Undergraduate, 10 ads), "We are looking for 200 special people" (9), the investor "sell 5 lakhs in 8 weeks" cold open (8); image ads: "You Don't Have to Quit Your Job to Learn to Build" (15 ads, Ascend), 92 of 115 image ads sell Ascend, none leads with an offer.
- **The page must answer for SSB**: what Mesa does that SSB does not (formats, hooks, proof, workhorses, the Ascend part-time push, image ads: SSB's sample has none), what SSB does that Mesa does not, a Focus / Start / Stop plan, and 5 or 6 script directions for SSB's performance content team, each with ONE full script that follows SSB's rules above.

## Files
- Pair folder to create: research/compare/scaler-school-of-business-vs-mesa/ (products.json with a programme key per ad, series.json, perspectives.json with a generator script, sample_rule.txt).
- Output page: <your scratchpad>/pages/scaler-school-of-business-vs-mesa/index.html. Publish with the Artifact tool, icon "chart". Add the link to LEAD_BRIEF.md.
- Mesa stills, transcripts and metrics are all in the repo; no mp4s are needed for the comparison.
