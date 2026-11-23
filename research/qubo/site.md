# Qubo: what the website sells

Fetched 23 Nov 2026 with curl through the session proxy (`curl -sS -L -A "Mozilla/5.0"`), tags stripped in Python. The site is a Shopify store, so each product's `/products/<handle>.js` gave its exact title, price and list price. Comparison: research/compare/atomberg-vs-qubo/.

## Pages read (200 unless noted)
- https://www.quboworld.com/ (home: menu of every product line, "Backed by the Hero Group" block, testimonials)
- https://www.quboworld.com/sitemap.xml and /sitemap_products_1.xml (152 product pages listed)
- https://www.quboworld.com/smart-locks (redirects to /collections/smart-door-locks; landing page of 11 lock ads)
- https://www.quboworld.com/products/smart-door-lock-select-black (landing page of 2 lock ads)
- https://www.quboworld.com/collections/smart-air-purifiers (landing page of 6 purifier ads)
- https://www.quboworld.com/products/q1000-smart-air-purifier (landing page of 2 purifier ads)
- https://www.quboworld.com/products/smart-video-doorbell-pro and /video-door-bell (redirects to /collections/video-doorbells)
- https://www.quboworld.com/smart-cameras (redirects to /collections/smart-security-cameras)
- https://www.quboworld.com/pages/security-bundles
- https://www.quboworld.com/collections/dashcams
- Product JSON: /products/smart-door-lock-select-black.js, smart-door-lock-essential-black.js, smart-door-lock-nova-black.js, ultra-wi-fi-smart-door-lock.js, smart-door-lock-optima.js, smart-door-lock-elite.js, smart-door-lock-prima.js, q1000-smart-air-purifier.js, q200-smart-air-purifier.js, smart-cam-360-3mp.js, smart-bullet-cam-pro-4mp.js, smart-video-doorbell-pro.js, dashcam-3k-f-r-starvis-2.js, dashcam-pro-2k-front-rear.js, dashcam-3-channel.js, ai-guard-pro.js
- https://www.quboworld.com/policies/refund-policy, /policies/terms-of-service

## Pages that failed (not guessed)
- https://www.quboworld.com/pages/about-us: 404.
- Home page counters ("Connected Devices", "App Downloads", "Homes Made Smarter", "Cars Made Safer") are filled in by a script; the served page shows "0+", so no figure was read.

## Products (product_key, headline claim quoted from the site, price on 23 Nov 2026)

| Key | Product | Headline claim (quoted) | Price (list) | In the 42 sampled ads |
|---|---|---|---|---|
| smart_lock | Smart door locks: Optima, Essential, Select, Nova, Ultra Wi-Fi (Elite and Prima listed without a page) | Collection: "Free Installation in 60+ cities", "Trusted by 1,00,000+ LOCK USERS", "Long Battery Life up to 1 Year"; seven ways listed: fingerprint, passcode, access card, mobile app, remote unlocking, one time guest access, mechanical key. Select: "7 Ways to Unlock \| Aluminium Alloy Build \| App Control \| Deadbolt Protection", "2 Year Warranty". Nova: "7 ways to unlock with deadbolt protection and 3-year warranty". Ultra Wi-Fi: "India's most advanced smart lock with inbuilt Wi-Fi, electric mortise, and 8 ways to unlock" | Optima ₹7,990 (₹17,990); Essential ₹9,490; Select ₹13,990 (₹22,990), 4.5 from 704 reviews; Nova ₹15,490; Ultra Wi-Fi ₹19,990 | 13 |
| security_camera | Smart security cameras (Smart Cam 360 3MP, Bullet Cam Pro 4MP and others) and the AI Guard plan | "Built to Protect, Not Just Record"; "India's Smartest Security Cameras"; AI Guard features carry "*Needs an active AI Guard plan. Applies to models manufactured post May 2026" | Smart Cam 360 3MP ₹2,890 (₹3,990); Bullet Cam Pro 4MP ₹3,990 (₹6,990); AI Guard Pro ₹1,490 | 10 |
| air_purifier | Smart air purifiers (Neo, Q200, R250, Q400, Q450, Q500, Q600, R700, Q1000, Q1000 Ultra) | Q1000: "smart air purifier with 1000 sq. ft. coverage area and 600 m3/h CADR", "1 Year Warranty". Q200: "200 sq. ft. coverage area and 150 m3/h CADR" | Q1000 ₹19,990 (₹29,990); Q200 ₹6,990 (₹12,990) | 9 |
| dashcam | Dashcams (Pro 2K F+R, Pro 3K F+R, 3-Channel Trio, 4K and others) | "Qubo - India's #1 Brand of Dashcams" on the collection, no source or year | Pro 2K F+R ₹6,990 (₹13,990); Pro 3K F+R ₹12,990 (₹21,990); 3-Channel Trio ₹10,990 (₹19,990) | 6 |
| video_doorbell | Smart Wi-Fi Video Doorbell Pro 2K | "2K resolution doorbell with instant video calls, person detection and remote app control"; doorbell collection: "Free Home Installation in 70+ cities"; "1 Year Warranty"; 4.5 (704 reviews) | ₹8,990 (₹14,990) | 3 |
| security_bundle | Security bundles (cameras, doorbell, AI Guard plan) | "Every bundle below already includes an" AI Guard plan; "Choose the number of cameras to see your savings with AI Guard" | not read per bundle | 1 |

Site only, in no sampled ad: smart bulbs and plugs, tyre pressure inflators and jump starters, car air purifiers, GPS trackers for bike, car and luggage, a bike cam, DashPlay in-car screens, magnetic power banks, a baby camera, a wireless door phone (InstaView) and combos of these.

## Results and scale claims on the site
- "Trusted by 1,00,000+ LOCK USERS" (lock collection).
- "Qubo - India's #1 Brand of Dashcams" (dashcam collection), no source.
- Select lock and Video Doorbell Pro: 4.5 from 704 reviews each, as served.
- Home: "Backed by the Hero Group", "Join us as we build India's biggest smart devices company" (an aim, not a claim of size).

## Terms and legal lines
- Refund policy: "we do not accept returns unless you have received a defective or incorrect product".
- Lock installation: free in "60+ cities" (lock collection, with a city list by state); doorbell installation free in "70+ cities" (doorbell collection).
- Warranties as listed: Select lock 2 years, Nova lock 3 years, Q1000 and Video Doorbell Pro 1 year.
- AI Guard features need a paid plan ("*Needs an active AI Guard plan"); AI Guard Pro ₹1,490.

## How the ads differ from the site
- **Lock warranty**: catalogue cards say "3 Years Warranty" (2 ads) and "2+ Years Warranty" (2 ads) for the same lock range; the site gives 2 years for the Select (the page two lock ads land on) and 3 years for the Nova.
- **Lock price**: the "Starting @ ₹7,990" card equals the Optima's price, the cheapest lock listed; its link description names the Select Black, which is ₹13,990.
- **Installation cities**: the doorbell ads' "Free installation in 70+ cities" matches the doorbell collection; the lock collection says 60+ cities. No lock ad names a city count.
- **"7 ways to unlock"**: the site lists the seven; the ads never list them.
- **Doorbell price**: one ad's link description says "lowest Price - INR 5990/-"; the product page lists ₹8,990 on 23 Nov. Prices may have moved since the ad started (22 Sep 2026), so this is a difference on 23 Nov, not an error proven.
- **Dashcam price**: one ad's text gives ₹6,490 as a "Limited-Time Deal" for the Pro 2K front and rear; the product page lists ₹6,990.
- **Q1000 price**: the ad says 19,900 aloud; the product page lists ₹19,990. Its "600 metre cube per hour" and "1000 sq ft" match the site.
- **AI Guard "free"**: one ad's voice says AI Guard is built in free in all Qubo cameras; the cameras page says its features need an active AI Guard plan, and AI Guard Pro is sold at ₹1,490.
- **"India's #1 brand of dashcams"**: the same unsourced line is on the dashcam collection and on all six dashcam ads.
- **Brand placeholder**: 11 catalogue ads show unfilled `{{product.brand}}` text and "by Hero Group" headlines; the site says Qubo is "Backed by the Hero Group".
