#!/usr/bin/env python3
"""After music-to-video's assemble-index.mjs rewrites index.html, inject the orchestrator-owned layers:
   sky (track 0, under every frame, own stacking context z-index:0, placed BEFORE the frames in DOM)
   overlay (track 3, z-index:1050, vignette + grain over everything).
Usage: python3 .work/inject_layers.py [--sky-only]   (--sky-only writes a test index with just sky+overlay+bgm)
"""
import re, sys, json
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
DUR = json.loads((PROJ / "audiomap.json").read_text())["audio"]["duration_sec"]
idx = PROJ / "index.html"

SKY = f'''      <div
        id="el-sky"
        class="frame"
        data-composition-id="sky"
        data-composition-src="compositions/sky.html"
        data-start="0"
        data-duration="{DUR}"
        data-track-index="0"
        style="z-index: 0"
      ></div>
'''
OVERLAY = f'''      <div
        id="el-overlay"
        class="frame"
        data-composition-id="overlay"
        data-composition-src="compositions/overlay.html"
        data-start="0"
        data-duration="{DUR}"
        data-track-index="3"
        style="z-index: 1050; pointer-events: none"
      ></div>
'''

if "--sky-only" in sys.argv:
    html = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
      .frame {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
{SKY}{OVERLAY}      <audio id="el-bgm" src="assets/bgm.mp3" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, {DUR});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
    idx.write_text(html)
    print("wrote sky-only test index.html")
    sys.exit(0)

INSERTS = [  # footage inserts (v2): id, track start, duration — mounted on track 2 above the frames
    ("ia-verse1", 11.10, 20.60),
    ("ib-verse2", 66.70, 19.85),
    ("ic-final", 144.30, 10.70),
    ("id-outro", 170.05, 10.70),
]
INS = "".join(f'''      <div
        id="el-{i}"
        class="frame"
        data-composition-id="{i}"
        data-composition-src="compositions/inserts/{i}.html"
        data-start="{s0}"
        data-duration="{d}"
        data-track-index="2"
        style="z-index: 600"
      ></div>
''' for i, s0, d in INSERTS if (PROJ / "compositions" / "inserts" / f"{i}.html").exists())

html = idx.read_text()
html = re.sub(r'\s*<div\s+id="el-sky".*?</div>\n', "\n", html, flags=re.S)
for i, _, _ in INSERTS:
    html = re.sub(rf'\s*<div\s+id="el-{i}".*?</div>\n', "\n", html, flags=re.S)
html = re.sub(r'\s*<div\s+id="el-overlay".*?</div>\n', "\n", html, flags=re.S)
# sky goes first inside #root, overlay right before the bgm audio
m = re.search(r'(<div\s+id="root"[^>]*>\n)', html, flags=re.S)
assert m, "root div not found"
html = html[: m.end()] + SKY + html[m.end():]
a = html.find('<audio id="el-bgm"')
assert a > 0, "bgm audio not found"
line_start = html.rfind("\n", 0, a) + 1
html = html[:line_start] + INS + OVERLAY + html[line_start:]
# v1 frames fully/partly covered by opaque footage are hidden on the root timeline while covered
# (keeps the layout checker from comparing invisible text and saves paint work). opacity only — the runtime owns visibility.
HIDE = [("02-f2", 11.10, 31.30), ("05-f5", 66.70, None), ("06-f6", 76.90, None), ("10-f10", 144.66, None),
        ("11-f11", 149.55, 154.70), ("12-f12", 170.05, None), ("13-f13", 180.60, 180.75)]
present = [h for h in HIDE if f'id="el-{h[0]}"' in html and any(f'id="el-{i}"' in html for i, _, _ in INSERTS)]
lines = []
for fid, a, b in present:
    lines.append(f'tl.set("#el-{fid}", {{ opacity: 0 }}, {a});')
    if b is not None:
        lines.append(f'tl.set("#el-{fid}", {{ opacity: 1 }}, {b});')
root_js = ('''    <script>
      window.__timelines = window.__timelines || {};
      (function () {
        var tl = gsap.timeline({ paused: true });
        ''' + "\n        ".join(lines) + f'''
        tl.set({{}}, {{}}, {DUR});
        window.__timelines["main"] = tl;
      }})();
    </script>''')
html = re.sub(r'    <script>\s*window.__timelines = window.__timelines \|\| \{\};.*?</script>', root_js, html, count=1, flags=re.S)
idx.write_text(html)
print("root hides:", len(lines), "sets")
print("injected sky (track 0) + overlay (track 3) + inserts:", [i for i, _, _ in INSERTS if f'id="el-{i}"' in html])
