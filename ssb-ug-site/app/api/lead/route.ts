import { NextResponse } from 'next/server';

// Receives waitlist / brochure / info-session sign-ups from the lead form.
// Forwards them to LEAD_WEBHOOK_URL (e.g. a Google Apps Script that appends to
// a Sheet, or Scaler's CRM once it is connected). OTP verification and the full
// application flow come in a later phase.
const FIELDS = ['name', 'email', 'phone', 'grade', 'school', 'state', 'intent', 'page', 'utm_source', 'utm_medium', 'utm_campaign'];

export async function POST(req: Request) {
  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false, error: 'Invalid JSON' }, { status: 400 });
  }
  const lead: Record<string, string> = { submitted_at: new Date().toISOString(), source: 'SSB-UG-Website' };
  for (const f of FIELDS) lead[f] = String(body[f] ?? '').slice(0, 300);
  if (!lead.name || !/^\d{10}$/.test(lead.phone) || !/^\S+@\S+\.\S+$/.test(lead.email) || !lead.grade || !lead.school || !lead.state) {
    return NextResponse.json({ ok: false, error: 'Missing or invalid fields' }, { status: 422 });
  }

  const hook = process.env.LEAD_WEBHOOK_URL;
  if (!hook) {
    console.warn('[lead] LEAD_WEBHOOK_URL is not set; lead not forwarded', { intent: lead.intent, page: lead.page });
    return NextResponse.json({ ok: true, forwarded: false });
  }
  try {
    const res = await fetch(hook, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(lead) });
    if (!res.ok) throw new Error(`Webhook responded ${res.status}`);
    return NextResponse.json({ ok: true, forwarded: true });
  } catch (e) {
    console.error('[lead] forward failed', e);
    return NextResponse.json({ ok: false, error: 'Could not save. Please try again.' }, { status: 502 });
  }
}
