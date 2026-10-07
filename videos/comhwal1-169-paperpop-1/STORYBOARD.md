---
compositionId: bgm
duration_s: 48.0 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "합격률 8.8%의 컴활 1급 실기, 쌩초보도 빠따로 한 방에"
variant: { name: comhwal1-169-paperpop-1, style: paper-pop, aspect: "16:9", seed: 27, intensity: standard }
style:
  font: "Paperlogy only — 600 telop/bubbles/labels/pen notes, 700 plain text, 800 numerals + onomatopoeia"
  palette: ["#F4EEE1", "#1A1A22", "#FFE13A", "#23268C", "#E5352B"]
assets: "assets/covers/9791124516614.jpg (the book, 1080×1440); assets/faces/{base,worry,happy,fired}/<slug>.png (512px paper-cut faces) + assets/faces/sm/{worry,happy}/<slug>.png (160px crowd copies); assets/props/bat.png (paper-cut baseball bat, transparent, diagonal handle bottom-left → barrel top-right); assets/brand/icon.png (gold rabbit logo mark); assets/fonts/*"
build_notes:
  - "follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)"
  - "no HUD in this variant — keep readable content in y 96–984, x 96–1824"
  - "AUDIO: 0–7.75 s is a SILENT cold open (no music; clock tick SFX on a 155-BPM grid: tick every 0.775 s, then quarter ticks 6.20/6.59/6.98/7.36). The band enters with the bat crack at 7.75. Bar = 1.55 s, beat = 0.3875 s."
  - "slugs: p rei lucas bible benny cindy esther alice ian jini kate thomas toynbee (fired/ only benny, jini). Faces are already paper-cut with their own shadow — add only a soft contact shadow if needed, never a CSS filter chain on 100 crowd faces (performance)."
  - "CROWD BOARD (F1 + F8 share it exactly): graph-paper board x 1000–1840, y 120–960 (840×840), 10×10 cells of 84 px, crowd face 76 px centred in each cell. Cell (r,c) index i = r*10+c; slug = SLUGS[(i*5) % 13] with SLUGS in the order above, EXCEPT cell (4,5) = jini. Survivors (9 cells that stay in F1 and are already happy in F8): (0,7) (1,3) (2,9) (3,5) (4,1) (5,6) (6,2) (7,8) (8,4)."
  - "paper boil (frame.md `boil`) on every face and sticker; telop = frame.md `telop` double outline; every frame starts on its scene_color ground; nothing essential in its first 0.3 s / last 0.3 s when a transition is set"
  - "the paper-fibre texture overlay and all transitions are added by the assembler — do not add grain or cover/reveal wipes yourself"
avoid: ["text over the cover", "drawn people/objects in SVG/CSS (use the face/prop PNGs)", "HUD chrome, confetti, label-box register flips (bold-beat devices)", "1위/No.1 claims", "black letterbox + top caption (Korean shorts cliché)"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 7.75s
- span_sec: [0.0, 7.75]
- pacing: beat_cut
- mood: [tense, comic]
- feel: SILENT cold open on a clock-tick grid (tick 0.0, tock 0.775, tick 1.55, tock 2.325, tick 3.10, tock 3.875, tick 4.65, tock 5.425, then accelerating quarter ticks 6.20, 6.59, 6.98, 7.36); bat swing 7.42 → crack at 7.75 (= F2 start)
- role: intro
- pattern_hint: COLD-OPEN-GRID (target call → number shock → pain voices → bat)
- scene_color: #F4EEE1
- transition_out: none
- sfx: tick@0.0, tock@0.775, tick@1.55, tock@2.325, tick@3.10, impact-bass-1@3.10, tock@3.875, tick@4.65, error@4.65, tock@5.425, tick@6.20, pop@6.20, tick@6.59, pop@6.59, tick@6.98, pop@6.98, tick@7.36, pop@7.36, whoosh-short@7.42
- copy_hint: ["컴활 1급,", "준비 중이세요?", "실기 합격률은?", "8.8%", "100번 보면 91번", "떨어지는 시험"]

### Groups

- **g1** — free_design
  - span_sec: [0.0, 3.10]
  - free_design: { dominant_system: "target call on a single worried paper face, then a pull-back reveals it is one of 100 faces on a graph-paper exam board", primitives: ["kinetic-letter-in", "dolly-zoom", "staggered-exit"], density_topology: "one → many" }
  - anchors: [0.0, 0.30, 0.775, 1.55, 2.325]
  - copy: { l1: "컴활 1급,", l2: "준비 중이세요?", l3: "실기 합격률은?" }
  - intent: "PAPER ground #F4EEE1 with the graph-paper CROWD BOARD (see build_notes) at the right, but at t=0 the board is scaled ~6.8× about jini's cell (4,5) so only jini fills the right half (~520 px, worry expression from assets/faces/worry/jini.png laid over her cell); all other crowd faces hidden. 0.0 (tick): jini pops in (ぽよん) and starts boiling at 8 fps. 0.30: telop 'l1' lands top-left (x≈110, y≈200; Paperlogy 800 ~120 px, white fill / 8 px ink stroke / 18 px yellow outer stroke / 6 px ink offset shadow). 0.775 (tock): 'l2' stacks under it (same telop, slightly smaller ~104 px). 0.95: three short ガーン gloom lines (sky blue) drop above jini's head. 1.55 (tick): the board zooms OUT to scale 1 (≈0.6 s, power3.inOut) about jini's cell while the 99 other worried crowd faces (assets/faces/sm/worry/<slug>.png, 76 px, tiny seeded tilts ±4°) pop in from the centre outward in a ripple; jini's cell swaps to the 160 px crowd copy so she ends as one ordinary cell. At the same time l1/l2 swap (0 ms) to 'l3' on a NAVY cushion (cushion scaleX 0→1 from left, white Paperlogy 600/Paperlogy text, ~92 px) top-left. 2.325 (tock): the whole board does one 2 px 'nervous' shake."
- **g2** — free_design
  - span_sec: [3.10, 6.20]
  - free_design: { dominant_system: "number slam + 91 paper faces physically FALL off the board (떨어지다 = fall/fail)", primitives: ["braam-punch", "radial-burst-lines", "staggered-exit"], density_topology: "slam → collapse → read" }
  - anchors: [3.10, 3.30, 3.875, 4.20, 4.65, 5.425]
  - copy: { stat: "8.8%", l4a: "100번 보면 91번", l4b: "떨어지는 시험", note: "※ 2025년 컴퓨터활용능력 1급 실기 합격률 · 국가기술자격 통계연보(대한상공회의소) · 응시 건 기준" }
  - intent: "3.10 (tick + impact): 'l3' stays small at top-left; the MEGA stat '8.8%' slams in on the left half (Paperlogy 800 ~300 px numerals, '%' at 0.45×, RED #E5352B fill with 10 px ink stroke + 20 px white outer stroke + ink offset shadow), scale 1.6→1 in 3 frames with a 4 px screen shake, while a ring of ink manga concentration lines flashes behind it for ~0.4 s. Footnote 'note' appears bottom-left (y≈1028, Paperlogy 500 20 px, ink 55%) and stays to the end of the frame. 3.30–4.30: the 91 non-survivor crowd faces FALL off the board in a seeded order (each: y +900…+1200 with gravity ease power2.in, rotation ±25…60°, 0.55–0.75 s each, staggered across ~1.0 s) — the survivors in build_notes stay. 4.20: the 9 survivors swap to sm/happy (tiny squash pop). 4.65 (tick + buzzer): 'l4a' and 'l4b' stack under the stat (telop ~84 px, ink fill + white outer stroke, the words '91번' and '떨어지는' in RED); '떨어지는' drops 10 px and bounces once (it 'falls'). 5.425: the stat gives one small 2 px wobble. Everything holds to 6.20."
- **g3** — free_design
  - span_sec: [6.20, 7.75]
  - free_design: { dominant_system: "pain voices: four big worried faces each pop a speech bubble on an accelerating tick, then the paper bat swings in", primitives: ["overlay-pop", "screen-shake"], density_topology: "accumulate → strike" }
  - anchors: [6.20, 6.59, 6.98, 7.36, 7.42, 7.75]
  - copy: { b1: "함수만 보면 머리가 하얘져…", b2: "액세스는 복불복이래…", b3: "벌써 3트째…", b4: "노베이스인데 될까?" }
  - intent: "6.20 (0 ms cut inside the frame, same paper ground, board and telop gone): four big worried faces (assets/faces/worry/{lucas,thomas,cindy,benny}.png, ~300 px) stand in a row along the bottom (y≈640–940, x≈170/610/1050/1490), each popping in on its tick (6.20 lucas, 6.59 thomas, 6.98 cindy, 7.36 benny) with a white paper speech bubble above it (frame.md `bubble`, Paperlogy 600 ~44 px, ink text; bubbles alternate heights y≈300–520 so they don't collide) carrying b1…b4. Each face jitters faster as ticks accelerate. 6.98–7.75 (revised 2026-10-07, the user found the cut too abrupt): the paper bat rises into frame at the far right (wind-up, ~6.98), cocks back (7.12–7.42), then accelerates (power3.in) through the centre so the barrel meets the impact point exactly at 7.75, with 2 smear copies; the four faces flinch left at 7.48; the camera layer leans in 1→1.07 from 7.0; concentration lines gather on the centre from 7.40 and a radial light builds from 7.55. F2 opens on the same bat pose (match cut), the same burst and a radial flash that fades over 0.22 s."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 3.09s
- span_sec: [7.75, 10.84]
- pacing: beat_cut
- mood: [hype]
- feel: band enters with the bat crack on the downbeat 7.75 (hi-hat fill into it); beats 8.13 8.54 8.92 | 9.31 9.68 10.08 10.45
- role: series0
- pattern_hint: BAT-CRACK (manga impact reveal of the book)
- scene_color: #FFE13A
- transition_out: tear
- sfx: bat-crack@7.75, impact-bass-2@7.75, whoosh@7.80, pop@8.54, pop@9.31, sparkle@10.08
- book: 9791124516614 | 2027 빠르게 따는 컴퓨터활용능력 1급 필기+실기 | 이강용(컴활킹) | NEW | assets/covers/9791124516614.jpg

### Groups

- **g1** — free_design
  - span_sec: [7.75, 10.84]
  - free_design: { dominant_system: "manga impact: concentration lines + onomatopoeia, the book is batted into frame and lands as a white-rimmed paper sticker", primitives: ["radial-burst-lines", "braam-punch", "kinetic-letter-in", "screen-shake"], density_topology: "impact → settle → read" }
  - anchors: [7.75, 8.13, 8.54, 9.31, 10.08]
  - copy: { sfx_word: "딱!", shout: "노베이스도 한 방에!", kicker: "2027 빠르게 따는", title: "컴퓨터활용능력 1급 필기+실기", badge: "2027~2029 출제기준 반영", brand: "골든래빗" }
  - intent: "YELLOW #FFE13A ground. 7.75 (crack, 0 ms): ink manga concentration lines fill the frame around an empty centre (frame.md `burst`, re-seeded every 1/8 s for the whole frame, opacity easing from 1 to ~0.35 by 8.6); a 1-frame white flash; the onomatopoeia '딱!' (Paperlogy 800 ~340 px, white fill, 12 px ink stroke, ink offset shadow, rotated −10°) pops at upper-left (x≈150–650, y≈90–420) with an 8 px shake; the paper bat (assets/props/bat.png ~560 px) is seen at lower-right finishing its follow-through (rotation continues −15°→−40°, then slides off-frame by 8.6). 7.80–8.30: the BOOK flies out of the impact point at frame centre — real cover assets/covers/9791124516614.jpg inside a white padded paper wrapper (12 px white border, radius 6, layered paper shadow; NO filter/text on the cover), ~450×600, spinning 1.5 turns with scale 0.25→1.08→1 and landing at x≈1080–1530, y≈200–800 tilted +4° (frame.md `place` landing). 8.54: shout telop '＼ 노베이스도 한 방에! ／' (frame.md `shout` + `telop`, ~92 px, white fill / ink stroke / navy outer) lands at left (x≈110–1000, y≈470–580). 9.31 (downbeat): a NAVY cushion bar slides in bottom-left (x≈110–1010, y≈650–860): kicker '2027 빠르게 따는' (Paperlogy 600 40 px, yellow) over title '컴퓨터활용능력 1급 필기+실기' (Paperlogy 800 ~62 px, white). From 8.13 a small brand sticker sits top-right (x≈1610–1824, y≈60–130): assets/brand/icon.png (~56 px) + '골든래빗' (Paperlogy 800 30 px ink) on a white paper pill. 10.08: a round red badge (~170 px, red paper circle with white Paperlogy 600 text 'badge' on 2–3 lines) pops on the book's lower-left corner OUTSIDE the cover edge (overlapping only the white wrapper margin/background, never the cover art). Hold."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 4.67s
- span_sec: [10.84, 15.51]
- pacing: beat_cut
- mood: [hype]
- feel: steady chorus, downbeats 10.84 12.40 13.96; beats 11.24 11.63 12.01 | 12.79 13.17 13.56 | 14.35 14.74 15.12
- role: series1
- pattern_hint: RED-SHEET (POINT 1 — 빈출 족보)
- scene_color: #F4EEE1
- transition_out: rings 760,560
- sfx: click-soft@11.24, pop@11.63, pop@12.79, whoosh-short@13.90, sparkle@14.05, pop@14.74
- hud_label: POINT 1 · 빈출 족보

### Groups

- **g1** — free_design
  - span_sec: [10.84, 15.51]
  - free_design: { dominant_system: "notebook telop with red-pen correction and a 赤シート (red acetate) that hides the answer, then slides off to reveal it", primitives: ["kinetic-letter-in", "mask-reveal", "outline-to-fill"], density_topology: "question → strike → hide → reveal" }
  - anchors: [10.84, 11.24, 11.63, 12.40, 12.79, 13.96, 14.35, 14.74]
  - copy: { label_num: "POINT 1", label: "빈출 족보", l1: "컴활 1급은", l2: "다 외우는 시험?", pen_no: "NO!", l3_key: "나올 것만", l3_rest: "외우는 시험", caption: "빈출 족보 + 빈출 XO로 이론 2회독" }
  - intent: "PAPER ground. 11.14: side label (frame.md `side-label`) slides in top-left (x≈96, y≈56): yellow pill 'POINT 1' (Paperlogy 600 34 px ink) + 'label' (Paperlogy 600 34 px ink) — it stays for the whole frame. 11.24: a white ruled NOTEBOOK sheet (≈1120×620, faint sky ruled lines every 64 px, a red margin line, paper shadow, rotated −2°) is placed (frame.md `place`) at x≈130–1250, y≈220–840. Inside it (ink Paperlogy 800, ~84 px, no outline needed on white paper): 11.24 'l1'; 11.63 'l2'. 12.40 (downbeat): a red-pen ✕ is drawn over 'l2' (two wobbly strokes, ~0.25 s, frame.md `red-pen`) and 'pen_no' is handwritten next to it (Paperlogy 600 red ~90 px, red, rotated −6°). 12.79: line 3 lands — 'l3_key' in RED (~96 px) followed by 'l3_rest' in ink — but 'l3_key' is already under a RED SHEET (frame.md `red-sheet`, ≈ the word's box + 24 px padding, slight tilt) so it reads as a blank red bar. On the right, a worried lucas (assets/faces/worry/lucas.png ~380 px, x≈1370–1750, y≈330–710) leans toward the sheet (boiling). 13.96 (downbeat): the red sheet slides off to the right (x → +130%, 0.35 s, power2.inOut) revealing 'l3_key'; a red hanamaru (spiral flower circle) draws around it (~0.4 s); lucas swaps to assets/faces/happy/lucas.png (squash pop). 14.74: 'caption' on a small yellow cushion under the notebook (Paperlogy 600 ~40 px ink, y≈880–940). Hold to the end (rings transition covers the last 0.3 s)."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 4.65s
- span_sec: [15.51, 20.16]
- pacing: beat_cut
- mood: [hype]
- feel: steady chorus; beats 15.88 16.28 16.65 | 17.04 17.44 17.83 18.20 | 18.60 18.97 19.36 19.74; downbeat 20.16 = next frame (and the music edit — keep the end clean, the transition covers it)
- role: series2
- pattern_hint: PROGRESS-WALK (POINT 2 — 6주 합격 패스)
- scene_color: #23268C
- transition_out: paper
- sfx: click-soft@16.28, click-soft@16.65, click-soft@17.04, click-soft@17.44, click-soft@17.83, click-soft@18.20, chime@18.60
- hud_label: POINT 2 · 쌩초보 6주 플랜

### Groups

- **g1** — free_design
  - span_sec: [15.51, 20.16]
  - free_design: { dominant_system: "a fired-up paper face hops block-to-block across six week tiles that drop in on the beats, reaching a 합격 sign", primitives: ["staggered-exit", "counting-punch", "overlay-pop"], density_topology: "path → arrival" }
  - anchors: [15.51, 15.88, 16.28, 16.65, 17.04, 17.44, 17.83, 18.20, 18.60, 18.97]
  - copy: { label_num: "POINT 2", label: "쌩초보 6주 플랜", t1a: "쌩초보 기준,", t1b: "딱 6주", t2: "필기 2주 + 실기 4주 합격 패스", wk: ["1주", "2주", "3주", "4주", "5주", "6주"], br1: "필기 2주", br2: "실기 4주", goal: "합격!" }
  - intent: "NAVY #23268C ground (a faint lighter-navy graph grid is fine). 15.81: side label top-left (yellow pill 'POINT 2' + 'label' in white Paperlogy 600). 15.88: telop 't1a' + 't1b' on one line, top-centre (y≈170–300): Paperlogy 800 ~110 px white fill with ink stroke + navy-dark outer, '6주' in YELLOW at 1.35× with a pop. Track: six paper tiles (≈190×110, gap 22, x≈210…1520, y≈640–750; tiles 1–2 YELLOW paper, tiles 3–6 WHITE paper; Paperlogy 600 ~44 px ink 'wk[i]') — tile i DROPS in (place motion, from y −60, slight rotation) on beats 16.28, 16.65, 17.04, 17.44, 17.83, 18.20. Brackets above them: a yellow bracket + 'br1' (Paperlogy 600 36 px yellow) over tiles 1–2, a white bracket + 'br2' (Paperlogy 600 36 px white) over tiles 3–6 — the brackets draw on at 17.04 and 18.20. The runner: assets/faces/fired/benny.png (~210 px, headband) starts at the left of tile 1 at 15.88 and HOPS onto each tile as it lands (each hop = parabolic arc, 0.3 s, motion stepped at 12 fps for a cut-paper puppet feel, a little squash on landing). 18.60 (downbeat): at the end of the track a paper goal sign pops (white paper board ~260×170 on a short stick, red border, 'goal' in RED Paperlogy 600 ~72 px) and benny makes a bigger jump onto it, swapping to assets/faces/happy/benny.png at the apex. 17.04: 't2' appears under the main telop (Paperlogy 600 ~44 px, white, y≈330). Hold the arrival (boil only) to the end."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 4.64s
- span_sec: [20.16, 24.80]
- pacing: beat_cut
- mood: [hype]
- feel: final-chorus bar 1 lands at 20.16 (strong kicks 20.13/21.27); beats 20.53 20.92 21.32 | 21.71 22.08 22.48 22.85 | 23.24 23.61 24.03 24.40
- role: series3
- pattern_hint: TRI-PANEL (POINT 3 — 기출변형 30회분)
- scene_color: #DDEDF8
- transition_out: tear
- sfx: pop@20.53, pop@20.92, pop@21.32, key-press@21.71, key-press@22.08, key-press@22.48, impact-bass-1@23.24, sparkle@23.40
- hud_label: POINT 3 · 최신 기출변형

### Groups

- **g1** — free_design
  - span_sec: [20.16, 24.80]
  - free_design: { dominant_system: "three paper panels (Japanese 3-split) slide up, each with a face and a 10회 count, then the sum slams across", primitives: ["staggered-exit", "counting-punch", "braam-punch"], density_topology: "split → count → sum" }
  - anchors: [20.16, 20.53, 20.92, 21.32, 21.71, 22.08, 22.48, 22.85, 23.24, 23.61]
  - copy: { label_num: "POINT 3", label: "최신 기출변형", p1: "필기", p2: "엑셀", p3: "액세스", count: "10회", plus: "+", sum_a: "기출변형", sum_b: "총 30회분" }
  - intent: "Light sky-paper #DDEDF8 ground. 20.36: side label top-left (yellow pill 'POINT 3' + 'label' in ink Paperlogy 600). 20.16 (downbeat): three white paper panels (≈470×560, radius 18, paper shadow, slight alternating tilts) slide UP from below the frame with a 0.1 s stagger and land at x≈190 / 725 / 1260, y≈190–750. Each panel: a face at top (assets/faces/worry/{kate,cindy,thomas}.png ~200 px — kate=필기, cindy=엑셀, thomas=액세스), a big count in the middle, and a label cushion along its bottom edge (p1 on YELLOW, p2 on WHITE with ink border, p3 on NAVY with white text; Paperlogy 600 ~52 px). Counts: 20.53 / 20.92 / 21.32 each panel's count odometer-steps 0→10 in ~0.3 s (transform strips or 0 ms text swaps, Paperlogy 800 ~150 px numerals, '회' at 0.45×). 21.71 / 22.08 / 22.48: each face swaps to its happy version (squash pop). 22.85: two '+' paper chips pop between the panels. 23.24 (downbeat): the SUM slams across the lower part, overlapping the panels' bottoms: a RED tilted cushion band (≈1300×150, rotated −3°) with 'sum_a' (Paperlogy 800 ~64 px white) + 'sum_b' (Paperlogy 800 ~104 px YELLOW with ink stroke, '30' at 1.3×), scale 1.3→1 in 3 frames + 3 px shake. Hold."

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 4.64s
- span_sec: [24.80, 29.44]
- pacing: beat_cut
- mood: [hype]
- feel: chorus; beats 25.17 25.57 25.94 | 26.33 26.73 27.12 27.49 | 27.89 28.28 28.68 29.05; kick roll 29.40 into the next frame
- role: series4
- pattern_hint: SCORE-CARD (POINT 4 — CBT & 자동 채점)
- scene_color: #F4EEE1
- transition_out: rings 960,540
- sfx: click-soft@25.17, typing@25.57, notification@26.33, sparkle@27.12, pop@27.89
- hud_label: POINT 4 · 웹 CBT · 자동 채점

### Groups

- **g1** — free_design
  - span_sec: [24.80, 29.44]
  - free_design: { dominant_system: "original paper 'grading' card: a file card drops in, two score bars fill past the 70점 line, a red hanamaru; telop stacks one word per beat", primitives: ["directional-fill", "kinetic-letter-in", "outline-to-fill"], density_topology: "input → process → verdict" }
  - anchors: [24.80, 25.17, 25.57, 25.94, 26.33, 27.12, 27.89]
  - copy: { label_num: "POINT 4", label: "웹 CBT · 자동 채점", card_title: "실기 자동 채점", tray: "답안 파일을 올려 주세요", file: "기출변형_07회.xlsx", row1: "엑셀", row1_score: "85점", row2: "액세스", row2_score: "80점", line: "합격선 70", pen: "합격권!", t1: "풀고,", t2: "올리면,", t3: "바로 채점!", caption: "필기는 웹 CBT 10회 · 실기는 자동 채점(엑셀·액세스)", note: "※ 화면은 이해를 돕기 위한 연출입니다" }
  - intent: "PAPER ground. 25.0: side label top-left (yellow pill 'POINT 4' + 'label' ink Paperlogy 600). LEFT: an ORIGINAL paper UI card (white paper, radius 20, layered paper shadow, ≈880×640 at x≈110–990, y≈200–840; NO real product UI or logos) with a navy title strip 'card_title' (Paperlogy 600 40 px white) and a dashed rounded upload tray reading 'tray' (Paperlogy 600 30 px, ink 50%). 25.17: a small yellow paper FILE card ('file', Paperlogy 600 26 px, with an 'xlsx' corner tab) drops into the tray (place motion). 25.57: a thin progress bar under the tray fills in 12-fps steps. 25.94→26.33: the tray is replaced by two result rows — 'row1' and 'row2' (Paperlogy 600 40 px) each with a horizontal paper bar (track 520 px) that fills (scaleX, stepped at 12 fps) to 85% / 80% of its track, a vertical RED dashed line at 70% labelled 'line' (Paperlogy 600 22 px red), and the scores (Paperlogy 800 ~56 px) counting up; both bars pass the red line by 26.33 (downbeat). 27.12: a red hanamaru draws around both scores and 'pen' is handwritten beside it (Paperlogy 600 red ~80 px red, −6°). RIGHT column (x≈1080–1824): telop stack t1 (25.17), t2 (25.57), t3 (25.94) — Paperlogy 800 ~118 px, ink fill + white outer stroke on a YELLOW cushion behind 't3' only, each line ぽよん in; faces rei (worry) and ian (worry) (~230 px) stand at the bottom-right (y≈700–930) and swap to happy at 26.33. 27.89 (downbeat): 'caption' on a navy cushion along the bottom (Paperlogy 600 ~36 px white, y≈900–960); 'note' tiny bottom-left footnote (Paperlogy 500 20 px ink 55%). Hold."

## Frame 7 — f7

- src: compositions/frames/07-f7.html
- duration: 4.65s
- span_sec: [29.44, 34.09]
- pacing: beat_cut
- mood: [hype]
- feel: chorus downbeat 29.44 after a kick roll; beats 29.81 30.23 30.60 | 31.00 31.37 31.77 32.14 | 32.53 32.93 33.32 33.69
- role: series5
- pattern_hint: BUBBLE-POP (bundle — everything in one book)
- scene_color: #FFF4C2
- transition_out: paper
- sfx: click-soft@29.44, pop@29.81, pop@30.23, pop@30.60, pop@31.00, pop@31.37, pop@31.77, chime@32.53
- hud_label: PLUS · 이 모든 게 한 권에

### Groups

- **g1** — free_design
  - span_sec: [29.44, 34.09]
  - free_design: { dominant_system: "Foresight-style feature bubbles: six paper circles pop one per beat around the book on a gingham ground, then the shout line", primitives: ["overlay-pop", "particle-burst", "kinetic-letter-in"], density_topology: "centre → orbit → statement" }
  - anchors: [29.44, 29.81, 30.23, 30.60, 31.00, 31.37, 31.77, 32.53]
  - copy: { b1: "유튜브 무료 강의", b2: "저자 직문직답 오픈채팅", b3: "합격왕 카페 스터디", b4: "엑셀 함수 정리 PDF", b5: "웹 CBT 10회", b6: "2027~2029 출제기준 반영", shout: "이 모든 게, 한 권에!" }
  - intent: "YELLOW GINGHAM: ground #FFF4C2 with crossing translucent #FFE13A stripes every 96 px (frame.md `board` gingham). 29.44 (downbeat): the BOOK (cover in the white padded paper wrapper, ≈390×520, no filter on the cover) is placed at centre (x≈765–1155, y≈300–820) with the place motion. Six paper bubbles (circles ≈250 px, paper shadow, alternating fills NAVY/white text, WHITE/ink text with 4 px ink outline, RED/white text; Paperlogy 600 ~36 px, 2 lines max) pop (ぽよん, back.out) one per beat around the book: b1 29.81 top-left (≈360,300), b2 30.23 top-right (≈1560,300), b3 30.60 left (≈300,640), b4 31.00 right (≈1620,640), b5 31.37 bottom-left (≈560,880), b6 31.77 bottom-right (≈1360,880). After landing every bubble floats ±6 px on a 2 s sine (phase by index). Small happy faces (assets/faces/happy/{alice,esther,p,toynbee}.png, ~120 px) cling to the outer edge of b1, b2, b3, b4 (pop with their bubble, boil). 32.53 (downbeat): the shout '＼ 이 모든 게, 한 권에! ／' lands top-centre (y≈70–180; telop ~96 px, white fill / ink stroke / navy outer; '한 권' in RED) with a 3 px shake. Hold."

## Frame 8 — f8

- src: compositions/frames/08-f8.html
- duration: 6.20s
- span_sec: [34.09, 40.29]
- pacing: beat_cut
- mood: [hype]
- feel: chorus climax; beats 34.46 34.85 35.25 | 35.64 (downbeat) 36.01 36.41 36.78 | 37.17 (downbeat) …; then a still hold 37.6–40.0
- role: climax
- pattern_hint: TAPE-BACK (callback to F1 — the faces get taped back on: 붙는다 = stick / pass)
- scene_color: #F4EEE1
- transition_out: tear
- sfx: pop@34.46, pop@34.85, pop@35.25, impact-bass-2@35.64, pop@36.01, pop@36.41, pop@36.78, sparkle@37.17
- hud_label: CLIMAX · 이번엔 붙는다

### Groups

- **g1** — free_design
  - span_sec: [34.09, 40.29]
  - free_design: { dominant_system: "the F1 exam board returns; the 91 fallen faces are slapped back on with masking tape, wave by wave, all happy; the pun line slams", primitives: ["tile-mosaic", "braam-punch", "radial-burst-lines", "screen-shake"], density_topology: "empty → filled → hold" }
  - anchors: [34.09, 34.46, 34.85, 35.25, 35.64, 36.01, 36.41, 36.78, 37.17, 38.73]
  - copy: { l1: "이번엔,", l2: "붙는다!", sub: "쌩초보도, 한 방에." }
  - intent: "PAPER ground with the CROWD BOARD exactly as in F1 (same geometry/slugs, build_notes): only the 9 survivors are on it (sm/happy), the other 91 cells show faint dashed outlines (empty slots). 34.30: 'l1' lands top-left (x≈110, y≈230; telop ~130 px, ink fill + white outer). WAVES: on the beats 34.46, 34.85, 35.25, 36.01, 36.41, 36.78, 37.17 (7 waves, 13 faces each, seeded order) faces (assets/faces/sm/happy/<slug>.png) slap onto their cells from slightly above (y −30, scale 1.15 → 1 in 3 frames) and each gets one masking-tape strip across its top (frame.md `tape`, alternating yellow/sky, seeded angle ±25°); the board shakes 2 px on each wave. 35.64 (downbeat): MEGA 'l2' slams under 'l1' (Paperlogy 800 ~260 px, YELLOW fill, 12 px ink stroke, 22 px white outer stroke, ink offset shadow; scale 1.6→1 in 3 frames), with a burst of ink concentration lines behind it for ~0.5 s and a 5 px shake. 37.17 (downbeat): the full board does one happy 'bounce' (scale 1→1.02→1) and 'sub' fades up under l2 (Paperlogy 600 ~56 px, ink, on a small yellow cushion). 37.6 → 40.0: HOLD — only the 8 fps boil moves (this is the video's ≥1.5 s still). Keep the last 0.3 s clean for the tear transition."

## Frame 9 — f9

- src: compositions/frames/09-f9.html
- duration: 7.71s
- span_sec: [40.29, 48.0]
- pacing: beat_cut
- mood: [hype → resolve]
- feel: last chorus bars then the song's stop-time ending: hits 44.14, 44.52, 44.92 (triplet), 45.69, FINAL HIT 46.46, decay to 48.0
- role: finale
- pattern_hint: SEARCH-CTA (vertical slogan + search bar typed on the stop-time hits + logo on the final hit)
- scene_color: #23268C
- transition_out: none
- sfx: click-soft@40.29, key-press@44.14, key-press@44.52, key-press@44.92, click@45.69, chime@46.46
- copy_hint: {"line": "합격으로 가는 가장 빠른 길", "search": "빠따 컴활 1급", "cta": "goldenrabbit.co.kr"}

### Groups

- **g1** — free_design
  - span_sec: [40.29, 48.0]
  - free_design: { dominant_system: "Japanese ad end card: book + vertical slogan, then a generic search bar typed on the stop-time hits, cursor click, logo lockup on the final hit", primitives: ["mask-reveal", "typewriter-reveal", "overlay-pop"], density_topology: "assemble → type → land → hold" }
  - anchors: [40.29, 40.66, 41.82, 43.38, 44.14, 44.52, 44.92, 45.69, 46.46]
  - copy: { v1: "합격으로 가는", v2: "가장 빠른 길", kicker: "2027 빠르게 따는", title: "컴퓨터활용능력 1급", title2: "필기+실기", author: "이강용(컴활킹) 지음", search: "빠따 컴활 1급", brand: "골든래빗", url: "goldenrabbit.co.kr" }
  - intent: "NAVY #23268C ground. 40.29 (downbeat): the BOOK (cover in the white padded paper wrapper, ≈480×640, no filter/text on the cover) is placed at left (x≈200–680, y≈200–840, tilt −3°) with the place motion; two happy faces peek from behind its edges (assets/faces/happy/kate.png ~170 px at the top-right edge, assets/faces/happy/bible.png ~150 px at the bottom-left edge; boil). 40.66: VERTICAL slogan at the far right (writing-mode: vertical-rl, two columns x≈1600–1830, y≈120–860): 'v1' and 'v2' in Paperlogy 800 ~104 px white with ink stroke, '빠른' in YELLOW — revealed top-to-bottom by a clip-path wipe (~0.6 s per column, v2 starts at 41.05). 41.82 (downbeat): title block in the middle column (x≈760–1520, y≈200–470): 'kicker' (Paperlogy 600 40 px yellow), 'title' (Paperlogy 800 ~84 px white), 'title2' (Paperlogy 800 ~60 px white), 'author' (Paperlogy 600 32 px white 80%). 43.38 (downbeat): a generic SEARCH BAR (frame.md `search`: white pill ≈740×104, 5 px ink outline, magnifier icon at right, NO real service logo) slides up into x≈770–1510, y≈560–664 with a blinking caret (0 ms toggles). Text 'search' types in three chunks on the stop-time hits: 44.14 '빠따', 44.52 ' 컴활', 44.92 ' 1급' (Paperlogy 600 ~52 px ink). 45.30–45.69: a white paper cursor arrow (ink outline) glides in and CLICKS the magnifier at 45.69 (press 0.9→1 + a yellow ripple ring). 46.46 (FINAL HIT): the logo lockup pops below the bar (x≈770–1510, y≈730–880): assets/brand/icon.png (~110 px) + 'brand' (Paperlogy 800 ~64 px white) + 'url' (Paperlogy 600 34 px yellow), with a small burst of yellow paper four-point sparkles around it; the faces swap to a final squash. 46.46 → 48.0: HOLD (only boil). Last frame must look like a finished poster."
