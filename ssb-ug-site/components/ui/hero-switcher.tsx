'use client';

import { useEffect, useState, type ReactNode } from 'react';

// A slim bar above the hero with numbered buttons (1, 2, 3, 4) to compare
// hero designs. The choice is kept in the URL (?hero=3) so a link can point
// straight at one option.
export function HeroSwitcher({ show, title, labels, panels }: { show: boolean; title: string; labels: string[]; panels: ReactNode[] }) {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const n = Number(new URLSearchParams(window.location.search).get('hero'));
    if (n >= 1 && n <= panels.length) setActive(n - 1);
  }, [panels.length]);

  const pick = (i: number) => {
    setActive(i);
    try {
      const url = new URL(window.location.href);
      url.searchParams.set('hero', String(i + 1));
      window.history.replaceState(null, '', url);
    } catch {
      // URL update is a convenience only
    }
  };

  return (
    <>
      {show && (
        <div className="border-b border-line bg-surface">
          <div className="wrap flex items-center gap-3 py-2.5">
            <span className="shrink-0 text-[11px] font-semibold uppercase tracking-[0.12em] text-ink-3">{title}</span>
            <div role="tablist" aria-label={title} className="no-scrollbar flex min-w-0 gap-1.5 overflow-x-auto">
              {labels.map((l, i) => (
                <button
                  key={i}
                  type="button"
                  role="tab"
                  aria-selected={active === i}
                  title={l}
                  onClick={() => pick(i)}
                  className={`flex shrink-0 items-center gap-2 rounded-lg border px-2.5 py-1.5 text-[13px] font-medium transition ${
                    active === i ? 'border-brand bg-brand text-white' : 'border-line-strong bg-white text-ink-2 hover:border-brand hover:text-brand-dark'
                  }`}
                >
                  <span
                    className={`grid h-5 w-5 place-items-center rounded-md text-[12px] font-bold ${active === i ? 'bg-white/20' : 'bg-surface-2 text-ink'}`}
                  >
                    {i + 1}
                  </span>
                  <span className="hidden max-w-[220px] truncate md:inline">{l}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
      <div key={active}>{panels[active]}</div>
    </>
  );
}
