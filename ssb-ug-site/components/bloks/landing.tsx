import type { Blok } from '@/lib/types';
import { Arrow, Chips, Heading, Img, Play, Section, Tag, lines, src } from '@/components/ui/primitives';
import { Carousel, Tabs, VideoTrigger } from '@/components/ui/client';
import { Cta } from '@/components/ui/lead';

/* ---------------------------- Proof bar --------------------------- */
export function ProofBar({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="pb-10">
      <div className="wrap">
        <div className="grid grid-cols-2 divide-line overflow-hidden rounded-2xl border border-line lg:grid-cols-4 lg:divide-x">
          {(blok.items ?? []).map((s: Blok, i: number) => (
            <div key={s._uid} className={`p-5 sm:p-6 ${i % 2 === 0 ? 'border-r border-line lg:border-r-0' : ''} ${i < 2 ? 'border-b border-line lg:border-b-0' : ''}`}>
              <p className="text-[26px] font-semibold tracking-tighter2 text-brand sm:text-[32px]">{s.value}</p>
              <p className="mt-1 text-[13px] leading-snug text-ink-3 sm:text-sm">{s.label}</p>
            </div>
          ))}
        </div>
        {blok.footnote && <p className="mt-3 text-xs italic text-ink-4">{blok.footnote}</p>}
      </div>
    </Section>
  );
}

/* ------------------------- Video feature ------------------------- */
export function VideoFeature({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-14 sm:py-20">
      <div className="wrap">
        <div className="grid items-center gap-8 rounded-3xl border border-line bg-surface p-4 sm:p-6 lg:grid-cols-[1fr_1.3fr] lg:gap-12 lg:p-10">
          <div className="p-2">
            <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.text} />
            {blok.note && <p className="mt-6 text-sm text-ink-3">{blok.note}</p>}
          </div>
          <VideoTrigger video={blok.video_url}>
            <div className="relative aspect-video overflow-hidden rounded-2xl bg-night">
              <Img asset={blok.poster} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.02]" />
              <span className="absolute inset-0 grid place-items-center">
                <span className="grid h-16 w-16 place-items-center rounded-full bg-white text-ink shadow-xl transition group-hover:scale-105">
                  <Play className="ml-1 h-6 w-6" />
                </span>
              </span>
              {blok.video_label && (
                <span className="absolute bottom-3 left-3 rounded-md bg-black/60 px-2 py-1 text-xs font-medium text-white">{blok.video_label}</span>
              )}
            </div>
          </VideoTrigger>
        </div>
      </div>
    </Section>
  );
}

/* ----------------------------- Pillars ---------------------------- */
export function Pillars({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-14 sm:py-20" tone="muted">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {(blok.items ?? []).map((p: Blok, i: number) => (
            <article key={p._uid} className="card group flex flex-col overflow-hidden">
              <div className="relative aspect-[16/9] overflow-hidden">
                <Img asset={p.image} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]" />
                <span className="absolute left-3 top-3 rounded-md bg-white/90 px-2 py-0.5 text-[12px] font-semibold text-brand-dark">
                  {String(i + 1).padStart(2, '0')}
                </span>
              </div>
              <div className="flex flex-1 flex-col p-5">
                <h3 className="text-[18px] font-semibold leading-snug tracking-tightish">{p.title}</h3>
                {p.lead && <p className="mt-1.5 text-[14px] leading-relaxed text-ink-3">{p.lead}</p>}
                <ul className="mt-4 space-y-2 border-t border-line pt-4">
                  {lines(p.points).map((pt) => (
                    <li key={pt} className="flex gap-2.5 text-[14px] leading-snug text-ink-2">
                      <svg viewBox="0 0 20 20" className="mt-0.5 h-4 w-4 shrink-0 text-brand" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M5 10.5l3 3 7-7" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                      {pt}
                    </li>
                  ))}
                </ul>
              </div>
            </article>
          ))}
        </div>
      </div>
    </Section>
  );
}

/* --------------------------- People tabs -------------------------- */
function PersonCard({ p }: { p: Blok }) {
  return (
    <article className="group relative h-full overflow-hidden rounded-2xl bg-night-2">
      <div className="relative aspect-[4/5]">
        <Img asset={p.image} className="h-full w-full object-cover object-top transition duration-500 group-hover:scale-[1.03]" />
        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent" />
      </div>
      <div className="absolute inset-x-0 bottom-0 p-4 text-white">
        {p.subject && <p className="text-[15px] font-semibold leading-tight">{p.subject}</p>}
        <p className={p.subject ? 'mt-1 text-[13px] text-white/80' : 'text-[16px] font-semibold'}>
          {p.subject ? `by ${p.name}` : p.name}
        </p>
        <p className="mt-1 text-[12px] leading-snug text-white/60">{p.role}</p>
        {(p.logo?.filename || p.company) && (
          <div className="mt-3 flex items-center gap-2 border-t border-white/15 pt-3">
            {p.logo?.filename && (
              <span className="grid h-6 w-6 place-items-center overflow-hidden rounded bg-white p-0.5">
                <Img asset={p.logo} className="max-h-full max-w-full object-contain" />
              </span>
            )}
            <span className="text-[12px] font-medium text-white/80">{p.company}</span>
          </div>
        )}
      </div>
    </article>
  );
}

function FounderCard({ p }: { p: Blok }) {
  return (
    <article className="card h-full overflow-hidden">
      <VideoTrigger video={p.video_url}>
        <div className="relative aspect-video overflow-hidden bg-night">
          <Img asset={p.image} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]" />
          {p.video_url && (
            <span className="absolute inset-0 grid place-items-center">
              <span className="grid h-12 w-12 place-items-center rounded-full bg-white/95 text-ink shadow-lg">
                <Play className="ml-0.5 h-5 w-5" />
              </span>
            </span>
          )}
          {p.subject && <span className="absolute bottom-3 left-3 rounded-md bg-black/60 px-2 py-1 text-[11px] font-medium text-white">{p.subject}</span>}
        </div>
      </VideoTrigger>
      <div className="p-5">
        {p.quote && <p className="text-[16px] font-semibold leading-snug tracking-tightish">{p.quote}</p>}
        <div className={`${p.quote ? 'mt-4 border-t border-line pt-4' : ''} flex items-center gap-3`}>
          {p.avatar?.filename && <Img asset={p.avatar} className="h-10 w-10 rounded-full object-cover" />}
          <div>
            <p className="text-[14px] font-semibold">{p.name}</p>
            <p className="text-[12px] leading-snug text-ink-3">{p.role}</p>
          </div>
        </div>
      </div>
    </article>
  );
}

export function PeopleTabs({ blok }: { blok: Blok }) {
  const groups: Blok[] = blok.groups ?? [];
  return (
    <Section blok={blok} className="py-14 sm:py-20">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-8">
          <Tabs
            labels={groups.map((g) => g.label)}
            panels={groups.map((g) =>
              g.layout === 'landscape' ? (
                <Carousel key={g._uid} label={g.label} itemClass="w-[85%] sm:w-[48%] lg:w-[32%]">
                  {(g.people ?? []).map((p: Blok) => (
                    <FounderCard key={p._uid} p={p} />
                  ))}
                </Carousel>
              ) : (
                <Carousel key={g._uid} label={g.label} itemClass="w-[62%] sm:w-[34%] lg:w-[23.5%]">
                  {(g.people ?? []).map((p: Blok) => (
                    <PersonCard key={p._uid} p={p} />
                  ))}
                </Carousel>
              ),
            )}
          />
        </div>
      </div>
    </Section>
  );
}

/* --------------------- Story scroll (outcomes) -------------------- */
export function StoryCard({ c, dark }: { c: Blok; dark?: boolean }) {
  return (
    <article className={`flex h-full flex-col overflow-hidden rounded-2xl ${dark ? 'bg-night-2 ring-1 ring-white/10' : 'card'}`}>
      <div className={`relative aspect-[4/3] overflow-hidden ${src(c.image) ? 'bg-night' : 'bg-gradient-to-br from-brand-deep via-brand-dark to-brand'}`}>
        {src(c.image) ? (
          <Img asset={c.image} className="h-full w-full object-cover" />
        ) : (
          <>
            <svg viewBox="0 0 200 200" className="absolute -right-10 -top-10 h-56 w-56 text-white/10" aria-hidden>
              <circle cx="100" cy="100" r="98" fill="none" stroke="currentColor" strokeWidth="1.5" />
              <circle cx="100" cy="100" r="64" fill="none" stroke="currentColor" strokeWidth="1.5" />
            </svg>
            <p className="absolute inset-x-5 top-[38%] -translate-y-1/2 text-center text-[28px] font-bold leading-tight tracking-tighter2 text-white/95">
              {c.name}
            </p>
          </>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/5 to-transparent" />
        {c.overlay && <p className="absolute inset-x-4 bottom-4 text-[17px] font-semibold leading-snug text-white">{c.overlay}</p>}
        {c.tag && (
          <span className="absolute left-3 top-3">
            <Tag>{c.tag}</Tag>
          </span>
        )}
      </div>
      <div className="flex-1 p-5">
        <h3 className={`text-[16px] font-semibold ${dark ? 'text-white' : ''}`}>{c.name}</h3>
        {c.by && <p className={`mt-0.5 text-[12px] ${dark ? 'text-white/50' : 'text-ink-4'}`}>{c.by}</p>}
        <p className={`mt-2 text-[14px] leading-relaxed ${dark ? 'text-white/65' : 'text-ink-3'}`}>{c.description}</p>
      </div>
    </article>
  );
}

export function StoryScroll({ blok }: { blok: Blok }) {
  const dark = blok.tone === 'dark';
  return (
    <Section blok={blok} tone={dark ? 'dark' : 'light'} className="py-14 sm:py-20">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} dark={dark} />
        <div className="mt-10">
          <Carousel label={blok.headline} dark={dark}>
            {(blok.cards ?? []).map((c: Blok) => (
              <StoryCard key={c._uid} c={c} dark={dark} />
            ))}
          </Carousel>
        </div>
        {blok.footnote && <p className={`mt-6 text-[13px] italic ${dark ? 'text-white/45' : 'text-ink-4'}`}>{blok.footnote}</p>}
      </div>
    </Section>
  );
}

/* --------------------------- Bento stats -------------------------- */
export function BentoStats({ blok }: { blok: Blok }) {
  const tiles: Blok[] = blok.tiles ?? [];
  return (
    <Section blok={blok} className="py-14 sm:py-20">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-10 grid auto-rows-[minmax(150px,auto)] grid-cols-2 gap-3 lg:grid-cols-4">
          {tiles.map((t) => {
            const size =
              t.size === 'wide'
                ? 'col-span-2 row-span-2'
                : t.size === 'tall'
                  ? 'col-span-2 row-span-2 sm:col-span-1 lg:col-span-1'
                  : t.size === 'wide_short'
                    ? 'col-span-2'
                    : 'col-span-1';
            const hasImage = Boolean(src(t.image));
            return (
              <div key={t._uid} className={`${size} relative overflow-hidden rounded-2xl ${hasImage ? 'bg-night text-white' : 'border border-line bg-surface'}`}>
                {hasImage && (
                  <>
                    <Img asset={t.image} className="absolute inset-0 h-full w-full object-cover" />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-black/10" />
                  </>
                )}
                <div className="relative flex h-full flex-col justify-between gap-4 p-5">
                  <div className="flex items-start justify-between gap-2">
                    <Tag dark={hasImage}>{t.tag}</Tag>
                    {t.badge?.filename && (
                      <span className="rounded-md bg-white px-2 py-1">
                        <Img asset={t.badge} className="h-4 w-auto" />
                      </span>
                    )}
                  </div>
                  <div>
                    {t.video_label && (
                      <VideoTrigger video={t.video_url} className="mb-3 w-auto">
                        <span className="inline-flex items-center gap-2 rounded-full bg-white/95 px-3 py-1.5 text-[12px] font-semibold text-ink">
                          <Play className="h-3.5 w-3.5" /> {t.video_label}
                        </span>
                      </VideoTrigger>
                    )}
                    <p className={`font-semibold tracking-tighter2 ${t.size === 'small' || t.size === 'wide_short' ? 'text-[26px]' : 'text-[30px] sm:text-[40px]'} ${hasImage ? '' : 'text-brand'} leading-[1.05]`}>
                      {t.big}
                    </p>
                    <p className={`mt-2 text-[13px] leading-snug ${hasImage ? 'text-white/75' : 'text-ink-3'}`}>{t.line}</p>
                    {t.flags && <p className="mt-2 text-lg tracking-widest">{t.flags}</p>}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </Section>
  );
}

/* ---------------------------- Logo wall --------------------------- */
export function LogoWall({ blok }: { blok: Blok }) {
  const logos: any[] = blok.logos ?? [];
  return (
    <Section blok={blok} className="py-14 sm:py-16" tone={blok.tone === 'muted' ? 'muted' : 'light'}>
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <ul className="mt-8 grid grid-cols-3 gap-px overflow-hidden rounded-2xl border border-line bg-line sm:grid-cols-4 lg:grid-cols-8">
          {logos.map((l, i) => (
            <li key={i} className="grid h-20 place-items-center bg-white px-4">
              <Img asset={l} className="max-h-7 w-auto max-w-[100px] object-contain" />
            </li>
          ))}
        </ul>
      </div>
    </Section>
  );
}

/* -------------------------- Innovation lab ------------------------ */
export function InnovationLab({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} tone="dark" className="py-16 sm:py-24">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} dark />
        {blok.highlight?.[0] && (
          <div className="mt-10 grid overflow-hidden rounded-3xl bg-night-2 ring-1 ring-white/10 lg:grid-cols-2">
            <div className="relative min-h-[260px]">
              <Img asset={blok.highlight[0].image} className="absolute inset-0 h-full w-full object-cover" />
            </div>
            <div className="flex flex-col justify-center p-6 sm:p-10">
              <Tag dark>{blok.highlight[0].tag}</Tag>
              <p className="mt-4 text-[24px] font-semibold leading-tight tracking-tightish sm:text-[30px]">{blok.highlight[0].overlay}</p>
              <p className="mt-3 text-[15px] leading-relaxed text-white/65">{blok.highlight[0].description}</p>
            </div>
          </div>
        )}
        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {(blok.facts ?? []).map((f: Blok) => (
            <div key={f._uid} className="overflow-hidden rounded-2xl bg-night-2 ring-1 ring-white/10">
              <Img asset={f.image} className="aspect-[16/10] w-full object-cover" />
              <div className="p-5">
                <p className="text-[16px] font-semibold">{f.title}</p>
                <p className="mt-1.5 text-[14px] leading-relaxed text-white/60">{f.text}</p>
              </div>
            </div>
          ))}
        </div>
        {blok.startups_title && <p className="mt-14 text-[18px] font-semibold">{blok.startups_title}</p>}
        <div className="mt-6">
          <Carousel dark label={blok.startups_title}>
            {(blok.startups ?? []).map((s: Blok) => (
              <article key={s._uid} className="flex h-full flex-col overflow-hidden rounded-2xl bg-night-2 ring-1 ring-white/10">
                <Img asset={s.image} className="aspect-[2/1] w-full object-cover" />
                <div className="flex-1 p-5">
                  <p className="text-[11px] font-semibold uppercase tracking-wider text-emerald-400">{s.kind}</p>
                  <h3 className="mt-1.5 text-[17px] font-semibold">
                    {s.url ? (
                      <a href={s.url} target="_blank" rel="noreferrer" className="hover:underline">
                        {s.name} ↗
                      </a>
                    ) : (
                      s.name
                    )}
                  </h3>
                  <p className="text-[12px] text-white/50">{s.by}</p>
                  <p className="mt-3 border-t border-white/10 pt-3 text-[14px] leading-relaxed text-white/65">{s.text}</p>
                </div>
              </article>
            ))}
          </Carousel>
        </div>
      </div>
    </Section>
  );
}

export { Chips };
