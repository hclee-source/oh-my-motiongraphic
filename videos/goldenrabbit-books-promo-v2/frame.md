---
version: alpha
name: Golden Rabbit v2 — Bold Beat (video / frame layer)
description: >
  Loud kinetic-poster system for a 1920×1080 beat-cut book promo. Three flat registers that flip
  at 0ms on strong beats (electric yellow / ink black / paper white). Huge Korean type cut word by
  word, label-box highlights, Latin/Korean pairs, words mixed from two typefaces, marquee texture,
  geometric confetti. Brand gold appears ONLY on the logo mark. A separate HUD overlay composition
  owns the corner chrome and the bottom ticker band; frames never draw their own HUD.
unit: the frame — 1920×1080
principle: one word per beat · flip the ground on hits · box the key word · gold is for the logo only

colors:
  yellow: "#FFE500"   # electric accent / full register
  ink: "#0B0B0B"      # black register + text on yellow/paper
  paper: "#F2F0EA"    # light register
  ink-60: "rgba(11,11,11,0.6)"
  paper-60: "rgba(242,240,234,0.6)"
  gold: "#CEAE73"     # logo mark ONLY (assets/brand/icon.png) — never UI

fonts:
  font-face: |
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype"); font-weight: 800; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-5Medium.ttf") format("truetype"); font-weight: 500; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-4Regular.ttf") format("truetype"); font-weight: 400; font-display: block; }
  korean: "Paperlogy — 800 for hero words, 400 for the contrasting light half of a line"
  latin-heavy: "Archivo Black (bundled, weight 400 only) — Latin caps: GOLDEN, SERIES, BEST, chips"
  latin-italic: "Playfair Display italic 700 — the lowercase half of a mixed word (GOLDEN *rabbit*, BEST *seller*)"
  mono: "IBM Plex Mono 400/700 (bundled) — counters, numerals, tiny labels"

typography:
  mega:     { fontFamily: "Paperlogy", px: 360, weight: 800, lineHeight: 0.9, tracking: "-0.05em", note: "may crop off the frame edge on purpose" }
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
  hud-reserved: "top band y 0–88 and bottom band y 1000–1080 belong to the HUD overlay — frames keep readable content in y 104–984 (mega type may crop past any edge as texture)"
  side-safe: 96px

components:
  registers:
    yellow: "ground {colors.yellow}, text {colors.ink}, label boxes ink with yellow text"
    ink: "ground {colors.ink}, text {colors.paper}, label boxes yellow with ink text"
    paper: "ground {colors.paper}, text {colors.ink}, label boxes ink with paper text"
    rule: "Flip registers at 0ms ON strong kicks/snares (tl.set). 1–2 beats per register in dense sections."
  label-box:
    style: "solid rectangle (no radius) tightly wrapping one key word; padding 0.08em 0.18em; pops in with scaleX 0→1 from the left edge in ~0.12s"
  pair-chip:
    style: "small chip under a hero word carrying its translation: Korean hero → Latin chip (Archivo Black), Latin hero → Korean chip (Paperlogy 800). ink box + yellow text, or yellow box + ink text"
  mixed-word:
    style: "one word set in two faces: CAPS half in Archivo Black + lowercase half in Playfair Display italic 700 (e.g. GOLDEN·rabbit, BEST·seller, NEW·release)"
  marquee:
    style: "full-width rows of a repeated phrase, alternating direction per row, alternating filled vs 2px outline (-webkit-text-stroke), speed derived from timeline time — never CSS animation"
  confetti:
    shapes: "● ■ ▲ ○ ✕ ◆ — flat ink or yellow (or paper on ink), 24–90px, pop with overshoot on hits, drift slightly, never cover a cover or a readable word"
  speed-trail:
    style: "fast moves get 2–3 ghost copies trailing behind at 0.35/0.2/0.1 opacity (seek-safe duplicates), or an SVG feGaussianBlur stdDeviation='18 0' during the move only"
  book-cover:
    style: "real cover JPG, never cropped/tinted/text-overlaid; 0 radius; hard offset shadow 14px 14px 0 {colors.ink} on yellow/paper, or 0 24px 60px rgba(0,0,0,.6) on ink; may sit rotated −8°..+8° like a tossed card"
  logo:
    mark: "assets/brand/icon.png — the ONLY gold element; on ink register only"
---

# Golden Rabbit v2 — Bold Beat

Every strong hit changes something you can see. A word lands, the ground flips, a box snaps
around a key word, or a cover is tossed in. Pacing is one readable word per beat (≈0.47s at
129 BPM) for texture words and 2–3 beats for words that must be read. Book titles always hold at
least 3 beats.

The yellow register is the voice of the brand: loud, fast, confident. The ink register is the stage
for covers and the logo. The paper register is for calm, editorial beats. Gold never appears
except on the logo mark, so the logo reveal feels earned.

## Do / Don't
- Do mix weights inside a Korean line (light 400 + heavy 800) and pair hero words with a translation chip.
- Do let mega type crop off the frame. Cropping is the point.
- Do use transforms (x/y/scale/rotation/opacity) for motion. Never animate left/top/width.
- Don't draw HUD/corner chrome in frames (the overlay owns it), and keep readable content out of y<104 and y>984.
- Don't use gradients, soft glows, or any color outside yellow / ink / paper (+ the gold logo mark).
