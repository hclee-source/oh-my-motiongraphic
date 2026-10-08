#!/usr/bin/env python3
"""Measure where each SFX actually *hits* (its loudest moment), so sfx.py can line that up with the cue
instead of the file's first sample. Many library files start with a short swell (whoosh, sparkle, chime),
so placing the file start on the beat makes the audible hit land late.

  python3 sfx_peaks.py            # (re)measure every shared/sfx/*.mp3 → shared/sfx/peaks.json
  python3 sfx_peaks.py --show     # print the table

peak_sec = time of the max |amplitude| of a 10 ms RMS envelope (mono, 8 kHz) — no numpy needed.
"""
import array, json, math, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import SHARED  # noqa: E402

SR, WIN = 8000, 80          # 8 kHz mono, 10 ms windows
OUT = SHARED / "sfx" / "peaks.json"


def peak_sec(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    best, best_i = -1.0, 0
    for i in range(0, max(1, len(a) - WIN), WIN):
        seg = a[i:i + WIN]
        e = math.sqrt(sum(x * x for x in seg) / max(1, len(seg)))
        if e > best:
            best, best_i = e, i
    return round(best_i / SR, 3)


def load():
    """{name: peak_sec}; measures and caches any file that is missing from peaks.json."""
    peaks = json.loads(OUT.read_text()) if OUT.exists() else {}
    changed = False
    for f in sorted((SHARED / "sfx").glob("*.mp3")):
        if f.stem not in peaks:
            peaks[f.stem] = peak_sec(f)
            changed = True
    if changed:
        OUT.write_text(json.dumps(peaks, indent=2, sort_keys=True))
    return peaks


if __name__ == "__main__":
    if "--show" not in sys.argv and OUT.exists():
        OUT.unlink()
    for k, v in load().items():
        print(f"  {k:<18} peak {v:6.3f}s")
