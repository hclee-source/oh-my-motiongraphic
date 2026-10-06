---
version: alpha
name: Golden Rabbit — Editorial Gold (video / frame layer)
description: >
  Calm editorial system for a {{canvas_w}}×{{canvas_h}} ({{aspect}}) kinetic-typography book promo. Warm black
  stage ({{ink}}), cream type ({{paper}}), one brand gold ({{accent}}) sampled from the logo. Big Korean type
  lands on the beat and holds still; gold rings, discs and hairlines (from the logo) carry the
  percussion; real covers are props that enter on hits and exit on a parabolic arc.
unit: the frame — {{canvas_w}}×{{canvas_h}}
principle: three colors only · type is the hero · shapes echo the logo circle · covers are props, not wallpaper

colors:
  ink: "{{ink}}"
  paper: "{{paper}}"
  accent: "{{accent}}"     # brand gold
  muted: "{{muted}}"

fonts:
  font-face: |
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype"); font-weight: 800; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-5Medium.ttf") format("truetype"); font-weight: 500; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-4Regular.ttf") format("truetype"); font-weight: 400; font-display: block; }
  latin-wordmark: "Montserrat 600 — GOLDEN RABBIT wordmark only, tracking 0.32em, uppercase"
  mono-chrome: "IBM Plex Mono 500 — Latin/numerals only (SERIES 01, counters, URL)"

typography:   # px already scaled for this aspect
  display: { fontFamily: "Paperlogy", px: {{px:220}}, weight: 800, lineHeight: 0.95, tracking: "-0.04em" }
  h1:      { fontFamily: "Paperlogy", px: {{px:150}}, weight: 800, lineHeight: 1.0, tracking: "-0.035em" }
  h2:      { fontFamily: "Paperlogy", px: {{px:96}},  weight: 800, lineHeight: 1.05, tracking: "-0.03em" }
  h3:      { fontFamily: "Paperlogy", px: {{px:56}},  weight: 800, lineHeight: 1.15, tracking: "-0.02em" }
  lead:    { fontFamily: "Paperlogy", px: {{px:40}},  weight: 500, lineHeight: 1.35 }
  caption: { fontFamily: "Paperlogy", px: {{px:30}},  weight: 500, lineHeight: 1.35 }
  label:   { fontFamily: "IBM Plex Mono", px: {{px:22}}, weight: 500, tracking: "0.14em", upper: true }
  wordmark:{ fontFamily: "Montserrat", px: {{px:44}}, weight: 600, tracking: "0.32em", upper: true }

layout:
  canvas: {{canvas_w}}×{{canvas_h}}
  safe: "{{hud_note}}"
  side-safe: {{side}}px

components:
  registers: "dark (ground {{ink}}, text {{paper}}, accent {{accent}}) or gold (ground {{accent}}, text {{ink}}); a 0ms register flip is a beat accent"
  book-cover: "real cover JPG, radius 6px, shadow 0 30px 60px rgba(0,0,0,.55); never cropped/tinted/text-overlaid; exits on a parabolic arc"
  caption-block: "title (caption, {{paper}}) + author/meta (label, {{accent}}), max 2 lines"
  kicker: "SERIES 0N — 시리즈명 (label, {{accent}})"
  shapes: "gold ring (2–3px stroke), solid gold disc, 1px hairlines, gold stub bar 48×4, radial burst lines, small 4-point sparkle — each moves ON an anchor"
  logo: "assets/brand/icon.png + 'GOLDEN RABBIT' wordmark + '골든래빗' (Paperlogy 800); dark register only"
---

# Golden Rabbit — Editorial Gold

Warm, confident, unhurried. One display moment per group; readable Korean lines hold ≥ 3 beats.
Covers sit beside the type, never under it. Failure looks like a corporate slideshow with every
cover the same size sliding left to right.
