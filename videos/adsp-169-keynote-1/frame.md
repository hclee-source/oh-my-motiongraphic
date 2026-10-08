---
version: alpha
name: Golden Rabbit — Launch Keynote (video / frame layer)
description: >
  A 1920×1080 (16:9) promo in product-launch grammar. Scenes sit on near-black (#0A0A0C) or
  off-white (#F5F5F7) — one ground per scene, never flipped mid-scene. One short Korean sentence per screen, large,
  with lots of empty space. The book is the product: real CSS-3D object, slow turns, a specular light sweep across the
  cover, macro push-ins on real cover details. Color comes only from the cover; the UI adds one accent (#D92741) on
  one word or one dot at most. Gold (#CEAE73) on the logo mark only.
unit: the frame — 1920×1080
principle: one sentence · one object · slow light · silence is part of the design

colors:
  night: "#0A0A0C"     # dark ground (type = white)
  white: "#F5F5F7"     # light ground (type = ink)
  ink: "#1D1D1F"         # type on white
  mid: "#86868B"         # secondary line (on either ground)
  accent: "#D92741"   # cover red — ONE word, dot or underline per scene, never a ground
  logo: "#CEAE73"       # logo mark only

fonts:
  font-face: |
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype"); font-weight: 800; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-5Medium.ttf") format("truetype"); font-weight: 500; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-4Regular.ttf") format("truetype"); font-weight: 400; font-display: block; }
  korean: "Paperlogy — 800 headline, 400 for the quiet half of a sentence, 500 body"
  mono: "IBM Plex Mono 500 (bundled) — numerals inside device UI only"

typography:   # px already scaled for this aspect
  hero:     { fontFamily: "Paperlogy", px: 150, weight: 800, lineHeight: 1.05, tracking: "-0.035em" }
  h1:       { fontFamily: "Paperlogy", px: 104, weight: 800, lineHeight: 1.1, tracking: "-0.03em" }
  h1-quiet: { fontFamily: "Paperlogy", px: 104, weight: 400, lineHeight: 1.1, tracking: "-0.025em" }
  h2:       { fontFamily: "Paperlogy", px: 56,  weight: 800, lineHeight: 1.2, tracking: "-0.02em" }
  sub:      { fontFamily: "Paperlogy", px: 36,  weight: 500, lineHeight: 1.4, color: mid }
  ui:       { fontFamily: "Paperlogy", px: 22,  weight: 500 }

layout:
  canvas: 1920×1080
  safe: "no HUD in this variant — keep readable content in y 96–984"
  side-safe: 96px
  rule: "type is centred or sits on a strict left edge at x = side-safe·2; never more than 2 text blocks on screen"

motion:
  eases: "power2.out / power3.out / expo.out for entrances, power2.inOut for camera moves; NO back/elastic overshoot, no bounces"
  durations: "entrances 0.8–1.4 s, camera drifts span the whole scene (slow continuous push/turn), holds ≥ 1.5 s on every readable line"
  entrance: "blur(14px)→0 + opacity 0→1 + y 24→0, or letter-by-letter opacity reveal with 0.03 s stagger"
  exit: "opacity → 0 with blur 0→8px over 0.4–0.6 s, or dip to the scene ground"
  scene-change: "inside the frame: last 0.4 s fades content to its ground; first 0.4 s of the next frame fades content in (dip-to-black / cross-dissolve feel). No wipes, irises or shape transitions."

components:
  book3d: "CSS-3D book per references/recipes/book3d.md — front = real cover, back = real back cover, spine = real spine image; page block SOLID paper color (no stripes — fine stripes moiré and pick up chroma bleed in H.264). Slow Y-turns (≥ 2 s per 30°)."
  light-sweep: "a specular band (white, 18–25% peak, soft edges) that travels once across the cover face in 1.2–1.8 s, clipped to the cover rectangle by a wrapper with overflow:hidden OUTSIDE the 3D chain or on the flat cover in 2D scenes. This is the ONLY gradient allowed in the style."
  floor-shadow: "soft contact shadow under products: flat blurred ellipse rgba(0,0,0,.45) on night / rgba(0,0,0,.12) on white, outside the 3D subtree"
  devices: "minimal original laptop + phone outlines: thin bezels (#2C2C2E on night, #D2D2D7 on white), rounded corners, no brand marks, white screens with ink UI; soft shadow 0 40px 90px rgba(0,0,0,.35)"
  live-dot: "solid accent circle 18–24 px that pulses opacity 1↔0.35 on beats (seek-safe tl.set / tweens)"
  logo: "assets/brand/icon.png — gold mark; lockup with '골든래빗' Paperlogy 800 in white/ink"
---

# Golden Rabbit — Launch Keynote

Quiet confidence instead of noise. Every scene is one ground, one sentence, one object. Motion is slow and
continuous: the camera keeps drifting, the book keeps turning, light passes over the cover. Rhythm comes from
*when* things appear (on the music's phrase starts and strong hits), not from how hard they hit.

## Do / Don't
- Do leave at least 40% of every frame empty. Do hold each readable sentence ≥ 1.5 s.
- Do pair a bold half and a quiet half in one sentence (800 vs 400), or a white line and a mid-gray line.
- Do macro-push into REAL cover details (the cover already carries the copy) instead of retyping them.
- Don't use label boxes, offset shadows, confetti, marquees, HUD chrome, colored grounds, overshoot eases or Latin chip labels.
- Don't put text over the cover. Don't use any gradient except the light sweep on the product.
