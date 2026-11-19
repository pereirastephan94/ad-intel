**The short version:** Mesa's 35 videos are almost all one thing: a person from the school, in a polo or a casual shirt, talking for about a minute in a Mesa office, with captions, a corner logo and a silent black end card. The scripts are tight and the hooks are good. The proof is thin, the numbers disagree with each other, and most videos never ask the viewer to do anything out loud.

How to read this: counts are out of the 35 video breakdowns and 71 static breakdowns. Ad and copy counts come from the `ads.json` file beside each video (94 video ads, 174 copies in total). Pacing numbers come from each `metrics.json`. Videos are named by a short quoted title. Speakers are described by clothing and setting. A name is used only where it is printed on screen or in the ad text.

### 1. The creative families

There are 35 video files but only about 22 different edits. The rest are recuts: the same edit in another shape, with a new first few seconds, or with a different end card.

| Family | Videos | Programme | Typical length | What it is | Ads / copies |
|---|---|---|---|---|---|
| Interview cut, maroon polo | 7 | Ascend 6, PGP 1 | 39 to 79 s, median 74 s | Seated man in a maroon polo in a teal office. Talks to someone off camera. Two cameras. Big captions with gold highlights. | 31 / 51 |
| Interview cut, peach shirt | 6 | PGP | 59 to 84 s, median 62 s | Seated man in a peach shirt. Talks off camera about placements, salaries, founders, student startups. Green highlights. | 8 / 9 |
| Staff talking head | 9 | PGP | 34 to 73 s, median 39 s | One staff member, mostly straight to the lens. Short, one idea, often a stat card. | 19 / 28 |
| Student story | 2 | PGP | 76 s | One student (named Apoorva in the ad text) tells her before and after. Square and a padded vertical copy. | 3 / 6 |
| Third-party podcast | 3 | PGP | 60 to 90 s | An investor-style endorser at a podcast microphone says founders should hire from Mesa. Three versions of one recording. | 8 / 12 |
| Borrowed clip plus selfie | 2 | PGP | 105.5 s | An 8 second stage clip of a known investor, then a staff selfie reacting to it. | 5 / 8 |
| Undergraduate podcast-mic | 3 | UG | 45 to 62 s | Man in a black Mesa polo at a studio microphone tells student success stories. Product shots, photos, logo cards. | 11 / 33 |
| Undergraduate presenter fast-cut | 3 | UG | 35 to 60 s | Presenter to the lens, one b-roll shot per claim, red and black title bars. | 9 / 27 |

- There is no animated explainer and no screen-recording-only video in the set. Every video is led by a person talking.
- By programme: 23 PGP videos (44 ads, 64 copies), 6 Ascend (30 ads, 50 copies), 6 Undergraduate (20 ads, 60 copies). Undergraduate has the fewest ads but the most copies per video.
- Most deployed single videos: "Average of the 5 people" (5 ads, 20 copies), "Two undergrads launched an app" (4 ads, 18 copies), "200 special people" square (7 ads, 13 copies), "Stuck in a rut" (6 ads, 11 copies), "90% of mid-career professionals" (6 ads, 11 copies).
- The simplest video is the most widely tested PGP one. "200 special people" is 38 s, one man, no b-roll, and it runs against at least 6 audiences.
- One shoot feeds many ads. The maroon-polo interview gives 6 Ascend videos plus "Software developer story (vertical)", which is the same edit with a full-time PGP end card.
- Recut pairs and sets: "B-school placements" (3 cuts), the investor endorsement (3 versions), "CAT 2025 question" (2), "25 lakhs" (2), "200 special people" (2), "Two years preparing for UPSC" (2), "Almost all startups" (2), "Software developer story" (2).
- Note: several breakdowns list fewer ads than the `ads.json` beside them now holds. The counts above use `ads.json`.

### 2. Hooks and the first 3 seconds

Hook types, one per video:

| Hook type | Videos | Examples |
|---|---|---|
| Statistic or money figure in the first sentence | 12 | "25 lakhs", "90% of mid-career professionals", "99.9% fail in the mind", "Only 0.001%", "50-60% salary increase", "200 special people", "Investor: sell 5 lakhs" |
| Story about a person or students | 8 | "Two years preparing for UPSC", "Software developer story", "5x-ed family business", "Pitched Elevation Capital", "Three 17 year olds, khakra brand" |
| Category problem or pain | 4 | "B-school placements" (3 cuts), "Stuck in a rut" |
| Curiosity tease | 3 | "CAT 2025 question" (2 cuts), "A stat schools never publish" |
| Question to a named audience | 2 | "#1 mistake", "Are you a parent" |
| Borrowed clip | 2 | "Almost all startups" (2 cuts) |
| Scenario or maxim said to "you" | 2 | "100+ founders", "Average of the 5 people" |
| Credential card, then a contrarian line | 1 | "Nobody asks for a CAT exam" |
| Outcome with a time qualifier | 1 | "In just their first year" |

- Only 2 of 35 open with a question. 12 open with a statistic. 8 open with a story. 9 name their audience in the first sentence (mid-career professionals, software developers, family business heirs, parents, students, CAT takers).
- 5 open with the filler "You know," ("B-school placements" in 2 cuts, "50 crore plus", "Two undergrads launched an app", "Three 17 year olds"). Mesa also runs a "B-school placements" cut with the filler removed, so they appear to be testing this.
- At 0 s, 32 of 35 open on the speaker in a close or medium shot, usually mid-word and mid-gesture. The other 3 open on a borrowed stage clip (2) or event footage with a name card (1). None opens on a logo sting or a title screen.
- Text is on screen by 0.5 s in 30 of 35. The exceptions use a stat card or name card that lands at 0.5 to 3 s.
- A number is spoken or shown in the first 3 seconds in 18 of 35. About 20 put a coloured stat card or highlighted number on screen in that window: "#1" in gold at 2 s, "90%" in gold at 0.5 s, "Avg Salary / 25 Lakh+" at 2 to 3 s, "200 / Special Students" at 1 s, "50-60%" in green at 2 s.
- Movement in the first second is usually a zoom, not a cut. At least 15 videos start tight on the face and snap or ease wider by 0.5 s. The software does not count this as a cut. 14 of 35 have no measured cut in the first 5 s. 15 have their first cut by 3 s.
- The Mesa logo is in a corner from the first frame in 29 of 35. One more shows only the "m" icon ("50 crore plus"). 5 have no logo until the end card: both "Two years preparing for UPSC" cuts and all 3 investor videos.
- Mesa is spoken in the first sentence in 4 videos ("200 special people" in 2 cuts, "50-60% salary increase", "50 crore plus"). It is first spoken after 20 s in at least 10. In "Almost all startups" it is first spoken at about 57 s. In 7 it is never spoken (see section 7).
- Two patterns for adding a reason to stay: a second hook mid-video ("And here's the interesting part" at 27.6 s in the student story; "And you know why?" at 10 s in "90% of mid-career professionals") and a pattern break (the black-and-white "REVERSE" rewind at 7.4 s in two investor versions).

The 10 strongest opening lines, verbatim (our pick, judged on how specific and how fast they are):

1. "Here's a stat most business schools will never publish."
2. "In the first eight weeks of their curriculum, every student has to sell 5 lakhs worth of product."
3. "I spent two years preparing for UPSC. Today, I work directly with the founder of a fast-growing F&B startup."
4. "One of the questions in CAT 2025 was this."
5. "Are you a parent who wants to see their child become a founder or a CEO?"
6. "Three of our first year students just pitched to Elevation Capital."
7. "Mesa alumni see a 50 to 60% increase in salaries one year into the job that they got post Mesa."
8. "So should I tell you the number one mistake that mid-career working professionals make?"
9. "Get up every day, go to office, do the same job over and over again."
10. "I know somebody who 5x-ed the profits of his family business by using AI."

### 3. People, clothing and look

- Who speaks: Mesa staff or leadership in 30 videos, a student in 2 (one student, two cuts), an outside investor-style endorser in 3. In the 6 Undergraduate videos students are shown and talked about but never speak.
- Names: a speaker is named on screen in only 2 of 35. "CAT 2025 question v2" and "Nobody asks for a CAT exam" carry a card reading "Ankit Agarwal / Harvard Business School / MBA, Class of 2016". No video gives a speaker's job title at Mesa. The student is named only in the ad text. The endorser is never named on screen; a small "AV" mark and a "V3 ventures" T-shirt are the only identifiers. One investor version shows a photo labelled "Varun Limaye" and "Ankit Agarwal".
- All main speakers are men except the one student. Stated or apparent ages are 30s to 40s for staff and 20s for the student.
- Clothing is casual and plain. The main speaker wears a polo in 23 of 35, a casual button-up shirt in 10, and a cardigan in 2. No suit, no blazer, no tie on any main speaker.
- Only 6 of 35 use Mesa-branded clothing (a black polo with a white Mesa chest logo). The rest are unbranded.
- No main speaker wears glasses. Hair is short and dark. Faces are clean shaven or have light stubble. A smartwatch and a small clip-on microphone are visible in most.
- Energy is high and fast. Median speech is 171 words per minute. Hands are in frame and moving in almost every still: pinched fingers on a number, a raised finger on "number one", a point at the lens on the call to action.
- Eye line: 20 of 35 look off camera at an unseen interviewer or podcast host. 14 look into the lens. One ("25 lakhs") is described both ways in its two breakdowns. All 13 interview cuts and all 3 investor videos are off camera.

Recurring presenters, by clothing and setting only:

| Look | Setting | Videos | Programme |
|---|---|---|---|
| Maroon polo, blue jeans, smartwatch | Dark armchair, teal wall, glass partitions, wooden "m" sign. Off camera. | 7 | Ascend 6, PGP 1 |
| Maroon polo | Bright glass-walled office, to the lens | 2 ("200 special people") | PGP |
| Peach long-sleeve shirt, sleeves rolled, khaki trousers | Seated, teal glass office and beige wall. Off camera. | 6 | PGP |
| Black polo with Mesa chest logo | Dim open-plan office, to the lens | 3 ("CAT 2025 question" 2 cuts, "A stat schools never publish") | PGP |
| Black polo with Mesa chest logo | Dark podcast studio, studio microphone. Off camera. | 3 | UG |
| Light grey polo with a small crocodile emblem | Dim office with warm ceiling lights | 3 ("25 lakhs" 2 cuts, "Only 0.001%") | PGP |
| Navy polo with white collar piping; pink "V3 ventures" T-shirt on campus | Podcast set with an abstract painting. Off camera. | 3 | PGP |
| Navy button-up shirt, clip microphone | Phone selfie in an office corridor | 2 | PGP |
| Black cardigan, gold hoop earrings | Bright campus hall, to the lens | 2 (student) | PGP |
| One-offs: navy polo, slate-blue polo, light blue chambray shirt, slate band-collar shirt | Office floors | 4 | UG 3, PGP 1 |

### 4. Setting, framing and camera

- Every talking head is indoors on what looks like Mesa premises or a podcast set. There are no outdoor talking heads and no home or street selfies. Only the 2 "Almost all startups" cuts are phone selfies, in an office corridor.
- Four backdrops cover almost everything: the teal glass office with a wooden "m" sign (15 videos), a dim open-plan office with out-of-focus ceiling lights (about 10), a dark podcast studio with a microphone on a boom arm (3 Undergraduate), and a podcast set with a painting (3 investor).
- Shot sizes: a medium or medium close-up base shot, with tight close-ups for emphasis. Interview cuts show knees and both hands. To-lens cuts are chest up.
- About 26 of 35 use two camera angles: a front angle and a side close-up. The edit cuts between them every 2 to 4 s. Single-camera videos fake a second angle with digital punch-ins.
- Cameras are static. Movement comes from cuts, re-crops and the opening zoom.
- Lighting is a soft key on the face, shallow depth of field, a blurred background. The full-time PGP look leans teal and warm. The Undergraduate look is darker with a red brand accent.
- B-roll is used in 30 of 35. It is always the same library: classrooms, students presenting, students selling at outdoor stalls, hands on laptops, guest speakers with microphones. It usually arrives in bursts under a list (16 cuts in 13 s in "50 crore plus"; 9 cuts in about 3 s in "25 lakhs").
- 5 have no b-roll in the body: "CAT 2025 question" (2 cuts), "Nobody asks for a CAT exam", "200 special people" (2 cuts).
- Real artefacts on screen are rare: an App Store listing (2 videos), a brand website screen recording (2), an Instagram Reel screenshot (1), a terminal recording (1), prize cheques (3).
- Shape by pixel size: 20 vertical, 11 square, 3 at 4:5, 1 landscape.
- Only 16 of the 20 vertical files fill the screen. The other 4 are square videos centred in a vertical frame with blurred bands that take about 22% at the top and 22% at the bottom ("Two years preparing for UPSC", "25 lakhs", "Only 0.001%", "200 special people"). One square file is the reverse: a vertical video inside a grey card ("Almost all startups").
- By programme: Ascend is never vertical (3 at 4:5, 3 square). PGP is mostly vertical (18 of 23). Undergraduate is mixed (3 square, 2 vertical, 1 landscape).
- The padded vertical copies all started on 18 November in one lookalike campaign that links to the `/pgp/` page. They look like a quick resize for a new placement, not a new edit.

### 5. Captions, on-screen text, logos and graphics

- All 35 have burned-in captions. None is continuous: most breakdowns note several stills with no caption at all.
- Four caption styles are in use:
  - Stacked build-up (13 interview cuts): large bold wide sans-serif, white, lower left, no box. A phrase builds over one to three lines, then blurs out.
  - Thin centred (about 10, including "CAT 2025 question", "A stat schools never publish", "Are you a parent", "Average of the 5 people"): light white sans-serif, 2 to 4 words at a time, over the chest. Several breakdowns call these small and hard to read.
  - Bold centred with a shadow (about 7, including "25 lakhs", "200 special people", the student story): 1 to 3 words at a time.
  - Boxed (3 investor videos): white on a grey translucent rounded box.
- One Undergraduate video ("Two undergrads launched an app") lights words up one at a time, grey then white. No other video does true word-by-word highlighting.
- Highlight colour follows the programme: gold for Ascend ("#1", "90%", "99.9%", "5x- ed", "50%", "50 crores"), green for PGP ("50-60%", "57.5%", "25 Lakh+", "200"), crimson red for Undergraduate ("three 17 year olds", "undergrad program", the "5" in "the 5 people").
- Card styles: PGP uses cream and green rounded cards with black text ("Avg Salary" / "25 Lakh+"; role cards "Founder's Office", "Entrepreneur in Residence", "Category Lead", "Marketing Lead"). Undergraduate uses stacked tilted bars, white text on crimson over white text on black ("Build / Real Businesses"). The investor video uses lime labels with line icons ("200+ Startups", "800 Crores").
- Numbered markers appear in the list videos: a gold "#1" and "#3" in the Ascend advice cuts, a numbered "3 Package it, brand it" label in "50 crore plus".
- Third-party logos are rare: an IIMB logo (3 placements cuts), an Elevation logo, a Perfora logo card, a Harvard crest in the name card. Employer names such as Zomato, Swiggy, Zepto and Urban Company are spoken, and no logo for them is visible in the stills.
- Corner logo: top right in 27, top left in 2 ("25 lakhs"), icon only in 1, absent in 5. Four of the 6 Undergraduate videos add the tag "OFFLINE UG PROGRAM" beside the logo.
- A second, physical logo is common: the wooden "m" wall sign, the chest logo on the black polo, wall lettering in classrooms.
- End cards: all 34 end cards seen are the same layout on black. Logo, programme name, an "Apply Now" button graphic. No voice. They last about 4.5 to 7 s. ("Stuck in a rut" ends on a black frame and its end card was not captured.)
  - PGP: white text "PGP in Startup Leadership & Entrepreneurship", green button.
  - Ascend: gold text "PGP in Business, AI & Entrepreneurship", gold button. The words "Ascend", "hybrid", "online" and "weekends" are not on it.
  - Undergraduate: crimson logo square, "Undergraduate Program in Business Management & Entrepreneurship", crimson button, "On-campus | Bangalore".
- 6 videos cut to a fully black frame before the end card ("CAT 2025 question" 2 cuts, "Nobody asks for a CAT exam", "200 special people" 2 cuts, "Only 0.001%").
- No video uses a progress bar, stickers or emoji.

### 6. Sound, music and pacing

Music was measured by software, not heard. The software estimates a tempo and guesses whether there is a sound bed under the voice. It cannot name a track or a genre, and its guesses change between two copies of the same edit ("25 lakhs" reads 161 and 144 bpm; "200 special people" reads "likely bed" in one copy and "cannot judge" in the other). Treat the music columns as rough.

| Video | Programme | Family | Shape | Length (s) | Cuts per 10 s | First cut (s) | Words per min | Tempo (bpm) | Music-bed guess |
|---|---|---|---|---|---|---|---|---|---|
| "#1 mistake" | Ascend | Interview cut, maroon polo | 4:5 | 77.6 | 3.09 | 2.68 | 165 | 96 | likely bed |
| "Stuck in a rut" | Ascend | Interview cut, maroon polo | 4:5 | 39.3 | 4.32 | 2.08 | 150 | 144 | little or none |
| "5x-ed family business" | Ascend | Interview cut, maroon polo | square | 63.6 | 3.46 | 1.96 | 169 | 144 | likely bed |
| "90% of mid-career professionals" | Ascend | Interview cut, maroon polo | 4:5 | 78.8 | 3.43 | 5.2 | 171 | 129 | little or none |
| "99.9% fail in the mind" | Ascend | Interview cut, maroon polo | square | 60.6 | 2.14 | 5.08 | 150 | 144 | little or none |
| "Software developer story" (square) | Ascend | Interview cut, maroon polo | square | 74.1 | 3.37 | 2.8 | 178 | 96 | likely bed |
| "Software developer story" (vertical) | PGP | Interview cut, maroon polo | vertical | 74.3 | 3.37 | 2.8 | 179 | 123 | little or none |
| "B-school placements" (vertical, no lead-in) | PGP | Interview cut, peach shirt | vertical | 60.1 | 3.83 | 3.56 | 141 | 89 | little or none |
| "B-school placements" (square) | PGP | Interview cut, peach shirt | square | 61.9 | 4.04 | 1.6 | 142 | 123 | little or none |
| "B-school placements" (vertical, "people ask me") | PGP | Interview cut, peach shirt | vertical | 61.7 | 3.89 | 1.6 | 143 | 123 | little or none |
| "100+ founders" | PGP | Interview cut, peach shirt | square | 68.3 | 2.49 | 7.88 | 159 | 96 | likely bed |
| "50-60% salary increase" | PGP | Interview cut, peach shirt | vertical | 58.7 | 2.9 | 1.12 | 171 | 103 | likely bed |
| "50 crore plus" | PGP | Interview cut, peach shirt | vertical | 83.8 | 3.82 | 3.09 | 201 | 108 | likely bed |
| "CAT 2025 question" | PGP | Staff talking head | vertical | 33.7 | 1.78 | 3.48 | 171 | 123 | likely bed |
| "CAT 2025 question v2" | PGP | Staff talking head | vertical | 37.3 | 2.15 | 0.88 | 155 | 117 | likely bed |
| "Nobody asks for a CAT exam" | PGP | Staff talking head | vertical | 39.0 | 1.03 | 0.88 | 188 | 99 | little or none |
| "25 lakhs" (full vertical) | PGP | Staff talking head | vertical | 44.0 | 5.22 | 7.04 | 159 | 161 | little or none |
| "25 lakhs" (padded vertical) | PGP | Staff talking head | vertical | 44.1 | 4.99 | 7.04 | 158 | 144 | little or none |
| "A stat schools never publish" | PGP | Staff talking head | vertical | 58.2 | 6.36 | 3.72 | 171 | 103 | likely bed |
| "Only 0.001%" | PGP | Staff talking head | vertical (padded) | 73.4 | 1.36 | 29.84 | 197 | 89 | little or none |
| "200 special people" (padded vertical) | PGP | Staff talking head | vertical | 38.2 | 1.57 | 9.8 | 163 | 117 | cannot judge |
| "200 special people" (square) | PGP | Staff talking head | square | 38.2 | 2.62 | 5.08 | 163 | 123 | likely bed |
| "Two years preparing for UPSC" (square) | PGP | Student story | square | 76.3 | 3.28 | 9.0 | 167 | 89 | little or none |
| "Two years preparing for UPSC" (padded vertical) | PGP | Student story | vertical | 76.3 | 3.01 | 10.3 | 167 | 89 | little or none |
| "Investor: 200+ startups" | PGP | Third-party podcast | vertical | 81.7 | 3.18 | 4.44 | 209 | 123 | little or none |
| "Investor: sell 5 lakhs" (60 s) | PGP | Third-party podcast | vertical | 60.1 | 2.99 | 7.36 | 188 | 123 | likely bed |
| "Investor: sell 5 lakhs" (90 s) | PGP | Third-party podcast | vertical | 90.1 | 3.55 | 7.36 | 205 | 123 | little or none |
| "Almost all startups" (vertical) | PGP | Borrowed clip plus selfie | vertical | 105.5 | 3.03 | 7.83 | 187 | 123 | likely bed |
| "Almost all startups" (square card) | PGP | Borrowed clip plus selfie | square | 105.5 | 1.42 | 7.83 | 187 | 123 | likely bed |
| "Two undergrads launched an app" | UG | UG podcast-mic | square | 62.0 | 2.42 | 2.4 | 179 | 96 | little or none |
| "Three 17 year olds, khakra brand" | UG | UG podcast-mic | vertical | 60.8 | 2.96 | 2.12 | 188 | 117 | little or none |
| "In just their first year" | UG | UG podcast-mic | square | 45.3 | 6.18 | 2.73 | 170 | 123 | likely bed |
| "Pitched Elevation Capital" | UG | UG presenter fast-cut | square | 50.4 | 4.56 | 1.33 | 200 | 123 | likely bed |
| "Are you a parent" | UG | UG presenter fast-cut | vertical | 35.3 | 5.94 | 2.64 | 173 | 89 | likely bed |
| "Average of the 5 people" | UG | UG presenter fast-cut | landscape | 60.3 | 6.14 | 3.56 | 193 | 117 | likely bed |

Ranges and medians:

| Group | Videos | Length (s), range and median | Cuts per 10 s, range and median | First cut (s), median | Words per min, range and median | Tempo (bpm), median | Music-bed guess |
|---|---|---|---|---|---|---|---|
| All | 35 | 33.7 to 105.5, 60.8 | 1.03 to 6.36, 3.28 | 3.56 | 141 to 209, 171 | 123 | 17 likely, 17 little or none, 1 cannot judge |
| PGP | 23 | 33.7 to 105.5, 61.7 | 1.03 to 6.36, 3.03 | 5.08 | 141 to 209, 171 | 123 | 10 likely, 12 little or none, 1 cannot judge |
| Ascend | 6 | 39.3 to 78.8, 68.9 | 2.14 to 4.32, 3.40 | 2.74 | 150 to 178, 167 | 136.5 | 3 likely, 3 little or none |
| Undergraduate | 6 | 35.3 to 62.0, 55.4 | 2.42 to 6.18, 5.25 | 2.52 | 170 to 200, 183.5 | 117 | 4 likely, 2 little or none |
| Interview cut, maroon polo | 7 | 39.3 to 78.8, 74.1 | 2.14 to 4.32, 3.37 | 2.80 | 150 to 179, 169 | 129 | 3 likely, 4 little or none |
| Interview cut, peach shirt | 6 | 58.7 to 83.8, 61.8 | 2.49 to 4.04, 3.83 | 2.34 | 141 to 201, 151 | 105.5 | 3 likely, 3 little or none |
| Staff talking head | 9 | 33.7 to 73.4, 39.0 | 1.03 to 6.36, 2.15 | 5.08 | 155 to 197, 163 | 117 | 4 likely, 4 little or none, 1 cannot judge |
| Student story | 2 | 76.3 | 3.01 to 3.28 | 9.65 | 167 | 89 | 2 little or none |
| Third-party podcast | 3 | 60.1 to 90.1, 81.7 | 2.99 to 3.55, 3.18 | 7.36 | 188 to 209, 205 | 123 | 1 likely, 2 little or none |
| Borrowed clip plus selfie | 2 | 105.5 | 1.42 to 3.03 | 7.83 | 187 | 123 | 2 likely |
| UG podcast-mic | 3 | 45.3 to 62.0, 60.8 | 2.42 to 6.18, 2.96 | 2.40 | 170 to 188, 179 | 117 | 1 likely, 2 little or none |
| UG presenter fast-cut | 3 | 35.3 to 60.3, 50.4 | 4.56 to 6.14, 5.94 | 2.64 | 173 to 200, 193 | 117 | 3 likely |

- Length: 9 videos are 45 s or shorter, 13 are 45 to 65 s, 13 are longer than 65 s. The typical Mesa video is one minute.
- Speech is fast everywhere. The slowest are the 3 "B-school placements" cuts (141 to 143 words per minute). The fastest are the investor videos (205 and 209) and "50 crore plus" (201).
- The fastest cutting: "A stat schools never publish" (6.36 cuts per 10 s, 37 cuts in 58 s), "In just their first year" (6.18), "Average of the 5 people" (6.14), "Are you a parent" (5.94). These hold the presenter for a few seconds, then run one b-roll shot per phrase, with a stat card or title bar on most beats. Undergraduate is the fastest programme (median 5.25).
- The slowest cutting: "Nobody asks for a CAT exam" (1.03, one jump cut in 30 s of talk), "Only 0.001%" (1.36, no cut until 29.8 s), "200 special people" and "CAT 2025 question" (about 1.6 to 2.6). These are one person to the lens with no b-roll, held up by delivery and caption animation.
- The tempo guess is 123 bpm in 12 of 35. The software found a likely sound bed in half the videos and little or none in the other half. Several breakdowns note that the last 2 s of the end card are fully silent.
- Speech starts at 0 s in nearly every video. Speech share is 0.82 to 0.98. The only regular silence is the end card.

### 7. Script structure

Common arcs, one per video:

| Arc | Videos | Shape | Examples |
|---|---|---|---|
| Outcome claim, then mechanism, then more proof | 10 | Lead with a result. Explain how the school produces it. Add a number. Silent end card. | "B-school placements" (3), "25 lakhs" (2), "50-60% salary increase", "50 crore plus", "100+ founders", "A stat schools never publish", "In just their first year" |
| Problem, then Mesa as the fix | 9 | Hook, problem or enemy, reframe, "that's where Mesa comes in", mechanism, sometimes a call to action. | "CAT 2025 question" (2), "Nobody asks for a CAT exam", "Only 0.001%", "Almost all startups" (2), "Stuck in a rut", "99.9% fail in the mind", "5x-ed family business" |
| Student result, then how, then "every student does this" | 6 | A specific student win, the steps they took, then the claim that it is the course. | "Two years preparing for UPSC" (2), "Pitched Elevation Capital", "Two undergrads launched an app", "Three 17 year olds", "Average of the 5 people" |
| Advice as content | 4 | Problem, then a numbered list of advice. The school is not pitched in speech. | "#1 mistake", "90% of mid-career professionals", "Software developer story" (2) |
| Third-party endorsement | 3 | Credentials, founders' hiring problem, "I found this school", the one mechanism, hiring number. | 3 investor versions |
| Direct pitch | 3 | Hook, promise, three points, spoken call to action. | "200 special people" (2), "Are you a parent" |

- Typical size: 96 to 329 words, median 179. The short direct pitches are about 100 words. The interview cuts are 140 to 280. "Almost all startups" is the longest at 329.
- Lists carry the middle of the script. 8 videos use a counted list ("three ways", "four things", "number one... number four"). Many more use an uncounted run of verbs: "pick a category, build a product and website, make content, run ads and then sell online and offline".
- One mechanism is repeated across voices: sell 5 lakh of product in the first 8 weeks. It is in all 3 investor videos and in "50 crore plus", and on 6 Ascend statics.
- AI is mentioned in speech in 24 of 35, usually as a threat to narrow jobs and then as a skill the programme teaches.
- 12 of 35 define Mesa against other schools: CAT, student-run placement committees, "fireside chats", "the 10,001th employee", BBA colleges with "a curriculum which is 100 years old".
- Spoken call to action: 11 of 35 ask the viewer to apply out loud. 2 more close softly ("make sure you're on the right side of that gap"; "All the best"). 22 end on the argument and leave the ask to the silent end card.
- The spoken asks are plain: "Apply to Mesa now.", "If you are interested, apply now.", "Apply as quickly as possible."
- 7 of 35 never say "Mesa" aloud: "#1 mistake", "Stuck in a rut", "90% of mid-career professionals", "Software developer story" (2 cuts), "Nobody asks for a CAT exam", "In just their first year". Four of those are Ascend, so 4 of the 6 Ascend videos never name the school in speech.
- No video names the Ascend programme in speech. It is called "the hybrid PGP in business, AI and entrepreneurship".
- The three investor videos speak to employers ("when you hire from Mesa") while the ads target applicants.

### 8. Claims and proof

No number in any video or static carries a source, a year, a cohort or a sample size. The checkable proof in the whole set is an App Store listing, a brand's Instagram page and product packs, and one name card.

| Claim | Where it appears | Proof shown | Problem |
|---|---|---|---|
| Every student sells 5 lakh of product in the first 8 weeks | 4 videos (3 investor, "50 crore plus"); 6 Ascend statics ("Make ₹5 Lakh in Revenue", "Generate 5L in just 8 Weeks") | B-roll of students at stalls | Per student in the videos. One Ascend static says "Teams of 3", "₹1L capital per team", "₹5L+ sales target". A PGP static says "80L+ revenue in 8 weeks" for all businesses combined. "Almost all startups" says each student's business reaches "almost one crore". |
| 100% placements | 3 videos ("B-school placements") | None | No year, cohort or report. |
| Average salary upwards of 25 lakhs | 2 videos | A card that repeats it | No definition. Other creatives use different salary measures: "50 to 60% increase in salaries one year into the job" (1 video) and "2.8x average salary jump" (1 static). |
| 57.5% joined super early stage startups; 54% got ESOP grants; many turned down offers 1.5x higher | 1 video | A "57.5%" card | Statics say "58% of Mesa graduates land in founder-facing roles" (2) and "71% Made a Career Pivot" (3). Three percentages, none defined. |
| Startups that hire from Mesa | "at least 500 startups" in touch (3 videos), "150 plus startups are already hiring" (3), "more than 100 plus startups trust talent" (1) | None. Urban Company, Zepto, Zomato, Swiggy are spoken only. | Three different numbers for a similar idea. |
| Careers team size | 3 cuts | A blurred green number | The breakdowns read it as 15, 16, 55 or 60. The stat does not land. |
| 100 plus founders visit campus; almost 40% of students get jobs through them | 2 videos; 1 video | Unlabelled b-roll | No founder named or shown. |
| Student startups: 50 crore in revenue, 25 crore raised, Shark Tank | "50 crore plus" ("50 crore plus", "two students" on Shark Tank), "99.9% fail in the mind" ("almost 50 crores", "multiple startups featured") | Caption text | Used to sell Ascend, though the track record is from full-time students. An Ascend static adds "~50 startups incubated". |
| 200 students, fifth cohort | 2 videos, 1 static; "5th cohort" in the investor ad text | A "200 / Special Students" card | Other ad text says "Cohort 2028 applications are open". Ascend statics say "Founding Online PGP Cohort", "Cohort Starting in 2027". |
| Pitch to VCs | "Demo days where you get to pitch to 50 plus VCs" (1 video); a student "pitched it to 50 plus VCs" (1 video); "Pitch it to 25+ VCs on Demo Day" (4 Ascend statics) | A stage photo | 50 for PGP, 25 for Ascend. |
| Khakra brand revenue | "20 lakh in revenue every single month" (1 video) and "25 lakh in revenue every single month" (1 video) | Product packs, a cheque for "Ten Thousand Only", a Reel with 54 likes | Two figures for the same brand in two ads launched the same day. |
| Students' app has "thousands of users" | 1 video | An App Store page showing "4 RATINGS" | The proof on screen undercuts the claim. |
| Less than 5% of applicants get an offer; "five step admissions process" | 1 video | A list card | Four steps are named and shown. |
| Founder and staff pedigree | "One is a Harvard Business School alum and the other went to Kellogg" (3 videos); name card with "Harvard Business School, MBA, Class of 2016" (2); "MBAs from IIMs, ISB and Harvard" (3); "at Kellogg" (1) | Harvard crest, IIMB logo | The best-anchored claim family, and still shown on only 2 name cards. |
| Big unsourced framing numbers | "90% of mid-career professionals", "99.9% of companies fail in the mind", "Only 0.001% of people", "Almost 95% of jobs in MNCs", average company "30 employees", "100% going to become irrelevant" | Gold or bold caption only | Rhetorical figures stated as facts. |
| "The only B-school teaching AI agents & no-code" | Headline on 13 of 94 video ads | None | Not said or shown in the videos it sits over. |
| 150 plus hours of applied AI; every student builds one working AI product | 1 video | None. No product is shown. | The three student examples are unnamed. |
| Grants up to Rs 10 lakh | 1 video | None | "Up to" is not explained. |

Other proof gaps noted in the breakdowns:

- B-roll that does not match the claim: a Mesa prize cheque shown under "pitched to Elevation Capital"; a terminal recording with another person's account name under "They used Claude Code"; a group talk under "one-on-one mentorship" (2 videos); a guest in a "BLUME" polo under an unnamed student's VC pitch.
- Audience definitions do not line up for Ascend: speech says "27 to 32 year olds" (2 videos), targeting is ages 25 to 38, ad text says "5+ years of experience".
- The student story is the only video with a causal chain (a named project, an AI agent she built, a named employer). Even there, no agent, offer or workplace is shown, and her name and title are not on screen.

### 9. Offers and calls to action

- No video states a fee, a deadline, a scholarship, a test date or an intake date. The only urgency in speech is "apply as quickly as possible" and "apply fast" (the last word is unclear in the transcript).
- Buttons on the 94 video ads: "Apply now" on 88, "See details" on 6. The 6 "See details" ads all carry videos whose end card says "Apply Now".
- Where the click goes: the homepage on 27 of 94, `/ascend` or `/pgp-ascend` on 30, the Undergraduate page on 20, `/pgp-sle1` on 11, `/pgp` on 6. More than half of the full-time PGP video ads land on the homepage.
- 13 of 94 video ads have no ad text and no headline at all. All are Undergraduate. The Undergraduate links carry no tracking tags.
- Headlines are shared across unrelated videos. "Your classmates could be your co-founders" (13 ads) sits over placements, salary and funding videos. "The only B-school teaching AI agents & no-code" (13 ads) sits over the CAT, investor and "stat" videos. Ascend headlines match their videos one to one ("Stuck in a rut at work? Start here", "No need to quit your job", "Grow beyond one function").
- Ascend ad text carries the facts the videos leave out: "12 months of weekends", "For professionals with 5+ years of experience", "About 10 hours a week", "6 short campus blocks in Bangalore".
- The real offers are in the statics, and mostly in the body text, not on the image:
  - Ascend early bird: "Early bird applications close Nov 26, 2026" appears in 17 static breakdowns. Only 2 images print the date. Two other ads say "Early bird closes 29 Nov".
  - Ascend scholarships "up to ₹10L": 12 static breakdowns, body text only.
  - "No application fee": 4 static breakdowns, body text only.
  - Ascend info session: "22 November", "12:00 PM IST", Zoom, "LIVE WITH VARUN LIMAYE" (3 statics, linking to an info session page). The image says "Register Now". The ad button says "Apply now".
  - PGP "UP TO 40% Scholarship": 2 images, with no ad record beside them.
- Scarcity lines: "200 special people", "less than 5% of the applicants get an offer", "Founding Online PGP Cohort", "handpicked cohort".

### 10. Statics

71 static breakdowns: 53 Ascend, 18 PGP, none for Undergraduate. 13 of the PGP ones are cards inside dynamic-creative ads, where Meta mixes images and text.

Templates:

- Ascend, centred dark: near-black background, two-line headline with the second line in gold, a wide rounded photo, a gold pill with the programme name, a bottom bar reading "Online", "12 Months", "Apply Now".
- Ascend, centred light: the same layout on off-white graph paper, with a gold highlighter bar under the key phrase.
- Ascend, editorial split: left-aligned bold headline, a middle band split into a colour panel ("Online", "12 Months", button) and a photo. Dark and light versions.
- Ascend, polaroid: square. Graph-paper top, black curved bottom, two tilted photos, outlined chips ("12 months", "Weekends").
- Ascend, text only: "Founding / Online PGP / Cohort" in huge type on dark green or over a blurred photo.
- Ascend, struck-through list: "Quit your job." "Move cities." "Pause your career." crossed out in gold, then "A PGP on weekends".
- Ascend, info session story: vertical, italic serif headline, date and time box, "Register Now".
- PGP, dark green: very dark green background, thin grey sans-serif mixed with a bold italic serif in a yellow-green gradient, cut-out portraits, pill chips ("12 months", "Full-time", "Bangalore").
- PGP, mint paper: pale mint crumpled-paper background with one large statistic.

Colour systems match the video end cards: gold on black or cream for Ascend, green and yellow-green on dark green for PGP. The logo is top right on all but 2.

Shapes: Ascend is 34 at 4:5, 16 square, 3 vertical. PGP is 10 vertical, 8 square. So Ascend statics, like Ascend videos, are almost never full-screen vertical.

Headline themes on the image:

| Theme | Programme | Statics | Copies |
|---|---|---|---|
| "Founding Online PGP Cohort" | Ascend | 11 | 32 |
| "You Don't Have to Quit Your Job to Learn to Build" | Ascend | 7 | 19 |
| "What If You Could Build Your Own Startup Without Quitting Your Job?" | Ascend | 6 | 18 |
| ₹5 lakh in 8 weeks | Ascend | 6 | 15 |
| "Spend a week inside the world's startup hubs." | Ascend | 6 | 13 |
| "A PGP on weekends" (struck-through list) | Ascend | 5 | 10 |
| "Pitch it to 25+ VCs on Demo Day." | Ascend | 4 | 9 |
| "Not another MBA." | Ascend | 4 | 7 |
| Info session | Ascend | 3 | 3 |
| "Become the AI-native operator at work" | Ascend | 1 | 4 |
| Named alumni stories ("Started as an Intern. Now Marketing Lead at Comet.") | PGP | 5 | 5 |
| "71% Made a Career Pivot" | PGP | 3 | 6 |
| "58% of Mesa graduates land in founder-facing roles" | PGP | 2 | 5 |
| "UP TO 40% Scholarship" | PGP | 2 | not known |
| One-offs: "BYOB", "200 STARTUP LEADERS", "2.8x", "Where startups become your classroom", "WHERE CAN YOUR AI SKILLS TAKE YOU?", role pills | PGP | 6 | 6 |

- Ascend statics sell one idea in several wordings: keep your job. 29 of 53 are a version of "don't quit" or "founding cohort".
- PGP statics do something the videos do not: they name people. Cards print alumni names, previous employers and current roles ("Prev: Deloitte", "Founder").
- Where image, text and button mismatch:
  - The programme has two labels. 29 Ascend images say "Online PGP". 21 say "Hybrid PGP". The videos say "hybrid".
  - The deadline, the scholarship and the fee waiver are in the body text and missing from most images.
  - Info session images say "Register Now" under an "Apply now" button.
  - PGP stat images say "Explore the PGP program" under an "Apply now" button.
  - In dynamic-creative ads the alumni image, the headline ("The only B-school teaching AI agents & no-code") and the body text (peers as co-founders) are three different messages.
  - The startup hubs image does not say the trips are "optional and paid separately". That is only in the body.
  - Photos are often generic: the same pitch-stage photo and the same classroom slide are reused across themes. Slides readable in the photos name unrelated products.

### 11. Weak spots a competitor can exploit

1. **Nobody says who is talking.** A speaker is named on screen in 2 of 35 videos and no video gives a Mesa job title. The student's name is only in the ad text. The endorser is never named. A competitor who puts a name, a title and a credential in a lower third from second one looks more accountable.
2. **Numbers with no source, and numbers that disagree.** 20 lakh against 25 lakh a month for the same khakra brand. 100, 150 and 500 startups. 25 lakh average salary, "50 to 60%" and "2.8x". 57.5%, 58% and 71%. A careers team of 15, 16, 55 or 60. One sourced, dated, defined number would stand out against all of them.
3. **Told, not shown.** Employers are spoken, not shown. No offer letter, dashboard, product demo or named founder appears. Where proof is shown it sometimes contradicts the line ("thousands of users" over "4 RATINGS"; a prize cheque under an investor pitch; a group talk under "one-on-one").
4. **Students almost never speak.** One student voice in 35 videos. The 6 Undergraduate videos are all staff describing students who are not named and do not talk. No employer, parent or manager appears either; the manager "quotes" in "50-60% salary increase" are read out by staff.
5. **No ask, then a silent card.** 22 of 35 have no spoken call to action. Every video ends on 4.5 to 7 s of black card with no voice. 7 never say the school's name. No video gives a deadline, a fee or a next step such as a call or an event.
6. **The wrapper fights the video.** Two shared headlines cover 26 of the 94 video ads and match almost none of the videos under them. 27 ads land on the homepage. 6 use "See details" over an "Apply Now" end card. 13 Undergraduate ads have no text at all.
7. **Weak use of the phone screen.** Only 16 of 35 are true full-screen vertical. 4 are padded squares that leave about 44% of the screen blurred. One is landscape with 20 copies behind it. Ascend has no vertical video and almost no vertical static.
8. **Soft, slow openings on the interview material.** 20 of 35 never look at the viewer. 14 have no cut in the first 5 s. 5 start with "You know,". "50 crore plus" takes 6 to 7 s to reach its number. "Only 0.001%" holds one shot for 29.8 s.
9. **Ascend hides its own product.** The end card does not say Ascend, hybrid, online or weekends. 4 of 6 Ascend videos never say Mesa. The proof is borrowed from full-time students. The statics cannot agree on "Online" or "Hybrid", or on 26 or 29 November. The "Software developer story" for a 10-year engineer is also run with a full-time PGP end card.
10. **Overclaiming and negativity.** "Almost 95% of jobs in MNCs are going to be taken away by AI", "graduates that are absolutely useless", "100% going to become irrelevant", "cut almost 50% of the workforce" as a win, "Zero. None." about CAT. The endorser calls the founders "my friends". A famous investor's clip is used with no sign of permission. A calmer, evidenced tone, and answers to what parents and working adults ask first (recognition, cost, time, outcomes), are open ground.
