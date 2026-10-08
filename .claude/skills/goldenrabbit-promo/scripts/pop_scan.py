#!/usr/bin/env python3
"""Find single-frame glitches in a rendered MP4 — the defects that contact sheets and spot snapshots miss
(an element flashing for one frame, a leak at a frame boundary, a tween that snaps and snaps back).

  python3 pop_scan.py videos/<name> [renders/<name>.mp4]     # exit 0 always; prints findings

Method (pure python, no numpy): ffmpeg decodes every frame to a 64×36 grayscale thumbnail. For frame i:
  d_prev = mean|f[i]-f[i-1]|, d_next = mean|f[i+1]-f[i]|, d_skip = mean|f[i+1]-f[i-1]|
- POP   : d_prev and d_next both jump (≥ 3× the local median and ≥ 4 grey levels) while d_skip stays small
          → frame i is unlike BOTH neighbours, which are like each other = a one-frame flash. Almost always a bug;
          a deliberate 1-frame shake (stamp wobble) can also trigger it at low Δ (< 5) — look before fixing.
- SPIKE : an ISOLATED jump — d_prev ≥ 3× the local median and ≥ 8 grey levels while d[i-1] and d[i+1] stay low —
          NOT within 2 frames of a storyboard frame boundary → a hard change mid-scene. Continuous fast motion
          (several big frames in a row) is not reported. Often intended (0 ms swap, register flip); look at it.
Each finding prints the track time; grab it with:  ffmpeg -ss <t-0.05> -i <mp4> -frames:v 3 -vf tile=3x1 out.png
"""
import json, statistics, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import parse_storyboard  # noqa: E402

W, H = 64, 36


def frames(mp4):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    n = W * H
    return [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]


def mad(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def main():
    proj = Path(sys.argv[1]).resolve()
    mp4 = Path(sys.argv[2]) if len(sys.argv) > 2 else proj / "renders" / f"{proj.name}.mp4"
    if not mp4.is_absolute():
        mp4 = proj / mp4
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate",
                            "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout.strip()
    num, _, den = probe.partition("/")
    fps = float(num) / float(den or 1)
    bounds = set()
    sb = proj / "STORYBOARD.md"
    if sb.exists():
        for f in parse_storyboard(sb):
            if "span" in f:
                bounds |= {round(f["span"][0] * fps), round(f["span"][1] * fps)}
    F = frames(mp4)
    d = [0.0] + [mad(F[i], F[i - 1]) for i in range(1, len(F))]
    pops, spikes = [], []
    for i in range(1, len(F) - 1):
        win = d[max(1, i - 8):i - 1] + d[i + 2:i + 10]
        base = statistics.median(win) if win else 0.0
        thr = max(3 * base, 2.5)
        if d[i] >= max(thr, 4.0) and d[i + 1] >= max(thr, 4.0) and mad(F[i + 1], F[i - 1]) < 0.35 * min(d[i], d[i + 1]):
            pops.append((i, d[i]))
        elif (d[i] >= max(3 * base, 8.0) and d[i - 1] < d[i] / 3 and d[i + 1] < d[i] / 3
              and not any(abs(i - b) <= 2 for b in bounds)):
            spikes.append((i, d[i]))
    print(f"pop_scan: {mp4.name} · {len(F)} frames @ {fps:g} fps · {len(pops)} pop(s) · {len(spikes)} mid-scene spike(s)")
    for i, v in pops:
        print(f"  ✗ POP   t={i / fps:7.3f}s (frame {i})  Δ={v:5.1f} — one-frame flash, unlike both neighbours")
    for i, v in spikes[:20]:
        print(f"  ⚠ SPIKE t={i / fps:7.3f}s (frame {i})  Δ={v:5.1f} — hard change mid-scene; intended?")
    if len(spikes) > 20:
        print(f"  … {len(spikes) - 20} more spikes")


if __name__ == "__main__":
    main()
