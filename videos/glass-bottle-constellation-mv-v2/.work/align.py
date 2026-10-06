# Forced alignment of the known lyrics onto the Demucs vocal stem with torchaudio MMS_FA.
# Korean is romanized (Revised Romanization, syllable by syllable) because MMS_FA's dictionary is Latin.
# Output: .work/lyrics_aligned.json  — per line: start/end + per-word start/end (track seconds).
import json, torch, torchaudio
import numpy as np, soundfile as sf
from torchaudio.pipelines import MMS_FA as bundle

LYRICS = [l.strip() for l in open('.work/lyrics.txt', encoding='utf-8') if l.strip() and not l.startswith('[')]

CHO = ['g','kk','n','d','tt','r','m','b','pp','s','ss','','j','jj','ch','k','t','p','h']
JUNG = ['a','ae','ya','yae','eo','e','yeo','ye','o','wa','wae','oe','yo','u','wo','we','wi','yu','eu','ui','i']
JONG = ['','k','k','k','n','n','n','t','l','k','m','l','l','l','p','l','m','p','p','t','t','ng','t','t','k','t','p','t']
def roman_syl(ch):
    c = ord(ch) - 0xAC00
    if 0 <= c < 11172:
        return CHO[c // 588] + JUNG[(c % 588) // 28] + JONG[c % 28]
    return ''
def roman_word(w):
    return ''.join(roman_syl(ch) for ch in w)

device = torch.device('cpu')
model = bundle.get_model(with_star=False).to(device)
tokenizer = bundle.get_tokenizer()
aligner = bundle.get_aligner()
SR = bundle.sample_rate

wav, sr = sf.read('.work/demucs/htdemucs/bgm/vocals.wav', dtype='float32')
if wav.ndim > 1: wav = wav.mean(axis=1)
wav = torch.from_numpy(wav)[None]
wav = torchaudio.functional.resample(wav, sr, SR)
N = wav.shape[1]

# chunked emissions (20 ms frames) with padding context
CH, PAD = 15 * SR, 2 * SR
ems = []
with torch.inference_mode():
    pos = 0
    while pos < N:
        a = max(0, pos - PAD); b = min(N, pos + CH + PAD)
        em, _ = model(wav[:, a:b].to(device))
        fr = em.shape[1] / (b - a)  # frames per sample
        keep_a = int(round((pos - a) * fr)); keep_b = int(round((min(N, pos + CH) - a) * fr))
        ems.append(em[:, keep_a:keep_b])
        pos += CH
emission = torch.cat(ems, dim=1)
frames = emission.shape[1]
sec_per_frame = (N / SR) / frames
print('frames', frames, 'sec/frame', round(sec_per_frame, 5))

words, owners = [], []
for li, line in enumerate(LYRICS):
    for w in line.split():
        r = roman_word(w)
        if r:
            words.append(r); owners.append((li, w))
tokens = tokenizer(words)
spans = aligner(emission[0], tokens)

out = []
for li, line in enumerate(LYRICS):
    out.append({'line': line, 'words': []})
for (li, w), sp in zip(owners, spans):
    s = sp[0].start * sec_per_frame; e = sp[-1].end * sec_per_frame
    score = float(np.mean([x.score for x in sp]))
    out[li]['words'].append({'w': w, 'start': round(s, 3), 'end': round(e, 3), 'score': round(score, 3)})
for L in out:
    L['start'] = L['words'][0]['start']; L['end'] = L['words'][-1]['end']
json.dump(out, open('.work/lyrics_aligned.json', 'w'), ensure_ascii=False, indent=1)
for L in out:
    ws = ' '.join(f"{x['w']}@{x['start']:.2f}" for x in L['words'])
    print(f"{L['start']:7.2f}-{L['end']:7.2f}  {ws}")
