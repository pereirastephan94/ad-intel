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
