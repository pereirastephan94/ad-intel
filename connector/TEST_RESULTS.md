# Test results – 18 Nov 2026

Run in a cloud container (logged out of Facebook, country IN). The server ran locally and a test
script (`test/client.ts`) called it over MCP exactly as Claude would. Mesa School of Business,
page ID 115513081449393. 3 videos, to save usage.

## Result: it works

| Step | Result | Time |
|---|---|---|
| Connect, list tools and prompts | `find_advertiser`, `list_ads`, `analyze_video` and the `audit` prompt all present | – |
| `find_advertiser("Mesa School of Business")` | 2 pages: Mesa School of Business (115513081449393) and Mesa School of Business – Forge (1135602339626863). An earlier probe also showed "Mesa School of Business – UG" (541696572356195). | 8 s |
| `list_ads(115513081449393)` | 30 ads: 20 video, 6 dynamic (DCO), 4 image. The Library reports 289 active ads in total. All fields filled (ID, start date, days running, text, headline, CTA, landing URL, video, thumbnail, copies). | 6–7 s |
| `analyze_video` ×3 | All 3 OK: 12 stills each (opening frames, scene changes, end card) and a timestamped English transcript | 21 s, 8 s, 7 s |
| Wrong secret in the URL | Refused (HTTP 401) | – |

A second short run (1 video) after a memory fix gave the same result.

### What came back (sample)
- **Ad 40210023251944395** (58.7 s, 16 days running): presenter in a pink shirt; on-screen captions "Mesa alumni see a **50-60%** increase in salaries one year…", a student with a microphone, a classroom shot, black end card "PGP in Startup Leadership & Entrepreneurship – Apply Now".
  Transcript starts: "Messa alumni see a 50 to 60 percent increase in salaries…" (Whisper misspells "Mesa"; the stills fix it).
- **Ads 1133899169019919 and 2199957264231150** (38.2 s): the same video under two IDs (the second has 7 copies). Presenter in a maroon shirt; caption "**200 Special Students**"; same end card. Transcript: "We are looking for 200 special people to be a part of the fifth cohort here at NASA [Mesa]…"

## Known limits seen in the test
1. **Only the first 30 ads.** Facebook answered "Rate limit exceeded" as soon as the page asked for more, every time. The tool stops and says so. 289 ads exist.
2. **"Days running" is short (≤16 days)** for these 30 because Facebook shows the highest-impression ads first, not the oldest.
3. **Rough ad counts in `find_advertiser` are often "unknown"**: the filter request that gives them was not always sent. The page list itself was right.
4. **Landing URLs keep Facebook's placeholders** such as `{{site_source_name}}`; that is how Facebook stores them.
5. **Regional video hosts:** downloads from `video-dfw5-…xx.fbcdn.net` were refused here, and the automatic switch to `video.xx.fbcdn.net` worked.
6. **Only English tested.** Hindi and Hinglish are not tested yet.
7. **The Docker image was not built here** (this container cannot reach the PyTorch download site). It uses standard parts, but the first build on the host is its first real test.

## Memory (decides the host size)
- Whisper `base`: about 1.05 GB peak; `tiny`: about 0.9 GB (most of it is PyTorch itself). Both take about 8 s for a 60 s video on 4 CPUs.
- Chromium: about 0.4 GB. The server closes the browser before each Whisper run, so they never overlap.
- **A 2 GB machine is needed. 512 MB plans will crash.**
