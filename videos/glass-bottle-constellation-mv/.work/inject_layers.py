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

html = idx.read_text()
html = re.sub(r'\s*<div\s+id="el-sky".*?</div>\n', "\n", html, flags=re.S)
html = re.sub(r'\s*<div\s+id="el-overlay".*?</div>\n', "\n", html, flags=re.S)
# sky goes first inside #root, overlay right before the bgm audio
m = re.search(r'(<div\s+id="root"[^>]*>\n)', html, flags=re.S)
assert m, "root div not found"
html = html[: m.end()] + SKY + html[m.end():]
a = html.find('<audio id="el-bgm"')
assert a > 0, "bgm audio not found"
line_start = html.rfind("\n", 0, a) + 1
html = html[:line_start] + OVERLAY + html[line_start:]
idx.write_text(html)
print("injected sky (track 0) + overlay (track 3) into index.html")
