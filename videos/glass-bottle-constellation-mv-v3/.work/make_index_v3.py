#!/usr/bin/env python3
"""v3 root: footage everywhere. Layers (bottom → top):
  track 1  compositions/footage.html          (z 100)  all non-insert footage, from .work/edl.json
  track 2  compositions/inserts/*.html         (z 600)  v2 footage+lyric inserts A–D (exits rewritten for v3)
  track 3  compositions/lyrics/<sec>.html      (z 700)  transparent lyric/light layers for the footage sections
  track 4  compositions/overlay.html           (z 1050) grain + vignette
  track 11 assets/bgm.mp3
No v1 graphic frames, no sky layer, no SVG bottle anywhere.
"""
import json
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
DUR = json.loads((PROJ / "audiomap.json").read_text())["audio"]["duration_sec"]

INSERTS = [("ia-verse1", 11.10, 20.60), ("ib-verse2", 66.70, 19.85), ("ic-final", 144.30, 10.70), ("id-outro", 170.05, 10.70)]
LYRICS = [("s01-intro", 0.00, 11.10), ("s03-pre1", 31.70, 10.70), ("s04-chorus1", 42.40, 24.30), ("s06-chorus2", 86.55, 32.05),
          ("s07-bridge", 118.60, 10.10), ("s08-build", 128.70, 10.30), ("s09-finalA", 139.00, 5.30), ("s11-finalB", 155.00, 15.05),
          ("s13-ending", 180.75, round(DUR - 180.75, 2))]


def host(cid, src, start, dur, track, z):
    return (f'      <div id="el-{cid}" class="frame" data-composition-id="{cid}" data-composition-src="{src}" '
            f'data-start="{start}" data-duration="{dur}" data-track-index="{track}" style="z-index: {z}"></div>\n')


layers = host("footage", "compositions/footage.html", 0, DUR, 1, 100)
for cid, s, d in INSERTS:
    if (PROJ / "compositions" / "inserts" / f"{cid}.html").exists():
        layers += host(cid, f"compositions/inserts/{cid}.html", s, d, 2, 600)
have = []
for cid, s, d in LYRICS:
    if (PROJ / "compositions" / "lyrics" / f"{cid}.html").exists():
        layers += host(cid, f"compositions/lyrics/{cid}.html", s, d, 3, 700)
        have.append(cid)
layers += host("overlay", "compositions/overlay.html", 0, DUR, 4, 1050)

html = f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      .frame {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
{layers}      <audio id="el-bgm" src="assets/bgm.mp3" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        var tl = gsap.timeline({{ paused: true }});
        tl.set({{}}, {{}}, {DUR});
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
"""
(PROJ / "index.html").write_text(html)
print("index.html: footage + inserts", [c for c, _, _ in INSERTS], "+ lyrics", have)
