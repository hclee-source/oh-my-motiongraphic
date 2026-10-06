#!/usr/bin/env python3
"""Generate the two orchestrator-owned layers of the MV from .work/sky_plan.json:

  compositions/sky.html      track 0, under every frame: sky gradients, 3-depth star field (deterministic LCG),
                             slow celestial rotation, hill silhouette + camera tilt, horizon bloom.
  compositions/overlay.html  track 3, over every frame: soft vignette + coarse film grain (8 fps jitter).

Every value is derived from the plan + indices (no Math.random); one paused GSAP timeline per layer.
Re-run after editing sky_plan.json; never hand-edit the generated HTML.
"""
import json, math, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
plan = json.loads((PROJ / ".work" / "sky_plan.json").read_text())
DUR = plan["duration"]
W, H = 1920, 1080

# ---------- sky gradient presets ----------
SKIES = {
    "black":  "#000000",
    "verse":  "radial-gradient(120% 60% at 50% 108%, rgba(44,90,122,.55) 0%, rgba(44,90,122,0) 60%), linear-gradient(180deg, #03050F 0%, #0B1230 58%, #18264F 100%)",
    "pre":    "radial-gradient(120% 65% at 50% 110%, rgba(86,74,150,.55) 0%, rgba(86,74,150,0) 62%), linear-gradient(180deg, #040616 0%, #10173C 55%, #24275C 100%)",
    "chorus": "radial-gradient(130% 75% at 50% 112%, rgba(120,92,190,.70) 0%, rgba(59,47,110,.35) 40%, rgba(59,47,110,0) 70%), linear-gradient(180deg, #070A26 0%, #1B1F4E 52%, #3B2F6E 100%)",
    "warm":   "radial-gradient(80% 60% at 82% 100%, rgba(255,180,92,.22) 0%, rgba(255,180,92,0) 60%), radial-gradient(120% 60% at 50% 108%, rgba(44,90,122,.40) 0%, rgba(44,90,122,0) 60%), linear-gradient(180deg, #03050F 0%, #0C1331 58%, #1B2550 100%)",
    "bridge": "radial-gradient(70% 50% at 50% 62%, rgba(255,210,122,.07) 0%, rgba(255,210,122,0) 70%), linear-gradient(180deg, #020309 0%, #05060F 60%, #0A0D1F 100%)",
    "build":  "radial-gradient(90% 70% at 50% 64%, rgba(255,210,122,.20) 0%, rgba(255,210,122,0) 70%), linear-gradient(180deg, #03040D 0%, #0B0F2A 60%, #1A1B44 100%)",
    "final":  "radial-gradient(140% 55% at 50% 112%, rgba(255,200,154,.85) 0%, rgba(242,163,160,.55) 30%, rgba(120,92,190,.25) 60%, rgba(120,92,190,0) 80%), linear-gradient(180deg, #0A0E36 0%, #22265E 45%, #4A3A7E 78%, #8A5A8A 100%)",
    "outro":  "radial-gradient(140% 60% at 50% 115%, rgba(255,214,190,.55) 0%, rgba(175,192,234,.35) 40%, rgba(175,192,234,0) 75%), linear-gradient(180deg, #121A40 0%, #2E3A72 50%, #6878B0 85%, #9AA9D8 100%)",
}

# ---------- deterministic star field ----------
class LCG:
    def __init__(self, seed): self.s = seed & 0xFFFFFFFF
    def next(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s / 2**32

FIELD_X0, FIELD_Y0, FIELD_W, FIELD_H = -360, -420, 2640, 1700   # larger than the frame: rotation + tilt never expose an edge
LAYERS = [  # name, count, size range, base alpha range, glow
    ("far", 280, (1.0, 1.8), (0.35, 0.80), False),
    ("mid", 110, (1.8, 2.7), (0.60, 0.95), False),
    ("near", 30, (2.8, 4.2), (0.85, 1.00), True),
]
rng = LCG(20261003)
stars = []
for li, (name, n, (smin, smax), (amin, amax), glow) in enumerate(LAYERS):
    for i in range(n):
        x = FIELD_X0 + rng.next() * FIELD_W
        # denser toward the top of the sky
        yy = rng.next() ** 1.35
        y = FIELD_Y0 + yy * FIELD_H
        s = smin + rng.next() * (smax - smin)
        a = amin + rng.next() * (amax - amin)
        warm = rng.next()
        col = "#FFF4D6" if warm < 0.55 else ("#DCEBFF" if warm < 0.9 else "#FFD27A")
        tw = 1.3 + rng.next() * 2.9      # twinkle half-period
        ph = rng.next() * tw             # phase
        stars.append(dict(layer=name, i=i, x=round(x, 1), y=round(y, 1), s=round(s, 2), a=round(a, 2), c=col, glow=glow,
                          tw=round(tw, 2), ph=round(ph, 2)))

def star_html(st):
    sid = f"sky_{st['layer']}{st['i']}"
    shadow = f"box-shadow:0 0 {st['s']*3:.1f}px {st['s']*0.9:.1f}px rgba(255,236,190,.55);" if st["glow"] else ""
    return (f'<i id="{sid}" class="sky-star sky-{st["layer"]}" style="left:{st["x"]}px;top:{st["y"]}px;'
            f'width:{st["s"]}px;height:{st["s"]}px;background:{st["c"]};opacity:{st["a"]};{shadow}"></i>')

# hill silhouette (two overlapping ridges) — 1920 wide, drawn in a 2200-wide svg for tilt safety
HILL = """<svg id="sky_hill" width="2200" height="420" viewBox="0 0 2200 420" style="position:absolute;left:-140px;top:{top}px">
  <defs><linearGradient id="sky_hillgrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A1028"/><stop offset="1" stop-color="#03050C"/></linearGradient></defs>
  <path d="M0 250 C 260 205, 520 170, 820 182 C 1060 192, 1240 238, 1480 228 C 1720 218, 1960 168, 2200 186 L2200 420 L0 420 Z" fill="#070C20" opacity="0.85"/>
  <path d="M0 300 C 300 286, 560 232, 900 214 C 1180 200, 1420 236, 1700 262 C 1900 280, 2060 286, 2200 282 L2200 420 L0 420 Z" fill="url(#sky_hillgrad)"/>
  <path d="M0 300 C 300 286, 560 232, 900 214 C 1180 200, 1420 236, 1700 262 C 1900 280, 2060 286, 2200 282" fill="none" stroke="#9FB6E8" stroke-opacity="0.22" stroke-width="2"/>
</svg>"""

def fmt(v): return f"{v:.3f}"

# ---------- timeline JS ----------
js = []
J = js.append
secs = plan["sections"]
INIT = {}   # element id -> inline initial style (initial states live in markup, not tl.set at 0)
sky_names = sorted({s["sky"] for s in secs} - {"black"})   # "black" = no gradient layer (stage bg is #000)
first = secs[0]["sky"]
for nm in sky_names:
    INIT[f"sky_g_{nm}"] = f"opacity:{1 if nm == first else 0}"
prev = first
for s in secs[1:]:
    if s["sky"] != prev:
        f = s.get("fade", 2.0)
        t0 = s["start"] if s.get("align") == "start" else s["start"] - (f * 0.5 if f > 0 else 0)
        if prev != "black":
            J(f'tl.to("#sky_g_{prev}",{{opacity:0,duration:{max(f,0.01)},ease:"sine.inOut"}},{fmt(t0)});')
        if s["sky"] != "black":
            J(f'tl.to("#sky_g_{s["sky"]}",{{opacity:1,duration:{max(f,0.01)},ease:"sine.inOut"}},{fmt(t0)});')
        prev = s["sky"]

# star layer levels per section (only tween on change)
lv = dict(secs[0]["stars"])
for ln in ("far", "mid", "near"):
    INIT[f"sky_L_{ln}"] = f"opacity:{lv[ln]}"
for s in secs[1:]:
    f = s.get("fade", 2.0)
    for ln in ("far", "mid", "near"):
        if s["stars"][ln] != lv[ln]:
            J(f'tl.to("#sky_L_{ln}",{{opacity:{s["stars"][ln]},duration:{max(f,0.01)},ease:"sine.inOut"}},{fmt(s["start"] - f*0.5)});')
            lv[ln] = s["stars"][ln]

# milky-way band level per section (only tween on change)
mk = secs[0].get("milky", 0)
INIT["sky_milky"] = f"opacity:{mk}"
for s_ in secs[1:]:
    f = s_.get("fade", 2.0)
    if s_.get("milky", 0) != mk:
        J(f'tl.to("#sky_milky",{{opacity:{s_.get("milky",0)},duration:{max(f,0.01)},ease:"sine.inOut"}},{fmt(s_["start"] - (0 if s_.get("align")=="start" else f*0.5))});')
        mk = s_.get("milky", 0)

# intro star switch-on: per-star pop on given hit times (star groups by index modulo)
for k, ev in enumerate(plan.get("star_pops", [])):
    t, ln, frac = ev["t"], ev["layer"], ev["frac"]
    J(f'tl.fromTo(".sky-{ln}.pop{k}",{{scale:0}},{{scale:1,duration:0.35,ease:"back.out(3)",stagger:{{each:0.004}}}},{fmt(t)});')

# twinkle: deterministic yoyo per star, finite repeats covering the duration
for st in stars:
    rep = int(math.ceil((DUR + 2) / st["tw"]))
    lo = round(st["a"] * (0.28 if st["layer"] != "near" else 0.55), 2)
    J(f'tl.fromTo("#sky_{st["layer"]}{st["i"]}",{{opacity:{st["a"]}}},{{opacity:{lo},duration:{st["tw"]},ease:"sine.inOut",yoyo:true,repeat:{rep},immediateRender:false}},{st["ph"]});')

# celestial rotation over the whole song (pivot = an off-screen pole up-right)
J(f'tl.fromTo("#sky_field",{{rotation:0}},{{rotation:{plan.get("rotation_deg", 6)},duration:{DUR},ease:"none"}},0);')

# camera: hill + field offsets per section (only tween on change; never overlap)
cam = dict(secs[0]["camera"])
INIT["sky_hillwrap"] = ""
INIT["sky_tilt"] = ""
PRESET = [f'gsap.set("#sky_hillwrap",{{y:{cam["hill"]}}});', f'gsap.set("#sky_tilt",{{y:{cam["field"]}}});']
for s in secs[1:]:
    c = s["camera"]; f = s.get("tilt", 2.6)
    for key, el in (("hill", "sky_hillwrap"), ("field", "sky_tilt")):
        if c[key] != cam[key]:
            J(f'tl.to("#{el}",{{y:{c[key]},duration:{f},ease:"power2.inOut"}},{fmt(s["start"] - f*0.35)});')
            cam[key] = c[key]

# horizon bloom breathing (slow), its color follows the sky gradients already
J(f'tl.fromTo("#sky_bloom",{{opacity:0.0}},{{opacity:0.55,duration:7.5,ease:"sine.inOut",yoyo:true,repeat:{int(DUR/7.5)+1},immediateRender:false}},0);')

# final black-out (outro end)
if plan.get("fade_out"):
    fo = plan["fade_out"]
    J(f'tl.to("#sky_black_out",{{opacity:1,duration:{fo["dur"]},ease:"sine.in"}},{fmt(fo["start"])});')
J(f'tl.set({{}},{{}},{DUR});')

# assign pop classes
pops = plan.get("star_pops", [])
pop_cls = {}
for k, ev in enumerate(pops):
    ln = ev["layer"]
    ids = [st for st in stars if st["layer"] == ln]
    lo = int(len(ids) * ev["frac_from"]); hi = int(len(ids) * ev["frac"])
    for st in ids[lo:hi]:
        pop_cls[(ln, st["i"])] = f"pop{k}"

def star_html2(st):
    h = star_html(st)
    k = pop_cls.get((st["layer"], st["i"]))
    if k:
        h = h.replace(f'class="sky-star sky-{st["layer"]}"', f'class="sky-star sky-{st["layer"]} {k}"')
    return h

layers_html = "".join(
    f'<div id="sky_L_{ln}" class="sky-layer" style="{INIT[f"sky_L_{ln}"]}">' + "".join(star_html2(st) for st in stars if st["layer"] == ln) + "</div>"
    for ln in ("far", "mid", "near"))
skies_html = "".join(f'<div id="sky_g_{nm}" class="sky-g" style="background:{SKIES[nm]};{INIT[f"sky_g_{nm}"]}"></div>' for nm in sky_names)

sky = f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /><!-- Generated by .work/make_sky.py from .work/sky_plan.json — re-run, don't hand-edit. --></head>
  <body>
    <template>
      <style>
        #stage {{ position: absolute; inset: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
        .sky-g {{ position: absolute; inset: 0; }}
        #sky_tilt {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
        #sky_field {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; transform-origin: 1500px -700px; }}
        .sky-layer {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
        .sky-star {{ position: absolute; display: block; border-radius: 50%; }}
        #sky_bloom {{ position: absolute; left: -10%; right: -10%; bottom: -30%; height: 70%;
                      background: radial-gradient(50% 50% at 50% 50%, rgba(160,140,230,.35) 0%, rgba(160,140,230,0) 70%); }}
        #sky_milky {{ position: absolute; left: -500px; top: 140px; width: 2900px; height: 520px; transform: rotate(-18deg);
                      background: radial-gradient(50% 50% at 50% 50%, rgba(214,206,255,.16) 0%, rgba(190,180,255,.07) 45%, rgba(190,180,255,0) 72%);
                      filter: blur(6px); }}
        #sky_hillwrap {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
        #sky_black_out {{ position: absolute; inset: 0; background: #000; opacity: 0; }}
      </style>
      <div id="stage" data-composition-id="sky" data-width="{W}" data-height="{H}" data-duration="{DUR}" data-layout-ignore="">
        {skies_html}
        <div id="sky_bloom"></div>
        <div id="sky_tilt" style="{INIT['sky_tilt']}"><div id="sky_field"><div id="sky_milky" style="{INIT['sky_milky']}"></div>{layers_html}</div></div>
        <div id="sky_hillwrap" style="{INIT['sky_hillwrap']}">{HILL.format(top=H - 300)}</div>
        <div id="sky_black_out"></div>
      </div>
      <script>
        (function () {{
          {" ".join(PRESET)}
          var tl = gsap.timeline({{ paused: true }});
          {chr(10).join('          ' + l for l in js).lstrip()}
          tl.seek(0);
          window.__timelines = window.__timelines || {{}};
          window.__timelines["sky"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
(PROJ / "compositions").mkdir(exist_ok=True)
(PROJ / "compositions" / "sky.html").write_text(sky)

# ---------- overlay: vignette + grain ----------
grng = LCG(7)
offs = [[int(grng.next() * 384), int(grng.next() * 384)] for _ in range(int(DUR * 8) + 2)]
overlay = f"""<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /><!-- Generated by .work/make_sky.py — re-run, don't hand-edit. --></head>
  <body>
    <template>
      <style>
        #stage {{ position: absolute; inset: 0; width: {W}px; height: {H}px; overflow: hidden; pointer-events: none; background: transparent; }}
        #ov_vig {{ position: absolute; inset: 0; background: radial-gradient(120% 95% at 50% 46%, rgba(0,0,0,0) 55%, rgba(0,0,0,.42) 100%); }}
        #ov_grain {{ position: absolute; inset: 0; background-image: url("assets/textures/grain.png"); background-size: 384px 384px; mix-blend-mode: screen; opacity: 0.07; }}
      </style>
      <div id="stage" data-composition-id="overlay" data-width="{W}" data-height="{H}" data-duration="{DUR}" data-layout-ignore="">
        <div id="ov_vig"></div><div id="ov_grain"></div>
      </div>
      <script>
        (function () {{
          var tl = gsap.timeline({{ paused: true }});
          var G={json.dumps(offs)};for(var k=0;k<G.length;k++){{tl.set('#ov_grain',{{backgroundPosition:G[k][0]+'px '+G[k][1]+'px'}},k/8);}}
          tl.set({{}},{{}},{DUR});
          tl.seek(0);
          window.__timelines = window.__timelines || {{}};
          window.__timelines["overlay"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
(PROJ / "compositions" / "overlay.html").write_text(overlay)
print("sky.html:", len(sky) // 1024, "KB,", len(js), "timeline lines;  overlay.html:", len(overlay) // 1024, "KB")
