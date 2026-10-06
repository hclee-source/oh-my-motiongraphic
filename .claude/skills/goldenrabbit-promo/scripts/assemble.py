#!/usr/bin/env python3
"""Assemble a variant: preflight → music-to-video assemble-index → HUD (if on) → inject HUD.

  python3 assemble.py videos/<name>            # stops on preflight errors
  python3 assemble.py videos/<name> --no-hud   # skip the HUD even if variant.json enables it
"""
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import M2V  # noqa: E402

HERE = Path(__file__).resolve().parent


def inject_overlay(proj, comp_id, track):
    """Mount compositions/<comp_id>.html full-length on `track` (above the frames, below the audio).
    Frame hosts are not stacking contexts, so z-indexed elements inside frames would otherwise paint OVER the
    overlay (seen: a card showing through a transition) — the host gets an explicit high z-index."""
    p = proj / "index.html"
    s = p.read_text()
    if f"compositions/{comp_id}.html" in s:
        return "already present"
    dur = json.loads((proj / "audiomap.json").read_text())["audio"]["duration_sec"]
    block = f'''
      <div
        id="el-{comp_id}"
        class="frame"
        data-composition-id="{comp_id}"
        data-composition-src="compositions/{comp_id}.html"
        data-start="0"
        data-duration="{dur}"
        data-track-index="{track}"
        style="z-index: {900 + track * 50}"
      ></div>
'''
    m = re.search(r"\n\s*<audio", s)
    i = m.start() if m else s.rfind("</div>")
    p.write_text(s[:i] + block + s[i:])
    return f"inserted on track {track}"


def main():
    proj = Path(sys.argv[1]).resolve()
    no_hud = "--no-hud" in sys.argv
    spec = json.loads((proj / "variant.json").read_text())
    r = subprocess.run([sys.executable, str(HERE / "preflight.py"), str(proj)])
    if r.returncode != 0:
        sys.exit("✗ preflight failed — fix the frames (or re-dispatch the worker with the findings) before assembling")
    out = subprocess.run(["node", str(M2V / "scripts/assemble-index.mjs"), "--storyboard", str(proj / "STORYBOARD.md"),
                          "--hyperframes", str(proj), "--audiomap", str(proj / "audiomap.json")], capture_output=True, text=True)
    print(out.stdout.strip()[-600:])
    if out.returncode != 0 or "✗" in out.stdout:
        sys.exit(out.stderr[-600:] or "✗ assemble-index failed")
    if spec.get("hud", True) and not no_hud:
        subprocess.run([sys.executable, str(HERE / "make_hud.py"), str(proj)], check=True)
        print(f"✓ HUD {inject_overlay(proj, 'hud', 2)}")
    sb = (proj / "STORYBOARD.md").read_text()
    if re.search(r"^- transition_out: (?!none)", sb, re.M):
        subprocess.run([sys.executable, str(HERE / "make_transitions.py"), str(proj)], check=True)
        print(f"✓ transitions overlay {inject_overlay(proj, 'transitions', 3)}")
    if re.search(r"^- (sfx|transition_out): (?!none)", sb, re.M) and not spec.get("sfx_off"):
        subprocess.run([sys.executable, str(HERE / "sfx.py"), str(proj)], check=True)
    print("next: npx hyperframes check . (in the project) → scripts/review.py → scripts/finalize.sh")


if __name__ == "__main__":
    main()
