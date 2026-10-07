#!/usr/bin/env python3
"""Generate compositions/transitions.html — a full-length overlay (track 3) that HIDES every frame→frame
hard cut under a shape transition, so a video stops feeling like a slideshow of hard cuts.

STORYBOARD fields read per frame (all optional):
  - scene_color: #D7E4BD                  # the frame's ground color
  - transition_out: iris 1300,560         # kind [+ origin x,y]; kinds: iris | blinds | wipe | stripes | rings | tear | paper | none
    rings = concentric circles in two palette colours + the next ground (Japanese ad iris, reveal through a growing hole)
    tear  = a torn-edged sheet of the next ground slides across (white torn core + paper shadow) and on off the other side
    paper = a sheet is laid down (tilt in, shadow shrinking) and then pulled away the other way
The cover color = the NEXT frame's scene_color (so the reveal lands on that frame's ground).
Timing: the cover is fully opaque from boundary−2 frames to boundary+2 frames; it covers over ~0.22s and reveals over ~0.30s.
Frames should therefore start on their own scene_color ground, and keep nothing essential in the first 0.3s or the last 0.25s.

  python3 make_transitions.py videos/<name>
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import aspect_cfg, parse_storyboard, load_style  # noqa: E402

COVER, REVEAL, HOLD = 0.22, 0.30, 0.07


def make_paper_texture(path, n=512):
    """Seamless static paper-fibre tile (multiply overlay): soft mottling + a few curved fibres + specks.
    Static on purpose (no jitter = small files). Seamless: periodic coarse grid upscaled from a 3×3 tiling, fibres wrap."""
    import math, random
    from PIL import Image, ImageDraw, ImageFilter
    path.parent.mkdir(parents=True, exist_ok=True)
    rnd = random.Random(11)
    g = n // 16
    coarse = Image.new("L", (g, g))
    coarse.putdata([int(rnd.gauss(246, 4)) for _ in range(g * g)])
    big = Image.new("L", (g * 3, g * 3))
    for i in range(3):
        for j in range(3):
            big.paste(coarse, (i * g, j * g))
    im = big.resize((n * 3, n * 3), Image.BICUBIC).crop((n, n, 2 * n, 2 * n)).filter(ImageFilter.GaussianBlur(4))
    d = ImageDraw.Draw(im)
    for _ in range(260):   # curved fibres, drawn with wrap-around copies so the tile stays seamless
        x, y, a = rnd.uniform(0, n), rnd.uniform(0, n), rnd.uniform(0, 6.283)
        pts, L = [(x, y)], rnd.uniform(10, 30)
        for _k in range(4):
            a += rnd.uniform(-0.5, 0.5)
            x, y = x + L / 4 * math.cos(a), y + L / 4 * math.sin(a)
            pts.append((x, y))
        c = int(rnd.uniform(224, 238))
        for ox in (-n, 0, n):
            for oy in (-n, 0, n):
                d.line([(px + ox, py + oy) for px, py in pts], fill=c, width=1)
    for _ in range(1200):  # specks
        d.point((rnd.randrange(n), rnd.randrange(n)), fill=int(rnd.uniform(214, 236)))
    im = im.filter(ImageFilter.GaussianBlur(0.7))
    # Bake it as dark fibres in the ALPHA channel (normal blending). mix-blend-mode: multiply does NOT reach the frames
    # below — the overlay host is its own stacking context — so a multiply layer rendered as a milky veil over the video.
    alpha = im.point(lambda v: max(0, min(255, int((250 - v) * 2.4))))
    rgba = Image.merge("RGBA", (Image.new("L", im.size, 92), Image.new("L", im.size, 70), Image.new("L", im.size, 40), alpha))
    rgba.save(path)


def torn_sheet(tid, color, W, H, seed):
    """A sheet wider than the frame with torn (jagged) left and right edges, a white torn core showing behind them."""
    import random
    rnd = random.Random(100 + seed)
    SW, SH = int(W * 1.45), H + 80
    def edge(x0, sign):
        pts, y = [], 0
        while y < SH:
            pts.append((x0 + sign * rnd.uniform(0, 34), y))
            y += rnd.uniform(14, 34)
        pts.append((x0 + sign * rnd.uniform(0, 34), SH))
        return pts
    left, right = edge(40, 1), edge(SW - 40, -1)
    def poly(lpts, rpts, grow):
        p = [(x - grow, y) for x, y in lpts] + [(x + grow, y) for x, y in reversed(rpts)]
        return " ".join(f"{x:.0f},{y:.0f}" for x, y in p)
    return (f'<svg class="tr-torn" id="{tid}" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}">'
            f'<polygon points="{poly(left, right, 9)}" fill="#FFFDF7"/>'
            f'<polygon points="{poly(left, right, 0)}" fill="{color}"/></svg>')


def main():
    proj = Path(sys.argv[1]).resolve()
    spec = json.loads((proj / "variant.json").read_text())
    A = aspect_cfg(spec.get("aspect", "16:9")); W, H = A["w"], A["h"]
    D = json.loads((proj / "audiomap.json").read_text())["audio"]["duration_sec"]
    frames = parse_storyboard(proj / "STORYBOARD.md")
    items, html_parts = [], []
    try:
        style, _ = load_style(spec.get("style", "bold-beat"))
    except SystemExit:
        style = {}
    toks = dict(style.get("tokens", {}))
    toks.update(spec.get("palette", {}))
    texture = spec.get("texture", style.get("texture", "grain" if spec.get("style") == "soft-studio" else "none"))
    if texture == "grain":
        tex = proj / "assets" / "textures" / "grain.png"
        if not tex.exists():
            import random
            from PIL import Image, ImageFilter
            tex.parent.mkdir(parents=True, exist_ok=True)
            rnd = random.Random(7)
            # soft, slightly coarse grain: full-res per-pixel noise jittered every frame made a 30s render 240MB
            im = Image.new("L", (192, 192))
            im.putdata([max(0, min(255, int(rnd.gauss(128, 40)))) for _ in range(192 * 192)])
            im = im.filter(ImageFilter.GaussianBlur(0.7)).resize((384, 384), Image.BILINEAR)
            im.convert("RGB").save(tex)
        html_parts.append('<div id="tr_grain"></div>')
    if texture == "paper":
        tex = proj / "assets" / "textures" / "paper.png"
        if not tex.exists():
            make_paper_texture(tex)
        html_parts.append('<div id="tr_paper"></div>')
    ring_pool = [toks[k] for k in ("yellow", "navy", "red", "accent", "ink") if k in toks]
    for i in range(len(frames) - 1):
        f, nxt = frames[i], frames[i + 1]
        spec_t = f["fields"].get("transition_out", "").split()
        kind = spec_t[0] if spec_t else "none"
        if kind == "none":
            continue
        color = nxt["fields"].get("scene_color", "#F4EFE6")
        b = round(f["span"][1], 3)
        ox, oy = (map(int, spec_t[1].split(",")) if len(spec_t) > 1 and "," in spec_t[1] else (W // 2, H // 2))
        tid = f"tr{i+1}"
        if kind == "iris":
            r = int(((max(ox, W - ox)) ** 2 + (max(oy, H - oy)) ** 2) ** 0.5) + 40
            html_parts.append(f'<svg class="tr-svg" id="{tid}" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><mask id="{tid}_m">'
                              f'<rect width="{W}" height="{H}" fill="white"/><circle id="{tid}_hole" cx="{ox}" cy="{oy}" r="{r}" fill="black"/></mask></defs>'
                              f'<rect width="{W}" height="{H}" fill="{color}" mask="url(#{tid}_m)"/></svg>')
            it_r = r
        elif kind == "blinds":
            n = 8
            bw = W / n
            bars = "".join(f'<div class="tr-bar {tid}-bar" style="left:{round(k*bw)}px;width:{round(bw)+2}px;background:{color}"></div>' for k in range(n))
            html_parts.append(f'<div class="tr-wrap" id="{tid}">{bars}</div>')
        elif kind == "stripes":
            n = 6
            sh = H / n
            bars = "".join(f'<div class="tr-row {tid}-row" style="top:{round(k*sh)}px;height:{round(sh)+2}px;background:{color}"></div>' for k in range(n))
            html_parts.append(f'<div class="tr-wrap" id="{tid}">{bars}</div>')
        elif kind == "wipe":
            html_parts.append(f'<div class="tr-wipe" id="{tid}" style="background:{color}"></div>')
        elif kind == "rings":
            r = int(((max(ox, W - ox)) ** 2 + (max(oy, H - oy)) ** 2) ** 0.5) + 40
            cols = [c for c in ring_pool if c.lower() != color.lower()][:2] or ["#FFE13A", "#23268C"]
            circles = "".join(f'<circle class="{tid}-ring" cx="{ox}" cy="{oy}" r="{r}" fill="{c}"/>' for c in [*cols, color])
            html_parts.append(f'<svg class="tr-svg" id="{tid}" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><mask id="{tid}_m">'
                              f'<rect width="{W}" height="{H}" fill="white"/><circle id="{tid}_hole" cx="{ox}" cy="{oy}" r="0" fill="black"/></mask></defs>'
                              f'<g mask="url(#{tid}_m)">{circles}</g></svg>')
            it_r = r
        elif kind == "tear":
            html_parts.append(torn_sheet(tid, color, W, H, i))
        elif kind == "paper":
            html_parts.append(f'<div class="tr-sheet" id="{tid}" style="background:{color}"></div>')
        else:
            sys.exit(f"✗ unknown transition kind '{kind}' in frame {f['id']}")
        items.append({"id": tid, "kind": kind, "b": b, "r": locals().get("it_r", 0)})

    js = []
    if texture == "grain":
        steps = int(D * 8)   # 8 fps "boil" — enough to read as film/paper, cheap enough to encode
        offs = [((k * 97) % 384, (k * 61) % 384) for k in range(steps)]
        js.append("var G=" + json.dumps(offs) + ";for(var k=0;k<G.length;k++){tl.set('#tr_grain',{backgroundPosition:G[k][0]+'px '+G[k][1]+'px'},k/8);}")
    for it in items:
        tid, b, k = it["id"], it["b"], it["kind"]
        c0, c1, r0, r1 = b - HOLD - COVER, b - HOLD, b + HOLD, b + HOLD + REVEAL
        if k == "iris":
            R = it["r"]
            js += [f'tl.set("#{tid}",{{autoAlpha:0}},0);',
                   f'tl.set("#{tid}",{{autoAlpha:1}},{c0:.3f});',
                   f'tl.fromTo("#{tid}_hole",{{attr:{{r:{R}}}}},{{attr:{{r:0}},duration:{COVER},ease:"power3.in",immediateRender:false}},{c0:.3f});',
                   f'tl.to("#{tid}_hole",{{attr:{{r:{R}}},duration:{REVEAL},ease:"power3.out"}},{r0:.3f});',
                   f'tl.set("#{tid}",{{autoAlpha:0}},{r1:.3f});']
        elif k == "blinds":
            js += [f'tl.set(".{tid}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},0);',
                   f'tl.to(".{tid}-bar",{{scaleX:1,duration:{COVER*0.7:.3f},ease:"power2.in",stagger:{COVER*0.3/7:.4f}}},{c0:.3f});',
                   f'tl.set(".{tid}-bar",{{transformOrigin:"100% 50%"}},{r0:.3f});',
                   f'tl.to(".{tid}-bar",{{scaleX:0,duration:{REVEAL*0.7:.3f},ease:"power2.out",stagger:{REVEAL*0.3/7:.4f}}},{r0:.3f});']
        elif k == "stripes":
            js += [f'tl.set(".{tid}-row",{{x:-{W}}},0);',
                   f'tl.to(".{tid}-row",{{x:0,duration:{COVER*0.7:.3f},ease:"power3.in",stagger:{COVER*0.3/5:.4f}}},{c0:.3f});',
                   f'tl.to(".{tid}-row",{{x:{W},duration:{REVEAL*0.7:.3f},ease:"power3.out",stagger:{REVEAL*0.3/5:.4f}}},{r0:.3f});']
        elif k == "rings":
            R = it["r"]
            rc0 = c0 - 0.16   # rings need a little longer than a flat cover
            js += [f'tl.set("#{tid}",{{autoAlpha:0}},0);',
                   f'tl.set(".{tid}-ring",{{attr:{{r:0}}}},0);',
                   f'tl.set("#{tid}",{{autoAlpha:1}},{rc0:.3f});',
                   f'tl.to(".{tid}-ring",{{attr:{{r:{R}}},duration:{COVER + 0.04:.3f},ease:"power3.inOut",stagger:0.07}},{rc0:.3f});',
                   f'tl.fromTo("#{tid}_hole",{{attr:{{r:0}}}},{{attr:{{r:{R}}},duration:{REVEAL + 0.05:.3f},ease:"power3.out",immediateRender:false}},{r0:.3f});',
                   f'tl.set("#{tid}",{{autoAlpha:0}},{r1 + 0.06:.3f});']
        elif k == "tear":
            js += [f'tl.set("#{tid}",{{x:{W + 120}}},0);',
                   f'tl.to("#{tid}",{{x:-{int(W*0.1)},duration:{COVER + 0.04:.3f},ease:"power3.in"}},{c0 - 0.04:.3f});',
                   f'tl.to("#{tid}",{{x:-{int(W*1.45) + 120},duration:{REVEAL + 0.06:.3f},ease:"power3.out"}},{r0:.3f});']
        elif k == "paper":
            js += [f'tl.set("#{tid}",{{x:{int(W*0.7)},y:{int(H*0.9)},rotation:14,autoAlpha:0}},0);',
                   f'tl.set("#{tid}",{{autoAlpha:1}},{c0 - 0.04:.3f});',
                   f'tl.to("#{tid}",{{x:0,y:0,rotation:0,duration:{COVER + 0.04:.3f},ease:"power3.in"}},{c0 - 0.04:.3f});',
                   f'tl.to("#{tid}",{{x:-{int(W*0.9)},y:-{int(H*0.75)},rotation:-12,duration:{REVEAL + 0.06:.3f},ease:"power3.in"}},{r0:.3f});',
                   f'tl.set("#{tid}",{{autoAlpha:0}},{r1 + 0.08:.3f});']
        elif k == "wipe":
            off = int(W * 1.25) + 360
            js += [f'tl.set("#{tid}",{{x:-{off}}},0);',
                   f'tl.to("#{tid}",{{x:-{int(W*0.12)},duration:{COVER},ease:"power3.in"}},{c0:.3f});',
                   f'tl.to("#{tid}",{{x:{W + 360},duration:{REVEAL},ease:"power3.out"}},{r0:.3f});']

    html = f'''<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /><!-- Generated by goldenrabbit-promo/scripts/make_transitions.py — re-run, don't hand-edit. --></head>
  <body>
    <template>
      <style>
        #stage {{ position: absolute; inset: 0; width: {W}px; height: {H}px; overflow: hidden; pointer-events: none; background: transparent; }}
        #tr_grain {{ position: absolute; inset: 0; background-image: url("assets/textures/grain.png"); background-size: 384px 384px; mix-blend-mode: multiply; opacity: 0.10; z-index: 5; }}
        .tr-iris {{ position: absolute; border-radius: 50%; transform: scale(0); }}
        .tr-wrap {{ position: absolute; inset: 0; }}
        .tr-bar {{ position: absolute; top: 0; height: {H}px; transform: scaleX(0); }}
        .tr-row {{ position: absolute; left: 0; width: {W}px; transform: translateX(-{W}px); }}
        .tr-wipe {{ position: absolute; top: -{H//4}px; left: 0; width: {int(W*1.25)}px; height: {int(H*1.5)}px; transform: translateX(-{int(W*1.25)+360}px) skewX(-12deg); }}
        .tr-svg {{ position: absolute; left: 0; top: 0; }}
        #tr_paper {{ position: absolute; inset: 0; background-image: url("assets/textures/paper.png"); background-size: 512px 512px; opacity: 0.5; z-index: 5; }}
        .tr-torn {{ position: absolute; top: -40px; left: 0; width: {int(W*1.45)}px; height: {H + 80}px; filter: drop-shadow(0 12px 22px rgba(60,40,10,.28)); }}
        .tr-sheet {{ position: absolute; left: -{int(W*0.06)}px; top: -{int(H*0.08)}px; width: {int(W*1.12)}px; height: {int(H*1.16)}px; box-shadow: 0 30px 60px rgba(60,40,10,.30), 0 4px 0 rgba(0,0,0,.06); }}
      </style>
      <div id="stage" data-composition-id="transitions" data-width="{W}" data-height="{H}" data-duration="{D}" data-layout-ignore="">
        {"".join(html_parts)}
      </div>
      <script>
        (function () {{
          var tl = gsap.timeline({{ paused: true }});
          {chr(10).join("          " + s for s in js).strip()}
          tl.set({{}}, {{}}, {D});
          tl.seek(0);
          window.__timelines = window.__timelines || {{}};
          window.__timelines["transitions"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''
    out = proj / "compositions" / "transitions.html"
    out.write_text(html)
    print(f"✓ {out} · {len(items)} transitions: " + ", ".join(f"{it['kind']}@{it['b']}" for it in items))
    return items


if __name__ == "__main__":
    main()
