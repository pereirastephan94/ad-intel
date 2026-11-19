# How to break down one static (image) ad

`<research_dir>` below is the research folder you were given (for example `research/<company>`).

For each image `<research_dir>/images/<library_id>.jpg`, look at the image itself (Read tool) and at that ad's record in
`<research_dir>/ads.json` (key = library_id: body, headline, link_description, cta, landing_url, start_date, copies, platforms, extra).
Write `<research_dir>/statics/<library_id>.md`. Start with one title line, `# <short descriptive title> (<library_id>)`, then these
sections, in plain English, short sentences, no em dashes:

- **Facts**: library id, link, start date, copies, format (image / carousel / mixed), product or programme as named in the ad, campaign and audience clues read from the utm values in landing_url, landing page.
- **Ad text**: body, headline, link description and button, verbatim.
- **Words on the image**: every word, verbatim, in reading order.
- **Visual**: layout, colours, background, typography (weight, case, size hierarchy), photo or graphic, logos and where they sit, any faces (describe only what is visible: apparent gender, clothing, expression, pose; never name or identify a person from their face; names are fine only if printed on the image or in the ad text).
- **Hook and message**: the single idea, who it is for, the promise.
- **Claims and proof**: each number or claim, and whether a source is shown.
- **Offer and call to action**.
- **Why it may work / where it is weak**: two or three lines each.
- **Same creative as**: other library ids in your batch that use the same or near-same image.

The image may be a thumbnail of a video or the first card of a carousel; say so if it looks that way. Only state what you can see.

Rules: do not edit any file other than the statics files assigned to you. Do not run git. Do not send anything to outside services.
When done, reply with one line per image: library id, title, and the single most notable thing about it.
