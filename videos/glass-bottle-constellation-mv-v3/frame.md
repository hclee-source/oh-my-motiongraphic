---
version: alpha
name: 유리병 별자리 — Night-Sky Lyric MV (video / frame layer)
description: >
  A J-pop-style kinetic-typography lyric music video for a Korean band. One continuous night sky (a shared
  background layer, compositions/sky.html, owned by the orchestrator) runs under every frame; each frame paints only
  its FOREGROUND on a transparent stage: lyric typography set in a Mincho-style serif (Noto Serif KR), starlight,
  one glass bottle and constellation lines. Light is the only accent. No HUD, no counters, no section labels,
  no timecodes, no slide numbers — nothing on screen but the song's world and its words.
unit: the frame — 1920×1080 (16:9, YouTube)
principle: readability first · the words are light · one hero device per section · reset at every section · something always drifts

colors:
  night-0: "#050714"     # deepest black-blue (bridge, letterbox)
  night-1: "#0B1230"     # navy — verse sky
  night-2: "#1B1F4E"     # indigo — chorus sky
  violet: "#3B2F6E"      # horizon bloom in choruses
  starlight: "#FFF4D6"   # warm white — stars, sparkles, lit lyric glyphs
  gold-glow: "#FFD27A"   # star glow, bottle light, emphasis keyword glow
  glass: "#DCEBFF"       # glass outline, constellation lines, cool secondary type
  amber: "#FFB45C"       # 'your window' light, 'hot' star in pocket, 타올라 (verse 2 / chorus heat only)
  dawn-rose: "#F2A3A0"   # final chorus horizon only
  dawn-peach: "#FFC89A"  # final chorus horizon only
  text: "#F4F1EA"        # lyric body text (warm paper white)
  text-dim: "#A9B3D6"    # secondary / whispered lines, echoes

fonts:
  font-face: |
    @font-face { font-family: "Noto Serif KR"; src: url("assets/fonts/NotoSerifKR-VF.woff2") format("woff2"); font-weight: 200 900; font-style: normal; font-display: block; }
    @font-face { font-family: "Cormorant Garamond"; src: url("assets/fonts/CormorantGaramond-Italic-VF.woff2") format("woff2"); font-weight: 300 700; font-style: italic; font-display: block; }
  korean: "Noto Serif KR (variable 200–900) — the ONLY Korean face. Light 250–350 for verses, 400–500 for body, 700–900 for chorus hits."
  latin: "Cormorant Garamond Italic 400–600 — the English title line only ('Glass-Bottle Constellation')."
  coverage: "Subset = all 2,350 KS X 1001 Hangul + ASCII + the lyrics. Use only storyboard copy."

typography:   # px for 1920×1080
  mega:     { fontFamily: "Noto Serif KR", px: 220, weight: 800, lineHeight: 1.0,  tracking: "-0.02em" }   # one chorus word (빛나라 / 날아가)
  hero:     { fontFamily: "Noto Serif KR", px: 118, weight: 700, lineHeight: 1.12, tracking: "-0.01em" }  # chorus line
  line:     { fontFamily: "Noto Serif KR", px: 76,  weight: 400, lineHeight: 1.3,  tracking: "0.01em" }   # verse line, horizontal
  vertical: { fontFamily: "Noto Serif KR", px: 58,  weight: 300, tracking: "0.32em", writing: "vertical-rl, text-orientation: upright" }  # 縦書き verse line
  whisper:  { fontFamily: "Noto Serif KR", px: 40,  weight: 300, lineHeight: 1.5,  tracking: "0.12em", color: "text-dim" }
  keyword:  "inside any line, the key noun (별 · 빛 · 유리병 · 별자리 · 이름 · 하늘 · 밤) is set 1.4–1.5× the line size and one weight step heavier, with a gold-glow text-shadow — the Hangul analogue of 'kanji bigger than kana'"
  title-en: { fontFamily: "Cormorant Garamond", px: 44, weight: 400, style: italic, tracking: "0.06em", color: "glass" }

glow:
  text-light: "text-shadow: 0 0 18px rgba(255,210,122,.45), 0 0 46px rgba(255,210,122,.18)"      # lit lyric glyph
  text-soft:  "text-shadow: 0 0 14px rgba(220,235,255,.25)"                                         # default lyric
  star:       "radial gradient starlight → gold-glow → transparent; never a hard-edged circle"

layout:
  canvas: 1920×1080
  safe: "readable lyrics inside x 140–1780, y 110–960. Mega words may bleed past edges only as texture (data-layout-allow-overflow)."
  horizon: "the sky layer draws a hill silhouette in y 900–1080 during verses/outro — keep lyrics above y 880 when the hill is up"
  stage: "#stage background MUST be transparent (the sky layer is underneath). Never paint a full-frame opaque background except where the storyboard asks for a black-out."

motifs:
  bottle: "assets/motifs/bottle.svg — THE glass bottle. Inline its markup verbatim (rename XX_ → fN_), never redraw your own. Parts: cork / glass / fill (light level) / glow / stars / shine / halo."
  sparkle: "assets/motifs/sparkle.svg — the 4-point star path. Reserved for collected / hero stars. Background stars are round dots (the sky layer has them)."
  constellation: "dots of starlight joined by 1.5px glass-colored lines at 60% opacity, drawn on with stroke-dashoffset (pathLength=1000)."
  bottle-constellation: |
    THE title constellation — a glass bottle drawn in stars. Shared by f07 (chorus 2, where it forms) and f13 (ending reprise).
    Node coordinates at 1920×1080 (scale/translate the whole group if a frame needs it smaller):
      A (960,150) cork top · B (902,250) neck-left · C (1018,250) neck-right · D (760,400) shoulder-left · E (1160,400) shoulder-right
      F (690,620) belly-left · G (1230,620) belly-right · H (800,870) base-left · I (1120,870) base-right
    Edges (draw order): A-B, A-C, B-D, C-E, D-F, E-G, F-H, G-I, H-I
    Node star = sparkle path scale 13–18 + soft halo r≈26; A and the belly nodes F/G are the brightest (scale 18).
  falling-star: "a 2–3px starlight head with a 180–320px tapering tail (linear-gradient to transparent), diagonal top-right → bottom-left, 0.6–1.1s."
---

# 유리병 별자리 — Night-Sky Lyric MV

## Concept
Someone sits on a hill every night picking up fallen stars — feelings they never say aloud — and keeps them in a
small glass bottle. The video is that night, from first star to almost-dawn. The **words are light**: lyric glyphs
glow like starlight, fall like shooting stars, drop into the bottle, and in the last chorus burst out of it and become a
constellation. The narrative arc of the image follows the arc of the song:

| section | sky | hero device | typography |
|---|---|---|---|
| intro | black → first star → sky switches on with the band hits | stars pop on hits; title | small vertical title + English italic |
| verse 1 | navy, hill silhouette | a falling star writes each line; the bottle appears | vertical (縦書き), small, wide-tracked, right side |
| pre-chorus 1 | navy warming | letters twinkle; the unnamed '이름' | horizontal, centered, growing |
| chorus 1 | indigo + violet bloom, camera tilts up | river of stars; light stuck in the throat; words dropped into the bottle | big, keyword mega |
| verse 2 | navy | your lit window; footprints of light | horizontal, lower-left, walking left→right |
| pre-chorus 2 | navy warming | one new star is born | centered |
| chorus 2 | indigo + violet | keywords become stars, lines connect into a constellation | words placed ON the constellation nodes |
| bridge (piano) | near-black | the full bottle alone, trembling | tiny vertical whisper, long holds |
| build | glow rising | light leaking from the cork, cork pops | letters gathering speed |
| final chorus (key change) | dawn-edged horizon (rose/peach) | stars burst out of the bottle into the sky | the biggest type of the video |
| outro (piano fades) | pre-dawn pale | the empty bottle, lighter, drifting up | vertical callback to verse 1, fade to black |

## Rules (from lyric-video research)
- **Readability first.** A lyric line must be fully legible ON the first syllable sung (lead the vocal by ~0.1–0.25s
  with the entrance) and stay until the singer finishes the phrase (until ~0.2s before the next line). Long held notes hold the line.
- **Reset at every section** (A-melo / B-melo / sabi). Each frame starts sparse and accumulates within itself.
- **Escalate:** verse = minimal motion, small type, dark. Pre-chorus = rising motion, more contrast. Chorus = large type,
  stronger animation. Bridge = visual reset. Final chorus (key change) = maximum.
- **Always drift.** Nothing is ever fully static: a slow push (scale 1→1.04), a float, or a letter-spacing breathe.
- **Combine 2 properties per entrance** (opacity+y, blur+scale, color+glow). Avoid rotation gimmicks (cheap) — the only
  rotations allowed are the cork pop and tiny (≤3°) tilts on falling/flying letters.
- **Vertical/horizontal alternate by section.** Vertical = intimate monologue; horizontal = addressed to 'you' / big statements.
- Ballad moments fade; band moments cut. Hard cuts only on real hits.

## Do / Don't
- Do let lyric glyphs become light (glow up, shrink into a dot, fall into the bottle).
- Do keep one hero device per section, and keep it different from the previous section's.
- Don't show any HUD, frame index, section name ('Verse', 'Chorus'), timer, progress bar, BPM, or credits other than the song title.
- Don't paint an opaque background on #stage; don't draw your own sky gradient or background star field (sky.html owns them).
- Don't redraw the bottle — inline assets/motifs/bottle.svg.
- Don't use emoji or icon fonts. Stars are SVG/CSS only.
