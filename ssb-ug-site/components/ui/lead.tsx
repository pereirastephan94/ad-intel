'use client';

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

// Top-funnel lead capture: "Join the early waitlist", "Download Brochure" and
// "Book your info session" all open this form with a different intent.
// Submissions go to /api/lead, which forwards them to LEAD_WEBHOOK_URL
// (a Google Sheet script today, Scaler's CRM later).

export type Intent = 'waitlist' | 'brochure' | 'info-session';

const COPY: Record<Intent, { title: string; sub: string; button: string; done: string }> = {
  waitlist: {
    title: 'Join the early waitlist',
    sub: 'Be the first to hear when applications open, and get priority for information sessions.',
    button: 'Join the waitlist',
    done: "You're on the waitlist. Our admissions team will reach out on WhatsApp and email.",
  },
  brochure: {
    title: 'Download the brochure',
    sub: "Tell us where to send it. You'll also get updates on information sessions.",
    button: 'Send me the brochure',
    done: "Thanks! We'll send the brochure to your email and WhatsApp shortly.",
  },
  'info-session': {
    title: 'Book your info session',
    sub: 'A 30-minute live session on the programme, fees and scholarships. Weekday and weekend slots for students and parents.',
    button: 'Request a slot',
    done: "Thanks! Our admissions team will share available slots with you on WhatsApp and email.",
  },
};

const Ctx = createContext<(i: Intent) => void>(() => {});
export const useLead = () => useContext(Ctx);

export function LeadProvider({ children }: { children: ReactNode }) {
  const [intent, setIntent] = useState<Intent | null>(null);
  return (
    <Ctx.Provider value={setIntent}>
      {children}
      {intent && <LeadModal intent={intent} onClose={() => setIntent(null)} />}
    </Ctx.Provider>
  );
}

/** A CTA: `lead:waitlist` style hrefs open the form, anything else is a link. */
export function Cta({
  href,
  children,
  variant = 'primary',
  className = '',
}: {
  href?: string;
  children: ReactNode;
  variant?: 'primary' | 'ghost' | 'light' | 'link';
  className?: string;
}) {
  const open = useLead();
  // Literal class names so Tailwind keeps them in the production CSS.
  const VARIANTS = {
    primary: 'btn-primary',
    ghost: 'btn-ghost',
    light: 'btn-light',
    link: 'inline-flex items-center gap-1.5 text-sm font-semibold text-brand hover:text-brand-dark',
  } as const;
  const cls = `${VARIANTS[variant]} ${className}`;
  if (href?.startsWith('lead:')) {
    return (
      <button type="button" className={cls} onClick={() => open(href.slice(5) as Intent)}>
        {children}
      </button>
    );
  }
  return (
    <a href={href || '#'} className={cls}>
      {children}
    </a>
  );
}

function LeadModal({ intent, onClose }: { intent: Intent; onClose: () => void }) {
  const copy = COPY[intent] ?? COPY.waitlist;
  const [state, setState] = useState<'idle' | 'sending' | 'done' | 'error'>('idle');
  const [error, setError] = useState('');

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const phone = String(form.get('phone') || '').replace(/\D/g, '').slice(-10);
    if (phone.length !== 10) {
      setError('Please enter a valid 10-digit mobile number.');
      return;
    }
    setError('');
    setState('sending');
    const params = new URLSearchParams(window.location.search);
    const payload = {
      ...Object.fromEntries(form.entries()),
      phone,
      intent,
      page: window.location.pathname,
      utm_source: params.get('utm_source') || '',
      utm_medium: params.get('utm_medium') || '',
      utm_campaign: params.get('utm_campaign') || '',
    };
    try {
      const res = await fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      setState(res.ok ? 'done' : 'error');
    } catch {
      setState('error');
    }
  }

  const field = 'mt-1.5 w-full rounded-lg border border-line-strong bg-white px-3.5 py-2.5 text-[15px] outline-none focus:border-brand focus:ring-2 focus:ring-brand/20';
  const label = 'block text-[13px] font-medium text-ink-2';

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="lead-title" className="fixed inset-0 z-[90] flex items-end justify-center bg-black/60 sm:items-center sm:p-4" onClick={onClose}>
      <div className="max-h-[92vh] w-full overflow-y-auto rounded-t-2xl bg-white p-6 shadow-2xl sm:max-w-md sm:rounded-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="eyebrow">Scaler School of Business · UG</p>
            <h2 id="lead-title" className="mt-2 text-xl font-semibold tracking-tightish">
              {copy.title}
            </h2>
          </div>
          <button type="button" onClick={onClose} className="rounded-full p-1.5 text-ink-3 hover:bg-surface" aria-label="Close">
            <svg viewBox="0 0 20 20" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
              <path d="M5 5l10 10M15 5L5 15" strokeLinecap="round" />
            </svg>
          </button>
        </div>
        {state === 'done' ? (
          <div className="mt-6 rounded-xl bg-brand-soft p-5 text-[15px] text-brand-deep">{copy.done}</div>
        ) : (
          <form onSubmit={submit} className="mt-5 space-y-4">
            <p className="text-sm text-ink-3">{copy.sub}</p>
            <div>
              <label className={label} htmlFor="lead-name">Full name</label>
              <input id="lead-name" name="name" required autoComplete="name" className={field} />
            </div>
            <div>
              <label className={label} htmlFor="lead-phone">Mobile number</label>
              <div className="flex gap-2">
                <span className="mt-1.5 grid place-items-center rounded-lg border border-line-strong bg-surface px-3 text-sm text-ink-3">+91</span>
                <input id="lead-phone" name="phone" required inputMode="numeric" autoComplete="tel-national" maxLength={14} className={field} />
              </div>
            </div>
            <div>
              <label className={label} htmlFor="lead-email">Email</label>
              <input id="lead-email" name="email" type="email" required autoComplete="email" className={field} />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className={label} htmlFor="lead-role">I am a</label>
                <select id="lead-role" name="role" className={field} defaultValue="Student">
                  <option>Student</option>
                  <option>Parent</option>
                </select>
              </div>
              <div>
                <label className={label} htmlFor="lead-city">City</label>
                <input id="lead-city" name="city" required autoComplete="address-level2" className={field} />
              </div>
            </div>
            <div>
              <label className={label} htmlFor="lead-status">Current status</label>
              <select id="lead-status" name="status" className={field} defaultValue="Currently in Class XII">
                <option>Currently in Class XII</option>
                <option>Passed Class XII in 2026</option>
                <option>Other</option>
              </select>
            </div>
            <label className="flex items-start gap-2.5 text-[13px] text-ink-3">
              <input type="checkbox" name="consent" value="yes" defaultChecked className="mt-0.5 accent-brand" />
              I agree to be contacted by Scaler School of Business on WhatsApp, phone and email.
            </label>
            {error && <p className="text-sm text-red-600">{error}</p>}
            {state === 'error' && <p className="text-sm text-red-600">Something went wrong. Please try again.</p>}
            <button type="submit" disabled={state === 'sending'} className="btn-primary w-full disabled:opacity-60">
              {state === 'sending' ? 'Sending…' : copy.button}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
