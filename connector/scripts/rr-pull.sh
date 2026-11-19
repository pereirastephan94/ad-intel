#!/bin/bash
# Round-robin puller: keeps pulling for a list of brands, ONE page view per brand per turn, 5 to 7 minutes between views,
# so every brand rests about an hour between its own views. Stops by itself after RR_MINUTES (default 105) so it fits
# inside a 2 hour background job; run it again to carry on (all state is in research/<slug>/crawl-state.json).
# Usage: rr-pull.sh <video_scratch_dir> "Brand A" "Brand B|alt spelling" ...
cd "$(dirname "$0")/.."
VID="$1"; shift
END=$(( $(date +%s) + ${RR_MINUTES:-105} * 60 ))
nap() { sleep $(( 300 + RANDOM % 120 )); }
while [ $(date +%s) -lt $END ]; do
  for SPEC in "$@"; do
    [ $(date +%s) -lt $END ] || break
    NAME="${SPEC%%|*}"
    SLUG=$(echo "$NAME" | tr 'A-Z' 'a-z' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//')
    OUT=../research/$SLUG; mkdir -p "$OUT"
    if ! { [ -s "$OUT/page.json" ] && grep -q '"page_id"' "$OUT/page.json"; }; then
      # one search per turn; rotate through the alternate spellings
      IFS='|' read -ra ALTS <<< "$SPEC"; N=$(cat "$OUT/.find_tries" 2>/dev/null || echo 0)
      TRY="${ALTS[$(( N % ${#ALTS[@]} ))]}"; echo $(( N + 1 )) > "$OUT/.find_tries"
      node scripts/find-page.mjs "$TRY" IN --exact > "$OUT/page.json" 2>>"$OUT/run.log"
      echo "$(date -u +%FT%TZ) $NAME: searched \"$TRY\" -> $(grep -c '"page_id"' "$OUT/page.json") candidate(s)"
      nap; continue
    fi
    PID=$(python3 -c "
import json
try:
    c=[x for x in json.load(open('$OUT/page.json'))['candidates'] if x['name_match']!='no']
    print(c[0]['page_id'] if c else '')
except Exception: print('')")
    if [ -z "$PID" ]; then echo "$(date -u +%FT%TZ) $NAME: no matching page in search result"; mv "$OUT/page.json" "$OUT/page.failed.$(date +%s).json"; continue; fi
    # make sure there is something in the queue: first the three plain views, later keyword views
    python3 - "$OUT/crawl-state.json" <<'PY'
import json, os, sys
f = sys.argv[1]
st = json.load(open(f)) if os.path.exists(f) else {"done": [], "total": None, "log": [], "keywordsQueued": True, "queue": [{"media": "all"}, {"media": "video"}, {"media": "image"}], "stage": 1}
if not st.get("queue"):
    stage = st.get("stage", 1)
    if stage == 1:
        st["queue"] = [{"media": "video", "retry": 7}, {"media": "image", "retry": 7}, {"media": "meme", "retry": 7}, {"media": "all", "sort": "relevancy_monthly_grouped", "dir": "desc", "retry": 7}]
    elif stage == 2:
        st["queue"] = [{"q": w} for w in ["you", "your", "the", "and", "for", "with", "now", "get", "new", "free", "best", "offer", "app", "today", "aap", "hai", "ke", "se", "ka", "to", "in", "a", "is", "of"]]
    else:
        st["queue"] = []
    st["stage"] = stage + 1
json.dump(st, open(f, "w"), indent=1)
PY
    if [ "$(python3 -c "import json;print(len(json.load(open('$OUT/crawl-state.json'))['queue']))")" = "0" ]; then continue; fi
    MAX_VIEWS=1 node scripts/slow-crawl.mjs "$PID" "$OUT" "$VID/$SLUG" 1 1 2>&1 | grep --line-buffered -E "view \{|rror" | sed "s/^/$NAME: /" | cut -c1-220
    nap
  done
done
echo "$(date -u +%FT%TZ) RR END"
