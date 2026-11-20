'use client';

import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { Countdown } from '@/components/ui/client';
import { Cta } from '@/components/ui/lead';
import type { Blok } from '@/lib/types';
import { PREVIEW, assetPath, pageHref } from '@/lib/preview';

export function Logo({ light }: { light?: boolean }) {
  return (
    <a href={pageHref('/')} className="flex items-center gap-2.5" aria-label="Scaler School of Business, home">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={assetPath('/logos/ssb.svg')} alt="" className={`h-8 w-auto ${light ? 'brightness-0 invert' : ''}`} />
      <span className={`text-[10px] font-bold uppercase leading-[1.05] tracking-[0.06em] ${light ? 'text-white' : 'text-ink'}`}>
        Scaler
        <br />
        School of
        <br />
        Business
      </span>
      <span className={`ml-1 rounded-md px-1.5 py-0.5 text-[10px] font-bold tracking-wider ${light ? 'bg-white/15 text-white' : 'bg-brand-soft text-brand-dark'}`}>
        UG
      </span>
    </a>
  );
}

export default function Header({ config }: { config: Blok }) {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const path = usePathname();
  const nav: Blok[] = config.nav ?? [];

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  useEffect(() => setOpen(false), [path]);

  return (
    <header className="sticky top-0 z-50">
      {config.announcement && (
        <div className="bg-night text-white">
          <div className="wrap flex min-h-9 items-center justify-center gap-2 py-1.5 text-center text-[12px] font-medium leading-snug sm:text-[13px]">
            <span>{config.announcement}</span>
            {config.deadline && <Countdown to={config.deadline} />}
          </div>
        </div>
      )}
      <div className={`border-b bg-white/95 backdrop-blur transition-colors ${scrolled ? 'border-line' : 'border-transparent'}`}>
        <div className="wrap flex h-16 items-center justify-between gap-6">
          <Logo />
          <nav aria-label="Main" className="hidden items-center gap-1 lg:flex">
            {nav.map((n) => {
              const active = PREVIEW
                ? !n.href.includes('#') &&
                  (n.href === 'home.html'
                    ? /\/((home|index)(\.html)?)?$/.test(path ?? '')
                    : (path ?? '').replace(/\.html$/, '').endsWith(`/${n.href.replace(/\.html$/, '')}`))
                : n.href === '/'
                  ? path === '/'
                  : path?.startsWith(n.href);
              return (
                <a
                  key={n._uid}
                  href={n.href}
                  className={`rounded-lg px-3 py-2 text-[14px] font-medium transition ${active ? 'text-brand' : 'text-ink-2 hover:text-ink'}`}
                >
                  {n.label}
                </a>
              );
            })}
          </nav>
          <div className="flex items-center gap-2">
            <Cta href={config.cta_href} className="hidden !px-4 !py-2.5 sm:inline-flex">
              {config.cta_label}
            </Cta>
            <button
              type="button"
              className="grid h-10 w-10 place-items-center rounded-lg border border-line lg:hidden"
              aria-label={open ? 'Close menu' : 'Open menu'}
              aria-expanded={open}
              onClick={() => setOpen(!open)}
            >
              <svg viewBox="0 0 20 20" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
                {open ? <path d="M5 5l10 10M15 5L5 15" strokeLinecap="round" /> : <path d="M3 6h14M3 10h14M3 14h14" strokeLinecap="round" />}
              </svg>
            </button>
          </div>
        </div>
        {open && (
          <nav aria-label="Mobile" className="border-t border-line bg-white lg:hidden">
            <div className="wrap flex flex-col py-3">
              {nav.map((n) => (
                <a key={n._uid} href={n.href} className="rounded-lg px-2 py-3 text-[15px] font-medium text-ink-2 hover:bg-surface">
                  {n.label}
                </a>
              ))}
              <Cta href={config.cta_href} className="mt-2 w-full">
                {config.cta_label}
              </Cta>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}
