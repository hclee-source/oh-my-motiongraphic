---
version: alpha
name: Golden Rabbit — Frame (video / frame layer)
description: >
  Brand spec derived from the Golden Rabbit logo (gold circular rabbit mark) for a 1920×1080
  kinetic-typography book promo. Structure modeled on the shipped `broadside` preset (two
  registers, one accent, massive display type as graphic primitive, flat plane, 1px hairlines),
  with the accent replaced by the brand gold sampled from assets/brand/icon.png and a
  Korean-capable display face (Paperlogy, embedded via @font-face).
unit: the frame — 1920×1080
principle: three colors only · type is the hero · shapes echo the logo circle · covers are props, not wallpaper

colors:
  ink-black: "#0F0E0C"
  ink-alt: "#1A1814"
  gold: "#CEAE73"
  gold-deep: "#A8874A"
  cream: "#F4EFE6"
  cream-muted: "#8C877E"
  border-dark: "#2A2721"

fonts:
  # Embedded — declare in every frame's <style> inside <template>; paths are relative to the project root.
  font-face: |
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype"); font-weight: 800; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-5Medium.ttf") format("truetype"); font-weight: 500; font-display: block; }
    @font-face { font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-4Regular.ttf") format("truetype"); font-weight: 400; font-display: block; }
  latin-wordmark: "Montserrat (bundled) — GOLDEN RABBIT wordmark only, weight 600, tracking 0.32em, uppercase"
  mono-chrome: "IBM Plex Mono (bundled) — Latin/numerals only: SERIES 01, counters, URL; weight 500, tracking 0.14em, uppercase"

typography:
  display:   { fontFamily: "Paperlogy", px: 220, weight: 800, lineHeight: 0.95, tracking: "-0.04em" }
  h1:        { fontFamily: "Paperlogy", px: 150, weight: 800, lineHeight: 1.0, tracking: "-0.035em" }
  h2:        { fontFamily: "Paperlogy", px: 96,  weight: 800, lineHeight: 1.05, tracking: "-0.03em" }
  h3:        { fontFamily: "Paperlogy", px: 56,  weight: 800, lineHeight: 1.15, tracking: "-0.02em" }
  lead:      { fontFamily: "Paperlogy", px: 40,  weight: 500, lineHeight: 1.35 }
  caption:   { fontFamily: "Paperlogy", px: 30,  weight: 500, lineHeight: 1.35 }
  label:     { fontFamily: "IBM Plex Mono", px: 22, weight: 500, tracking: "0.14em", upper: true }
  wordmark:  { fontFamily: "Montserrat", px: 44, weight: 600, tracking: "0.32em", upper: true }

spacing:
  pad-x: 104px
  pad-y: 96px

components:
  registers:
    dark: "ground {colors.ink-black}, text {colors.cream}, accent {colors.gold}"
    gold: "ground {colors.gold}, text {colors.ink-black}"
    description: "Two surfaces only. One register per group; a 0ms register flip is a beat accent."
  book-cover:
    shape: "the real cover JPG (assets/covers/*.jpg), aspect ~1:1.4–1:1.5, object-fit cover, border-radius 6px"
    elevation: "box-shadow 0 30px 60px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,255,255,0.06)"
    size: "hero cover ~460–560px tall; supporting covers ~300–380px; finale grid ~200px"
    description: "Covers are never cropped, recolored, or overlaid with text. Text sits beside them."
  caption-block:
    title: "{typography.caption} in {colors.cream}, max 2 lines, max-width 560px"
    meta: "{typography.label} in {colors.gold}"
  kicker:
    typography: "{typography.label}"
    color: "{colors.gold} (dark) / ink 60% (gold)"
    pattern: "SERIES 0N — 시리즈명"
  shapes:
    vocabulary: "gold ring (2–3px stroke circle, echoes the logo), solid gold disc, 1px hairline rules, gold stub bar 48×4px, radial burst lines, small 4-point sparkle (from the logo)"
    description: "Shapes are rhythm, not decoration — each appears or moves ON an anchor."
  logo:
    mark: "assets/brand/icon.png (gold circular rabbit mark, transparent PNG 428×411)"
    lockup: "mark + 'GOLDEN RABBIT' wordmark (Montserrat) + '골든래빗' (Paperlogy 800)"
    description: "Never recolor or redraw the mark. Place on dark register only."
---

# Golden Rabbit — Frame

## Overview

A warm-black stage, cream type and a single brand gold. Korean display type at 150–220px is the
hero of every group. It lands on the beat, holds still long enough to read, and leaves with a hard
cut or an arc. The real book covers are props on that stage: they enter on hits, sit beside the
type, and exit along a **parabolic arc** (x travel plus a y-arc plus a slight rotation), never a
plain linear slide. Gold circles, rings and hairlines borrowed from the logo carry the
percussion: a ring scales out on a kick, a stub bar wipes on a snare, a disc flips the register
on a surge.

## Frame Craft Bar

- **Squint** — one display moment dominates each group; covers support it.
- **Restraint** — three colors only: ink-black, cream, gold. Covers bring their own colors, so
  never add a fourth UI color.
- **Readability** — a readable Korean line holds ≥ 3 beats (≈1.4s at 129 BPM); anything shorter is texture.
- **Safe area** — 104px sides / 96px top-bottom; nothing important crosses it.
- **Reference failure** — a corporate slideshow with every cover the same size sliding left to right.

## Do / Don't

- Do declare the three `@font-face` rules above inside each frame's `<template><style>`.
- Do write Korean copy in Paperlogy. Use IBM Plex Mono only for Latin and numbers.
- Don't blur, tint, crop, or put text over the covers.
- Don't use gradients or a second accent color. A solid gold field is the only "loud" surface.
