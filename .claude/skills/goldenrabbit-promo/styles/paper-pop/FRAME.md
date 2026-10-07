---
version: alpha
name: Golden Rabbit — Paper Pop (video / frame layer)
description: >
  A {{canvas_w}}×{{canvas_h}} ({{aspect}}) promo in the language of Japanese qualification-book ads and paper-craft
  motion (切り絵 / ペーパークラフト + バラエティ テロップ). Everything is a piece of paper lying on paper: a warm ground
  ({{paper}}) with fibre texture, graph-paper or gingham boards, layered paper-cut character faces, white-rimmed
  cutout stickers with soft stacked shadows, double-outlined Korean telop on cushions, red-pen marks. Colours come
  from the cover (yellow {{yellow}}, navy {{navy}}) plus red pen ({{red}}). Gold ({{logo}}) is the logo mark only.
unit: the frame — {{canvas_w}}×{{canvas_h}}
principle: every object is paper · faces carry the emotion · one telop idea per beat · numbers get a ※ source

colors:
  paper: "{{paper}}"     # ground (cream construction paper)
  ink: "{{ink}}"         # text, outlines, the black rim of stickers
  yellow: "{{yellow}}"   # cover yellow — cushions, bursts, highlight
  navy: "{{navy}}"       # cover navy — cushions, panels, title band
  red: "{{red}}"         # red pen: ✕ / ○ / hanamaru / key numbers / red sheet
  sky: "{{sky}}"         # sweat-drop blue, cool accents (sparingly)
  grid: "{{grid}}"       # graph-paper lines on paper boards
  logo: "{{logo}}"       # logo mark ONLY (assets/brand/icon.png)

fonts:
  font-face: |
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype"); font-weight: 800; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-7Bold.ttf") format("truetype"); font-weight: 700; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-6SemiBold.ttf") format("truetype"); font-weight: 600; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-5Medium.ttf") format("truetype"); font-weight: 500; font-display: block; }
  telop: "Paperlogy 600 (SemiBold) for outlined telop, 700 for plain text on cushions/paper, 800 ONLY for big numerals (8.8%, 30, 10회). 800 + thick outlines closed the gaps inside Hangul (붙, 권, 격) and the user said it was unreadable (2026-10-07)."
  single-family: "PAPERLOGY ONLY (user, 2026-10-07: '폰트는 페이퍼로지로 통합'). No Jua / Black Han Sans / Nanum Pen / Gmarket in this style."
  pop: "Paperlogy 600 — speech bubbles, chips, side labels, captions, bubble pops"
  onomatopoeia: "Paperlogy 800 — 딱! / 두둥 / 헉! sound words, tilted −8…−12° (≈0.75× the size you'd use for Black Han Sans)"
  pen: "Paperlogy 600 in red, tilted −6° — the 'handwritten' note next to ✕ / ○ marks (the red-pen stroke carries the hand-drawn feel)"
  numbers: "Paperlogy 800 tabular; unit at 0.45× the numeral size (Japanese price-card ratio)"

typography:   # px already scaled for this aspect
  mega:   { fontFamily: "Paperlogy", px: {{px:260}}, weight: 700, lineHeight: 0.95, tracking: "0.01em" }
  telop:  { fontFamily: "Paperlogy", px: {{px:110}}, weight: 600, lineHeight: 1.1, tracking: "0.02em" }
  telop-s:{ fontFamily: "Paperlogy", px: {{px:76}},  weight: 600, lineHeight: 1.15, tracking: "0.02em" }
  pop:    { fontFamily: "Paperlogy", px: {{px:50}}, weight: 600, lineHeight: 1.25 }
  label:  { fontFamily: "Paperlogy", px: {{px:32}}, weight: 600, tracking: "0.02em" }
  pen:    { fontFamily: "Paperlogy", px: {{px:52}}, weight: 600, color: red, rotate: "-6deg" }
  note:   { fontFamily: "Paperlogy", px: {{px:20}}, weight: 500, note: "※ footnote band, ink at 55%" }

layout:
  canvas: {{canvas_w}}×{{canvas_h}}
  safe: "{{hud_note}}"
  side-safe: {{side}}px
  footnote: "※ band: bottom-left, y ≈ {{canvas_h}} − 52px, note style; required under any statistic"

components:
  paper-layer: "every flat object is a paper piece: box-shadow '0 2px 0 rgba(0,0,0,.08), 0 10px 18px rgba(60,40,10,.18)'; deeper layers add a larger second shadow. Never flat vector fills without a shadow."
  sticker: "white-rim cutout (切り絵ステッカー): an element gets a 10px white rim + soft shadow — for images use filter: drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(6px 10px 0 rgba(0,0,0,.16)); tilt ±2–4°. (Do NOT put filters on the book cover itself — use a white padded wrapper div with box-shadow instead.)"
  faces: "assets/faces/{base,worry,happy,fired}/<slug>.png (512px, transparent, already paper-cut with their own shadows) and assets/faces/sm/{worry,happy}/<slug>.png (160px) for crowds. slugs: p rei lucas bible benny cindy esther alice ian jini kate thomas toynbee (fired: benny, jini only). Expression change = swap the <img> at 0ms on a beat with a 0.12s scale squash (1→0.92→1.04→1). Never redraw faces."
  boil: "カクカク paper boil on faces/stickers: every 1/8 s (tl.set at k/8) rotation ±1.5° and x/y ±2px from an index-seeded table — seek-safe, no Math.random."
  pop-in: "ぽよん: scale 0→1.2 (5 frames) →1.0 (+2 frames), then scaleX 1.1→1 / scaleY 1.06→1 squash (2 frames each)."
  place: "'putting paper down': rotation −6°→+1.5°→0, y +40→0, 0.25 s, shadow offset shrinking (lifted → laid)."
  telop: "stacked copies (shadow / outer / mid / fill) with STROKES IN em, never px: the fill must contrast with the GROUND. Light ground (paper, yellow, gingham) → ink fill, white halo 0.10–0.13em, optional yellow outer 0.15em, offset shadow (0.03em, 0.045em) in ink 30%. Dark ground (navy) → white fill, ink outline 0.06–0.07em, dark-navy outer 0.11–0.13em. Never white fill on a light ground (reads as hollow outline text). Key word in red; particles 80%. -webkit-text-stroke is centred on the glyph edge, so anything wider than ~0.13em floods the gaps inside Hangul."
  cushion: "座布団: a navy / yellow / ink rectangle (or tilted band, or pill) behind telop; scaleX 0→1 from the left in 0.2 s (power3.out), text follows 0.06 s later."
  shout: "＼ … ／ shout brackets: two short slanted strokes either side of a phrase, sliding in 12px from outside, jittering 2px every 2 frames."
  side-label: "サイドテロップ: a pill fixed top-left for the whole scene ('POINT 1' in yellow pill + topic in ink Paperlogy 600) — content changes under it."
  bubble: "speech bubble: white paper with ink 4px outline + tail + paper shadow; Paperlogy 600 text; pops in with pop-in."
  burst: "manga concentration lines (集中線): 90–120 thin ink/yellow triangles pointing at a centre, empty centre circle ~40% of the short side; re-seed the line set every 1/8 s (pre-built sets toggled with tl.set)."
  gloom: "ガーン gloom lines: 5–7 vertical sky/ink strokes above a head, dropping in 2 frames."
  red-pen: "red ✕ / ○ / underline / hanamaru (spiral flower circle) drawn as SVG paths with stroke-dashoffset (pathLength=1000, dasharray 1000), slight wobble."
  red-sheet: "赤シート: translucent red acetate (rgba(214,0,38,.82), mix-blend-mode multiply, rounded 10px, paper shadow) laid over red text hides it; sliding it away (x → 120%) reveals."
  tape: "masking tape (マステ): 26–34px strips, semi-opaque yellow/sky washi with zig-zag torn ends (clip-path polygon), slapped on at 0ms with a 2px shake."
  board: "graph-paper board: paper colour + repeating-linear-gradient grid lines ({{grid}}) every 44px, paper shadow; gingham: two crossing translucent yellow stripes 48px."
  search: "generic search bar CTA (no real service logo): white pill, ink 4px outline, magnifier icon; text types per hit; cursor clicks with a 0.9→1 press and a ripple ring."
  footnote: "※ small grey line at the bottom-left under any number or claim."
  texture: "a paper-fibre overlay sits on top of every frame (generated by make_transitions.py) — do not add your own grain."
---

# Golden Rabbit — Paper Pop

The visual grammar of Japanese qualification-book ads (TAC, FOM, Foresight, AGAROOT, Studying), re-made in paper.
Rhythm comes from paper pieces being *placed*, *flipped*, *taped* and *torn* on the beat, from faces changing
expression, and from telop that stacks one idea per beat. The cover's own colours run the scene; red pen marks
what matters.

## Do / Don't
- Do start a frame on its `scene_color` ground; keep the first ~0.3 s and last ~0.25 s free of essential reads (transitions).
- Do put a ※ source line under every statistic (e.g. ※ 2025년 컴활 1급 실기 · 대한상공회의소 · 응시 건 기준).
- Do let the paper faces carry the emotion of each point (worried → happy / fired) — they are the hero device.
- Don't draw illustrations in SVG/CSS (people, objects, mascots). Faces and props come from assets/faces and assets/props.
  Shapes that are graphic devices (bubbles, tape, red-pen strokes, concentration lines, panels) are fine.
- Don't crop, tint or overlay text on the book cover. Don't use HUD chrome, label-box flips or confetti from bold-beat.
- Don't claim "1위" or anything not in the storyboard copy.
