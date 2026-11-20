import type { Blok } from '@/lib/types';
import { BentoStats, InnovationLab, LogoWall, PeopleTabs, Pillars, ProofBar, StoryScroll, VideoFeature } from './landing';
import { LearnSection } from './learn';
import { Hero, HeroOptions } from './hero';
import { CampusGallery, Sessions, Testimonials } from './community';
import {
  AdmissionsSummary,
  BulletPanel,
  CtaBand,
  Faq,
  OutcomeGroup,
  PageIntro,
  Pathways,
  ProcessSteps,
  StatStrip,
  TableBlock,
  YearBlock,
} from './admissions';

// Storyblok component name -> React component. Add new section types here.
export const registry: Record<string, (p: { blok: Blok }) => React.ReactNode> = {
  hero: Hero,
  hero_options: HeroOptions,
  proof_bar: ProofBar,
  video_feature: VideoFeature,
  pillars: Pillars,
  people_tabs: PeopleTabs,
  story_scroll: StoryScroll,
  bento_stats: BentoStats,
  logo_wall: LogoWall,
  innovation_lab: InnovationLab,
  learn_section: LearnSection,
  campus_gallery: CampusGallery,
  sessions: Sessions,
  testimonials: Testimonials,
  admissions_summary: AdmissionsSummary,
  faq: Faq,
  cta_band: CtaBand,
  page_intro: PageIntro,
  year_block: YearBlock,
  bullet_panel: BulletPanel,
  process_steps: ProcessSteps,
  table_block: TableBlock,
  stat_strip: StatStrip,
  pathways: Pathways,
  outcome_group: OutcomeGroup,
};

export function Blocks({ body }: { body?: Blok[] }) {
  return (
    <>
      {(body ?? []).map((blok) => {
        const C = registry[blok.component];
        if (!C) {
          return process.env.NODE_ENV === 'development' ? (
            <div key={blok._uid} className="wrap my-4 rounded-lg border border-dashed border-red-300 p-4 text-sm text-red-600">
              Unknown block: {blok.component}
            </div>
          ) : null;
        }
        return <C key={blok._uid} blok={blok} />;
      })}
    </>
  );
}
