// Source: master doc → tab "Pg 3: Admission & Fees". Copy kept word for word.
// Application fee (₹1,000, discount codes later) confirmed by Stephan, 20 Nov 2026.
import type { Story } from '@/lib/types';
import { b, img, list, table } from './helpers';
import { closingCta, explorePages } from './shared';

export const admission: Story = {
  name: 'Admission & Fees',
  slug: 'admission',
  full_slug: 'admission',
  content: b('page', {
    seo_title: 'Admission & Fees',
    seo_description: 'Eligibility, the 5-step admission process, important dates, fee structure and scholarships for SSB’s UG programme in Business, Entrepreneurship & AI.',
    body: [
      b('page_intro', {
        eyebrow: 'Admission & Fees',
        headline: 'Admission & Fees.',
        muted: 'Eligibility, process, dates, fees and scholarships.',
        subhead: 'Early Round applications close on 31st December 2026, 11:59 PM. The programme commences in August 2027.',
        image: img('/admission/students-lab.jpg', 'SSB students on campus'),
        primary_cta_label: 'Book your info session',
        primary_cta_href: 'lead:info-session',
        secondary_cta_label: 'Download Brochure',
        secondary_cta_href: 'lead:brochure',
      }),
      b('bullet_panel', {
        anchor: 'eligibility',
        eyebrow: 'Eligibility',
        headline: 'Who can apply.',
        items: list(
          'Students currently in Class XII, or who passed Class XII in 2026',
          'Minimum 60% in Class XII from a recognised board (CBSE, ISC, state boards, IB, IGCSE or equivalent)',
          'Open to all streams: science, commerce and humanities',
        ),
      }),
      b('process_steps', {
        anchor: 'process',
        eyebrow: 'Admission process',
        headline: 'Five steps',
        muted: 'from information session to offer.',
        items: [
          b('process_step', {
            label: 'Step 1',
            title: 'Register and Attend an Information Session',
            text: 'Register on the website and book a 30-minute live information session with the admissions team. The session covers the programme, curriculum, global immersions, fees and scholarships, followed by a Q&A. Weekday and weekend slots are available for students and parents. Attendance is mandatory to proceed with the application.',
          }),
          b('process_step', {
            label: 'Step 2',
            title: 'Take the SSB Scholarship & Aptitude Test (SSAT)',
            text: 'The SSAT is a 70-minute online proctored test that assesses admission and scholarship eligibility.',
            points: list(
              'It covers logical reasoning, numerical ability, data interpretation and a problem-solving exercise.',
              'It must be taken in one sitting within 7 days of attending the information session.',
              'A practice test will be shared in advance.',
            ),
            note: 'Fast track: Candidates with qualifying JEE, SAT, CUET or IPMAT scores may skip the SSAT and proceed directly to the application.',
          }),
          b('process_step', {
            label: 'Step 3',
            title: 'Submit Your Application Online',
            text: 'Shortlisted candidates complete the application form:',
            points: list(
              'Fill in your personal details, academic records (Class X, XI and XII marks with supporting documents) and any JEE, SAT, CUET or IPMAT scores.',
              'Add up to five extracurricular achievements with your role, level and supporting proof.',
              'Pay the application fee of ₹1,000 to proceed to the next stage.',
              'Submit a video essay within 3 days on why you want to pursue this programme at Scaler School of Business.',
            ),
            note: 'Candidates may also visit the campus during this stage.',
          }),
          b('process_step', {
            label: 'Step 4',
            title: 'Appear for Interviews',
            text: 'The interview stage has 2 rounds:',
            points: list(
              'First-round interview: An online, AI-led interview that assesses structured thinking, communication and intent.',
              'Second-round interview: A case interview with SSB’s senior leadership at the Bengaluru campus (online in exceptional cases). It focuses on a business problem or guesstimate and your motivation for the programme.',
            ),
          }),
          b('process_step', {
            label: 'Step 5',
            title: 'Receive Your Admission Decision',
            text: 'Results are shared within 10 days of the interview. Candidates are either Accepted, Waitlisted or Not Selected.',
            points: list(
              'Accepted: You receive your offer with your scholarship. Confirm your admission within 10 days by paying the admission fee of ₹50,000.',
              'Waitlisted: SSB does not maintain a ranked waitlist. Waitlisted candidates are reviewed at the end of every round.',
              'Not selected: You may reapply in the next academic year.',
            ),
          }),
        ],
        footnote: 'Final Class XII marks are verified once board results are declared.',
      }),
      b('table_block', {
        anchor: 'dates',
        eyebrow: 'Important dates',
        headline: 'Important dates.',
        table: table(
          ['Round', 'Application Deadline', 'SSAT', 'Interviews', 'Decision', 'Commencement'],
          [
            ['Early Round', '31st December 2026, 11:59 PM', 'Within 7 days of the info session', 'December 2026 - January 2027', 'Within 10 days of the interview', 'August 2027'],
            ['Round 1', 'To be announced', 'To be announced', 'To be announced', 'To be announced', 'August 2027'],
          ],
        ),
        notes: list('Scholarships are limited. Applying early increases your chances of receiving one.', 'The early-applicant scholarship is available only in the Early Round.'),
      }),
      b('table_block', {
        anchor: 'fees',
        tone: 'muted',
        eyebrow: 'Fee structure',
        headline: 'Fee structure.',
        highlight_last_row: true,
        table: table(
          ['Year', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Total'],
          [
            ['Admission Fee', '₹50,000', '-', '-', '-', '₹50,000'],
            ['Tuition Fee', '₹11 lakh', '₹11.5 lakh', '₹11 lakh', '₹5.5 lakh', '₹39 lakh'],
            ['Total', '₹11.5 lakh', '₹11.5 lakh', '₹11 lakh', '₹5.5 lakh', '₹39.5 lakh'],
          ],
        ),
        notes: list(
          'The admission fee is payable within 10 days of accepting the offer, to confirm your seat.',
          'Tuition fees are payable term-wise.',
          'Hostel is optional. Fees for apartment-style housing will be shared as part of your offer letter.',
          'The parallel online degree fee is paid directly to the University as per its schedule.',
          'Application fee: ₹1,000, paid with your online application.',
        ),
      }),
      b('table_block', {
        anchor: 'scholarships',
        eyebrow: 'Scholarships',
        headline: 'Scholarships.',
        subhead: 'Scholarships are awarded based on SSAT performance, interviews and the overall profile. All applicants are considered automatically.',
        table: table(
          ['#', 'Scholarship', 'Eligibility'],
          [
            ['01', 'Merit', 'Exceptional academic and SSAT performance'],
            ['02', 'Builder', 'Students who have started a business, side project or creator channel'],
            ['03', 'Leadership', 'Demonstrated leadership in school, clubs or community initiatives'],
            ['04', 'Sports', 'Representation at state, national or international level'],
            ['05', 'Women in Business', 'Women who have demonstrated leadership or started their own venture'],
            ['06', 'Merit-cum-Need', 'Strong candidates whose families require financial support'],
            ['07', 'Early Applicant', 'Candidates who apply in the Early Round'],
          ],
        ),
        cta_label: 'Book your info session',
        cta_href: 'lead:info-session',
      }),
      explorePages('admission'),
      closingCta('Your seat in the first batch starts with an info session.'),
    ],
  }),
};
