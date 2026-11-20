// Landing page. Source: master doc "SSB UG: Website copy" → tab "Pg 1: Highlights".
// Copy is kept word for word; small fixes are noted inline.
import type { Story } from '@/lib/types';
import { b, img, imgs, list, stat } from './helpers';
import { campusTabs, closingCta, internshipCards, internshipStats, recruiterLogos } from './shared';

const person = (name: string, role: string, image: string, company: string, logo?: string, subject?: string) =>
  b('person', { name, role, company, image: img(image, name), ...(logo ? { logo: img(logo) } : {}), ...(subject ? { subject } : {}) });

export const home: Story = {
  name: 'Home',
  slug: 'home',
  full_slug: 'home',
  content: b('page', {
    seo_title: 'UG Programme in Business, Entrepreneurship & AI',
    seo_description:
      'A four-year UG programme in Business, Entrepreneurship & AI, on the Scaler campus in Bengaluru. Build 4 real businesses, ship AI products and intern from Year 1.',
    body: [
      /* ---------------- Section 1: Hero (Option 6 of 9 in the doc) ---------------- */
      b('hero', {
        eyebrow: 'UG programme in Business, Entrepreneurship & AI',
        headline: 'Build 4 businesses before you graduate.',
        subhead: 'A four-year UG programme in Business, Entrepreneurship & AI, on the Scaler campus in Bengaluru.',
        video: img('/media/hero-film.mp4'),
        poster: img('/media/campus-film-poster.jpg', 'Students on the Scaler campus'),
        pills: list('Learn by building startups', 'Taught by CXOs & Founders', 'AI embedded curriculum'),
        boxes: [
          b('fact_box', { title: '4 years', text: 'Incl. internships & study abroad' }),
          b('fact_box', { title: 'Bangalore', text: 'World-class campus in India’s Silicon Valley' }),
          b('fact_box', { title: 'Only 100 seats', text: 'Highly talented peers' }),
        ],
        primary_cta_label: 'Join the early waitlist',
        primary_cta_href: 'lead:waitlist',
        secondary_cta_label: 'Download Brochure',
        secondary_cta_href: 'lead:brochure',
        built_by_label: 'Built by 100+ industry leaders from',
        built_by_logos: imgs('/logos/google.svg', '/logos/meta.svg', '/logos/mckinsey.svg', '/logos/bcg.svg', '/logos/bain.svg'),
        backed_by_label: 'Backed by',
        backed_by_logos: imgs('/logos/sequoia.svg', '/logos/lightrock.svg'),
        backed_by_names: 'Tiger Global',
      }),

      /* ---------------- Proof bar (directly under the hero) ---------------- */
      b('proof_bar', {
        items: [
          stat('₹44 LPA', 'Highest CTC at Scaler'),
          stat('₹2 Cr+', 'ARR from a student startup'),
          stat('100%', 'Internship placement at SSB'),
          stat('1,200+', 'Scaler hiring partners'),
        ],
      }),

      /* ---------------- Vision behind the programme [Launch video] ---------------- */
      b('video_feature', {
        eyebrow: 'The vision',
        headline: 'Vision behind the programme.',
        text: 'Watch the launch video for SSB’s UG programme in Business, Entrepreneurship & AI.',
        poster: img('/media/why-story-cohort.webp', 'SSB students at convocation'),
        video_url: '/media/campus-film.mp4',
        video_label: 'Launch video',
      }),

      /* ---------------- Section 2: Pillars of the programme ---------------- */
      b('pillars', {
        anchor: 'programme',
        eyebrow: 'Why SSB UG',
        headline: 'Pillars of the programme.',
        subhead: 'Graduate with 3 career pathways: scale your startup, grow your family business, or get placed at a top startup or MNC.',
        items: [
          b('pillar', {
            title: 'World-class faculty, mentors & peers',
            lead: '250+ hours with the people who build, run and fund companies.',
            points: list('Curriculum built by Founders, CXOs & Industry leaders', 'Professors from Stanford, Oxford, IIM & ISB', 'A selective cohort, plus talented SST & PGP peers'),
            image: img('/campus/class-fireside.webp'),
          }),
          b('pillar', {
            title: 'Build 4 real businesses',
            lead: 'A MicroSaaS tool, a D2C brand, a content channel and your own startup.',
            points: list('₹5 Cr venture fund & VC Demo Days with 50+ investors', 'Access to Scaler Innovation Lab & SST tech co-founders', 'Content Creator Lab to support your creator-preneur journey'),
            image: img('/media/d2c-bazaar-800.webp'),
          }),
          b('pillar', {
            title: 'Internships from Year 1',
            lead: 'Work inside real companies from your first summer.',
            points: list('Founder’s office & EIR roles at top Indian startups', '12+ global internships across Singapore, Dubai, etc.', '1,200+ hiring partners across MNCs & AI companies'),
            image: img('/media/lab-mentor-1400.webp'),
          }),
          b('pillar', {
            title: 'Ship 4+ no-code AI products',
            lead: 'Build AI agents that real businesses use.',
            points: list('500+ hours of applied AI & 4+ shipped products', '1:1 mentorship from experts from OpenAI, Meta, Google', '30+ tools & 3 hackathons with SST'),
            image: img('/media/lab-hand-1400.webp'),
          }),
          b('pillar', {
            title: 'Global & Pan-India Immersions',
            lead: 'Study business on factory floors and in global hubs.',
            points: list('2+ Global immersions at top schools across Singapore, Dubai, etc.', '6+ Visits to India’s manufacturing hubs and headquarters', '4+ Winter Treks & cultural experiences across India'),
            image: img('/media/singapore/marina-dusk.webp'),
          }),
          b('pillar', {
            title: 'Live projects, including your family business',
            lead: 'Solve real problems for real businesses.',
            points: list('Companies like Mokobara, Ajio, Practo & Quenzy', 'An optional Family Business track from Year 3', 'Harvard Business School cases'),
            image: img('/live-projects/mokobara.jpg'),
          }),
        ],
      }),

      /* ---------------- Section 3: World-class faculty (photos as on SSB PGP) ---------------- */
      b('people_tabs', {
        anchor: 'faculty',
        eyebrow: 'Faculty',
        headline: 'Learn from world-class faculty.',
        muted: 'Founders, investors & top b-school professors.',
        groups: [
          b('people_group', {
            label: 'Marquee founders',
            layout: 'landscape',
            people: [
              b('person', {
                name: 'Anupam Mittal',
                role: 'Founder & CEO, Shaadi.com · Shark Tank India judge',
                quote: 'Offered ₹50 lakh to a student startup',
                subject: 'Student pitches at SSB',
                image: img('/on-campus/anupam-mittal.webp', 'Anupam Mittal with SSB students'),
                avatar: img('/media/mittal-avatar.jpg', 'Anupam Mittal'),
                video_url: 'https://www.youtube.com/watch?v=fCP4SbBrwKQ',
              }),
              b('person', {
                name: 'Shantanu Deshpande',
                role: 'Founder & CEO, Bombay Shaving Company',
                quote: 'Taught the ₹100 crore D2C playbook',
                subject: 'Masterclass at SSB',
                image: img('/media/shantanu-card.webp', 'Shantanu Deshpande at SSB'),
                avatar: img('/media/shantanu-avatar.jpg', 'Shantanu Deshpande'),
              }),
              b('person', {
                name: 'Kiran Shah',
                role: 'Founder, Go Zero · Shark Tank India',
                quote: 'From one parlour to a national brand',
                subject: 'SSB commencement',
                image: img('/media/kiran-card.webp', 'Kiran Shah at SSB'),
                avatar: img('/media/kiran-avatar.jpg', 'Kiran Shah'),
              }),
              b('person', {
                name: 'Ankur Warikoo',
                role: 'Founder, WebVeda · Author, Do Epic Shit',
                quote: 'Handed our graduates their degrees',
                subject: 'Convocation at SSB',
                image: img('/on-campus/ankur-warikoo.webp', 'Ankur Warikoo at SSB'),
                avatar: img('/media/warikoo-avatar.jpg', 'Ankur Warikoo'),
                video_url: 'https://www.youtube.com/watch?v=ZFVqtpqSlyI',
              }),
            ],
          }),
          b('people_group', {
            label: 'Mentors & Investors',
            layout: 'portrait',
            people: [
              person('Deepinder Goyal', 'Co-founder, Zomato', '/people/deepinder-goyal.webp', 'Zomato', '/logos/marks/fc-zomato.png'),
              person('Binny Bansal', 'Co-founder, Flipkart', '/people/binny-bansal.webp', 'Flipkart', '/logos/marks/flipkart-mark.svg'),
              person('Vijay Shekhar Sharma', 'MD, Paytm', '/people/vijay-shekhar-sharma.webp', 'Paytm', '/logos/marks/fc-paytm.png'),
              person('Kunal Shah', 'Founder, CRED', '/people/kunal-shah.webp', 'CRED', '/logos/marks/fc-cred.png'),
              person('Rajan Anandan', 'MD, Peak XV', '/people/rajan-anandan.webp', 'Peak XV Partners', '/logos/marks/fc-peakxv.png'),
              person('Navin Parwal', 'Founder, Mokobara', '/people/navin-parwal.webp', 'Mokobara', '/logos/marks/fc-mokobara.png'),
              person('Roel Janssen', 'Partner, Global Founders Capital, Ex-McKinsey', '/people/roel-janssen.webp', 'Global Founders Capital', '/logos/marks/fc-global-founders-capital.png'),
              person('Vedant Trivedi', 'Investor, Peak XV, Ex-Sequoia', '/people/vedant-trivedi.webp', 'Peak XV Partners', '/logos/marks/fc-peakxv.png'),
              person('Divya Venkataraghavan', 'Principal, Lightrock / Aspada', '/people/divya-venkataraghavan.webp', 'Lightrock', '/logos/marks/fc-lightrock.png'),
              person('Sidhant Goyal', 'EIR, Toddle, Ex-Sequoia', '/people/sidhant-goyal.webp', 'Toddle', '/logos/marks/fc-toddle.png'),
            ],
          }),
          b('people_group', {
            label: 'Faculty',
            layout: 'portrait',
            people: [
              person('Siddharth Menon', 'Ex-CMO, Epigamia/Colgate', '/faculty/siddharth-menon.webp', 'Epigamia', '/logos/marks/fc-epigamia.png', 'Operations Management'),
              person('Akash Sinha', 'CEO & Co-Founder, Cashfree', '/faculty/akash-sinha.webp', 'Cashfree', '/logos/marks/fc-cashfree.png', 'Growth Marketing'),
              person('Dhron Kanish', 'Associate Partner, McKinsey', '/faculty/dhron-kanish.webp', 'McKinsey & Company', '/logos/marks/lead-mckinsey.png', 'Product Management'),
              person('Jacob Singh', 'Ex-CTO, Blinkit', '/faculty/jacob-singh.webp', 'Blinkit', '/logos/marks/fc-blinkit.png', 'Business Analytics'),
              person('Saurabh Jain', 'Co-Founder, Stable Money', '/faculty/saurabh-jain.webp', 'Stable Money', '/logos/marks/fc-stable-money.png', 'Brand Strategy'),
              person('Puneet', 'Partner, BCG', '/faculty/puneet.webp', 'BCG', '/logos/marks/fc-bcg.png', 'Corporate Finance'),
              person('Sidhant Goyal', 'Toddle; Ex-Sequoia Capital', '/faculty/sidhant-goyal.webp', 'Toddle', '/logos/marks/fc-toddle.png', 'Sales Leadership'),
              person('Malthi SS', 'Ex-Product Director, PayPal', '/faculty/malthi-ss.webp', 'PayPal', '/logos/marks/fc-paypal.png', 'Strategy & Consulting'),
              person('Kanishk Mehta', 'Sr. Product Director, Razorpay', '/faculty/kanishk-mehta.webp', 'Razorpay', '/logos/marks/fc-razorpay.png', 'Operations Management'),
              person('Gaurav Dadhich', 'Founder, Ex-Flipkart/Razorpay/Amazon', '/faculty/gaurav-dadhich.webp', 'Flipkart', '/logos/marks/flipkart-mark.svg', 'Growth Marketing'),
              person('Sandeep Das', 'Ex-Global Lead, Mars/PwC/Accenture', '/faculty/sandeep-das.webp', 'Mars', '/logos/marks/fc-mars.png', 'Product Management'),
              person('Saurabh Sengupta', 'Ex-SVP Sales, Zomato', '/faculty/saurabh-sengupta.webp', 'Zomato', '/logos/marks/fc-zomato.png', 'Brand Strategy'),
              person('Amit Puniyani', 'Ex-VP, Deutsche Bank/J.P. Morgan', '/faculty/amit-puniyani.webp', 'Deutsche Bank', '/logos/marks/fc-deutschebank.png', 'Corporate Finance'),
              person('Narahari Hansoge', 'IIM Faculty, PhD IIM-B', '/faculty/narahari-hansoge.webp', 'IIM Bangalore', '/logos/marks/iimb-mark.svg', 'Sales Leadership'),
              person('Vatsal Sanghvi', 'Founder, Ex-Flipkart', '/faculty/vatsal-sanghvi.webp', 'Flipkart', '/logos/marks/flipkart-mark.svg', 'Business Analytics'),
            ],
          }),
        ],
      }),

      /* ---------------- Section 4: Proven outcomes ---------------- */
      b('story_scroll', {
        anchor: 'outcomes',
        tone: 'dark',
        eyebrow: 'Our proven outcomes',
        headline: 'Scaler’s legacy of 10+ years in education.',
        subhead: 'Achievements of students at Scaler School of Business and Scaler School of Technology.',
        footnote: 'SSB UG welcomes its first batch in 2027. Outcomes shown are from Scaler’s existing programmes.',
        cards: [
          b('story_card', { name: 'NeoSapiens', tag: 'Scaler Innovation Lab', overlay: 'Funded on Shark Tank India', description: 'A Scaler Innovation Lab startup won funding on Shark Tank India for its AI-native wearable pendant.' }),
          b('story_card', { name: 'Dream Kit', tag: 'SSB', overlay: '₹2 Cr Toy Brand · 12,000+ paying customers', description: 'Aashish US built a STEAM toy brand used across schools while working full-time at The Whole Truth.', image: img('/deck/built/dream-kit.webp') }),
          b('story_card', { name: 'Gredo', tag: 'SSB', overlay: '₹1 Cr+ ARR · Vending machines across Bengaluru', description: 'Sanskriti Deshmukh built a protein-food brand live on Swiggy and Zomato.', image: img('/deck/built/gredo.webp') }),
          b('story_card', { name: 'Antimattr', tag: 'Scaler Innovation Lab', overlay: 'Selected for Y Combinator · Backed by Nikhil Kamath’s WTFund', description: 'Built at Scaler Innovation Lab, Antimattr is building voice-first AI hardware.', image: img('/startups/antimattr.webp') }),
          b('story_card', { name: 'Percevia', tag: 'SST', overlay: '₹25 Lakh Samsung Grant, in 2nd Year', description: 'Chosen from 20,000+ entries, Tushar is building AI glasses for the visually impaired.' }),
          b('story_card', { name: 'First Student at Apple', tag: 'SST', overlay: 'Selected for Apple Academy, in 2nd Year', description: 'Krishna cracked Apple’s prestigious Apple Academy while still at SST.' }),
          b('story_card', { name: 'Trackaroo', tag: 'SST', overlay: '₹25 Lakh Revenue · Clients Like Tata & Ather', description: 'Pratyush built a dealership management platform trusted by leading auto brands.' }),
          // Name pending in the master doc ("[Name] from Uttar Pradesh").
          b('story_card', { name: 'Product Intern at Fam', tag: 'SST', overlay: 'PM Intern at YC-Backed Fam · 2 Crore+ Users', description: 'A student from Uttar Pradesh builds products used by millions.' }),
          b('story_card', { name: 'Investing at Avendus', tag: 'SSB', overlay: 'Fresher → Investment Advisor, Avendus', description: 'Pranav Bagla stepped up to an investment advisory role after SSB.', image: img('/alumni/pranav-bagla.webp') }),
          b('story_card', { name: 'Chaubaraa', tag: 'SSB', overlay: '₹30L+ ARR', description: 'Three SSB students built a perfume brand inspired by familiar memories and emotions.', image: img('/deck/built/chaubaraa.webp') }),
          // Name pending in the master doc ("[Name] from Telangana").
          b('story_card', { name: 'Voice AI at 20', tag: 'SST', overlay: 'Backed by a Former JioHotstar Director', description: 'A student from Telangana is building a voice AI social concierge, two years after writing her first line of code.' }),
          b('story_card', { name: 'Onlyfeet', tag: 'SSB', overlay: '₹28L+ ARR', description: 'Mahnoor Z Mistry built a premium socks brand packaged in collectible cans for Gen Z.', image: img('/deck/built/onlyfeet.webp') }),
        ],
      }),

      b('bento_stats', {
        eyebrow: 'Stellar career prospects',
        headline: 'Stellar Career Prospects.',
        muted: 'Internships from your first year. Offers before you graduate.',
        tiles: [
          b('bento_tile', { size: 'wide', big: 'SSB’s founding cohort tripled its pay', line: '3.2x average salary hike, featured in The Times of India', tag: 'SSB PGP', image: img('/media/why-story-cohort.webp') }),
          b('bento_tile', { size: 'tall', big: '₹44 LPA', line: 'Offered via PPO to an undergraduate, before placement season even opened', tag: 'SST', image: img('/campus/class-session.webp'), video_label: 'Watch Video' }),
          b('bento_tile', { size: 'small', big: '₹20.4L', line: 'Average CTC for SST’s first undergraduate batch', tag: 'SST' }),
          b('bento_tile', { size: 'small', big: '100%', line: 'Internship placement across both SSB cohorts', tag: 'SSB PGP' }),
          b('bento_tile', { size: 'small', big: '₹2L/month', line: 'Highest internship stipend, earned in 2nd year', tag: 'SST' }),
          b('bento_tile', { size: 'small', big: '₹30.7L', line: 'Top 10% average CTC, SSB cohorts 1 & 2', tag: 'SSB PGP' }),
          b('bento_tile', { size: 'wide_short', big: '12+ Global internships', line: 'Bali, Singapore, New York and Germany', tag: 'SST', flags: '🇮🇩 🇸🇬 🇺🇸 🇩🇪' }),
        ],
      }),

      b('logo_wall', {
        eyebrow: 'Recruiters',
        headline: 'Our recruiter network.',
        muted: 'Startups, MNCs & AI companies.',
        logos: recruiterLogos,
      }),

      /* ---------------- Section 5: Innovation lab (as on SSB PGP) ---------------- */
      b('innovation_lab', {
        anchor: 'innovation-lab',
        eyebrow: 'Scaler Innovation Lab',
        headline: 'Network with industry leaders',
        muted: 'incubated in our startup ecosystem.',
        highlight: [
          b('story_card', {
            tag: 'Shark Tank India',
            overlay: 'NeoSapiens, a Scaler Innovation Lab startup, was funded on Shark Tank India.',
            description: 'A Scaler Innovation Lab startup won funding on Shark Tank India for its AI-native wearable pendant.',
            image: img('/media/lab-build-1890.webp', 'Students building hardware at Scaler Innovation Lab'),
          }),
        ],
        facts: [
          b('photo_card', { title: 'Shared Innovation Lab', text: '10+ startups incubated, ₹10Cr+ in revenue and $1B+ in valuations, on campus.', image: img('/media/lab-space-800.webp') }),
          b('photo_card', { title: '1:1 mentorship', text: 'From leaders at BCG, McKinsey, Paytm, Blinkit, Google, Zomato, Flipkart and Bain.', image: img('/media/lab-mentor-800.webp') }),
          b('photo_card', { title: 'VC Demo Days', text: 'Pitch to Peak XV, Tiger Global, Y Combinator, Entrepreneur First, Campus Fund and Mela Ventures.', image: img('/campus/navera-shark-tank.webp') }),
        ],
        startups_title: 'Startups from the lab',
        startups: [
          b('startup_card', { kind: 'Deep tech', name: 'Gahan AI', by: 'Sohini & Pallab · Co-founders', text: 'Automotive-grade mmWave radar for ADAS, smart infrastructure and industrial automation, built for Indian roads.', image: img('/startups/gahan-ai.webp'), url: 'https://gahanai.com/' }),
          b('startup_card', { kind: 'AI infrastructure', name: 'Maximem', by: 'Gaurav Dadhich · Founder', text: 'The memory layer for AI: your data stays encrypted, even from Maximem, so the agents you build can finally remember.', image: img('/startups/maximem.webp'), url: 'https://www.maximem.ai/' }),
          b('startup_card', { kind: 'Robotics', name: 'xSpecies AI', by: 'Srikanth V · Founder', text: 'Humanoid robots built to work safely and reliably in human spaces, from homes and retail to healthcare and logistics.', image: img('/startups/xspecies-ai.webp'), url: 'https://www.xspecies.ai/' }),
          b('startup_card', { kind: 'Biotech', name: 'Lemnisca Bio Tech', by: 'Dr & Dr · Co-founders', text: 'AI that predicts whether a small bioreactor formulation will stay stable at production scale, before the scale-up.', image: img('/startups/lemnisca-bio-tech.webp'), url: 'https://www.lemnisca.bio/' }),
          b('startup_card', { kind: 'Fintech', name: 'Handa Uncle', by: 'Ravi, Vikas & Madhuker · Co-founders', text: 'India’s AI-powered personal finance platform: unbiased money guidance that puts users first, not commissions.', image: img('/startups/handa-uncle.webp'), url: 'https://www.handauncle.com/' }),
          b('startup_card', { kind: 'AI wearables', name: 'Antimattr', by: 'Sridipto & Sirsho · Co-founders', text: 'MattrPods: an AI-powered audio wearable with a modular camera, for hands-free ambient computing through the day.', image: img('/startups/antimattr.webp'), url: 'https://www.antimattr.one/' }),
        ],
      }),

      /* ---------------- Section 6: Curriculum (5 pillars) ---------------- */
      b('learn_section', {
        anchor: 'curriculum',
        eyebrow: 'Curriculum',
        headline: 'How you learn.',
        muted: 'Every term ends in something you built.',
        pillars: [
          b('curriculum_pillar', {
            nav_label: 'Build real businesses',
            eyebrow: 'Build real businesses',
            headline: 'Learn business by running four of them.',
            chips: list('₹5 Cr venture fund', 'VC Demo Days with Peak XV, Tiger Global & more', 'SST students as tech co-founders', 'Scaler Innovation Lab & Content Creator Lab'),
            grid_title: 'The 4 businesses',
            grid: [
              b('feature_card', { title: 'MicroSaaS Tool', text: 'Build an AI tool that small businesses pay for.' }),
              b('feature_card', { title: 'D2C Brand', text: 'Launch a brand and sell it through India’s festive rush.' }),
              b('feature_card', { title: 'Content Channel', text: 'Grow an audience that buys and brings in brand deals.' }),
              b('feature_card', { title: 'Your Own Startup', text: 'Turn your best idea into a funded company.' }),
            ],
            carousel_title: 'Built by Scaler students',
            carousel: [
              b('project_card', { tag: 'MicroSaaS', metric: '₹25L revenue', name: 'Trackaroo', text: 'A dealership platform used by Tata and Ather' }),
              b('project_card', { tag: 'D2C', metric: '₹2 Cr', name: 'Dream Kit', text: 'A STEAM toy brand used by 12,000+ paying customers', image: img('/media/built/dreamkit.webp') }),
              b('project_card', { tag: 'Content', metric: '12.6M views', name: 'Tanisha Singhal', text: 'Tech events and resources, 13 brand deals', image: img('/immersions/tanisha-singhal.webp') }),
              b('project_card', { tag: 'Startup', metric: 'Y Combinator', name: 'Antimattr', text: 'Voice-first hardware, backed by WTFund', image: img('/startups/antimattr.webp') }),
              b('project_card', { tag: 'MicroSaaS', metric: '₹2L+ MRR', name: 'Ather Labs', text: 'A fintech startup built by Advith and Arsh' }),
              b('project_card', { tag: 'D2C', metric: '₹1 Cr+ ARR', name: 'Gredo', text: 'A protein brand live on Zomato and Swiggy', image: img('/media/built/gredo.webp') }),
              b('project_card', { tag: 'Content', metric: '11.2M views', name: 'Shubham Singh', text: 'Bollywood × Business', image: img('/immersions/shubham-singh.webp') }),
              b('project_card', { tag: 'Startup', metric: 'Shark Tank India', name: 'NeoSapiens', text: 'An AI-native wearable, funded by the Sharks' }),
            ],
          }),
          b('curriculum_pillar', {
            nav_label: 'Ship 4+ AI products',
            eyebrow: 'Master AI for business',
            headline: 'Ship 4+ AI products.',
            muted: 'No coding background needed.',
            subhead: 'Build in Scaler’s Innovation Lab, home to startups selected for Y Combinator and funded on Shark Tank India.',
            chips: list('500+ hours of applied AI', '30+ AI tools', '3 hackathons with SST', 'Mentors from OpenAI, Meta & Google'),
            grid_title: 'The 4 products you’ll ship',
            grid: [
              b('feature_card', { title: 'WhatsApp Customer Assistant', text: 'Answers queries and takes bookings for a local business', image: img('/deck/products/party.webp') }),
              b('feature_card', { title: 'AI Invoice & GST App', text: 'Turns bill photos into GST invoices', image: img('/deck/products/expense.webp') }),
              b('feature_card', { title: 'AI Sales Agent', text: 'Finds leads, writes outreach and books meetings', image: img('/deck/products/negotiation.webp') }),
              b('feature_card', { title: 'AI Voice Agent', text: 'Calls customers in Hindi and English', image: img('/deck/products/language.webp') }),
            ],
            tools_title: 'Tools you’ll use',
            tools: list('ChatGPT', 'Claude', 'Gemini', 'Lovable', 'Cursor', 'n8n', 'Zapier', 'ElevenLabs', 'Sarvam AI', '+21'),
            stepper_title: 'Your AI journey',
            stepper: [
              b('step', { label: 'Term 1', title: 'AI Foundations & No-Code Automation' }),
              b('step', { label: 'Term 2', title: 'AI for Marketing & Customer Research' }),
              b('step', { label: 'Term 3', title: 'AI for Finance & Operations' }),
              b('step', { label: 'Term 4', title: 'AI for Content, Storytelling & Pitching' }),
              b('step', { label: 'Term 5', title: 'AI Agents for Sales & Growth' }),
              b('step', { label: 'Term 6', title: 'AI Strategy, Costs & Responsible Use' }),
              b('step', { label: 'Year 4', title: 'Voice & Multimodal AI' }),
            ],
            carousel_title: 'Built with AI at Scaler',
            carousel: [
              b('project_card', { tag: 'AI hardware', metric: '₹25L Samsung grant', name: 'Percevia', text: 'AI glasses for the visually impaired' }),
              b('project_card', { tag: 'Robotics', metric: 'India’s first humanoid', name: 'Xspecies AI', text: 'Incubated at Scaler Innovation Lab', image: img('/media/lab-hand-1400.webp') }),
              b('project_card', { tag: 'Voice AI', metric: 'Real-time voice AI', name: 'Ninad AI', text: 'Speech that feels human' }),
              b('project_card', { tag: 'Voice AI', metric: 'Backed by an ex-JioHotstar Director', name: 'Voice AI concierge', text: 'Built by a 20-year-old student' }),
              b('project_card', { tag: 'EdTech', metric: 'AI exam grading', name: 'Gradesense', text: 'Grades handwritten answers at scale', image: img('/deck/built/gradesense.webp') }),
              b('project_card', { tag: 'Hackathon', metric: 'SIH 2025 winners', name: 'Team AntarDrishti', text: 'A solution chosen for national deployment' }),
            ],
          }),
          b('curriculum_pillar', {
            nav_label: 'Immersions',
            eyebrow: 'Learn beyond the classroom',
            headline: 'The best business lessons aren’t taught in a classroom.',
            subhead: 'Step onto factory floors, into dark stores and inside global HQs, and see how real companies make, sell and scale.',
            chips: list('6+ industry immersions', '2 global immersions', '1 every term'),
            grid_title: 'Global Immersions · ~1 week, in Years 2 and 3',
            grid: [
              b('feature_card', { tag: 'Startup hub', title: 'Singapore', subtitle: 'Year 2', text: 'Meet founders, investors and global tech teams in Asia’s startup capital, then pitch to an industry jury.', image: img('/media/singapore/supertrees.webp') }),
              b('feature_card', { tag: 'Trade & capital', title: 'Dubai', subtitle: 'Year 3 option', text: 'Visit free zones and ports, and family groups that took Indian businesses global.', }),
              b('feature_card', { tag: 'Manufacturing', title: 'China', subtitle: 'Year 3 option', text: 'Walk the electronics markets and factories that supply the world.' }),
              b('feature_card', { tag: 'Emerging markets', title: 'Southeast Asia', subtitle: 'Year 3 option', text: 'See how the next billion consumers are being served, from Jakarta to Ho Chi Minh City.', image: img('/media/singapore/dragon-boat.webp') }),
            ],
            carousel_title: 'Learn on the ground, across India.',
            carousel: [
              b('project_card', { tag: 'Term 1', name: 'Chickpet & SP Road, Bengaluru', text: 'Shadow a shopkeeper and see how India’s wholesale markets price, sell and give credit.', image: img('/media/bengaluru-vidhana-soudha-1280.webp') }),
              b('project_card', { tag: 'Term 2', name: 'Akshayakalpa', text: 'Follow organic milk from farm to fridge, and see how a farmer-first dairy built its brand.', image: img('/immersions/akshayakalpa.webp'), logo: img('/logos/akshayakalpa.webp') }),
              b('project_card', { tag: 'Term 3', name: 'Britannia', text: 'Walk the production line of one of India’s oldest FMCG brands, from mixing to packing.', image: img('/immersions/britannia.webp'), logo: img('/logos/britannia.webp') }),
              b('project_card', { tag: 'Term 4', name: 'Swiggy Instamart', text: 'Watch a 10-minute order get picked, packed and dispatched from a dark store.', image: img('/media/built/tally.webp'), logo: img('/logos/swiggy.svg') }),
              b('project_card', { tag: 'Term 5', name: 'Akshaya Patra', text: 'See how one kitchen cooks lakhs of mid-day meals a day, on a tight budget.', image: img('/immersions/farm-trip.webp') }),
              b('project_card', { tag: 'Term 6', name: 'Surat Textile Houses', text: 'Step inside a family-run mill in India’s fabric capital, and see how the next generation is modernising it.', image: img('/media/built/zari.webp') }),
            ],
          }),
          b('curriculum_pillar', {
            nav_label: 'Live consulting projects',
            eyebrow: 'Work on live projects',
            headline: 'Solve real case studies by known companies.',
            subhead: 'Solve live business problems for leading brands and family businesses, then defend your recommendations to the people who run them.',
            chips: list('4 live projects', 'Harvard Business School cases', 'Present to founders & leadership', 'Family business projects'),
            carousel_title: 'Projects you could work on',
            carousel: [
              b('project_card', { tag: 'International expansion', name: 'Mokobara', text: 'Design the APAC expansion plan for a ₹200 Cr luggage brand.', image: img('/live-projects/mokobara.jpg'), logo: img('/logos/marks/fc-mokobara.png') }),
              b('project_card', { tag: 'Conversion', name: 'Ajio', text: 'Find where shoppers drop off between discovery and checkout, and fix it.', image: img('/live-projects/ajio.jpg'), logo: img('/logos/live/ajio.svg') }),
              b('project_card', { tag: 'Healthcare growth', name: 'Practo', text: 'Grow healthcare transactions across primary, secondary and tertiary care.', image: img('/live-projects/practo.jpg'), logo: img('/logos/live/practo.svg') }),
              b('project_card', { tag: 'Go-to-market', name: 'Quenzy', text: 'Find product-market fit and plan the launch for an emerging brand.', image: img('/live-projects/quenzy.jpg') }),
              b('project_card', { tag: 'App launch', name: 'Meolaa', text: 'Build the roadmap for launching a new consumer app.', image: img('/live-projects/meolaa.jpg'), logo: img('/logos/live/meolaa.png') }),
              b('project_card', { tag: 'Family business', name: 'Your family’s business', text: 'Diagnose the business and build its digital, export or AI growth plan.', image: img('/media/built/tally.webp') }),
            ],
          }),
          b('curriculum_pillar', {
            nav_label: 'Internships from Year 1',
            eyebrow: 'Internships from Year 1',
            headline: 'Every student interns.',
            stats: internshipStats(),
            carousel_title: 'Where Scaler students intern',
            carousel: internshipCards(),
          }),
        ],
      }),

      /* ---------------- Section 7: Campus life and peer group ---------------- */
      b('campus_gallery', {
        anchor: 'campus-life',
        eyebrow: 'Campus life',
        headline: 'Life beyond the classroom.',
        muted: 'A lively campus and a peer group shared with SST and SSB.',
        subhead: 'Snapshots from SST & SSB cultural events, sports, clubs and the Bengaluru campus.',
        tabs: campusTabs(),
        video: img('/media/campus-film.mp4'),
        video_poster: img('/media/campus-film-poster.jpg'),
        video_label: 'Take the campus tour',
      }),

      /* ---------------- Section 8: Super Mentor sessions & events (from SSB) ---------------- */
      b('sessions', {
        eyebrow: 'Super Mentor sessions & events',
        headline: 'Super Mentor Sessions.',
        muted: 'Leaders from Google, Blinkit, PhonePe and OpenAI.',
        subhead: 'Mentored by India’s top business leaders.',
        items: [
          b('session_card', { name: 'Rajan Anandan', role: 'Ex-MD SEA, Google', text: 'He spoke about striving for excellence, learning from failure, and staying hungry for success.', video_url: 'https://www.youtube.com/watch?v=M7H1SHc1f2Q', image: img('/sessions/rajan-anandan.webp'), logo: img('/sessions/rajan-anandan-logo.png', 'Google') }),
          b('session_card', { name: 'Jacob Singh', role: 'Ex-CTO, Blinkit, India’s Largest Q-Commerce', text: 'He shared deep insights on tech leadership and product thinking with the students.', video_url: 'https://www.youtube.com/watch?v=QMjFvjBwuE4', image: img('/sessions/jacob-singh.webp'), logo: img('/sessions/jacob-singh-logo.png', 'Blinkit') }),
          b('session_card', { name: 'Rahul Chari', role: 'Co-Founder, PhonePe (India’s largest UPI app)', text: 'Rejected by Google, built a leading UPI platform. A journey of grit and innovation.', video_url: 'https://www.youtube.com/watch?v=fN43OAasN5w', image: img('/sessions/rahul-chari.webp'), logo: img('/sessions/rahul-chari-logo.png', 'PhonePe') }),
          b('session_card', { name: 'Yash Kumar', role: 'Lead Engineer, OpenAI (ChatGPT Agents)', text: 'The creator of OpenAI’s first agent, addressed students on Commencement Day.', video_url: 'https://www.youtube.com/watch?v=5R95YlIdeBg', image: img('/sessions/yash-kumar.webp'), logo: img('/sessions/yash-kumar-logo.png', 'OpenAI') }),
        ],
      }),

      /* ---------------- Section 9: Hear from our students ---------------- */
      b('testimonials', {
        eyebrow: 'Student stories',
        headline: 'Hear from our students',
        muted: 'from the Scaler ecosystem.',
        items: [
          b('video_card', { title: 'Created GTM strategy', caption: 'Akarsh · Created GTM strategy', image: img('/testimonials/akarsh.webp') }),
          b('video_card', { title: 'Career pivot', caption: 'Yukthi · Career pivot, operations to strategy', image: img('/testimonials/yukthi.webp') }),
          b('video_card', { title: 'Building a Shark Tank funded startup', caption: 'Moh · Building a Shark Tank funded startup', image: img('/testimonials/moh.webp') }),
          b('video_card', { title: 'From CA to Private Equity', caption: 'Ayush · From CA to Private Equity', image: img('/testimonials/ayush.webp') }),
          b('video_card', { title: 'From Fintech intern to Founder’s Office', caption: 'Yash · From fintech intern to Founder’s Office', image: img('/testimonials/yash.webp') }),
        ],
      }),

      /* ---------------- Section 10: Eligibility, admission process ---------------- */
      b('admissions_summary', {
        anchor: 'admissions',
        eyebrow: 'Admissions',
        headline: 'Eligibility, admission process,',
        muted: 'fees & scholarships.',
        criteria: [
          b('criterion', { title: 'Education', text: 'Currently in Class XII or passed Class XII in 2026, with a minimum of 60% from a recognised board. Open to all streams.' }),
          b('criterion', { title: 'Initiative', text: 'Ideal for students with a strong track record of initiative, such as clubs, competitions, sports, side projects or a business of their own.' }),
          b('criterion', { title: 'Profile-Based Evaluation', text: 'We evaluate your academics, SSAT score, extracurricular achievements and leadership, along with your motivation to build.' }),
        ],
        steps: [
          b('step', { label: 'Step 1', title: 'Information Session', text: 'Attend a mandatory 30-minute live session covering the programme, fees and scholarships.' }),
          b('step', { label: 'Step 2', title: 'Scholarship & Aptitude Test', text: 'Take the 70-minute online SSAT, which assesses admission and scholarship eligibility.' }),
          b('step', { label: 'Step 3', title: 'Application Online', text: 'Submit your application with academic records, achievements and a video essay and pay the application fee.' }),
          b('step', { label: 'Step 4', title: 'Interview Rounds', text: 'Shortlisted candidates appear for an online interview, followed by a case interview with senior leadership.' }),
          b('step', { label: 'Step 5', title: 'Offer & Acceptance', text: 'Receive your decision, then confirm your seat within 10 days of the offer.' }),
        ],
        cta_label: 'Book your info session',
        cta_href: 'lead:info-session',
        link_label: 'For more info about fees & scholarships',
        link_href: '/admission',
      }),

      /* ---------------- Section 11: FAQs ---------------- */
      b('faq', {
        anchor: 'faq',
        eyebrow: 'FAQs',
        headline: 'Questions, answered.',
        muted: 'For students and parents.',
        cta_label: 'Book your info session',
        cta_href: 'lead:info-session',
        items: [
          b('faq_item', { question: 'Who can apply?', answer: 'Students currently in Class XII, or who passed Class XII in 2026, with a minimum of 60% in Class XII from a recognised board (CBSE, ISC, state boards, IB, IGCSE or equivalent). The programme is open to all streams: science, commerce and humanities.' }),
          b('faq_item', { question: 'What does the admission process look like?', answer: 'Five steps: a mandatory 30-minute information session, the 70-minute online SSB Scholarship & Aptitude Test (SSAT), an online application with a video essay, two interview rounds, and the admission decision.' }),
          b('faq_item', { question: 'Can I skip the SSAT?', answer: 'Yes. Candidates with qualifying JEE, SAT, CUET or IPMAT scores may skip the SSAT and proceed directly to the application.' }),
          b('faq_item', { question: 'What is the application fee?', answer: 'The application fee is ₹1,000, paid when you submit your online application.' }),
          b('faq_item', { question: 'How much are the fees?', answer: 'The total programme fee is ₹39.5 lakh over four years: a ₹50,000 admission fee to confirm your seat, plus tuition fees payable term-wise. Hostel is optional, and the full fee structure is on the Admission & Fees page.' }),
          b('faq_item', { question: 'Are scholarships available?', answer: 'Yes. Scholarships are awarded based on SSAT performance, interviews and the overall profile, and all applicants are considered automatically. They include Merit, Builder, Leadership, Sports, Women in Business, Merit-cum-Need and Early Applicant scholarships.' }),
          b('faq_item', { question: 'When does the programme start, and where?', answer: 'The first batch starts in August 2027, on the Scaler campus in Bengaluru. There are only 100 seats.' }),
          b('faq_item', { question: 'When is the Early Round deadline?', answer: '31st December 2026, 11:59 PM. The early-applicant scholarship is available only in the Early Round.' }),
        ],
      }),

      closingCta(),
    ],
  }),
};
