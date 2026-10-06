#!/usr/bin/env python3
"""Generate compositions/frames/07-f7.html (chorus 2 — the bottle constellation forms)."""
import json, math

OUT = "/Users/canine89/Documents/dev/oh-my-motiongraphic/videos/glass-bottle-constellation-mv/compositions/frames/07-f7.html"
SPARK = "M0,-1 C0.1,-0.1 0.1,-0.1 1,0 C0.1,0.1 0.1,0.1 0,1 C-0.1,0.1 -0.1,0.1 -1,0 C-0.1,-0.1 -0.1,-0.1 0,-1 Z"

# ---------------- constellation (frame.md motifs.bottle-constellation) ----------------
# k, x, y, ignite(local s), big, detach(local s), fall dur, fall dist
NODES = [
    ("A", 960, 150, 2.98, 1, 26.90, 1.05, 1300),
    ("B", 902, 250, 3.98, 0, 31.13, 0.60, 800),
    ("C", 1018, 250, 4.80, 0, 30.48, 0.80, 1000),
    ("D", 760, 400, 5.92, 0, 31.45, 0.50, 650),
    ("E", 1160, 400, 7.88, 0, 30.80, 0.72, 950),
    ("F", 690, 620, 8.68, 1, 31.78, 0.22, 330),
    ("G", 1230, 620, 9.05, 1, 31.47, 0.48, 650),
    ("H", 800, 870, 9.96, 0, 31.80, 0.20, 300),
    ("I", 1120, 870, 10.48, 0, 31.79, 0.21, 320),
]
NODE = {n[0]: n for n in NODES}
# edge, draw start, draw dur (each edge arrives at its target node's ignition)
EDGES = [
    ("A", "B", 3.38, 0.60), ("A", "C", 4.20, 0.60), ("B", "D", 5.32, 0.60), ("C", "E", 7.28, 0.60),
    ("D", "F", 8.08, 0.60), ("E", "G", 8.45, 0.60), ("F", "H", 9.36, 0.60), ("G", "I", 9.88, 0.60),
    ("H", "I", 9.96, 0.52),
]


def short(p, q, g=15.0):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    return (p[0] + dx * g / L, p[1] + dy * g / L), (q[0] - dx * g / L, q[1] - dy * g / L)


edge_rows = []
edge_js = []
for a, b, t0, d in EDGES:
    p, q = short(NODE[a][1:3], NODE[b][1:3])
    dpath = f"M{p[0]:.1f} {p[1]:.1f} L{q[0]:.1f} {q[1]:.1f}"
    eid = f"f7_e_{a}{b}"
    edge_rows.append(
        f'          <g id="{eid}">'
        f'<path class="f7-eglow" d="{dpath}" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000"/>'
        f'<path class="f7-ecore" d="{dpath}" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000"/></g>'
    )
    fade_t = min(NODE[a][5], NODE[b][5])
    fade_d = 0.35 if fade_t < 30 else (0.3 if fade_t < 31.3 else 0.2)
    edge_js.append([eid, t0, d, round(fade_t, 3), fade_d])

node_rows = []
node_js = []
for i, (k, x, y, t, big, td, fd, fdist) in enumerate(NODES):
    hs = 150 if big else 120  # halo size
    sc = 18 if big else 14  # sparkle scale
    parts = "".join(f'<div class="f7-pp" id="f7_pp_{k}{j}"></div>' for j in range(6))
    node_rows.append(
        f'        <div class="f7-node" id="f7_n_{k}" style="left:{x}px;top:{y}px" data-layout-ignore>'
        f'{parts}'
        f'<div class="f7-node-pop" id="f7_np_{k}"><div class="f7-node-tw" id="f7_nt_{k}">'
        f'<div class="f7-halo" id="f7_nh_{k}" style="left:{75 - hs / 2:.0f}px;top:{75 - hs / 2:.0f}px;width:{hs}px;height:{hs}px"></div>'
        f'<svg class="f7-spk" viewBox="-24 -24 48 48" width="48" height="48"><path d="{SPARK}" transform="scale({sc})" fill="#FFF4D6"/></svg>'
        f'</div></div></div>'
    )
    node_js.append([k, x, y, t, td, fd, fdist, i])

# falling stars (screen-space layer, positioned by JS at build time from the camera math)
fall_rows = []
for k, *_ in NODES:
    fall_rows.append(
        f'        <div class="f7-fs" id="f7_fs_{k}"><div class="f7-fs-rot">'
        f'<div class="f7-fs-tail" id="f7_ft_{k}"></div><div class="f7-fs-head"></div></div></div>'
    )

# ---------------- slam burst (particle-burst primitive, sparkles) ----------------
s = 20261003


def rnd():
    global s
    s = (1664525 * s + 1013904223) & 0xFFFFFFFF
    return s / 4294967296.0


burst_rows = []
burst_js = []
N = 20
for i in range(N):
    x0 = 670 + (i + rnd() * 0.8) / N * 580
    y0 = 420 + rnd() * 120
    ang = math.atan2((y0 - 480) * 1.0, (x0 - 960) * 0.55) + (rnd() - 0.5) * 0.5
    dist = 230 + rnd() * 300
    dx, dy = math.cos(ang) * dist, math.sin(ang) * dist * 0.9
    if dy > 0:  # keep the lower sparkles off the sub line (저 하늘 너머로)
        dy *= 0.3
        dx *= 1.35
    sc = 0.55 + rnd() * 0.65
    dur = 0.95 + rnd() * 0.55
    burst_rows.append(
        f'        <div class="f7-bs" id="f7_bs{i}" style="left:{x0 - 22:.0f}px;top:{y0 - 22:.0f}px">'
        f'<svg viewBox="-22 -22 44 44" width="44" height="44"><path d="{SPARK}" transform="scale(13)" fill="#FFF4D6"/></svg></div>'
    )
    burst_js.append([round(dx, 1), round(dy, 1), round(sc, 2), round(dur, 2)])

# ---------------- lyric rows (frame-local layout, inside the constellation) ----------------
KW = lambda kid, txt: f'<span class="f7-kw" id="{kid}">{txt}</span>'
LYR = [
    # id, extra class, row height, [(center_y, html)]
    ("f7_l22", "", 100, [(536, "숨겨 둔"), (644, KW("f7_kw22", "별") + "들이"), (760, "흘러가")]),
    ("f7_l23", "", 116, [(530, "입술 끝에"), (652, "머문 " + KW("f7_kw23", "빛") + "들이")]),
    ("f7_l24", "", 132, [(585, '<span class="f7-hero" id="f7_kw24">별자리가</span>'), (735, "되어 가")]),
    ("f7_l25", "f7-whisper", 70, [(600, "괜찮아"), (688, "너는 몰라도 돼")]),
    ("f7_l26", "", 116, [(590, "이 " + KW("f7_kw26", "밤") + "이 대신"), (716, "기억할 테니")]),
    ("f7_l27", "", 100, [(600, "언젠가 고개"), (702, "들어 본다면")]),
    ("f7_l28", "f7-held", 120, [(585, "그거면"), (700, '<span class="f7-w28" id="f7_w28">충분해</span>')]),
]
lyr_rows = []
for lid, cls, h, rows in LYR:
    inner = "".join(
        f'<div class="{("f7-row " + cls).strip()}" style="top:{cy - h / 2:.0f}px;height:{h}px;line-height:{h}px">{html}</div>'
        for cy, html in rows
    )
    lyr_rows.append(f'        <div class="f7-line" id="{lid}" data-layout-allow-overlap>{inner}</div>')

HTML = f'''<!doctype html>
<html lang="ko">
  <head><meta charset="UTF-8" /><!-- Frame 7 — chorus 2: the glass-bottle constellation forms (track 86.55–118.6). Generated by .work/gen_f7.py — re-run, don't hand-edit. --></head>
  <body>
    <template>
      <style>
        @font-face {{ font-family: "Noto Serif KR"; src: url("assets/fonts/NotoSerifKR-VF.woff2") format("woff2"); font-weight: 200 900; font-style: normal; font-display: block; }}
        @font-face {{ font-family: "Cormorant Garamond"; src: url("assets/fonts/CormorantGaramond-Italic-VF.woff2") format("woff2"); font-weight: 300 700; font-style: italic; font-display: block; }}
        #stage {{ position: absolute; inset: 0; width: 1920px; height: 1080px; overflow: hidden; background: transparent; }}
        #f7_g1 {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
        .f7-layer {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
        #f7_cam, #f7_drift {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
        .f7-inglow {{ position: absolute; left: 650px; top: 330px; width: 620px; height: 580px; border-radius: 50%;
          background: radial-gradient(closest-side, rgba(255,210,122,0.09) 0%, rgba(255,210,122,0.045) 45%, rgba(255,210,122,0) 100%); }}
        .f7-edges {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; }}
        .f7-eglow {{ fill: none; stroke: #DCEBFF; stroke-width: 6; stroke-opacity: 0.13; stroke-linecap: butt; }}
        .f7-ecore {{ fill: none; stroke: #DCEBFF; stroke-width: 1.6; stroke-linecap: butt; }}
        .f7-node {{ position: absolute; width: 0; height: 0; }}
        .f7-node-pop {{ position: absolute; left: -75px; top: -75px; width: 150px; height: 150px; }}
        .f7-node-tw {{ position: absolute; left: 0; top: 0; width: 150px; height: 150px; }}
        .f7-halo {{ position: absolute; border-radius: 50%;
          background: radial-gradient(closest-side, rgba(255,244,214,0.95) 0%, rgba(255,232,170,0.55) 12%, rgba(255,210,122,0.22) 30%, rgba(255,210,122,0.07) 58%, rgba(255,210,122,0) 100%); }}
        .f7-spk {{ position: absolute; left: 51px; top: 51px; width: 48px; height: 48px; overflow: visible; }}
        .f7-pp {{ position: absolute; left: -2.5px; top: -2.5px; width: 5px; height: 5px; border-radius: 50%; background: #FFF4D6;
          box-shadow: 0 0 8px 2px rgba(255,210,122,0.65); opacity: 0; }}
        .f7-line {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; opacity: 0; }}
        .f7-row {{ position: absolute; left: 50%; transform: translateX(-50%); white-space: nowrap; text-align: center;
          font-family: "Noto Serif KR"; font-weight: 500; font-size: 76px; letter-spacing: 0.01em; color: #F4F1EA;
          text-shadow: 0 0 14px rgba(220,235,255,0.25), 0 0 40px rgba(220,235,255,0); }}
        .f7-kw {{ display: inline-block; font-size: 1.4em; font-weight: 600; line-height: 1; color: #FFD27A;
          text-shadow: 0 0 18px rgba(255,210,122,0.45), 0 0 46px rgba(255,210,122,0.18); }}
        .f7-hero {{ display: inline-block; font-size: 118px; font-weight: 700; line-height: 1; letter-spacing: -0.01em; color: #FFD27A;
          text-shadow: 0 0 18px rgba(255,210,122,0.45), 0 0 46px rgba(255,210,122,0.18); }}
        .f7-whisper {{ font-size: 52px; font-weight: 300; letter-spacing: 0.12em; color: #A9B3D6;
          text-shadow: 0 0 14px rgba(220,235,255,0.18), 0 0 40px rgba(220,235,255,0); }}
        .f7-held {{ font-size: 96px; font-weight: 500; letter-spacing: 0.02em; }}
        .f7-w28 {{ display: inline-block; }}
        .f7-mega-wrap {{ position: absolute; left: 0; top: 370px; width: 1920px; height: 220px; text-align: center; }}
        .f7-mega-punch {{ position: relative; display: inline-block; font-family: "Noto Serif KR"; font-weight: 800; font-size: 220px;
          line-height: 220px; letter-spacing: -0.02em; white-space: nowrap; }}
        .f7-mega-stroke {{ display: block; color: transparent; -webkit-text-stroke: 2px #FFF4D6; text-shadow: 0 0 22px rgba(255,244,214,0.22); opacity: 0; }}
        .f7-mega-fill {{ position: absolute; left: 0; top: 0; display: block; color: #FFF4D6; opacity: 0; }}
        .f7-bs {{ position: absolute; width: 44px; height: 44px; border-radius: 50%; opacity: 0;
          background: radial-gradient(closest-side, rgba(255,226,160,0.55) 0%, rgba(255,210,122,0.12) 50%, rgba(255,210,122,0) 100%); }}
        .f7-bs svg {{ position: absolute; left: 0; top: 0; overflow: visible; }}
        .f7-fs {{ position: absolute; width: 0; height: 0; opacity: 0; }}
        .f7-fs-rot {{ position: absolute; left: 0; top: 0; width: 0; height: 0; transform: rotate(124deg); }}
        .f7-fs-tail {{ position: absolute; left: -260px; top: -1.5px; width: 260px; height: 3px; border-radius: 2px;
          background: linear-gradient(to right, rgba(255,244,214,0) 0%, rgba(255,232,180,0.35) 55%, rgba(255,244,214,0.95) 100%); }}
        .f7-fs-head {{ position: absolute; left: -11px; top: -11px; width: 22px; height: 22px; border-radius: 50%;
          background: radial-gradient(closest-side, rgba(255,250,235,1) 0%, rgba(255,244,214,0.9) 22%, rgba(255,210,122,0.35) 55%, rgba(255,210,122,0) 100%); }}
      </style>
      <div id="stage" data-composition-id="07-f7" data-width="1920" data-height="1080" data-duration="32.05">
        <div id="f7_g1">
          <div id="f7_cam">
            <div id="f7_drift">
              <div class="f7-inglow" id="f7_inglow" data-layout-ignore></div>
              <svg class="f7-edges" id="f7_edgesvg" viewBox="0 0 1920 1080" width="1920" height="1080" data-layout-ignore>
                <g id="f7_edges">
{chr(10).join(edge_rows)}
                </g>
              </svg>
{chr(10).join(node_rows)}
{chr(10).join(lyr_rows)}
            </div>
          </div>
          <div class="f7-layer" id="f7_l21">
            <div class="f7-layer" id="f7_burst" data-layout-ignore>
{chr(10).join(burst_rows)}
            </div>
            <div class="f7-mega-wrap" id="f7_mega_wrap"><div class="f7-mega-punch" id="f7_mega_punch"><span class="f7-mega-stroke" id="f7_mega_stroke">빛나라</span><span class="f7-mega-fill" id="f7_mega_fill">빛나라</span></div></div>
            <div class="f7-line" id="f7_l21sub" style="opacity:0"><div class="f7-row" style="top:630px;height:100px;line-height:100px">저 {KW("f7_kw21", "하늘")} 너머로</div></div>
          </div>
          <div class="f7-layer" id="f7_fall" data-layout-ignore>
{chr(10).join(fall_rows)}
          </div>
        </div>
      </div>
      <script>
        (function () {{
          var tl = gsap.timeline({{ paused: true }});
          function $(id) {{ return document.getElementById(id); }}
          var KW_REST = "0 0 18px rgba(255,210,122,0.45), 0 0 46px rgba(255,210,122,0.18)";
          var KW_PEAK = "0 0 26px rgba(255,232,170,0.95), 0 0 72px rgba(255,210,122,0.55)";
          var FILL_PEAK = "0 0 34px rgba(255,236,180,1), 0 0 110px rgba(255,210,122,0.8)";
          var FILL_DOT = "0 0 46px rgba(255,240,200,1), 0 0 140px rgba(255,210,122,0.95)";
          var SOFT = "0 0 14px rgba(220,235,255,0.25), 0 0 40px rgba(220,235,255,0)";
          var WARM = "0 0 18px rgba(255,210,122,0.42), 0 0 46px rgba(255,210,122,0.16)";

          var g1 = $("f7_g1");
          tl.set(g1, {{ autoAlpha: 1 }}, 0);

          function kwPop(el, t) {{
            gsap.set(el, {{ scale: 1, textShadow: KW_REST, transformOrigin: "50% 60%" }});
            tl.to(el, {{ scale: 1.1, textShadow: KW_PEAK, duration: 0.12, ease: "power2.out" }}, t);
            tl.to(el, {{ scale: 1, textShadow: KW_REST, duration: 0.65, ease: "power2.inOut" }}, t + 0.12);
          }}

          // ---------- L21 「빛나라」: outline in the band stop → fills with light on the slam (outline-to-fill) ----------
          var mWrap = $("f7_mega_wrap"), mPunch = $("f7_mega_punch"), mStroke = $("f7_mega_stroke"), mFill = $("f7_mega_fill");
          gsap.set(mWrap, {{ x: 0, y: 0, scale: 1, opacity: 1, transformOrigin: "50% 50%" }});
          gsap.set(mPunch, {{ scale: 1, transformOrigin: "50% 50%" }});
          gsap.set(mStroke, {{ opacity: 0, scale: 1.06, filter: "blur(8px)", transformOrigin: "50% 50%" }});
          gsap.set(mFill, {{ opacity: 0, clipPath: "inset(100% -30% -45% -30%)", textShadow: FILL_PEAK }});
          tl.to(mStroke, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "power2.out" }}, 0.02);
          tl.to(mPunch, {{ scale: 1.025, duration: 0.85, ease: "sine.inOut" }}, 0.36);
          tl.to(mFill, {{ opacity: 1, duration: 0.08, ease: "power2.out" }}, 1.21);
          tl.to(mFill, {{ clipPath: "inset(-45% -30% -45% -30%)", duration: 0.24, ease: "expo.out" }}, 1.21);
          tl.to(mFill, {{ textShadow: KW_REST, duration: 0.9, ease: "power2.out" }}, 1.45);
          tl.to(mPunch, {{ scale: 1.08, duration: 0.06, ease: "power3.out" }}, 1.25);
          tl.to(mPunch, {{ scale: 1, duration: 0.55, ease: "power3.out" }}, 1.31);
          tl.to(mPunch, {{ scale: 1.03, duration: 0.65, ease: "sine.inOut" }}, 1.86);
          tl.to(mStroke, {{ opacity: 0.3, duration: 0.5, ease: "power1.out" }}, 1.4);
          // the word rises into the sky and becomes star A
          tl.to(mStroke, {{ opacity: 0, duration: 0.2, ease: "power1.out" }}, 2.5);
          tl.to(mFill, {{ textShadow: FILL_DOT, duration: 0.4, ease: "power1.in" }}, 2.55);
          tl.to(mWrap, {{ y: -330, scale: 0.05, duration: 0.5, ease: "power2.in" }}, 2.5);
          tl.to(mWrap, {{ opacity: 0, duration: 0.08, ease: "none" }}, 2.96);

          // slam burst (~20 sparkles), deterministic offsets from a fixed-seed LCG
          var BURST = {json.dumps(burst_js)};
          BURST.forEach(function (b, i) {{
            var el = $("f7_bs" + i);
            var t0 = 1.25 + (i % 5) * 0.012;
            gsap.set(el, {{ x: 0, y: 0, scale: 0, opacity: 0 }});
            tl.to(el, {{ opacity: 1, scale: b[2], duration: 0.08, ease: "power2.out" }}, t0);
            tl.to(el, {{ x: b[0], y: b[1], duration: b[3], ease: "expo.out" }}, t0);
            tl.to(el, {{ scale: 0, opacity: 0, duration: b[3] * 0.7, ease: "power2.in" }}, t0 + b[3] * 0.3);
          }});

          // 「저 하늘 너머로」
          var sub = $("f7_l21sub");
          gsap.set(sub, {{ opacity: 0, y: 14, filter: "blur(6px)" }});
          tl.to(sub, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.19, ease: "power2.out" }}, 1.14);
          kwPop($("f7_kw21"), 1.69);
          tl.to(sub, {{ opacity: 0, y: -10, filter: "blur(6px)", duration: 0.13, ease: "power2.in" }}, 2.8);

          // ---------- constellation camera ----------
          var cam = $("f7_cam"), drift = $("f7_drift");
          gsap.set(cam, {{ x: 0, y: 0, scale: 1, rotation: 0, transformOrigin: "960px 510px" }});
          gsap.set(drift, {{ y: 0 }});
          tl.to(drift, {{ y: -10, duration: 14, ease: "sine.inOut" }}, 3.0);
          tl.to(cam, {{ scale: 0.92, y: 40, duration: 0.74, ease: "power2.inOut" }}, 17.31);   // 고개 들어 — we look up
          tl.to(cam, {{ scale: 0.95, duration: 5.8, ease: "sine.inOut" }}, 18.9);              // held note: very slow push
          tl.to(cam, {{ scale: 0.7, rotation: -8, y: 10, duration: 7.3, ease: "sine.inOut" }}, 24.7); // afterglow: turn + recede
          var SIO = gsap.parseEase("sine.inOut");
          function screenPos(x, y, t) {{
            var p = Math.min(1, Math.max(0, (t - 24.7) / 7.3)), e = SIO(p);
            var s = 0.95 - 0.25 * e, r = (-8 * e) * Math.PI / 180, ty = 40 - 30 * e;
            var vx = (x - 960) * s, vy = (y - 10 - 510) * s;
            return {{ x: 960 + vx * Math.cos(r) - vy * Math.sin(r), y: 510 + ty + vx * Math.sin(r) + vy * Math.cos(r) }};
          }}

          // ---------- edges: draw on (stroke-dashoffset 1000 → 0), fade when an endpoint falls ----------
          var edgesG = $("f7_edges");
          gsap.set(edgesG, {{ opacity: 0.6 }});
          var EDGES = {json.dumps(edge_js)};
          EDGES.forEach(function (e) {{
            var g = $(e[0]), paths = g.querySelectorAll("path");
            gsap.set(paths, {{ strokeDashoffset: 1000 }});
            gsap.set(g, {{ opacity: 1 }});
            tl.to(paths, {{ strokeDashoffset: 0, duration: e[2], ease: "power1.inOut" }}, e[1]);
            tl.to(g, {{ opacity: 0, duration: e[4], ease: "power1.out" }}, e[3]);
          }});
          tl.to(edgesG, {{ opacity: 1, duration: 0.15, ease: "power2.out" }}, 10.48);            // bottle completes on 가
          tl.to(edgesG, {{ opacity: 0.65, duration: 0.8, ease: "power2.inOut" }}, 10.63);
          tl.to(edgesG, {{ opacity: 0.9, duration: 2.6, ease: "sine.inOut" }}, 13.61);            // L26 brightens .6 → .9
          tl.to(edgesG, {{ opacity: 0.5, duration: 2.2, ease: "sine.inOut" }}, 24.7);             // afterglow recedes

          var inglow = $("f7_inglow");
          gsap.set(inglow, {{ opacity: 0 }});
          tl.to(inglow, {{ opacity: 1, duration: 1.1, ease: "sine.out" }}, 10.48);
          tl.to(inglow, {{ opacity: 0, duration: 1.9, ease: "sine.inOut" }}, 24.7);

          // ---------- nodes: ignite (sparkle + halo + spark dots), twinkle, then fall as shooting stars ----------
          var WAVE = {{ A: 10.56, B: 10.62, C: 10.62, D: 10.68, E: 10.68, F: 10.74, G: 10.74, H: 10.8 }};
          var NODES = {json.dumps(node_js)};
          NODES.forEach(function (n) {{
            var k = n[0], t = n[3], td = n[4], fdur = n[5], fdist = n[6], idx = n[7];
            var node = $("f7_n_" + k), pop = $("f7_np_" + k), tw = $("f7_nt_" + k), halo = $("f7_nh_" + k);
            gsap.set(node, {{ autoAlpha: 1 }});
            gsap.set(pop, {{ scale: 0, autoAlpha: 0, transformOrigin: "50% 50%" }});
            gsap.set(tw, {{ scale: 1, opacity: 1, transformOrigin: "50% 50%" }});
            gsap.set(halo, {{ scale: 0.4, opacity: 0, transformOrigin: "50% 50%" }});
            tl.to(pop, {{ autoAlpha: 1, duration: 0.05, ease: "none" }}, t - 0.02);
            tl.to(pop, {{ scale: 1, duration: 0.45, ease: "back.out(2.2)" }}, t - 0.02);
            tl.to(halo, {{ scale: 1.6, opacity: 1, duration: 0.16, ease: "power2.out" }}, t);
            tl.to(halo, {{ scale: 1, duration: 0.6, ease: "power2.inOut" }}, t + 0.16);
            for (var j = 0; j < 6; j++) {{
              var pp = $("f7_pp_" + k + j);
              var a = (j / 6) * Math.PI * 2 + idx * 0.7, r = 34 + ((j * 13 + idx * 7) % 30);
              gsap.set(pp, {{ x: 0, y: 0, scale: 1, opacity: 0 }});
              tl.set(pp, {{ opacity: 0.95 }}, t);
              tl.to(pp, {{ x: Math.cos(a) * r, y: Math.sin(a) * r, scale: 0.3, duration: 0.6, ease: "expo.out" }}, t);
              tl.to(pp, {{ opacity: 0, duration: 0.45, ease: "power1.in" }}, t + 0.15);
            }}
            if (WAVE[k] !== undefined) {{
              tl.to(halo, {{ scale: 1.45, duration: 0.12, ease: "power2.out" }}, WAVE[k]);
              tl.to(halo, {{ scale: 1, duration: 0.5, ease: "power2.inOut" }}, WAVE[k] + 0.12);
            }}
            // twinkle: finite yoyo, ends back at rest before the node detaches
            var d = 0.62 + ((idx * 0.29) % 0.4), t0 = t + 0.75, span = td - 0.12 - t0;
            var plays = Math.floor(span / d); if (plays % 2 === 1) plays -= 1;
            if (plays >= 2) tl.to(tw, {{ scale: 0.84, opacity: 0.74, duration: d, ease: "sine.inOut", yoyo: true, repeat: plays - 1 }}, t0);
            // detach on a snare hit: flare, vanish, a shooting star takes its place
            tl.to(pop, {{ scale: 1.4, duration: 0.07, ease: "power2.out" }}, td);
            tl.to(node, {{ autoAlpha: 0, duration: 0.06, ease: "none" }}, td + 0.05);
            var fs = $("f7_fs_" + k), tail = $("f7_ft_" + k), sp = screenPos(n[1], n[2], td);
            fs.style.left = sp.x.toFixed(1) + "px";
            fs.style.top = sp.y.toFixed(1) + "px";
            gsap.set(fs, {{ x: 0, y: 0, opacity: 0 }});
            gsap.set(tail, {{ scaleX: 0, transformOrigin: "100% 50%" }});
            var ts = td + 0.03;
            tl.set(fs, {{ opacity: 1 }}, ts);
            tl.to(fs, {{ x: -0.5596 * fdist, y: 0.8288 * fdist, duration: fdur, ease: "power1.in" }}, ts);
            tl.to(tail, {{ scaleX: 1, duration: fdur * 0.45, ease: "power2.out" }}, ts);
            tl.to(fs, {{ opacity: 0, duration: fdur * 0.35, ease: "power1.in" }}, ts + fdur * 0.65);
          }});

          // ---------- lyric lines inside the bottle (one at a time; exits finish before the next entrance) ----------
          var LINES = [
            ["f7_l22", 2.96, 5.68], ["f7_l23", 5.79, 8.40], ["f7_l24", 8.51, 10.69], ["f7_l25", 10.8, 13.37],
            ["f7_l26", 13.48, 16.07], ["f7_l27", 16.18, 18.66], ["f7_l28", 18.77, -1]
          ];
          LINES.forEach(function (L) {{
            var el = $(L[0]);
            gsap.set(el, {{ opacity: 0, y: 12, filter: "blur(6px)" }});
            tl.to(el, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.12, ease: "power2.out" }}, L[1]);
            if (L[2] > 0) tl.to(el, {{ opacity: 0, y: -10, filter: "blur(6px)", duration: 0.11, ease: "power2.in" }}, L[2]);
          }});
          kwPop($("f7_kw22"), 3.98);   // 별들이 — node B ignites
          kwPop($("f7_kw23"), 7.88);   // 빛들이 — node E ignites
          kwPop($("f7_kw24"), 8.68);   // 별자리가 — node F ignites
          kwPop($("f7_kw26"), 13.73);  // 밤이
          // 「그거면 충분해」 held note — a still; 충분해 only warms its glow
          var w28 = $("f7_w28"), l28 = $("f7_l28");
          gsap.set(w28, {{ textShadow: SOFT, color: "#F4F1EA" }});
          tl.to(w28, {{ textShadow: WARM, color: "#FFF4D6", duration: 1.6, ease: "sine.inOut" }}, 21.16);
          tl.to(l28, {{ opacity: 0, filter: "blur(5px)", duration: 0.4, ease: "sine.in" }}, 24.45);

          tl.set(g1, {{ autoAlpha: 0 }}, 32.05);
          window.__timelines["07-f7"] = tl;
          tl.seek(0);
        }})();
      </script>
    </template>
  </body>
</html>
'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote", OUT, len(HTML))
