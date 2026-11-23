"""Writes research/compare/scaler-school-of-business-vs-mesa/perspectives.json (v4 schema: plan + scripts, shared product).

Usage: python3 make_persp.py <out perspectives.json>
A = Scaler School of Business (SSB, the owner's school, primary reader), B = Mesa School of Business.
Focus product: the full-time PGP on both sides (SSB's PGP in Management & Tech against Mesa's PGP in Startup Leadership).
Every figure was checked against comparison.json, research/<brand>/concepts.md, extras.json, series.json or site.md
(see COMPARE_RUNBOOK.md step 6). SSB scripts follow SSB's own script rules (7 beats, a number every 25 to 31 words,
named companies, operators as faculty, a call to action with seats, deadline and scholarships, never "MBAs are broken").
Anything neither brand's ads nor site state is a [placeholder].
"""
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
HERE = Path(__file__).resolve().parent
COMP = json.loads((HERE / "comparison.json").read_text())


def ids(k, idea):
    return [l for l, a in COMP["ads"].items() if a["brand"] == k and a["tags"].get("concept_id") == idea]


C10, C09, C11, C01, C04, C07, C06S = (ids("A", x) for x in ("SSB-c10", "SSB-c09", "SSB-c11", "SSB-c01", "SSB-c04", "SSB-c07", "SSB-c06"))
M23, M19, M11, M10, M06, M09, M08 = (ids("B", x) for x in ("MS-c23", "MS-c19", "MS-c11", "MS-c10", "MS-c06", "MS-c09", "MS-c08"))
EARLY = ["954275137769376", "1123141853818596", "1406583844890391", "4572207989702796"]

# ---------------------------------------------------------------- compliance and measures
COMPLIANCE_SSB = [
    "Call it the PGP in Management & Tech, a certificate programme. Never \"MBA\", \"degree\" or \"MBA students\": SSB's site says it is not a university and does not confer degrees.",
    "Every CTC or placement figure carries its cohort and source on screen (\"19 LPA avg. CTC, Cohort 1\", \"23 LPA current avg. CTC, Cohort 2\"). Scaler's online figures (5,000+ placed, 19 lakh median) are labelled as Scaler's online programmes, never as SSB's.",
    "Scholarships are \"up to 100%\", with \"awarded at the discretion of the Scaler Impact Foundation\" on the end card.",
    "One live deadline: the one on the admission page on the day of the edit (29 Nov 2026 on 22 Nov). Take a dated card down the day after it passes.",
    "No \"India's only\" or \"India's first\" without a source on screen; pick one tagline for all ads.",
    "Name every speaker with a role on screen; get written consent from students and from named companies (Mokobara, Zomato, Razorpay) before they appear.",
    "No unsourced figures about other schools or their graduates (\"one in four unemployable\").",
]
COMPLIANCE_MESA = [
    "Each outcome figure once, defined, with its cohort: the site's 26L average CTC and 2.8X, not \"upwards of 25 lakhs\" in one ad and \"50 to 60%\" in another.",
    "One count per claim in every ad: partner startups (100, 150 or 500), founders (100 or 200), the khakra brand (20 or 25 lakh a month).",
    "Seats as the site states them (175 for the full-time PGP), not \"200 people\".",
    "Ascend and the PGP are not university degrees (Mesa's own FAQ); say PGP, never MBA.",
    "Any fee shown is \"exclusive of 18% GST\", as the site says.",
    "Name speakers on screen; an outside investor's endorsement needs his written consent and a label.",
]
MEASURE_SSB = [
    "Hold to 3 seconds and to 15 seconds against the square \"By month 3\" cut (your highest-scoring idea)",
    "Form fills on the minimal landing page (all 30 sampled ads go there) and cost per form",
    "Applications with the fee paid within 14 days of the form",
    "Comments asking \"is it an MBA?\" or \"what is the fee?\", a sign of what the ad left unclear",
]
MEASURE_MESA = [
    "Hold to 3 seconds and to 15 seconds against the square cohort call (your 9-ad control)",
    "Applications started on the PGP page, and MAT bookings",
    "Interview slots booked (the ₹1,500 step) within 14 days",
    "Comments that question a figure (\"which cohort?\", \"100 or 500?\")",
]


def seven(t_rows):
    """Beats from the script rows, with SSB's beat names."""
    names = ["Handoff", "Problem", "Bridge", "Product specs", "Experiential proof", "Credibility stack", "Call to action"]
    return [{"t": r["t"], "beat": n, "note": r.get("note", "")} for n, r in zip(names, t_rows)]


# ---------------------------------------------------------------- scripts: SSB (A)
A_SCRIPTS = []

rows = [
    {"t": "0-3 s", "voice": "Scaler School of Business. Our first cohort's average CTC: 19 LPA.",
     "screen": "Big text \"19 LPA avg. CTC, Cohort 1\" with \"Source: [SSB placement report]\". Lower-third: [speaker name], [role], SSB.",
     "note": "Brand and the strongest proof in the first line; the figure with its cohort."},
    {"t": "3-12 s", "voice": "Every recruiter asks the same question. Not where you studied. What have you actually built, sold or shipped? Most graduates have read about business. Few have done it.",
     "screen": "Caption: \"What have you actually built?\"",
     "note": "The problem, without running down the MBA."},
    {"t": "12-15 s", "voice": "At SSB, you build from week one.", "screen": "Cut to students at a market stall.",
     "note": "One-line pivot."},
    {"t": "15-22 s", "voice": "18 months, full time, on our Bengaluru campus. Taught by CEOs, CMOs and product heads, with mentors from Zomato and Razorpay.",
     "screen": "Text: \"18 months | Full time | Bengaluru\".",
     "note": "Format, length, place, operators who built companies."},
    {"t": "22-31 s", "voice": "You run a live D2C brand with a ₹5 lakh revenue target in 6 weeks, and build go-to-market plans for brands like Mokobara, presented to the founders.",
     "screen": "Real footage of the D2C stall and the Mokobara session; caption \"₹5L+ target in 6 weeks\".",
     "note": "Named company project, set up first."},
    {"t": "31-38 s", "voice": "Scaler has been in education since 2016, with 1,200+ hiring partners. And Cohort 2's current average CTC? 23 LPA.",
     "screen": "Text: \"1,200+ hiring partners\" / \"23 LPA current avg. CTC, Cohort 2\" with its source.",
     "note": "Tenure, distribution, second cohort outcome."},
    {"t": "38-45 s", "voice": "[Seats] seats. Applications close [next deadline]. Scholarships up to 100%. Apply now, link below.",
     "screen": "End card: \"PGP in Management & Tech\", [seats] seats, \"Apply by [next deadline]\", \"Scholarships up to 100%*\".",
     "note": "Scarcity, deadline, incentive, one action."},
]
A_SCRIPTS.append({
    "title": "Proof first: open on one cohort's average CTC, with its source on screen",
    "persona": "22 to 27, a graduate or 1 to 3 years into a job, weighing an MBA, who wants proof of placement before anything else.",
    "why": "Mesa states a graduate outcome in 30 of its 93 PGP ads (100% placements, a 25 lakh average, 58%, 2.8x, named alumni roles). None of your 30 ads gives a placement or salary figure, though your site lists 19 and 23 LPA by cohort.",
    "evidence_ads": ["1488536809855650", "1498875895417529", "1615063316971151", C10[0]],
    "format": "Programme or careers lead to camera, vertical, phone or one-camera set, cut to real campus footage for the proof beat",
    "length": "45 seconds",
    "language": "English",
    "openings": [
        "Scaler School of Business. Our first cohort's average CTC: 19 LPA.",
        "Cohort 1 averaged 19 LPA. Cohort 2 is at 23. Here's what they did.",
        "40 placements and 5 founders, from our very first batch.",
    ],
    "beats": seven(rows), "script": rows,
    "on_screen": "Every figure on screen with its cohort and source line; the speaker's name and role from the first second. No MBA comparison.",
    "end_card": "SSB logo, \"PGP in Management & Tech\", \"18-Month | Full-Time | Bangalore Campus\", [seats] seats, \"Apply by [next deadline]\", \"Scholarships up to 100%*\", \"*At the discretion of the Scaler Impact Foundation. Certificate programme.\"",
})

rows = [
    {"t": "0-3 s", "voice": "Scaler School of Business is picking its next [seats] students. Here's who we want.",
     "screen": "Caption: \"[Seats] seats. PGP in Management & Tech.\" Lower-third: [name], [admissions role], SSB.",
     "note": "Brand and scarcity at once."},
    {"t": "3-12 s", "voice": "Not the best marks. People who've sold something, built something or run a side hustle. Admission is a profile review and 2 interviews with industry leaders, with a case.",
     "screen": "Captions: \"Sold something?\" / \"Built something?\" / \"2 interviews, 1 case\".",
     "note": "Who it is for, and how they are picked."},
    {"t": "12-15 s", "voice": "Because the PGP is built for doers.", "screen": "Cut to a pitch in a classroom.",
     "note": "Pivot."},
    {"t": "15-22 s", "voice": "18 months, full time, in Bengaluru, with a mandatory internship and 100+ industry leaders who teach.",
     "screen": "Text: \"18 months | Internship built in | 100+ industry leaders\".",
     "note": "Specs and who teaches."},
    {"t": "22-31 s", "voice": "Term 1, you're on Bangalore streets selling to real customers. By graduation, you've shipped 3 AI products and 10+ real company projects.",
     "screen": "Street-selling footage; caption \"3 AI products | 10+ company projects\".",
     "note": "What students do."},
    {"t": "31-38 s", "voice": "Scaler has over a decade in education and 1,200+ hiring partners.",
     "screen": "Text: \"Since 2016\" / \"1,200+ hiring partners\".",
     "note": "Tenure and distribution."},
    {"t": "38-45 s", "voice": "[Seats] seats. Apply by [next deadline]. Apply early: it raises your chance at a scholarship of up to 100%.",
     "screen": "End card with the date and \"Scholarships up to 100%*\".",
     "note": "Seats, deadline, scholarship, said aloud."},
]
A_SCRIPTS.append({
    "title": "The cohort call: seats, one date and scholarships, said aloud",
    "persona": "Someone who already knows SSB and Mesa and is deciding where to apply this month; needs a reason to apply now.",
    "why": "Mesa's highest-scoring PGP idea is a 38-second cohort call: 9 ads, 16 versions, \"200 special people\" for the fifth cohort. None of your 30 ads names a scholarship; \"the next 100 students\" is said only in the timeline film, and the only date shown has passed.",
    "evidence_ads": [M23[0], M23[1], EARLY[0]],
    "format": "Admissions lead to camera, one room, two angles, captions on, vertical and square",
    "length": "45 seconds",
    "language": "English",
    "openings": [
        "Scaler School of Business is picking its next [seats] students. Here's who we want.",
        "[Seats] seats. One deadline: [next deadline]. Here's how to get one.",
        "No CAT score. 2 interviews. [Seats] seats. That's SSB admissions.",
    ],
    "beats": seven(rows), "script": rows,
    "on_screen": "The seat count only if admissions confirm it; the deadline from the admission page on the day of the edit.",
    "end_card": "\"PGP in Management & Tech\", [seats] seats, \"Apply by [next deadline]\", \"Scholarships up to 100%*\", Apply now.",
})

rows = [
    {"t": "0-3 s", "voice": "Day one at Scaler School of Business: you're on the streets of Bangalore, selling.",
     "screen": "Caption: \"Day 1\". Lower-third: Stephan Pereira, [role], SSB.",
     "note": "Brand, the first milestone, the speaker named with a role."},
    {"t": "3-12 s", "voice": "Most people learn business in a classroom for 2 years and meet a real customer after. Here it's the other way round.",
     "screen": "Caption: \"Customers first\".",
     "note": "The problem, as a contrast in order, not an attack."},
    {"t": "12-15 s", "voice": "Here's your first 6 months.", "screen": "Timeline graphic: Day 1 / Week 6 / Month 6.",
     "note": "Pivot."},
    {"t": "15-22 s", "voice": "It's an 18-month, full-time PGP in Bengaluru, mentored by leaders from McKinsey, Zomato, Razorpay and Apple.",
     "screen": "Text: \"18 months | Full time | Bengaluru\".",
     "note": "Specs; operators named as in your own ads."},
    {"t": "22-31 s", "voice": "Week 6: your D2C brand chasing a ₹5 lakh revenue target. Month 6: you're pitching your business to [named VC firm].",
     "screen": "Real footage of each step; caption \"Week 6: ₹5L+ target\" / \"Month 6: investor pitch\".",
     "note": "One named company per step; define every rupee figure."},
    {"t": "31-38 s", "voice": "Scaler: in education since 2016, with 1,200+ hiring partners.",
     "screen": "Text: \"Since 2016\" / \"1,200+ hiring partners\".",
     "note": "Tenure and distribution."},
    {"t": "38-45 s", "voice": "The next [seats] students start [batch start]. Apply by [next deadline], scholarships up to 100%. Apply now.",
     "screen": "End card with seats, date and scholarship line.",
     "note": "Spoken ask with all three levers."},
]
A_SCRIPTS.append({
    "title": "By month 3: the timeline series, one named company per step",
    "persona": "21 to 26, a recent graduate who wants speed and responds to concrete milestones more than to arguments.",
    "why": "Your highest-scoring idea: the timeline film runs as 5 ads and 7 versions in two shapes, from day one on Bangalore streets to investors by month 6. The speaker is captioned by name only, \"50 lakh\" is never defined, and nothing is asked aloud.",
    "evidence_ads": C10[:3],
    "format": "Speaker to camera on campus and in the city, fast cuts to real footage of each step, vertical first, square cut from it",
    "length": "45 seconds",
    "language": "English",
    "openings": [
        "Day one at Scaler School of Business: you're on the streets of Bangalore, selling.",
        "Week 6 at SSB: your own D2C brand, with a ₹5 lakh target.",
        "Month 6 at SSB: you're pitching investors. Here's how you get there.",
    ],
    "beats": seven(rows), "script": rows,
    "on_screen": "Name and role under the speaker in every episode; each step shown with real footage of that step. Drop \"more experience than most MBA graduates\".",
    "end_card": "\"PGP in Management & Tech\", \"18-Month | Full-Time | Bangalore Campus\", [seats] seats, \"Apply by [next deadline]\", \"Scholarships up to 100%*\".",
})

rows = [
    {"t": "0-3 s", "voice": "Preparing for CAT? Good. Scaler School of Business needs no test score at all.",
     "screen": "Caption: \"No CAT score needed\". Lower-third: [name], [admissions role], SSB.",
     "note": "The strongest claim for MBA aspirants, first."},
    {"t": "3-12 s", "voice": "A percentile tells a school how you do in a 2-hour test. It says nothing about whether you can sell, lead a team or build something people pay for.",
     "screen": "Caption: \"2 hours vs what you've built\".",
     "note": "The problem is the test, not the MBA."},
    {"t": "12-15 s", "voice": "So we look at what you've done.", "screen": "Cut to an interview room.",
     "note": "Pivot."},
    {"t": "15-22 s", "voice": "Your profile, then 2 interviews with industry leaders, with a case. The PGP itself: 18 months, full time, in Bengaluru.",
     "screen": "Steps: \"Profile\" / \"2 interviews + case\" / \"Decision in 3 to 5 days\".",
     "note": "The admission process and the specs."},
    {"t": "22-31 s", "voice": "Once you're in, you run a D2C brand with a ₹5 lakh target in 6 weeks and build GTM plans for brands like Mokobara.",
     "screen": "D2C stall and Mokobara session footage.",
     "note": "What students do."},
    {"t": "31-38 s", "voice": "Cohort 1's average CTC was 19 LPA, with 1,200+ hiring partners.",
     "screen": "Text: \"19 LPA avg. CTC, Cohort 1\" with source / \"1,200+ hiring partners\".",
     "note": "Outcome with its cohort."},
    {"t": "38-45 s", "voice": "[Seats] seats. Apply by [next deadline], scholarships up to 100%. Keep your CAT plan, and apply here too.",
     "screen": "End card: \"No CAT score needed\", seats, date, scholarships.",
     "note": "Ask that does not ask them to give anything up."},
]
A_SCRIPTS.append({
    "title": "No CAT score needed: the admissions explainer for MBA aspirants",
    "persona": "22 to 26, preparing for CAT or GMAT, wants an MBA and will defend that choice if an ad mocks it.",
    "why": "11 of your 30 ads open by calling the MBA or college outdated, dead or not enough, which your own rules say backfires with MBA aspirants. Mesa takes on the entrance test instead, in a 4-ad CAT question video. Your site says no test score is needed.",
    "evidence_ads": C01[:2] + C04[:1] + M08[:2],
    "format": "Admissions lead to camera, then the interview room and campus footage, vertical",
    "length": "45 seconds",
    "language": "English",
    "openings": [
        "Preparing for CAT? Good. Scaler School of Business needs no test score at all.",
        "No CAT score needed. 2 interviews with industry leaders instead.",
        "Your percentile isn't your profile. Here's how SSB admits people.",
    ],
    "beats": seven(rows), "script": rows,
    "on_screen": "No line that mocks the MBA, MBA colleges or their graduates. Say \"PGP\", never \"MBA\".",
    "end_card": "\"No CAT score needed\", \"PGP in Management & Tech\", [seats] seats, \"Apply by [next deadline]\", \"Scholarships up to 100%*\".",
})

rows = [
    {"t": "0-3 s", "voice": "Yaar, ek baat bolun? Main jab bhi hire karta hoon, 1 cheez dekhta hoon: skills.",
     "screen": "Lower-third: [name], [role, company]. Caption in Roman script.",
     "note": "Speaker named with a role; Hinglish from the first word."},
    {"t": "3-12 s", "voice": "College ka naam nahi, marks nahi. Kya tum bech sakte ho? Team chala sakte ho? Zyada tar log yeh kabhi try hi nahi karte.",
     "screen": "Caption: \"Bech sakte ho? Team chala sakte ho?\"",
     "note": "The problem, about skills, not about the MBA."},
    {"t": "12-15 s", "voice": "Isliye Scaler School of Business alag hai.", "screen": "SSB campus.",
     "note": "Brand pivot."},
    {"t": "15-22 s", "voice": "18 mahine, full time, Bengaluru campus. Padhate hain CEOs, CMOs aur product heads.",
     "screen": "Text: \"18 months | Full time | Bengaluru\".",
     "note": "Specs and operators."},
    {"t": "22-31 s", "voice": "Students 6 hafte mein apna D2C brand chalate hain, ₹5 lakh ke target ke saath, aur Mokobara jaise brands ke liye GTM plan banate hain.",
     "screen": "Stall footage; caption \"₹5L+ target, 6 weeks\".",
     "note": "Named project."},
    {"t": "31-38 s", "voice": "Cohort 1 ka average CTC: 19 LPA. Aur 1,200+ hiring partners.",
     "screen": "Text with cohort and source.",
     "note": "Outcome."},
    {"t": "38-45 s", "voice": "Sirf [seats] seats. Last date [next deadline]. Scholarships 100% tak. Abhi apply karo.",
     "screen": "End card in English with the same figures.",
     "note": "All three levers, in Hinglish throughout."},
]
A_SCRIPTS.append({
    "title": "Hinglish to camera: a hirer on why he looks at skills, all in Hinglish",
    "persona": "22 to 27, from a Hindi-speaking city, more at ease in Hinglish than in English, sceptical of polished B-school ads.",
    "why": "Your two Hinglish ideas run as 6 of your 30 ads; all 126 of Mesa's videos are in English. Your Hinglish endorsement names no one on screen and its speaker is unlabelled.",
    "evidence_ads": C09 + C11[:1],
    "format": "One speaker to camera, one take, two angles, Roman-script captions, vertical",
    "length": "45 seconds",
    "language": "Hinglish",
    "openings": [
        "Yaar, ek baat bolun? Main jab bhi hire karta hoon, 1 cheez dekhta hoon: skills.",
        "College ka naam? Mujhe farak nahi padta. Skills dikhao.",
        "6 hafte mein ₹5 lakh ka target. Yeh hai Scaler School of Business.",
    ],
    "beats": seven(rows), "script": rows,
    "on_screen": "Keep the whole script in Hinglish; no switch to English halfway. The speaker's name and role on screen, with consent.",
    "end_card": "English card: \"PGP in Management & Tech\", [seats] seats, \"Apply by [next deadline]\", \"Scholarships up to 100%*\".",
})

for s in A_SCRIPTS:
    s.setdefault("compliance", COMPLIANCE_SSB)
    s.setdefault("measure", MEASURE_SSB)

# ---------------------------------------------------------------- scripts: Mesa (B)
B_SCRIPTS = []


def six(rows_):
    names = ["Hook", "Problem", "Mechanism", "Proof", "Offer", "Call to action"]
    return [{"t": r["t"], "beat": n, "note": r.get("note", "")} for n, r in zip(names, rows_)]


rows = [
    {"t": "0-3 s", "voice": "We are looking for 175 people for the next cohort at Mesa.", "screen": "Caption: \"175 seats\". Lower-third: [name], [role], Mesa.", "note": "Seats as the site states them."},
    {"t": "3-12 s", "voice": "People who would rather build a company, or lead inside a startup, than sit in a back-office role.", "screen": "Caption: \"Build or lead\".", "note": "Who it is for."},
    {"t": "12-24 s", "voice": "12 months, full time, in Bangalore: a curriculum taught by business experts, live projects with startups, and a business you build from scratch.", "screen": "Three captions, one per pillar.", "note": "The three ways, as today."},
    {"t": "24-32 s", "voice": "Our last cohorts averaged a 26 lakh CTC. [Source line, as the placement report words it.]", "screen": "\"26L average CTC\" with cohort and source.", "note": "One figure, defined."},
    {"t": "32-38 s", "voice": "Round 1 closes [Round 1 date].", "screen": "\"Round 1 closes [date]\"", "note": "A date."},
    {"t": "38-42 s", "voice": "Take the MAT and apply now.", "screen": "End card: PGP in Startup Leadership, Apply now.", "note": "Spoken ask."},
]
B_SCRIPTS.append({
    "title": "The cohort call, now with the seats, the round date and the ask",
    "persona": "1 to 5 years into work, already curious about startups, who needs a reason to apply this round.",
    "why": "Your cohort call is your highest-scoring PGP idea, 9 ads and 16 versions, and ends \"apply fast\" with no date. It says 200 people; your site says 175 seats.",
    "evidence_ads": M23[:3],
    "format": "The same speaker and room as the cohort call, two angles, captions on, square and vertical",
    "length": "42 seconds", "language": "English",
    "openings": ["We are looking for 175 people for the next cohort at Mesa.", "175 seats. Round 1 closes [Round 1 date].", "Mesa's next cohort: 175 people who want to build."],
    "beats": six(rows), "script": rows,
    "on_screen": "Seats, the round date and one sourced outcome; nothing the site does not state.",
    "end_card": "PGP in Startup Leadership & Entrepreneurship, \"175 seats\", \"Round 1 closes [date]\", Apply now.",
})
rows = [
    {"t": "0-3 s", "voice": "Week 1 at Mesa, I was selling on the street.", "screen": "Caption: \"Week 1\". Lower-third: [student name], PGP, Cohort [n].", "note": "The student speaks, first person."},
    {"t": "3-12 s", "voice": "Before Mesa I was [previous role]. I'd never sold anything.", "screen": "Old photo at work.", "note": "Where they started."},
    {"t": "12-24 s", "voice": "Week 8: our team's business hit [our revenue] in sales. Month [n]: I was presenting to [named founder or VC].", "screen": "Timeline: Week 1 / Week 8 / Month [n].", "note": "Steps with real figures from that student."},
    {"t": "24-32 s", "voice": "Now I'm [role] at [company].", "screen": "Caption with the role and company, with consent.", "note": "The outcome, this student's own."},
    {"t": "32-38 s", "voice": "175 seats for the next cohort.", "screen": "\"175 seats\"", "note": "Scarcity from the site."},
    {"t": "38-42 s", "voice": "Apply before [Round 1 date].", "screen": "End card.", "note": "Spoken ask."},
]
B_SCRIPTS.append({
    "title": "A student's year, month by month, told by the student",
    "persona": "23 to 28, considering a career switch, who trusts a peer more than staff.",
    "why": "SSB's highest-scoring idea walks a year month by month, from day one on the street to investors by month 6, in 5 ads. Your only student voice is one 5-ad video; undergraduate students are talked about in six videos and speak in none.",
    "evidence_ads": C10[:2] + M10[:2],
    "format": "Student to camera, cut to footage of each step, vertical",
    "length": "42 seconds", "language": "English",
    "openings": ["Week 1 at Mesa, I was selling on the street.", "8 weeks into Mesa, our team had real customers.", "A year ago I was [previous role]. Here's every step."],
    "beats": six(rows), "script": rows,
    "on_screen": "Every figure is this student's own, with consent; the student is named on screen.",
    "end_card": "PGP in Startup Leadership & Entrepreneurship, \"175 seats\", Apply now.",
})
rows = [
    {"t": "0-3 s", "voice": "I'm [name], I run careers at Mesa. Here's our placement number, and where it comes from.", "screen": "Lower-third: [name], [careers role], Mesa.", "note": "Named speaker, first line."},
    {"t": "3-12 s", "voice": "You'll see a lot of salary numbers in B-school ads. Ask which cohort, and who checked.", "screen": "Caption: \"Which cohort? Who checked?\"", "note": "The doubt the viewer already has."},
    {"t": "12-24 s", "voice": "Our average CTC was 26 lakh, [cohorts], and 58% went into founder-facing roles.", "screen": "\"26L average CTC\" / \"58% founder-facing roles\" with source.", "note": "Two site figures, defined."},
    {"t": "24-32 s", "voice": "[Number] startups hire from us. That's the number in our placement report.", "screen": "One partner count, as the report states it.", "note": "One count, everywhere."},
    {"t": "32-38 s", "voice": "175 seats in the next cohort.", "screen": "\"175 seats\"", "note": "Scarcity."},
    {"t": "38-42 s", "voice": "Read the report, then apply.", "screen": "End card: Download placement report / Apply now.", "note": "Ask."},
]
B_SCRIPTS.append({
    "title": "Named careers lead, one sourced figure: the placement number and where it comes from",
    "persona": "A sceptic comparing B-school placement claims who has seen too many unsourced numbers.",
    "why": "30 of your 93 PGP ads state a graduate outcome, but the figures disagree: 100% placements, upwards of 25 lakhs, 50 to 60% rises, 2.8x; startups hiring are 100, 150 or 500. Your careers lead is unnamed in 4 ads.",
    "evidence_ads": M06[:2] + M09[:1] + ["40210023251944395"],
    "format": "Careers lead to camera, one take, the report page on screen, vertical",
    "length": "42 seconds", "language": "English",
    "openings": ["I'm [name], I run careers at Mesa. Here's our placement number, and where it comes from.", "26 lakh average CTC. Here's which cohort, and who checked.", "Ask every B-school one question: which cohort?"],
    "beats": six(rows), "script": rows,
    "on_screen": "Only figures that the placement report states, each with its cohort.",
    "end_card": "\"26L average CTC, [cohorts]\", \"175 seats\", Apply now.",
})
rows = [
    {"t": "0-3 s", "voice": "Ascend: Mesa's PGP for people who keep their job.", "screen": "Gold Ascend caption; lower-third: [name], [role].", "note": "Say Ascend aloud, first line."},
    {"t": "3-12 s", "voice": "You've mastered your role. Now you want to lead the whole business, without quitting.", "screen": "Caption: \"Keep your job\".", "note": "The audience call-out."},
    {"t": "12-24 s", "voice": "12 months of weekends, about 10 hours a week: a Saturday class, a Sunday founder session, one weekday check-in.", "screen": "Week grid: Sat / Sun / one evening.", "note": "The site's schedule."},
    {"t": "24-32 s", "voice": "In 8 weeks, you and two teammates run a real business with a ₹5 lakh revenue target.", "screen": "Caption: \"₹5L target, 8 weeks, 3-person team\".", "note": "The site's build claim, defined."},
    {"t": "32-38 s", "voice": "Early bird closes [early bird date]. Scholarships up to ₹10 lakh.", "screen": "\"Early bird [date]\" / \"Scholarships up to ₹10L\"", "note": "Date as the site states it on the day."},
    {"t": "38-42 s", "voice": "Apply to Ascend now.", "screen": "End card in gold.", "note": "Spoken ask."},
]
B_SCRIPTS.append({
    "title": "Ascend by name: weekends, 10 hours a week, keep your job, said aloud",
    "persona": "25 to 38, mid-career, will not quit a salary, has seen the \"don't quit your job\" image ads.",
    "why": "Your Ascend shoot runs as 32 ads across six ideas and the speech never says Ascend; the quit-your-job image cards add 32 more. One image idea says the early bird closes 26 November, your site 29 Nov.",
    "evidence_ads": ids("B", "MS-c13")[:2] + ids("B", "MS-s05")[:2],
    "format": "Ascend speaker to camera, the same set, vertical, gold captions",
    "length": "42 seconds", "language": "English",
    "openings": ["Ascend: Mesa's PGP for people who keep their job.", "Keep your job. Learn the whole business. That's Ascend.", "10 hours a week, 12 months of weekends: Ascend."],
    "beats": six(rows), "script": rows,
    "on_screen": "Ascend named in voice and caption; one early bird date, the site's.",
    "end_card": "Ascend: Hybrid PGP in Business, AI & Entrepreneurship, \"Early bird [date]\", Apply now.",
})
for s in B_SCRIPTS:
    s.setdefault("compliance", COMPLIANCE_MESA)
    s.setdefault("measure", MEASURE_MESA)

SER_A_MBA = "series:A:Openings that run down the MBA"
SER_B_OUT = "series:B:Graduate outcomes, in figures or named alumni"

persp = {
    "A": {
        "verdict": "Full-time PGP against PGP: Mesa puts a person to camera in 34 of its 67 PGP videos; you, 7 of 30. Your edge: the month-by-month timeline, 5 of 30.",
        "plan": {
            "focus": {"title": "Open PGP ads on your own cohort outcomes, sourced.",
                      "why": "Mesa states a graduate outcome in 30 of its 93 PGP ads: 100% placements, a 25 lakh average, 58% founder-facing, 2.8x. Its figures conflict. None of your 30 gives a placement or salary figure.",
                      "basis": SER_B_OUT, "evidence": "strong", "effort": "Low",
                      "first_test": "Three 45-second cuts, each opening on one site figure with cohort and source: 19 LPA Cohort 1, 23 LPA Cohort 2, 40 placements.",
                      "script": 1},
            "start": [
                {"title": "Answer Mesa's cohort call: seats, date, scholarships, aloud.",
                 "why": "Mesa's highest-scoring PGP idea is a 38-second cohort call, 9 ads and 16 versions: 200 people, the fifth cohort, \"apply fast\". None of your 30 names a scholarship or a live date.",
                 "basis": "idea:B:MS-c23", "evidence": "strong", "effort": "Low",
                 "first_test": "Admissions lead to camera, 45 seconds: [seats], the admission page's next deadline, scholarships up to 100%, said and on the end card.",
                 "script": 2},
                {"title": "Make \"By month 3\" a series, speaker named with a role.",
                 "why": "Your highest-scoring idea: 5 ads, 7 versions, two shapes, day one on Bangalore streets to investors by month 6. The speaker has a name and no role; nothing is asked aloud.",
                 "basis": "idea:A:SSB-c10", "evidence": "strong", "effort": "Medium",
                 "first_test": "Recut the square version: role under the name, \"50 lakh\" defined, a spoken close with seats, deadline and scholarships.",
                 "script": 3},
                {"title": "Start PGP image ads; Mesa runs 26, you none.",
                 "why": "Mesa runs 26 image ads for its full-time PGP, 15 of them product or people across 11 ideas. None of your 30 sampled ads is an image; 6 live ads were not pulled.",
                 "basis": "row:I2", "evidence": "moderate", "effort": "Low",
                 "first_test": "Three image ads: a cohort CTC figure with source, a deadline and scholarships card, a still from the Mokobara project."},
            ],
            "stop": [
                {"title": "Stop opening on \"MBAs are outdated\".",
                 "why": "11 of your 30 ads open by calling the MBA or college outdated, dead or not enough; 3 add an unsourced \"one in four MBA graduates is unemployable\". Your own rules say this backfires.",
                 "basis": SER_A_MBA, "evidence": "strong", "effort": "Low",
                 "first_test": "Recut the 3 \"outdated\" ads to open on \"No CAT score needed\", the site's line; keep the investor's middle.",
                 "script": 4},
                {"title": "Fix the passed date and the \"MBA\" wording.",
                 "why": "4 ads started 17 to 19 Nov still show \"Early Bird Deadline 1st November 2026\"; your site says 29 Nov. 29 ad texts say \"MBA-equivalent PGP\"; the site says certificate, not degree.",
                 "basis": "contradictions:A",
                 "first_test": "Today: drop the dated headline on 2 ads and the dated end card on 2; say \"PGP in Management & Tech\" in all ad text."},
            ],
        },
        "workhorse_read": "You spread 30 ads over 11 ideas: the timeline film carries 5 (17%), the three largest 12 (40%). Mesa's full-time PGP leans on the cohort call (9 ads) and one investor recording (11 ads); half of all Mesa's ads, 127 of 249, sell its part-time Ascend.",
        "now_read": "All 30 of your sampled ads started in November, 25 of them on 17 to 19 Nov. Mesa started 191 of its 249 on 16 to 19 Nov, 93 of them Ascend ads on 17 Nov alone; 63 of its 93 PGP ads started in those four days.",
        "india_read": [
            "Language: video, you speak English in 24 of 30 and Hinglish in 6 (two ideas); Mesa speaks English in all 126 videos. Image: you have none; Mesa's 115 tagged image ads are in English.",
            "Timing: both pushed after Diwali (8 Nov 2026) and before early bird closes on 29 Nov 2026 (your PGP and Mesa's Ascend, per each site); no festival falls on 16 to 19 Nov.",
            "Destination: all 30 of your ads go to one page, scaler.com/school-of-business/minimal-landing/; Mesa sends each programme to its own pages: PGP 93, Ascend 127, Undergraduate 29.",
        ],
        "scripts": A_SCRIPTS,
    },
    "B": {
        "verdict": "Full-time PGP: SSB walks a student month by month in 5 of its 30 ads; no PGP idea of yours does. Your edge: person to camera, 34 of 67 videos.",
        "plan": {
            "focus": {"title": "Give the cohort call a spoken date and the site's seat count.",
                      "why": "Your highest-scoring PGP idea, 9 ads and 16 versions, calls for 200 people for the fifth cohort and ends \"apply fast\" with no date. Your site says 175 seats.",
                      "basis": "idea:B:MS-c23", "evidence": "strong", "effort": "Low",
                      "first_test": "Recut the square cohort call: \"175 seats\", the Round 1 date as the PGP page states it, then the end card.",
                      "script": 1},
            "start": [
                {"title": "Walk one student through the year, month by month.",
                 "why": "SSB's highest-scoring idea runs as 5 ads and 7 versions: day one on Bangalore streets, a D2C brand by month 3, investors by month 6. No PGP idea of yours walks the year in steps.",
                 "basis": "idea:A:SSB-c10", "evidence": "strong", "effort": "Medium",
                 "first_test": "One PGP student to camera, 42 seconds: week 1, week 8, month [n], each with footage and the student's own figures.",
                 "script": 2},
                {"title": "Name the investor and your staff on screen.",
                 "why": "Your investor recording runs as 11 ads in two edits, one opening on \"200 plus startups\", one on 5 lakhs in 8 weeks; he is never named on screen.",
                 "basis": "series:B:One investor recording, two edits", "evidence": "strong", "effort": "Low",
                 "first_test": "Add a name and role card in the first 3 seconds of the 8 cold-open ads, with his written consent.",
                 "script": 3},
                {"title": "Test one Hinglish cut.",
                 "why": "SSB's Hinglish endorsement runs as 3 ads and 5 versions; all 126 of your videos are in English.",
                 "basis": "idea:A:SSB-c09", "evidence": "moderate", "effort": "Low",
                 "first_test": "A Hinglish cut of the careers lead's placement answer, 40 seconds, captions in Roman script."},
            ],
            "stop": [
                {"title": "Settle one count per claim across your ads.",
                 "why": "Startups hiring from you are 100, 150 or 500 by ad; one student brand does 20 or 25 lakh a month; the 5 lakh line has no stated scope.",
                 "basis": "contradictions:B",
                 "first_test": "Take the placement report's figure for each and recut the careers-lead, khakra and salary-rise videos first.",
                 "script": 3},
            ],
        },
        "workhorse_read": "In your 93 full-time PGP ads the cohort call carries 9 (10%), the three largest 24 (26%). Across all 249, Ascend leads: 32 quit-your-job image cards and a 32-ad interview shoot. SSB's 30 ads sit on 11 ideas, led by its 5-ad timeline film.",
        "now_read": "191 of your 249 sampled ads started on 16 to 19 Nov, 93 of them Ascend on 17 Nov; 63 of your 93 PGP ads started in those days. SSB started 25 of its 30 on 17 to 19 Nov.",
        "india_read": [
            "Language: video, you speak English in all 126; SSB speaks English in 24 of 30 and Hinglish in 6. Image: your 115 tagged image ads are in English; SSB's sample has no image ads.",
            "Timing: both pushed after Diwali (8 Nov 2026) and before early bird closes on 29 Nov 2026 (Ascend and SSB's PGP, per each site); no festival falls on 16 to 19 Nov.",
            "Destination: you send each programme to its own pages (PGP 93, Ascend 127, Undergraduate 29); all 30 of SSB's go to one page, scaler.com/school-of-business/minimal-landing/.",
        ],
        "scripts": B_SCRIPTS,
    },
    "extras": {
        "source": "Read from each brand's ads by hand (research/<brand>/concepts.md) and from each brand's website (research/<brand>/site.md: SSB read 22 Nov 2026, Mesa's saved text of 19 and 20 Nov). The two samples differ in size: SSB 30 ads, nearly all its live ads; Mesa 249 of about 320. Compare shares, not counts.",
        "contradictions": {
            "A": [
                {"text": "The early bird deadline of 1 November 2026 is in the headline of two ads started on 19 Nov and on the end card of two started on 17 Nov; SSB's site says the early bird closes 29 Nov 2026.",
                 "ads": EARLY},
                {"text": "The programme is \"MBA student\" and \"MBA graduates\" in speech, \"MBA-equivalent PGP\" in 29 ad texts and \"PGP in Management & Tech\" on 22 end cards; the site says it is a certificate, not a degree, and SSB is not a university.",
                 "ads": ["2128818651073533", "1124686257016435", "1406583844890391", "2559185667923714"]},
                {"text": "50 lakh is a brand's revenue in one caption, a unit count in the software transcript of another cut, a D2C aim \"in just 12 [?]\" and a funding offer to a student, with no source for any.",
                 "ads": ["2559185667923714", "2128818651073533", "1171509055224316", "1124686257016435"]},
                {"text": "The end card says 18-Month; the timeline promises results by month 3 and \"in less than a year\"; a voiceover says \"the last two years\".",
                 "ads": ["2559185667923714", "2128818651073533", "1171509055224316"]},
                {"text": "The headline says \"India's Only B-School Designed by Industry Leaders\"; one end card says \"India's First Industry and AI-Led Business School\"; the site uses both \"only\" and \"first\".",
                 "ads": ["2559185667923714", "1406583844890391", "4572207989702796"]},
            ],
            "B": [
                {"text": "Startups that hire from Mesa: one video says 100 plus, the investor cuts say 150 plus, the careers lead says at least 500, and the ad text of the stat video says 100+ live startups.",
                 "ads": ["40210023251944395", "4585145681703758", "1498875895417529", "1634433821103521"]},
                {"text": "One student brand: the khakra business does 20 lakh a month in one video and 25 lakh a month in another, and the two ads started on the same day.",
                 "ads": ["1885584672793111", "1512248814079802"]},
                {"text": "The 5 lakh line has no stated scope: \"every student has to sell 5 lakhs\", \"every single student does 5 lakh\", \"over 5 lakh\" from a D2C business, and \"almost one crore\" for each student business.",
                 "ads": ["4585145681703758", "1576676950895208", "1609473000417031", "29250519677942503", "1358399446249615"]},
                {"text": "Pay claims: an average salary \"upwards of 25 lakhs\", alumni with a \"50 to 60% increase\", a \"2.8x average salary jump\" on an image, beside \"100% placements\" and \"57.5% joined super early stage startups\", none defined.",
                 "ads": ["1488536809855650", "40210023251944395", "1498875895417529", "1615063316971151"]},
                {"text": "The cohort call asks for \"200 special people\" for the fifth cohort; Mesa's PGP page says 175 seats.",
                 "ads": M23[:3]},
            ],
        },
    },
}
OUT.write_text(json.dumps(persp, indent=1, ensure_ascii=False))
print("wrote", OUT)
