# Rubric: is this comparison good enough to show a founder?

Version 2 (19 Nov 2026). 15 lines, each scored 0, 1 or 2 (maximum 30).
Ship at 26 or more, with no zero, and every GATE line at 2.
This file is meant to grow: when a review finds a miss the rubric did not catch, add a line or sharpen one, and log it below.

| # | Test | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | GATE First screen | Verdict or moves need scrolling on a 390 x 700 screen | Verdict visible, but moves or the toggle need a scroll | Header with sample and date, toggle, verdict and 2 to 4 ranked moves all visible; the map starts on screen |
| 2 | Verdict sentence | Missing, vague, or describes each brand separately | Has a gap or an edge but not both, or lacks numbers, or runs over 30 words | 30 words or fewer, one gap and one edge named by map row, at least two "n of N" figures |
| 3 | GATE Evidence | Claims with no count or no link to the ads | Counts present, but some lack a denominator or a tap-through | Every claim has n of N with its denominator, and one tap reaches the ads behind it |
| 4 | GATE Honest limits | Reads as if it knows what works, or a banned performance word appears | Limits stated only in the method section | Sample rule, snapshot date and "no spend or results are public" on the first screen; zero banned performance words; the founder rule appears wherever founders are mentioned |
| 5 | Gap map | No per-row comparison | Map present, but rows or status do not follow the stated rules, or one medium is missing | All 7 rows, both media, status and evidence follow the stated thresholds, denominators given per medium |
| 6 | Moves | Observations only | Moves present but missing a first test, effort or evidence label | Each move follows the wording rule: verb, row, rival n of N and idea count, one concrete first test, effort, evidence |
| 7 | Confidence | No strength labels | Labels present but not computed by rule, or a thin row drives move 1 | Every row and move labelled by rule; no thin row is move 1 |
| 8 | Not generic | The verdict or a move survives the swap test | One move survives the swap test | The verdict and every move are false for any other pair of brands |
| 9 | Fair both ways | Only what the reader lacks | Edge mentioned, but with weaker evidence than the gaps | Edge in the verdict, at least one move builds on it, table stakes shown, and the toggle gives the other brand a distinct and correct verdict |
| 10 | Now vs always | No time view | Launch dates shown but not read | Ads launched in the last 30 days that made the sample are listed by row and read in one line per brand |
| 11 | Visual proof on a phone | Text only, or horizontal scroll at 390 px | Stills present but unpaired, or a chart unreadable at 390 px | Paired stills per row, every row legible at 390 px, page self-contained (no external calls after open except the font stylesheet) |
| 12 | Craft depth | Summaries of ads only | Scripts present, but standouts chosen without a stated rule | Exact opening lines and scripts for every ad; frame by frame for 2 standouts per brand chosen by the stated rule |
| 13 | Accuracy | Errors found in the spot check | Tag agreement not reported, or one minor error found | Tag agreement reported; 3 random claims, quotes and counts all check out; row counts add up to the medium totals |
| 14 | India read | No mention of language, timing or destination | One of the three covered | Language mix, festive or sale timing of launches, and destination type (app, web, WhatsApp, lead form) each read in one line where they differ |
| 15 | Leader language | Visible jargon a founder would not use (for example DCO, UTM, tercile, concept_id, WPM) | One or two jargon terms visible | No jargon in visible text: say "versions" not DCO, "idea" not concept, "campaign tag" not UTM, "words a minute" not WPM |

Banned performance words (line 4): works, winning, winner, best-performing, top-performing, converts, effective, successful, profitable, ROI, ROAS, scaling. "Top" is allowed only as "top by Library impressions" or "top 30".

## Review procedure (10 minutes)

1. Minutes 0 to 1: open the page at 390 px width. Read only the first screen. Write down the verdict and move 1 in your own words. Score lines 1 and 2.
2. Minutes 1 to 3: run the swap test on the verdict and each move. Search the page for the banned performance words and the jargon list. Score lines 4, 6, 7, 8 and 15.
3. Minutes 3 to 6: pick 3 claims at random (one from the verdict, one move, one map row). Tap through, check n of N, check the ads match their row, check one quoted line against the transcript, check row counts add up. Score lines 3, 5 and 13.
4. Minutes 6 to 8: flip the toggle. Check the other brand's verdict and moves are distinct and correct; check the edge and table stakes. Read Now vs always and the India lines. Score lines 9, 10 and 14.
5. Minutes 8 to 10: open two row folds and one standout. Confirm the selection rule is stated. Check for horizontal scroll and that the page works offline once loaded. Score lines 11 and 12. Total, and log any miss the rubric did not catch.

## Change log
- v1 (19 Nov 2026): first version, written before any comparison was built.
- v2 (19 Nov 2026): gates added (lines 1, 3, 4); every 1 defined; swap test, banned performance words, confidence labels, now vs always, table stakes, India read, standout selection rule and accuracy added; v1 "lanes" replaced by the 7-row map; line 15 "Leader language" added. Maximum 30, ship at 26.
- To do after the first real comparison: re-check line 14 (is the India read useful or padding?) and the row thresholds in COMPARE_SPEC.md (present at 3 ads, lead at 2x, strong at 8 ads and 3 ideas, thin under 4 ads or 1 idea) against real cell sizes.
