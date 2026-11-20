import type { Asset, Blok } from '@/lib/types';

// Small helpers to write content in Storyblok's exact JSON shape.
let counter = 0;
export function b(component: string, fields: Record<string, any> = {}): Blok {
  counter += 1;
  return { _uid: `${component}-${counter.toString(36).padStart(4, '0')}`, component, ...fields };
}

export const img = (filename: string, alt = ''): Asset => ({ filename, alt });

/** Several images at once (Storyblok "multi-assets" field). */
export const imgs = (...files: string[]): Asset[] => files.map((f) => img(f));

/** Storyblok "table" field shape. */
export function table(head: string[], rows: string[][]) {
  return {
    thead: head.map((value, i) => ({ _uid: `th-${i}`, value, component: '_table_head' })),
    tbody: rows.map((r, ri) => ({
      _uid: `tr-${ri}`,
      component: '_table_row',
      body: r.map((value, ci) => ({ _uid: `td-${ri}-${ci}`, value, component: '_table_col' })),
    })),
  };
}

/** Newline-separated list (Storyblok textarea), rendered as bullets or chips. */
export const list = (...items: string[]) => items.join('\n');

export const stat = (value: string, label: string, tag?: string) => b('stat', { value, label, ...(tag ? { tag } : {}) });
