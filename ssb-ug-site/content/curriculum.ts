// Source: master doc → tab "Pg 2: Curriculum". Copy kept word for word.
import type { Story } from '@/lib/types';
import { b, img } from './helpers';
import { closingCta, explorePages } from './shared';

const row = (label: string, text: string) => b('term_row', { label, text });

export const curriculum: Story = {
  name: 'Curriculum',
  slug: 'curriculum',
  full_slug: 'curriculum',
  content: b('page', {
    seo_title: 'Curriculum',
    seo_description: 'Four years, eight terms: start with foundations and graduate into 3 career pathways: your own startup, a campus placement or your family business.',
    body: [
      b('page_intro', {
        eyebrow: 'Curriculum',
        headline: 'Curriculum that goes beyond classrooms.',
        subhead: 'Start with foundations to graduate into 3 career pathways: your own startup, a campus placement or your family business.',
        image: img('/campus/class-group-work.webp', 'Students working in groups at SSB'),
        primary_cta_label: 'Download Brochure',
        primary_cta_href: 'lead:brochure',
        secondary_cta_label: 'Join the early waitlist',
        secondary_cta_href: 'lead:waitlist',
      }),
      b('year_block', {
        anchor: 'year-1',
        label: 'Year 1',
        title: 'Foundational Learning',
        text: 'Understand how businesses and AI work and apply the fundamentals by launching your first business and acquiring real customers.',
        image: img('/media/d2c-bazaar-800.webp'),
        terms: [
          b('term', {
            title: 'Term 1',
            months: 'August to December',
            outcome: 'You learn to turn a problem into a product people buy.',
            rows: [
              row('Term project', 'MicroSaaS Tool, built in teams of three on no-code platforms'),
              row('Beyond the classroom', 'Orientation Week street-selling challenge in Bengaluru'),
              row('In class', 'Critical Thinking & Problem Structuring · Principles of Microeconomics · Business Communication, Storytelling & Digital Presence · Business Statistics · Introduction to Entrepreneurship · AI Foundations & No-Code Automation · Excel & PowerPoint Foundations'),
              row('Immersions', 'Small business and markets (Chickpet, SP Road, Yeshwanthpur APMC) · Winter trek'),
            ],
          }),
          b('term', {
            title: 'Term 2',
            months: 'January to May',
            outcome: 'You learn to launch and run your own D2C brand.',
            rows: [
              row('Term project', 'D2C Brand Launch, with ₹50,000 in seed funding per team'),
              row('Beyond the classroom', 'AI Product 1, a WhatsApp Customer Assistant for your brand or a local business · SSB × SST Hackathon 1 · Stockathon, a live trading simulation'),
              row('In class', 'Financial Accounting · Marketing Management · Consumer Behaviour & Market Research · Macroeconomics & the Indian Economy · Organisational Behaviour & Teamwork · AI for Marketing & Customer Research'),
              row('Immersions', 'Farm to brand (Akshayakalpa, a Coorg coffee estate, Mysore Silk)'),
              row('Summer', "Internship opportunity in a founder's office (8 weeks)"),
            ],
          }),
        ],
      }),
      b('year_block', {
        anchor: 'year-2',
        tone: 'muted',
        label: 'Year 2',
        title: 'Core Competency Development',
        text: 'Learn to manage core business functions and use data, technology and business strategy to grow an existing venture.',
        image: img('/immersions/britannia.webp'),
        terms: [
          b('term', {
            title: 'Term 3',
            months: 'August to December',
            outcome: 'You learn to manage a business through its busiest season.',
            rows: [
              row('Term project', 'Festive Season Launch, on your own online store and one marketplace'),
              row('Beyond the classroom', 'AI Product 2, an AI Invoice & GST App used by 5 small businesses'),
              row('In class', 'Managerial Accounting & Costing · Operations & Supply Chain Management · Sales & Distribution in India · Introduction to Product Management · Business Law, Ethics & Governance · AI for Finance & Operations'),
              row('Immersions', 'Consumer goods manufacturing (Britannia, MTR Foods, Titan) · Winter: Singapore (Block71, Singapore Exchange, SMU)'),
            ],
          }),
          b('term', {
            title: 'Term 4',
            months: 'January to May',
            outcome: 'You learn to grow a business using content and social media.',
            rows: [
              row('Term project', 'Content-creation, through a channel for your own product or a niche you choose'),
              row('Beyond the classroom', 'Live Project 1 with a national brand (e.g. Ajio) · SSB × SST Hackathon 2'),
              row('In class', 'Corporate Finance · Business Strategy · Digital & Social Media Marketing · Data Analytics & Visualisation · Negotiation & Influence · AI for Content, Storytelling & Pitching'),
              row('Immersions', 'Quick commerce and retail (Zepto, Swiggy Instamart, a Flipkart fulfilment centre)'),
              row('Summer', 'Internship opportunity at a startup or company (8 weeks)'),
            ],
          }),
        ],
      }),
      b('year_block', {
        anchor: 'year-3',
        label: 'Year 3',
        title: 'Advanced Integration & Specialisation',
        text: 'Develop deep expertise in your chosen business specialisation and build a scalable venture, pitching to investors at VC Demo Day.',
        tracks: 'Finance\nMarketing & Branding\nTech, Data & Product\nStrategy & Operations\nFamily Business (optional)',
        image: img('/media/singapore/marina-dusk.webp'),
        terms: [
          b('term', {
            title: 'Term 5',
            months: 'August to December',
            outcome: 'You learn to start a venture in your chosen field.',
            rows: [
              row('Term project', 'HUSTLE Pre-Seed, with ₹50,000 in seed funding per team'),
              row('Beyond the classroom', 'AI Product 3, an AI Sales Agent that books meetings for a real company · Live Project 2 (e.g. Practo) · SSB × SST Hackathon 3, your chance to find a tech co-founder'),
              row('In class', 'New Venture Creation · Building AI Agents for Sales & Growth · 3 electives in your track · Career Practicum I (optional)'),
              row('Immersions', 'Social impact (Akshaya Patra, SELCO Foundation, Hasiru Dala) · Winter: Dubai, China or Southeast Asia'),
            ],
          }),
          b('term', {
            title: 'Term 6',
            months: 'January to May',
            outcome: 'You learn to grow a venture and raise funding.',
            rows: [
              row('Term project', 'HUSTLE MVP and Investor Demo Day, where selected teams join Innovation Lab incubation'),
              row('Beyond the classroom', 'Live Project 3 (e.g. Mokobara)'),
              row('In class', 'Venture Finance & Fundraising · AI Strategy, Costs & Responsible Use · 3 electives in your track · Career Practicum II (optional)'),
              row('Immersions', 'Family-run businesses (Surat textiles, TVS Motor, Himalaya Wellness)'),
              row('Summer', 'Internship opportunity in your specialisation (8 to 10 weeks), or full-time work on your venture if incubated'),
            ],
          }),
        ],
      }),
      b('year_block', {
        anchor: 'year-4',
        tone: 'muted',
        label: 'Year 4',
        title: 'Industry Readiness',
        text: 'Apply your learnings through a capstone project in your specialisation and choose your path: startup, family business, or placements.',
        image: img('/media/why-story-cohort-800.webp'),
        terms: [
          b('term', {
            title: 'Term 7',
            months: 'August to December',
            outcome: 'You learn to solve real problems for an established company.',
            rows: [
              row('Term project', 'Industry Capstone, a live project with a partner company'),
              row('Beyond the classroom', 'AI Product 4, a Hindi-English AI Voice Agent that makes 200+ calls for a real business'),
              row('In class', 'Leadership & People Management · Building Voice & Multimodal AI Agents'),
            ],
          }),
          b('term', {
            title: 'Term 8',
            months: 'January to May',
            outcome: 'You step into your path: your startup, your family business or a job.',
            rows: [
              row('Build your startup', 'Selected founders continue at the Innovation Lab'),
              row('Grow your family business', "Lead an initiative in your family's business"),
              row('Sit for campus placements', 'With startups and MNCs'),
            ],
          }),
        ],
      }),
      explorePages('curriculum'),
      closingCta(),
    ],
  }),
};
