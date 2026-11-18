# Ad Audit connector: Node 22 + Playwright Chromium + ffmpeg + local Whisper (CPU).
# The Playwright image already has Node 22 and a Chromium matching playwright 1.59.1.
FROM mcr.microsoft.com/playwright:v1.59.1-noble

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg python3-venv python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Whisper with CPU-only PyTorch (much smaller than the default GPU build).
RUN python3 -m venv /opt/whisper \
 && /opt/whisper/bin/pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && /opt/whisper/bin/pip install --no-cache-dir openai-whisper
ENV PYTHON=/opt/whisper/bin/python \
    WHISPER_MODEL=base \
    WHISPER_CACHE=/opt/whisper-models
# Download the model at build time (from openaipublic.azureedge.net) so each start is fast.
RUN /opt/whisper/bin/python -c "import whisper; whisper.load_model('base', download_root='/opt/whisper-models')"

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json transcribe.py ./
COPY src ./src
RUN npx tsc -p . && npm prune --omit=dev

ENV NODE_ENV=production PORT=8080
EXPOSE 8080
CMD ["node", "dist/server.js"]
