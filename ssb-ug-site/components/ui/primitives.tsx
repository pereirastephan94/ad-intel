import type { Asset, Blok } from '@/lib/types';
import type { ReactNode } from 'react';

type AssetLike = Asset | { filename?: string; alt?: string } | string | null | undefined;
export const src = (a?: AssetLike) => (typeof a === 'string' ? a : a?.filename) || '';
export const alt = (a?: AssetLike, fallback = '') => (typeof a === 'string' ? fallback : a?.alt) || fallback;

export function Img({
  asset,
  className = '',
  alt: altText,
  eager,
  style,
}: {
  asset?: AssetLike;
  className?: string;
  alt?: string;
  eager?: boolean;
  style?: React.CSSProperties;
}) {
  const s = src(asset);
  if (!s) return <div className={`bg-surface-2 ${className}`} aria-hidden />;
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={s}
      alt={altText ?? alt(asset)}
      loading={eager ? 'eager' : 'lazy'}
      decoding="async"
      className={className}
      style={style}
    />
  );
}

/** Storyblok's visual editor uses this attribute to highlight the block being edited. */
export function editable(blok: Blok) {
  if (!blok?._editable) return {};
  try {
    const json = JSON.parse(blok._editable.replace(/^<!--#storyblok#/, '').replace(/-->$/, ''));
    return { 'data-blok-c': JSON.stringify(json), 'data-blok-uid': `${json.id}-${json.uid}` };
  } catch {
    return {};
  }
}

export function Section({
  blok,
  children,
  className = '',
  tone = 'light',
  id,
}: {
  blok: Blok;
  children: ReactNode;
  className?: string;
  tone?: 'light' | 'muted' | 'dark';
  id?: string;
}) {
  const toneCls = tone === 'dark' ? 'bg-night text-white' : tone === 'muted' ? 'bg-surface' : 'bg-paper';
  return (
    <section id={id || blok.anchor || undefined} className={`${toneCls} scroll-mt-28 ${className}`} {...editable(blok)}>
      {children}
    </section>
  );
}

export function Heading({
  eyebrow,
  headline,
  muted,
  sub,
  dark,
  center,
  className = '',
}: {
  eyebrow?: string;
  headline?: string;
  muted?: string;
  sub?: string;
  dark?: boolean;
  center?: boolean;
  className?: string;
}) {
  return (
    <div className={`${center ? 'mx-auto text-center' : ''} max-w-3xl ${className}`}>
      {eyebrow && <p className={`eyebrow mb-3 ${dark ? 'text-emerald-400' : ''}`}>{eyebrow}</p>}
      {headline && (
        <h2 className="h-section">
          {headline}
          {muted && <span className={dark ? ' text-white/45' : ' text-ink-4'}> {muted}</span>}
        </h2>
      )}
      {sub && <p className={`h-sub ${center ? 'mx-auto' : ''} ${dark ? 'text-white/60' : ''}`}>{sub}</p>}
    </div>
  );
}

export function Chips({ items, dark }: { items?: (string | { text: string })[]; dark?: boolean }) {
  if (!items?.length) return null;
  return (
    <ul className="flex flex-wrap gap-2">
      {items.map((c, i) => (
        <li
          key={i}
          className={
            dark
              ? 'inline-flex items-center rounded-full border border-white/15 bg-white/5 px-3 py-1.5 text-[13px] font-medium text-white/85'
              : 'chip'
          }
        >
          <span className={`h-1.5 w-1.5 rounded-full ${dark ? 'bg-emerald-400' : 'bg-brand'}`} aria-hidden />
          {typeof c === 'string' ? c : c.text}
        </li>
      ))}
    </ul>
  );
}

/** Splits "a\nb" text fields into lines; Storyblok textareas use newlines. */
export const lines = (v?: string) => (v ? v.split('\n').map((s) => s.trim()).filter(Boolean) : []);

export function Tag({ children, dark }: { children: ReactNode; dark?: boolean }) {
  return (
    <span
      className={`inline-flex items-center rounded-md px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wider ${
        dark ? 'bg-white/10 text-white/80' : 'bg-brand-soft text-brand-dark'
      }`}
    >
      {children}
    </span>
  );
}

export function Arrow({ className = 'h-4 w-4' }: { className?: string }) {
  return (
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.8" className={className} aria-hidden>
      <path d="M4 10h12M11 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function Play({ className = 'h-5 w-5' }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden>
      <path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5Z" />
    </svg>
  );
}
