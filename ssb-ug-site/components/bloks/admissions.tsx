import type { Blok } from '@/lib/types';
import { Arrow, Heading, Img, Section, Tag, editable, lines, src } from '@/components/ui/primitives';
import { Carousel } from '@/components/ui/client';
import { Cta } from '@/components/ui/lead';
import { StoryCard } from './landing';
import { ProjectCard } from './learn';

/* ---------------------- Admissions summary ------------------------ */
export function AdmissionsSummary({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} tone="dark" className="py-16 sm:py-24" id={blok.anchor || 'admissions'}>
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} dark />
        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          <div className="space-y-3">
            {(blok.criteria ?? []).map((c: Blok) => (
              <div key={c._uid} className="rounded-2xl bg-night-2 p-6 ring-1 ring-white/10">
                <p className="text-[17px] font-semibold">{c.title}</p>
                <p className="mt-2 text-[14px] leading-relaxed text-white/65">{c.text}</p>
              </div>
            ))}
            <div className="flex flex-wrap items-center gap-4 pt-3">
              {blok.cta_label && (
                <Cta href={blok.cta_href}>
                  {blok.cta_label} <Arrow />
                </Cta>
              )}
              {blok.link_label && (
                <a href={blok.link_href} className="inline-flex items-center gap-1.5 text-sm font-semibold text-white/85 hover:text-white">
                  {blok.link_label} <Arrow />
                </a>
              )}
            </div>
          </div>
          <ol className="rounded-2xl bg-night-2 p-6 ring-1 ring-white/10">
            {(blok.steps ?? []).map((s: Blok, i: number) => (
              <li key={s._uid} className="relative flex gap-4 pb-6 last:pb-0">
                {i < blok.steps.length - 1 && <span className="absolute left-[15px] top-9 h-[calc(100%-36px)] w-px bg-white/15" aria-hidden />}
                <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-brand text-[13px] font-semibold">{i + 1}</span>
                <div>
                  <p className="text-[11px] font-semibold uppercase tracking-wider text-emerald-400">{s.label}</p>
                  <p className="mt-0.5 text-[16px] font-semibold">{s.title}</p>
                  <p className="mt-1 text-[14px] leading-relaxed text-white/60">{s.text}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </Section>
  );
}

/* ------------------------------ FAQ ------------------------------- */
export function Faq({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-14 sm:py-20" id={blok.anchor || 'faq'}>
      <div className="wrap grid gap-10 lg:grid-cols-[1fr_1.5fr]">
        <div>
          <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
          {blok.cta_label && (
            <div className="mt-6">
              <Cta href={blok.cta_href}>
                {blok.cta_label} <Arrow />
              </Cta>
            </div>
          )}
        </div>
        <div className="divide-y divide-line border-y border-line">
          {(blok.items ?? []).map((q: Blok) => (
            <details key={q._uid} className="group py-5" {...editable(q)}>
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-[16px] font-medium">
                {q.question}
                <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full border border-line text-ink-3 transition group-open:rotate-45">+</span>
              </summary>
              <div className="mt-3 space-y-2 pr-10 text-[15px] leading-relaxed text-ink-3">
                {lines(q.answer).map((l) => (
                  <p key={l}>{l}</p>
                ))}
              </div>
            </details>
          ))}
        </div>
      </div>
    </Section>
  );
}

/* ---------------------------- CTA band ---------------------------- */
export function CtaBand({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="pb-16 pt-4 sm:pb-24">
      <div className="wrap">
        <div className="relative isolate overflow-hidden rounded-3xl bg-night px-6 py-14 text-white sm:px-12 sm:py-20">
          <Img asset={blok.image} className="absolute inset-0 -z-10 h-full w-full object-cover opacity-45" />
          <div className="absolute inset-0 -z-10 bg-gradient-to-r from-black/85 via-black/60 to-black/20" />
          {blok.eyebrow && <p className="eyebrow text-emerald-400">{blok.eyebrow}</p>}
          <h2 className="mt-3 max-w-2xl text-[30px] font-semibold leading-tight tracking-tighter2 sm:text-[44px]">
            {blok.headline}
            {blok.muted && <span className="text-white/55"> {blok.muted}</span>}
          </h2>
          {blok.text && <p className="mt-4 max-w-xl text-[16px] leading-relaxed text-white/75">{blok.text}</p>}
          <div className="mt-8 flex flex-wrap gap-3">
            {blok.primary_cta_label && (
              <Cta href={blok.primary_cta_href}>
                {blok.primary_cta_label} <Arrow />
              </Cta>
            )}
            {blok.secondary_cta_label && (
              <Cta href={blok.secondary_cta_href} variant="light">
                {blok.secondary_cta_label}
              </Cta>
            )}
          </div>
        </div>
      </div>
    </Section>
  );
}

/* --------------------------- Page intro --------------------------- */
export function PageIntro({ blok }: { blok: Blok }) {
  const hasImage = Boolean(src(blok.image));
  return (
    <Section blok={blok} className="pb-10 pt-12 sm:pt-16">
      <div className={`wrap grid items-center gap-10 ${hasImage ? 'lg:grid-cols-[1.1fr_1fr]' : ''}`}>
        <div>
          {blok.eyebrow && <p className="eyebrow mb-3">{blok.eyebrow}</p>}
          <h1 className="text-[34px] font-semibold leading-[1.08] tracking-tighter2 sm:text-[48px]">
            {blok.headline}
            {blok.muted && <span className="text-ink-4"> {blok.muted}</span>}
          </h1>
          {blok.subhead && <p className="mt-4 max-w-2xl text-[16px] leading-relaxed text-ink-3 sm:text-lg">{blok.subhead}</p>}
          <div className="mt-7 flex flex-wrap gap-3">
            {blok.primary_cta_label && (
              <Cta href={blok.primary_cta_href}>
                {blok.primary_cta_label} <Arrow />
              </Cta>
            )}
            {blok.secondary_cta_label && (
              <Cta href={blok.secondary_cta_href} variant="ghost">
                {blok.secondary_cta_label}
              </Cta>
            )}
          </div>
        </div>
        {hasImage && <Img asset={blok.image} eager className="aspect-[4/3] w-full rounded-3xl object-cover" />}
      </div>
    </Section>
  );
}

/* ---------------------------- Year block -------------------------- */
export function YearBlock({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-12 sm:py-16" tone={blok.tone === 'muted' ? 'muted' : 'light'} id={blok.anchor}>
      <div className="wrap">
        <div className="grid gap-8 lg:grid-cols-[300px_1fr]">
          <div className="lg:sticky lg:top-32 lg:self-start">
            <p className="eyebrow">{blok.label}</p>
            <h2 className="mt-2 text-[28px] font-semibold leading-tight tracking-tighter2 sm:text-[34px]">{blok.title}</h2>
            <p className="mt-3 text-[15px] leading-relaxed text-ink-3">{blok.text}</p>
            {blok.tracks && (
              <div className="mt-5">
                <p className="text-[13px] font-semibold text-ink-2">{blok.tracks_title || 'Specialisation tracks'}</p>
                <ul className="mt-2 flex flex-wrap gap-2">
                  {lines(blok.tracks).map((t) => (
                    <li key={t} className="chip">
                      {t}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {src(blok.image) && <Img asset={blok.image} className="mt-6 hidden aspect-[4/3] w-full rounded-2xl object-cover lg:block" />}
          </div>
          <div className="grid gap-4 xl:grid-cols-2">
            {(blok.terms ?? []).map((t: Blok) => (
              <article key={t._uid} className="card flex flex-col p-6" {...editable(t)}>
                <div className="flex items-baseline justify-between gap-3">
                  <h3 className="text-[19px] font-semibold tracking-tightish">{t.title}</h3>
                  <span className="text-[12px] font-medium text-ink-4">{t.months}</span>
                </div>
                {t.outcome && (
                  <p className="mt-3 rounded-xl bg-brand-soft px-4 py-3 text-[14px] font-medium leading-snug text-brand-deep">{t.outcome}</p>
                )}
                <dl className="mt-4 space-y-3.5">
                  {(t.rows ?? []).map((r: Blok) => (
                    <div key={r._uid}>
                      <dt className="text-[12px] font-semibold uppercase tracking-wider text-ink-4">{r.label}</dt>
                      <dd className="mt-1 text-[14px] leading-relaxed text-ink-2">{r.text}</dd>
                    </div>
                  ))}
                </dl>
              </article>
            ))}
          </div>
        </div>
      </div>
    </Section>
  );
}

/* --------------------------- Bullet panel ------------------------- */
export function BulletPanel({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-12 sm:py-16" id={blok.anchor}>
      <div className="wrap grid gap-8 lg:grid-cols-[1fr_1.4fr]">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <ul className="card divide-y divide-line">
          {lines(blok.items).map((l) => (
            <li key={l} className="flex gap-3 p-5 text-[15px] leading-relaxed text-ink-2">
              <svg viewBox="0 0 20 20" className="mt-1 h-4 w-4 shrink-0 text-brand" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 10.5l3 3 7-7" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              {l}
            </li>
          ))}
        </ul>
      </div>
    </Section>
  );
}

/* ------------------------- Process steps -------------------------- */
export function ProcessSteps({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-12 sm:py-16" tone="muted" id={blok.anchor}>
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <ol className="mt-10 space-y-4">
          {(blok.items ?? []).map((s: Blok, i: number) => (
            <li key={s._uid} className="card grid gap-4 p-6 sm:grid-cols-[64px_1fr] sm:p-8" {...editable(s)}>
              <span className="grid h-12 w-12 place-items-center rounded-full bg-brand text-[17px] font-semibold text-white">{i + 1}</span>
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-wider text-brand">{s.label}</p>
                <h3 className="mt-1 text-[20px] font-semibold tracking-tightish">{s.title}</h3>
                {s.text && <p className="mt-2 text-[15px] leading-relaxed text-ink-3">{s.text}</p>}
                {s.points && (
                  <ul className="mt-3 space-y-2">
                    {lines(s.points).map((p) => (
                      <li key={p} className="flex gap-2.5 text-[15px] leading-relaxed text-ink-2">
                        <span className="mt-2.5 h-1.5 w-1.5 shrink-0 rounded-full bg-brand" aria-hidden />
                        {p}
                      </li>
                    ))}
                  </ul>
                )}
                {s.note && <p className="mt-4 rounded-xl bg-brand-soft px-4 py-3 text-[14px] leading-relaxed text-brand-deep">{s.note}</p>}
              </div>
            </li>
          ))}
        </ol>
        {blok.footnote && <p className="mt-6 text-[14px] text-ink-3">{blok.footnote}</p>}
      </div>
    </Section>
  );
}

/* ---------------------------- Table block ------------------------- */
type Table = { thead?: { value: string }[]; tbody?: { body: { value: string }[] }[] };

export function TableBlock({ blok }: { blok: Blok }) {
  const table: Table = blok.table ?? {};
  const head = table.thead ?? [];
  const rows = table.tbody ?? [];
  const lastRowTotal = blok.highlight_last_row;
  return (
    <Section blok={blok} className="py-12 sm:py-16" tone={blok.tone === 'muted' ? 'muted' : 'light'} id={blok.anchor}>
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-8 overflow-x-auto rounded-2xl border border-line bg-white">
          <table className="w-full min-w-[640px] border-collapse text-left text-[14px]">
            <thead>
              <tr className="bg-surface">
                {head.map((h, i) => (
                  <th key={i} scope="col" className="border-b border-line px-5 py-3.5 text-[12px] font-semibold uppercase tracking-wider text-ink-3">
                    {h.value}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, ri) => {
                const isTotal = lastRowTotal && ri === rows.length - 1;
                return (
                  <tr key={ri} className={`${isTotal ? 'bg-brand-soft font-semibold text-brand-deep' : ''} border-b border-line last:border-b-0`}>
                    {r.body.map((c, ci) =>
                      ci === 0 ? (
                        <th key={ci} scope="row" className="px-5 py-4 font-semibold">
                          {c.value}
                        </th>
                      ) : (
                        <td key={ci} className="px-5 py-4 leading-relaxed">
                          {c.value}
                        </td>
                      ),
                    )}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        {blok.notes && (
          <ul className="mt-5 space-y-1.5">
            {lines(blok.notes).map((n) => (
              <li key={n} className="flex gap-2.5 text-[14px] leading-relaxed text-ink-3">
                <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-ink-4" aria-hidden />
                {n}
              </li>
            ))}
          </ul>
        )}
        {blok.cta_label && (
          <div className="mt-8">
            <Cta href={blok.cta_href}>
              {blok.cta_label} <Arrow />
            </Cta>
          </div>
        )}
      </div>
    </Section>
  );
}

/* ---------------------------- Stat strip -------------------------- */
export function StatStrip({ blok }: { blok: Blok }) {
  const dark = blok.tone === 'dark';
  return (
    <Section blok={blok} tone={dark ? 'dark' : 'light'} className="py-12 sm:py-16">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} dark={dark} />
        <div className={`mt-8 grid grid-cols-2 gap-3 ${(blok.items ?? []).length > 4 ? 'lg:grid-cols-5' : 'lg:grid-cols-4'}`}>
          {(blok.items ?? []).map((s: Blok) => (
            <div key={s._uid} className={`rounded-2xl p-5 ${dark ? 'bg-night-2 ring-1 ring-white/10' : 'border border-line bg-surface'}`}>
              <p className={`text-[28px] font-semibold tracking-tighter2 ${dark ? 'text-emerald-400' : 'text-brand'}`}>{s.value}</p>
              <p className={`mt-1 text-[13px] leading-snug ${dark ? 'text-white/60' : 'text-ink-3'}`}>{s.label}</p>
              {s.tag && (
                <div className="mt-3">
                  <Tag dark={dark}>{s.tag}</Tag>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </Section>
  );
}

/* ----------------------------- Pathways --------------------------- */
export function Pathways({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-12 sm:py-16" tone="muted" id={blok.anchor}>
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-10 grid gap-4 md:grid-cols-3">
          {(blok.items ?? []).map((p: Blok, i: number) => (
            <article key={p._uid} className="card overflow-hidden">
              <Img asset={p.image} className="aspect-[16/10] w-full object-cover" />
              <div className="p-6">
                <p className="text-[13px] font-semibold text-brand">Path {String(i + 1).padStart(2, '0')}</p>
                <h3 className="mt-1 text-[20px] font-semibold tracking-tightish">{p.title}</h3>
                <p className="mt-2 text-[14px] leading-relaxed text-ink-3">{p.text}</p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </Section>
  );
}

/* --------------------------- Outcome group ------------------------ */
export function OutcomeGroup({ blok }: { blok: Blok }) {
  const dark = blok.tone === 'dark';
  const stats: Blok[] = blok.stats ?? [];
  return (
    <Section blok={blok} tone={dark ? 'dark' : blok.tone === 'muted' ? 'muted' : 'light'} className="py-12 sm:py-16" id={blok.anchor}>
      <div className="wrap">
        <div className="flex flex-wrap items-center gap-3">{blok.tag && <Tag dark={dark}>{blok.tag}</Tag>}</div>
        <Heading headline={blok.headline} muted={blok.muted} sub={blok.subhead} dark={dark} className="mt-3" />
        {stats.length > 0 && (
          <div className={`mt-8 grid grid-cols-2 gap-3 sm:grid-cols-3 ${stats.length > 4 ? 'lg:grid-cols-6' : 'lg:grid-cols-4'}`}>
            {stats.map((s) => (
              <div key={s._uid} className={`rounded-2xl p-5 ${dark ? 'bg-night-2 ring-1 ring-white/10' : 'border border-line bg-white'}`}>
                <p className={`text-[26px] font-semibold tracking-tighter2 ${dark ? 'text-emerald-400' : 'text-brand'}`}>{s.value}</p>
                <p className={`mt-1 text-[13px] leading-snug ${dark ? 'text-white/60' : 'text-ink-3'}`}>{s.label}</p>
              </div>
            ))}
          </div>
        )}
        {(blok.cards ?? []).length > 0 && (
          <div className="mt-10">
            {blok.cards_title && <p className={`mb-4 text-[15px] font-semibold ${dark ? 'text-white' : ''}`}>{blok.cards_title}</p>}
            <Carousel dark={dark} label={blok.cards_title || blok.headline}>
              {blok.cards.map((c: Blok) => (blok.card_style === 'project' ? <ProjectCard key={c._uid} c={c} /> : <StoryCard key={c._uid} c={c} dark={dark} />))}
            </Carousel>
          </div>
        )}
        {(blok.journeys ?? []).length > 0 && (
          <div className="mt-10">
            {blok.journeys_title && <p className="mb-4 text-[15px] font-semibold">{blok.journeys_title}</p>}
            <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {blok.journeys.map((j: Blok) => (
                <li key={j._uid} className="card flex items-center gap-4 p-4">
                  {src(j.image) && <Img asset={j.image} className="h-14 w-14 shrink-0 rounded-full object-cover" />}
                  {src(j.image) ? (
                    <div className="min-w-0">
                      <p className="text-[15px] font-semibold">{j.name}</p>
                      <p className="text-[13px] leading-snug text-ink-3">
                        {j.from && <span>{j.from} → </span>}
                        <span className="font-medium text-ink-2">{j.to}</span>
                      </p>
                    </div>
                  ) : (
                    <div className="flex min-w-0 flex-1 items-center justify-between gap-3">
                      <div className="min-w-0">
                        <p className="text-[15px] font-semibold">{j.name}</p>
                        {j.from && <p className="text-[13px] text-ink-4">{j.from}</p>}
                      </div>
                      <span className="shrink-0 rounded-lg bg-brand-soft px-3 py-1.5 text-[13px] font-semibold text-brand-deep">{j.to}</span>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
        {(blok.logos ?? []).length > 0 && (
          <div className="mt-10">
            {blok.logos_title && <p className="mb-4 text-[15px] font-semibold">{blok.logos_title}</p>}
            <ul className="flex flex-wrap gap-2">
              {blok.logos.map((l: any, i: number) => (
                <li key={i} className="grid h-16 w-[calc(33.333%-6px)] place-items-center rounded-xl border border-line bg-white px-3 sm:w-[132px]">
                  <Img asset={l} className="max-h-6 w-auto max-w-[90px] object-contain" />
                </li>
              ))}
            </ul>
          </div>
        )}
        {blok.names && (
          <div className="mt-8">
            {blok.names_title && <p className="mb-3 text-[15px] font-semibold">{blok.names_title}</p>}
            <ul className="flex flex-wrap gap-2">
              {lines(blok.names).map((n) => (
                <li key={n} className="chip">
                  {n}
                </li>
              ))}
            </ul>
          </div>
        )}
        {blok.cta_label && (
          <div className="mt-8">
            <Cta href={blok.cta_href} variant={dark ? 'light' : 'primary'}>
              {blok.cta_label} <Arrow />
            </Cta>
          </div>
        )}
      </div>
    </Section>
  );
}

/* --------------------------- Page links --------------------------- */
// "Explore the programme": cards linking to the other pages of the site.
export function PageLinks({ blok }: { blok: Blok }) {
  const items: Blok[] = blok.items ?? [];
  return (
    <Section blok={blok} className="py-14 sm:py-16" tone="muted">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} />
        <ul className={`mt-8 grid gap-4 sm:grid-cols-2 ${items.length > 3 ? 'lg:grid-cols-4' : 'lg:grid-cols-3'}`}>
          {items.map((it) => (
            <li key={it._uid}>
              <a href={it.href} className="card group flex h-full flex-col overflow-hidden transition hover:-translate-y-0.5 hover:shadow-lg">
                <div className="aspect-[16/10] overflow-hidden bg-surface-2">
                  <Img asset={it.image} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.04]" />
                </div>
                <div className="flex flex-1 flex-col p-5">
                  <p className="flex items-center justify-between gap-2 text-[17px] font-semibold tracking-tightish">
                    {it.title}
                    <span className="grid h-8 w-8 place-items-center rounded-full bg-brand-soft text-brand-dark transition group-hover:bg-brand group-hover:text-white">
                      <Arrow />
                    </span>
                  </p>
                  <p className="mt-1.5 text-[14px] leading-relaxed text-ink-3">{it.text}</p>
                </div>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </Section>
  );
}
