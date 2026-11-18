#!/bin/bash
# Run the Ad Audit connector on your Mac and give claude.ai a temporary public link to it.
# Usage (in Terminal, inside the connector folder):   bash start-mac.sh
# Stop it with Ctrl+C. Nothing runs after you close it. Free, no accounts needed.
set -e
cd "$(dirname "$0")"

say() { printf "\n\033[1m%s\033[0m\n" "$1"; }

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is needed first. Install it from https://brew.sh (copy the one line on that page into Terminal), then run this again."
  exit 1
fi

say "1/5 Checking tools (Node, ffmpeg, Python, Cloudflare tunnel)..."
for pkg in node ffmpeg python@3.12 cloudflared; do
  brew list "$pkg" >/dev/null 2>&1 || brew install "$pkg"
done
PY="$(brew --prefix python@3.12)/bin/python3.12"

say "2/5 Setting up speech-to-text (first time only, a few minutes)..."
if [ ! -x .venv-whisper/bin/python ]; then
  "$PY" -m venv .venv-whisper
  .venv-whisper/bin/pip install --quiet --upgrade pip
  .venv-whisper/bin/pip install --quiet openai-whisper
fi

say "3/5 Setting up the server and browser (first time only)..."
[ -d node_modules ] || npm ci --silent
npx playwright install chromium >/dev/null
npm run build --silent

[ -f .token ] || openssl rand -hex 24 > .token
TOKEN="$(cat .token)"

say "4/5 Starting the server..."
PORT=8080 ACCESS_TOKEN="$TOKEN" PYTHON="$PWD/.venv-whisper/bin/python" WHISPER_MODEL=base \
  node dist/server.js > server.log 2>&1 &
SERVER=$!
trap 'kill $SERVER $TUNNEL 2>/dev/null; echo; echo "Stopped."; exit 0' INT TERM EXIT
sleep 3
curl -sf http://localhost:8080/health >/dev/null || { echo "Server did not start. See server.log"; exit 1; }

say "5/5 Opening a temporary public link..."
cloudflared tunnel --no-autoupdate --url http://localhost:8080 > tunnel.log 2>&1 &
TUNNEL=$!
URL=""
for _ in $(seq 1 30); do
  URL="$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' tunnel.log | head -1 || true)"
  [ -n "$URL" ] && break
  sleep 1
done
[ -n "$URL" ] || { echo "Could not open the link. See tunnel.log"; exit 1; }

cat <<EOF

==================================================================
 READY. Keep this window open while you test.

 Connector link (paste into claude.ai):

   $URL/mcp/$TOKEN

 1. claude.ai -> Settings -> Connectors -> Add custom connector
 2. Name: Ad Audit (test)   URL: the link above   -> Add
 3. New chat -> tools menu -> switch on "Ad Audit (test)"
 4. Type:  Audit Mesa's ads

 The link changes every time you run this script, so update the
 connector's URL (or remove and re-add it) each time.

 Using Claude Code on this Mac instead? Run this once:
   claude mcp add --transport http ad-audit http://localhost:8080/mcp/$TOKEN

 Press Ctrl+C to stop.
==================================================================
EOF
wait $SERVER
