import type { Story } from './types';
import { localStories } from '@/content';
import { previewize } from './preview';

// Storyblok Content Delivery API hosts per region.
const CDN_HOSTS: Record<string, string> = {
  eu: 'https://api.storyblok.com',
  us: 'https://api-us.storyblok.com',
  ap: 'https://api-ap.storyblok.com',
  ca: 'https://api-ca.storyblok.com',
  cn: 'https://app.storyblokchina.cn',
};

const token = process.env.STORYBLOK_PREVIEW_TOKEN;
const version = process.env.STORYBLOK_VERSION === 'draft' ? 'draft' : 'published';
const host = CDN_HOSTS[process.env.STORYBLOK_REGION ?? 'eu'] ?? CDN_HOSTS.eu;

export const usingStoryblok = Boolean(token);

/**
 * Loads a page. With a Storyblok token set, it reads the story from Storyblok
 * (draft or published). Without one, or if Storyblok has no such story yet,
 * it falls back to the bundled content in /content so the site always renders.
 */
export async function getStory(slug: string): Promise<Story | null> {
  if (token) {
    try {
      const url = `${host}/v2/cdn/stories/${encodeURIComponent(slug)}?version=${version}&token=${token}`;
      const res = await fetch(url, { next: { revalidate: version === 'draft' ? 0 : 60 } });
      if (res.ok) {
        const data = await res.json();
        return previewize(data.story as Story);
      }
    } catch {
      // fall through to local content
    }
  }
  return previewize(localStories[slug] ?? null);
}
