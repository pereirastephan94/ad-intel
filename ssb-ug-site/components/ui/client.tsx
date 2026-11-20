'use client';

import { useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import { PREVIEW } from '@/lib/preview';

/* ------------------------------------------------------------------ */
/* Carousel: native horizontal scroll with snap, plus prev/next.      */
/* ------------------------------------------------------------------ */
export function Carousel({
  children,
  label,
  dark,
  itemClass = 'w-[78%] sm:w-[46%] lg:w-[31%]',
}: {
  children: ReactNode[];
  label?: string;
  dark?: boolean;
  itemClass?: string;
}) {
  const ref = useRef<HTMLUListElement>(null);
  const [edge, setEdge] = useState({ start: true, end: false });
  const update = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    setEdge({ start: el.scrollLeft < 8, end: el.scrollLeft + el.clientWidth > el.scrollWidth - 8 });
  }, []);
  useEffect(() => {
    update();
    const el = ref.current;
    el?.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    return () => {
      el?.removeEventListener('scroll', update);
      window.removeEventListener('resize', update);
    };
  }, [update]);
  const go = (dir: number) => {
    const el = ref.current;
    if (!el) return;
    el.scrollBy({ left: dir * el.clientWidth * 0.9, behavior: 'smooth' });
  };
  const btn = `grid h-10 w-10 place-items-center rounded-full border transition disabled:opacity-30 ${
    dark ? 'border-white/20 text-white hover:bg-white/10' : 'border-line-strong bg-white text-ink hover:bg-surface'
  }`;
  return (
    <div>
      <ul
        ref={ref}
        aria-label={label}
        className="no-scrollbar -mx-4 flex snap-x snap-mandatory gap-4 overflow-x-auto scroll-px-4 px-4 pb-2 sm:-mx-6 sm:scroll-px-6 sm:px-6 lg:mx-0 lg:scroll-px-0 lg:px-0"
      >
        {children.map((c, i) => (
          <li key={i} className={`shrink-0 snap-start ${itemClass}`}>
            {c}
          </li>
        ))}
      </ul>
      {children.length > 1 && (
        <div className="mt-5 flex justify-end gap-2">
          <button type="button" className={btn} onClick={() => go(-1)} disabled={edge.start} aria-label="Previous">
            <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8">
              <path d="M12 5l-5 5 5 5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
          <button type="button" className={btn} onClick={() => go(1)} disabled={edge.end} aria-label="Next">
            <svg viewBox="0 0 20 20" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8">
              <path d="M8 5l5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Tabs                                                               */
/* ------------------------------------------------------------------ */
export function Tabs({ labels, panels, dark }: { labels: string[]; panels: ReactNode[]; dark?: boolean }) {
  const [active, setActive] = useState(0);
  return (
    <div>
      <div
        role="tablist"
        className={`no-scrollbar inline-flex max-w-full gap-1 overflow-x-auto rounded-xl border p-1 ${
          dark ? 'border-white/10 bg-white/5' : 'border-line bg-white'
        }`}
      >
        {labels.map((l, i) => (
          <button
            key={l}
            role="tab"
            type="button"
            aria-selected={active === i}
            onClick={() => setActive(i)}
            className={`whitespace-nowrap rounded-lg px-4 py-2 text-sm font-medium transition ${
              active === i
                ? 'bg-brand text-white'
                : dark
                  ? 'text-white/70 hover:text-white'
                  : 'text-ink-3 hover:text-ink'
            }`}
          >
            {l}
          </button>
        ))}
      </div>
      <div role="tabpanel" className="mt-8">
        {panels[active]}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Video: a thumbnail that opens a YouTube or MP4 player in a dialog. */
/* ------------------------------------------------------------------ */
function youtubeId(url?: string) {
  if (!url) return null;
  const m = url.match(/(?:youtu\.be\/|v=|embed\/|shorts\/)([A-Za-z0-9_-]{11})/);
  return m ? m[1] : /^[A-Za-z0-9_-]{11}$/.test(url) ? url : null;
}

export function VideoTrigger({ video, children, className = '' }: { video?: string; children: ReactNode; className?: string }) {
  const [open, setOpen] = useState(false);
  if (!video) return <div className={className}>{children}</div>;
  const yt = youtubeId(video);
  // The static preview copy can't embed YouTube, so those videos open on YouTube.
  if (PREVIEW && yt) {
    return (
      <a href={`https://www.youtube.com/watch?v=${yt}`} target="_blank" rel="noreferrer" className={`group block w-full text-left ${className}`}>
        {children}
      </a>
    );
  }
  return (
    <>
      <button type="button" onClick={() => setOpen(true)} className={`group block w-full text-left ${className}`}>
        {children}
      </button>
      {open && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-[80] grid place-items-center bg-black/85 p-4"
          onClick={() => setOpen(false)}
        >
          <div className="relative aspect-video w-full max-w-5xl overflow-hidden rounded-2xl bg-black" onClick={(e) => e.stopPropagation()}>
            {yt ? (
              <iframe
                className="h-full w-full"
                src={`https://www.youtube-nocookie.com/embed/${yt}?autoplay=1&rel=0`}
                title="Video"
                allow="autoplay; encrypted-media; picture-in-picture"
                allowFullScreen
              />
            ) : (
              <video className="h-full w-full" src={video} controls autoPlay playsInline />
            )}
          </div>
          <button type="button" className="absolute right-5 top-5 rounded-full bg-white/10 px-4 py-2 text-sm text-white" onClick={() => setOpen(false)}>
            Close
          </button>
        </div>
      )}
    </>
  );
}

/* ------------------------------------------------------------------ */
/* Countdown to the application deadline (announcement bar).          */
/* ------------------------------------------------------------------ */
export function Countdown({ to }: { to: string }) {
  const target = new Date(to).getTime();
  const [now, setNow] = useState<number | null>(null);
  useEffect(() => {
    setNow(Date.now());
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);
  if (now === null || Number.isNaN(target) || target <= now) return null;
  const s = Math.floor((target - now) / 1000);
  const parts: [number, string][] = [
    [Math.floor(s / 86400), 'd'],
    [Math.floor((s % 86400) / 3600), 'h'],
    [Math.floor((s % 3600) / 60), 'm'],
    [s % 60, 's'],
  ];
  return (
    <span className="ml-2 hidden items-center gap-1 font-mono tabular-nums sm:inline-flex" aria-label="Time left">
      {parts.map(([v, u]) => (
        <span key={u} className="rounded bg-brand px-1.5 py-0.5 text-[11px]">
          {String(v).padStart(2, '0')}
          {u}
        </span>
      ))}
    </span>
  );
}
