# Comparison runbook: two written-up brands to a page that ships

For one agent, start to finish. Rules: COMPARE_SPEC.md (v4.1). Scoring: RUBRIC.md (v4; ship at 40 of 48, Useful 18 of 20, every gate at 2). Worked examples: research/compare/stable-money-vs-wint-wealth/ (shared product) and research/compare/cult-fit-vs-fitelo/ (no shared product). Never commit or push unless asked. Never edit research/<brand>/ except to add site.md. No em or en dashes; British spelling.

## 0. Check the inputs (5 minutes)
Each brand folder needs ads.json, concepts.md (ideas table, series, "Numbers that disagree", products table), extras.json, videos/<asset>/{tags.json, transcript.json, metrics.json, stills}, statics/<id>.tags.json. If tags or concepts.md are missing, stop: the write-up comes first.
Read crawl-state.json for each brand and write down what the pull really did: which views (all, video, image), sorted by impressions or not, which came back empty, how many ads each gave. This becomes the sample rule; never copy the spec's default wording.
Read both concepts.md files in full. Every figure on the page traces back to them, to comparison.json or to site.md.

## 1. Read each website and write research/<brand>/site.md
- curl through the session proxy (`curl -sS -L -A "Mozilla/5.0" <url>`); strip tags in Python to read. WebFetch may not resolve.
- Try the home page, the product pages, pricing, terms or refunds, and the sitemap (sitemap.xml often lists server-rendered pages, such as Cult.fit's pack pages with prices, when the main pages are script-only).
- Pages that need a browser: Playwright with `chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'})`. If scripts load from a host the proxy refuses, the page stays empty: list it as failed.
- site.md holds: date fetched, every URL read, every URL that failed and why, a table of products (product_key, headline claim quoted exactly, in how many sampled ads), results and scale claims, legal lines, and "How the ads differ from the site". Never name a person the ads do not name, even if the site does.

## 2. products.json
```
P=research/compare/<a>-vs-<b>
python3 teardown/compare/products.py research/<a> research/<b> $P/products.json --rules $P/product_rules.json
```
Write product_rules.json first ({key: [keywords]}, first match wins; put specific keys before broad ones). Then check: per brand, the counts per key must equal concepts.md's "Products advertised" table, and every idea must map to one key (print concept_id to key). Add by hand: `labels`, `site` ({"fetched", "A": [{key, claim, url, status?}], "B": [...]}; status unclear, registration_only or not_read), and `cities` ({library_id: place named in the ad text}) when a brand re-sends one film per city or centre. Add site-only products too (they fill "On the site but in none of the sampled ads").

## 3. series.json
From each concepts.md "Series and recurring devices" and extras.json. List every ad id of the series (extras.json lists only three examples). Count the ids against the concepts.md text ("19 ads", "16 ads"). Notes are shown on the page: no banned words inside them, even quoted ("WINNER" tripped the lint).

## 4. compute.py
```
python3 teardown/compare/compute.py research/<a> research/<b> $P/comparison.json \
  --products $P/products.json --series $P/series.json --focus-product <key|auto> \
  --sample-rule "$(cat $P/sample_rule.txt)" --sample-order <impressions|default> \
  --sample-short "<few words for the header>" --name-a "<Brand A>" --name-b "<Brand B>"
```
Keep the sample rule in $P/sample_rule.txt. Use `--focus-product` only for a product both brands advertise; if none is shared, leave it out (the page then compares whole samples and needs `extras.comparable`). Use `--sample-order default` when the views were not sorted by impressions. Use `--name-a/--name-b` when the Library page name is not the brand (Cult.fit's page is "cult").
Then print and read: rows (n, share, ideas, status, evidence), lean[k].all (top ideas, series, concentration), by_product, standouts, now, launches, breakdowns, pacing. Write down the figures you will use.

## 5. perspectives.json from a generator script
Copy $P/make_persp.py from the latest pair and rewrite every line; keep the generator in the pair folder. Contents per reader (A and B): verdict, plan (focus, 2 to 3 start, 1 to 2 stop), workhorse_read, now_read, india_read (language by medium, timing checked against the festival calendar, destination), 4 to 6 scripts; plus extras (source, contradictions up to 5 per brand, and for no shared product: products_note, map_note, comparable).
Plan rules: Focus never thin; one item builds on the reader's own workhorse or edge, one answers the rival's workhorse; each item has basis, why in n of N, first test, effort, and a script link where one fits. Phone first screen: titles about 40 characters, Focus why about 30 words, or Stop or fix falls below 700 px.
Script rules: a one-line title the team can repeat (persona-led, member or creator first-person, character series, coach-led, demo, founder-led); persona; why with evidence ads; format and length; 3 opening lines in Roman Hinglish where the ads are Hinglish; 5 or more beats; one full draft ending between 30 and 45 s; on-screen and end-card notes; the category's compliance watch-outs; what to measure. Only facts from the brand's own ads or site; anything that varies or is unknown is a [placeholder]; never invent prices, rates or results; founder-led directions carry a `label` saying they are a recommendation.

## 6. Verify every figure (do not skip; the first pair shipped 7 wrong claims)
**Every figure in a plan item must come from an ad in the row, idea, series or product its basis names.** Clicking "Ads" must land on ads that hold the figure. Then check each number against comparison.json or concepts.md with a short script: counts, idea counts, versions, days live, dates, quoted lines (grep the ad text and transcripts). Mistakes caught so far:
1. A figure quoted from an ad outside the move's row (11,000 crore from a scene ad in a person-to-camera move).
2. A share of a 3-ad base driving the verdict ("you run 1 of 3"); say "its sample holds 3 image ads".
3. "All" for a majority ("all on Earn Monthly Interest" when 8 of 9 were).
4. Holding up the rival's "one figure, 11%" while its own ads contradict it on tenure and minimum.
5. A timing word unchecked against the calendar ("around Diwali" for 7 October, a month early).
6. A "single burst" overcount (28 of 30 in October, when the burst was 20 on two days).
7. Language counted across media ("14 of 30 in English" mixed image text with video speech); split by medium.
Found on Cult.fit vs Fitelo: "five scale ideas say ₹999" when one shows no price; "no recurring character" when the rival has a recurring unnamed presenter; "eight places" when the ids gave seven; a method line saying the impressions views failed for both brands when only one was tried.
Found on SSB vs Mesa: a figure from another video of the rival (its careers lead) inside a reason whose basis is the investor recording; "you have no ad naming seats" when the reader's own film says "the next 100 students"; "three shapes" for three cuts in two shapes. Check every "none of your" against the reader's transcripts, not only its ad text.
Found on Atomberg vs Qubo: the brief named a shared product that was not one (Atomberg's Intellon is a water purifier, Qubo's Q200 and Q1000 air purifiers; check the product type on both sites before choosing the focus); "5 ads in Tamil or Telugu" when one of the five is unreadable (4 of 5); "catalogue cards" for a set of 8 cards and 2 clips; "the week before Diwali" for 27 Oct (12 days early); a `contradictions:` basis that counted every contradiction's ads ("In 13 ads" on a lock fix; use `ads:` with the item's own ads); a customer line paraphrased inside quotation marks (quote the transcript exactly, filler words included). Festival dates: only Diwali (8 Nov 2026) is pinned in this repo and no calendar host was reachable; name no other festival without a source.
Found on the Cult.fit vs Fitelo rebuild (60 ads): an inherited "free offer on 12" that came from a per-video tag (one gag video's three ads carry a trial headline on two; the ad text holds 11); a sample that grew after write-ups (Fitelo 58 ads, 34 written up: count only written-up ads and say so where the image rows sit); "every ad started 13 October to 17 November, longest 38 days" and "none of your ads shows a member, a rating or a result" both went false when 30 September ads joined (a first-person trek montage captioned "I gained muscle & lost fat"); a Library view counted as empty twice when it was three times. Re-read every old sentence against the new sample, not only the numbers.

## 7. Build, lint, look
```
python3 teardown/compare/build.py $P/comparison.json $P/perspectives.json research/<a> research/<b> <scratchpad>/pages/<pair>/
```
Lint must print 0 (banned performance words, "top" outside "top 30" or "top by", jargon, dashes, word limits, plan and script checks). "works out" and "winner" inside your own text both trip it.
Screenshot with Playwright at 390 x 700 (#A and #B), 1280 x 900, and the sections lean, wholemap or bonds, products, comparable, scripts, plus dark mode (`colorScheme: 'dark'`). Print `document.documentElement.scrollWidth`: it must be 390 at phone width. LOOK at every image:
- First screen for both readers: header, sample and date, toggle, verdict, Focus with reason and chip, every Start title with its chip, and Stop or fix begins on screen.
- Lean-on: rule printed, caveat present, stills and opening lines, concentration.
- Scripts: readable stacked rows at 390 px, copy button, founder label.
- Nothing unfinished: no "0 of 0", truncated names, lowercased brand words from `lowfirst` (start site claims with "The ..." if they begin with a capitalised product name).

## 8. Rebuild the earlier pages
After any change to compute.py, build.py or template.html, rebuild every published pair to its scratchpad folder and confirm lint 0 and scrollWidth 390.

## 9. Score and report
Score under RUBRIC.md v4 line by line, honestly; a 2 needs the evidence the line names. Iterate until it ships or say exactly which line cannot reach 2 and why (line 13 stays at 1 until a hand tag check exists). Report: both action plans and script titles, the score, tool changes (and document them in COMPARE_SPEC.md), what the websites showed, and what is still weak. Add any new miss to RUBRIC.md's change log and to the list in step 6.
