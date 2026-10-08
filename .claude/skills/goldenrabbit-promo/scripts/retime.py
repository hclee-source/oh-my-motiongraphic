#!/usr/bin/env python3
"""Re-time a finished variant onto a different music track (e.g. a user's own song), frame by frame.

Each output frame is an existing frame of the source variant whose timeline is WARPED piecewise-linearly so that its
old bar lines land on the new track's downbeats. Frames can be dropped (a shorter song) or re-ordered; nothing is rebuilt.

  python3 retime.py videos/<src> <new-name> --bgm path/to/song.mp3 --plan plan.json [--sfx-gain 0.7] [--drop-sfx tick,tock]

plan.json:
  {"frames": [
     {"src": "01-f1", "old": [0, 1.55, 3.10, 4.65, 6.20, 7.75], "new": [0, 2.76, 4.43, 6.11, 7.78, 9.45]},
     {"src": "02-f2", "old": [7.75, 9.30, 10.84],               "new": [9.45, 11.15, 12.82]}, …]}
  old/new = matching marks in ABSOLUTE seconds (old track / new track): first and last = the frame's span. Frames tile the
  new track in the listed order; the last frame's last `new` mark is stretched to the song's real duration.

What it does: copies the project (no renders/snapshots/caches), keeps only the listed frames, rewrites each frame's
#stage data-duration and wraps its registered timeline in an outer timeline that tweens the inner `time` through a
piecewise-linear ease (seek-safe), remaps STORYBOARD spans/anchors/sfx cues through the same maps, installs the song
as assets/bgm.mp3, re-analyzes the audiomap and writes variants/<new>.json. Then run assemble.py → check → review → finalize.
"""
import argparse, bisect, json, re, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import ROOT, VIDEOS, VARIANTS, PY, M2V  # noqa: E402

SKIP = {"renders", "snapshots", ".hyperframes", ".thumbnails", ".waveform-cache", ".backup", "node_modules"}


def interp(xs, ys, x):
    """Piecewise-linear map xs→ys (clamped)."""
    if x <= xs[0]:
        return ys[0] + (x - xs[0]) * ((ys[1] - ys[0]) / (xs[1] - xs[0]))
    if x >= xs[-1]:
        return ys[-1] + (x - xs[-1]) * ((ys[-1] - ys[-2]) / (xs[-1] - xs[-2]))
    i = bisect.bisect_right(xs, x) - 1
    u = (x - xs[i]) / (xs[i + 1] - xs[i])
    return ys[i] + u * (ys[i + 1] - ys[i])


WRAP = '''          // ---- retimed by goldenrabbit-promo/scripts/retime.py: the authored timeline (OLD s) is driven through a
          // piecewise-linear warp so its bar lines land on the new track's downbeats (NEW s). Seek-safe: a tween on tl.time.
          (function (inner) {{
            var MAP = {map};   // [new local s, old local s]
            var OLD = {old}, NEW = {new};
            function warp(p) {{
              var t = p * NEW;
              for (var i = 1; i < MAP.length; i++) {{
                if (t <= MAP[i][0] || i === MAP.length - 1) {{
                  var a = MAP[i - 1], b = MAP[i], u = (t - a[0]) / (b[0] - a[0]);
                  return (a[1] + (b[1] - a[1]) * Math.max(0, Math.min(1, u))) / OLD;
                }}
              }}
              return 1;
            }}
            inner.pause();
            var outer = gsap.timeline({{ paused: true }});
            outer.fromTo(inner, {{ time: 0 }}, {{ time: OLD, duration: NEW, ease: warp, immediateRender: false }}, 0);
            outer.seek(0.001); outer.seek(0);
            window.__timelines["{fid}"] = outer;
          }})({var});'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("name")
    ap.add_argument("--bgm", required=True); ap.add_argument("--plan", required=True)
    ap.add_argument("--sfx-gain", type=float, default=1.0)
    ap.add_argument("--drop-sfx", default="tick,tock")
    ap.add_argument("--fade", type=float, default=0.3)
    a = ap.parse_args()
    src = Path(a.src).resolve(); dst = VIDEOS / a.name
    plan = json.loads(Path(a.plan).read_text())["frames"]
    if dst.exists():
        sys.exit(f"✗ {dst} exists — pick a new name (never overwrite a variant)")
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP])
    keep = {f["src"] for f in plan}
    for f in (dst / "compositions/frames").glob("*.html"):
        if f.stem not in keep:
            f.unlink()

    # ---- song → assets/bgm.mp3 + audiomap
    song = Path(a.bgm).expanduser().resolve()
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(song)],
                               capture_output=True, text=True).stdout.strip())
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(song), "-map", "0:a", "-af",
                    f"afade=t=in:st=0:d=0.02,afade=t=out:st={max(0, dur - a.fade):.3f}:d={a.fade}",
                    "-c:a", "libmp3lame", "-b:a", "256k", str(dst / "assets/bgm.mp3")], check=True)
    subprocess.run([str(PY), str(M2V / "scripts/analyze-beatgrid.py"), str(dst / "assets/bgm.mp3"), "-o", str(dst / "audiomap.json")],
                   check=True, capture_output=True)
    D = json.loads((dst / "audiomap.json").read_text())["audio"]["duration_sec"]
    plan[-1]["new"][-1] = D
    if abs(plan[0]["new"][0]) > 1e-6:
        sys.exit("✗ the first frame must start at new time 0")
    for i in range(1, len(plan)):
        if abs(plan[i]["new"][0] - plan[i - 1]["new"][-1]) > 1e-3:
            sys.exit(f"✗ frames must tile: {plan[i-1]['src']} ends {plan[i-1]['new'][-1]} but {plan[i]['src']} starts {plan[i]['new'][0]}")

    # ---- frames: data-duration + warp wrapper
    for f in plan:
        p = dst / "compositions/frames" / f"{f['src']}.html"
        s = p.read_text()
        o0, n0 = f["old"][0], f["new"][0]
        old_d, new_d = f["old"][-1] - o0, f["new"][-1] - n0
        # Studio may insert attributes (data-hf-id) before id="stage" — don't anchor on attribute order
        s, k = re.subn(rf'(<div\b[^>]*\bid="stage" data-composition-id="{f["src"]}"[^>]*data-duration=")[\d.]+(")',
                       rf"\g<1>{new_d:.3f}\g<2>", s)
        if k != 1:
            sys.exit(f"✗ {p.name}: could not set #stage data-duration")
        m = re.search(rf'[ \t]*window\.__timelines\[(?:"{f["src"]}"|[A-Z_]+)\] = (\w+);', s)   # ["01-f1"] or [FID]
        if not m:
            sys.exit(f"✗ {p.name}: timeline registration not found")
        mp = [[round(nn - n0, 4), round(oo - o0, 4)] for oo, nn in zip(f["old"], f["new"])]
        block = "          window.__timelines = window.__timelines || {};\n" + \
                WRAP.format(map=json.dumps(mp), old=f"{old_d:.4f}", new=f"{new_d:.4f}", fid=f["src"], var=m.group(1))
        s = s[:m.start()] + block + s[m.end():]
        p.write_text(s)

    # ---- STORYBOARD: keep the listed frame blocks in order, remap seconds
    sb = (dst / "STORYBOARD.md").read_text()
    head, rest = sb.split("\n## Frame ", 1)
    blocks = {}
    for b in re.split(r"\n(?=## Frame )", "## Frame " + rest):
        mm = re.match(r"## Frame \d+ — (\S+)", b)
        if mm:
            blocks[mm.group(1)] = b
    drop = {x.strip() for x in a.drop_sfx.split(",") if x.strip()}
    out = []
    for n, f in enumerate(plan, 1):
        tag = f["src"].split("-")[1]
        b = blocks[tag]
        mapf = lambda x: interp(f["old"], f["new"], x)  # noqa: E731
        b = re.sub(r"^## Frame \d+ — ", f"## Frame {n} — ", b, count=1)
        b = re.sub(r"^- duration: [\d.]+s", f"- duration: {f['new'][-1] - f['new'][0]:.3f}s", b, flags=re.M)
        b = re.sub(r"span_sec: \[([\d.]+), ([\d.]+)\]",
                   lambda r: f"span_sec: [{round(mapf(float(r.group(1))), 3)}, {round(mapf(float(r.group(2))), 3)}]", b)
        b = re.sub(r"anchors: \[([^\]]*)\]",
                   lambda r: "anchors: [" + ", ".join(str(round(mapf(float(x)), 2)) for x in r.group(1).split(",") if x.strip()) + "]", b)
        def sfx_line(r):
            cues = []
            for c in r.group(1).split(","):
                nm, _, t = c.strip().partition("@")
                if nm and t and nm not in drop:
                    cues.append(f"{nm}@{round(mapf(float(t)), 2)}")
            return "- sfx: " + ", ".join(cues) if cues else "- sfx_none: (dropped)"
        b = re.sub(r"^- sfx: (.*)$", sfx_line, b, flags=re.M)
        b = re.sub(r"^(- span_sec: .*)$", rf"\1\n- retimed: old {f['old']} → new {[round(x, 3) for x in f['new']]} (group intents keep their ORIGINAL seconds)", b, count=1, flags=re.M)
        if n == len(plan):
            b = re.sub(r"^- transition_out: .*$", "- transition_out: none", b, flags=re.M)
        out.append(b.rstrip() + "\n")
    head = re.sub(r"duration_s: [\d.]+", f"duration_s: {D}", head)
    head = re.sub(r"(variant: \{ name: )[^,]+", rf"\g<1>{a.name}", head)
    head = head.replace("build_notes:\n", f"build_notes:\n  - \"RETIMED from {src.name} onto {song.name} by scripts/retime.py — frame timelines are warped; edit the source variant, then re-run retime\"\n", 1)
    (dst / "STORYBOARD.md").write_text(head.rstrip() + "\n\n" + "\n".join(out))

    # ---- records
    var = json.loads((dst / "variant.json").read_text())
    var.update({"name": a.name, "retimed_from": src.name, "sfx_gain": a.sfx_gain,
                "bgm": {"file": str(song), "duration": D, "source": "user-supplied song"}, "retime_plan": plan})
    var.pop("outputs", None)
    (dst / "variant.json").write_text(json.dumps(var, ensure_ascii=False, indent=2))
    spec = json.loads((VARIANTS / f"{src.name}.json").read_text()) if (VARIANTS / f"{src.name}.json").exists() else {}
    spec.update({"name": a.name, "retimed_from": src.name, "sfx_gain": a.sfx_gain,
                 "bgm": {"file": str(song.relative_to(ROOT)) if str(song).startswith(str(ROOT)) else str(song), "duration": D,
                         "license": "user-supplied (made with Suno by the user)"}, "retime_plan": plan})
    spec.pop("outputs", None)
    (VARIANTS / f"{a.name}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2))
    mj = dst / "meta.json"
    if mj.exists():
        m = json.loads(mj.read_text()); m["id"] = m["name"] = a.name; mj.write_text(json.dumps(m, indent=2))
    print(f"✓ {dst.relative_to(ROOT)} · {len(plan)} frames · {D}s · next: python3 scripts/assemble.py {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
