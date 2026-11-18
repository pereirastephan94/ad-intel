"""Transcribe one audio file with local Whisper and print JSON.

Usage: python3 transcribe.py <audio.wav> [model]
Model files come from openaipublic.azureedge.net (whisper's default), cached in ~/.cache/whisper
or $WHISPER_CACHE.
"""
import json
import os
import sys

import whisper

audio = sys.argv[1]
model_name = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("WHISPER_MODEL", "base")
model = whisper.load_model(model_name, download_root=os.environ.get("WHISPER_CACHE") or None)
result = model.transcribe(audio, fp16=False, verbose=None)
print(json.dumps({
    "language": result.get("language"),
    "text": result.get("text", "").strip(),
    "segments": [
        {"start": round(s["start"], 1), "end": round(s["end"], 1), "text": s["text"].strip()}
        for s in result.get("segments", [])
    ],
}))
