import type { Blok } from '@/lib/types';
import { Logo } from './Header';

export default function Footer({ config }: { config: Blok }) {
  const cols: Blok[] = config.footer_columns ?? [];
  return (
    <footer className="bg-night text-white">
      <div className="wrap grid gap-10 py-14 md:grid-cols-[1.4fr_repeat(3,1fr)]">
        <div>
          <Logo light />
          <p className="mt-5 max-w-xs text-sm leading-relaxed text-white/55">{config.footer_blurb}</p>
          {config.address && <p className="mt-4 max-w-xs text-sm leading-relaxed text-white/40">{config.address}</p>}
        </div>
        {cols.map((c) => (
          <div key={c._uid}>
            <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-white/45">{c.title}</p>
            <ul className="mt-4 space-y-2.5">
              {(c.links ?? []).map((l: Blok) => (
                <li key={l._uid}>
                  <a href={l.href} className="text-sm text-white/75 hover:text-white">
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="border-t border-white/10">
        <div className="wrap flex flex-col gap-2 py-6 text-xs text-white/40 sm:flex-row sm:justify-between">
          <p>{config.copyright}</p>
          <p>{config.footnote}</p>
        </div>
      </div>
    </footer>
  );
}
