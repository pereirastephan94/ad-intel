# Brief: break down one Mesa video ad

You are documenting competitor video ads for a marketing team at another Indian business school.
The reader will use your notes to write and shoot their own ads, so be concrete and exact. No padding.

For each video folder `research/mesa/videos/<asset>/` you are given, read ALL of:
- every `still*.jpg` (frames; the file name gives the time in seconds). Look at each image.
- `transcript.json` (machine transcript with timestamps; expect errors with names, Hindi/Hinglish and numbers)
- `metrics.json` (measured cuts, tempo, music-bed estimate, words per minute)
- `ads.json` (the ads that use this video: ad text, headline, button, landing page, start date, copies)

Then write `research/mesa/videos/<asset>/breakdown.md` with exactly these sections:

```
# <short descriptive title> (<asset id>)
- Creative name: <utm_content value(s) from ads.json landing_url, decoded; or "not in link">
- Programme: PGP (full-time) / Ascend (part-time) / Undergraduate / other
- Length, shape: <seconds>, <vertical 9:16 / square / 4:5 / landscape> (from metrics width x height)
- Language: <English / Hinglish / Hindi>
- Format: <e.g. founder talking head, student testimonial, influencer, podcast clip, screen recording, animation>
- Ads using it: <count>, earliest start <date>, total copies <sum>; links: <facebook ad library links>

## Script (verbatim)
Timestamped lines. Fix obvious transcription errors using on-screen captions where a frame shows them.
Mark any word you are unsure of with [?]. Do not invent lines. If Hindi is spoken, write it in Roman script and add an English gloss in brackets.

## First 3 seconds
What is on screen at 0, 0.5, 1, 2, 3 s (person, pose, text overlay word for word, graphic), what is said, and what kind of hook it is.

## Person on screen
Who (use a name ONLY if a caption, lower-third or the ad text names them; never guess identity from a face), role as stated,
apparent age band, clothing in detail (garment, colour, fit, accessories, glasses), hair/grooming, expression, energy, gestures,
whether they look at the lens or off-camera.

## Setting, framing and look
Location and background objects, shot sizes (close/medium/wide), angle, camera movement or static, lighting, colour grade,
production level (phone selfie / studio / podcast set / event footage), b-roll and cutaways with times.

## On-screen text, captions, logos, graphics
Caption style (position, font feel, colours, highlight words, one word or full line at a time), every headline/stat card word for word with its time,
logos shown (Mesa and any others, where and when), progress bars, stickers, emoji, end card contents word for word.

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
- Never identify a real person from their face. Names only from captions or ad text.
- Plain English. No hype. No em dashes.
- Do not edit any file other than the breakdown.md files assigned to you. Do not run git.
- When done, reply with one line per video: asset id, title, and the single most notable thing about it.
