# REPET-SIM vocal separation (librosa docs recipe) -> vocal energy envelope -> vocal-on segments
import librosa, numpy as np, json
y, sr = librosa.load('assets/bgm.mp3', sr=22050, mono=True)
S_full, phase = librosa.magphase(librosa.stft(y, n_fft=2048, hop_length=512))
S_filter = librosa.decompose.nn_filter(S_full, aggregate=np.median, metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr, hop_length=512)))
S_filter = np.minimum(S_full, S_filter)
margin_v, power = 10, 2
mask_v = librosa.util.softmask(S_full - S_filter, margin_v * S_filter, power=power)
S_fg = mask_v * S_full
freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
band = (freqs > 250) & (freqs < 4000)
e = S_fg[band].sum(axis=0)
e = np.convolve(e, np.ones(9)/9, mode='same')
t = librosa.frames_to_time(np.arange(len(e)), sr=sr, hop_length=512)
thr = np.percentile(e, 55)
on = e > thr
segs=[]; start=None
for i,v in enumerate(on):
    if v and start is None: start=t[i]
    if not v and start is not None:
        if t[i]-start>0.25: segs.append([round(float(start),2), round(float(t[i]),2)])
        start=None
# merge gaps < 0.35s
m=[]
for s in segs:
    if m and s[0]-m[-1][1] < 0.35: m[-1][1]=s[1]
    else: m.append(s)
json.dump({'segments':m,'env_t':[round(float(x),3) for x in t[::4]],'env':[round(float(x/e.max()),4) for x in e[::4]]}, open('.work/vocal_activity.json','w'))
for s in m: print(f"{s[0]:7.2f} - {s[1]:7.2f}  ({s[1]-s[0]:.2f}s)")
