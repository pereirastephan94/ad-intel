# Cult.fit: what the website sells

Fetched 20 Nov 2026 with curl through the session proxy (and Playwright for two script-only pages). Comparison: research/compare/cult-fit-vs-fitelo/.

## Pages read
- https://www.cult.fit/fitness (200): product menu, current offers, free-trial buttons, FAQ.
- https://www.cult.fit/cult/cultpack/<city>/<pack>/productsId/<id> (200): one page per cultpass ELITE pack and city, with list price, sale price and offer lines. 53 pack pages read for Delhi NCR, Bangalore, Hyderabad, Jaipur, Ahmedabad, Chandigarh Tricity, Surat, Amritsar and Indore (list of URLs: https://www.cult.fit/sitemap/fitness.xml).
- https://www.cult.fit/fitness/cultpass-live (200): cultpass HOME prices.
- https://www.cult.fit/sitemap.xml, /sitemap/center-pages.xml, /sitemap/fitness.xml (200): centre and pack lists.

## Pages that failed (not guessed)
- https://www.cult.fit/ : a script sends the browser to next.cult.fit/home, which this session's proxy refuses. The home page was not read.
- https://www.cult.fit/fitness/cultpass-elite, /fitness/cultpass-pro, /cult/cult-pass: redirect to next.cult.fit (refused).
- Centre pages for the places the ads name (Mall Road Amritsar /3098, Prahlad Nagar /2918, VIP Road Vesu /2950, Cult Neo Gym Kondapur /2834, Impackt Fitness Kondapur /2568) and the listing pages gyms-in-amritsar, gyms-in-chandigarh, gyms-in-indore: all redirect to next.cult.fit (refused).
- https://www.cult.fit/play and https://www.cult.fit/fitness/cult-transform: script-only shells; empty in Playwright too, because the scripts load from hosts this session cannot reach. https://www.cult.fit/fitness/cultpass-play: 404.

## Products (product_key, headline claim quoted from the site)

| Key | Product | Headline price or claim | In the sampled ads |
|---|---|---|---|
| cultpass_elite | cultpass ELITE | FAQ: "unlimited access to cult group classes, gyms and At-home workouts". Packs of 1, 3, 6, 12 and 24 months; offer on /fitness: "FREE ₹1,500 Amazon Pay Gift Card + 1-Month Extension on cultpass ELITE", with an "Ends In" timer. 24-month pack in Bangalore and Hyderabad ₹27,890 (list ₹32,090), which is ₹1,162 a month. | 14 ads (tour, break-up gag, Fitstart barbell card) |
| cult_membership | No product of this name | The ads' "Cult" with "two free group workouts" and no pass named; on the site group classes come with ELITE (unlimited) or PRO (2 a month). /fitness shows "TRY FOR FREE" and "START A FREE TRIAL". | 8 ads ("don't feel like the gym") |
| cultpass_play | cultpass PLAY (sports) | Listed under SPORTS in the menu; the PLAY page did not load (see above). No price read. | 8 ads (Fitstart astronaut card) |
| cultpass_pro | cultpass PRO | FAQ: "unlimited access to gyms and At-home workouts and limited access to cult group classes" (2 sessions a month at cult centres or ELITE gyms). Offer: "FREE 2 Months Extension + Extra ₹1,600 OFF on cultpass PRO". No price read. | none |
| home_workouts | cultpass HOME (LIVE) | "Starting at ₹108 / month*", 24 months ₹2,599; "*Effective Monthly Pricing including Extension, if any"; offer "FREE ₹200 Amazon Pay Gift Card + 3 Months Extension". | none |
| weight_loss_coaching | cult Transform | FAQ: a Transform coach on WhatsApp and calls "to achieve your health goals which include fat loss, weight loss and getting fit", workout plan, nutrition guidance; "this does not include a gym membership". Offer: "FREE ₹1,100 Amazon Pay Gift Card + 1.5 Months Extension on cult TRANSFORM". Page itself did not load; no price read. | none |

Also in the menu: Bootcamp, Transform Plus, Luxury Gyms, a store (redirects to cultsport.com).

## cultpass ELITE, price a month by city (pack price divided by months, pack pages read 20 Nov 2026)

| City (pack page) | 24 months | 12 months | 1 month |
|---|---|---|---|
| Indore | ₹25,560 = ₹1,065 | ₹17,490 = ₹1,458 | ₹4,990 |
| Bangalore | ₹27,890 = ₹1,162 | ₹16,950 = ₹1,412 | ₹7,344 |
| Hyderabad | ₹27,890 = ₹1,162 | ₹16,950 = ₹1,412 | ₹7,344 |
| Surat | ₹28,176 = ₹1,174 | ₹18,490 = ₹1,541 | ₹5,390 |
| Jaipur | ₹28,176 = ₹1,174 | ₹18,490 = ₹1,541 | ₹8,500 |
| Ahmedabad | ₹30,576 = ₹1,274 | ₹19,490 = ₹1,624 | ₹5,590 |
| Amritsar | ₹31,790 = ₹1,325 | ₹20,490 = ₹1,708 | ₹6,990 |
| Delhi NCR | ₹33,050 = ₹1,377 | ₹20,990 = ₹1,749 | ₹8,950 |
| Chandigarh Tricity | ₹1,12,100 = ₹4,671 | ₹52,880 = ₹4,407 | ₹6,850 and ₹6,490 (two packs) |

24-month packs carry "Extra ₹4,200 OFF applied" and "₹1000 Instant Discount with ICICI Credit Card"; 12-month packs "Extra ₹2,500 OFF applied" and the ₹1,500 gift card with a 1-month extension; most packs add "Free Kickstart Onboarding Pack (Two 1:1 Trainer Sessions)".

## How the ads differ from the site
- The Fitstart ELITE card's "₹1,162/month*" (Impackt Fitness Kondapur, Hyderabad) equals the Hyderabad 24-month pack divided by 24. "Starting at" in the ads therefore reads as a 24-month price a month; no ad says so.
- Ad prices by place against the 24-month pack a month on the site: Amritsar ₹1,250 (site ₹1,325); Prahlad Nagar, Ahmedabad ₹1,199 (site ₹1,274); Chandigarh ₹1,291 (site's Chandigarh Tricity packs ₹4,671, so the ad price matches no pack read); VIP Road ₹1,199 (the site's only VIP Road centre is in Surat, ₹1,174). The no-city ₹1,099 matches no pack page read (lowest: Indore ₹1,065). Prices may have moved since the ads started, so these are differences on 20 Nov, not errors proven.
- "Fitstart Days", "Fitstart Sale" and "India's biggest fitness sale" appear on none of the pages read; the site's live offers are gift cards and extensions.
- "Lowest Prices Today" (ad headlines): no comparison or date on the site.
- cult Transform, Cult's weight-loss coaching, is on the site and in none of the 30 sampled ads.
- Legal and claims lines: pack pages say the workouts "are guaranteed to show results"; /fitness shows a 4.8 rating. Formats named: boxing, dance fitness, yoga, Adidas Strength+, Burn, HRX.
- No person is named in any sampled ad; this file names none either.
