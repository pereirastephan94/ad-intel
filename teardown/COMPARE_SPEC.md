# Head-to-head comparison: page spec

One self-contained HTML page comparing the live Meta ads of two brands in the same category.
Readers are founders, CMOs and growth heads, and the performance content teams they brief. In one minute they must see what to do on Monday: one focus, what to start, what to stop or fix. Then: which ideas each brand leans on, how the two compare on the same product, and script directions the content team can brief from. Depth sits behind folds.

**Version 4 (20 Nov 2026), after the owner's review of Stable Money vs Wint Wealth failed the v3 page.** His points: one creative or series can carry a brand (Papa Explaining), so counting ads per row misleads; compare only the same product, checked against each brand's website, and summarise the rest separately; the page gave no clear action; and it gave the content team nothing to brief from. v4 answers each with a section and a rubric gate (RUBRIC.md v4). The v3 layout (verdict, moves, 7-row map on the first screen) still renders when `--focus-product` and `plan` are absent, for back compatibility.

Related files: `RUBRIC.md` (how a page is scored), `TAGGING.md` (per-ad tags), `compare/compute.py` and `compare/build.py` (the pipeline).

## Pipeline

```
research/<brand>/ads.json + tags + metrics + concepts.md     (per brand, from the teardown pipeline and TAGGING.md)
research/<brand>/site.md                                     (what the brand sells on its own website; written by hand, see below)
  -> compare/products.py A B research/compare/<pair>/products.json [--rules rules.json]
        drafts one product_key per ad from tags.product (edit by hand; add "labels" and "site")
  -> research/compare/<pair>/series.json                    (series and recurring scripts from concepts.md; optional,
        falls back to the "series" list in research/<brand>/extras.json)
  -> compare/compute.py A B research/compare/<pair>/comparison.json \
        --products products.json --focus-product <key|auto> --series series.json [--sample-rule "..."]
        (all counts, the focus-product map, the full-sample map as rows_all, workhorses, standouts)
  -> a person or model writes perspectives.json (verdict, plan, scripts, reads; rules below)
  -> compare/build.py comparison.json perspectives.json A B out_dir   (index.html, with a lint report)
```

For Stable Money vs Wint Wealth:
```
python3 teardown/compare/products.py research/stable-money research/wint-wealth research/compare/stable-money-vs-wint-wealth/products.json
python3 teardown/compare/compute.py research/stable-money research/wint-wealth research/compare/stable-money-vs-wint-wealth/comparison.json \
  --products research/compare/stable-money-vs-wint-wealth/products.json --focus-product bonds \
  --series research/compare/stable-money-vs-wint-wealth/series.json --sample-rule "<the run's sample rule>"
```
(`products.py` keeps an existing file's "labels" and "site" blocks and redrafts only "ads".)

`build.py` prints a lint report: banned performance words, "top" outside "top 30" or "top by", jargon, em and en dashes, verdict over 30 words; for a plan: one focus not on thin evidence, 2 to 3 start and 1 to 2 stop items, titles over 14 words, reasons over 40, first tests over 25 or missing, an evidence label that differs from its basis's rule, a basis or script reference that does not resolve; for scripts: 4 to 6 directions, each with persona, why, format, length, 2 or more openings, 5 or more beats, compliance and measures, a full script ending between 30 and 45 s, and a founder-led direction without a recommendation label. Quoted ad content is excluded from the word checks. (v3 move checks still run when a side has `moves` and no `plan`.)

## Sample rule (printed on the page)

Per brand, three Ad Library views, each sorted by the Library's "total impressions, high to low": all ads, video only, image only, about 30 each, overlapping. The sample is "the ads the Library ranks highest by impressions, with video and image each guaranteed a look".

Consequences:
- The video and image mix of the sample is our construction. Video rows are shares of the brand's sampled video ads; image rows are shares of its sampled image ads.
- The brand's real lean between video and image comes only from the "all ads" view (its top 30) and is shown as one line. This needs the crawler to record which view each ad came from (`sample_views` on the ad, see JSON below). If it is missing, the page says "not recorded" instead of guessing.
- Impressions are lifetime totals, so older ads are favoured. New ads that made the sample anyway are worth calling out (Now vs always).
- "Days live" is days so far for ads still running.

Medium: an ad is video if the Library says VIDEO or it carries a video asset; everything else (image, carousel, mixed-format ads without video) is image.

Untagged or `unclear` rows still count in the medium total N but in no row. The method section reports how many.

## The 7 rows

| id | Label (16 chars max) | Medium | Decision rule (first match wins, see TAGGING.md) |
|---|---|---|---|
| V1 | Person to camera | video | one person speaks to camera in at least 4 of 8 stills, first-person speech |
| V3 | Product or app demo | video | product or app in use fills the frame in at least 4 of 8 stills |
| V2 | Scene or story | video | people in at least 3 stills, not to camera |
| V4 | Text and motion | video | everything else |
| I1 | Offer-led | image | price, discount, cashback, rate or "free" is the largest text |
| I3 | Proof | image | quote, rating, reviews, press, comparison or list is the main element |
| I2 | Product or people | image | everything else |

Display order: V1, V2, V3, V4, I1, I2, I3.

Founder is never a row. One line sits under the map: "Founder says so on screen: Brand A 0, Brand B 5 (all Person to camera). Counted only where the ad itself says founder." Every founder mention elsewhere carries the same caveat.

## Status and evidence rules

Per row, per brand: n (ads), share (n / that brand's sampled ads of that medium), ideas (distinct concept_id), median days live, versions (sum of the Library's copies count), founder count.

- A brand is **present** in a row at 3 or more ads.
- **Only them / Only you**: one side present, the other not (2 ads or fewer; the cell still shows the count).
- **Them Nx / You Nx**: both present and the share ratio is 2 or more (N rounded down).
- **Even**: both present, ratio under 2.
- **Neither**: neither side present. (A 2 against 2 row reads Neither: 2 ads is too few to claim a lane.)

(Changed while building: round 2 said "the other has 1 ad or fewer" for Only, which left 2 against 5 undefined. Now any row with exactly one side present is Only.)

Evidence, judged on the side with more ads in the row:
- **strong**: 8 or more ads across 3 or more ideas.
- **thin**: under 4 ads, or 1 idea.
- **moderate**: everything else.

**Table stakes** are the Even rows. **Gaps** for a reader are rows where the rival is Only or leads (Nx). **Edges** are the reverse.

Re-checked after the first real comparison (Stable Money vs Wint Wealth, 19 Nov 2026). Video cells ran 0 to 16 ads on totals of 19 and 30, and the thresholds sorted them sensibly: the three strong rows (Person to camera, Scene or story, Product or people) each had 9 or more ads across 6 or more ideas; Text and motion at 3 ads across 2 ideas read thin, rightly. They broke on the image side, where one brand had 3 image ads in all: 2 of 3 (67%) shaded as the heaviest cell yet read Neither, and a 1 of 3 cell carried a "strong" gap because evidence is judged only on the side with more ads. Kept: present 3, lead 2x, strong 8 and 3, thin under 4 or 1 idea. Added: the small-base rule below (display now, compute.py to do).

## Page sections, in order

1. **First screen** (fixed layout below).
1b. **What they sell and what they say** (only when `extras` is present; see the JSON section).
2. **The map, row by row**: one fold per row with both brands' counts, ideas, versions, median days, founder count, and up to 2 evidence cards per side (still, opening line, days live, versions, Ad Library link). Card rule: the brand's ads in that row, one per idea, sorted by days live, then versions.
3. **Where you lead**: the reader's edge rows restated with their evidence (flips with the toggle).
4. **Table stakes**: the Even rows, "both of you do this, so differentiate inside it".
5. **Now vs always**: ads launched in the last 30 days that still made the sample, by row, per brand; launch month strip per brand (festive and sale timing).
6. **Hooks, offers and destination**: hook type for video and for image, offer type, angle, language, who is on screen, destination type, top campaign tags.
7. **Pacing**: per brand and per video row, medians over distinct videos (not ads): length, cuts per 10 seconds, words a minute, first cut.
8. **Standouts, frame by frame**: 2 per brand (rule below).
9. **Kept, gone, new** (planned): rendered only when a second snapshot exists (see below).
10. **Method and limits**: sample rule, snapshot date, denominators, unclear count, days-so-far caveat, versions caveat, founder rule, tag agreement.
11. **Appendix**: every ad of both brands with still, row, tags, days, versions, opening line, ad text, script, Library link.

### Standout rule
For each brand, take its two most distinctive rows: rows where it is present, ranked by its share minus the rival's share. In each row, take the idea whose lead ad has the most days live (ties broken by versions). Video rows are preferred when a brand has any video row present, so at least one standout is frame by frame. The rule is printed above the standouts.

(Changed while building: v1 said "the rows named in the moves". Moves are written after computing, so the rule now uses distinctiveness, which is computable and nearly always the same rows.)

### Kept, gone, new (planned)
Re-run the same sample 30 days later and pass the earlier comparison with `compute.py --previous old.json`. Per brand and per row: ads in both snapshots (kept), ads in the earlier one only (gone: stopped, or fell out of the top by impressions; the Library sample cannot tell which), ads in the later one only (new). The same by idea. The builder renders this section only when `rerun` is present.

## First screen (390 x 700)

Order, top to bottom:
1. Title line: "Brand A vs Brand B".
2. Sample line: "Meta ads in India, snapshot 19 Nov 2026. A 61 ads, B 74: the ones the Ad Library ranks highest by impressions. No spend or results are public."
3. Toggle: [I am Brand A] [I am Brand B]. Remembered per viewer; also set by `#A` or `#B` in the link.
4. Verdict.
5. Moves, 2 to 4, ranked, each with Effort and Evidence chips and a "See the ads" link that opens the row's fold (added while building: without it the moves had no tap-through, which fails the Evidence gate).
6. Top 30 line: "Top 30 overall: you 9 video, 21 image; they 20 video, 10 image." (When a medium has a small base, this line moves into that medium's small-base note inside the map.)
6b. What they sell line, when `extras.product_mix` is present.
7. Map: group header per medium ("VIDEO  you 31, them 34 sampled"), 7 rows, then the founder line.

Verdict and moves always fit on the first screen; the map starts on it and finishes within one swipe.

### Map row at 390 px
Usable width 358 px. Row height 44 px.
- Label column, 114 px: row name, 16 characters at most, 14 px semibold.
- Your cell, 84 px: share (4 characters at most, "41%"), 17 px bold; below it "14 ads, 63d" (11 characters at most), 12 px. Background shaded by share in 4 steps.
- Their cell, 84 px: the same. Your column is always on the left and flips with the toggle.
- Status column, 76 px: status (9 characters at most: Only them, Only you, Them 3x, You 4x, Even, Neither), and below it the evidence (strong, moderate, thin).
- The whole row is a tap target opening its fold.

### Worked dummy (I am Brand A)

```
Brand A vs Brand B
Meta ads in India, snapshot 19 Nov 2026. A 61 ads, B 74: the ones the Ad Library ranks
highest by impressions. No spend or results are public.
[ I am Brand A ]  [ I am Brand B ]

Brand B puts a person to camera in 14 of its 34 top videos; you have 2.
You lead on offer-led statics: 17 of your 30 top images against their 6 of 40.

1 Shoot 3 person-to-camera videos, one objection each. They run 14 of 34, across 5 ideas,
  median 63 days. First test: staff expert, phone, Hinglish, 30 s, on "is my money safe".
                                                         Effort Low   Evidence strong
2 Make proof statics: customer quotes and rating cards. They run 16 of 40 across 4 ideas;
  you run 1. First test: 3 quote cards on your best seller.  Effort Low  Evidence strong
3 Widen your offer statics: your 17 are 2 ideas. First test: add a cashback card and a
  deadline card beside your price card.                 Effort Low   Evidence moderate

Top 30 overall: you 9 video, 21 image; they 20 video, 10 image.

                    YOU            THEM           STATUS
VIDEO  you 31, them 34 sampled
Person to camera     6%  2 ads,18d  41% 14 ads,63d  Only them  strong
Scene or story      39% 12 ads,40d  24%  8 ads,35d  Even       moderate
Product or app demo 45% 14 ads,22d  29% 10 ads,30d  Even       strong
Text and motion     10%  3 ads,15d   6%  2 ads, 9d  Only you   thin
IMAGE  you 30, them 40 sampled
Offer-led           57% 17 ads,48d  15%  6 ads,20d  You 4x     moderate
Product or people   40% 12 ads,31d  45% 18 ads,55d  Even       strong
Proof                3%  1 ad, 12d  40% 16 ads,70d  Only them  strong

Founder says so on screen: you 0, them 5 (all Person to camera). Counted only where the ad itself says founder.
```

## Wording rules

### Verdict
- 30 words at most, one or two sentences.
- Exactly one gap (a row where the rival is Only or leads) and one edge (a row where the reader is Only or leads), each named by its row label.
- At least two "n of N" figures.
- Second person: "you", and the rival by name.
- No banned performance words (below).
- Must fail the swap test: false if another pair of brands is substituted.
- If there is no edge: "We found no row where you lead." Do not invent one.

### Move
- 2 to 4 moves, ranked.
- Each starts with a verb, names a row, cites the rival's n of N and idea count (or the reader's own, for an edge move), and gives one concrete first test (who, length, language, the claim).
- 35 words at most for the move text and 25 for the first test (build.py checks both), plus two labels: Effort (Low: phone shoot or template static; Medium: one shoot day or a designer week; High: agency production) and Evidence (the row's label).
- A thin row is never move 1.
- At least one move builds on an edge.

### Banned performance words
works, winning, winner, best-performing, top-performing, converts, effective, successful, profitable, ROI, ROAS, scaling. "Top" only as "top by Library impressions" or "top 30".

### Leader language (no jargon in visible text)
Say "versions" not DCO or copies, "idea" not concept or concept_id, "campaign tag" not UTM, "words a minute" not WPM, no "tercile", no "Entity ID".

## JSON

### Per ad, in research/<brand>/ads.json (already produced by the crawler)
`library_id, link, start_date, days_running, media_type, body, headline, link_description, cta, landing_url, copies, video_asset, extra`, plus optional `sample_views: {"all": rank, "video": rank, "image": rank}` (rank in each Library view it appeared in; needed for the top 30 line).

Tags: `videos/<asset>/tags.json` and `statics/<library_id>.tags.json`, shape in TAGGING.md.
Optional `tag_check.json` in the research folder: `{"n_checked": 14, "agreement": {"row": 0.86, "face": 0.79, "concept_id": 0.71}}`.

### comparison.json (written by compute.py)

```json
{
  "meta": {
    "snapshot_date": "2026-11-19", "country": "IN", "rules_version": "rows-v1",
    "sample_rule": "...",
    "brands": {
      "A": {"name": "Brand A", "dir": "research/brand-a", "n": 61, "n_video": 31, "n_image": 30,
            "unique_videos": 12, "unclear": {"video": 0, "image": 1},
            "top30_all": {"video": 9, "image": 21}},
      "B": {}
    },
    "tag_check": {"A": {"n_checked": 14, "agreement": {"row": 0.86}}, "B": null}
  },
  "rows": [
    {"id": "V1", "label": "Person to camera", "medium": "video",
     "A": {"n": 2, "share": 0.06, "ideas": 1, "median_days": 18, "versions": 3, "founder": 0, "ad_ids": ["..."]},
     "B": {"n": 14, "share": 0.41, "ideas": 5, "median_days": 63, "versions": 22, "founder": 5, "ad_ids": ["..."]},
     "status": "only_B", "lead": "B", "ratio": null, "evidence": "strong",
     "cards": {"A": ["ad_id"], "B": ["ad_id", "ad_id"]}}
  ],
  "table_stakes": ["V3", "I2"],
  "now": {"A": {"n": 3, "ad_ids": ["..."], "by_row": {"V3": 2}}, "B": {}},
  "launches": {"A": {"2026-09": 4, "2026-10": 9}, "B": {}},
  "breakdowns": {
    "hook": {"A": {"video": {"question": 9}, "image": {"offer": 14}}, "B": {}},
    "offer": {}, "angle": {}, "language": {}, "production": {}, "face": {},
    "destination": {"A": {"app": 40, "web": 21}, "B": {}},
    "deadline": {"A": 3, "B": 0},
    "campaign_tags": {"A": [["fd_rates_q3", 12]], "B": []}
  },
  "pacing": {"A": {"all": {"videos": 12, "duration_s": 28, "cuts_per_10s": 3.2, "wpm": 150, "first_cut_s": 1.8},
                   "by_row": {"V1": {}}}, "B": {}},
  "standouts": {"A": [{"ad_id": "...", "row": "V3", "idea": "A-c03", "why": "...",
                       "frames": [{"t": 0, "still": "videos/<asset>/still00_0s.jpg", "spoken": "..."}]}], "B": []},
  "ads": {"<library_id>": {"brand": "A", "medium": "video", "row": "V1", "tags": {}, "days": 63, "versions": 5,
                           "start_date": "...", "link": "...", "still": "videos/<asset>/still02_1s.jpg",
                           "hook_text": "...", "headline": "...", "body": "...", "cta": "...",
                           "destination": "app", "transcript": "...", "asset": "..."}},
  "rerun": null
}
```

(Changed while building: an `ads` block was added so the builder needs the research folders only for images; `copies` is shown as "versions".)

### perspectives.json (written by a person or model, merged by build.py)

```json
{
  "A": {"verdict": "Brand B puts a person to camera in 14 of its 34 top videos; you have 2. You lead on offer-led statics: 17 of your 30 top images against their 6 of 40.",
        "moves": [{"rank": 1, "row": "V1", "text": "Shoot 3 person-to-camera videos, one objection each. They run 14 of 34, across 5 ideas, median 63 days.",
                   "first_test": "Staff expert, phone, Hinglish, 30 s, on \"is my money safe\".",
                   "effort": "Low", "evidence": "strong"}],
        "now_read": "One line reading the reader's own and the rival's recent launches.",
        "india_read": ["Language: ...", "Timing: ...", "Destination: ..."]},
  "B": {}
}
```

`now_read` and `india_read` are optional; when missing the builder shows the numbers without a reading line (and rubric lines 10 and 14 score 1).

### Optional `extras` block (added after the first real comparison)

The 7-row map cannot show what each brand sells, its recurring series, or where its own ads disagree on figures. A founder wants all three near the top. When `perspectives.json` has a top-level `extras` key, `build.py` renders:
- one line on the first screen, just above the map: "What they sell, ads per product: you, ...; Rival, ...", with a link to the section below;
- a section "What they sell and what they say" straight after the first screen, before the row folds: product bars per brand, series and recurring lines per brand, and "Where their own ads disagree" (the reader's own ads first; flips with the toggle).

```json
"extras": {
  "source": "One line on how these were read (shown as the section lede).",
  "product_mix": {"A": {"items": [["Fixed deposits", 11], ["Bonds", 8]], "note": "optional line"}, "B": {}},
  "series": {"A": [{"name": "Papa Explaining", "ads": ["<library_id>"], "note": "what recurs"}], "B": []},
  "contradictions": {"A": [{"text": "Money invested: says 11,000 crore over its own 7,000 Cr+ end card.", "ads": ["<library_id>"]}], "B": []}
}
```

Rules: every key is optional. `ads` are library ids from comparison.json; each renders as an "ad 1, ad 2" link to the Ad Library (this is the tap-through for rubric line 3). Product counts must add up to the brand's sampled ads. Contradictions are figures that differ between ads of one brand or inside one ad (users, money invested, rate, tenure, minimum, payout schedule, exit), taken from the "Numbers that disagree across ads" list in `research/<brand>/concepts.md`, at most 5 per brand, each with the ads that show it. The wording rules (no banned words, no dashes, no jargon) apply; the lint covers the rendered text.

### Small bases (added after the first real comparison)
When either brand has fewer than 10 sampled ads of a medium (`SMALL_BASE` in build.py), that medium's map cells show counts ("2 of 3") instead of shares, are not shaded, and the group carries a note: "Small base ... shares say little about which kind of image ad each brand prefers", followed by the top 30 video and image split. Standout reasons use counts in the same case. A verdict or move must not rest on a share of a small base; say "its top 30 holds 3 images" instead. (To do in compute.py: cap evidence at moderate and use status "small base" when the other side's medium total is under 10.)

### Phone first screen (added after the first real comparison)
Three moves at the full word limits (35 + 25 words each) plus a 30-word verdict do not fit on 390 x 700. Under 720 px the first test sits behind a "First test" chip (one tap), and the move text, Effort, Evidence and "See the ads" stay visible. On wider screens the first test shows inline.

### Standout reason
The builder writes the reason from the rows, not from compute.py's `why`, so it never claims a lead the numbers do not show: "X is the brand's widest gap over Y (47% against 21%)" or, for a row where the brand trails, "X is the brand's other present row; here it trails Y (53% against 63%)". Frame strips drop stills inside the first 3 seconds that repeat the opening line, keeping the first and the one nearest 3 s.


## Version 4 additions

### Page order (v4, when a focus product is set)
1. **First screen**: header with sample and date, toggle, verdict, then the plan: Focus, Start, Stop or fix. Desktop right column, and on phones straight after the plan: "What they lean on" in brief (each brand's biggest series or idea, a still, its opening line, and the proxy caveat).
2. **What they lean on** (workhorses, below).
3. **<Product> against <product>**: the 7-row map restricted to the focus product, with small-base handling; a fold "All products together" holds the full-sample map as context.
4. The map, row by row (folds, focus product only).
5. **What each one sells**: a table per product of ads in the sample and the claim on each brand's site; then "What else each one advertises" (each other product with its ad count, ideas and the idea it leans on, with still and opening line) and "On the site but in none of the sampled ads".
6. **Scripts to brief** (per reader).
7. **Where their own ads disagree** (contradictions, from `extras`).
8. Where you lead and table stakes (focus product), Now vs always, Hooks and offers, Pacing (whole sample), Standouts, Method, Appendix.

### Workhorses: what they lean on
Unit: the idea (concept_id) and the series (a named set of ads from series.json or the brand's extras.json).
Leaning score, from public signals only: `ads using it + 0.5 x (versions - ads) + longest days live / 30 + 2 x (products or cities it is re-cut for - 1)`. Cities count only where tags carry `city`. The constants are `LEAN_DAYS` and `LEAN_RECUT` in compute.py and are printed on the page.
Per brand compute.py writes, for the whole sample, the focus product and each other product: the ideas ranked by score (top 5, each with ads, versions, longest days, products, lead ad), the series ranked the same way with their share of the sample, and concentration (ads carried by the top 1 and top 3 ideas, as n of N and share).
The page says, wherever leaning is shown: long life and many versions are the nearest public sign that a brand keeps paying for an idea, never that it performs.
Evidence for a plan item built on an idea or series: strong at 5 ads, or 120 days live with 2 ads; moderate at 2 ads or 90 days; thin otherwise.
Standouts (frame by frame) are now each brand's two highest-scoring video ideas in the focus product, so they are the workhorses, shown in full.

### Like for like by product
1. Read each brand's website and write `research/<brand>/site.md`: date fetched, URLs read, each product with its product_key, the headline rate or claim quoted exactly, other stated terms, scale claims, legal lines, and how the ads differ from the site. Pages that fail (404, server error, rendered only in the browser) are listed as such, never guessed.
2. `products.json` in the pair folder: `{"labels": {key: label}, "site": {"fetched": date, "A": [{"key", "claim", "url", "status"?}], "B": [...]}, "ads": {library_id: product_key}}`. `status` is `unclear` (signs of the product but not confirmed) or `registration_only`. Keys are normalised (bonds, fixed_deposit, recurring_deposit, fd_backed_card, mutual_funds, gold, or a category's own: gym_pass, diet_plan ...).
3. `--focus-product` restricts rows, table stakes and standouts to that key on both sides; `auto` takes the shared key with the most ads. If no key is shared (Cult.fit and Fitelo: gym passes against diet plans), there is no like-for-like map: say so in the verdict, and compare on the job the customer hires each for, or not at all.
4. Small bases: in the focus map a medium total under 10 on either side shows counts, not shares, caps evidence at moderate (now in compute.py), and a zero total shows "none, no image ads" instead of "0 of 0".

### perspectives.json, v4 schema
```json
{
  "A": {
    "verdict": "<= 30 words: names the product compared, one gap and one edge (a row, an idea or a series), two n of N figures",
    "plan": {
      "focus": {"title": "<= 14 words, imperative", "why": "<= 40 words, n of N", "basis": "series:A:Papa Explaining",
                "evidence": "strong", "effort": "Medium", "first_test": "<= 25 words", "script": 1},
      "start": [{"title": "...", "why": "...", "basis": "idea:B:WW-c10 | row:I2", "evidence": "...", "effort": "Low",
                 "first_test": "...", "script": 3}],
      "stop":  [{"title": "...", "why": "...", "basis": "contradictions:A | ads:<id>,<id>", "first_test": "..."}]
    },
    "workhorse_read": "one line reading both brands' leaning for this reader",
    "now_read": "...", "india_read": ["Language: ...", "Timing: ...", "Destination: ..."],
    "scripts": [{
      "title": "one line a head of marketing can say to the team",
      "label": "only for founder-led or untested directions: why it is a recommendation",
      "persona": "who it talks to, one line", "why": "evidence in this pair", "evidence_ads": ["<library_id>"],
      "format": "...", "length": "40 seconds", "language": "Hinglish",
      "openings": ["exact first line, Roman script where the evidence is Hinglish", "..."],
      "beats": [{"t": "0-3 s", "beat": "Hook", "note": "..."}],
      "script": [{"t": "0-3 s", "voice": "...", "screen": "..."}],
      "on_screen": "...", "end_card": "...", "compliance": ["..."], "measure": ["..."]
    }]
  },
  "B": {},
  "extras": {"source": "...", "contradictions": {"A": [{"text": "...", "ads": ["<library_id>"]}], "B": []}}
}
```
Basis kinds: `row:<id>` (focus map row; evidence must equal the row's), `idea:<brand>:<concept_id>` and `series:<brand>:<name>` (evidence by the workhorse rule above), `contradictions:<brand>` and `ads:<ids>` (shown as "In N ads", no strength label). `script` is the 1-based index of the reader's script direction the item links to.
Plan rules: Focus is the one thing, never on thin evidence; Start 2 to 3; Stop or fix 1 to 2 (contradicting figures, claims the site or the ads' own small print contradict). At least one item builds on the reader's edge or workhorse, and at least one answers the rival's workhorse.
Script rules: 4 to 6 directions per reader; each a full draft of 30 to 45 seconds. Use only facts the brand's own ads or site state; any figure that varies or is unknown is a placeholder ([your rate range], [your minimum], [tenure]). Founder-led directions carry a `label` saying they are a recommendation, since a founder counts only where an ad says so. Compliance notes name what this category's ads and sites show (for Indian fixed income: "up to" with every rate, tenure next to rate, minimum matching the app, no "guaranteed" or "assured", the risk disclaimer and broker strip, sale before maturity subject to a buyer, DICGC applies to bank FDs only). The page renders each direction as a fold with a "Copy this brief" button that copies a plain-text brief.
On phones the plan shows Focus with its reason and the titles and evidence chips of Start and Stop; each item's reason and first test open with one tap ("Why and test").
