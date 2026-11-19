# Stable Money: concepts

33 ads (30 video, 3 image) fall into 24 concepts. Counts are ads in ads.json whose `video_asset` equals the asset id (image ads count 1 each). A concept's count is the sum over its assets. Rules: same footage in another shape, length or end card is one concept; the same script performed by a different person is a new concept (linked by `script_twin`).

| Concept | Short name | Row | Assets or library ids | Ads | Idea |
|---|---|---|---|---|---|
| SM-c01 | Boring FD beat the stocks | V1 | 1061581183380693 | 1 | A presenter says influencers mocked FD, yet the boring FD beat the market, and sells 8.5% FDs. |
| SM-c02 | Nani Tuitions | V2 | 1113897927910622, 2183485612579648 | 2 | A grandmother is taught to book an FD in the app, asks if it is safe, and learns about 8.5% and the 5 lakh cover. |
| SM-c03 | Podcast: small finance banks | V2 | 1164032119285655 | 1 | Two people on a podcast set say small finance banks are RBI regulated and pay up to 8.5% against 5-6%. |
| SM-c04 | Papa Explaining: monthly payout FD | V2 | 1199052999315565, 966609952841691 | 2 | A son asks why money lands in his account every month; Papa explains monthly payout FDs. |
| SM-c05 | SIP for goals, monthly RD | V1 | 1371387538214253, 2933453097006450 | 3 | A creator-style presenter asks about retirement SIPs, then sells a monthly RD as an SIP for short-term goals at up to 8.5%. |
| SM-c06 | Video-call lounge skit | V2 | 1402156101838563 | 1 | Two friends on a video call before a flight; one eats free at the lounge with a card from an FD. |
| SM-c07 | Couple: 4.5 lakh in savings | V2 | 1419759219573556 | 1 | Two people at home compare 2.5% on savings with 8.5% on an FD, then point to DICGC cover. |
| SM-c08 | Desk presenter: lounge cards fail | V1 | 1444888800891750, 935043619677161 | 2 | A man at a desk says lounge cards need big spends, then pitches a lifetime-free FD-backed card with 8 free visits. |
| SM-c09 | Mic presenter: the card that earns | V1 | 1472636994553170 | 1 | A presenter with a mic pitches a lifetime-free card from an FD that earns interest and gives 8 lounge visits. |
| SM-c10 | Couple's row, then bonds man | V1 | 1752268299241939 | 3 | A couple argue over idle money, then a man to camera pitches Stable Money bonds at 9 to 12%. |
| SM-c11 | Tree-planting bonds | V1 | 1760917031791377 | 1 | A man plants a tree while telling viewers with idle money to buy bonds at 9 to 12% fixed returns. |
| SM-c12 | Hoodie man: idle money to bonds | V1 | 1768509427669435 | 2 | Same idle-money bonds script as c10, delivered by a different man to camera in a purple-lit room. |
| SM-c13 | Papa Explaining: market fear, 8.3% FDs | V2 | 17861189070656308 | 1 | A son worried by the share market asks Papa about 1 lakh in savings; told FDs pay up to 8.3%. |
| SM-c14 | Papa Explaining: bonds | V2 | 17868682956656308 | 2 | A son asks Papa about money landing in his account; Papa explains bonds, 9 to 12% and a Rs 1,000 start. |
| SM-c15 | Bookshop street interview | V2 | 1911598616485842 | 1 | A man interviews a woman who says the FD-backed card gives 8 free lounge visits with no minimum spend. |
| SM-c16 | Papa Explaining: car SIP to RD | V2 | 2086076648968459 | 1 | A dad tells his son to stop a car-fund SIP and use a monthly RD for safe, fixed returns. |
| SM-c17 | Street interview, then 8,500 on 1 lakh | V2 | 2194829677911441 | 1 | Street interviews on savings balances, then a presenter says an FD pays up to 8,500 rupees on 1 lakh. |
| SM-c18 | 30% less interest, matrimony | V1 | 2255487748522741 | 1 | A presenter says your FD earns 30% less than the best 8.5% and switching is as easy as matrimony. |
| SM-c19 | Cafe presenter: FD gives lounge access | V1 | 4463581000622798 | 1 | A woman at a cafe table says an FD can bring a lifetime-free card with 8 free lounge visits. |
| SM-c20 | Savings over 50,000 costs you | V1 | 922795270702177 | 1 | A woman says savings pay 2-3% and own-bank FDs 5-6%, so compare FDs on Stable Money for up to 8.5%. |
| SM-c21 | Showroom friends: car paid by RD | V2 | 996386489755150 | 1 | Two friends outside a car showroom; one paid for his car with an RD that works like an SIP. |
| SM-c22 | Static: 8 free lounge access | I1 | 1022650000551778 | 1 | Cream card, woman on a lounge sofa, "8 Free Airport Lounge Access" with cashback and FD rate stats. |
| SM-c23 | Static: lounge scene in card frame | I2 | 2077379136540472 | 1 | Woman laughing in a lounge chair inside a card-shaped frame, stat row below, no headline. |
| SM-c24 | Static: 8.10% FD-backed card | I1 | 948406311403969 | 1 | Dark card with a hand holding the purple card: "Earn 8.10% p.a. on FD-backed credit card" and 10 free lounge visits. |

## Series and recurring devices

- **Papa Explaining** (title card or caption, and "Explained by Papa" in ad text): c04, c13, c14, c16. Six ads in all (2 + 1 + 2 + 1). The son opens with "Papa, ..." every time; same cast, product swapped between FD, bonds and RD. c04 and c14 share the opening line about the bank statement.
- **Nani Tuitions** ("How To Book FD Online"): c02, two ads. The only series with a title card on a bed set.
- **Same script, different performer**: the idle-money bonds script ("account mein idle paisa... bonds on Stable Money") appears as c10 (after a skit, man in black tee) and c12 (man in maroon hoodie). Linked by script_twin. c11 is a different script on the same idea.
- **Same footage, different shape**: c02, c04, c05 and c08 each run in two shapes or lengths (square with bars, vertical, landscape). c08 stills are byte-identical.
- **Skit then explainer**: c10 opens with a couple's row; c17 opens with street interviews, then a presenter takes over.
- **SIP analogy for RD or FD**: c05, c16, c21 all explain the monthly RD as the fixed-deposit version of an SIP. c16 and c21 also both use a car purchase.
- **Savings versus FD rate comparison**: c03, c07, c13, c17, c20 all pit 2-3% (or 5-6% at the customer's own bank) against up to 8.5%.
- **FD-backed credit card with lounge access** is the largest run: five videos (c06, c08, c09, c15, c19) and three statics, all built around "8 free lounge visits".
- **SEBI strip**: the "OBPP Name: Stable Broking Private Limited | SEBI Registration No: INZ000314637" line runs along the bottom of the bond videos (c10, c11, c12).
- **End-card social proof**: "50L+ Users", "7,000+ Crore", "3500+ Cities" on the FD end cards.
- **Dynamic creative with unfilled ad text**: 10 ads (7 video, 3 image) show `{{product.name}}` and `{{product.brand}}` as headline and body; tagged from the creative alone.
- **Shared ad copy**: 9 ads carry the identical "Earn Up to 8.5% p.a. on FD" headline and body over different videos.

## Numbers that disagree across ads

- **Users**: "50 lakh" (speech or end card "50L+ Users" in 1061581183380693, 1164032119285655, 1371387538214253, 1419759219573556, 2255487748522741, 2933453097006450) against "60 lakh" (spoken in 1164032119285655 and 922795270702177, and "60 Lakh+ Customers" on the end card of 2183485612579648). 1164032119285655 says 60 lakh in speech and 50L+ on its end card.
- **Money invested**: "7,000+ Crore" (end cards and speech in 1061581183380693, 1371387538214253, 1419759219573556, 2255487748522741, 2933453097006450, 996386489755150) against "11,000 Cr" spoken in 1113897927910622 and 2183485612579648. The 2183485612579648 end card itself says "7000 Cr+".
- **Lounge visits**: "8 free" in 1444888800891750, 935043619677161, 1472636994553170, 4463581000622798, 1911598616485842, 1402156101838563 and static 1022650000551778, but "10 free airport lounge" in static 948406311403969.
- **FD rate behind the card**: "up to 8.10%" in the statics, 1402156101838563 and 1472636994553170; "8.5%" in 1444888800891750 and 935043619677161; "8%" spoken in 4463581000622798.
- **Top FD rate**: "up to 8.5%" in most FD ads against "up to 8.3%" in 17861189070656308.
- **RD return**: "7-8%" in 996386489755150 against "up to 8.5%" in 1371387538214253, 2933453097006450 and 2086076648968459.
- **Bonds**: headline "9 to 12%" (c10, c11, c12, c14), but the app screen in 17868682956656308 shows examples at 8.00% to 9.75% YTM, below the range.
- **"More return" maths**: 1164032119285655 and 922795270702177 say "30-40% more" for 8.5% against 5-6%, which is 42-70% more; 2255487748522741 says "30% less".
- **FD return claim**: 1061581183380693 says the FD gave 1.5% a year while selling 8.5% FDs.
- **Market return in skit**: 2086076648968459 has the son expecting "12-13%" from the market against the RD's 8.5%.

## Products advertised

| Product | Ads | Concepts |
|---|---|---|
| Fixed deposits (FD marketplace, monthly payout, small finance banks) | 11 | c01, c02, c03, c04, c07, c13, c17, c18, c20 |
| FD-backed credit card (lounge access) | 9 | c06, c08, c09, c15, c19, c22, c23, c24 |
| Bonds (9 to 12% fixed returns) | 8 | c10, c11, c12, c14 |
| Recurring deposit (RD) | 5 | c05, c16, c21 |
