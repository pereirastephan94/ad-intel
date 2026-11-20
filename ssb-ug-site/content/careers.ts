// Source: master doc → tab "Pg 4: Career pathways". Copy kept word for word.
import type { Story } from '@/lib/types';
import { b, img, imgs, list, stat } from './helpers';
import { closingCta, internshipCards, internshipStats, recruiterLogos, explorePages } from './shared';

const card = (name: string, by: string, overlay: string, description: string, tag: string, image?: string) =>
  b('story_card', { name, by, overlay, description, tag, ...(image ? { image: img(image, name) } : {}) });

const journey = (name: string, from: string, to: string, image?: string) => b('journey', { name, from, to, ...(image ? { image: img(image, name) } : {}) });

export const careers: Story = {
  name: 'Career pathways',
  slug: 'career-pathways',
  full_slug: 'career-pathways',
  content: b('page', {
    seo_title: 'Career pathways',
    seo_description: 'Three career pathways, one programme: your own startup, your family business or placements, backed by Scaler’s ecosystem and 1,200+ hiring partners.',
    body: [
      b('page_intro', {
        eyebrow: 'Career pathways',
        headline: 'Backed by Scaler’s ecosystem.',
        muted: 'A legacy of 10+ years in practical education.',
        subhead: 'Get access to Scaler School of Business, Scaler School of Technology, the Scaler Innovation Lab and Scaler’s 1,200+ hiring network.',
        image: img('/media/why-story-cohort.webp', 'SSB graduates at convocation'),
        primary_cta_label: 'Join the early waitlist',
        primary_cta_href: 'lead:waitlist',
      }),
      b('stat_strip', {
        items: [
          stat('1,200+', 'Scaler hiring partners'),
          stat('₹44 LPA', 'Highest CTC (SST)'),
          stat('3.2x', 'Average salary hike (SSB)'),
          stat('₹2 Cr+', 'ARR from a student startup (SSB)'),
        ],
      }),
      b('pathways', {
        anchor: 'pathways',
        eyebrow: 'Your path',
        headline: '3 career pathways.',
        muted: 'One programme.',
        items: [
          b('pathway', {
            title: 'Own Startup',
            text: 'You build four businesses in four years at Scaler’s innovation lab with a seed funding pool of 5cr+, AI tools and SST tech co-founders, and pitch to 50+ investors at VC Demo Day.',
            image: img('/media/lab-build-1890.webp'),
          }),
          b('pathway', {
            title: 'Family Business',
            text: 'You take electives in succession, working capital and exports, learn from mentors who run family businesses, and work on a live project to modernise and scale your family business in Year 4.',
            image: img('/media/built/zari.webp'),
          }),
          b('pathway', {
            title: 'Placements',
            text: 'You build your profile through 3 internships and live projects with brands like Ajio and Mokobara, get career prep in Year 3, and land a PPO or an on-campus offer from 1,200+ hiring partners.',
            image: img('/campus/class-case-study.webp'),
          }),
        ],
      }),

      /* ---------------- Entrepreneurship outcomes ---------------- */
      b('outcome_group', {
        anchor: 'entrepreneurship',
        tag: 'SSB PGP',
        headline: 'Entrepreneurship outcomes.',
        muted: 'Ventures built by SSB students.',
        stats: [stat('₹2 Cr+', 'Highest venture revenue'), stat('₹1 Cr+', 'ARR consumer brand'), stat('₹30L+', 'ARR'), stat('₹28L+', 'ARR')],
        cards: [
          card('Dream Kit', 'Aashish US', '₹2 Cr · 12,000+ students', 'A STEAM toy brand used across schools, built while working full-time at The Whole Truth.', 'D2C', '/deck/built/dream-kit.webp'),
          card('Gredo', 'Sanskriti Deshmukh', '₹1 Cr+ ARR', 'A protein-food brand live on Zomato and Swiggy, with vending machines across Bengaluru.', 'D2C', '/deck/built/gredo.webp'),
          card('Chaubaraa', 'Chavda Tirthrajsinh, Geetika Mehta, Malika Gupta', '₹30L+ ARR', 'Perfumes inspired by familiar memories and emotions.', 'D2C', '/deck/built/chaubaraa.webp'),
          card('Onlyfeet', 'Mahnoor Z Mistry', '₹28L+ ARR', 'Premium novelty socks in collectible cans for Gen Z.', 'D2C', '/deck/built/onlyfeet.webp'),
          card('Gradesense', 'Ayush Poojary', 'AI platform', 'Grades handwritten and descriptive exams at scale.', 'AI', '/deck/built/gradesense.webp'),
          card('Tally Konnect', 'Moh Agarwal', 'Family business', 'Scaled through a new ERP automation platform.', 'Family business', '/deck/built/tally-konnect.webp'),
        ],
      }),
      b('outcome_group', {
        tone: 'dark',
        tag: 'SST UG',
        headline: 'Startups from Scaler School of Technology.',
        stats: [stat('10+', 'Startups founded by students'), stat('7+', 'Deep-tech startups incubated'), stat('₹2 Cr+', 'Innovation Lab fund')],
        cards: [
          card('Antimattr', 'Backed by Y Combinator', 'Backed by Y Combinator', 'Voice-first AI hardware, backed by Nikhil Kamath’s WTFund.', 'AI hardware', '/startups/antimattr.webp'),
          card('NeoSapiens', 'Funded on Shark Tank India', 'Funded on Shark Tank India', 'Funded for its AI-native wearable pendant.', 'AI wearable'),
          card('Percevia', 'Tushar', '₹25L Samsung grant', 'AI glasses for the visually impaired, chosen from 20,000+ entries.', 'AI hardware'),
          card('Trackaroo', 'Pratyush', '₹25L revenue', 'A dealership platform with clients like Tata and Ather.', 'SaaS'),
          card('Ather Labs', 'Advith & Arsh', '₹2L+ MRR', 'An AI-powered fintech startup.', 'Fintech'),
          card('Xspecies AI', 'India’s first humanoid', 'India’s first humanoid', 'A robotics startup incubated at the Innovation Lab.', 'Robotics', '/startups/xspecies-ai.webp'),
        ],
      }),

      /* ---------------- Placement outcomes ---------------- */
      b('outcome_group', {
        anchor: 'placements',
        tone: 'muted',
        tag: 'SSB PGP',
        headline: 'Placement outcomes.',
        muted: 'Our founding cohort tripled its pay.',
        stats: [
          stat('3.2x', 'Average salary hike (Cohort 1)'),
          stat('₹19L', 'Average CTC (Cohort 1)'),
          stat('₹21L', 'Average CTC (Cohort 2, ongoing)'),
          stat('₹26L', 'Top 25% average CTC'),
          stat('₹30.7L', 'Top 10% average CTC'),
          stat('500+', 'Hiring companies'),
        ],
        logos_title: 'Companies on campus',
        logos: recruiterLogos.slice(0, 12),
        journeys_title: 'Career journeys',
        journeys: [
          journey('Sagnik Banerjee', 'Project Lead', 'Sr. Strategy Manager, Urban Company', '/alumni/sagnik-banerjee.webp'),
          journey('Uttara Nambiar', 'Software Developer', 'Asst. Program Manager, Blinkit', '/alumni/uttara-nambiar.webp'),
          journey('Suhaas Sastry', 'Sales Engineer', 'Partnerships, Razorpay', '/alumni/suhaas-sastry.webp'),
          journey('Pranav Bagla', 'Investment Analyst', 'Investment Advisor, Avendus', '/alumni/pranav-bagla.webp'),
          journey('Kritika Bhatia', 'Financial Analyst', 'Growth Marketing, Emergent', '/alumni/kritika-bhatia.webp'),
          journey('Bharath Ramesh', 'Executive', 'Growth Manager, Ninjacart', '/alumni/bharath-ramesh.webp'),
        ],
      }),
      b('outcome_group', {
        tag: 'SST UG',
        headline: 'Offers before placement season.',
        stats: [stat('₹44 LPA', 'Highest CTC, via PPO'), stat('₹33L', 'Top 25% average CTC'), stat('₹20.4L', 'Average CTC')],
        logos_title: 'Companies on campus',
        logos: imgs('/logos/amazon.svg', '/logos/rippling.svg'),
        names_title: 'Also hiring: ',
        names: list('Mamaearth', 'Slice', 'Medianet', '1 Pharmacy'),
        journeys_title: 'Internship + PPO highlights',
        journeys: [
          journey('Ananya Srivastava', '3rd Year', 'Wealthy'),
          journey('Shubh Kesharwani', '3rd Year', 'Tasket'),
          journey('Abhishek Kumar Shah', '3rd Year', 'Emergent'),
          journey('Divyanshu Pandey', '3rd Year', 'Mamaearth'),
        ],
      }),

      /* ---------------- Internship outcomes ---------------- */
      b('outcome_group', {
        anchor: 'internships',
        tone: 'muted',
        headline: 'Internship outcomes.',
        muted: 'Every Student Interns.',
        stats: internshipStats(),
        cards_title: 'Internship highlights',
        card_style: 'project',
        cards: internshipCards(),
        cta_label: 'Download the audited report',
        cta_href: 'lead:brochure',
      }),
      explorePages('career-pathways'),
      closingCta(),
    ],
  }),
};
