#!/bin/bash
# Light sample pull for several companies, one after another, slowly.
# Usage: sample-run.sh <video_scratch_dir> "Company A" "Company B" ...
# Per company: 1 search view + 3 ad views (all, video only, image only, in the Library's default order), 4 to 7 minutes apart.
# Do NOT add sort_data to these views: views sorted by total_impressions came back empty most of the time.
cd "$(dirname "$0")/.."
VID="$1"; shift
nap() { sleep $(( ${NAPMIN:-660} + RANDOM % 180 )); }
for SPEC in "$@"; do
  NAME="${SPEC%%|*}"
  SLUG=$(echo "$NAME" | tr 'A-Z' 'a-z' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//')
  OUT=../research/$SLUG; mkdir -p "$OUT"
  # Names can carry alternates: "Cult.fit|cultfit|Cult". Try each until a page matches.
  IFS='|' read -ra ALTS <<< "$SPEC"
  for TRY in "${ALTS[@]}" "${ALTS[@]}"; do
    [ -s "$OUT/page.json" ] && grep -q '"page_id"' "$OUT/page.json" && break
    node scripts/find-page.mjs "$TRY" IN --exact > "$OUT/page.json" 2>>"$OUT/run.log"
    nap
  done
  PID=$(python3 -c "
import json,sys
try:
    c=[x for x in json.load(open('$OUT/page.json'))['candidates'] if x['name_match']!='no']
    print(c[0]['page_id'] if c else '')
except Exception: print('')")
  if [ -z "$PID" ]; then echo "$(date -u +%FT%TZ) $NAME: NO PAGE FOUND"; mv "$OUT/page.json" "$OUT/page.failed.json"; continue; fi
  [ -f "$OUT/crawl-state.json" ] || echo '{"done":[],"total":null,"log":[],"keywordsQueued":true,"queue":[{"media":"all"},{"media":"video"},{"media":"image"}]}' > "$OUT/crawl-state.json"
  echo "$(date -u +%FT%TZ) $NAME: page $PID"
  MAX_VIEWS=${MAXV:-4} node scripts/slow-crawl.mjs "$PID" "$OUT" "$VID/$SLUG" 11 15 2>&1 | grep --line-buffered -E "view \{|PAUSED|DONE|rror" | cut -c1-200
  nap
done
echo "$(date -u +%FT%TZ) BATCH END"
