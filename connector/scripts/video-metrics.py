# Pacing and music measurements for one ad video. Usage: video-metrics.py <mp4> <asset_dir_with_transcript.json>
# Writes metrics.json: cuts, cut rate, aspect, speech share, tempo, and a music-bed estimate
# (how loud and how tonal the audio is in the gaps where nobody is speaking).
import sys, json, subprocess, re, os
import numpy as np, librosa
mp4, d = sys.argv[1], sys.argv[2]
out = os.path.join(d, 'metrics.json')
pr = json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate:format=duration','-of','json',mp4],capture_output=True,text=True).stdout)
v = next((s for s in pr['streams'] if s['codec_type']=='video'), {})
dur = float(pr['format']['duration'])
err = subprocess.run(['ffmpeg','-hide_banner','-i',mp4,'-an','-vf',"select='gt(scene,0.3)',showinfo",'-f','null','-'],capture_output=True,text=True).stderr
cuts = [round(float(x),2) for x in re.findall(r'pts_time:([0-9.]+)', err)]
m = {'duration_s': round(dur,1), 'width': v.get('width'), 'height': v.get('height'),
     'cuts': len(cuts), 'cuts_per_10s': round(len(cuts)/dur*10,2), 'first_cut_s': cuts[0] if cuts else None,
     'cuts_in_first_5s': sum(1 for c in cuts if c < 5), 'cut_times': cuts}
has_audio = any(s['codec_type']=='audio' for s in pr['streams'])
m['has_audio'] = has_audio
if has_audio:
    wav = out + '.tmp.wav'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',mp4,'-vn','-ac','1','-ar','22050','-y',wav],check=True)
    y, sr = librosa.load(wav, sr=22050, mono=True); os.remove(wav)
    hop = 512
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
    segs = (json.load(open(os.path.join(d,'transcript.json'))).get('transcript') or {}).get('segments') or []
    speech = np.zeros(len(rms), bool)
    for s in segs: speech |= (t >= s['start']) & (t <= s['end'])
    db = lambda x: round(float(20*np.log10(np.mean(x)+1e-9)),1) if len(x) else None
    H, P = librosa.effects.hpss(y)
    hr = librosa.feature.rms(y=H, hop_length=hop)[0]; prr = librosa.feature.rms(y=P, hop_length=hop)[0]
    gap = ~speech
    tempo, beats = librosa.beat.beat_track(y=P, sr=sr, hop_length=hop)
    flat = librosa.feature.spectral_flatness(y=y, hop_length=hop)[0]
    m.update({'speech_share': round(float(speech.mean()),2), 'words': sum(len(s['text'].split()) for s in segs),
      'words_per_min': round(sum(len(s['text'].split()) for s in segs)/dur*60) if dur else None,
      'first_speech_s': segs[0]['start'] if segs else None,
      'level_speech_db': db(rms[speech]), 'level_gaps_db': db(rms[gap]), 'gap_seconds': round(float(gap.sum()*hop/sr),1),
      'gap_tonal_share': round(float(hr[gap].sum()/(hr[gap].sum()+prr[gap].sum()+1e-9)),2) if gap.any() else None,
      'gap_flatness': round(float(flat[gap].mean()),3) if gap.any() else None,
      'tempo_bpm': round(float(np.atleast_1d(tempo)[0])), 'beat_strength': round(float(librosa.onset.onset_strength(y=P, sr=sr).mean()),2),
      'level_first_1s_db': db(rms[t<1]), 'level_last_2s_db': db(rms[t>dur-2])})
    g, s_ = m['level_gaps_db'], m['level_speech_db']
    m['music_bed_guess'] = ('no gaps to judge' if m['gap_seconds'] < 1 else 'likely music or sound bed under the voice' if g is not None and s_ is not None and g > s_ - 18 and g > -45 else 'gaps are near silent: little or no music')
json.dump(m, open(out,'w'), indent=1)
print(os.path.basename(d), m['duration_s'], 'cuts', m['cuts'], m.get('tempo_bpm'), m.get('music_bed_guess'))
