---
compositionId: bgm
duration_s: 40.85 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "비전공자·노베이스도 ADsP, 빠르게 따는 책 한 권이면 된다"
variant: { name: adsp-169-boldbeat-1, style: bold-beat, aspect: "16:9", seed: 7, intensity: standard }
style:
  font: "Paperlogy 800/400 (embedded, Korean) / Archivo Black (Latin caps) / Playfair Display italic 700 (mixed-word lowercase) / IBM Plex Mono (numerals)"
  palette: ["#FFE500", "#1E2687", "#F2F0EA", "#CEAE73"]
assets: "assets/covers/9791194383697.jpg (real front cover 1080×1476); assets/book/back.jpg (real back cover 877×1200: 학습법 3종 블록 + QR); assets/book/spine.jpg (real spine 88×1200); assets/brand/icon.png (gold logo mark), assets/brand/logo.png; assets/fonts/ Paperlogy 4/5/6/7/8"
build_notes:
  - "follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)"
  - "no HUD in this variant — keep readable content in y 96–984, x 96–1824"
  - "Korean exam-ad grammar: question hook in the first 3 s with 2+ cuts → numbers → '된다' turn + book on the first SURGE → 3 points → cover-tagline climax → store CTA"
  - "Korean exam motifs (draw them, flat): OMR 답안지 bubbles filled by a computer-sign pen, yellow highlighter sweeps, RED grading pen ✕ / ○ (red #E8213F is the ONLY extra colour, used only as pen ink), 합격 stamp"
  - "CSS-3D book: follow .claude/skills/goldenrabbit-promo/references/recipes/book3d.md exactly; front = assets/covers/9791194383697.jpg, back = assets/book/back.jpg, spine = assets/book/spine.jpg (use the real spine image instead of a typed spine title)"
  - "facts are fixed — use the copy verbatim; never add rankings (1위/최단기), pass rates or 'N주 합격'"
avoid: ["text over covers", "gradients/glows", "copying reference videos' copy or layouts", "unsupported claims (1위, 합격률, N주 합격)"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 7.92s
- span_sec: [0.0, 7.92]
- pacing: beat_cut
- mood: [tense, hype]
- feel: quiet 4-on-the-floor intro (bars 0–2) → kick accel-roll from 6.0 into the big hit at 7.92 (next frame). Beats 0.21 0.72 1.21 1.67 | 2.16 2.65 3.13 3.60 | 4.09 4.55 5.04 5.53 | 6.01 6.48 6.97 7.43
- role: intro (HOOK)
- pattern_hint: HOOK-SLAM → number triple-tap → held question
- scene_color: #F2F0EA
- transition_out: none
- sfx: pop@0.21, pop@1.21, pop@2.16, click@4.09, click@4.55, error@5.04, riser@6.01

### Groups

- **g1** — free_design
  - span_sec: [0.0, 4.09]
  - free_design: { dominant_system: "one worried question word per two beats, ground flipping at 0ms on each", primitives: ["palette-flip", "braam-punch", "kinetic-letter-in"], density_topology: "replace" }
  - anchors: [0.21, 1.21, 2.16, 3.13]
  - copy: { q: ["비전공자?", "노베이스?", "통계 0?"], chips: ["NON-MAJOR", "ZERO BASE", "STATS 0"], sub: "ADsP 준비, 이런 고민 중이라면" }
  - intent: "Pull up a nervous test-taker's three doubts, fast (Korean ad hook: 2+ cuts inside 3 s). 0.21 PAPER ground: '비전공자?' slams in centre (display 240 px Paperlogy 800, ink) with pair chip 'NON-MAJOR' (Archivo Black chip, ink box / paper text) under it. 1.21 0ms flip to INK: previous word gone, '노베이스?' (paper colour) + chip 'ZERO BASE' (accent box). 2.16 0ms flip to ACCENT: '통계 0?' (ink) — the '0' set in IBM Plex Mono 700 at 1.3× + chip 'STATS 0'. 3.13 back to PAPER: all three words reappear small (h2 88 px) stacked left like sticky notes tilted −4°/+3°/−2°, and 'sub' types in on the right (caption 34 px, ink) — a breath before the numbers. Every word enters with a 1-frame scale overshoot; nothing eases out — cuts only."
- **g2** — free_design
  - span_sec: [4.09, 7.92]
  - free_design: { dominant_system: "exam facts as an OMR-sheet number triple-tap, then the held question over the kick roll", primitives: ["counting-punch", "screen-shake", "outline-to-fill"], density_topology: "accumulate → hold" }
  - anchors: [4.09, 4.55, 5.04, 6.01, 6.48, 6.97, 7.43]
  - copy: { n1: "50문항", n2: "90분", n3: "과목별 40% 과락", q1: "ADsP,", q2: "나도 될까?" }
  - intent: "INK ground with a faint OMR-answer-sheet motif: a column of answer bubbles ①②③④ (2 px paper outlines, 30% paper colour) along the left edge as texture (data-layout-ignore). 4.09 '50문항' counts 0→50 in IBM Plex Mono 700 (~200 px, paper) on the left third; 4.55 '90분' counts 0→90 in the middle third; 5.04 '과목별 40% 과락' lands on the right third in a RED (#E8213F) hand-drawn box and a red pen ✕ strikes through it (SVG stroke draw-on, pathLength 1000) + a short screen-shake. 6.01: the three facts slide down and shrink into a row at y≈880 (caption size), and the kick roll starts: 'q1' 'ADsP,' (Archivo Black ~260 px, accent) punches in at 6.48, 'q2' '나도 될까?' (Paperlogy 800 ~200 px, paper; '될까?' in a label box ACCENT with ink text, scaleX 0→1 from left) lands at 6.97 and HOLDS to 7.92; on 7.43 a micro shake + the question mark bounces. Hard cut at 7.92 (next frame flips to accent on the hit) — keep everything on screen until the very last frame."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 5.76s
- span_sec: [7.92, 13.68]
- pacing: beat_cut
- mood: [hype, triumphant]
- feel: SURGE — the drop lands on 7.92 with strong kicks 7.99 8.45, then a steady groove. Beats 7.92 8.41 8.87 9.36 | 9.85 10.31 10.80 11.29 | 11.75 12.24 12.72 13.21
- role: series0 (REVEAL)
- pattern_hint: BOOK3D slam + statement turn ("된다.")
- scene_color: #FFE500
- transition_out: stripes
- sfx: impact-bass-1@7.92, whoosh-short@7.99, pop@8.45, pop@9.36, whoosh@11.75
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [7.92, 9.85]
  - free_design: { dominant_system: "answer slam: burst lines + a CSS-3D book flying in toward camera", primitives: ["radial-burst-lines", "crash-zoom-in", "braam-punch"], density_topology: "explode → settle" }
  - anchors: [7.92, 7.99, 8.45, 9.36]
  - copy: { a1: "된다.", a2a: "빠르게", a2b: "따면." }
  - intent: "7.92 ACCENT ground at 0ms + ink radial burst lines from centre-right (flat ink wedges, no glow). 7.99 the CSS-3D book (recipe book3d.md; front = real cover, back = assets/book/back.jpg, spine = assets/book/spine.jpg; book ~430×588 scaled) crashes in from deep z / small scale at x≈1260 and lands in its rest pose (rotationY −28, rotationX 8) with a hard ink offset shadow plate on the ground. 8.45 'a1' '된다.' slams on the left (mega 360 px Paperlogy 800, ink), may crop off the left edge (data-layout-allow-overlap). 9.36 'a2a' + 'a2b' on one line under it: '빠르게' 800 / '따면.' 400 (h1 150 px, ink) — weight-contrast pair."
- **g2** — free_design
  - span_sec: [9.85, 13.68]
  - free_design: { dominant_system: "title lockup beside the slowly spinning 3D book", primitives: ["mask-reveal", "3d-card-flip"], density_topology: "settle → hold" }
  - anchors: [9.85, 10.80, 11.75, 12.72]
  - copy: { kicker: "노베이스도 한방에!", title: "2026 빠르게 따는 ADsP", sub: "데이터분석 준전문가 · 1권 이론 + 2권 빈출 족보·기출·모의고사", chip: "ADsP" }
  - intent: "9.85 '된다. 빠르게 따면.' clears left on a parabolic arc; the book glides to x≈1320. On the left (x 120–1000): 'kicker' small label (ink box, accent text, chip-ko 30 px) at 9.85; 'title' reveals with a mask wipe at 10.31 in two lines ('2026 빠르게 따는' h2 88 px 800 / 'ADsP' Archivo Black ~200 px in a INK label box with ACCENT text) and holds to the end (≥3 beats readable); 'sub' caption fades up at 10.80. 11.75 the book does one slow 360° Y-spin (front → spine → back cover → front, landing at 13.21) so the real back cover is seen. Keep the last 0.3 s calm (transition overlay covers the cut)."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 5.78s
- span_sec: [13.68, 19.46]
- pacing: beat_cut
- mood: [confident, clear]
- feel: breakdown bar (13.68) — space for a still — then groove back. Beats 13.68 14.16 14.65 15.12 | 15.60 16.09 16.56 17.04 | 17.53 18.00 18.48 18.97
- role: series1 (POINT 01 — 완독 = 2회독)
- pattern_hint: equation slam + 4-step highlighter path + real back cover hold
- scene_color: #F2F0EA
- transition_out: wipe
- sfx: pop@14.16, impact-bass-2@14.65, click-soft@15.60, click-soft@16.09, click-soft@16.56, click-soft@17.04, whoosh-short@17.53
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [13.68, 17.53]
  - free_design: { dominant_system: "an equation that slams together, then a 4-step study path ticked with a highlighter", primitives: ["braam-punch", "directional-fill", "staggered-exit"], density_topology: "build → accumulate" }
  - anchors: [14.16, 14.65, 15.60, 16.09, 16.56, 17.04]
  - copy: { label: "POINT 01", e1: "완독", e2: "=", e3: "2회독", sub: "이론 2회독 + 기출 2회독", steps: ["1권 이론", "2권 빈출 족보", "기출 · 모의고사", "빈출 XO"], effects: ["이론 1회독", "이론 2회독", "기출 1회독", "기출 2회독"] }
  - intent: "PAPER ground. Top-left side label 'POINT 01' (IBM Plex Mono label in an ink box). 14.16 'e1' '완독' slams left (display 240 px 800, ink); 14.65 '=' + 'e3' '2회독' slam right — '2회독' in an ACCENT label box with a yellow highlighter sweep under it; one short shake. 15.12 'sub' caption under the equation. 15.60–17.04: the equation shrinks up to y≈230 and a horizontal 4-step path appears across y≈560–760: one step card per beat (ink outline cards ~360×150, 'steps[i]' h2-ish 52 px 800 ink, 'effects[i]' as a small mono tag under it), each card gets a yellow highlighter sweep + a ✓ in RED pen as it lands; a dashed connector draws between cards."
- **g2** — free_design
  - span_sec: [17.53, 19.46]
  - free_design: { dominant_system: "the real back cover as evidence — a tossed card with a slow camera push", primitives: ["crash-zoom-in", "staggered-exit"], density_topology: "replace → hold" }
  - anchors: [17.53, 18.48]
  - copy: { cap1: "뒤표지에 다 있다", cap2: "비전공자·노베이스용 / 빠르게 따는 / 책과 함께하는 학습법" }
  - intent: "17.53 the steps clear (parabolic arcs, staggered). The REAL back cover assets/book/back.jpg (never cropped/tinted/no text on it; ~560×766, rotation −4°, hard ink offset shadow) is tossed in from the right to x≈1250 and then pushes in slowly (scale 1 → 1.08) — a ≥1.5 s still to read. Left side: 'cap1' (h1 150 px 800, ink, '다 있다' in an accent label box) at 17.53 and 'cap2' (caption 34 px, three lines) at 18.48. Keep the last 0.3 s calm."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 5.73s
- span_sec: [19.46, 25.19]
- pacing: beat_cut
- mood: [focused, calm]
- feel: thinned groove, near-silent breakdown from 23.3 — beat-typed UI. Beats 19.46 19.92 20.41 20.88 | 21.36 21.83 22.31 22.80 | 23.29 23.75 24.24 24.73
- role: series2 (POINT 02 — 손안의 CBT)
- pattern_hint: original phone CBT mockup + OMR marks per beat
- scene_color: #1E2687
- transition_out: iris
- sfx: click@19.92, click@20.41, click@20.88, ping@21.36, typing@22.31, pop@23.29, pop@23.75, pop@24.24
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [19.46, 25.19]
  - free_design: { dominant_system: "an original phone mockup running a mock-exam CBT; answers marked one per beat; feature chips pop beside it", primitives: ["typewriter-reveal", "counting-punch", "word-grid-burst"], density_topology: "build → accumulate → hold" }
  - anchors: [19.46, 19.92, 20.41, 20.88, 21.36, 22.31, 23.29, 23.75, 24.24]
  - copy: { label: "POINT 02", t1: "지하철에서도", t2: "실전처럼.", chip: "웹 CBT · PC / 모바일", n_a: "모의고사 5회", plus: "+", n_b: "기출 5회", feats: ["중간 저장", "일시 정지", "힌트 보기"], phone_title: "ADsP 모의고사 1회", phone_q: "Q1. 다음 중 DIKW 피라미드의 순서로 옳은 것은?", phone_timer: "89:59" }
  - intent: "INK ground. Side label 'POINT 02' top-left (accent box, mono). 19.46: an ORIGINAL flat phone mockup (rounded rect ~420×860, paper screen, ink 14 px bezel, no real brand UI) rises in at x≈520 with a slight −6° tilt. On its screen: header 'phone_title' + mono timer 'phone_timer' ticking down (0ms digit swaps on beats), question 'phone_q' (Paperlogy 500 26 px, ink), four OMR-style answer bubbles ①②③④. 19.92 / 20.41 / 20.88 the screen advances Q1→Q2→Q3 (0ms content-swap) and each time one bubble fills solid ink like a computer-sign pen mark (click). Right side (x 1000–1820): 19.46 't1' (h1 150 px 800, paper) and 20.41 't2' (h1-light 400, paper; '실전처럼' with accent underline draw). 21.36 'chip' pops (accent box, ink text). 22.31 the counts: '모의고사 5회 + 기출 5회' — numerals count 0→5 in IBM Plex Mono 700 accent ~140 px, words Paperlogy 800 72 px paper. 23.29 / 23.75 / 24.24 the three 'feats' chips pop in a row under it (paper outline pills, overshoot) and the phone shows a matching icon each time (save ✓, pause ‖, hint 💡 drawn as simple SVG line icons). Hold the full layout from 24.24 to the end; last 0.3 s calm (iris covers the cut)."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 6.02s
- span_sec: [25.19, 31.21]
- pacing: beat_cut
- mood: [build, euphoric]
- feel: the quietest bar (25.19) building through 27.26 into the strongest SURGE at 29.28 (kick 29.49), DROP-ish 31. Beats 25.19 25.68 26.17 26.73 | 27.26 27.79 28.33 28.79 | 29.28 29.77 30.26 30.72
- role: series3 (POINT 03 — 합격 토탈 패키지) + CLIMAX
- pattern_hint: SERIES-TOSS-style token build → CLIMAX-SLAM on the strongest surge
- scene_color: #F2F0EA
- transition_out: none
- sfx: pop@25.19, pop@25.68, pop@26.17, pop@26.73, pop@27.26, riser@27.79, impact-bass-2@29.28, sparkle@29.77
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [25.19, 29.28]
  - free_design: { dominant_system: "the package equation assembled one token per beat, then a stamped 'Live 특강' ticket", primitives: ["word-grid-burst", "overlay-pop", "staggered-exit"], density_topology: "accumulate" }
  - anchors: [25.19, 25.68, 26.17, 26.73, 27.26, 27.79, 28.33]
  - copy: { label: "POINT 03", tokens: ["책", "특강", "CBT", "카페", "단톡"], ticket: "시험 직전 Live 마무리 특강", sum: "합격 토탈 패키지" }
  - intent: "PAPER ground, side label 'POINT 03'. One token per beat on a centred line (y≈420): 25.19 '책' … 27.26 '단톡', each in its own INK label box with paper text (h1 150 px 800), joined by '+' signs in accent-on-ink circles; each token pops with overshoot and a tiny geometric confetti (● ■ ▲) on landing. 27.79 'sum' types in under the line (h2 88 px, ink, highlighter sweep). 28.33 a ticket-shaped card 'ticket' (accent ground, ink text, perforated edge drawn with dashes) slides up from the bottom and a round RED '합격' stamp thumps onto its corner (scale 1.6→1 + shake). Everything stays until 29.28."
- **g2** — free_design
  - span_sec: [29.28, 31.21]
  - free_design: { dominant_system: "climax slam of the cover's own tagline with burst lines and confetti", primitives: ["palette-flip", "braam-punch", "radial-burst-lines", "particle-burst", "screen-shake"], density_topology: "explode → freeze" }
  - anchors: [29.28, 29.49, 29.77, 30.26]
  - copy: { c1: "노베이스도", c2: "한방에!" }
  - intent: "29.28 0ms flip to INK, everything from g1 gone. 'c1' '노베이스도' (h1-light 150 px 400, paper) lands upper-left; 29.49 (kick) 'c2' '한방에!' MEGA (360 px 800, ACCENT) slams in with ink-on-accent radial burst lines behind and flat geometric confetti (● ■ ▲ ○ ✕ ◆ in accent/paper) bursting out; 30.26 '한방에!' gets an accent label-box pulse + one screen-shake. Freeze the composition 30.72 → 31.21 (hard cut to the finale)."

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 9.64s
- span_sec: [31.21, 40.85]
- pacing: beat_cut
- mood: [triumphant, resolved]
- feel: full groove to the end; strong bars 31.21, 35.06, 36.97; last hit ~40.05; music fades out in the final 0.8 s. Beats 31.21 31.67 32.16 32.65 | 33.13 33.60 34.09 34.58 | 35.06 35.53 36.01 36.48 | 36.97 37.43 37.92 38.41 | 38.89 39.36 39.84 40.33
- role: finale
- pattern_hint: book + stat bubbles → lockup → CTA (FINALE-BURST variant with the 3D book)
- scene_color: #1E2687
- transition_out: none
- sfx: whoosh-short@31.21, pop@32.16, pop@33.13, pop@34.09, whoosh@35.06, chime@36.97, click@37.92, sparkle@38.89
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [31.21, 35.06]
  - free_design: { dominant_system: "3D book centre stage, three count-up stat cards popping around it", primitives: ["counting-punch", "overlay-pop", "3d-card-flip"], density_topology: "accumulate" }
  - anchors: [31.21, 32.16, 33.13, 34.09]
  - copy: { s1n: "80", s1: "빈출 족보 테마", s2n: "4", s2: "2025 최신 기출 (회분)", s3n: "3", s3: "LEVEL 모의고사 (회분)", s4: "+ 유튜브 무료 강의 · 카페 Q&A" }
  - intent: "INK ground. 31.21 the CSS-3D book (same recipe/assets as f2) swings in to centre (rest pose, slow idle sway ±4°). Stat cards (paper cards ~360×200, 0 radius, accent hard offset shadow) pop around it one per beat: 32.16 upper-left 's1n'+'s1' (numeral counts 0→80, IBM Plex Mono 700 120 px ink), 33.13 lower-left 's2n'+'s2' (0→4), 34.09 right 's3n'+'s3' (0→3); 34.58 's4' caption (paper, 34 px) along the bottom. Cards never overlap the book."
- **g2** — free_design
  - span_sec: [35.06, 40.85]
  - free_design: { dominant_system: "lockup: book left, title + where-to-buy + logo + URL right; final icon burst", primitives: ["staggered-exit", "mask-reveal", "particle-burst"], density_topology: "replace → hold" }
  - anchors: [35.06, 36.01, 36.97, 37.92, 38.89]
  - copy: { title1: "2026 빠르게 따는", title2: "ADsP", where: "예스24 · 교보문고 · 알라딘", url: "goldenrabbit.co.kr", brand: "골든래빗" }
  - intent: "35.06 the stat cards fly out on parabolic arcs; the book glides left to x≈560 (scale up slightly). Right column (x 980–1800): 'title1' (h2 88 px 800, paper) + 'title2' (Archivo Black ~220 px, ACCENT) mask-reveal at 35.06; 36.01 'where' (caption 34 px paper, with a thin accent rule above). 36.97 the gold logo mark assets/brand/icon.png (~120 px, the ONLY gold) pops in with 'brand' wordmark text beside it (Paperlogy 800 48 px, paper); 37.92 'url' in an ACCENT label box (ink text, IBM Plex Mono 700 44 px) snaps on scaleX 0→1. 38.89 a ring of six small flat line icons (book, check, phone, star, chat, stamp — simple SVG strokes in accent/paper) bursts around the logo and settles. Hold everything still to 40.85 (music fades)."
