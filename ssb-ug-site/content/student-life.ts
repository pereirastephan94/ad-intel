// Source: master doc → tab "Pg 5: Student life" ("Snapshots and videos from
// SST & SSB cultural events - premium and lively"). Images from the SSB site.
import type { Story } from '@/lib/types';
import { b, img } from './helpers';
import { campusTabs, closingCta } from './shared';

export const studentLife: Story = {
  name: 'Student life',
  slug: 'student-life',
  full_slug: 'student-life',
  content: b('page', {
    seo_title: 'Student life',
    seo_description: 'Life on the Scaler campus in Bengaluru: classrooms, clubs, sports, fests and cultural nights with SST & SSB peers.',
    body: [
      b('page_intro', {
        eyebrow: 'Student life',
        headline: 'Life beyond the classroom.',
        muted: 'A fully residential campus in Bengaluru.',
        subhead: 'Snapshots and videos from SST & SSB cultural events, clubs, sports and campus life.',
        image: img('/campus/holi-colours.webp', 'Students celebrating Holi on campus'),
        primary_cta_label: 'Join the early waitlist',
        primary_cta_href: 'lead:waitlist',
      }),
      b('campus_gallery', {
        eyebrow: 'On campus',
        headline: 'Campus, clubs and culture.',
        muted: 'Shared with SST and SSB peers.',
        tabs: campusTabs(),
        video: img('/media/campus-film.mp4'),
        video_poster: img('/media/campus-film-poster.jpg'),
        video_label: 'Take the campus tour',
      }),
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
      closingCta(),
    ],
  }),
};
