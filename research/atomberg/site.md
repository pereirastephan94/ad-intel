# Atomberg: what the website sells

Fetched 23 Nov 2026 with curl through the session proxy (`curl -sS -L -A "Mozilla/5.0"`), tags stripped in Python. The site is a Shopify store, so each product's `/products/<handle>.js` gave its exact title, price and list price. Comparison: research/compare/atomberg-vs-qubo/.

## Pages read (all 200)
- https://atomberg.com/ (home: menu, product tiles with prices, price-match terms, return, COD and genuine-product blocks)
- https://atomberg.com/sitemap.xml and https://atomberg.com/sitemap_products_1.xml (59 product pages listed)
- https://atomberg.com/smart-lock-sl-1 (redirects to /products/atomberg-smart-lock-key-free-locks-care-free-lifestyle; the SL 1 page, landing page of both lock ads)
- https://atomberg.com/collections/smart-locks (three locks)
- https://atomberg.com/intellon-waterpurifier (redirects to /products/intellon-waterpurifier; landing page of 9 Intellon ads)
- https://atomberg.com/atomberg-zenova-mixer-grinder-with-coarse-mode (redirects to the product page; landing page of 8 mixer ads)
- https://atomberg.com/atomberg-ceiling-fans and /collections/atomberg-ceiling-fans (same page)
- https://atomberg.com/pedestal-fans (redirects to /collections/pedestal-fans)
- https://atomberg.com/exhaust-fans (redirects to /collections/exhaust-fans)
- https://atomberg.com/renesa-table-fan (redirects to /products/renesa-table-fan; landing page of one pedestal fan ad)
- Product JSON: /products/atomberg-smart-lock-key-free-locks-care-free-lifestyle.js, atomberg-azhero-smart-door-lock.js, atomberg-cypheo-elite-smart-door-lock.js, intellon-waterpurifier.js, atomberg-zenova-mixer-grinder-with-coarse-mode.js, aris-contour-ceiling-fan.js, erica-signature-ceiling-fan.js, atomberg-renesa-halo-bldc-motor-3-blade-ceiling-fan.js, atomberg-pedestal-fan-renesa-bldc-motor-energy-saving-pedestal-fan-400mm-with-remote-control.js, atomberg-studio-exhaust-fan-with-bldc-motor.js, renesa-table-fan.js
- https://atomberg.com/policies/refund-policy, /policies/terms-of-service, /pages/about-us (the about page holds only the menu as plain text)

## Pages that failed (not guessed)
- https://www.atomberg.com/ and https://www.atomberg.com/sitemap.xml: refused by this session's proxy (403, host not allowed). The bare host atomberg.com is allowed and serves the same store; every page above was read there.
- The Amazon.in listing that the one image ad links to (amazon.in/Atomberg-Intellon-Alkaliser-TDS-Based-Filtration/dp/B0F6CXR97M) was not read.

## Products (product_key, headline claim quoted from the site, price on 23 Nov 2026)

| Key | Product | Headline claim (quoted) | Price (list) | In the 30 sampled ads |
|---|---|---|---|---|
| smart_lock | SL 1 Smart Lock | "Atomberg SL 1 Smart Door Lock \| 6 Ways Unlocking \| Fingerprint \| PIN \| Remote OTP \| NFC Card \| Atomberg Home App (Data Stored in India) \| Key \| 5 Stainless Steel Bolt \| 2 Year Warranty" | ₹14,999 (₹25,000); "Starting from ₹1,250/Month" no cost EMI | 2 |
| smart_lock (site only) | Azhero Smart Door Lock | listed in the smart-locks collection | ₹10,499 (₹18,500) | 0 |
| smart_lock (site only) | Cypheo Elite Smart Door Lock | listed in the smart-locks collection | ₹29,999 (₹50,000) | 0 |
| water_purifier | Intellon Water Purifier | "Atomberg Intellon - India's 1st Adaptive Water Purifier* \| RO+UF+UV+Alkaliser \| ... \| 2 Year Warranty \| Lowest Cost of Ownership * For Home & Domestic Category" | ₹18,999 (₹27,999) | 10 |
| mixer_grinder | Zenova Mixer Grinder | "Unique Coarse Mode for Silbatta-like Texture \| Intelligent BLDC Motor \| Safety Features \| 4 Jars including Chopper \| Hands-Free Operation \| 2+1* Year Warranty" | ₹7,399 (₹11,999); brass and copper trims ₹8,099 | 8 |
| ceiling_fan | BLDC ceiling fans (Aris Contour, Renesa Halo, Erica Signature and others) | "Save Up to 65% on Electricity with Atomberg's BLDC Ceiling Fans"; Renesa Halo: "Value For Money-Saves Up To ₹ 1500/Year" | Aris Contour ₹7,099 (₹12,300); Renesa Halo from ₹4,099; Erica Signature ₹3,849 | 6 |
| pedestal_fan | Renesa Pedestal Fan | "Our BLDC pedestal fans consume up to 65% less energy compared to regular fans"; "35W BLDC motor, 1500 RPM speed, and remote control with oscillation and timer modes" | ₹3,699 (₹6,700) | 3 |
| exhaust_fan | Studio Exhaust Fan | "Say goodbye to fumes and odours with our BLDC exhaust fans!" | ₹1,799 (₹3,300) | 1 |

Site only, in no sampled ad: wall fans, table fans (Renesa Table Fan ₹3,149), a personal fan, the Althea cold press juicer, Zenova Fresh juicer mixer grinder, Zenova Flex blender, Yulia and Tavi mixer grinders, a nutri blender, a hand blender and jars, and the Azhero and Cypheo Elite locks.

## Results and scale claims on the site
- Top banner: "1 Cr + People Trust Atomberg Fans". The fan collection pages say "25 Lakhs+ customers bought Atomberg fans"; the home page says "25 Lakhs+ customers bought Atomberg ceiling fans". Two scale figures for one customer base, unsourced.
- Ratings on tiles: SL 1 4.6 (437 reviews); Azhero 4.4 (541).
- Intellon page: "8-Year Total Cost of Ownership"; "Up to ₹25,000 in 8 years" saving against other ROs whose cost "Can go up to ~₹30,000–₹35,000 over 8 years"; "Zero Wastage in Adaptive Mode with municipal water".

## Terms and legal lines
- Price Match Guarantee against Amazon.in and Flipkart within 24 hours of purchase; "our only authorized sellers online are Amazon.in & Flipkart".
- "10 Days Return / No Questions Asked" block on the home and product pages. The refund policy page says the opposite: "Once purchased, Atomberg Technologies Limited ... does not accept the return of the product", except damaged or defective goods reported within 10 days.
- Intellon: 2-year "No Service Cost" warranty covering "All filters, membranes, and electrical components in case of a defect" and "Any service or technician visit charges for the first 2 years", provided installation and servicing are by the authorised team; "the first installation is free of cost". The same "No Service Cost" warranty block also shows on the SL 1 lock page, where filters and membranes do not apply.
- SL 1: "Free installation is available in select pincodes"; "Restricted access for 1 minute after 5 false PIN attempts"; "App to Cloud Communication: Data encrypted using AES256"; battery 4x AA.
- Zenova: "3-year warranty on the product (including a 1-year additional warranty upon registration)".
- COD on orders up to ₹20,000; 5% upfront from ₹5,001.

## How the ads differ from the site
- **No price in any ad**, while every product page leads with a sale price against a list price and an EMI a month (SL 1 "₹1,250/Month"). The only money figures in the ads are savings.
- **SL 1 unlocking ways**: the site and both lock ads' text say 6 (fingerprint, PIN, remote OTP, NFC card, app, key). The box in the ad shows five icons and the voice names four. "End-to-end data encryption" (collection page and ad text) is not spoken; the voice says only that data is stored in India, as the product title does.
- **Lock installation and price**: the site offers free installation in select pincodes and EMI; neither lock ad says either.
- **Intellon**: the site's "2-year No Service Cost warranty" and "Up to ₹25,000 in 8 years" match two ads (1100991832415673 says about 25,000 rupees over 8 years). The ads' other promises, "2-year unconditional warranty", "zero maintenance", "No AMC" and the static's "Save up to ₹13,000*", are not stated on the product page in those words; ₹13,000 appears nowhere on the pages read.
- **"India's 1st Adaptive Water Purifier*"** carries an asterisk on the site ("For Home & Domestic Category"); the ads that say "India's 1st Adaptive" carry no qualifier.
- **Fan saving**: the site says up to 65% less energy and, for the Renesa Halo, up to ₹1,500 a year. Ads say ₹1,500 "every season", "per year" or no period, and the pedestal fan's ₹400 a summer or season appears on no page read.
- **Zenova**: "India's first BLDC Mixer Grinder" (ad text of five ads) is not on the product page read; "Ventless Body" is.
- **Scale**: no ad uses "1 Cr+" or "25 Lakhs+"; one ad shows "1 crore+" printed on a fan box.
