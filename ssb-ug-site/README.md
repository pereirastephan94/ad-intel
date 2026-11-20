# SSB UG website

The top-funnel website for Scaler School of Business's **UG programme in Business, Entrepreneurship & AI**. It has five pages:

| Route | Page | Copy source (Google Doc "SSB UG: Website copy") |
| --- | --- | --- |
| `/` | Landing | Pg 1: Highlights (all 11 sections) |
| `/curriculum` | Curriculum | Pg 2: Curriculum |
| `/admission` | Admission & Fees | Pg 3: Admission & Fees |
| `/career-pathways` | Career pathways | Pg 4: Career pathways |
| `/student-life` | Student life | Pg 5: Student life |

The design and images come from the SSB PGP review site (ssb-pages-review.vercel.app).

**Stack:** Next.js 15 (App Router) + Tailwind CSS. Content is stored as **Storyblok blocks**, so marketing can edit every page in Storyblok without code.

## Run it locally

```bash
cd ssb-ug-site
npm install
npm run dev        # http://localhost:3000
npm run build      # production build (type-checks everything)
```

With no environment variables set, the site renders the content bundled in `content/`. That bundled content is the same data that gets pushed to Storyblok.

## How content works

- Each page is a list of blocks (`hero`, `pillars`, `faq`, `table_block`, …).
- `components/bloks/index.tsx` maps each block name to the React component that renders it.
- `content/*.ts` holds the current copy, in Storyblok's exact JSON shape. Sections reused on several pages (internships, campus gallery, closing CTA) live in `content/shared.ts`.
- `lib/storyblok.ts` loads a page from Storyblok when `STORYBLOK_PREVIEW_TOKEN` is set. If Storyblok has no such page, it falls back to `content/`.
- Header, announcement bar, countdown and footer come from the `config` story (`content/index.ts`).
- Any new story created in Storyblok renders at `/<slug>` automatically, via `app/[...slug]`.
- Any CTA link can open the sign-up form, by setting its link to `lead:waitlist`, `lead:brochure` or `lead:info-session`.

## Connect Storyblok

1. In Storyblok, create a personal access token: **My Account → Account settings → Personal access token**. Note the **space ID** (Settings → Space). A separate space for the UG site is recommended, so nothing on other sites changes.
2. Push the block types, images and pages:
   ```bash
   STORYBLOK_PERSONAL_ACCESS_TOKEN=… STORYBLOK_SPACE_ID=… STORYBLOK_REGION=eu npm run storyblok:push -- --publish
   ```
   - Try `--dry-run` first to see what would be sent.
   - It is safe to re-run: blocks and pages are matched by name and slug, and updated in place.
   - It creates 51 block types, uploads about 190 images and 2 videos, and creates 6 stories.
   - `npm run storyblok:schema` writes the block definitions to `storyblok/components.json` for review.
3. In the space's **Settings → Access tokens**, copy the **Preview** token. Set it on the site (locally in `.env.local`, or on Vercel):
   ```
   STORYBLOK_PREVIEW_TOKEN=…
   STORYBLOK_VERSION=draft        # "published" on the live site
   STORYBLOK_REGION=eu
   ```
4. For live preview while editing, set the Visual Editor's preview URL (**Settings → Visual Editor**) to the deployed site, e.g. `https://<your-site>/`. The site loads Storyblok's bridge only inside the editor and refreshes on save.

The official Storyblok MCP server (`https://mcp.labs.storyblok.com/mcp`, with the personal access token as a Bearer header) can also be connected to Claude, to edit content conversationally.

> Note: `storyblok/push.ts` follows Storyblok's Management API docs but has not yet been run against a real space. Run `--dry-run` first, then a real push to a test space.

## Deploy (Vercel)

1. Import the GitHub repo in Vercel and set **Root Directory** to `ssb-ug-site`.
2. Add the environment variables from `.env.example`.
3. Pages are static and refresh from Storyblok every 60 seconds (`revalidate = 60`).

## Leads (waitlist, brochure, info session)

- The form posts to `/api/lead`. The route validates the name, a 10-digit mobile number and the email, then forwards the lead as JSON to `LEAD_WEBHOOK_URL`, with the UTM parameters, the page and the intent.
- For now, point `LEAD_WEBHOOK_URL` at a Google Apps Script that appends rows to a Sheet. Later, point it at Scaler's CRM.
- Without the variable set, leads are accepted but **not stored** (a warning is logged).
- Coming in the next phase: OTP verification of the mobile number, the full application form (with save and resume), and the ₹1,000 application fee with discount codes.

## Content status: needs sign-off before launch

These come straight from the master doc, or were flagged by the SSB UG Chief of Staff review:

- **Claims to verify:**
  - "Professors from Stanford, Oxford, IIM & ISB".
  - "Backed by Sequoia, Tiger Global, Lightrock".
  - "₹5 Cr venture fund" (the curriculum says ₹50,000 seed per team).
  - "500+ hours of applied AI" (the curriculum sheet says 600+).
  - "4+ Winter Treks".
- **Labels:** SST and SSB PGP outcomes (₹44 LPA, ₹20.4L, 3.2x, ₹30.7L) are labelled as such, and the footnote says UG starts in 2027. Keep those labels.
- **Release rights:** there are no release rights on record for some marquee founders and mentors (Anupam Mittal, Shantanu Deshpande, Kunal Shah, Deepinder Goyal). Ashneer Grover is listed in the doc but has no photo, so he is not shown.
- **Placeholders:**
  - The launch video: the campus film is used for now.
  - Testimonial video links: the cards have thumbnails but no videos.
  - The NeoSapiens Shark Tank screenshot: a lab photo is used.
  - Photos for NeoSapiens, Percevia, Trackaroo, Ather Labs, Ninad AI, Krishna, Shruti and Om: these use branded green cards.
  - Two student names are still missing in the doc ("[Name] from Uttar Pradesh" and "[Name] from Telangana").
  - Round 1 dates: shown as "To be announced".
  - The brochure PDF: the brochure button collects details for now.
- **Hero:** uses Option 6 of the 9 headline options in the doc ("Build 4 businesses before you graduate."). Change it in the `hero` block.
