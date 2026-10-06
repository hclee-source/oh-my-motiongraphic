---
compositionId: bgm
duration_s: 30.75 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "AI 입문, 바로바로 네 권이면 충분하다"
variant: { name: baro-series-169-softstudio-1, style: soft-studio, aspect: "16:9", seed: 11, intensity: standard }
style:
  font: "Gmarket Sans 700/500/300 (embedded OTF, Korean) / Outfit 700 (Latin) / Space Mono 400/700 (UI mockups, numerals)"
  palette: ["#F4EFE6", "#1B1A1F", "#5B5BF0", "#6E6A72"]
assets: "assets/covers/<isbn>.jpg × 4; assets/brand/icon.png (logo); assets/fonts/ Paperlogy; assets/keyvisual/baro-kv-01.png — user-supplied key visual (clay characters) — MUST be used"
build_notes:
  - "follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)"
  - "no HUD in this variant — keep readable content in y 96–984"
  - "register order hint for this seed: ink → scene-tint → cream"
avoid: ["text over covers", "gradients/glows", "copying reference videos' copy or layouts"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 6.99s
- span_sec: [0.0, 6.99]
- pacing: beat_cut
- mood: [hype]
- feel: VOID→HIGH energy; 1 roll(s); key SURGE@1; strong hits [4.46, 4.97, 6.46, 6.97]
- role: intro
- pattern_hint: TYPE-WINDOW → KV window card
- scene_color: #F4EFE6
- transition_out: wipe
- sfx: typing@1.0, pop@2.51, sparkle@3.05, whoosh@4.85
- copy_hint: ["AI 공부,", "어디서부터?"]

### Groups

- **g1** — free_design
  - span_sec: [0.0, 6.99]
  - free_design: { dominant_system: "type-as-window: a question types in, then the giant word 바로바로 becomes a window onto the key visual, which then opens into a rounded window card (2.5D parallax)", primitives: ["typewriter-reveal", "mask-reveal", "dolly-zoom"], density_topology: "type → window → reveal" }
  - anchors: [1.0, 2.0, 2.51, 3.0, 3.99, 4.99, 5.99]
  - copy: { q1: "AI 공부,", q2: "어디서부터?", window_word: "바로바로", caption: "바로 배워 바로 쓰는, 바로바로 시리즈" }
  - intent: "CREAM ground. 0–1.0 (song intro): only a small accent cursor blinks at left-center. 1.0 (downbeat): 'AI 공부,' types in (h1 700, ink, character by character with a stepped 12fps bounce — 'on twos' feel). 2.0: '어디서부터?' lands under it (h1-light 300). 2.51: tiny bounce on the '?'. 3.0: a hand-drawn accent (#5B5BF0) circle SCRIBBLES around '어디서부터?' (SVG path with a slight wobble, drawn via stroke-dashoffset in ~0.35s). 3.99 (downbeat): the question slides up and fades; the giant word '바로바로' (Gmarket 700, ~360px, centered) slams in as a TYPE-WINDOW: the letters are filled with the key visual (background-clip:text using assets/keyvisual/baro-kv-01.png, background-size cover, slowly panning) — the clay characters are visible only through the letters. 4.99 (snare): the window OPENS — the word scales up past the frame while a rounded window card (radius 36px, soft shadow) with the full key visual (card-full.jpg) scales from 0.6→1.0 into the center (~1280×853); the image inside drifts slower than the card (parallax). 5.99: caption '바로 배워 바로 쓰는, 바로바로 시리즈' (body 500, ink) fades up under the card. Hold to 6.99 (wipe transition covers the end)."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 4.02s
- span_sec: [6.99, 11.01]
- pacing: beat_cut
- mood: [hype]
- feel: HIGH energy; 1 roll(s); key none; strong hits [8.96, 9.96, 10.96]
- role: series0
- pattern_hint: CHAT-UI (override of BOOK3D-OPEN — the chat device suits a ChatGPT book; the open-book device moves to 클로드)
- scene_color: #D4E3BA
- transition_out: blinds
- sfx: typing@7.48, click-soft@8.5, pop@9.01, ping@9.96
- hud_label: BARO 01 · 챗GPT
- book: 9791124516294 | 바로바로 챗GPT X 덕테이프 X 코덱스 | 박현규 |  | assets/covers/9791124516294.jpg

### Groups

- **g1** — free_design
  - span_sec: [6.99, 11.01]
  - free_design: { dominant_system: "original chat-window mockup: a question is typed, the assistant answers with a spinning 3D book inside its reply bubble", primitives: ["typewriter-reveal", "overlay-pop"], density_topology: "conversation" }
  - anchors: [7.48, 7.99, 8.5, 9.01, 9.5, 9.96, 10.49]
  - copy: { window_title: "AI 채팅", user: "AI, 바로 써먹고 싶어요", reply_lead: "이 책부터 펼쳐 보세요", book_title: "바로바로 챗GPT X 덕테이프 X 코덱스", author: "박현규", stat: "45개 실습", cover: "assets/covers/9791124516294.jpg" }
  - intent: "GROUND #D4E3BA. 7.34: an ORIGINAL chat window (ui-window: rounded 28px, cream body, soft shadow, title bar with 3 neutral dots and the label 'AI 채팅' — no third-party logos) rises into center-left (~1100×760). 7.48: the user's bubble (right-aligned, ink fill, cream Gmarket 500 text) types '바로 써먹고 싶어요' preceded by 'AI,'. 8.5: an assistant row appears with an AVATAR: a #1B1A1F circle (96px) containing assets/keyvisual/spr-green.png (the green clay character) and a 3-dot typing indicator bouncing on beats. 9.01 (downbeat): the reply bubble pops (cream, 1px ink/15% border) with '이 책부터 펼쳐 보세요' and, OUTSIDE the window on the right, a 3D book (book3d recipe, deep #365A16 spine, scale ~0.75) turns in from the side and lands at rest pose. 9.5: caption under the book: '바로바로 챗GPT X 덕테이프 X 코덱스' (h2-ish 44px, 700) and a pill sticker '박현규' (#365A16 fill, cream text). 9.96 (kick): a second pill sticker '45개 실습' pops with a little bounce. 10.49: the book does a slow quarter-turn showing its spine, then settles. Blinds transition covers from ~10.72."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 4.99s
- span_sec: [11.01, 16]
- pacing: beat_cut
- mood: [hype]
- feel: HIGH→LOW energy; 1 roll(s); key DROP@15; strong hits [11.45, 11.96, 13.44, 13.96, 15.21, 15.3, 15.95]
- role: series1
- pattern_hint: BOOK3D-OPEN + DEPTH-TYPE + STAT-RING (hold ≥1.5s on the open book)
- scene_color: #F1CBB3
- transition_out: iris 1180,560
- sfx: whoosh-short@11.3, pop@13.49, ping@15.21
- hud_label: BARO 02 · 클로드
- book: 9791124516133 | 바로바로 클로드 with 코워크, 스킬, 클로드 코드, 디자인 | 차진우 | BEST | assets/covers/9791124516133.jpg

### Groups

- **g1** — free_design
  - span_sec: [11.01, 16.0]
  - free_design: { dominant_system: "hero 3D book: turns in, spins to show spine/back, opens on its hinge; a huge word sits BEHIND it; page 1 carries a dotted stat ring that counts to 82; then a ≥1.5s hold on the open book", primitives: ["counting-punch", "freeze-hold"], density_topology: "object hero → hold" }
  - anchors: [11.45, 11.96, 13.0, 13.49, 14.0, 15.0, 15.21]
  - copy: { behind_word: "CLAUDE", kicker: "바로바로", title: "클로드", sub: "with 코워크 · 스킬 · 클로드 코드 · 디자인", page_number: "82", page_label: "가지 실습", sticker: "차진우", badge: "BEST", cover: "assets/covers/9791124516133.jpg" }
  - intent: "GROUND #F1CBB3. Behind everything, the Latin word 'CLAUDE' (Outfit 700, ~430px, color #622A0E at 14% opacity) spans the frame center (DEPTH-TYPE: type behind the object). Left column (x≈140): '바로바로' (h2) over '클로드' (display 700) and the sub line (body) — they slide in at 11.45. 11.45 (kick): the 3D book (book3d recipe, deep #622A0E spine with '바로바로 클로드' on it, scale ~1.05, centered at x≈1180) turns in from the right and lands at rest. 11.96 (kick): full 360° spin across ~1.0s (spine → back → pages → front). 13.49: the cover OPENS on the hinge; page 1 (the .bk-page face) shows a dotted stat ring (40 dots, #622A0E) that fills dot-by-dot while a Space Mono number counts 0→82, locking at 14.0 (downbeat) with '가지 실습' under it. 14.0–15.21: HOLD — the open book floats ±4px, nothing else moves (the 'beautiful still'). 15.21 (kick): two pill stickers pop near the book: 'BEST' (accent #5B5BF0) and '차진우' (#622A0E). The iris transition from the book (1180,560) covers from ~15.71."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 5.01s
- span_sec: [16, 21.01]
- pacing: beat_cut
- mood: [hype]
- feel: HIGH energy; 1 roll(s); key SURGE@16, DROP@17, SURGE@18, SURGE@20; strong hits [17.95]
- role: series2
- pattern_hint: SLOGAN-WEIGHT (on the 16.0 surge) → OBJECT-IN-SENTENCE (override of SHELF-PULL)
- scene_color: #D3DEF2
- transition_out: stripes
- sfx: impact-bass-1@16.05, whoosh-short@17.4, pop@18.99
- hud_label: BARO 03 · 제미나이·구글 AI
- book: 9791124516157 | 구글 AI 활용 입문서 | 공냥이 |  | assets/covers/9791124516157.jpg

### Groups

- **g1** — free_design
  - span_sec: [16.0, 17.0]
  - free_design: { dominant_system: "CLIMAX slogan revealed by the iris on the surge, with a weight pulse", primitives: ["braam-punch"], density_topology: "single statement" }
  - anchors: [16.0, 16.51]
  - copy: ["바로 배워,", "바로 쓴다."]
  - intent: "GROUND #D3DEF2. Already in place when the iris opens (16.07–16.37): '바로 배워,' (h1-light 300, ink) over '바로 쓴다.' (display 700, ink), centered. 16.51 (beat): '바로 쓴다.' does a weight-feel pulse (scale 1→1.06→1 with a quick letter-spacing tighten) and an accent underline draws under it (SVG stroke, #5B5BF0)."
- **g2** — free_design
  - span_sec: [17.0, 21.01]
  - free_design: { dominant_system: "object-in-sentence: the sentence parts to make a gap and a spinning 3D book drops into it", primitives: ["staggered-reveal", "overlay-pop"], density_topology: "sentence → object" }
  - anchors: [17.0, 17.48, 18.0, 18.99, 19.99, 20.5]
  - copy: { left: "바로바로 제미나이", right: "구글 AI", author: "공냥이", avatar: "assets/keyvisual/spr-robot.png", cover: "assets/covers/9791124516157.jpg" }
  - intent: "17.0 (downbeat): the slogan slides up and out; a one-line sentence '바로바로 제미나이 ___ 구글 AI' (h1 700, ink) sits at y≈540 with the two halves touching. 17.48 (beat): the halves slide apart (left moves left, right moves right, ~520px gap) and a small 3D book (book3d recipe, deep #223A4E spine, scale ~0.55) DROPS into the gap from above with a soft bounce and its contact shadow. 18.0: the book does a full spin in the gap (~0.9s). 18.99 (downbeat): under the sentence a pill sticker '공냥이' (#223A4E) pops; to its left a #1B1A1F avatar circle (110px) with assets/keyvisual/spr-robot.png pops in. 19.99: the whole sentence + book drift 20px up (camera ease). 20.5: subtle hold. Stripes transition covers from ~20.72."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 4.0s
- span_sec: [21.01, 25.01]
- pacing: beat_cut
- mood: [hype]
- feel: HIGH energy; 1 roll(s); key SURGE@22; strong hits [22.96, 24.96]
- role: series3
- pattern_hint: CODE-UI
- scene_color: #B9D7E0
- transition_out: iris 960,540
- sfx: typing@21.5, click@22.96, whoosh-short@23.05, pop@23.5
- hud_label: BARO 04 · 바이브 코딩
- book: 9791194383871 | 바로바로 바이브 코딩 with 커서 | 박현규 |  | assets/covers/9791194383871.jpg

### Groups

- **g1** — free_design
  - span_sec: [21.01, 25.01]
  - free_design: { dominant_system: "original code-editor mockup: three lines type on the beat, ▶ run, a terminal says success and a 3D book flies out of the editor toward the camera", primitives: ["typewriter-reveal", "crash-zoom-in", "overlay-pop"], density_topology: "type → run → reveal" }
  - anchors: [21.5, 21.99, 22.5, 22.96, 23.5, 23.99, 24.96]
  - copy: { tab: "baro.js", line1: "const 나 = \"AI 처음\";", line2: "바로바로.배운다(나);", line3: "// ✓ 바로 쓴다", terminal: "✓ 빌드 성공 · 0.51s", run: "▶ 실행", book_title: "바로바로 바이브 코딩 with 커서 AI", author: "박현규", avatar: "assets/keyvisual/spr-orange.png", cover: "assets/covers/9791194383871.jpg" }
  - intent: "GROUND #B9D7E0. 21.36: an ORIGINAL dark code editor window (#1B1A1F body, rounded 24px, tab 'baro.js', line numbers, Space Mono 30px, syntax colors limited to cream/#B9D7E0/accent/#E70080) slides up into the left 60% of the frame. Its top-right corner has a 72px avatar circle with assets/keyvisual/spr-orange.png. 21.5 / 21.99 / 22.5: one line types per beat (caret visible): line1, line2, line3. 22.96 (kick): the '▶ 실행' button (accent) depresses; a terminal strip under the code prints '✓ 빌드 성공 · 0.51s'. 23.05–23.5: a 3D book (book3d recipe, deep #0E4862 spine, scale ~0.8) launches out of the editor toward camera (z from −600 to 0 while moving right), landing at x≈1430 at rest pose (motion blur feel via 2 trailing ghost copies of the FLAT shadow only — never on the 3D chain). 23.5: caption '바로바로 바이브 코딩 with 커서 AI' + pill '박현규' (#0E4862). 24.96 (snare): the book bumps. Iris transition from center covers from ~24.72."

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 5.74s
- span_sec: [25.01, 30.75]
- pacing: beat_cut
- mood: [hype]
- feel: HIGH energy; 2 roll(s); key DROP@29; strong hits [27.45, 29.44, 29.95]
- role: finale
- pattern_hint: SPINE-STACK → row → lockup
- scene_color: #F4EFE6
- transition_out: none
- sfx: pop@25.5, pop@26.01, pop@26.49, pop@27.0, whoosh@27.4, chime@29.0, sparkle@29.5
- copy_hint: {"line": "시작은, 바로바로.", "cta": "goldenrabbit.co.kr"}

### Groups

- **g1** — free_design
  - span_sec: [25.01, 30.75]
  - free_design: { dominant_system: "spine stack: four 3D books drop one per beat into a pile showing their spines, then turn to the front into a row; slogan and logo lockup settle on cream", primitives: ["staggered-reveal", "overlay-pop", "blur-resolve"], density_topology: "accumulate → turn → lockup" }
  - anchors: [25.5, 26.01, 26.49, 27.0, 27.45, 28.49, 29.0, 29.49]
  - copy: { line: ["시작은,", "바로바로."], mark: "assets/brand/icon.png", wordmark: "GOLDEN RABBIT", url: "goldenrabbit.co.kr", books: [ {cover: "assets/covers/9791124516294.jpg", spine: "바로바로 챗GPT", deep: "#365A16"}, {cover: "assets/covers/9791124516133.jpg", spine: "바로바로 클로드", deep: "#622A0E"}, {cover: "assets/covers/9791124516157.jpg", spine: "바로바로 제미나이", deep: "#223A4E"}, {cover: "assets/covers/9791194383871.jpg", spine: "바로바로 바이브 코딩", deep: "#0E4862"} ] }
  - intent: "CREAM ground. 25.5 / 26.01 / 26.49 / 27.0 (beats): four 3D books (book3d recipe, scale ~0.55 each) DROP one per beat into a horizontal pile at center (books lying flat: rotationZ 90 so spines face the camera, stacked upward with small x jitter by index), each spine showing its title in cream on its deep color; soft contact shadow under the pile. 27.45 (kick): the pile un-stacks — each book stands up and turns to its FRONT, moving into a row of four across the lower half (y≈640, spacing ~330px, rest pose rotationY −18), staggered 0.08s. 28.49: '시작은,' (h1-light 300) + '바로바로.' (h1 700) slide in above the row (y≈250). 29.0 (downbeat): the logo lockup resolves top-center replacing the line: gold mark (~110px) + 'GOLDEN RABBIT' (Outfit 700, tracking .2em, ink) + 'goldenrabbit.co.kr' (Space Mono 28px, accent) — the slogan moves to sit between lockup and books, smaller. 29.49: each book gives a tiny hop in sequence. Hold perfectly still from ~30.0 to 30.75 (audio fades)."
