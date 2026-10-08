#!/usr/bin/env python3
"""Add a sound-design layer: SFX clips on the root timeline, from STORYBOARD cues + automatic transition whooshes.

STORYBOARD fields per frame:
  - sfx: pop@7.99, typing@12.10, chime@31.1      # TRACK seconds; names = files in shared/sfx (without .mp3)
                                                  # a cue time = when the sound should HIT (see alignment below)
  - sfx: riser@6.01:start                         # per-cue override: :start (file start on the cue) or :peak
  - sfx_auto: off                                 # disable the automatic whoosh for this frame's transition_out
Automatic: every frame with a `transition_out` (≠ none) gets `whoosh-short` 0.18s before its end boundary.

Library (shared/sfx, Pixabay Content License — commercial use, no attribution required):
  whoosh whoosh-short whoosh-cinematic riser · impact-bass-1 impact-bass-2 ping pop · glitch-1/2/3 error ·
  click click-soft key-press typing notification · chime sparkle
Synthesized here (CC0, shared/sfx/src/synth_sfx.py): tick tock (clock, for silent cold opens) · bat-crack (wooden bat hit)

  python3 sfx.py videos/<name>          # idempotent: replaces previously injected sfx clips

Alignment: variant.json `sfx_align: peak` (written by new_variant.py since 2026-10-08) shifts each clip earlier by the
file's measured loudest moment (sfx_peaks.py → shared/sfx/peaks.json), so the audible hit lands on the cue — e.g.
whoosh-cinematic peaks 2.54 s in, chime 0.42 s. Textures that should *begin* on the cue (typing, riser) stay start-aligned.
Projects without the key keep the old start alignment, so re-assembling an old video does not move its sounds.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import SHARED, parse_storyboard  # noqa: E402
from sfx_peaks import load as load_peaks  # noqa: E402

START_ALIGNED = {"typing", "riser"}   # textures: the cue marks where they begin

VOL = {"whoosh": 0.40, "whoosh-short": 0.40, "whoosh-cinematic": 0.35, "riser": 0.35, "impact-bass-1": 0.5, "impact-bass-2": 0.5,
       "ping": 0.35, "pop": 0.45, "glitch-1": 0.3, "glitch-2": 0.3, "glitch-3": 0.3, "error": 0.3, "click": 0.4, "click-soft": 0.4,
       "key-press": 0.35, "typing": 0.30, "notification": 0.35, "chime": 0.45, "sparkle": 0.40,
       "tick": 0.55, "tock": 0.5, "bat-crack": 0.85}


def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return round(float(out.stdout.strip() or 0.5), 3)


def main():
    proj = Path(sys.argv[1]).resolve()
    D = json.loads((proj / "audiomap.json").read_text())["audio"]["duration_sec"]
    vj = proj / "variant.json"
    vjd = json.loads(vj.read_text()) if vj.exists() else {}
    gain = float(vjd.get("sfx_gain", 1.0))   # <1 under a vocal song
    align = vjd.get("sfx_align", "start")
    peaks = load_peaks() if align == "peak" else {}
    cues = []
    for f in parse_storyboard(proj / "STORYBOARD.md"):
        for c in [x.strip() for x in f["fields"].get("sfx", "").split(",") if x.strip()]:
            name, _, t = c.partition("@")
            t, _, mode = t.partition(":")
            name = name.strip()
            mode = mode.strip() or ("start" if align != "peak" or name in START_ALIGNED else "peak")
            if mode == "peak":
                peaks = peaks or load_peaks()
                t = float(t) - peaks.get(name, 0.0)
            cues.append((round(float(t), 3), name))
        tr = f["fields"].get("transition_out", "none").split()
        if tr and tr[0] != "none" and f["fields"].get("sfx_auto", "on") != "off" and "span" in f:
            cues.append((round(f["span"][1] - 0.18, 3), "whoosh-short"))   # file start; its swish (0.16 s in) lands just before the cut
    cues.sort()
    (proj / "assets/sfx").mkdir(parents=True, exist_ok=True)
    tags, last_end = [], {}
    for n, (t, name) in enumerate(cues, 1):
        src = SHARED / "sfx" / f"{name}.mp3"
        if not src.exists():
            sys.exit(f"✗ unknown sfx '{name}' (see shared/sfx)")
        dst = proj / "assets/sfx" / f"{name}.mp3"
        if not dst.exists():
            shutil.copy2(src, dst)
        off = 0.0
        if t < 0:                       # hit cued earlier than the file's lead-in allows: skip into the file instead
            off, t = round(-t, 3), 0.0
        d = min(dur(dst) - off, max(0.05, D - t))
        track = next(k for k in range(21, 40) if last_end.get(k, -1) <= t)   # overlapping clips need distinct tracks
        last_end[track] = t + d
        tags.append(f'      <audio id="sfx-{n:02d}" class="gr-sfx" src="assets/sfx/{name}.mp3" data-start="{max(0, t):.3f}" '
                    + (f'data-media-start="{off:.3f}" ' if off else "") +
                    f'data-duration="{d:.3f}" data-track-index="{track}" data-volume="{round(VOL.get(name, 0.4) * gain, 3)}"></audio>')
    idx = proj / "index.html"
    s = idx.read_text()
    s = re.sub(r'\n\s*<audio id="sfx-\d+" class="gr-sfx"[^>]*></audio>', "", s)
    m = list(re.finditer(r"<audio[^>]*el-bgm[^>]*>(?:\s*</audio>)?", s))
    if not m:
        sys.exit("✗ no BGM <audio> in index.html — assemble first")
    i = m[-1].end()
    s = s[:i] + "\n" + "\n".join(tags) + s[i:]
    idx.write_text(s)
    print(f"✓ {len(tags)} sfx clips → index.html: " + ", ".join(f"{n}@{t}" for t, n in cues))


if __name__ == "__main__":
    main()
