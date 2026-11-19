# Rubric: is this comparison good enough to show a founder?

Version 3 (19 Nov 2026). 17 lines, each scored 0, 1 or 2 (maximum 34).
Ship at 30 or more, with no zero, and every GATE line at 2.
This file is meant to grow: when a review finds a miss the rubric did not catch, add a line or sharpen one, and log it below.

| # | Test | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | GATE First screen | Verdict or moves need scrolling on a 390 x 700 screen | Verdict visible, but moves or the toggle need a scroll | Header with sample and date, toggle, verdict and 2 to 4 ranked moves (text, Effort, Evidence, "See the ads") all visible; the first test may sit one tap away on a phone; the map (its header or the line above it) starts on screen |
| 2 | Verdict sentence | Missing, vague, or describes each brand separately | Has a gap or an edge but not both, or lacks numbers, or runs over 30 words | 30 words or fewer, one gap and one edge named by map row, at least two "n of N" figures, none of them a share of a small base (line 17) |
| 3 | GATE Evidence | Claims with no count or no link to the ads | Counts present, but some lack a denominator or a tap-through, or a tap lands on a row that does not hold the ads behind the figure | Every claim has n of N with its denominator, and one tap reaches the ads behind it |
| 4 | GATE Honest limits | Reads as if it knows what works, or a banned performance word appears | Limits stated only in the method section, or the method describes a sample rule this run did not follow | Sample rule, snapshot date and "no spend or results are public" on the first screen; any part of the sample rule that failed on the night is stated where it bites (for example on the image rows); zero banned performance words; the founder rule appears wherever founders are mentioned |
| 5 | Gap map | No per-row comparison | Map present, but rows or status do not follow the stated rules, or one medium is missing | All 7 rows, both media, status and evidence follow the stated thresholds, denominators given per medium |
| 6 | Moves | Observations only | Moves present but missing a first test, effort or evidence label | Each move follows the wording rule: verb, row, rival n of N and idea count, one concrete first test, effort, evidence |
| 7 | Confidence | No strength labels | Labels present but not computed by rule, or a thin row drives move 1 | Every row and move labelled by rule; no thin row is move 1 |
| 8 | Not generic | The verdict or a move survives the swap test | One move survives the swap test | The verdict and every move are false for any other pair of brands |
| 9 | Fair both ways | Only what the reader lacks | Edge mentioned, but with weaker evidence than the gaps, or a move praises the rival for something its own ads contradict | Edge in the verdict, at least one move builds on it, table stakes shown, and the toggle gives the other brand a distinct and correct verdict |
| 10 | Now vs always | No time view | Launch dates shown but not read | Ads launched in the last 30 days that made the sample are listed by row and read in one line per brand |
| 11 | Visual proof on a phone | Text only, or horizontal scroll at 390 px | Stills present but unpaired, a chart unreadable at 390 px, or unfinished marks: truncated brand names, "0 ads, 0d" in place of "no ads", bars drawn for zero, a chart with a single bar per brand, an empty block that only says "none" | Paired stills per row, every row legible at 390 px, nothing looks unfinished, page self-contained (no external calls after open except the font stylesheet) |
| 12 | Craft depth | Summaries of ads only | Scripts present, but standouts chosen without a stated rule, a standout's printed reason is false, a standout is a single image, or its frames are near-duplicates | Exact opening lines and scripts for every ad; frame by frame for 2 standouts per brand chosen by the stated rule, with distinct frames and a reason that matches the numbers |
| 13 | Accuracy | Errors found in the spot check | Tag agreement not reported, or one minor error found | Tag agreement reported; 6 claims checked, at least 2 of them figures quoted inside moves, each traced to an ad in the row the move names; row counts add up to the medium totals |
| 14 | India read | No mention of language, timing or destination | One of the three covered, or a festival linked to launch dates without checking the date | Language mix split by medium (video speech is not image text), launch timing with dates checked against the festival calendar, and destination type, each in one line; where a dimension is identical for both brands, one line saying so is enough |
| 15 | Leader language | Visible jargon a founder would not use (for example DCO, UTM, tercile, concept_id, WPM) | One or two jargon terms visible | No jargon in visible text: say "versions" not DCO, "idea" not concept, "campaign tag" not UTM, "words a minute" not WPM, "image ad" not static |
| 16 | What they sell and say | Product mix not shown | Product mix shown only deep in the page, or series and self-contradictions missing | One line on or next to the first screen says what each brand advertises, with ad counts; recurring series are named; up to 5 figures each brand's own ads contradict are listed with links to the ads |
| 17 | Small bases | A share of a medium total under 10 drives the verdict or a move | Small bases shown as shares, or shaded like full bases, but not used for a claim | Under 10 ads of a medium on either side: counts not shares, no shading, a visible note, and no claim rests on the share |

Banned performance words (line 4): works, winning, winner, best-performing, top-performing, converts, effective, successful, profitable, ROI, ROAS, scaling. "Top" is allowed only as "top by Library impressions" or "top 30".

## Review procedure (12 minutes)

1. Minutes 0 to 1: open the page at 390 px width. Read only the first screen. Write down the verdict and move 1 in your own words, and what each brand sells. Score lines 1, 2 and 16.
2. Minutes 1 to 3: run the swap test on the verdict and each move. Search the page for the banned performance words and the jargon list. Score lines 4, 6, 7, 8 and 15.
3. Minutes 3 to 7: check 6 claims (one from each verdict, two figures quoted inside moves, one map row, one contradiction). For each move figure, find the ad that says it and confirm it sits in the row the move names. Check one quoted line against the transcript and that row counts add up. Look at every medium total under 10. Score lines 3, 5, 13 and 17.
4. Minutes 7 to 9: flip the toggle. Check the other brand's verdict and moves are distinct and correct; check the edge and table stakes, and that no move praises the rival for a figure its own ads contradict. Read Now vs always and the India lines; check any festival against its date. Score lines 9, 10 and 14.
5. Minutes 9 to 12: open two row folds, one standout and the dark theme. Confirm the selection rule is stated and the standout's reason matches the map. Look for unfinished marks (line 11). Check for horizontal scroll and that the page works offline once loaded. Score lines 11 and 12. Total, and log any miss the rubric did not catch.

## Change log
- v1 (19 Nov 2026): first version, written before any comparison was built.
- v2 (19 Nov 2026): gates added (lines 1, 3, 4); every 1 defined; swap test, banned performance words, confidence labels, now vs always, table stakes, India read, standout selection rule and accuracy added; v1 "lanes" replaced by the 7-row map; line 15 "Leader language" added. Maximum 30, ship at 26.
- v3 (19 Nov 2026), after the first real comparison (Stable Money vs Wint Wealth). Misses v2 did not catch, and the fix for each:
  - Move figures quoted from ads outside the move's row (11,000 crore from a scene ad cited in a person-to-camera move; "1,000 rupees" from a text-and-motion ad in another), so "See the ads" opened ads that did not hold the figure. Lines 3 and 13 sharpened: trace move figures to an ad in the named row; check 6 claims, not 3.
  - A 3-ad image base drove a verdict, a move and a standout ("you run 1 of 3", "82% against 33%"), and 2 of 3 was shaded as the heaviest cell. New line 17; spec gains the small-base display rule.
  - The method section described the planned sample (video and image each guaranteed a look) when the image view had failed. Line 4 sharpened.
  - A move held up the rival's "one figure, 11%" while the rival's own ads contradict themselves on tenure and minimum. Line 9 sharpened; new line 16 asks for product mix, series and self-contradictions, which the 7-row map cannot show.
  - Unfinished marks passed v2: "Stable Mo..." in the map header, "0 ads, 0d", slivers drawn for zero, a one-bar destination chart, an empty campaign-tag block. Line 11 sharpened.
  - A standout reason claimed the brand "differs most" in a row where it trails (53% against 63%); frame strips showed three identical stills from the first second; one standout was a single image. Line 12 sharpened.
  - Line 1 could not be met at the spec's own word limits (three moves of 35 + 25 words plus a 30-word verdict overflow 390 x 700). Line 1 now allows the first test one tap away on a phone.
  - Line 14 re-checked as the v2 to-do asked: useful, not padding. The timing line carried the sharpest fact about the rival (20 of 30 launched on two days), but it said "around Diwali" for 7 October, a month early, and the language line counted image text with video speech. Sharpened to check festival dates and split language by medium; identical dimensions take one line.
  - Row thresholds re-checked (see COMPARE_SPEC.md, "Status and evidence rules"): kept for video; small bases need their own rule.
  - Procedure lengthened to 12 minutes for the extra checks. Maximum 34, ship at 30.
- To do: put the small-base status and evidence cap into compute.py; run a tag check (n_checked, agreement) for each brand so line 13 can reach 2; prefer two video standouts per brand when the brand has two present video rows.
