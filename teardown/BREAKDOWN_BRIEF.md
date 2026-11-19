# Brief: break down one competitor video ad

You are documenting a company's video ads for a marketing team that competes with it, or wants to learn from it.
The reader will use your notes to write and shoot their own ads, so be concrete and exact. No padding.

`<research_dir>` below is the research folder you were given (for example `research/<company>`).

For each video folder `<research_dir>/videos/<asset>/` you are given, read ALL of:
- every `still*.jpg` (frames; the file name gives the time in seconds). Look at each image.
- `transcript.json` (machine transcript with timestamps; expect errors with names, numbers and any language that is not English)
- `metrics.json` (measured cuts, tempo, music-bed estimate, words per minute)
- `ads.json` (the ads that use this video: ad text, headline, button, landing page, start date, copies)

Then write `<research_dir>/videos/<asset>/breakdown.md` with exactly these sections:

```
# <short descriptive title> (<asset id>)
- Creative name: <utm_content value(s) from ads.json landing_url, decoded; or "not in link">
- Product or programme: as named in the ad (headline, link description, end card or landing page; or "not stated")
- Length, shape: <seconds>, <vertical 9:16 / square / 4:5 / landscape> (from metrics width x height)
- Language: <for example English, Hindi, Hinglish, Spanish>
- Format: <e.g. founder talking head, customer testimonial, influencer, podcast clip, product demo, screen recording, animation>
- Ads using it: <count>, earliest start <date>, total copies <sum>; links: <facebook ad library links>

## Script (verbatim)
Timestamped lines. Fix obvious transcription errors using on-screen captions where a frame shows them.
Mark any word you are unsure of with [?]. Do not invent lines. If a language other than English is spoken, write it as spoken
(Roman script for Hindi and similar) and add an English gloss in brackets.

## First 3 seconds
What is on screen at 0, 0.5, 1, 2, 3 s (person, pose, text overlay word for word, graphic), what is said, and what kind of hook it is.

## Person on screen
Who (use a name ONLY if a caption, lower-third or the ad text names them; never guess identity from a face), role as stated,
apparent age band, clothing in detail (garment, colour, fit, accessories, glasses), hair/grooming, expression, energy, gestures,
whether they look at the lens or off-camera. If nobody is on screen, say so.

## Setting, framing and look
Location and background objects, shot sizes (close/medium/wide), angle, camera movement or static, lighting, colour grade,
production level (phone selfie / studio / podcast set / event footage / animation), b-roll and cutaways with times.

## On-screen text, captions, logos, graphics
Caption style (position, font feel, colours, highlight words, one word or full line at a time), every headline/stat card word for word with its time,
logos shown (the advertiser's and any others, where and when), progress bars, stickers, emoji, end card contents word for word.

## Sound and pacing
From metrics.json: cuts, cuts per 10 s, first cut time, cuts in first 5 s, words per minute, tempo, music-bed estimate, speech share.
Say plainly that music was measured by software, not heard, so the genre and track cannot be named.

## Structure
Beat-by-beat table: time range | beat (hook, problem, proof, mechanism, offer, CTA...) | what happens.

## Claims and proof
Every number or factual claim made, word for word, and what proof (if any) is shown on screen for it.

## Offer and call to action
What the viewer is asked to do in the video, the button and headline in ads.json, where the link goes, and all ad text variants (verbatim, deduplicated).

## Why it may work, and where it is weak
3-6 bullets each. Judge as a performance marketer. Say only what the evidence supports.
```

Rules:
- Only describe what you can actually see or read. If something is not visible in the frames, write "not visible in the frames".
- Never identify a real person from their face. Names only from captions, lower-thirds, what is said aloud, or the ad text.
- Quote scripts and on-screen words verbatim.
- Cuts, tempo and the music-bed estimate are measured by software. Say so. Everything else is what you saw in the frames.
- Plain English. No hype. No em dashes.
- Do not edit any file other than the breakdown.md files assigned to you. Do not run git. Do not send anything to outside services.
- When done, reply with one line per video: asset id, title, and the single most notable thing about it.
