// Pushes the whole site into a Storyblok space via the Management API:
//   1. creates/updates every block type (component schema),
//   2. uploads every image/video in /public that the content uses,
//   3. creates/updates each page as a story (and publishes it with --publish).
//
// Usage (from ssb-ug-site/):
//   STORYBLOK_PERSONAL_ACCESS_TOKEN=... STORYBLOK_SPACE_ID=... npx tsx storyblok/push.ts [--dry-run] [--publish] [--skip-assets]
// Region: STORYBLOK_REGION=eu|us|ap|ca|cn (defaults to eu).
// Safe to re-run: components and stories are matched by name/slug and updated.
import fs from 'node:fs';
import path from 'node:path';
import { buildComponents } from './schema';
import { localStories } from '../content';
import type { Blok } from '../lib/types';

const MAPI: Record<string, string> = {
  eu: 'https://mapi.storyblok.com/v1',
  us: 'https://api-us.storyblok.com/v1',
  ap: 'https://api-ap.storyblok.com/v1',
  ca: 'https://api-ca.storyblok.com/v1',
  cn: 'https://app.storyblokchina.cn/v1',
};

const args = new Set(process.argv.slice(2));
const DRY = args.has('--dry-run');
const PUBLISH = args.has('--publish');
const SKIP_ASSETS = args.has('--skip-assets');
const token = process.env.STORYBLOK_PERSONAL_ACCESS_TOKEN || process.env.STORYBLOK_OAUTH_TOKEN;
const spaceId = process.env.STORYBLOK_SPACE_ID;
const base = `${MAPI[process.env.STORYBLOK_REGION ?? 'eu'] ?? MAPI.eu}/spaces/${spaceId}`;
const PUBLIC_DIR = path.resolve(process.cwd(), 'public'); // run from ssb-ug-site/ (npm run storyblok:push)

if (!DRY && (!token || !spaceId)) {
  console.error('Set STORYBLOK_PERSONAL_ACCESS_TOKEN and STORYBLOK_SPACE_ID (or pass --dry-run).');
  process.exit(1);
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function api(method: string, url: string, body?: unknown): Promise<any> {
  if (DRY) {
    console.log(`[dry-run] ${method} ${url}`);
    return {};
  }
  for (let attempt = 0; attempt < 6; attempt++) {
    const res = await fetch(`${base}${url}`, {
      method,
      headers: { Authorization: token!, 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (res.status === 429) {
      await sleep(1000 * (attempt + 1));
      continue;
    }
    const text = await res.text();
    if (!res.ok) throw new Error(`${method} ${url} → ${res.status}: ${text.slice(0, 400)}`);
    await sleep(250); // stay under the Management API rate limit
    return text ? JSON.parse(text) : {};
  }
  throw new Error(`${method} ${url} → rate limited`);
}

async function listAll(url: string, key: string): Promise<any[]> {
  const out: any[] = [];
  for (let page = 1; ; page++) {
    const data = await api('GET', `${url}${url.includes('?') ? '&' : '?'}per_page=100&page=${page}`);
    const items = data[key] ?? [];
    out.push(...items);
    if (items.length < 100) return out;
  }
}

/* --------------------------- 1. Components --------------------------- */
async function pushComponents() {
  const comps = buildComponents();
  const existing = DRY ? [] : await listAll('/components', 'components');
  const byName = new Map(existing.map((c: any) => [c.name, c]));
  for (const c of comps) {
    const found = byName.get(c.name);
    if (found) await api('PUT', `/components/${found.id}`, { component: { ...found, ...c } });
    else await api('POST', '/components', { component: c });
    console.log(`${found ? 'updated' : 'created'} component ${c.name}`);
  }
}

/* ----------------------------- 2. Assets ----------------------------- */
const assetMap = new Map<string, { id: number; filename: string }>();

function collectAssets(node: unknown, acc: Set<string>) {
  if (Array.isArray(node)) node.forEach((n) => collectAssets(n, acc));
  else if (node && typeof node === 'object') {
    const o = node as Record<string, unknown>;
    if (typeof o.filename === 'string' && o.filename.startsWith('/')) acc.add(o.filename);
    Object.values(o).forEach((v) => collectAssets(v, acc));
  }
}

async function uploadAsset(local: string) {
  const file = path.join(PUBLIC_DIR, local);
  const buf = fs.readFileSync(file);
  const signed = await api('POST', '/assets', { filename: path.basename(local), size: '', validate_upload: 1 });
  if (DRY) return { id: 0, filename: local };
  const form = new FormData();
  for (const [k, v] of Object.entries(signed.fields)) form.append(k, String(v));
  form.append('file', new Blob([buf]), path.basename(local));
  const up = await fetch(signed.post_url, { method: 'POST', body: form });
  if (!up.ok && up.status !== 204) throw new Error(`upload ${local} → ${up.status}`);
  await api('GET', `/assets/${signed.id}/finish_upload`);
  return { id: signed.id, filename: signed.pretty_url as string };
}

async function pushAssets() {
  const all = new Set<string>();
  Object.values(localStories).forEach((s) => collectAssets(s.content, all));
  const existing = DRY ? [] : await listAll('/assets', 'assets');
  const byName = new Map(existing.map((a: any) => [String(a.filename).split('/').pop(), a]));
  for (const local of all) {
    // Storyblok keeps the original file name at the end of the asset URL.
    const known = byName.get(path.basename(local));
    const asset = known ? { id: known.id, filename: known.filename } : await uploadAsset(local);
    assetMap.set(local, asset);
    console.log(`${known ? 'reused' : 'uploaded'} ${local}`);
  }
}

function withStoryblokAssets(node: any): any {
  if (Array.isArray(node)) return node.map(withStoryblokAssets);
  if (node && typeof node === 'object') {
    const out: any = {};
    for (const [k, v] of Object.entries(node)) out[k] = withStoryblokAssets(v);
    if (typeof node.filename === 'string' && assetMap.has(node.filename)) {
      const a = assetMap.get(node.filename)!;
      Object.assign(out, { id: a.id, filename: a.filename, fieldtype: 'asset', alt: node.alt ?? '' });
    }
    return out;
  }
  return node;
}

/* ----------------------------- 3. Stories ---------------------------- */
async function pushStories() {
  for (const story of Object.values(localStories)) {
    const content = withStoryblokAssets(story.content as Blok);
    const existing = DRY ? null : (await api('GET', `/stories?with_slug=${encodeURIComponent(story.full_slug)}`)).stories?.[0];
    const payload = {
      story: {
        name: story.name,
        slug: story.slug,
        content,
        // The home story lives at "/" in the visual editor preview.
        ...(story.slug === 'home' ? { path: '/' } : {}),
      },
      publish: PUBLISH ? 1 : 0,
    };
    if (existing) await api('PUT', `/stories/${existing.id}`, { ...payload, force_update: 1 });
    else await api('POST', '/stories', payload);
    console.log(`${existing ? 'updated' : 'created'} story ${story.full_slug}${PUBLISH ? ' (published)' : ''}`);
  }
}

(async () => {
  console.log(`Storyblok space ${spaceId ?? '(dry run)'}${DRY ? ' — dry run, nothing is sent' : ''}`);
  await pushComponents();
  if (!SKIP_ASSETS) await pushAssets();
  await pushStories();
  console.log('Done.');
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
