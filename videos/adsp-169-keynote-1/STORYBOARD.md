---
compositionId: bgm
duration_s: 31.82 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "통계를 처음 해도, 이 책 한 권으로 ADsP를 빠르게 딴다"
variant: { name: adsp-169-keynote-1, style: launch-keynote, aspect: "16:9", seed: 11, intensity: calm }
style:
  font: "Paperlogy 800/500/400 (embedded, Korean) / IBM Plex Mono 500 (numerals in UI only)"
  palette: ["#0A0A0C", "#F5F5F7", "#1D1D1F", "#86868B", "#D92741"]
assets: "assets/covers/9791194383697.jpg (real front cover 1080×1476); assets/book/back.jpg (real back cover 877×1200); assets/book/spine.jpg (real spine 88×1200); assets/brand/icon.png (gold logo mark); assets/fonts/ Paperlogy"
build_notes:
  - "follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)"
  - "no HUD in this variant — keep readable content in y 96–984"
  - "grounds per frame (scene_color): f1 night, f2 night, f3 white, f4 night, f5 white, f6 night — ONE ground per frame, never flipped mid-frame"
  - "scene changes are in-frame dips: each frame fades its content IN over its first ~0.4 s and OUT to its own ground over its last ~0.4 s (f6 excepted: it ends on the lockup). No shape transitions (transition_out: none everywhere)."
  - "launch grammar (frame.md motion): eases power2/power3/expo only, NO back/elastic/overshoot; entrances blur(14px)→0 + y 24→0 over 0.8–1.4 s; every readable line holds ≥ 1.5 s; ≥ 40% of the frame stays empty; ≤ 2 text blocks on screen"
  - "CSS-3D book: follow .claude/skills/goldenrabbit-promo/references/recipes/book3d.md exactly; front = assets/covers/9791194383697.jpg, back = assets/book/back.jpg, spine = assets/book/spine.jpg (real images); page block + top face = SOLID #F4EFE6 (no stripes: they moiré and pick up chroma bleed in H.264)"
  - "light sweep = the only gradient allowed: a soft white band (peak 18–25% alpha) clipped to the cover face, travelling once in 1.2–1.8 s"
  - "facts are fixed — use the copy verbatim; never add rankings, pass rates or 'N주 합격'"
avoid: ["text over covers", "gradients/glows except the light sweep on the product", "overshoot/bounce eases", "label boxes, offset shadows, confetti, marquees, HUD", "Latin chip labels", "copying reference videos' copy or layouts", "unsupported claims (1위, 합격률, N주 합격)"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 4.41s
- span_sec: [0.0, 4.41]
- pacing: phrase_flow
- mood: [cinematic, quiet]
- feel: VOID 0–1.0 (near silence, soft snare fill) → piano/strings enter on the 1.53 downbeat (SURGE@1). Beats 0.07 0.86 1.53 2.23 3.06 3.76 | next downbeat 4.41
- role: intro (HOOK — cold line)
- pattern_hint: COLD-LINE
- scene_color: #0A0A0C
- transition_out: none
- sfx: whoosh-cinematic@1.30

### Groups

- **g1** — free_design
  - span_sec: [0.0, 4.41]
  - free_design: { dominant_system: "one sentence resolving out of black, two-weight contrast", primitives: ["blur-resolve", "kinetic-letter-in"], density_topology: "single" }
  - anchors: [1.53, 2.23, 3.76]
  - copy: { a: "통계,", b: "처음이어도." }
  - intent: "NIGHT ground #0A0A0C for the whole frame, nothing else on screen. 0–1.4 s: pure black (silence is part of the design). 1.53: 'a' resolves as the first half of a single centred line — Paperlogy 800 ~120 px white #F5F5F7, blur 14px→0 + opacity 0→1 + y 24→0 over 1.0 s power3.out. 2.23: 'b' (same line, after a space) resolves the same way in Paperlogy 400 ~120 px, colour mid gray #86868B settling to white #F5F5F7 over 0.8 s (the quiet half of the sentence). The whole line is optically centred (x centre 960, y ≈ 540). 1.53→4.0: very slow scale 1.00→1.04 on the line (camera drift, power1.inOut). 3.95→4.41: line fades out with blur 0→8px (power2.in). Last frame = pure black."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 5.78s
- span_sec: [4.41, 10.19]
- pacing: phrase_flow
- mood: [cinematic, reveal]
- feel: MEDIUM warm build, kick fills at 7.22–7.90 and 9.01–9.66, hi-hat fill 10.12 into the SURGE. Beats 4.41 5.08 5.78 6.64 7.31 7.96 8.64 9.40 10.19 (downbeats 4.41, 7.31, 10.19)
- role: series0 (REVEAL — the product)
- pattern_hint: DARK-REVEAL + PRODUCT-TURN
- scene_color: #0A0A0C
- transition_out: none
- sfx: whoosh-cinematic@4.35, sparkle@7.31
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [4.41, 10.19]
  - free_design: { dominant_system: "the book emerges from darkness as a product: slow 3D turn, one light sweep, then its name", primitives: ["spotlight-sweep", "blur-resolve"], density_topology: "reveal → hold" }
  - anchors: [4.41, 5.78, 7.31, 8.64, 10.19]
  - copy: { title: "2026 빠르게 따는 ADsP" }
  - intent: "NIGHT ground. CSS-3D book (430×588 base, scale ~0.95) centred at x 960, y ≈ 470, with a soft floor shadow ellipse below it (outside the 3D chain). 4.41: the book is at rotateY -38°, rotateX 6°, in near-darkness — implement darkness as a NIGHT-coloured plate in front of the whole book layer (opacity 0.92 → 0 over 2.2 s power2.out), NOT a filter on the 3D chain. Through the whole frame the book turns continuously from rotateY -38° to -10° (power2.inOut, 4.41→10.0) and drifts up 20 px — never stops, never overshoots. 7.31 (downbeat): ONE light sweep — a soft white diagonal band (peak 22% alpha) clipped to the cover face travels left→right across the cover in 1.5 s. 7.31: 'title' resolves under the book (centred, y ≈ 900) — Paperlogy 800 ~56 px white, blur→sharp 1.0 s; the word 'ADsP' may carry the accent #D92741 (the only accent on screen). Hold title to 9.75. 9.75→10.19: everything fades to NIGHT."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 5.55s
- span_sec: [10.19, 15.74]
- pacing: phrase_flow
- mood: [warm, confident]
- feel: SURGE at ~11 then HIGH heavy 11–14, dip at 14, SURGE at 15. Beats 10.19 10.87 11.52 12.19 12.89 13.63 14.40 15.07 | downbeats 10.19, 12.89, 15.74
- role: series1 (노베이스부터)
- pattern_hint: MACRO-PUSH + HERO-LINE
- scene_color: #F5F5F7
- transition_out: none
- sfx: whoosh-short@10.15
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [10.19, 15.74]
  - free_design: { dominant_system: "macro camera push into a real cover detail, sentence on the empty side", primitives: ["dolly-zoom", "blur-resolve"], density_topology: "push → hold" }
  - anchors: [10.19, 11.52, 12.89, 15.07]
  - copy: { line: "노베이스부터." }
  - intent: "WHITE ground #F5F5F7 (first light scene; content still fades in over the first 0.4 s). RIGHT half: the REAL flat cover assets/covers/9791194383697.jpg (2D, not 3D), never tinted or overlaid, with a soft shadow 0 40px 90px rgba(0,0,0,.18). 10.19: cover shown whole (~520×711, centred x ≈ 1300, y 540). 10.19→15.5: one slow continuous camera push (scale 1 → ~2.4, power2.inOut) centred on the cover's lower-right hashtag block (#노베이스 #비전공자 #독학 … — roughly 62–92% x, 66–76% y of the cover image) so that by ~13 s those real hashtags read large. The cover sits inside a fixed RIGHT-HALF window (x 900–1824, y 96–984, overflow hidden) so it never reaches the left side. LEFT half (x 192–820): 11.52 'line' resolves — Paperlogy 800 ~104 px ink #1D1D1F, blur→sharp 1.0 s; hold to 15.3. 12.89: a thin 6 px accent #D92741 underline draws under '노베이스' (scaleX 0→1, 0.8 s expo.out) — the only accent. 15.3→15.74: fade content to WHITE."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 5.34s
- span_sec: [15.74, 21.08]
- pacing: phrase_flow
- mood: [focused, modern]
- feel: HIGH steady. Beats 15.74 16.44 17.30 18.00 18.65 19.30 19.85 20.41 | downbeats 15.74, 18.65, 21.08
- role: series2 (PC·모바일 CBT)
- pattern_hint: DEVICE-PAIR + QUIET-STAT
- scene_color: #0A0A0C
- transition_out: none
- sfx: click-soft@16.44, click-soft@17.30, click-soft@18.00, tick@18.65

### Groups

- **g1** — free_design
  - span_sec: [15.74, 21.08]
  - free_design: { dominant_system: "laptop and phone side by side running the same mock exam; answers appear on both at once", primitives: ["blur-resolve", "counting-punch"], density_topology: "build → replace → hold" }
  - anchors: [15.74, 16.44, 17.30, 18.00, 18.65, 20.41]
  - copy: { a: "PC에서도. 폰에서도.", b: "모의고사 5회 + 기출 5회", ui_title: "ADsP 모의고사 1회", ui_sheet: "답안 표기란" }
  - intent: "NIGHT ground. Minimal ORIGINAL devices (no brands), soft shadows, thin bezels #2C2C2E, white #F5F5F7 screens with ink UI: a laptop (screen ~760×475 + thin base) centred x ≈ 820, y ≈ 460, and a phone (~230×470) standing to its right, overlapping the laptop's right edge slightly (x ≈ 1330). Both screens show the SAME CBT question: header 'ui_title' + a timer in IBM Plex Mono, 'Q3.' + grey text bars, 4 numbered option circles; the laptop also shows a small answer-sheet column ('ui_sheet', 5 rows × 4 bubbles) on its LEFT side so the phone never hides it. 15.74: devices rise 40 px + blur→sharp (1.2 s power3.out, phone 0.15 s later). 16.44 / 17.30 / 18.00: one answer marked per beat — the SAME option fills on the phone, on the laptop question and in the laptop answer sheet simultaneously (fill ink, 0.25 s power2.out, no overshoot), timer ticks down on both. Text centred under the devices (y ≈ 900): 15.9 'a' resolves (Paperlogy 800 ~56 px white; '폰에서도.' may be weight 400). 18.65: 'a' fades up and out; 'b' resolves in its place (Paperlogy 800 ~56 px white, the two '5' numerals in accent #D92741, counting 0→5 with 0 ms text swaps over 0.4 s). Hold to 20.65. Slow camera drift scale 1→1.03 across the frame. 20.65→21.08: fade to NIGHT."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 4.92s
- span_sec: [21.08, 26.0]
- pacing: phrase_flow
- mood: [urgent, warm]
- feel: HIGH heavy, phrase change at 23.75, hard stop at 26. Beats 21.08 21.78 22.45 23.08 23.75 24.40 25.08 | downbeats 21.08, 23.75
- role: series3 (Live 마무리 특강)
- pattern_hint: LIVE-DOT
- scene_color: #F5F5F7
- transition_out: none
- sfx: ping@21.78

### Groups

- **g1** — free_design
  - span_sec: [21.08, 26.0]
  - free_design: { dominant_system: "a single pulsing live dot leads a two-line sentence", primitives: ["blur-resolve", "kinetic-letter-in"], density_topology: "build → hold" }
  - anchors: [21.08, 21.78, 22.45, 23.75, 24.40, 25.08]
  - copy: { a: "시험 직전,", b: "Live 마무리 특강." }
  - intent: "WHITE ground #F5F5F7. Strict left edge at x 192, two-line block vertically centred (y ≈ 540). 21.08: a solid accent #D92741 dot (22 px) fades in at the left edge above line a, then pulses opacity 1 ↔ 0.35 on each beat (21.78, 22.45, 23.08, 23.75, 24.40, 25.08) — seek-safe tweens. 21.78: 'a' resolves (Paperlogy 400 ~104 px, mid #86868B settling to ink, blur→sharp 1.0 s). 22.45: 'b' resolves on the line below at x 192 (Paperlogy 800 ~104 px ink #1D1D1F; 'Live' in accent #D92741 — the only accent word). Hold both to 25.55. Slow drift: block x +0 → +16 px across the frame. 25.55→26.0: fade to WHITE."

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 5.82s
- span_sec: [26.0, 31.82]
- pacing: phrase_flow
- mood: [triumphant, calm]
- feel: drop at 26, SURGE 27, small dip 28, SURGE 29, strong hits 27.03 27.75 29.00 30.02 30.53 30.77 → end 31.82
- role: finale (PRODUCT-LOCKUP)
- pattern_hint: PRODUCT-LOCKUP
- scene_color: #0A0A0C
- transition_out: none
- sfx: whoosh-cinematic@25.95, chime@29.00
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [26.0, 31.82]
  - free_design: { dominant_system: "hero product shot + name + logo lockup", primitives: ["spotlight-sweep", "blur-resolve"], density_topology: "reveal → hold" }
  - anchors: [26.0, 27.03, 29.0, 30.02]
  - copy: { title: "2026 빠르게 따는 ADsP", where: "예스24 · 교보문고 · 알라딘", brand: "골든래빗" }
  - intent: "NIGHT ground. LEFT: CSS-3D book (scale ~1.0) centred x ≈ 640, y ≈ 520, front nearly facing camera (rotateY -14° → -6° slowly over the whole frame, power2.inOut), soft floor shadow. 26.0: book rises 30 px while a NIGHT plate in front of it goes 0.9→0 (1.0 s). 27.03 (SURGE): one light sweep across the cover (1.4 s). RIGHT column (x 1120–1760, left-aligned, vertically centred): 27.03 'title' resolves (Paperlogy 800 ~84 px white, may wrap to two lines '2026 빠르게 따는' / 'ADsP' with 'ADsP' in accent #D92741); 29.0 'where' resolves under it (Paperlogy 500 ~34 px mid #86868B); 30.02 the logo lockup resolves at the bottom of the column: assets/brand/icon.png (~56 px tall) + 'brand' Paperlogy 800 ~34 px white. Hold everything to the end (≥ 1.5 s calm hold); no fade out — the video ends on the lockup."
