---
compositionId: bgm
duration_s: 46.6 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "골든래빗 — 시리즈별 대표 도서 16권, 비트에 맞춰 과감하게"
track_read: "129 BPM instrumental EDM excerpt. Beat = 0.465s. Sparse breakdown with real kick pairs 0–8 → surge 8–10 → silence 10–11 → dense kick/snare + hi-hat rolls 11–40 (peaks 17–19, 25–28, 34–36) → silence 41 → final hits 42.49 / 42.96 / 45.33."
style:
  font: "Paperlogy 800/400 (embedded, Korean) / Archivo Black (Latin caps) / Playfair Display italic 700 (mixed-word lowercase) / IBM Plex Mono (numerals)"
  palette: ["#FFE500", "#0B0B0B", "#F2F0EA", "#CEAE73"]
assets: "assets/covers/ = 16 cover JPGs; assets/brand/icon.png = gold logo mark (only gold element); assets/fonts/ = Paperlogy"
build_notes:
  - "one paused timeline per frame; frame-local time = track_t − span_sec[0]"
  - "CSS: style the root as plain #stage (NEVER #stage[data-composition-id=…]); prefix every id/class with the frame tag (f1_, f2_ …)"
  - "a separate HUD overlay (compositions/hud.html) draws corner labels + bottom ticker: keep readable content inside y 104–984; frames draw NO corner chrome"
  - "register flips (yellow / ink / paper ground) are 0ms tl.set ON the listed hits"
  - "one word per beat for texture words; titles and hero lines hold ≥ 3 beats (~1.4s)"
  - "covers: real JPG, never cropped / tinted / text-overlaid; tossed-card rotation allowed; exits on a parabolic arc with speed trails"
  - "motion via transforms only; marquee offsets derived from timeline time (tweens), never CSS animation"
avoid: ["gold anywhere except the logo mark", "gradients / glows", "slow fades on hits", "copying any reference video's copy, names or exact layouts", "text over covers"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 11.0s
- span_sec: [0.0, 11.0]
- pacing: beat_cut
- mood: [hype, cinematic]
- feel: sparse breakdown but every anchor is a MEASURED kick (events[]), not grid — 1.39/1.86, 3.27/3.76/4.23, 6.11, 7.06; synth surge 8.0–10.0 (downbeat 8.52); silence 10.0–11.0

### Groups

- **g1** — free_design
  - span_sec: [0.0, 8.52]
  - free_design: { dominant_system: "word-per-kick slams with 0ms register flips; a pair chip under each hero word; mega word crops off the frame", primitives: ["hard-cut", "palette-flip", "kinetic-letter-in", "flash-cut"], density_topology: "replace one-per-hit, then accumulate into a marquee" }
  - anchors: [0.95, 1.39, 1.86, 3.27, 3.76, 4.23, 6.11, 7.06]
  - copy: ["AI는", "매일", "바뀐다.", "그래서", "우리는", "읽는다."]
  - intent: "0–0.95: ink ground, empty except a tiny blinking yellow ■ at center. 1.39: 'AI는' (display, paper) slams in centered and the chip 'AI' sits under it. 1.86: flip to YELLOW, 'AI는' cuts to '매일' (display, ink) with the chip 'EVERY DAY'. 3.27: flip to INK and '바뀐다.' lands as h1 with the period in yellow. A yellow label-box snaps around '바뀐다' left-to-right (chip 'CHANGES'). 3.76: flip to PAPER and '그래서' appears small (h2, ink 60%). 4.23: '우리는' (h1-light, 400) appears under it, and confetti ▲ ● pop in two corners. 6.11: flip to YELLOW and '읽는다.' crashes in as MEGA type (360px, ink) cropped off the left and right edges, with a speed trail from the right (chip 'WE READ' in an ink box). 7.06: the mega word shrinks into the top row of a 4-row marquee ('읽는다 ✦ READ ✦' repeated, alternating filled/outline, rows sliding opposite ways) that keeps moving into the surge."
- **g2** — free_design
  - span_sec: [8.52, 11.0]
  - free_design: { dominant_system: "brand reveal — the yellow marquee is wiped by ink, the GOLD logo mark (first and only gold) punches in with a mixed-type wordmark", primitives: ["system-replace", "braam-punch", "iris-open"], density_topology: "single hero" }
  - anchors: [8.52, 9.4, 10.0]
  - copy: { mark: "assets/brand/icon.png", wordmark: "GOLDEN·rabbit", name: "골든래빗", tagline: "더 탁월한 가치를 제공하는 콘텐츠" }
  - intent: "8.52 (surge downbeat): a 0ms system-replace to the INK register. The gold mark (~260px) punches in center with overshoot, and a yellow ring irises out once behind it. The wordmark sits right under it: 'GOLDEN' in Archivo Black (paper) + 'rabbit' in Playfair Display italic (yellow). '골든래빗' follows in a yellow label-box chip (ink text). 9.4: the tagline (caption, paper 60%) types in word by word. 10.0–11.0 (silence): dead still, then 2 small yellow confetti ◆ blink once at 10.4."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 5.6s
- span_sec: [11.0, 16.6]
- pacing: beat_cut
- mood: [hype, playful]
- feel: dense kick/snare stream with short hi-hat fills 11.08–13.42, sustained fill 13.68–16.49 building to the 17s surge

### Groups

- **g1** — free_design
  - span_sec: [11.0, 16.6]
  - free_design: { dominant_system: "series title split into two slams, then three tossed covers each landing with a register flip; a marquee of the series name runs as texture behind the covers", primitives: ["hard-cut", "palette-flip", "overlay-pop", "staggered-exit"], density_topology: "replace one-at-a-time" }
  - anchors: [11.31, 11.77, 12.24, 13.68, 15.07, 16.02]
  - copy: { kicker: "SERIES 01", title: ["이게", "되네?"], chip: "IT WORKS?", books: [ { cover: "assets/covers/gemini81.jpg", title: "제미나이 완전 미친 활용법 81제", author: "오힘찬", badge: "BEST" }, { cover: "assets/covers/openclaw50.jpg", title: "오픈클로 미친 활용법 50제", author: "한준구", badge: "BEST" }, { cover: "assets/covers/ai-product-image.jpg", title: "AI 상품 이미지 만들기", author: "박상균", badge: "NEW" } ] }
  - intent: "11.31: YELLOW ground, '이게' in an ink label-box (h1, yellow text) slams top-left. 11.77: '되네?' crashes in beside it as display (ink), and the '?' wobbles. The chip 'IT WORKS?' sits under it. 12.24: flip to INK; the title shrinks to a left column (h2, paper, '되네?' stays in a yellow box), and cover 1 is TOSSED in from bottom-right (rotation −6°, overshoot, speed trail). Its caption is a label box: a yellow 'BEST' chip plus the title in paper caption under the cover. A faint outline marquee '이게 되네? ✦' runs behind the cover, outlined only. 13.68: flip to PAPER; cover 1 arcs out up-left and cover 2 is tossed in (rotation +5°), caption swaps at 0ms. 15.07: flip to YELLOW and cover 3 comes in the same way (hard offset ink shadow). 16.02: two confetti ■ ▲ pop and the whole stage punches in 4%."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 6.38s
- span_sec: [16.6, 22.98]
- pacing: beat_cut
- mood: [hype]
- feel: surge at 17 into an accelerating hi-hat roll 17.69–22.85; strong kicks 16.97, 18.39, 19.81, 20.73, 21.69

### Groups

- **g1** — template: `card-flyby`
  - span_sec: [16.6, 22.98]
  - params: { theme: "mono", bgColor: "#0B0B0B", yaw: -12, cards: "[{tag:'SERIES 02', title:'바로 배워 / 바로 쓰는', meta:'BARO·baro', color:'#FFE500'}, {tag:'BEST', title:'바로바로 클로드', meta:'차진우', cover:'assets/covers/baro-claude.jpg', color:'#F2F0EA'}, {tag:'바로바로', title:'챗GPT X 덕테이프 X 코덱스', meta:'박현규', cover:'assets/covers/baro-chatgpt-codex.jpg', color:'#FFE500'}, {tag:'AI 비서', title:'유튜브 AI 비서 고용하기', meta:'조현정', cover:'assets/covers/youtube-ai-secretary.jpg', color:'#F2F0EA'}, {tag:'돈이 되네?', title:'네이버 블로그', meta:'정소희', cover:'assets/covers/naver-blog.jpg', color:'#FFE500'}]", landings: "[16.97, 18.39, 19.81, 20.73, 21.69]" }
  - role_bindings: { landing: { times: [16.97, 18.39, 19.81, 20.73, 21.69] }, hold: { from: 21.69, to: 22.98 } }
  - copy: "바로 배워 / 바로 쓰는 — BARO·baro"
  - intent: "Fork card-flyby with all its motion: a depth column, the solid wipe on each landing, and dwells that shrink so the deck accelerates. Re-skin it LOUD. Card faces alternate YELLOW and PAPER on an INK stage, with square corners and a hard 16px ink offset shadow. Card 1 is a type card: '바로 배워' (h1-light) over '바로 쓰는' (h1, 800), with the mixed-word chip 'BARO·baro' (Archivo Black + Playfair italic). Cards 2–5 are book cards: the real cover on the left, and on the right an ink label-box tag chip, the title (h2, ink), the author (caption). Wipes are solid INK. Between landings, a big yellow counter '01'→'05' (IBM Plex Mono 700, ~120px) ticks at 0ms in the stage corner inside the safe area. The last card holds to 22.98 while two confetti ✕ ● pop on 22.64."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 4.72s
- span_sec: [22.98, 27.7]
- pacing: beat_cut
- mood: [hype, aggressive]
- feel: short roll 23.13–23.80, LOW dip 24–25, then HIGH 25–28 over a sustained fill 24.06–26.86 with kicks 24.54, 25.47, 26.42

### Groups

- **g1** — free_design
  - span_sec: [22.98, 27.7]
  - free_design: { dominant_system: "mega-type statement cropped off the frame, then a split stage: a vertical rotated series word on the left edge, two covers face off with label-box captions", primitives: ["system-replace", "palette-flip", "hypercut-whip", "screen-shake"], density_topology: "statement → pair" }
  - anchors: [22.98, 23.45, 24.06, 24.54, 25.47, 26.42]
  - copy: { kicker: "SERIES 03", title: ["요즘", "개발"], chip: "DEV NOW", books: [ { cover: "assets/covers/danggeun-ai.jpg", title: "요즘 당근 AI 개발", author: "당근 팀", badge: "BEST" }, { cover: "assets/covers/vibe-harness.jpg", title: "요즘 바이브 코딩 하네스 with 클로드 코드", author: "조성진" } ] }
  - intent: "22.98: YELLOW ground. '요즘' as MEGA (360px, ink) whips in from the right with a speed trail, cropped off the bottom edge. 23.45: '개발' slams next to it in an ink label-box (yellow text), with the chip 'DEV NOW'. 24.06: a 0ms flip to INK. The title rotates to a vertical word on the left edge ('요즘 개발' rotated −90°, h2, yellow) next to the small mono label 'SERIES 03'. 24.54: cover 1 is tossed in left-center (rotation −5°), with caption label boxes under it (a yellow BEST chip and the title in paper). 25.47: flip to PAPER, and cover 2 is tossed in right-center (rotation +4°, hard ink offset shadow), with a big ink '×' between the two covers. 26.42: screen-shake (≤10px) and a yellow ● burst ring behind the ×. Hold to 27.7."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 8.77s
- span_sec: [27.7, 36.47]
- pacing: beat_cut
- mood: [hype, aggressive]
- feel: dense kick/snare stream with short fills 27.84–32.55, sustained fill 32.81–35.39 driving the biggest SURGE (energy 0.91 at 34), hard stop at 36

### Groups

- **g1** — free_design
  - span_sec: [27.7, 32.68]
  - free_design: { dominant_system: "count-in — giant numerals 01→04 punch on each strong kick, each bringing one exam book; ground flips every number", primitives: ["counting-punch", "palette-flip", "overlay-pop", "hard-cut"], density_topology: "replace number, accumulate covers" }
  - anchors: [28.3, 29.26, 30.19, 31.14, 32.09]
  - copy: { kicker: "SERIES 04", title: "빠따", chip: "FAST PASS", sub: "빠르게 따는 자격증", books: [ { cover: "assets/covers/ppatta-computer1.jpg", title: "컴퓨터활용능력 1급", author: "이강용(컴활킹)", badge: "NEW" }, { cover: "assets/covers/ppatta-computer2.jpg", title: "컴퓨터활용능력 2급", author: "이강용(컴활킹)", badge: "NEW" }, { cover: "assets/covers/ppatta-bigdata-written.jpg", title: "빅데이터분석기사 필기", author: "이유성, 조영훈" }, { cover: "assets/covers/ppatta-bigdata-practical.jpg", title: "빅데이터분석기사 실기", author: "조영훈, 이유성", badge: "NEW" } ] }
  - intent: "28.3: INK ground. '빠따' as display (yellow) top-left, with the chip 'FAST PASS' (ink on paper box) and the sub (caption, paper 60%). 29.26 / 30.19 / 31.14 / 32.09: on each kick the ground flips (YELLOW, INK, PAPER, YELLOW). A giant numeral ('01'…'04', IBM Plex Mono 700, ~300px, outline 3px in ink or paper) punches in at the right, and one cover is tossed into a fanned stack lower-center, each rotated a little differently. The newest book's caption swaps at 0ms as a label box (title + author)."
- **g2** — free_design
  - span_sec: [32.68, 36.47]
  - free_design: { dominant_system: "climax — marquee rows build during the roll, then the statement slams with weight contrast and confetti on the surge", primitives: ["braam-punch", "radial-burst-lines", "screen-shake", "particle-burst", "freeze-hold"], density_topology: "build → slam → freeze" }
  - anchors: [32.81, 33.97, 34.97, 35.88]
  - copy: { line: ["합격까지,", "빠르게."], marquee: "FAST PASS ✦ 빠따 ✦" }
  - intent: "32.81–33.97 (sustained fill): INK ground. The covers compress into a tight stack, and 3 marquee rows ('FAST PASS ✦ 빠따 ✦', alternating outline/filled, opposite directions) slide in behind them, accelerating. 33.97 (SURGE): 0ms flip to YELLOW. '합격까지,' (h1-light 400, ink) and '빠르게.' (display 800, ink, in nothing but weight) slam together, with radial burst lines (ink) and a confetti burst of ● ■ ▲ ◆ ✕ (ink). The stack shrinks below the line. 34.97: flip to INK, the text turns paper, '빠르게.' snaps into a yellow label-box, and a screen-shake ≤10px fires. 35.88: freeze everything (hard stop at 36) until 36.47."

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 4.53s
- span_sec: [36.47, 41.0]
- pacing: beat_cut
- mood: [elegant, hype]
- feel: MEDIUM dense with a sustained hi-hat fill 36.59–40.12 into a DROP to silence at 41

### Groups

- **g1** — free_design
  - span_sec: [36.47, 41.0]
  - free_design: { dominant_system: "editorial paper register — a vertical rotated word on the left, one verb per kick, each bringing one cover into a tossed collage; everything clears on parabolic arcs before the silence", primitives: ["hard-cut", "staggered-reveal", "staggered-exit"], density_topology: "accumulate → clear" }
  - anchors: [36.83, 37.76, 38.71, 39.66, 40.12, 40.59]
  - copy: { vertical: "INSIGHT", words: ["넓게,", "깊게,", "읽는다."], books: [ { cover: "assets/covers/ai-gukburon.jpg", title: "AI 국부론", author: "이승현" }, { cover: "assets/covers/ai-literacy.jpg", title: "AI는 생각하지 않는다, AI 리터러시", author: "이제현", badge: "COMING SOON" }, { cover: "assets/covers/f1-glossary.jpg", title: "F1 용어집 1211", author: "윤재수" } ] }
  - intent: "36.47: hard cut to PAPER. 'INSIGHT' is set vertically up the left edge (Archivo Black, ~200px, ink, rotated −90°, cropped by the top/bottom of the frame), and a mono label 'SERIES 05' sits beside it. 36.83 / 37.76 / 38.71: on each kick a verb lands top-right ('넓게,' 400 → '깊게,' 400 → '읽는다.' 800, each replacing the last, h1 size), and one cover is tossed into a 3-cover collage (rotations −6°, +3°, −2°, hard ink shadows) with a small label-box caption. 39.66: flip to YELLOW and confetti ◆ ● pop. 40.12: all covers leave on staggered parabolic arcs up and outward, with speed trails. 40.59: flip to INK and the rest wipes off, so the frame is empty ink by 41.0."

## Frame 7 — f7

- src: compositions/frames/07-f7.html
- duration: 5.6s
- span_sec: [41.0, 46.6]
- pacing: beat_cut
- mood: [hype, warm]
- feel: silence 41–42 then three MEASURED final kicks 42.49 / 42.96 / 45.33 (events[]), a short swell 43–44, fade 45.6–46.6

### Groups

- **g1** — free_design
  - span_sec: [41.0, 46.6]
  - free_design: { dominant_system: "finale pop — a question in silence, then all 16 covers burst into a grid with confetti, then the gold logo resolves with an icon burst", primitives: ["negative-space-hold", "mosaic-pack", "particle-burst", "flash-cut", "blur-resolve"], density_topology: "empty → full burst → single mark" }
  - anchors: [41.0, 42.49, 42.96, 43.42, 45.33]
  - copy: { line: "다음 한 권은?", mark: "assets/brand/icon.png", wordmark: "GOLDEN·rabbit", name: "골든래빗", url: "goldenrabbit.co.kr", covers: ["assets/covers/gemini81.jpg", "assets/covers/openclaw50.jpg", "assets/covers/ai-product-image.jpg", "assets/covers/baro-claude.jpg", "assets/covers/baro-chatgpt-codex.jpg", "assets/covers/youtube-ai-secretary.jpg", "assets/covers/naver-blog.jpg", "assets/covers/danggeun-ai.jpg", "assets/covers/vibe-harness.jpg", "assets/covers/ppatta-computer1.jpg", "assets/covers/ppatta-computer2.jpg", "assets/covers/ppatta-bigdata-written.jpg", "assets/covers/ppatta-bigdata-practical.jpg", "assets/covers/ai-gukburon.jpg", "assets/covers/ai-literacy.jpg", "assets/covers/f1-glossary.jpg"] }
  - intent: "41.0–42.49 (silence): INK ground, '다음 한 권은?' (h1, paper; the '?' in a yellow label-box) types in one syllable at a time. 42.49 (kick): a 0ms flip to YELLOW and all 16 covers burst out of the center into an 8×2 grid (~200px tall, slight random-by-index rotation ±4°, hard ink offset shadows), staggered from the center outward, with an ink confetti burst (● ■ ▲ ◆ ✕). 42.96 (kick): flip to INK; every cover bumps +6% and the confetti reverses to yellow/paper. 43.42: the grid parts to the top and bottom edges (staying inside y 104–984) and dims to 40%. In the clear middle band the logo resolves: the GOLD mark (~180px) + 'GOLDEN·rabbit' mixed wordmark (paper Archivo Black + yellow Playfair italic) + the chip '골든래빗' (yellow box, ink). 45.33 (final kick): 'goldenrabbit.co.kr' pops in a yellow label-box (IBM Plex Mono 700, ink). Eight small original line icons (book, pencil, lightning bolt, sparkle, bar chart, speech bubble, bookmark, star; 2px yellow strokes, simple SVG) burst outward around the logo and settle. Hold still to 46.6."
