#!/usr/bin/env python3
"""Redo the transcript of every non-English video in Roman script (Hinglish as people type it).
The first-pass transcript (Whisper "base") writes Hindi speech in Urdu or Devanagari script and garbles it.
This pass uses the "medium" model with the language fixed to Hindi and a Roman-script prompt, which gives readable Hinglish.
Usage: retranscribe.py <research_dir> <video_dir> ["Brand name and product words for the prompt"]
Keeps the first pass under transcript_raw. Skips videos already redone. About 1.5x the video length on 4 CPU cores."""
import json, os, re, subprocess, sys, tempfile, glob
import whisper
R, V = sys.argv[1], sys.argv[2]
hint = sys.argv[3] if len(sys.argv) > 3 else ''
PROMPT = f"Yeh ek Hinglish ad hai, Roman script mein likha hua. {hint} App download karo, aaj hi invest karo, best offer, kya aap jaante ho?"
model = None
for d in sorted(glob.glob(R + '/videos/*/')):
    a = os.path.basename(d.rstrip('/')); tp = d + 'transcript.json'; mp4 = f'{V}/{a}.mp4'
    if not os.path.exists(tp) or not os.path.exists(mp4): continue
    t = json.load(open(tp)); tr = t.get('transcript') or {}
    if t.get('transcript_raw') is not None: continue
    text = tr.get('text', '')
    nonlatin = len(re.findall(r'[^\x00-ɏ -⁯₹]', text))
    if tr.get('language') == 'en' and nonlatin < 5: continue
    if len(text) < 15: continue
    model = model or whisper.load_model('medium')
    wav = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-ac', '1', '-ar', '16000', wav], check=True)
    r = model.transcribe(wav, fp16=False, language='hi', initial_prompt=PROMPT, condition_on_previous_text=False)
    os.remove(wav)
    t['transcript_raw'] = tr
    t['transcript'] = {'language': 'hinglish (roman, second pass)', 'text': r['text'].strip(),
                       'segments': [{'start': round(s['start'], 1), 'end': round(s['end'], 1), 'text': s['text'].strip()} for s in r['segments']]}
    json.dump(t, open(tp, 'w'), ensure_ascii=False, indent=1)
    print(a, 'redone:', r['text'][:80], flush=True)
print('RETRANSCRIBE DONE')
