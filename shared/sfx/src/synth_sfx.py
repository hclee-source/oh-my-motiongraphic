"""Synthesize small SFX that the Pixabay set lacks (CC0, made here): tick, tock (clock), bat-crack (wooden bat hit).
   .venv/bin/python -I shared/sfx/src/synth_sfx.py   → shared/sfx/{tick,tock,bat-crack}.mp3"""
import subprocess, numpy as np, soundfile as sf
from pathlib import Path
from scipy.signal import butter, sosfilt

SR = 44100
OUT = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(7)

def env(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))

def bp(x, lo, hi):
    return sosfilt(butter(4, [lo, hi], btype="band", fs=SR, output="sos"), x)

def save(name, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.89
    wav = OUT / "src" / f"{name}.wav"
    sf.write(wav, np.stack([x, x], 1), SR)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "192k", str(OUT / f"{name}.mp3")], check=True)
    wav.unlink()

def clock(f0, noise_band):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    click = bp(rng.standard_normal(n), *noise_band) * env(n, 0.004)
    ping = (np.sin(2 * np.pi * f0 * t) + 0.4 * np.sin(2 * np.pi * f0 * 2.7 * t)) * env(n, 0.018)
    return click * 1.0 + ping * 0.55

save("tick", clock(2300, (3500, 9000)))
save("tock", clock(1500, (2000, 6000)))

# wooden bat crack: sharp broadband transient + wood body modes + a short low thump
n = int(0.45 * SR)
t = np.arange(n) / SR
crack = bp(rng.standard_normal(n), 1200, 9000) * env(n, 0.012)
modes = sum(a * np.sin(2 * np.pi * f * t + p) * env(n, d) for f, a, d, p in
            [(480, 0.9, 0.05, 0.0), (1230, 0.7, 0.035, 1.0), (2410, 0.5, 0.025, 2.0), (3650, 0.3, 0.018, 0.5)])
thump = np.sin(2 * np.pi * 95 * t) * env(n, 0.06) * 0.8
tail = bp(rng.standard_normal(n), 300, 2500) * env(n, 0.09) * 0.12
save("bat-crack", crack * 1.3 + modes * 0.8 + thump + tail)
print("ok", [p.name for p in OUT.glob("*.mp3") if p.stem in ("tick", "tock", "bat-crack")])
