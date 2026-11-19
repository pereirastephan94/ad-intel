#!/usr/bin/env python3
"""Builds the Mesa ad teardown page from the research files.
Usage: build.py <out_dir>   (writes index.html, img/v_<asset>.jpg contact sheets, img/s_<id>.jpg statics)"""
import json, os, sys, glob, html, collections, re, urllib.parse as U
import markdown
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1]; os.makedirs(OUT + '/img', exist_ok=True)
ads = json.load(open(R + '/ads.json'))
md = lambda s: markdown.markdown(s, extensions=['tables'])
esc = html.escape
def frag(name):
    p = f'{R}/doc/{name}.md'
    return md(open(p).read()) if os.path.exists(p) else '<p class="todo">Section still being written.</p>'
def utm(x, k):
    return (U.parse_qs(U.urlparse(x.get('landing_url') or '').query).get(k) or [''])[0]
def prog(x):
    u = (x.get('landing_url') or '').lower()
    return 'Ascend (part-time)' if 'ascend' in u else 'Undergraduate' if ('undergrad' in u or '/ug' in u) else 'PGP (full-time)'

# ---- videos
vids = []
for d in sorted(glob.glob(R + '/videos/*/')):
    a = os.path.basename(d.rstrip('/'))
    t = json.load(open(d + 'transcript.json'))
    m = json.load(open(d + 'metrics.json')) if os.path.exists(d + 'metrics.json') else {}
    uses = [x for x in ads.values() if x.get('video_asset') == a]
    bd = open(d + 'breakdown.md').read() if os.path.exists(d + 'breakdown.md') else ''
    title = (re.match(r'#\s*(.+)', bd).group(1) if bd.startswith('#') else a)
    title = re.sub(r'\s*\(\d{10,}\)\s*$', '', title)
    stills = sorted(glob.glob(d + 'still*.jpg'))
    pick = stills[:5:2] + [stills[i] for i in (len(stills)*5//10, len(stills)*7//10, len(stills)-1)] if len(stills) >= 8 else stills
    ims = [Image.open(p).convert('RGB') for p in pick]
    h = 260; ims = [i.resize((max(1, i.width * h // i.height), h)) for i in ims]
    sheet = Image.new('RGB', (sum(i.width for i in ims) + 4 * (len(ims) - 1), h), (255, 255, 255)); x = 0
    for i in ims: sheet.paste(i, (x, 0)); x += i.width + 4
    sheet.save(f'{OUT}/img/v_{a}.jpg', quality=72)
    vids.append(dict(a=a, t=t, m=m, uses=uses, bd=bd, title=title, prog=prog(uses[0]) if uses else '?',
                     copies=sum(int(u.get('copies') or 1) for u in uses)))
vids.sort(key=lambda v: (v['prog'], -len(v['uses']), -v['copies']))

# ---- statics
stat = []
for p in sorted(glob.glob(R + '/images/*.jpg')):
    i = os.path.basename(p)[:-4]
    if i not in ads: continue
    im = Image.open(p).convert('RGB'); im.thumbnail((420, 420)); im.save(f'{OUT}/img/s_{i}.jpg', quality=72)
    f = f'{R}/statics/{i}.md'
    stat.append(dict(i=i, x=ads[i], bd=open(f).read() if os.path.exists(f) else ''))
stat.sort(key=lambda s: (prog(s['x']), s['x'].get('headline') or ''))

C = collections.Counter
def table(rows, head):
    return '<div class="scroll"><table><thead><tr>' + ''.join(f'<th>{esc(h)}</th>' for h in head) + '</tr></thead><tbody>' + \
        ''.join('<tr>' + ''.join(f'<td>{esc(str(c))}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'
n = len(ads); copies = sum(int(x.get('copies') or 1) for x in ads.values())
fm = C((x.get('extra') or {}).get('display_format') or x.get('media_type') for x in ads.values())
numbers = table([[k, v] for k, v in C(prog(x) for x in ads.values()).most_common()], ['Programme', 'Ads']) + \
    table([[k, v] for k, v in fm.most_common()], ['Format (DCO = Facebook mixes several images, videos and texts)', 'Ads']) + \
    table([[k, v] for k, v in sorted(C((x.get('start_date') or '')[:10] for x in ads.values()).items())], ['Start date', 'Ads started']) + \
    table([[k or '(no headline)', v] for k, v in C(x.get('headline') for x in ads.values()).most_common(30)], ['Headline under the ad', 'Ads']) + \
    table([[U.urlparse(k).path or '/', v] for k, v in C((x.get('landing_url') or '').split('?')[0].rstrip('/') for x in ads.values()).most_common()], ['Landing page on mesaschool.co', 'Ads']) + \
    table([[k.strip() or '(not tagged)', v] for k, v in C(utm(x, 'utm_campaign') for x in ads.values()).most_common()], ["Campaign name (Mesa's own tag)", 'Ads']) + \
    table([[k.strip() or '(not tagged)', v] for k, v in C(utm(x, 'utm_content') for x in ads.values()).most_common()], ["Creative name (Mesa's own tag)", 'Ads'])

def script(v):
    segs = (v['t'].get('transcript') or {}).get('segments') or []
    if not segs: return '<p class="muted">No speech found in this video.</p>'
    return '<ol class="script">' + ''.join(f'<li><span>{s["start"]:.0f}s</span>{esc(s["text"].strip())}</li>' for s in segs) + '</ol>'
def chips(v):
    m = v['m']; c = [f'{v["prog"]}', f'{len(v["uses"])} ads, {v["copies"]} copies']
    if m: c += [f'{m.get("duration_s")} s', f'{m.get("width")}×{m.get("height")}', f'{m.get("cuts_per_10s")} cuts per 10 s',
                f'{m.get("words_per_min")} words/min', f'first cut {m.get("first_cut_s")} s', f'tempo {m.get("tempo_bpm")} bpm', str(m.get('music_bed_guess'))]
    return '<p class="chips">' + ''.join(f'<span>{esc(str(x))}</span>' for x in c) + '</p>'
scripts = ''.join(f'<article id="s{v["a"]}"><h3>{esc(v["title"])}</h3>{chips(v)}{script(v)}<p><a href="#v{v["a"]}">Full breakdown</a></p></article>' for v in vids)
breakdowns = ''.join(f'<details id="v{v["a"]}"><summary><b>{esc(v["title"])}</b><small>{esc(v["prog"])} · {len(v["uses"])} ads · {v["m"].get("duration_s","?")} s</small></summary>'
    f'<div class="scroll"><img loading="lazy" src="img/v_{v["a"]}.jpg" alt="Frames from the video"></div>{chips(v)}{md(re.sub(r"^#.*\n", "", v["bd"], 1)) if v["bd"] else "<p class=todo>Breakdown still being written.</p>"}</details>' for v in vids)
def stext(s):
    x = s['x']
    return (md(re.sub(r'^#.*\n', '', s['bd'], 1)) if s['bd'] else
            f'<p><b>{esc(x.get("headline") or "")}</b></p><p>{esc(x.get("body") or "")}</p>')
statics = ''.join(f'<details id="i{s["i"]}"><summary><b>{esc(s["x"].get("headline") or "(no headline)")}</b><small>{esc(prog(s["x"]))} · started {esc((s["x"].get("start_date") or "")[:10])} · '
    f'{s["x"].get("copies") or 1} copies</small></summary><div class="static"><img loading="lazy" src="img/s_{s["i"]}.jpg" alt="The ad image"><div>{stext(s)}<p><a href="{esc(s["x"]["link"])}">See it in the Ad Library</a></p></div></div></details>' for s in stat)

page = open(f'{R}/doc/template.html').read()
for k, v in dict(SUMMARY=frag('summary'), HOW=frag('how-ads-run'), NUMBERS=numbers, WEBSITE=frag('website'), SCRIPTS=scripts, BREAKDOWNS=breakdowns,
                 STATICS=statics, PATTERNS=frag('patterns'), SSB=frag('ssb-insights'), METHOD=frag('method'),
                 N=str(n), COPIES=str(copies), NV=str(len(vids)), NS=str(len(stat))).items():
    page = page.replace('{{' + k + '}}', v)
import base64
page = re.sub(r'src="(img/[^"]+)"', lambda m: 'src="data:image/jpeg;base64,' + base64.b64encode(open(OUT + '/' + m.group(1), 'rb').read()).decode() + '"', page)
open(OUT + '/index.html', 'w').write(page)
print(n, 'ads', len(vids), 'videos', len(stat), 'statics', os.path.getsize(OUT + '/index.html') // 1024, 'KB html', len(os.listdir(OUT + '/img')), 'images')
