#!/usr/bin/env bash
# Builds a static "internal preview" copy of the site into ./out-preview, for
# hosting as plain files (e.g. a private claude.ai link for team review).
# Links and images are relative, sign-up forms are off, and a banner marks it
# as a preview. Usage (from ssb-ug-site/): bash scripts/build-preview.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# Build in a throwaway copy: a static export can't include the /api route.
tar -C "$ROOT" --exclude=node_modules --exclude=.next --exclude=out --exclude=out-preview -cf - . | tar -C "$WORK" -xf -
ln -s "$ROOT/node_modules" "$WORK/node_modules"
rm -rf "$WORK/app/api"
sed -i 's/export const dynamicParams = true;/export const dynamicParams = false;/; s/^export const revalidate = 60;$//' "$WORK/app/[...slug]/page.tsx" "$WORK/app/page.tsx"
cat > "$WORK/next.config.mjs" <<'EOF'
import path from 'node:path';
import { fileURLToPath } from 'node:url';
export default { output: 'export', outputFileTracingRoot: path.dirname(fileURLToPath(import.meta.url)), images: { unoptimized: true } };
EOF
(cd "$WORK" && NEXT_PUBLIC_PREVIEW_EXPORT=1 NEXT_TELEMETRY_DISABLED=1 npx next build >/dev/null)

OUT="$ROOT/out-preview"
rm -rf "$OUT"
cp -r "$WORK/out" "$OUT"

python3 - "$OUT" <<'EOF'
import glob, os, re, sys
os.chdir(sys.argv[1])
pages = ['home.html', 'curriculum.html', 'admission.html', 'career-pathways.html', 'student-life.html']
os.rename('index.html', 'home.html')
# Make Next's own asset paths relative, so the copy works from any folder, and
# rename _next/ to assets/ (hosts such as claude.ai reserve names starting "_").
os.rename('_next', 'assets')
for f in pages:
    s = open(f, encoding='utf-8').read()
    open(f, 'w', encoding='utf-8').write(re.sub(r'(\\?")/_next/', r'\1assets/', s))
for f in glob.glob('assets/static/chunks/webpack-*.js'):
    s = open(f).read()
    assert 'r.p="/_next/"' in s
    open(f, 'w').write(s.replace('r.p="/_next/"', 'r.p="assets/"'))
# The catch-all page's chunk folder is named "[...slug]"; give it a plain name.
for d in glob.glob('assets/static/chunks/app/[[]*[]]'):
    os.rename(d, 'assets/static/chunks/app/slug')
for f in pages + glob.glob('assets/static/chunks/*.js'):
    s = open(f, encoding='utf-8').read()
    t = s.replace('app/%5B...slug%5D/', 'app/slug/').replace('app/[...slug]/', 'app/slug/')
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
for f in glob.glob('assets/static/css/*.css'):
    s = open(f).read()
    open(f, 'w').write(s.replace('url(/_next/static/media/', 'url(../media/'))
# Some hosts reject XML DTD declarations in SVGs; they aren't needed to render.
for f in glob.glob('**/*.svg', recursive=True):
    s = open(f, encoding='utf-8', errors='ignore').read()
    t = re.sub(r'<!DOCTYPE[^>]*>\s*', '', s)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
# Some hosts reject a raw U+FFFD character; inside JS strings the \\uFFFD escape is identical.
for f in glob.glob('assets/**/*.js', recursive=True):
    s = open(f, encoding='utf-8').read()
    if '\ufffd' in s:
        open(f, 'w', encoding='utf-8').write(s.replace('\ufffd', '\\uFFFD'))
# Entry page: forwards to the real home page.
open('index.html', 'w').write('''<title>SSB UG Website Preview</title>
<meta http-equiv="refresh" content="0; url=home.html">
<style>body{font-family:system-ui,sans-serif;background:#fff;color:#121212;display:grid;place-items:center;min-height:100vh;margin:0;padding-inline:max(16px,env(safe-area-inset-left,0px)) max(16px,env(safe-area-inset-right,0px))}a{color:#CC5500;font-weight:600}</style>
<p>Opening the SSB UG website preview… <a href="home.html">Open it</a></p>
<script>location.replace('home.html')</script>
''')
# List only the files the pages actually use (keeps the upload small).
text = ''.join(open(p, encoding='utf-8').read() for p in pages)
text += ''.join(open(f, encoding='utf-8', errors='ignore').read() for f in glob.glob('assets/**/*.js', recursive=True) + glob.glob('assets/**/*.css', recursive=True))
used = set(pages)
for r, _, fs in os.walk('.'):
    for name in fs:
        f = os.path.relpath(os.path.join(r, name))
        # Skip payload files and Pages Router leftovers (_error, _buildManifest):
        # the App Router pages don't load them, and hosts reserve "_" names.
        if f.endswith('.txt') or f in ('404.html', 'index.html') or name.startswith('_') or f in used:
            continue
        if (name if f.startswith('assets/') else f) in text:
            used.add(f)
open('files.txt', 'w').write('\n'.join(sorted(used)) + '\n')
print(f'{len(used)} files, {sum(os.path.getsize(f) for f in used) / 1e6:.1f} MB')
EOF
echo "Preview built in $OUT (entry: index.html)"
