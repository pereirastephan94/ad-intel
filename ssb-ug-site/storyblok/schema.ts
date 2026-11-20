// Builds Storyblok component (block) definitions by reading the bundled content
// in /content. Every block type and field used on the site becomes a Storyblok
// component with a matching field type, so the content can be pushed 1:1.
import fs from 'node:fs';
import path from 'node:path';
import { localStories } from '../content';
import type { Blok } from '../lib/types';

type Field = Record<string, any>;
type Component = {
  name: string;
  display_name: string;
  is_root: boolean;
  is_nestable: boolean;
  schema: Record<string, Field>;
  preview_field?: string;
};

const ROOTS = new Set(['page', 'site_config']);
const OPTION_FIELDS = new Set(['tone', 'layout', 'size', 'card_style']);
const IMAGE_EXT = /\.(png|jpe?g|webp|gif|svg|avif)$/i;
const VIDEO_EXT = /\.(mp4|webm|mov)$/i;

const title = (s: string) => s.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
const isBlokArray = (v: unknown): v is Blok[] => Array.isArray(v) && v.length > 0 && typeof v[0] === 'object' && 'component' in (v[0] as object);
const isAsset = (v: unknown): v is { filename: string } => !!v && typeof v === 'object' && !Array.isArray(v) && 'filename' in (v as object);
const isAssetArray = (v: unknown) => Array.isArray(v) && v.length > 0 && isAsset(v[0]);
const isTable = (v: unknown) => !!v && typeof v === 'object' && 'thead' in (v as object) && 'tbody' in (v as object);

export function buildComponents(): Component[] {
  const comps = new Map<string, Component>();
  const options = new Map<string, Set<string>>(); // "comp.field" -> values
  const whitelist = new Map<string, Set<string>>(); // "comp.field" -> nested component names

  const visit = (blok: Blok) => {
    let c = comps.get(blok.component);
    if (!c) {
      c = { name: blok.component, display_name: title(blok.component), is_root: ROOTS.has(blok.component), is_nestable: !ROOTS.has(blok.component), schema: {} };
      comps.set(blok.component, c);
    }
    let pos = Object.keys(c.schema).length;
    for (const [key, value] of Object.entries(blok)) {
      if (key === '_uid' || key === 'component' || key === '_editable') continue;
      const k = `${blok.component}.${key}`;
      let field: Field | undefined;
      if (isBlokArray(value)) {
        const wl = whitelist.get(k) ?? new Set<string>();
        value.forEach((v) => wl.add(v.component));
        whitelist.set(k, wl);
        field = { type: 'bloks' };
        value.forEach(visit);
      } else if (isAssetArray(value)) {
        field = { type: 'multiasset', filetypes: ['images'] };
      } else if (isAsset(value)) {
        const f = value.filename;
        field = { type: 'asset', filetypes: VIDEO_EXT.test(f) ? ['videos'] : IMAGE_EXT.test(f) ? ['images'] : ['images', 'videos'] };
      } else if (isTable(value)) {
        field = { type: 'table' };
      } else if (typeof value === 'boolean') {
        field = { type: 'boolean' };
      } else if (OPTION_FIELDS.has(key)) {
        const set = options.get(k) ?? new Set<string>();
        set.add(String(value));
        options.set(k, set);
        field = { type: 'option' };
      } else if (typeof value === 'string') {
        field = { type: value.includes('\n') || value.length > 90 ? 'textarea' : 'text' };
      }
      if (!field) continue;
      const prev = c.schema[key];
      // Prefer the richer type if the same field appears with different shapes.
      if (!prev || (prev.type === 'text' && field.type === 'textarea')) {
        c.schema[key] = { ...field, pos: prev?.pos ?? pos++, display_name: title(key) };
      }
    }
  };

  for (const story of Object.values(localStories)) visit(story.content);

  // Fields the React components support that the current content doesn't use
  // yet, so editors can fill them in later (e.g. video links for testimonials).
  const text = { type: 'text' };
  const tone = { type: 'option' };
  const EXTRA: Record<string, Record<string, Field>> = {
    video_card: { video_url: { ...text, description: 'YouTube link or video file URL' } },
    bento_tile: { video_url: { ...text, description: 'YouTube link or video file URL' }, badge: { type: 'asset', filetypes: ['images'] } },
    stat: { tag: text },
    proof_bar: { footnote: text },
    stat_strip: { eyebrow: text, headline: text, muted: text, subhead: text, tone },
    pillars: { muted: text },
    story_scroll: { muted: text },
    video_feature: { muted: text, note: text },
    logo_wall: { subhead: text, tone },
    year_block: { tracks_title: text },
  };
  for (const name of ['people_tabs', 'bento_stats', 'innovation_lab', 'learn_section', 'admissions_summary', 'faq', 'process_steps', 'pathways', 'outcome_group', 'testimonials', 'campus_gallery']) {
    EXTRA[name] = { ...(EXTRA[name] ?? {}), subhead: { type: 'textarea' } };
  }
  for (const [name, fields] of Object.entries(EXTRA)) {
    const c = comps.get(name);
    if (!c) continue;
    let pos = Object.keys(c.schema).length;
    for (const [key, field] of Object.entries(fields)) {
      if (!c.schema[key]) c.schema[key] = { ...field, pos: pos++, display_name: title(key) };
    }
  }

  // Field details that only make sense once every story has been read.
  for (const c of comps.values()) {
    for (const [key, field] of Object.entries(c.schema)) {
      const k = `${c.name}.${key}`;
      if (field.type === 'bloks' && whitelist.has(k)) {
        field.restrict_components = true;
        field.restrict_type = '';
        field.component_whitelist = [...whitelist.get(k)!];
      }
      if (field.type === 'option') {
        const values = new Set([...(options.get(k) ?? [])]);
        if (key === 'tone') ['light', 'muted', 'dark'].forEach((v) => values.add(v));
        if (key === 'size') ['small', 'wide', 'wide_short', 'tall'].forEach((v) => values.add(v));
        if (key === 'layout') ['portrait', 'landscape'].forEach((v) => values.add(v));
        field.options = [...values].map((v) => ({ name: title(v), value: v }));
      }
      if (field.type === 'textarea' && ['pills', 'points', 'chips', 'tools', 'items', 'notes', 'tracks', 'names'].includes(key)) {
        field.description = 'One item per line.';
      }
      if (key.endsWith('_href') || key === 'href' || key === 'cta_href') {
        field.description = 'A page path like /admission, a full URL, or lead:waitlist / lead:brochure / lead:info-session to open the sign-up form.';
      }
    }
    const preview = ['headline', 'title', 'name', 'label', 'question', 'value', 'big'].find((f) => c.schema[f]);
    if (preview) c.preview_field = preview;
  }
  return [...comps.values()].sort((a, b) => a.name.localeCompare(b.name));
}

// `npx tsx storyblok/schema.ts` writes storyblok/components.json for review.
if (process.argv[1]?.endsWith('schema.ts')) {
  const out = path.resolve(process.cwd(), 'storyblok/components.json');
  const comps = buildComponents();
  fs.writeFileSync(out, JSON.stringify({ components: comps }, null, 2));
  console.log(`Wrote ${comps.length} components to storyblok/components.json`);
}
