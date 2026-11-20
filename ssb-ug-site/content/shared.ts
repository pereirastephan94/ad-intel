// Blocks reused on more than one page. Copy from the master doc
// ("SSB UG: Website copy") unless marked as borrowed from the SSB PGP site.
import { b, img, imgs, list } from './helpers';

export const recruiterLogos = imgs(
  '/logos/amazon.svg',
  '/logos/goldman-sachs.svg',
  '/logos/ey.svg',
  '/logos/nomura.svg',
  '/logos/samsung.svg',
  '/logos/uber.svg',
  '/logos/razorpay.svg',
  '/logos/swiggy.svg',
  '/logos/zomato.svg',
  '/logos/freshworks.svg',
  '/logos/blinkit.svg',
  '/logos/phonepe.svg',
  '/logos/myntra.svg',
  '/logos/urban-company.svg',
  '/logos/groww.png',
  '/logos/bharatpe.png',
  '/logos/lenskart.svg',
  '/logos/zepto.svg',
  '/logos/arcelormittal.svg',
  '/logos/pine-labs.svg',
  '/logos/bigbasket.svg',
  '/logos/oyo.png',
  '/logos/zendesk.svg',
  '/logos/vedantu.png',
);

// Internship highlights (master doc: Pg 1 Pillar 5 and Pg 4 Internship outcomes).
export const internshipCards = () => [
  b('project_card', { tag: 'Apple', name: 'Krishna', text: 'Selected for Apple Academy in his 2nd year (SST)' }),
  b('project_card', { tag: 'Razorpay', name: 'Sarosha Pais', text: 'Moved from HR into Partnerships (SSB)', logo: img('/logos/razorpay.svg') }),
  b('project_card', { tag: 'Singapore', name: 'Sourashish Sarkar', text: 'Interning in Singapore at ₹2L/month (SST)', image: img('/media/singapore/cbd-sunset.webp') }),
  b('project_card', { tag: 'The Whole Truth', name: 'Aashish US', text: 'Founder to Brand Marketing (SSB)', image: img('/alumni/aashish-us.webp'), logo: img('/logos/marks/wholetruth.svg') }),
  b('project_card', { tag: 'Fam (YC-backed)', name: 'Shruti', text: 'PM intern on products used by 2 crore+ people (SST)' }),
  b('project_card', { tag: 'Pync', name: 'Akarsh Sharma', text: "Data Analyst at Uber to Founder's Office (SSB)", image: img('/testimonials/akarsh.webp'), logo: img('/internship/marks/pync.png') }),
  b('project_card', { tag: '2 internships at once', name: 'Om', text: 'Cracked 2 internships in his 2nd year (SST)' }),
  b('project_card', { tag: 'Vincere Partners', name: 'Yukthi N Hanji', text: 'Data Management to Investment Banking (SSB)', image: img('/testimonials/yukthi.webp') }),
  b('project_card', { tag: 'SpotDraft', name: 'Chandana Mendan', text: 'Software Engineer to Associate Product Manager (SSB)', logo: img('/internship/logos/spotdraft.png') }),
];

export const internshipStats = () => [
  b('stat', { value: '96%', label: 'Secured internships by 2nd year' }),
  b('stat', { value: '₹2L/month', label: 'Highest internship stipend' }),
  b('stat', { value: '150+', label: 'Companies have hired our interns' }),
  b('stat', { value: '12', label: 'Global internships, from Bali to New York' }),
  b('stat', { value: '52%+', label: "In Product & Founder's Office roles" }),
];

export const campusTabs = () => [
  b('gallery_tab', {
    label: 'Campus',
    images: imgs('/campus/cohort.webp', '/campus/arch.webp', '/campus/building.webp', '/campus/residence-courtyard.webp', '/media/campus-entrance-1280.webp'),
  }),
  b('gallery_tab', {
    label: 'Classrooms',
    images: imgs('/campus/class-session.webp', '/campus/class-discussion.webp', '/campus/class-group-work.webp', '/campus/class-case-study.webp', '/campus/classroom.webp'),
  }),
  b('gallery_tab', {
    label: 'Sports & gym',
    images: imgs('/campus/cricket-winners.webp', '/campus/basketball.webp', '/campus/badminton.webp', '/campus/gym.webp', '/campus/cricket-floodlights.webp'),
  }),
  b('gallery_tab', {
    label: 'Clubs',
    images: imgs('/campus/club-consulting.webp', '/campus/club-marketing.webp', '/campus/club-case-crunch.webp', '/campus/club-guest-session.webp', '/campus/club-whiteboard.webp'),
  }),
  b('gallery_tab', {
    label: 'Fests & events',
    images: imgs('/campus/navera-awards.webp', '/campus/navera-standup.webp', '/campus/navera-shark-tank.webp', '/campus/navera-music.webp', '/campus/warikoo-fireside.webp'),
  }),
  b('gallery_tab', {
    label: 'Cultural',
    images: imgs('/campus/holi-colours.webp', '/campus/music-night.webp', '/campus/prom.webp', '/campus/navera-music.webp', '/campus/anupam-session.webp'),
  }),
];

export const closingCta = (headline = 'Build 4 businesses before you graduate.') =>
  b('cta_band', {
    eyebrow: 'Early Round · Applications close 31st December 2026',
    headline,
    muted: 'Join the first SSB UG batch, August 2027.',
    text: 'Only 100 seats. Scholarships are limited, and applying early increases your chances of receiving one.',
    image: img('/footer/campus.webp'),
    primary_cta_label: 'Join the early waitlist',
    primary_cta_href: 'lead:waitlist',
    secondary_cta_label: 'Book your info session',
    secondary_cta_href: 'lead:info-session',
  });

export const programmeFacts = list('4 years, incl. internships & study abroad', 'Bengaluru campus', 'Only 100 seats');
