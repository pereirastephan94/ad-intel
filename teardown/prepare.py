#!/usr/bin/env python3
"""Gets a research folder ready for the write-up step, and says what still needs writing.

Usage: prepare.py <research_dir> <video_dir>
  <research_dir>  e.g. research/<slug> (holds ads.json, videos/, images/, statics/)
  <video_dir>     the scratch folder outside the repo where slow-crawl.mjs saved <asset>.mp4

Does three things:
  1. For every video folder without metrics.json, runs connector/scripts/video-metrics.py on <video_dir>/<asset>.mp4.
  2. (Re)writes each video folder's ads.json: the records in <research_dir>/ads.json whose video_asset is that folder.
  3. Prints JSON: video folders with no breakdown.md, and image ads with no statics/<id>.md. Images are grouped by md5,
     so an exact duplicate is listed with the twin to copy from instead of being written again.
Safe to run again and again. Changes nothing else.
"""
import collections, glob, hashlib, json, os, subprocess, sys, time

if len(sys.argv) != 3:
    sys.exit(__doc__)
R, VID = sys.argv[1].rstrip('/'), sys.argv[2].rstrip('/')
METRICS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'connector', 'scripts', 'video-metrics.py')

def load_ads():
    # The crawl may be rewriting ads.json at this very moment; try a few times.
    for _ in range(5):
        try:
            return json.load(open(R + '/ads.json'))
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(2)
    sys.exit(f'Could not read {R}/ads.json')
ads = load_ads()

out = {'research_dir': R, 'ads': len(ads), 'metrics_written': [], 'metrics_failed': [], 'videos_not_ready': []}
video_dirs = sorted(d.rstrip('/') for d in glob.glob(R + '/videos/*/'))
need_breakdown = []
for d in video_dirs:
    a = os.path.basename(d)
    if not os.path.exists(d + '/transcript.json'):
        out['videos_not_ready'].append(a); continue        # download or transcript still in progress, or it failed
    if not os.path.exists(d + '/metrics.json'):
        mp4 = f'{VID}/{a}.mp4'
        if not os.path.exists(mp4):
            out['metrics_failed'].append({'asset': a, 'why': f'no file {mp4}'})
        else:
            r = subprocess.run([sys.executable, METRICS, mp4, d], capture_output=True, text=True)
            if r.returncode == 0 and os.path.exists(d + '/metrics.json'): out['metrics_written'].append(a)
            else: out['metrics_failed'].append({'asset': a, 'why': (r.stderr or r.stdout).strip().splitlines()[-1:] or ['unknown']})
    uses = [x for x in ads.values() if x.get('video_asset') == a]
    json.dump(uses, open(d + '/ads.json', 'w'), indent=1)
    if not os.path.exists(d + '/breakdown.md'):
        need_breakdown.append({'asset': a, 'ads': len(uses), 'has_metrics': os.path.exists(d + '/metrics.json')})

# ---- images: only those that belong to a collected ad
os.makedirs(R + '/statics', exist_ok=True)
md5 = {}
for p in sorted(glob.glob(R + '/images/*.jpg')):
    i = os.path.basename(p)[:-4]
    if i in ads: md5[i] = hashlib.md5(open(p, 'rb').read()).hexdigest()
by_hash = collections.defaultdict(list)
for i, h in md5.items(): by_hash[h].append(i)
written = lambda i: os.path.exists(f'{R}/statics/{i}.md')
to_write, to_copy = [], []
for h, ids in by_hash.items():
    done = [i for i in ids if written(i)]
    todo = [i for i in ids if not written(i)]
    if not todo: continue
    if done:
        to_copy += [{'id': i, 'copy_from': done[0], 'twin_is_written': True} for i in todo]
    else:
        to_write.append({'id': todo[0], 'exact_duplicates': todo[1:]})
        to_copy += [{'id': i, 'copy_from': todo[0], 'twin_is_written': False} for i in todo[1:]]

out.update({
    'video_folders': len(video_dirs),
    'videos_needing_breakdown': need_breakdown,
    'image_ads': len(md5),
    'images_needing_writeup': to_write,
    'images_that_are_exact_duplicates': to_copy,
    'how_to_use': 'Write breakdown.md for each video in videos_needing_breakdown and statics/<id>.md for each id in images_needing_writeup. '
                  'For each entry in images_that_are_exact_duplicates, copy statics/<copy_from>.md to statics/<id>.md (after it is written) and correct '
                  'the Facts and Ad text from that id\'s own record in ads.json.',
})
print(json.dumps(out, indent=1))
