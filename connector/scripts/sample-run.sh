#!/bin/bash
# Light sample pull for several companies, one after another, slowly.
# Usage: sample-run.sh <video_scratch_dir> "Company A" "Company B" ...
# Per company: 1 search view + 3 ad views (top ads, top videos, top images), 4 to 7 minutes apart.
cd "$(dirname "$0")/.."
VID="$1"; shift
nap() { sleep $(( 240 + RANDOM % 180 )); }
for NAME in "$@"; do
  SLUG=$(echo "$NAME" | tr 'A-Z' 'a-z' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//')
  OUT=../research/$SLUG; mkdir -p "$OUT"
  if [ ! -f "$OUT/page.json" ]; then
    node scripts/find-page.mjs "$NAME" IN --exact > "$OUT/page.json" 2>>"$OUT/run.log"
    nap
  fi
  PID=$(python3 -c "
import json,sys
try:
    c=[x for x in json.load(open('$OUT/page.json'))['candidates'] if x['name_match']!='no']
    print(c[0]['page_id'] if c else '')
except Exception: print('')")
  if [ -z "$PID" ]; then echo "$(date -u +%FT%TZ) $NAME: NO PAGE FOUND"; mv "$OUT/page.json" "$OUT/page.failed.json"; continue; fi
  [ -f "$OUT/crawl-state.json" ] || echo '{"done":[],"total":null,"log":[],"keywordsQueued":true,"queue":[{"media":"all","sort":"total_impressions","dir":"desc"},{"media":"video","sort":"total_impressions","dir":"desc"},{"media":"image","sort":"total_impressions","dir":"desc"}]}' > "$OUT/crawl-state.json"
  echo "$(date -u +%FT%TZ) $NAME: page $PID"
  MAX_VIEWS=3 node scripts/slow-crawl.mjs "$PID" "$OUT" "$VID/$SLUG" 4 7 2>&1 | grep -E "view \{|PAUSED|DONE|rror" | cut -c1-200
  nap
done
echo "$(date -u +%FT%TZ) BATCH END"
