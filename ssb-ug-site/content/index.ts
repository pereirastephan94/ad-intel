import type { Story } from '@/lib/types';
import { b } from './helpers';
import { home } from './home';
import { curriculum } from './curriculum';
import { admission } from './admission';
import { careers } from './careers';
import { studentLife } from './student-life';

const link = (label: string, href: string) => b('nav_link', { label, href });

// Global settings (header, announcement bar, footer). In Storyblok this is the
// "config" story, so the team can change the nav or the deadline without code.
export const config: Story = {
  name: 'Config',
  slug: 'config',
  full_slug: 'config',
  content: b('site_config', {
    announcement: 'Early Round applications close on 31st December 2026, 11:59 PM',
    deadline: '2026-12-31T23:59:00+05:30',
    cta_label: 'Join the early waitlist',
    cta_href: 'lead:waitlist',
    nav: [
      link('Home', '/'),
      link('Curriculum', '/curriculum'),
      link('Admission & Fees', '/admission'),
      link('Career Pathways', '/career-pathways'),
      link('Student Life', '/student-life'),
      link('FAQs', '/#faq'),
    ],
    footer_blurb: 'UG programme in Business, Entrepreneurship & AI. Four years on the Scaler campus in Bengaluru, first batch August 2027.',
    address: 'Scaler School of Business, Bengaluru, Karnataka',
    footer_columns: [
      b('footer_column', {
        title: 'Programme',
        links: [link('Curriculum', '/curriculum'), link('Career Pathways', '/career-pathways'), link('Student Life', '/student-life'), link('Faculty', '/#faculty')],
      }),
      b('footer_column', {
        title: 'Admissions',
        links: [link('Eligibility', '/admission#eligibility'), link('Process', '/admission#process'), link('Fees', '/admission#fees'), link('Scholarships', '/admission#scholarships')],
      }),
      b('footer_column', {
        title: 'Scaler',
        links: [
          link('Scaler School of Business', 'https://www.scaler.com/school-of-business/'),
          link('Instagram', 'https://www.instagram.com/scalerschool_of_business/'),
          link('FAQs', '/#faq'),
        ],
      }),
    ],
    copyright: '© 2026 Scaler School of Business. All rights reserved.',
    footnote: 'SSB UG welcomes its first batch in 2027. Outcomes shown are from Scaler’s existing programmes.',
  }),
};

export const localStories: Record<string, Story> = {
  home,
  curriculum,
  admission,
  'career-pathways': careers,
  'student-life': studentLife,
  config,
};
