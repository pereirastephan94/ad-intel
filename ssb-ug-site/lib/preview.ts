// "Preview export" mode builds a static copy of the site (no server) that can be
// hosted as plain files, e.g. as a private claude.ai link for internal review.
// Links and images become relative paths, sign-ups are switched off, and a
// banner marks the copy as a preview. Normal builds are unaffected.
export const PREVIEW = process.env.NEXT_PUBLIC_PREVIEW_EXPORT === '1';

/** "/curriculum#x" -> "curriculum.html#x", "/" -> "home.html" (preview only). */
export function pageHref(h?: string) {
  if (!PREVIEW || !h || !h.startsWith('/')) return h;
  const [path, hash] = h.split('#');
  const page = path === '/' || path === '' ? 'home' : path.replace(/^\/|\/$/g, '');
  return `${page}.html${hash ? `#${hash}` : ''}`;
}

/** "/campus/x.webp" -> "campus/x.webp" (preview only). */
export const assetPath = (s: string) => (PREVIEW && s.startsWith('/') ? s.slice(1) : s);

/** Rewrites every link and local asset path in a story for the preview copy. */
export function previewize<T>(node: T): T {
  if (!PREVIEW) return node;
  const walk = (v: any, key = ''): any => {
    if (Array.isArray(v)) return v.map((x) => walk(x));
    if (v && typeof v === 'object') {
      const out: any = {};
      for (const [k, x] of Object.entries(v)) out[k] = walk(x, k);
      return out;
    }
    if (typeof v === 'string' && (key === 'href' || key.endsWith('_href'))) return pageHref(v);
    if (typeof v === 'string' && key === 'filename') return assetPath(v);
    return v;
  };
  return walk(node);
}
