---
version: alpha
name: Golden Rabbit — Bold Beat (video / frame layer)
description: >
  Loud kinetic-poster system for a 1920×1080 (16:9) beat-cut book promo. Three flat
  registers flip at 0ms on strong beats (accent #FFE500 / ink #1E2687 / paper #F2F0EA). Huge Korean type
  cut word by word, label-box highlights, Latin/Korean pair chips, mixed-face words, marquee
  texture, geometric confetti. Brand gold (#CEAE73) appears ONLY on the logo mark.
unit: the frame — 1920×1080
principle: one word per beat · flip the ground on hits · box the key word · gold is for the logo only

colors:
  accent: "#FFE500"   # loud register + label boxes on ink
  ink: "#1E2687"         # black register + text on accent/paper
  paper: "#F2F0EA"     # light register
  logo: "#CEAE73"       # logo mark ONLY (assets/brand/icon.png) — never UI

fonts:
  font-face: |
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype"); font-weight: 800; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-5Medium.ttf") format("truetype"); font-weight: 500; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-4Regular.ttf") format("truetype"); font-weight: 400; font-display: block; }
  korean: "Paperlogy — 800 hero words, 400 for the contrasting light half of a line"
  latin-heavy: "Archivo Black (bundled, weight 400 only) — Latin caps, chips"
  latin-italic: "Playfair Display italic 700 — lowercase half of a mixed word (GOLDEN·rabbit, BEST·seller)"
  mono: "IBM Plex Mono 400/700 (bundled) — counters, numerals, tiny labels"

typography:   # px already scaled for this aspect
  mega:     { fontFamily: "Paperlogy", px: 360, weight: 800, lineHeight: 0.9, tracking: "-0.05em", note: "may crop off the frame on purpose" }
  display:  { fontFamily: "Paperlogy", px: 240, weight: 800, lineHeight: 0.92, tracking: "-0.045em" }
  h1:       { fontFamily: "Paperlogy", px: 150, weight: 800, lineHeight: 1.0, tracking: "-0.04em" }
  h1-light: { fontFamily: "Paperlogy", px: 150, weight: 400, lineHeight: 1.0, tracking: "-0.03em" }
  h2:       { fontFamily: "Paperlogy", px: 88,  weight: 800, lineHeight: 1.05, tracking: "-0.03em" }
  caption:  { fontFamily: "Paperlogy", px: 34,  weight: 800, lineHeight: 1.25 }
  chip:     { fontFamily: "Archivo Black", px: 30, tracking: "0.02em", upper: true }
  chip-ko:  { fontFamily: "Paperlogy", px: 30, weight: 800 }
  label:    { fontFamily: "IBM Plex Mono", px: 20, weight: 700, tracking: "0.12em", upper: true }

layout:
  canvas: 1920×1080
  safe: "no HUD in this variant — keep readable content in y 96–984"
  side-safe: 96px

components:
  registers:
    accent: "ground #FFE500, text #1E2687, label boxes ink with accent text"
    ink: "ground #1E2687, text #F2F0EA, label boxes accent with ink text"
    paper: "ground #F2F0EA, text #1E2687, label boxes ink with paper text"
    rule: "Flip registers at 0ms ON strong kicks/snares (tl.set). 1–2 beats per register in dense sections."
  label-box: "solid rectangle (no radius) tightly wrapping one key word; padding 0.08em 0.18em; pops scaleX 0→1 from the left in ~0.12s"
  pair-chip: "small chip under a hero word carrying its translation (Korean hero → Latin chip, Latin hero → Korean chip)"
  mixed-word: "CAPS half in Archivo Black + lowercase half in Playfair Display italic 700"
  marquee: "full-width rows of a repeated phrase, alternating direction, alternating filled vs 2px outline; offsets are timeline tweens"
  confetti: "● ■ ▲ ○ ✕ ◆ — flat ink/accent (paper on ink), 24–90px, pop with overshoot on hits, never over a cover or readable word"
  speed-trail: "fast moves get 2–3 ghost copies at 0.35/0.2/0.1 opacity (seek-safe duplicates)"
  book-cover: "real cover JPG, never cropped/tinted/text-overlaid; 0 radius; hard offset shadow 14px 14px 0 #1E2687 on accent/paper, 0 24px 60px rgba(0,0,0,.6) on ink; tossed rotation −8°..+8°"
  logo: "assets/brand/icon.png — the ONLY gold element; on ink register only"
---

# Golden Rabbit — Bold Beat

Every strong hit changes something visible: a word lands, the ground flips, a box snaps around a
key word, a cover is tossed in. Texture words get one beat (≈0.47s at 129 BPM). Readable lines
and book titles hold at least 3 beats.

## Do / Don't
- Do mix Korean weights (400 + 800) and pair hero words with a translation chip.
- Do let mega type crop off the frame. Mark such elements `data-layout-allow-overlap`.
- Do move things with transforms (x/y/scale/rotation/opacity) only.
- Don't use gradients, glows, or any color outside accent / ink / paper (+ the gold logo mark).
- Don't draw corner chrome in frames when the HUD is on.
