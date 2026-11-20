import type { Blok } from '@/lib/types';
import { Chips, Heading, Img, Section, Tag, editable, lines, src } from '@/components/ui/primitives';
import { Carousel } from '@/components/ui/client';

export function ProjectCard({ c }: { c: Blok }) {
  return (
    <article className="group relative h-full overflow-hidden rounded-2xl bg-night text-white">
      <div className="relative aspect-[4/5] sm:aspect-[5/6]">
        {src(c.image) ? (
          <>
            <Img asset={c.image} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/35 to-black/5" />
          </>
        ) : (
          <div className="h-full w-full bg-gradient-to-br from-brand-deep via-brand-dark to-brand">
            <svg viewBox="0 0 200 200" className="absolute -right-10 -top-10 h-56 w-56 text-white/10" aria-hidden>
              <circle cx="100" cy="100" r="98" fill="none" stroke="currentColor" strokeWidth="1.5" />
              <circle cx="100" cy="100" r="64" fill="none" stroke="currentColor" strokeWidth="1.5" />
            </svg>
          </div>
        )}
      </div>
      <div className="absolute inset-0 flex flex-col justify-between p-5">
        <div className="flex items-start justify-between gap-2">
          {c.tag && <Tag dark>{c.tag}</Tag>}
          {src(c.logo) && (
            <span className="grid h-8 max-w-[96px] place-items-center rounded-md bg-white px-2">
              <Img asset={c.logo} className="max-h-5 w-auto object-contain" />
            </span>
          )}
        </div>
        <div>
          {c.metric && <p className="text-[24px] font-semibold leading-tight tracking-tighter2">{c.metric}</p>}
          <h3 className="mt-1 text-[16px] font-semibold">{c.name}</h3>
          {c.text && <p className="mt-1.5 text-[13px] leading-relaxed text-white/75">{c.text}</p>}
        </div>
      </div>
    </article>
  );
}

function FeatureCard({ c, index }: { c: Blok; index: number }) {
  // Cards with a tag (e.g. immersion cities) always get a visual header;
  // without a photo it falls back to a branded panel showing the title.
  const hasImage = Boolean(src(c.image)) || Boolean(c.tag);
  return (
    <article className="card flex h-full flex-col overflow-hidden">
      {hasImage && (
        <div className="relative aspect-[16/9] overflow-hidden bg-brand-soft">
          {src(c.image) ? (
            <Img asset={c.image} className="h-full w-full object-cover" />
          ) : (
            <div className="flex h-full w-full items-end bg-gradient-to-br from-brand-deep via-brand-dark to-brand p-5">
              <span className="text-[34px] font-semibold tracking-tighter2 text-white/90">{c.title}</span>
            </div>
          )}
          {c.tag && (
            <span className="absolute left-3 top-3">
              <Tag>{c.tag}</Tag>
            </span>
          )}
        </div>
      )}
      <div className="flex-1 p-5">
        {!hasImage && <p className="text-[13px] font-semibold text-brand">{String(index + 1).padStart(2, '0')}</p>}
        {!hasImage && c.tag && <Tag>{c.tag}</Tag>}
        <h4 className="mt-1 text-[17px] font-semibold tracking-tightish">{c.title}</h4>
        {c.subtitle && <p className="text-[12px] font-medium text-ink-4">{c.subtitle}</p>}
        <p className="mt-2 text-[14px] leading-relaxed text-ink-3">{c.text}</p>
      </div>
    </article>
  );
}

function Stepper({ steps }: { steps: Blok[] }) {
  return (
    <ol className="no-scrollbar -mx-4 flex gap-3 overflow-x-auto px-4 pb-2 sm:-mx-6 sm:px-6 lg:mx-0 lg:grid lg:grid-cols-7 lg:px-0">
      {steps.map((s, i) => (
        <li key={s._uid} className="relative w-[200px] shrink-0 rounded-xl border border-line bg-white p-4 lg:w-auto">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-brand">{s.label}</span>
          <p className="mt-1.5 text-[14px] font-medium leading-snug">{s.title}</p>
          {i < steps.length - 1 && <span className="absolute -right-2 top-1/2 hidden h-px w-3 bg-line-strong lg:block" aria-hidden />}
        </li>
      ))}
    </ol>
  );
}

export function CurriculumPillar({ blok, index }: { blok: Blok; index: number }) {
  const grid: Blok[] = blok.grid ?? [];
  const carousel: Blok[] = blok.carousel ?? [];
  const stats: Blok[] = blok.stats ?? [];
  return (
    <div id={`pillar-${index + 1}`} className="scroll-mt-32 border-t border-line py-12 first:border-t-0 first:pt-0" {...editable(blok)}>
      <span className="inline-flex items-center gap-2 rounded-md bg-brand-soft px-2 py-1 text-[12px] font-semibold text-brand-dark">
        <span className="rounded bg-brand px-1.5 text-white">{String(index + 1).padStart(2, '0')}</span>
        {blok.eyebrow}
      </span>
      <h3 className="mt-4 text-[26px] font-semibold leading-tight tracking-tighter2 sm:text-[34px]">
        {blok.headline}
        {blok.muted && <span className="text-ink-4"> {blok.muted}</span>}
      </h3>
      {blok.subhead && <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-ink-3">{blok.subhead}</p>}
      {blok.chips && (
        <div className="mt-5">
          <Chips items={lines(blok.chips)} />
        </div>
      )}

      {stats.length > 0 && (
        <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
          {stats.map((s) => (
            <div key={s._uid} className="rounded-xl border border-line bg-surface p-4">
              <p className="text-[24px] font-semibold tracking-tighter2 text-brand">{s.value}</p>
              <p className="mt-1 text-[13px] leading-snug text-ink-3">{s.label}</p>
            </div>
          ))}
        </div>
      )}

      {grid.length > 0 && (
        <div className="mt-8">
          {blok.grid_title && <p className="mb-4 text-[15px] font-semibold">{blok.grid_title}</p>}
          <div className={`grid gap-4 sm:grid-cols-2 ${grid.length > 4 ? 'lg:grid-cols-3' : ''}`}>
            {grid.map((c, i) => (
              <FeatureCard key={c._uid} c={c} index={i} />
            ))}
          </div>
        </div>
      )}

      {blok.tools && (
        <div className="mt-6 flex flex-wrap items-center gap-2">
          {blok.tools_title && <span className="mr-1 text-[13px] font-medium text-ink-3">{blok.tools_title}</span>}
          {lines(blok.tools).map((t) => (
            <span key={t} className="rounded-md border border-line bg-white px-2.5 py-1 text-[13px] font-medium text-ink-2">
              {t}
            </span>
          ))}
        </div>
      )}

      {(blok.stepper ?? []).length > 0 && (
        <div className="mt-10">
          {blok.stepper_title && <p className="mb-4 text-[15px] font-semibold">{blok.stepper_title}</p>}
          <Stepper steps={blok.stepper} />
        </div>
      )}

      {carousel.length > 0 && (
        <div className="mt-10">
          {blok.carousel_title && <p className="mb-4 text-[15px] font-semibold">{blok.carousel_title}</p>}
          <Carousel label={blok.carousel_title} itemClass="w-[72%] sm:w-[40%] lg:w-[30%]">
            {carousel.map((c) => (
              <ProjectCard key={c._uid} c={c} />
            ))}
          </Carousel>
        </div>
      )}
    </div>
  );
}

export function LearnSection({ blok }: { blok: Blok }) {
  const pillars: Blok[] = blok.pillars ?? [];
  return (
    <Section blok={blok} className="py-14 sm:py-20" id={blok.anchor || 'curriculum'}>
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-10 grid gap-10 lg:grid-cols-[220px_1fr]">
          <nav aria-label="Curriculum pillars" className="hidden lg:block">
            <ol className="sticky top-32 space-y-1">
              {pillars.map((p, i) => (
                <li key={p._uid}>
                  <a href={`#pillar-${i + 1}`} className="flex gap-3 rounded-lg px-3 py-2.5 text-[14px] font-medium text-ink-2 hover:bg-brand-soft hover:text-brand-dark">
                    <span className="text-brand">{String(i + 1).padStart(2, '0')}</span>
                    {p.nav_label || p.eyebrow}
                  </a>
                </li>
              ))}
            </ol>
          </nav>
          <div className="min-w-0">
            {pillars.map((p, i) => (
              <CurriculumPillar key={p._uid} blok={p} index={i} />
            ))}
          </div>
        </div>
      </div>
    </Section>
  );
}
