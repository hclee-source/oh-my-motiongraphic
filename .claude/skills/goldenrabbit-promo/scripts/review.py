#!/usr/bin/env python3
"""Snapshot a variant at every frame's start/middle/end + every key moment, and print the
contact sheets to inspect. Workers' self-tests don't see cross-frame bugs — this does.

  python3 review.py videos/<name> [--out snapshots/review] [--extra 12.5,30]
"""
import argparse, json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import parse_storyboard  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--out", default="snapshots/review")
    ap.add_argument("--extra", default="")
    a = ap.parse_args()
    proj = Path(a.project).resolve()
    am = json.loads((proj / "audiomap.json").read_text())
    D = am["audio"]["duration_sec"]
    ts = set()
    for f in parse_storyboard(proj / "STORYBOARD.md"):
        if "span" in f:
            s, e = f["span"]
            ts.update([s + 0.25, (s + e) / 2, max(s, e - 0.15)])
    ts.update(k["t"] + 0.1 for k in am.get("key_moments", []))
    ts.update(float(x) for x in a.extra.split(",") if x)
    ts = sorted(round(t, 2) for t in ts if 0 <= t <= D - 0.05)
    print(f"snapshotting {len(ts)} times → {a.out}")
    r = subprocess.run([("npx.cmd" if sys.platform == "win32" else "npx"), "hyperframes", "snapshot", ".", "-o", a.out, "--at", ",".join(map(str, ts)), "--no-end", "--describe", "false"],
                       cwd=proj, capture_output=True, text=True)
    print(r.stdout[-400:] if r.returncode == 0 else r.stderr[-800:])
    sheets = sorted((proj / a.out).glob("contact-sheet*.jpg"))
    print("inspect every sheet (Read tool):")
    for s in sheets:
        print("  ", s)
    print("look for: stray elements repeated across frames · text over covers · text hidden under the HUD · blank/unstyled frames · fallback (serif) Korean glyphs")


if __name__ == "__main__":
    main()
