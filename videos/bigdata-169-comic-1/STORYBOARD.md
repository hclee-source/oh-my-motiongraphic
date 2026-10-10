---
compositionId: bgm
duration_s: 42.71 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "비전공자·노베이스도 빅데이터분석기사 필기, 빠르게 따는 책 한 권으로 한방에"
variant: { name: bigdata-169-comic-1, style: bold-beat, aspect: "16:9", seed: 21, intensity: standard }
style:
  font: "Paperlogy 800/400 (embedded, Korean) / Archivo Black (Latin caps) / IBM Plex Mono (numerals)"
  palette: ["#008D41", "#222685", "#FEF21C", "#F2F0EA", "#CEAE73"]
assets: "assets/covers/9791124516317.jpg (real front cover 1080×1476: green ground, comic starburst, '노베이스도 한방에!', bat + spark lower-right); assets/book/back.jpg (real back cover 877×1200); assets/book/spine.jpg (real spine 126×1200); assets/brand/icon.png (gold logo mark); assets/characters/{stance,swing,slide,thumbs,cheer}.png (user's baseball character, transparent PNGs — place, never redraw; swing/thumbs/cheer are cut flat at the bottom → hang them from the frame's bottom edge); assets/fonts/ Paperlogy"
build_notes:
  - "follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)"
  - "no HUD in this variant — keep readable content in y 96–984"
  - "read frame.md incl. the 'Big Data variant addendum': green register #008D41, comic devices (starburst, lightning, speed lines, impact spark), house grammar (one held ground per frame, ≤12 readable chars per screen, ≤2 text chunks, blur-in/spring entrances, mega type at most once per frame)"
  - "the reference for the look is videos/adsp-169-clean-1 (user-approved) — same type ramp, label boxes, offset shadows; this video swaps its search-bar/stack grammar for comic speech bubbles and the cover's starburst"
  - "characters = the user's art: plain <img> elements animated with transforms, never filtered/tinted/recoloured; keep them in empty corners, never over copy or the cover"
  - "CSS-3D book: follow .claude/skills/goldenrabbit-promo/references/recipes/book3d.md; front = assets/covers/9791124516317.jpg, back = assets/book/back.jpg, spine = assets/book/spine.jpg; page block + top = SOLID #F4EFE6 (no stripes — they moiré in H.264)"
  - "facts are fixed — use the copy verbatim; never add '4주 합격', '+10점', '85개 테마', rankings or pass rates"
avoid: ["text over covers", "gradients/glows", "copying reference videos' copy or layouts", "unsupported claims (4주 합격, +10점, 1위, 합격률)", "characters on the hook or on the reveal"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 6.78s
- span_sec: [0.0, 6.78]
- pacing: beat_cut
- mood: [relatable, curious]
- feel: sparse intro (VOID/LOW; hats + light kick), beats 0.49 0.97 1.46 1.95 | 2.44 2.93 3.41 3.90 | 4.39 4.85 5.34 5.83 | 6.32 → first SURGE on the 6.78 downbeat (next frame)
- role: intro (HOOK — comic speech bubbles)
- pattern_hint: COMIC-BUBBLES (new): the back cover's worry line as comic balloons, answered by a 'NO' stamp
- scene_color: #008D41
- transition_out: none
- sfx: pop@0.97, pop@1.95, pop@2.93, pop@3.90, impact-bass-1@4.85, whoosh-short@6.55

### Groups

- **g1** — free_design
  - span_sec: [0.0, 6.78]
  - free_design: { dominant_system: "speech balloons pop one per bar half, then a stamp answers them", primitives: ["overlay-pop", "kinetic-letter-in"], density_topology: "accumulate → answer" }
  - anchors: [0.97, 1.95, 2.93, 3.90, 4.85, 5.83]
  - copy: { b1: "비전공자", b2: "노베이스", q: "걱정되나요?", stamp: "고민 NO!" }
  - intent: "GREEN ground #008D41 held for the whole frame (subtle paper-dot halftone at 6% is fine, flat). 0.97 / 1.95: two comic speech balloons pop in (paper #F2F0EA fill, 6 px ink outline, a pointed tail, 6 px hard offset shadow ink) — balloon 1 upper-left with 'b1', balloon 2 lower-right with 'b2' (Paperlogy 800 ~92 px ink). Each pops scale 0.6→1 with a spring (back.out(1.6), 0.3 s) + a tiny 2-line 'burst' tick mark beside it. 2.93: 'q' lands centred between them in a bigger rounded balloon (Paperlogy 800 ~110 px ink, '걱정' may carry a yellow highlighter sweep). 3.90: the three balloons wobble once (rotation ±2°). 4.85 (beat with impact): a ROUND rubber stamp 'stamp' slams centre-right over the balloons' gap (ink #222685 disc with a 10 px accent #FEF21C ring, accent text Paperlogy 800 ~84 px, rotated −12°), scale 1.6→1 power3.in 0.12 s + 4-frame screen shake; at the same moment balloons 1–2 deflate slightly (scale 0.94). 5.83→6.78: everything holds; on 6.55 the balloons whip off left with speed lines so the frame ends on the stamp alone on green (hard cut to f2's burst on the 6.78 surge). No character in this frame."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 5.81s
- span_sec: [6.78, 12.59]
- pacing: beat_cut
- mood: [hype, triumphant]
- feel: SURGE on 6.78 into HIGH 7–13. Beats 6.78 7.27 7.75 8.24 | 8.73 9.22 9.68 10.17 | 10.66 11.15 11.63 12.12. Strong: hat 7.73, kick 8.78, hat 9.64, hat 11.59
- role: series0 (REVEAL)
- pattern_hint: STARBURST-REVEAL (new) + BOOK3D land
- scene_color: #222685
- transition_out: none
- sfx: impact-bass-2@6.78, whoosh@6.80, sparkle@8.78, pop@10.66
- book: 9791124516317 | 2027 빠르게 따는 빅데이터분석기사 필기 | 이유성, 조영훈 | | assets/covers/9791124516317.jpg

### Groups

- **g1** — free_design
  - span_sec: [6.78, 12.59]
  - free_design: { dominant_system: "the cover's own comic starburst explodes and the 3D book lands inside it; title stacks beside", primitives: ["radial-burst-lines", "crash-zoom-in", "kinetic-letter-in"], density_topology: "explode → hold" }
  - anchors: [6.78, 7.27, 7.75, 8.78, 9.68, 10.66]
  - copy: { t1: "2027 빠르게 따는", t2: "빅데이터분석기사", t3: "필기" }
  - intent: "INK ground #222685 held. 6.78: a big flat comic STARBURST (14 spikes, accent #FEF21C fill, 10 px ink-darker outline #0E0C33, ~980 px) slams in centred at x≈1250 (scale 0.2→1, power4.out 0.18 s) with ~16 paper speed lines radiating behind it (scale out + fade 0.4 s) and a 1-frame paper flash at 18% (fade 0.12 s). 6.78–7.4: the CSS-3D book (430×588, ~0.95 scale) crash-zooms in at the starburst centre (scale 2.2→1, rotateY −28°→−14°, power3.out 0.5 s), soft shadow below; through the rest of the frame the book drifts rotateY −14°→−8°. 7.75: two small lightning bolts (accent, ink outline) zap in at the starburst's upper-left and lower-right spikes (scale 0→1 back.out, then a 2-frame flicker on 8.78). 8.78 (kick): one white-yellow impact spark pops at the book's lower-right corner — where the cover's own bat spark is — (8-point star, scale 0→1.2→1, 0.25 s). LEFT column x 120–720, stacked, left-aligned: 7.27 't1' (Paperlogy 800 ~64 px paper), 7.75 't2' (Paperlogy 800 ~104 px accent — the hero line; may wrap onto two lines '빅데이터' / '분석기사' if wider than 600 px), 8.24 't3' in a paper label box with ink text (~80 px). Each line blur-in + y 30→0 (0.3 s power3.out). Hold all to 12.3; 12.3→12.59 the starburst shrinks 1→0.9 and everything keeps still (hard cut). Text never over the book. No character in this frame."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 7.75s
- span_sec: [12.59, 20.34]
- pacing: beat_cut
- mood: [focused, playful]
- feel: MEDIUM 13–16, LOW 16–17, MEDIUM 17–19, LOW 19–20 building into the big SURGE at 20.34. Beats 13.07 13.56 14.05 14.54 | 15.02 15.51 15.97 16.46 | 16.95 17.44 17.93 18.41 | 18.90 19.36 19.85. Kicks 14.58 16.51 18.46
- role: series1 (완독 = 2회독 — the diamond)
- pattern_hint: BASEBALL-DIAMOND (new): the back cover's 4 study steps as the 4 bases; crossing home = 2회독
- scene_color: #008D41
- transition_out: wipe
- sfx: click@13.07, click@14.54, click@16.46, click@18.41, bat-crack@18.46, impact-bass-1@19.36, whoosh-short@20.10

### Groups

- **g1** — free_design
  - span_sec: [12.59, 20.34]
  - free_design: { dominant_system: "a flat baseball diamond seen from above; each base lights with its study step on a bar line; a runner's path draws base to base; home = 2회독", primitives: ["typewriter-reveal", "overlay-pop"], density_topology: "path → payoff" }
  - anchors: [12.59, 13.07, 14.54, 16.46, 18.41, 19.36]
  - copy: { b1: "1권 이론", b2: "2권 빈출 족보", b3: "기출 + 모의고사", home: "빈출 XO", eq1: "완독", eq2: "=", eq3: "2회독" }
  - intent: "GREEN ground #008D41 held (the field). A flat diamond (a square rotated 45°, ~620 px side, paper #F2F0EA 8 px chalk lines, infield slightly darker green #0B6652) sits centred at x≈760, y≈560; four bases = paper squares (60 px, ink 4 px outline) at 1st (right), 2nd (top), 3rd (left), home (bottom, pentagon). 12.59–13.07: diamond lines draw in (stroke-dashoffset, 0.45 s). Then ONE base per bar line, in running order: 13.07 1st, 14.54 2nd, 16.46 3rd, 18.41 HOME — each base fills accent #FEF21C (scale punch 1.25→1) and its step label pops next to it on a small ink label box with paper text (Paperlogy 800 ~40 px): 1st 'b1', 2nd 'b2', 3rd 'b3', home 'home'. A dashed accent runner path draws from home→1st→2nd→3rd→home, each leg finishing on its base's bar line (eased). Labels stay readable (≤ 2 new chunks at a time; earlier labels may dim to 70%). 18.41 (kick): the user's character slide.png (~520 px wide) SLIDES into home from the left side of the plate (x −700 → final, power3.out 0.35 s) with a few flat dust puffs (paper circles) — keep it below/left of the home label, never over the equation. 19.36: on the RIGHT (x 1180–1800) the equation lands stacked: 'eq1' Paperlogy 800 ~140 px paper, 'eq2', 'eq3' in an accent label box with ink text ~170 px (the only mega moment) — blur-in + spring; hold to 20.2. 'wipe' transition out."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 5.81s
- span_sec: [20.34, 26.15]
- pacing: beat_cut
- mood: [focused, energetic]
- feel: SURGE on 20.34, HIGH 20–28. Beats 20.34 20.83 21.32 21.78 | 22.27 22.76 23.24 23.73 | 24.20 24.68 25.17 25.66
- role: series2 (CBT & 용어 학습)
- pattern_hint: DEVICE-SYNC (house) + a term-card flip
- scene_color: #222685
- transition_out: iris
- sfx: click-soft@20.83, click-soft@21.32, click-soft@21.78, pop@22.27, whoosh-short@24.18, pop@24.20, chime@25.17

### Groups

- **g1** — free_design
  - span_sec: [20.34, 24.20]
  - free_design: { dominant_system: "original flat desktop monitor + phone running the same mock exam; the same answer fills on both per beat", primitives: ["counting-punch", "typewriter-reveal"], density_topology: "build → replace" }
  - anchors: [20.34, 20.83, 21.32, 21.78, 22.27]
  - copy: { t1: "PC도 폰도", t2: "실전처럼", n: "기출변형 4회 + 모의고사 3회", ui: "빅데이터분석기사 필기 모의고사" }
  - intent: "INK ground held. Reuse the DEVICE-SYNC idea of videos/adsp-169-clean-1/compositions/frames/04-f4.html (monitor behind, phone in front, an OMR answer column on the monitor's LEFT so the phone never hides it), restyled: monitor bezel paper, screen paper, accent offset shadow 14 px. 20.34: devices land (monitor spring from y +60, phone 0.12 s later). 20.83 / 21.32 / 21.78: one answer per beat fills on phone + monitor question + monitor answer sheet together. Right column x 1080–1820: 20.40 't1' (Paperlogy 800 ~120 px paper) + 't2' (Paperlogy 400 ~120 px paper, accent underline draws on 20.83). 22.27: t1/t2 slide up and out; 'n' replaces them (Paperlogy 800 ~64 px, the numerals '4' and '3' in accent, counting 0→N with 0 ms text swaps). The UI header text 'ui' is small (~22 px) inside the screens. 22.76: the user's character thumbs.png (~340 px tall) pops up from the bottom edge at x≈1700 (back.out 0.4 s; its flat crop sits on the frame's bottom edge) — keep it clear of the copy; stays to 24.0 then drops out."
- **g2** — free_design
  - span_sec: [24.20, 26.15]
  - free_design: { dominant_system: "a vocabulary card flips: term on the front, plain-language meaning on the back", primitives: ["3d-card-flip"], density_topology: "single" }
  - anchors: [24.20, 24.68, 25.17]
  - copy: { label: "CBT & 용어 학습", term: "과적합", meaning: "학습 데이터에만 너무 잘 맞는 상태" }
  - intent: "Same INK ground (0 ms swap of content, devices exit down on 24.18). 24.20: 'label' lands top-centre in an accent label box with ink text (Paperlogy 800 ~72 px). 24.20: one big paper card (760×420, ink 6 px outline, accent offset shadow) springs in centre-below showing 'term' (Paperlogy 800 ~150 px ink). 25.17: the card flips on Y (3d-card-flip, 0.4 s power2.inOut, backface hidden) to show 'meaning' (Paperlogy 800 ~58 px ink, max 2 lines). Hold to the iris."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 5.80s
- span_sec: [26.15, 31.95]
- pacing: beat_cut
- mood: [hype, warm]
- feel: HIGH to 28, MEDIUM 28–31, LOW 31–32. Beats 26.63 27.10 27.59 28.07 | 28.56 29.05 29.54 30.02 | 30.51 30.98 31.46. Snare 27.07; hats 29.00 29.98 30.95 31.90
- role: series3 (책 + 특강 + CBT + 카페 + 단톡 → Live 빠따 특강)
- pattern_hint: COMIC-STICKERS (new): package tokens as comic stickers slapped on a panel, then the Live ticket
- scene_color: #F2F0EA
- transition_out: none
- sfx: pop@26.63, pop@27.10, pop@27.59, pop@28.07, pop@28.56, whoosh-short@29.00, notification@29.54, ping@30.02

### Groups

- **g1** — free_design
  - span_sec: [26.15, 31.95]
  - free_design: { dominant_system: "five comic stickers slap onto a halftone panel one per beat, then a LIVE ticket tears in; the batter steps up at the end", primitives: ["overlay-pop", "word-grid-burst"], density_topology: "accumulate → ticket" }
  - anchors: [26.63, 27.10, 27.59, 28.07, 28.56, 29.54, 30.02, 30.98]
  - copy: { tokens: ["책", "특강", "CBT", "카페", "단톡"], ticket: "시험 직전 Live 빠따 특강" }
  - intent: "PAPER ground held, with a large flat comic panel frame (ink 8 px border, ~1600×520, a faint green halftone inside) at the top half. 26.63 / 27.10 / 27.59 / 28.07 / 28.56: one sticker per beat slaps onto the panel in a row: each a rounded-corner sticker with a white 6 px die-cut border + ink 3 px outline, alternating fills (green #008D41 with paper text, accent with ink text, ink with accent text), Paperlogy 800 ~110 px, small rotations (−6°..+6°, index-derived), entrance scale 1.4→1 power3.out 0.14 s + 2-frame mini shake; '+' discs between them pop on the off-beats. 29.54: a ticket (accent fill, perforated stub with a red #E8213F LIVE dot that pulses on 30.02 / 30.51 / 30.98, ink text 'ticket' Paperlogy 800 ~62 px; 'Live' may be Archivo Black) tears in from the bottom under the panel (y 420→0, rotation 3°→−1.5°). 30.02: the user's character stance.png (~520 px tall, feet on y≈1040) steps in at the far right (x≈1640, spring from x +400) — at bat, waiting for the climax; keep it clear of the ticket. Hold to 31.95 (hard cut into the climax)."

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 3.88s
- span_sec: [31.95, 35.83]
- pacing: beat_cut
- mood: [tense, euphoric]
- feel: LOW 31–32, VOID 32–33 (the break: near silence, hat 32.88), SURGE 33.90, DROP 34 (hard stop), LOW 34–36. Beats 31.95 32.44 32.93 33.41 | 33.90 34.39 34.88 35.34
- role: CLIMAX (노베이스도 한방에!)
- pattern_hint: AT-BAT → SWING-IMPACT (from adsp-169-baseball-1: f5 + characters.html swing)
- scene_color: #F2F0EA
- transition_out: none
- sfx: tick@32.44, tick@32.93, tick@33.41, whoosh-short@33.80, bat-crack@33.90, impact-bass-2@33.90, sparkle@34.39

### Groups

- **g1** — free_design
  - span_sec: [31.95, 33.90]
  - free_design: { dominant_system: "the at-bat pause in the silent bar", primitives: ["blur-resolve"], density_topology: "single" }
  - anchors: [31.95, 32.44, 32.93, 33.41]
  - copy: { a1: "노베이스도" }
  - intent: "PAPER ground. The batter stance.png large (~800 px tall, feet on y≈1040) at x≈1450, slight bat waggle (rotation ±1.6° on 32.44 / 32.93 / 33.41 — quiet beats). 'a1' resolves left (Paperlogy 800 ~170 px ink) with an accent highlighter on 32.44. Copy this group's build from videos/adsp-169-baseball-1/compositions/frames/05-f5.html g1 (same idea, retime to these anchors, recolour highlighter to #FEF21C, ink #222685)."
- **g2** — free_design
  - span_sec: [33.90, 35.83]
  - free_design: { dominant_system: "the swing impact + mega line + one colour flip", primitives: ["palette-flip", "braam-punch", "radial-burst-lines", "particle-burst"], density_topology: "explode → freeze" }
  - anchors: [33.90, 34.39, 34.88]
  - copy: { c1: "노베이스도", c2: "한방에!" }
  - intent: "0 ms flip to GREEN #008D41 on 33.90 (the cover's ground — the climax colour). Build exactly the impact recipe of videos/adsp-169-baseball-1/compositions/characters.html (swing whips in from the right edge with 3 afterimages at .35/.2/.1, a 1-frame white flash + fast fade, ~14 ink wedge burst lines from the bat's sweet spot, a baseball (paper circle + red #E8213F stitches) leaving frame upward on an arc with a 4-ball trail — path clear of the copy) combined with the mega slam of adsp-169-baseball-1 05-f5 g2: 'c1' upper-left (Paperlogy 400 ~150 px paper), 'c2' mega (Paperlogy 800 ~330 px accent) centred-left at x≈780; 34.39 its accent #FEF21C label box snaps behind it and the text turns ink #222685 + one 7-step screen shake; 2 accent rings + ~8 flat confetti, none in the batter's corner. Swing sprite = assets/characters/swing.png (~660×675) hanging from the bottom-right edge (x≈1600). Freeze from 34.88 to the end (hard stop at 34)."

## Frame 7 — f7

- src: compositions/frames/07-f7.html
- duration: 6.88s
- span_sec: [35.83, 42.71]
- pacing: beat_cut
- mood: [triumphant]
- feel: LOW 34–36, MEDIUM 36–37, SURGE 37.76 → HIGH to 42, DROP 42 (ending). Beats 36.32 36.78 37.27 37.76 | 38.24 38.73 39.20 39.68 | 40.17 40.66 41.15 41.63 | 42.12. Kick 41.68
- role: finale
- pattern_hint: BOOK3D + LOCKUP (house finale of adsp-169-clean-1 f6, recoloured)
- scene_color: #222685
- transition_out: none
- sfx: whoosh@35.85, pop@37.76, chime@39.68, sparkle@41.63
- book: 9791124516317 | 2027 빠르게 따는 빅데이터분석기사 필기 | 이유성, 조영훈 | | assets/covers/9791124516317.jpg

### Groups

- **g1** — free_design
  - span_sec: [35.83, 42.71]
  - free_design: { dominant_system: "book + stacked title + stores + logo lockup", primitives: ["kinetic-letter-in", "overlay-pop"], density_topology: "build → hold" }
  - anchors: [35.83, 36.78, 37.76, 38.73, 39.68, 41.63]
  - copy: { title1: "2027 빠르게 따는", title2: "빅데이터분석기사", title3: "필기", where: "예스24 · 교보문고 · 알라딘", brand: "골든래빗" }
  - intent: "INK ground. Follow the finale build of videos/adsp-169-clean-1/compositions/frames/06-f6.html g2 (3D book on the left with real back/spine, title stack + stores + logo lockup on the right), recoloured to this palette (accent #FEF21C, green #008D41 used for one small label box or underline only). 35.83: book turns in (rotateY −40°→−12°, 0.6 s) on the left (x≈620). 36.78 'title1' (Paperlogy 800 ~64 px paper), 37.76 (SURGE) 'title2' (Paperlogy 800 ~120 px accent, may wrap to 2 lines) + 'title3' in a green label box with paper text, 38.73 'where' (Paperlogy 500 ~34 px paper 80%), 39.68 logo lockup (assets/brand/icon.png ~64 px + 'brand' Paperlogy 800 ~40 px paper). 41.63: a small flat starburst sparkle behind the book's corner (accent, 0.3 s) — final hit. Hold everything still from 41.9 to the end (≥ 0.8 s calm)."
