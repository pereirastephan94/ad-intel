# Review log: sub-bot write-ups and what changed in the briefs

## Review 1 (20 Nov 2026): Stable Money videos 1 to 5, Sonnet
Read in full: 2933453097006450 (breakdown and tags). Skimmed the bot's report on all five.
- Good: stills read carefully, small print caught (voice sells an RD, end card shows a senior-citizen FD rate; "withdraw any time" against "penalties may apply"), no names guessed from faces, claims listed with proof or "no proof shown".
- Bad: the transcript was unusable. Whisper "base" wrote Hinglish in Urdu script and the bot had to guess a Roman reading. Fixed at the source: `teardown/retranscribe.py` (medium model, Hindi, Roman-script prompt).
- Bad: far too long (about 1,800 words a video, 42k tokens each). Capped at 600 words plus the script table.
- Unclear in the briefs (the bot listed 17 points): how many stills, what V1 means, mixed skit and presenter, hook tiebreak, script for hook_text, a "character" face value, which claim sets the angle, two offers at once, phone on a tripod, square files holding vertical video, placeholder ad text, who speaks which line, same script with a new person. All ruled on in the "Rulings from review 1" sections of both briefs.
- Added to tags: `product`, `one_line`, `script_twin`, `offer_also`, `ad_text_missing`.
Next checks: write-ups 6 to 10 lightly, then around the 10th, 15th, 20th and at irregular points.

## Review 2 (20 Nov 2026): Stable Money videos 6 to 15, Sonnet (spot check at the 10th)
Read: 1113897927910622 header, verdict section and tags; the bot's report on all ten.
- Length cap held. Twins were found without being asked twice (same take in 9:16 and square; same script in landscape).
- New pattern the tags must carry: recurring personas ("Papa Explaining", "Nani Tuitions"). `character` value used correctly.
- Inconsistent: hook for dialogue openers (number_claim vs story_open vs question) and the row for two people talking. Ruled in "Rulings from review 2".
- Some second-pass transcripts are still partly Devanagari; the bot romanised them. Acceptable, marked [?].
