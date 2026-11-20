import type { Blok } from '@/lib/types';
import { Arrow, Img, Section, lines, src } from '@/components/ui/primitives';
import { Cta } from '@/components/ui/lead';
import { HeroSwitcher } from '@/components/ui/hero-switcher';

/*
 * Hero section. One block, four layouts (the `layout` field):
 *   card      – video inside a rounded card, copy bottom-left (default)
 *   split     – light page, big headline left, video right with facts on it
 *   fullbleed – edge-to-edge video, white headline, feature strip (SST-style)
 *   mosaic    – green-tinted video, headline + 2×2 tiles of the 4 businesses
 * `hero_options` wraps several heroes and adds a 1·2·3·4 bar to compare them.
 */

/** Renders the headline, colouring `accent` (a phrase inside it) in the brand green. */
function Headline({ blok, className, accentClass }: { blok: Blok; className: string; accentClass: string }) {
  const h: string = blok.headline ?? '';
  const a: string = blok.headline_accent ?? '';
  const i = a ? h.indexOf(a) : -1;
  return (
    <h1 className={className}>
      {i < 0 ? (
        h
      ) : (
        <>
          {h.slice(0, i)}
          <span className={accentClass}>{a}</span>
          {h.slice(i + a.length)}
        </>
      )}
    </h1>
  );
}

function BgVideo({ blok, className = '' }: { blok: Blok; className?: string }) {
  return src(blok.video) ? (
    <video
      className={`h-full w-full object-cover ${className}`}
      src={src(blok.video)}
      poster={src(blok.poster)}
      autoPlay
      muted
      loop
      playsInline
      preload="metadata"
    />
  ) : (
    <Img asset={blok.poster} eager className={`h-full w-full object-cover ${className}`} />
  );
}

function Ctas({ blok, secondary = 'light' }: { blok: Blok; secondary?: 'light' | 'ghost' }) {
  return (
    <div className="flex flex-wrap gap-3">
      {blok.primary_cta_label && (
        <Cta href={blok.primary_cta_href}>
          {blok.primary_cta_label} <Arrow />
        </Cta>
      )}
      {blok.secondary_cta_label && (
        <Cta href={blok.secondary_cta_href} variant={secondary}>
          {blok.secondary_cta_label}
        </Cta>
      )}
    </div>
  );
}

function Pills({ blok, tone }: { blok: Blok; tone: 'glass' | 'light' | 'outline' }) {
  const cls =
    tone === 'glass'
      ? 'border-white/25 bg-white/10 text-white backdrop-blur'
      : tone === 'outline'
        ? 'border-white/30 text-white/90'
        : 'border-brand-line bg-brand-soft text-brand-deep';
  return (
    <div className="flex flex-wrap gap-2">
      {lines(blok.pills).map((p) => (
        <span key={p} className={`rounded-md border px-2.5 py-1 text-[13px] font-medium ${cls}`}>
          {p}
        </span>
      ))}
    </div>
  );
}

function LogoRow({ label, logos, names, align = 'right', dark = true }: { label?: string; logos?: any[]; names?: string; align?: 'left' | 'right'; dark?: boolean }) {
  if (!label && !logos?.length) return null;
  const right = align === 'right';
  return (
    <div className={right ? 'lg:text-right' : ''}>
      {label && <p className={`mb-2 text-[11px] font-medium uppercase tracking-[0.12em] ${dark ? 'text-white/60' : 'text-ink-4'}`}>{label}</p>}
      <div className={`flex flex-wrap items-center gap-1.5 ${right ? 'lg:justify-end' : ''}`}>
        {(logos ?? []).map((l, i) => (
          <span key={i} className={`grid h-9 min-w-[64px] place-items-center rounded-md bg-white px-2.5 ${dark ? '' : 'border border-line'}`}>
            <Img asset={l} className="max-h-5 w-auto max-w-[84px] object-contain" />
          </span>
        ))}
        {lines(names).map((n) => (
          <span key={n} className={`grid h-9 place-items-center rounded-md bg-white px-2.5 text-[12px] font-bold text-black ${dark ? '' : 'border border-line'}`}>
            {n}
          </span>
        ))}
      </div>
    </div>
  );
}

const Eyebrow = ({ text, dark }: { text?: string; dark?: boolean }) =>
  text ? (
    <span
      className={`inline-flex items-center gap-2 rounded-md px-2.5 py-1 text-[12px] font-semibold ${
        dark ? 'bg-white/10 text-white ring-1 ring-white/20' : 'bg-brand-soft text-brand-deep'
      }`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${dark ? 'bg-emerald-400' : 'bg-brand'}`} aria-hidden />
      {text}
    </span>
  ) : null;

/* ----------------------------- 1. Card ----------------------------- */
function HeroCard({ blok }: { blok: Blok }) {
  return (
    <div className="pb-6 pt-3 sm:pt-4">
      <div className="mx-auto max-w-[1440px] px-2 sm:px-4">
        <div className="relative isolate overflow-hidden rounded-[22px] bg-night">
          <div className="absolute inset-0 -z-10">
            <BgVideo blok={blok} />
          </div>
          <div className="absolute inset-0 -z-10 bg-gradient-to-t from-black/85 via-black/45 to-black/25" />
          <div className="flex min-h-[640px] flex-col justify-end gap-8 p-5 pb-6 sm:p-10 lg:min-h-[720px] lg:p-14">
            <div className="max-w-3xl text-white">
              <Eyebrow text={blok.eyebrow} />
              <Headline blok={blok} accentClass="text-emerald-300" className="mt-4 text-[34px] font-semibold leading-[1.05] tracking-tighter2 sm:text-[52px] lg:text-[64px]" />
              {blok.subhead && <p className="mt-4 max-w-2xl text-[16px] leading-relaxed text-white/80 sm:text-lg">{blok.subhead}</p>}
              <div className="mt-5">
                <Pills blok={blok} tone="glass" />
              </div>
              <div className="mt-7">
                <Ctas blok={blok} />
              </div>
            </div>
            <div className="grid gap-4 lg:grid-cols-[1fr_auto] lg:items-end">
              <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
                {(blok.boxes ?? []).map((b: Blok) => (
                  <div key={b._uid} className="rounded-xl border border-white/15 bg-white/10 p-4 text-white backdrop-blur-md">
                    <p className="text-[15px] font-semibold">{b.title}</p>
                    <p className="mt-1 text-[13px] leading-snug text-white/70">{b.text}</p>
                  </div>
                ))}
              </div>
              <div className="flex flex-col gap-3 text-white lg:items-end">
                <LogoRow label={blok.built_by_label} logos={blok.built_by_logos} />
                <LogoRow label={blok.backed_by_label} logos={blok.backed_by_logos} names={blok.backed_by_names} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ----------------------------- 2. Split ---------------------------- */
function HeroSplit({ blok }: { blok: Blok }) {
  const boxes: Blok[] = blok.boxes ?? [];
  const spots = ['left-4 top-4 sm:left-5 sm:top-5', 'right-4 top-1/2 -translate-y-1/2 sm:right-5', 'bottom-4 left-4 sm:bottom-5 sm:left-5'];
  return (
    <div className="relative overflow-hidden bg-paper pb-10 pt-8 sm:pt-12 lg:pb-14">
      <div className="pointer-events-none absolute -left-40 -top-40 h-[520px] w-[520px] rounded-full bg-brand-soft blur-3xl" aria-hidden />
      <div className="wrap relative grid items-center gap-10 lg:grid-cols-[1.05fr_1fr] lg:gap-14">
        <div>
          <Eyebrow text={blok.eyebrow} />
          <Headline
            blok={blok}
            accentClass="text-brand"
            className="mt-5 text-[40px] font-bold leading-[1.02] tracking-tighter2 sm:text-[58px] lg:text-[68px]"
          />
          {blok.subhead && <p className="mt-5 max-w-xl text-[18px] leading-relaxed text-ink-2 sm:text-[21px]">{blok.subhead}</p>}
          <div className="mt-6">
            <Pills blok={blok} tone="light" />
          </div>
          <div className="mt-8">
            <Ctas blok={blok} secondary="ghost" />
          </div>
          <div className="mt-10 grid gap-5 border-t border-line pt-6 sm:grid-cols-2">
            <LogoRow label={blok.built_by_label} logos={blok.built_by_logos} align="left" dark={false} />
            <LogoRow label={blok.backed_by_label} logos={blok.backed_by_logos} names={blok.backed_by_names} align="left" dark={false} />
          </div>
        </div>
        <div className="relative">
          <div className="relative aspect-[4/5] overflow-hidden rounded-[28px] bg-night shadow-[0_30px_80px_-30px_rgba(6,136,82,0.45)] sm:aspect-[5/5] lg:aspect-[4/5]">
            <BgVideo blok={blok} />
            <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-black/10" />
            <span className="absolute right-4 top-4 inline-flex items-center gap-1.5 rounded-full bg-black/50 px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-white backdrop-blur sm:right-5 sm:top-5">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-red-500" aria-hidden /> Life at Scaler
            </span>
            {boxes.slice(0, 3).map((b, i) => (
              <div key={b._uid} className={`absolute max-w-[220px] rounded-2xl bg-black/75 p-3.5 shadow-xl ring-1 ring-white/15 backdrop-blur ${spots[i]}`}>
                <p className="text-[18px] font-bold leading-tight text-brand-deep">{b.title}</p>
                <p className="mt-0.5 text-[12.5px] leading-snug text-ink-3">{b.text}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/* --------------------------- 3. Full bleed -------------------------- */
function HeroFullBleed({ blok }: { blok: Blok }) {
  const boxes: Blok[] = blok.boxes ?? [];
  return (
    <div className="relative isolate overflow-hidden bg-night text-white">
      <div className="absolute inset-0 -z-10">
        <BgVideo blok={blok} className="scale-105" />
      </div>
      <div className="absolute inset-0 -z-10 bg-gradient-to-r from-black/90 via-black/60 to-black/25" />
      <div className="absolute inset-x-0 bottom-0 -z-10 h-1/2 bg-gradient-to-t from-black/90 to-transparent" />
      <div className="wrap flex min-h-[680px] flex-col justify-between gap-12 pb-0 pt-16 lg:min-h-[760px] lg:pt-24">
        <div className="grid gap-10 lg:grid-cols-[1.4fr_1fr] lg:items-end">
          <div>
            <Eyebrow text={blok.eyebrow} dark />
            <Headline
              blok={blok}
              accentClass="text-emerald-300"
              className="mt-5 max-w-3xl text-[31px] font-bold uppercase leading-[0.98] tracking-tight min-[400px]:text-[34px] sm:text-[56px] lg:text-[72px]"
            />
            {blok.subhead && <p className="mt-6 max-w-xl text-[18px] font-medium leading-relaxed text-white/85 sm:text-[22px]">{blok.subhead}</p>}
            <div className="mt-6">
              <Pills blok={blok} tone="outline" />
            </div>
            <div className="mt-8">
              <Ctas blok={blok} />
            </div>
            {blok.deadline_note && <p className="mt-4 text-[13px] font-semibold text-white/75">{blok.deadline_note}</p>}
          </div>
          <div className="flex flex-col gap-5 lg:items-end">
            <LogoRow label={blok.built_by_label} logos={blok.built_by_logos} />
            <LogoRow label={blok.backed_by_label} logos={blok.backed_by_logos} names={blok.backed_by_names} />
          </div>
        </div>
        <div className="grid grid-cols-1 divide-y divide-white/15 border-t border-white/20 sm:grid-cols-3 sm:divide-x sm:divide-y-0">
          {boxes.map((b) => (
            <div key={b._uid} className="py-5 sm:px-6 sm:first:pl-0">
              <p className="text-[18px] font-bold">{b.title}</p>
              <p className="mt-1 text-[14px] leading-snug text-white/65">{b.text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ----------------------------- 4. Mosaic ---------------------------- */
function HeroMosaic({ blok }: { blok: Blok }) {
  const tiles: Blok[] = blok.tiles ?? [];
  const boxes: Blok[] = blok.boxes ?? [];
  return (
    <div className="relative isolate overflow-hidden bg-night text-white">
      <div className="absolute inset-0 -z-10 opacity-35 mix-blend-luminosity">
        <BgVideo blok={blok} />
      </div>
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-night via-night/90 to-[#04321d]/90" />
      <div
        className="absolute inset-0 -z-10 opacity-[0.07]"
        style={{ backgroundImage: 'linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)', backgroundSize: '56px 56px' }}
        aria-hidden
      />
      <div className="wrap grid gap-10 py-14 lg:grid-cols-[1fr_1fr] lg:items-center lg:gap-14 lg:py-16">
        <div>
          <Eyebrow text={blok.eyebrow} dark />
          <Headline
            blok={blok}
            accentClass="text-emerald-300"
            className="mt-5 text-[38px] font-bold leading-[1.02] tracking-tighter2 sm:text-[54px] lg:text-[62px]"
          />
          {blok.subhead && <p className="mt-5 max-w-xl text-[17px] leading-relaxed text-white/80 sm:text-[19px]">{blok.subhead}</p>}
          <div className="mt-6">
            <Pills blok={blok} tone="glass" />
          </div>
          <div className="mt-8">
            <Ctas blok={blok} />
          </div>
          <dl className="mt-10 grid grid-cols-3 gap-3 border-t border-white/15 pt-6">
            {boxes.map((b) => (
              <div key={b._uid}>
                <dt className="text-[15px] font-bold sm:text-[17px]">{b.title}</dt>
                <dd className="mt-1 text-[12px] leading-snug text-white/60 sm:text-[13px]">{b.text}</dd>
              </div>
            ))}
          </dl>
        </div>
        <div>
          {blok.tiles_title && <p className="mb-3 text-[12px] font-semibold uppercase tracking-[0.14em] text-emerald-300">{blok.tiles_title}</p>}
          <ul className="grid grid-cols-2 gap-3">
            {tiles.map((t, i) => (
              <li key={t._uid} className={`group relative aspect-[4/5] overflow-hidden rounded-2xl bg-night lg:aspect-square ${i % 2 === 1 ? 'lg:translate-y-8' : ''}`}>
                <Img asset={t.image} className="h-full w-full object-cover transition duration-700 group-hover:scale-105" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-transparent" />
                <div className="absolute inset-x-0 bottom-0 p-4">
                  <p className="text-[12px] font-semibold text-emerald-300">{String(i + 1).padStart(2, '0')} · {t.label}</p>
                  <p className="mt-1 text-[15px] font-semibold leading-snug sm:text-[17px]">{t.title}</p>
                </div>
              </li>
            ))}
          </ul>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:mt-14">
            <LogoRow label={blok.built_by_label} logos={blok.built_by_logos} align="left" />
            <LogoRow label={blok.backed_by_label} logos={blok.backed_by_logos} names={blok.backed_by_names} align="left" />
          </div>
        </div>
      </div>
    </div>
  );
}

const LAYOUTS: Record<string, (p: { blok: Blok }) => React.ReactNode> = {
  card: HeroCard,
  split: HeroSplit,
  fullbleed: HeroFullBleed,
  mosaic: HeroMosaic,
};

function HeroBody({ blok }: { blok: Blok }) {
  const L = LAYOUTS[blok.layout] ?? HeroCard;
  return <L blok={blok} />;
}

export function Hero({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok}>
      <HeroBody blok={blok} />
    </Section>
  );
}

/** Several hero designs with a 1·2·3·4 bar to switch between them. */
export function HeroOptions({ blok }: { blok: Blok }) {
  const options: Blok[] = blok.options ?? [];
  if (!options.length) return null;
  return (
    <Section blok={blok}>
      <HeroSwitcher
        show={blok.show_switcher !== false && options.length > 1}
        title={blok.switcher_title || 'Hero options'}
        labels={options.map((o) => o.option_label || o.headline)}
        panels={options.map((o) => (
          <HeroBody key={o._uid} blok={o} />
        ))}
      />
    </Section>
  );
}
