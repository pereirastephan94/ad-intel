# Tagging brief: one ad, eight tags

This brief is pasted into the tagger. It powers the head-to-head comparison (see COMPARE_SPEC.md).

## Inputs and output

You get, per creative: up to 8 stills, the transcript (videos), the ad text, headline and button.
Medium (video or image) comes from the Ad Library and is not yours to tag. Carousels and mixed-format ads with no video are tagged as images, judged on the first card.

Write one JSON file per creative:
- video: `videos/<asset>/tags.json` (one file per video asset, shared by every ad that uses it)
- image: `statics/<library_id>.tags.json`

Every tag allows `"unclear"`. List any tag you were unsure of in `tagging.unsure`.
Never identify anyone from their face. A name or role counts only if the ad itself says it (caption, lower-third, speech, ad text).

## The eight tags

### 1. row
Take the first rule that matches, in order.

Video:
- **V1 Person to camera**: one person faces and speaks to camera in at least 4 of the 8 stills, and the transcript is first-person speech.
- **V3 Product or app demo**: a product or app screen in use fills the frame in at least 4 of the 8 stills.
- **V2 Scene or story**: people appear in at least 3 stills but are not speaking to camera (acted scene, skit, montage, brand film).
- **V4 Text and motion**: everything else (animated text, graphics, stock footage with captions).

Image:
- **I1 Offer-led**: a price, discount, cashback, rate or "free" is the largest or first-read text.
- **I3 Proof**: a customer quote, rating, review count, press logo, comparison table or list of reasons is the main element.
- **I2 Product or people**: everything else (product shot, lifestyle, model, brand line).

### 2. face (the main person on screen)
- **founder_declared**: the ad text, a lower-third or the speech says founder, co-founder or CEO of this brand. Copy the exact words into `founder_evidence`.
- **expert_or_staff**: a labelled role (doctor, adviser, "our team") without a founder claim.
- **creator**: the Library shows a paid partnership, or a creator handle is shown.
- **celebrity_named**: the ad names a known public figure.
- **customer**: labelled as a customer or user, or speaks a first-person testimonial about using the product.
- **presenter**: speaks to camera with no label.
- **actor_model**: in an acted scene or posed shot, no label.
- **none**: no person.

### 3. hook
Video: the first 3 seconds (stills 1 and 2 plus the first spoken or on-screen sentence). Image: the largest text.
Take the first that applies, in this order:
1. **offer**: an incentive.
2. **number_claim**: a statistic or figure that is not an offer.
3. **social_proof**: users, ratings, awards.
4. **question**.
5. **problem**: names a pain.
6. **callout**: addresses an audience ("If you are a ...").
7. **story_open**: starts a narrative.
8. **visual_only**: no words in the first 3 seconds.

Also copy the exact first line into `hook_text` (spoken line for video if there is speech, else the first on-screen text; largest text for images).

### 4. offer
Only a concrete incentive stated in the ad: **none**, **discount** (percentage or amount off), **cashback**, **free** (item, trial, delivery), **rate_return** (an interest or return figure), **emi_or_bundle**, **other**.
Set `deadline` to true if a date or "today only" style limit appears.

### 5. angle
The main reason to buy, taken from the first claim made: **price_value**, **trust_safety**, **convenience_speed**, **quality_design**, **outcome** (a result for the user), **popularity** (scale, users), **feature** (one named feature), **identity** (who you become or belong with).

### 6. language
The spoken language if there is speech, else the on-screen text: **english**, **hindi**, **hinglish** (Hindi and English mixed within sentences), or **regional:<language>** (for example `regional:tamil`).

### 7. production
- **phone_lofi**: handheld, natural light, selfie framing.
- **studio**: lit set, steady camera, single location.
- **high_film**: several locations, cinematic grade, actors.
- **designed_static**: a graphic layout.
- **ai_or_stock**: visibly generated imagery or stock footage.

### 8. concept_id (second pass, after tags 1 to 7 are done for the whole brand)
Two creatives share a concept when all three match: the same row, the same main claim (same angle and essentially the same hook line), and the same main visual (same person, same product shot or same layout).
Differences in crop, aspect ratio, caption, button, end card, small copy edits or a dubbed language keep the same concept.
A new person, a new main claim or a new row makes a new concept.
Format: `<brand letter or slug>-c01`, `-c02`, and so on, numbered in the order you first meet them.

## Output shape

```json
{
  "tags": {
    "row": "V1",
    "face": "founder_declared",
    "founder_evidence": "lower-third: 'Asha, co-founder, Brand A'",
    "hook": "question",
    "hook_text": "Is your FD beating inflation?",
    "offer": "rate_return",
    "deadline": false,
    "angle": "outcome",
    "language": "hinglish",
    "production": "phone_lofi",
    "concept_id": "A-c07"
  },
  "tagging": {
    "model": "sonnet",
    "unsure": ["face"],
    "human_checked": false
  }
}
```

`founder_evidence` is an empty string unless `face` is `founder_declared`.

## Worked examples

**1. Video, a woman talks to camera in a kitchen for 28 seconds, Hinglish, no caption naming her.**
Stills: she faces camera in 6 of 8. Transcript opens "Mera paisa FD mein tha, par inflation ne sab kha liya."
Row V1 (person to camera wins before demo). Face **presenter** (no label; do not guess founder or creator). Hook **problem** (names a pain; no offer, number or question comes first). Offer none. Angle outcome. Language hinglish. Production phone_lofi.

**2. Image, a card with "9.1% p.a." as the biggest text, a bank logo strip and "Open in 2 minutes".**
Row I1 (the rate is the largest text, so offer-led beats proof even though logos are present). Face none. Hook **offer** (offer comes first in the order). Offer rate_return. Angle outcome. Language english. Production designed_static. If a second card has the same "9.1% p.a." layout with a different background colour, it gets the same concept_id.

**3. Video, an app screen recording with a voiceover, ending on a man saying "I'm Rohan, co-founder of Brand B" for 3 seconds.**
Stills: app screen in 5 of 8, the man in 2. Row V3 (he is to camera in only 2 stills, so V1 fails; the demo fills 5). Face **founder_declared** with `founder_evidence` "spoken: I'm Rohan, co-founder of Brand B". Hook from the first 3 seconds of the voiceover, for example "Three taps. That's all it takes." gives **number_claim**. Production studio if the screen recording is clean and the end shot is lit; otherwise phone_lofi.

## Rulings from review 1 (20 Nov 2026, after the first 5 Stable Money videos). These override anything above.
1. **How many stills.** Folders hold 8 to 16 stills. "At least 4 of 8" means "at least half of the stills that show the main footage" (ignore end cards and title cards).
2. **V1 means speaks to camera**, whatever the grammar ("I", "you" or "we"). A person talking to the lens while doing something (cooking, digging, walking) is still V1.
3. **Mixed videos** (a skit, then a presenter): the row is whichever fills more of the runtime. The hook is always judged on the first 3 seconds only.
4. **Hook tiebreak:** an opener shaped "If you..." or "Agar aap..." is `callout`. A flat statement of a pain is `problem`.
5. **hook_text** comes from the Roman-script transcript (the second pass, if `transcript_raw` exists in transcript.json, the main transcript is already the better one). Where a burned-in caption shows the words, the caption wins. Always Roman script, never Devanagari or Urdu script.
6. **face has one more value: `character`**: a recurring persona the ad itself labels (for example "Explained by Papa"). Quote the label in `founder_evidence`.
7. **angle** is the first product claim that is SPOKEN. An opening caption counts only if nobody speaks.
8. **offer** stays one value (the one given most prominence). Put any others in an optional list `offer_also`.
9. **production:** a phone on a tripod at home or in an office is `phone_lofi`, even with a ring light. `studio` needs a built set, a backdrop or clearly professional lighting.
10. **Three extra keys in `tags`** (free text, they feed the comparison writer):
    - `product`: what the ad sells, 8 words at most (for example "Bonds, 9 to 12% fixed returns").
    - `one_line`: the ad in one sentence, 25 words at most, plain English.
    - `script_twin`: the asset id of another video of this brand with nearly the same script but a different person or edit, else null.
11. **Catalogue ads.** If the ad text is unfilled placeholders such as `{{product.brand}}`, tag from the creative alone and add `"ad_text_missing": true`.

## Rulings from review 2 (20 Nov 2026, after Stable Money videos 6 to 15)
1. **People talking to each other** (skit, podcast set, video call, interview with an off-camera voice) is V2, not V1. V1 is only a person addressing the viewer.
2. **Unlabelled people in a V2 scene** are `actor_model`.
3. **A series title is a label.** "Papa Explaining", "Nani Tuitions" and the like make the face `character`; quote the title.
4. **Hook, tighter:** judge the FIRST sentence only. `number_claim` needs a statistic about the world or the product; a character's own bank balance in dialogue is `story_open`. A question one character asks another is `story_open`; `question` is only a question put to the viewer.
5. **script_twin** includes the same footage re-uploaded in another shape or length.
6. **Podcast set** with microphones and a dressed room is `studio`.

## Rulings from review 3 (20 Nov 2026, after Stable Money was finished)
1. **Same footage, new shape = same concept_id** (and also list it in script_twin). Same script, different person = new concept.
2. **A person who never looks at the lens** (reads a paper, answers an off-camera voice, street interview) is V2.
3. **Street interviews followed by a presenter:** V2 if the interviews fill more of the runtime.
4. **Hook is the first SENTENCE spoken**, even if a later sentence inside 3 seconds is a question. Twins must carry the same hook.
5. **angle for a pure rate claim** ("up to 8.5%") is `outcome`. A named product benefit (lounge access, monthly payout) is `feature`.
6. **Image with no headline** and a small stat row: I2. I1 needs the offer to be the largest or first-read text.
7. **Image ads can also carry `ad_text_missing`.**
8. Always note brand-level numbers that disagree across ads (user counts, amounts invested, visit counts) at the end of your reply; they go into the comparison.

## Rulings from review 4 (20 Nov 2026, after Wint Wealth videos 1 to 7)
1. **An order or promise to the viewer** ("Learn how to make money", "Stop doing this") is `callout`. Use `unclear` only when there are no words and no clear picture.
2. **Voiceover with no visible speaker:** face `none`. Hand-drawn, paper-craft or stop-motion explainers are V4 even with a short talking head; production value `animation_craft` (new allowed value).
3. **Creator:** a creator handle or name credited in the ad text, a caption or a partnership label makes the face `creator`. Quote it in `founder_evidence`.
4. **A spoken legal disclaimer** that only the raw transcript caught belongs in the Script table, marked "(disclaimer, from the first-pass transcript)".
5. **Romanising:** if a stretch of the main transcript is still not Roman script, romanise it yourself from captions and sound sense and mark [?]. That is expected, not a failure.

## Rulings from review 5 (20 Nov 2026, after Cult.fit)
1. **offer has one more value: `price_from`** (a "starting at" or "from" price with no discount stated). A free trial or free classes is `free`.
2. **deadline** is true only with a date, a day or "today". "Limited-time" with no date is false.
3. **A reviewer walking round a place** who opens to camera and then shows the venue is V2 if the tour fills more of the runtime; face is `presenter` unless the ad labels a creator or customer.
4. **"Don't feel like X? Then don't"** style openers are `callout`.
5. **Same footage with a different price or city on the end card** is the same idea (same concept_id). Record each price and city in `product` or `one_line`, because the spread across cities is itself a finding.
6. **production `high_film`** is about craft (graded, stabilised, several set-ups), with or without actors.

## Rulings from review 6 (20 Nov 2026, after Fitelo)
1. **Photo slideshows** (still photos, before-and-after pictures, captions, music or voiceover, nobody filmed speaking) are V4, not V2. V2 needs filmed people in a scene.
2. **Presenter plus customer montage of about equal length:** V1 if the presenter opens and closes the video.
3. **Before-and-after people:** face `customer` when the ad names them or labels the story as a user's (caption, lower-third, ad text); otherwise `actor_model`.
4. **A Library page category** ("Digital Creator", "Public figure") is not a creator credit. `creator` needs a handle, a name or a partnership label on the ad itself.
5. **Hook:** a claim that sets up a story ("Weight loss can make you look younger") is `story_open`; a start weight or size as the opener ("108 kg ...") is `problem`; a result as the opener ("He lost 25 kg in 90 days") is `number_claim`.
6. **Offer when sources differ:** the video itself wins (speech, then end card), then the headline, then the ad text. Put the others in `offer_also`.
7. **Results claims:** always record the kilos, the timeframe and what the small print says a typical user loses, in `one_line` or the breakdown. The gap between the headline result and the small print is a finding.

## Rulings from review 7 (23 Nov 2026, after Qubo)
- Feature or slogan headline as the opening ("Colour Night Vision", "Fingerprint is the new key"): hook `callout`. Testimonial or skit that opens on a story: `story_open`; on a rating or count: `social_proof`.
- Silent video: fill the Script table and `hook_text` from on-screen text, and say so. A machine transcript that does not fit the pictures is ignored and noted.
- Offer taken from the ad text or link description when the video has none; a flat price only in the ad text is `price_from`; a feature called "free" (built-in software) is not an offer: `none`, noted in prose.
- A person the ad text names but no frame or caption ties to the face: tag `celebrity_named`, never name them in prose from the face. A possibly famous unlabelled person: `actor_model`, flag unsure.
- CCTV or found footage of strangers (intruders, road clips): row V4 (scene, no presenter).
- The same footage reused in different edits is not a `script_twin`; note the overlap in prose.
- `music_bed_guess`: report the measured level beside the guess when they disagree.
