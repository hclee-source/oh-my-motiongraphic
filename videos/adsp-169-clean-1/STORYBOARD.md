---
compositionId: bgm
duration_s: 40.85 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "비전공자·노베이스도 ADsP, 빠르게 따는 책 한 권이면 된다"
variant: { name: adsp-169-clean-1, style: bold-beat, aspect: "16:9", seed: 7, intensity: standard }
style:
  font: "Paperlogy 800/400 (embedded, Korean) / Archivo Black (Latin caps) / Playfair Display italic 700 (mixed-word lowercase) / IBM Plex Mono (numerals)"
  palette: ["#FFE500", "#1E2687", "#F2F0EA", "#CEAE73"]
assets: "assets/covers/9791194383697.jpg (real front cover 1080×1476); assets/book/back.jpg (real back cover 877×1200: 학습법 3종 블록 + QR); assets/book/spine.jpg (real spine 88×1200); assets/brand/icon.png (gold logo mark), assets/brand/logo.png; assets/fonts/ Paperlogy 4/5/6/7/8"
build_notes:
  - "follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)"
  - "no HUD in this variant — keep readable content in y 96–984, x 96–1824"
  - "2025–26 grammar (research/kr-edu-ads-2026/FINDINGS.md): hold ONE ground per frame (no beat-by-beat colour flips), stack mid-size type instead of replacing mega words, ≤12 readable chars per screen and ≤2 text chunks at once, no Latin chip labels, one accent word per screen, entrances = blur-in / spring / syllable reveal rather than scale slams, mega type at most once per frame"
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
- mood: [relatable, curious]
- feel: quiet 4-on-the-floor intro (bars 0–2) → kick accel-roll from 6.0 into the big hit at 7.92 (next frame). Beats 0.21 0.72 1.21 1.67 | 2.16 2.65 3.13 3.60 | 4.09 4.55 5.04 5.53 | 6.01 6.48 6.97 7.43
- role: intro (HOOK — search-bar autocomplete)
- pattern_hint: SEARCH-AUTOCOMPLETE (new, 2025–26 grammar: one held ground, UI as the viewer's inner voice, stacked list, product as the answer)
- scene_color: #1E2687
- transition_out: none
- sfx: key-press@0.72, key-press@1.21, key-press@1.67, key-press@2.16, pop@2.65, pop@3.13, pop@3.60, pop@4.09, click@4.55, whoosh-short@5.04, riser@6.01

### Groups

- **g1** — free_design
  - span_sec: [0.0, 4.55]
  - free_design: { dominant_system: "an original search bar: the query types in, autocomplete rows stack one per beat", primitives: ["typewriter-reveal", "staggered-exit"], density_topology: "accumulate" }
  - anchors: [0.21, 0.72, 2.16, 2.65, 3.13, 3.60, 4.09]
  - copy: { query: "ADsP 비전공자 독학", rows: ["ADsP 노베이스 합격", "ADsP 통계 몰라도", "ADsP 과락 40%", "ADsP 책 추천"] }
  - intent: "INK ground #1E2687 held for the WHOLE frame — no colour flips. A flat subtle paper-dot grid texture at 6% is fine; no gradients. 0.0–0.21: an ORIGINAL search bar (no Google/Naver branding — a plain rounded pill ~1100×120, paper #F2F0EA, 0 shadow blur, a 6 px accent offset shadow, a simple drawn magnifier icon on the left) rises into place at y≈300 with a soft spring (back.out(1.4), 0.4 s) and a blinking caret (blink via 0ms tl.set on beats, seek-safe). 0.72–2.16: 'query' types in character by character (Paperlogy 800 ~58 px ink) — chars spread evenly across 0.72→2.16 so typing feels human; the word '비전공자' gets a thin accent underline after it lands. 2.65 / 3.13 / 3.60 / 4.09: an autocomplete dropdown grows under the bar (paper panel, ink 2 px hairline dividers) and ONE row is added per beat (each row: small magnifier icon + text Paperlogy 500 ~44 px ink, slides down 12 px + blur 8px→0 + fade in, 0.3 s power3.out). Earlier rows stay fully readable (stacked list, not replaced). On 4.09 the last row 'ADsP 책 추천' gets an accent highlight bar behind it (the only accent word on screen). Keep everything at mid size (text ≤ 58 px) — no mega type in this group."
- **g2** — free_design
  - span_sec: [4.55, 7.92]
  - free_design: { dominant_system: "click → the answer card springs in where the results would be → camera push into the cover", primitives: ["crash-zoom-in", "overlay-pop"], density_topology: "replace → push" }
  - anchors: [4.55, 5.04, 6.01, 6.97, 7.43]
  - copy: { result: "2026 빠르게 따는 ADsP", meta: "골든래빗 · 임한울 외" }
  - intent: "Same INK ground. 4.55: a drawn cursor arrow clicks the row 'ADsP 책 추천' (row flashes accent for 2 frames, click), then the dropdown folds up into the bar (0.25 s) and the bar slides up to y≈150 and scales 0.8. 5.04: ONE result card springs in centre (paper card ~920×420, 0 radius, 8 px accent offset shadow, back.out(1.6) from scale 0.9 + y 40 + blur 10→0): on its left the REAL cover assets/covers/9791194383697.jpg (~250×342, never cropped/tinted/no text on it), on its right 'result' (Paperlogy 800 ~56 px ink) and under it 'meta' (Paperlogy 500 ~30 px ink at 70%). Hold readable 5.04→6.01 (2 beats). 6.01→7.92 (the kick accel-roll): slow-then-fast camera push into the cover — the card scales up around the cover's centre (scale 1 → ~3.2, power3.in) so the cover fills the frame by 7.85; the rest of the card/bar leaves frame naturally. Light 1-frame shake on 6.97 and 7.43 only. Last frame = cover large in centre (hard cut to f2's book on the hit)."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 5.76s
- span_sec: [7.92, 13.68]
- pacing: beat_cut
- mood: [hype, triumphant]
- feel: SURGE — the drop lands on 7.92 with strong kicks 7.99 8.45, then a steady groove. Beats 7.92 8.41 8.87 9.36 | 9.85 10.31 10.80 11.29 | 11.75 12.24 12.72 13.21
- role: series0 (REVEAL)
- pattern_hint: BOOK3D land + one mega statement (the only mega moment before the climax)
- scene_color: #FFE500
- transition_out: stripes
- sfx: impact-bass-1@7.92, whoosh-short@7.99, pop@8.45, pop@9.36, whoosh@11.75
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [7.92, 9.85]
  - free_design: { dominant_system: "answer statement + the CSS-3D book landing (no burst lines)", primitives: ["crash-zoom-in", "braam-punch"], density_topology: "land → settle" }
  - anchors: [7.92, 7.99, 8.45, 9.36]
  - copy: { a1: "된다.", a2a: "빠르게", a2b: "따면." }
  - intent: "(REVISION of the existing file — keep the 3D book build and timings.) ACCENT ground held for the whole frame. REMOVE the radial burst wedges and the ring of ink ticks entirely — instead one soft concentric ring pulse (2 px ink outline circle scaling 0.6→1.6 while fading, single, 0.5 s) behind the book on 7.99. Keep the book crash-in and rest pose, '된다.' mega (this is the frame's single mega) and '빠르게 따면.' weight pair. Soften entrances: '된다.' = scale 1.08→1 + blur 12px→0 + fade over 0.18 s with a tiny overshoot instead of the 1.3× slam/camera punch; keep at most one micro shake."
- **g2** — free_design
  - span_sec: [9.85, 13.68]
  - free_design: { dominant_system: "title lockup beside the slowly spinning 3D book", primitives: ["mask-reveal", "3d-card-flip"], density_topology: "settle → hold" }
  - anchors: [9.85, 10.31, 10.80, 11.75, 12.72]
  - copy: { title: "2026 빠르게 따는 ADsP", sub: "데이터분석 준전문가" }
  - intent: "(REVISION.) Keep the arc exit of g1, the book glide and the 360° spin. Text chunks on screen ≤ 2: the title ('2026 빠르게 따는' + 'ADsP' label box) and 'sub' only. DELETE the kicker label '노베이스도 한방에!' (it's the climax line later) and replace the long two-line sub caption with just '데이터분석 준전문가' (Paperlogy 500 ~40 px ink)."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 5.78s
- span_sec: [13.68, 19.46]
- pacing: beat_cut
- mood: [confident, clear]
- feel: breakdown bar (13.68) — space for a still — then groove back. Beats 13.68 14.16 14.65 15.12 | 15.60 16.09 16.56 17.04 | 17.53 18.00 18.48 18.97
- role: series1 (완독 = 2회독)
- pattern_hint: equation + 4-step path (short labels) + real back cover hold
- scene_color: #F2F0EA
- transition_out: wipe
- sfx: pop@14.16, impact-bass-2@14.65, click-soft@15.60, click-soft@16.09, click-soft@16.56, click-soft@17.04, whoosh-short@17.53
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [13.68, 17.53]
  - free_design: { dominant_system: "the equation, then a 4-step path with short labels ticked one per beat", primitives: ["braam-punch", "directional-fill"], density_topology: "build → accumulate" }
  - anchors: [14.16, 14.65, 15.60, 16.09, 16.56, 17.04]
  - copy: { e1: "완독", e2: "=", e3: "2회독", steps: ["이론", "족보", "기출", "XO"] }
  - intent: "(REVISION of the existing file.) DELETE the 'POINT 01' label, the sub caption '이론 2회독 + 기출 2회독' and the per-card effect tags. Make the equation BIG and central (it is this frame's single big text, ~200 px; '2회독' keeps the accent box). The 4-step path becomes four compact cards with ONE short word each ('steps', Paperlogy 800 ~64 px) — wider spacing, bigger, centred under the equation, ✓ in red pen per beat as now. Blur-in entrances (blur 10→0 + y 16→0) instead of hard slams; at most one micro shake on '2회독'. Fill the frame better: equation centred around y≈380, path around y≈700."
- **g2** — free_design
  - span_sec: [17.53, 19.46]
  - free_design: { dominant_system: "the real back cover as evidence — a tossed card with a slow camera push", primitives: ["crash-zoom-in"], density_topology: "replace → hold" }
  - anchors: [17.53]
  - copy: { cap1: "뒤표지에 다 있다" }
  - intent: "(REVISION.) Keep the back cover toss + push exactly. DELETE 'cap2' (the three-line list). Keep only 'cap1'."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 5.73s
- span_sec: [19.46, 25.19]
- pacing: beat_cut
- mood: [focused, calm]
- feel: thinned groove, near-silent breakdown from 23.3 — beat-typed UI. Beats 19.46 19.92 20.41 20.88 | 21.36 21.83 22.31 22.80 | 23.29 23.75 24.24 24.73
- role: series2 (PC·모바일 CBT)
- pattern_hint: original phone CBT mockup + OMR marks per beat
- scene_color: #1E2687
- transition_out: iris
- sfx: click@19.92, click@20.41, click@20.88, typing@22.31, pop@23.29, pop@23.75, pop@24.24
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [19.46, 25.19]
  - free_design: { dominant_system: "an original phone mockup running a mock-exam CBT; answers marked one per beat", primitives: ["typewriter-reveal", "counting-punch"], density_topology: "build → replace → hold" }
  - anchors: [19.46, 19.92, 20.41, 20.88, 22.31, 23.29, 23.75, 24.24]
  - copy: { t1: "PC도 폰도", t2: "실전처럼.", n_a: "모의고사 5회", plus: "+", n_b: "기출 5회" }
  - revision_3: "user: the CBT works on desktop AND mobile, so do not push mobile only. Added an original flat desktop monitor behind the phone (same CBT; its OMR answer sheet fills on the same beats as the phone), phone scaled 0.7 in front, t1 changed to PC도 폰도. Also f2: book page-edge stripes made opaque (semi-transparent ink let the back cover bleed through as red/blue stripes)."
  - intent: "(REVISION of the existing file — keep the phone, its screen, timer, OMR marks and the save/pause/hint toolbar icon lighting at 23.29/23.75/24.24.) Text chunks beside the phone ≤ 2 at any moment: 19.46–22.31 show t1+t2; at 22.31 REPLACE them (t1/t2 slide up + fade) with the counts line '모의고사 5회 + 기출 5회' (numerals still count 0→5). DELETE the 'POINT 02' label, the chip '웹 CBT · PC / 모바일' and the three feature pills (the phone toolbar icons lighting up carry that message; keep the phone toast text)."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 6.02s
- span_sec: [25.19, 31.21]
- pacing: beat_cut
- mood: [build, euphoric]
- feel: the quietest bar (25.19) building through 27.26 into the strongest SURGE at 29.28 (kick 29.49), DROP-ish 31. Beats 25.19 25.68 26.17 26.73 | 27.26 27.79 28.33 28.79 | 29.28 29.77 30.26 30.72
- role: series3 (합격 토탈 패키지) + CLIMAX
- pattern_hint: token stack → ticket + stamp → climax (single colour change)
- scene_color: #F2F0EA
- transition_out: none
- sfx: pop@25.19, pop@25.68, pop@26.17, pop@26.73, pop@27.26, riser@27.79, impact-bass-2@29.28, sparkle@29.77
- book: 9791194383697 | 2026 빠르게 따는 ADsP | 임한울, 조영훈, 이유성 | | assets/covers/9791194383697.jpg

### Groups

- **g1** — free_design
  - span_sec: [25.19, 29.28]
  - free_design: { dominant_system: "the package tokens stacked one per beat, then a Live 특강 ticket with a stamp", primitives: ["word-grid-burst", "overlay-pop"], density_topology: "accumulate" }
  - anchors: [25.19, 25.68, 26.17, 26.73, 27.26, 28.33]
  - copy: { tokens: ["책", "특강", "CBT", "카페", "단톡"], ticket: "시험 직전 Live 마무리 특강" }
  - intent: "(REVISION of the existing file.) DELETE the 'POINT 03' label and the '합격 토탈 패키지' line (too many chunks). Keep the five tokens + '+' circles and the ticket + red 합격 stamp, but move the ticket up to sit under the tokens (two chunks total). Token entrances: spring + blur-in (no confetti on each token; one small confetti puff only on the 5th token)."
- **g2** — free_design
  - span_sec: [29.28, 31.21]
  - free_design: { dominant_system: "climax: the cover's own tagline, one colour change, a clean ring burst", primitives: ["palette-flip", "braam-punch", "particle-burst"], density_topology: "explode → freeze" }
  - anchors: [29.28, 29.49, 29.77, 30.26]
  - copy: { c1: "노베이스도", c2: "한방에!" }
  - intent: "(REVISION.) Keep the cut to INK and '노베이스도' + mega '한방에!' with its accent label box (this is the climax — the one allowed mega + colour change). REPLACE the 24 radial burst lines with two thin concentric accent rings expanding from behind the word (scale 0.7→1.5, fading). Reduce confetti to ~10 pieces, spaced evenly around the word. Keep one screen-shake on 30.26."

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
