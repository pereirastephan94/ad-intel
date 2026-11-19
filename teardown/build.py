#!/usr/bin/env python3
"""Builds one self-contained ad teardown page from a research folder.

Usage: build.py <research_dir> <out_dir> "<Company name>"
Reads  <research_dir>/ads.json, videos/<asset>/{transcript.json,metrics.json,breakdown.md,still*.jpg},
       images/<library_id>.jpg, statics/<library_id>.md and the hand-written doc/<name>.md sections.
Writes <out_dir>/index.html (images embedded) plus <out_dir>/img/.

Hand-written sections (each is left out, with its link, when the file does not exist):
  doc/summary.md, doc/insights.md, doc/ssb-insights.md, doc/how-ads-run.md, doc/patterns.md, doc/website.md, doc/method.md
"""
import base64, collections, glob, html, json, os, re, sys, urllib.parse as U
import markdown
from PIL import Image

if len(sys.argv) != 4:
    sys.exit(__doc__)
R, OUT, COMPANY = sys.argv[1].rstrip('/'), sys.argv[2].rstrip('/'), sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT + '/img', exist_ok=True)
ads = json.load(open(R + '/ads.json'))
md = lambda s: markdown.markdown(s, extensions=['tables'])
esc = html.escape
C = collections.Counter

def frag(name):
    p = f'{R}/doc/{name}.md'
    return md(open(p).read()) if os.path.exists(p) and open(p).read().strip() else None
def utm(x, k):
    return (U.parse_qs(U.urlparse(x.get('landing_url') or '').query).get(k) or [''])[0]
def landing(x):
    u = U.urlparse((x.get('landing_url') or '').split('?')[0])
    return (u.netloc.removeprefix('www.') + (u.path.rstrip('/') or '/')) if u.netloc else '(no link)'
def group(x):
    """Product line of an ad: the line under the headline, else the first part of the landing page path."""
    ld = (x.get('link_description') or '').strip()
    if ld: return ld
    u = U.urlparse(x.get('landing_url') or '')
    seg = u.path.strip('/').split('/')[0]
    return '/' + seg if seg else (u.netloc.removeprefix('www.') or 'Not stated')
def title_of(text, fallback):
    m = re.match(r'#\s*(.+)', text or '')
    t = re.sub(r'\s*\(\d{10,}\)\s*$', '', m.group(1)).strip() if m else ''
    return t if t and not re.fullmatch(r'\d{10,}', t) else fallback
def body_of(text):
    return md(re.sub(r'^#.*\n', '', text, count=1))

# ---- videos
vids = []
for d in sorted(glob.glob(R + '/videos/*/')):
    if not os.path.exists(d + 'transcript.json'): continue
    a = os.path.basename(d.rstrip('/'))
    t = json.load(open(d + 'transcript.json'))
    m = json.load(open(d + 'metrics.json')) if os.path.exists(d + 'metrics.json') else {}
    uses = [x for x in ads.values() if x.get('video_asset') == a]
    bd = open(d + 'breakdown.md').read() if os.path.exists(d + 'breakdown.md') else ''
    stills = sorted(glob.glob(d + 'still*.jpg'))
    pick = stills[:5:2] + [stills[i] for i in (len(stills)*5//10, len(stills)*7//10, len(stills)-1)] if len(stills) >= 8 else stills
    sheet = False
    if pick:
        ims = [Image.open(p).convert('RGB') for p in pick]
        h = 260; ims = [i.resize((max(1, i.width * h // i.height), h)) for i in ims]
        im = Image.new('RGB', (sum(i.width for i in ims) + 4 * (len(ims) - 1), h), (255, 255, 255)); x = 0
        for i in ims: im.paste(i, (x, 0)); x += i.width + 4
        im.save(f'{OUT}/img/v_{a}.jpg', quality=72); sheet = True
    vids.append(dict(a=a, t=t, m=m, uses=uses, bd=bd, title=title_of(bd, a), sheet=sheet, prog=group(uses[0]) if uses else 'Not stated',
                     copies=sum(int(u.get('copies') or 1) for u in uses)))
vids.sort(key=lambda v: (v['prog'], -len(v['uses']), -v['copies']))

# ---- statics
stat = []
for p in sorted(glob.glob(R + '/images/*.jpg')):
    i = os.path.basename(p)[:-4]
    if i not in ads: continue
    try:
        im = Image.open(p).convert('RGB'); im.thumbnail((420, 420)); im.save(f'{OUT}/img/s_{i}.jpg', quality=72)
    except Exception as e:
        print('skipping unreadable image', i, e, file=sys.stderr); continue
    f = f'{R}/statics/{i}.md'
    stat.append(dict(i=i, x=ads[i], bd=open(f).read() if os.path.exists(f) else ''))
stat.sort(key=lambda s: (group(s['x']), s['x'].get('headline') or ''))

def table(rows, head):
    if not rows: return ''
    return '<div class="scroll"><table><thead><tr>' + ''.join(f'<th>{esc(h)}</th>' for h in head) + '</tr></thead><tbody>' + \
        ''.join('<tr>' + ''.join(f'<td>{esc(str(c))}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'
n = len(ads); copies = sum(int(x.get('copies') or 1) for x in ads.values())
fm = C((x.get('extra') or {}).get('display_format') or x.get('media_type') for x in ads.values())
numbers = table([[k, v] for k, v in C(group(x) for x in ads.values()).most_common()], ['Product line (the line under the headline, or the landing page)', 'Ads']) + \
    table([[k, v] for k, v in fm.most_common()], ['Format (DCO = Facebook mixes several images, videos and texts)', 'Ads']) + \
    table([[k or '(not given)', v] for k, v in sorted(C((x.get('start_date') or '')[:10] for x in ads.values()).items())], ['Start date', 'Ads started']) + \
    table([[k or '(no headline)', v] for k, v in C(x.get('headline') for x in ads.values()).most_common(30)], ['Headline under the ad', 'Ads']) + \
    table([[k or '(no button)', v] for k, v in C(x.get('cta') for x in ads.values()).most_common()], ['Button', 'Ads']) + \
    table([[k, v] for k, v in C(landing(x) for x in ads.values()).most_common(40)], ['Landing page', 'Ads']) + \
    table([[k.strip() or '(not tagged)', v] for k, v in C(utm(x, 'utm_campaign') for x in ads.values()).most_common(60)], ["Campaign name (the advertiser's own tag in the link)", 'Ads']) + \
    table([[k.strip() or '(not tagged)', v] for k, v in C(utm(x, 'utm_content') for x in ads.values()).most_common(60)], ["Creative name (the advertiser's own tag in the link)", 'Ads'])

def script(v):
    segs = (v['t'].get('transcript') or {}).get('segments') or []
    if not segs: return '<p class="muted">No speech found in this video.</p>'
    return '<ol class="script">' + ''.join(f'<li><span>{s["start"]:.0f}s</span>{esc(s["text"].strip())}</li>' for s in segs) + '</ol>'
def chips(v):
    m = v['m']; c = [f'{v["prog"]}', f'{len(v["uses"])} ads, {v["copies"]} copies']
    if m: c += [f'{m.get("duration_s")} s', f'{m.get("width")}×{m.get("height")}', f'{m.get("cuts_per_10s")} cuts per 10 s'] + \
        ([f'{m.get("words_per_min")} words/min', f'tempo {m.get("tempo_bpm")} bpm', str(m.get('music_bed_guess'))] if m.get('has_audio') else ['no sound']) + \
        [f'first cut {m.get("first_cut_s")} s']
    return '<p class="chips">' + ''.join(f'<span>{esc(str(x))}</span>' for x in c) + '</p>'
scripts = ''.join(f'<article id="s{v["a"]}"><h3>{esc(v["title"])}</h3>{chips(v)}{script(v)}<p><a href="#v{v["a"]}">Full breakdown</a></p></article>' for v in vids)
breakdowns = ''.join(f'<details id="v{v["a"]}"><summary><b>{esc(v["title"])}</b><small>{esc(v["prog"])} · {len(v["uses"])} ads · {v["m"].get("duration_s", v["t"].get("duration_s", "?"))} s</small></summary>'
    + (f'<div class="scroll"><img loading="lazy" src="img/v_{v["a"]}.jpg" alt="Frames from the video"></div>' if v['sheet'] else '')
    + f'{chips(v)}{body_of(v["bd"]) if v["bd"] else "<p class=todo>Breakdown still being written.</p>"}</details>' for v in vids)
def stext(s):
    x = s['x']
    return (body_of(s['bd']) if s['bd'] else
            f'<p><b>{esc(x.get("headline") or "")}</b></p><p>{esc(x.get("body") or "")}</p><p class="todo">Breakdown still being written.</p>')
statics = ''.join(f'<details id="i{s["i"]}"><summary><b>{esc(s["x"].get("headline") or title_of(s["bd"], "(no headline)"))}</b><small>{esc(group(s["x"]))} · started {esc((s["x"].get("start_date") or "")[:10])} · '
    f'{s["x"].get("copies") or 1} copies</small></summary><div class="static"><img loading="lazy" src="img/s_{s["i"]}.jpg" alt="The ad image"><div>{stext(s)}<p><a href="{esc(s["x"].get("link") or "")}">See it in the Ad Library</a></p></div></div></details>' for s in stat)

# ---- sections: (anchor, link text, heading, intro line, content). A section with no content is left out, link and all.
LEDE = '<p class="lede">%s</p>'
sections = [
    ('summary', 'Summary', 'Summary', '', frag('summary')),
    ('insights', 'What it means for you', 'What it means for you', '', frag('insights')),
    ('ssb', 'What it means for SSB', 'What it means for SSB', '', frag('ssb-insights')),
    ('how', 'How they run ads', f'How {esc(COMPANY)} runs its ads', '', frag('how-ads-run')),
    ('patterns', 'Creative patterns', 'Creative patterns: look, sound, pacing', '', frag('patterns')),
    ('website', 'Website', 'Website and messaging', '', frag('website')),
    ('scripts', 'All scripts', 'All video scripts, word for word',
     LEDE % 'Typed out by software from the audio, so names and odd words can be slightly off. Times are seconds from the start.', scripts),
    ('videos', 'Video breakdowns', 'Video breakdowns',
     LEDE % 'Open a row for the frames, the first three seconds, who is on screen and what they wear, framing, captions, logos, sound, structure, claims and offer.', breakdowns),
    ('statics', 'Image ads', 'Image ads', '', statics),
    ('numbers', 'The counts', 'The counts', '', numbers if n else ''),
    ('method', 'How this was made', 'How this was made', '', frag('method')),
]
sections = [s for s in sections if s[4]]
nav = ''.join(f'<a href="#{i}">{esc(l)}</a>' for i, l, *_ in sections)
body = '\n'.join(f'  <h2 id="{i}">{h}</h2>{intro}{content}' for i, _, h, intro, content in sections)

page = open(f'{HERE}/template.html').read()
# Fill the frame first and the long generated parts last, so text inside an ad can never be mistaken for a placeholder.
for k, v in [('TITLE', esc(COMPANY) + ' Ad Teardown'), ('COMPANY', esc(COMPANY)), ('N', str(n)), ('COPIES', str(copies)),
             ('NV', str(len(vids))), ('NS', str(len(stat))), ('NAV', nav), ('BODY', body)]:
    page = page.replace('{{' + k + '}}', v)
page = re.sub(r'src="(img/[^"]+)"', lambda m: 'src="data:image/jpeg;base64,' + base64.b64encode(open(OUT + '/' + m.group(1), 'rb').read()).decode() + '"', page)
open(OUT + '/index.html', 'w').write(page)
print(n, 'ads', len(vids), 'videos', len(stat), 'statics', os.path.getsize(OUT + '/index.html') // 1024, 'KB html', len(os.listdir(OUT + '/img')), 'images',
      '| sections:', ' '.join(s[0] for s in sections))
