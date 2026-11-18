// How Claude should write the audit. Generic for any business.

export const AUDIT_GUIDE = `Ad Audit tools read the public Facebook Ad Library (active ads only, no spend or results data).

Workflow:
1. find_advertiser(name) -> show the candidate pages and confirm the right one with the user (a brand can run several pages).
2. list_ads(page_id) -> ads sorted longest-running first. Long-running ads and ads with many copies are the likely winners.
3. analyze_video(library_id) on the top video ads (3-5 unless asked for more; each takes up to a minute). Read the stills, not just the transcript: on-screen text often carries the proof (numbers, logos, names) and corrects transcription errors.

Write the audit with these sections:
- Snapshot: how many active ads, mix of video/image/carousel, oldest ad, landing pages used.
- Per top ad: hook in the first 3 seconds (exact words and what is on screen), who is on camera (founder, customer, creator, actor, no one), format (talking head, UGC, montage, screen recording, static, etc.), beats in order with timestamps, claims and the proof shown for each, offer, CTA and end card.
- Patterns: what repeats across ads (hooks, formats, presenters, claims, offers, visual style), and what they are testing (same script with different people or numbers, different headlines on one video).
- What to run against them: specific angles, hooks and proof the user can use to compete, and gaps nobody is covering.

Rules: every claim cites the ad's Library ID with its link, written as https://www.facebook.com/ads/library/?id=<id>. Separate what the ad shows from your interpretation. Say what you could not see (ads not loaded because of rate limits, videos not analysed, no spend data).`

export function auditPrompt(advertiser: string, myBusiness?: string): string {
  return (
    `Audit the Facebook and Instagram ads of "${advertiser}" using the Ad Audit tools.\n` +
    (myBusiness ? `My business is: ${myBusiness}. Make the "What to run against them" section specific to it.\n` : '') +
    '\n' +
    AUDIT_GUIDE
  )
}
