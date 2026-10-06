---
compositionId: bgm
duration_s: 32.0 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous
message: "바로 배워 바로 쓰는 — 바로바로 시리즈 4권"
variant: { name: baro-series-169-boldbeat-1, style: bold-beat, aspect: "16:9", seed: 5, intensity: hype }
style:
  font: "Paperlogy 800/400 (embedded, Korean) / Archivo Black (Latin caps) / Playfair Display italic 700 (mixed-word lowercase) / IBM Plex Mono (numerals)"
  palette: ["#FFE500", "#040404", "#F2F0EA", "#CEAE73"]
assets: "assets/covers/<isbn>.jpg × 4; assets/brand/icon.png (logo); assets/fonts/ Paperlogy; assets/keyvisual/baro-kv-01.png — user-supplied key visual (clay characters + glows on pure black) — MUST be used"
build_notes:
  - "follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)"
  - "a separate HUD overlay (compositions/hud.html) owns the corner chrome and the bottom band — keep readable content in y 104–984"
  - "register order hint for this seed: paper → yellow → ink"
  - "KEY VISUAL (user-supplied, MUST appear): layers in assets/keyvisual/ — kv-full.png (1536×1024, edges feathered), spr-green/orange/robot/yellow/person/laptop.png (feathered character crops), card-full.jpg (hard crop). Feathered layers ONLY on the INK register (#040404 = KV black, so they dissolve seamlessly); on yellow/paper use card-full.jpg as a tossed photo card with hard ink shadow. Never upscale a sprite beyond 1.4× its native size. Do NOT redraw, trace or recreate any character or logo from the KV — only place these PNG/JPG layers."
  - "series slogan (from the covers): 바로 배워 바로 쓰는! · cover tagline: 인공지능이 처음이어도 바로!"
avoid: ["text over covers", "gradients/glows", "copying reference videos' copy or layouts"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 5.0s
- span_sec: [0.0, 5.0]
- pacing: beat_cut
- mood: [cinematic]
- feel: VOID→MEDIUM→LOW energy; 0 roll(s); key SURGE@1, DROP@2; strong hits [0.42, 1.37]
- role: intro
- pattern_hint: HOOK-SLAM
- copy_hint: ["AI,", "처음이어도", "바로!"]

### Groups

- **g1** — free_design
  - span_sec: [0.0, 4.71]
  - free_design: { dominant_system: "hook slams on the two real kicks, then the key visual is born out of the black in the quiet before the drop", primitives: ["hard-cut", "palette-flip", "kinetic-letter-in", "blur-resolve"], density_topology: "replace, then single hero" }
  - anchors: [0.42, 1.37, 2.83, 4.0]
  - copy: { w1: "AI,", chip1: "AI", w2: "처음이어도", chip2: "FIRST TIME?" }
  - intent: "0–0.42: INK, empty except a blinking accent ■ at center. 0.42 (kick): 'AI,' slams center (display, paper) with chip 'AI' under it. 1.37 (kick, surge): 0ms flip to YELLOW, '처음이어도' lands (h1, ink; '처음' inside an ink label-box with yellow text) with chip 'FIRST TIME?'. 2.0–2.83: hold (silence). 2.83 (downbeat): 0ms flip to INK and the text clears; kv-full.png resolves out of the black (blur 18px→0 + scale 1.12→1.0 over ~1.1s, centered, height ≈1000px so its black edges melt into the ground). 4.0: a slow push continues (scale 1.0→1.04)."
- **g2** — free_design
  - span_sec: [4.71, 5.0]
  - free_design: { dominant_system: "one-word sting over the key visual right before the drop", primitives: ["braam-punch"], density_topology: "single hero" }
  - anchors: [4.71]
  - copy: "바로!"
  - intent: "4.71 (downbeat): the KV stays (same position as g1's end state — keep it in a shared layer), and '바로!' slams in the KV's dark top-left corner as an accent label-box (h1 150px, ink text on yellow box) with a weight punch. Hold to 5.0."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 5.85s
- span_sec: [5.0, 10.85]
- pacing: beat_cut
- mood: [hype]
- feel: MEDIUM→HIGH energy; 4 roll(s); key SURGE@5, DROP@10; strong hits [5.11, 5.62, 6.08, 6.55, 7.01, 7.5, 7.99, 8.45, 8.92, 9.38]
- role: series0
- pattern_hint: SERIES-TOSS
- hud_label: BARO 01 · 챗GPT
- book: 9791124516294 | 바로바로 챗GPT X 덕테이프 X 코덱스 | 박현규 |  | assets/covers/9791124516294.jpg

### Groups

- **g1** — free_design
  - span_sec: [5.0, 10.85]
  - free_design: { dominant_system: "crash-zoom from the KV's laptop logo into the series, the green chat-bubble character pops next to the title, then the cover is tossed on a yellow flip", primitives: ["crash-zoom-in", "hard-cut", "palette-flip", "overlay-pop", "staggered-exit"], density_topology: "replace one-at-a-time" }
  - anchors: [5.11, 5.62, 6.55, 7.01, 7.99, 8.45, 8.92, 10.33, 10.8]
  - copy: { kicker: "바로바로", title: "챗GPT", sub: ["덕테이프", "코덱스"], chip: "CHATGPT", cover: "assets/covers/9791124516294.jpg", book_title: "바로바로 챗GPT X 덕테이프 X 코덱스", author: "박현규" }
  - intent: "5.0: INK. spr-laptop.png fills the center (~1.35× native) and crash-zooms toward its logo (scale 1→1.35 + slight blur) until 5.11. 5.11 (snare): hard cut. spr-green.png (green chat bubble, ~1.25×) pops in on the RIGHT half with overshoot. On the left, the small kicker '바로바로' (h2, paper) and '챗GPT' (display, paper; 'GPT' half in Archivo Black) slam in, with chip 'CHATGPT'. 5.62 (kick): the bubble bumps 6%. 6.55 / 7.01 (snares): 'X 덕테이프' then 'X 코덱스' pop under the title as two yellow label boxes (ink text), one per snare. 7.99 (strongest snare): 0ms flip to YELLOW; the sprite cuts out (yellow register: no feathered layers), the title column turns ink, and the real cover is TOSSED in from bottom-right to center-right (rotation −6°, overshoot, hard 14px ink shadow, speed trail). The caption label box sits under it: '바로바로 챗GPT X 덕테이프 X 코덱스' / '박현규'. 8.45 / 8.92: confetti ● ▲ (ink) pop clear of the cover. 10.33: the cover arcs out up-right with a trail. 10.8: 0ms flip to INK; the title clears."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 6.36s
- span_sec: [10.85, 17.21]
- pacing: beat_cut
- mood: [hype]
- feel: MEDIUM→LOW→HIGH energy; 2 roll(s) incl. accel-roll; key SURGE@17; strong hits [11.29, 12.21, 12.7, 13.19, 13.65, 14.12, 14.58, 15.05, 16.0, 16.49]
- role: series1
- pattern_hint: FLIPBOOK-RESOLVE (override of SHELF — this span is one accel-roll, so the words should accelerate with it)
- hud_label: BARO 02 · 클로드
- book: 9791124516133 | 바로바로 클로드 with 코워크, 스킬, 클로드 코드, 디자인 | 차진우 | BEST | assets/covers/9791124516133.jpg

### Groups

- **g1** — free_design
  - span_sec: [10.85, 17.21]
  - free_design: { dominant_system: "accel-roll word flipbook: the cover's feature words cycle faster and faster beside the yellow character, resolving onto the cover", primitives: ["content-swap", "palette-flip", "overlay-pop", "staggered-exit"], density_topology: "accelerating cycle → resolve" }
  - anchors: [11.29, 12.21, 12.7, 13.19, 13.65, 14.12, 14.58, 15.05, 16.0, 16.49, 16.95]
  - copy: { kicker: "바로바로", title: "클로드", chip: "CLAUDE", flip_words: ["코워크", "스킬", "클로드 코드", "디자인", "82가지 실습"], cover: "assets/covers/9791124516133.jpg", book_title: "바로바로 클로드", book_sub: "with 코워크, 스킬, 클로드 코드, 디자인", author: "차진우", badge: "BEST" }
  - intent: "10.85: INK. 11.29 (kick): spr-yellow.png (yellow character with glasses, ~1.2×) peeks in from the LEFT edge (x slide + slight rotation, like it's leaning in). '클로드' (display, paper) slams right of center with the kicker '바로바로' above and the chip 'CLAUDE' below. 12.21→16.0 (accel-roll): under the title, ONE yellow label box (ink text, h2) swaps its word at 0ms on every listed hit — 코워크 → 스킬 → 클로드 코드 → 디자인 → 82가지 실습 → (repeat) — so the swaps speed up with the roll. These are texture words. 13.19 (strongest kick, 0.6): 0ms flip to YELLOW; the sprite cuts out, the title and flipbook re-ink (ink box with yellow text), and the cover is tossed in center-right (rotation +5°, hard shadow). 16.0: the flipbook stops on '82가지 실습'. 16.49 (snare): the caption label box locks under the cover ('BEST' chip + '바로바로 클로드' + 'with 코워크, 스킬, 클로드 코드, 디자인' + '차진우'), and is readable until the cut. 16.95: everything punches 3% into the surge."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 4.74s
- span_sec: [17.21, 21.95]
- pacing: beat_cut
- mood: [hype]
- feel: HIGH→MEDIUM energy; 1 roll(s); key DROP@18; strong hits [17.44, 17.88, 18.37, 18.86, 19.3, 19.78, 20.25, 20.73, 21.66]
- role: series2
- pattern_hint: MEGA-SPLIT
- hud_label: BARO 03 · 제미나이·구글 AI
- book: 9791124516157 | 바로바로 제미나이 구글 AI (catalog: 구글 AI 활용 입문서) | 공냥이 |  | assets/covers/9791124516157.jpg

### Groups

- **g1** — free_design
  - span_sec: [17.21, 21.95]
  - free_design: { dominant_system: "mega word whips in cropped on the surge snare, then a face-off: robot character vs the cover around a big ✕", primitives: ["hypercut-whip", "palette-flip", "overlay-pop", "screen-shake"], density_topology: "statement → pair" }
  - anchors: [17.44, 18.37, 18.86, 19.78, 20.73, 21.66]
  - copy: { mega: "제미나이", label: "구글 AI", chip: "GEMINI · GOOGLE AI", cover: "assets/covers/9791124516157.jpg", book_title: "바로바로 제미나이 구글 AI", author: "공냥이" }
  - intent: "17.21: YELLOW. 17.44 (snare 0.63): 'mega' word '제미나이' (360px, ink) whips in from the right with a speed trail, cropped off the bottom edge under the HUD band (mark it data-layout-allow-overlap). 18.37 (snare): '구글 AI' slams in an ink label-box (yellow text) top-right, with chip 'GEMINI · GOOGLE AI'. 18.86 (kick 0.54): 0ms flip to INK. The mega word shrinks to a vertical rail on the left edge (rotated −90°, h2, yellow). spr-robot.png (robot on books, ~1.3×) pops in left-center, and the cover is tossed in right-center (rotation +4°, 0 24px 60px shadow on ink). A big yellow ✕ sits between them. The caption label box goes under the cover ('바로바로 제미나이 구글 AI' / '공냥이'). 19.78: the robot bumps (a wave). 20.73: screen-shake ≤10px and a yellow ● ring pulse behind the ✕. 21.66: the robot and cover arc out on opposite parabolas."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 5.66s
- span_sec: [21.95, 27.61]
- pacing: beat_cut
- mood: [hype]
- feel: MEDIUM→HIGH energy; 4 roll(s); key SURGE@25; strong hits [22.15, 22.62, 23.08, 23.57, 24.03, 24.5, 25.45, 25.91, 26.4, 26.86]
- role: series3
- pattern_hint: TYPE-TOSS + CLIMAX-SLAM (override of SHELF — single book; typing suits the coding title; climax on the 25.45 surge)
- hud_label: BARO 04 · 바이브 코딩
- book: 9791194383871 | 바로바로 바이브 코딩 with 커서 | 박현규 |  | assets/covers/9791194383871.jpg

### Groups

- **g1** — free_design
  - span_sec: [21.95, 25.45]
  - free_design: { dominant_system: "code line types the title beside the orange monitor character, then the cover lands on paper while slogan marquee rows build into the surge", primitives: ["typewriter-reveal", "palette-flip", "overlay-pop"], density_topology: "type → accumulate" }
  - anchors: [22.15, 22.62, 23.08, 23.57, 24.03, 24.5]
  - copy: { kicker: "바로바로", title: "바이브 코딩", code: "> with 커서 AI_", chip: "VIBE CODING", cover: "assets/covers/9791194383871.jpg", book_title: "바로바로 바이브 코딩 with 커서 AI", author: "박현규", marquee: "바로 배워 ✦ 바로 쓰는 ✦" }
  - intent: "21.95: INK. 22.15 (snare): spr-orange.png (orange monitor bubble, ~1.25×) pops in on the RIGHT. On the left, '바이브 코딩' types in one syllable per hit (22.15/22.62/23.08 groups, display paper) with a blinking yellow caret, then the mono line '> with 커서 AI_' (IBM Plex Mono 700, yellow) and the chip 'VIBE CODING'. 23.57 (kick): 0ms flip to PAPER; the sprite cuts out, the text re-inks, the cover is tossed in center-right (hard ink shadow, rotation −4°), and the caption label box sits under it ('바로바로 바이브 코딩 with 커서 AI' / '박현규'). 24.03 / 24.5: two outline marquee rows '바로 배워 ✦ 바로 쓰는 ✦' slide in behind (top and bottom bands inside y 104–984, opposite directions, outline only, data-layout-ignore), accelerating into the surge."
- **g2** — free_design
  - span_sec: [25.45, 27.61]
  - free_design: { dominant_system: "CLIMAX — the series slogan slams with weight contrast, burst lines and confetti on the strongest surge, then a label box on the second hit", primitives: ["braam-punch", "radial-burst-lines", "particle-burst", "screen-shake", "freeze-hold"], density_topology: "slam → freeze" }
  - anchors: [25.45, 26.4, 27.35]
  - copy: ["바로 배워,", "바로 쓴다."]
  - intent: "25.45 (SURGE, energy 0.83): 0ms flip to YELLOW. '바로 배워,' (h1-light 400, ink) and '바로 쓴다.' (display 800, ink) slam together, centered, with ink radial burst lines and a confetti burst (● ■ ▲ ◆ ✕ in ink). 26.4 (kick): 0ms flip to INK, the text turns paper, '바로 쓴다.' snaps into a yellow label-box (ink text), and a screen-shake ≤10px. 27.35 (kick): the confetti bumps once, then everything freezes until 27.61."

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 4.39s
- span_sec: [27.61, 32.0]
- pacing: beat_cut
- mood: [cinematic]
- feel: MEDIUM→LOW energy; 3 roll(s); key none; strong hits [27.82, 28.28, 28.75, 29.23, 29.7, 30.19, 31.14, 31.21]
- role: finale
- pattern_hint: FINALE-BURST
- copy_hint: {"line": "지금, 바로.", "cta": "goldenrabbit.co.kr"}

### Groups

- **g1** — free_design
  - span_sec: [27.61, 32.0]
  - free_design: { dominant_system: "finale — the key visual returns whole, the four covers pop up in front of it, then the logo lockup takes over and the URL lands on the last kick with an icon burst", primitives: ["blur-resolve", "overlay-pop", "particle-burst", "flash-cut"], density_topology: "hero → full → single mark" }
  - anchors: [27.82, 29.23, 30.19, 31.14, 31.21]
  - copy: { line: "지금, 바로.", mark: "assets/brand/icon.png", wordmark: "GOLDEN·rabbit", chip: "바로바로 시리즈", url: "goldenrabbit.co.kr", covers: ["assets/covers/9791124516294.jpg", "assets/covers/9791124516133.jpg", "assets/covers/9791124516157.jpg", "assets/covers/9791194383871.jpg"] }
  - intent: "27.61: INK; kv-full.png returns large (height ≈ 900px, centered, y slightly above center) with a quick blur-resolve. 27.82 (kick): the four covers pop up in a row across the lower third, in front of the KV's dark lower band (≈230px tall each, spaced evenly, slight alternating rotation ±3°, staggered 0.06s, overshoot). 29.23 (kick): '지금, 바로.' slams in an accent label-box (h1, ink on yellow) in the KV's dark top-left area. 30.19 (kick): the KV slides up and dims to 35%, '지금, 바로.' clears, and the logo lockup resolves centered on a clean ink band: the gold mark (~140px) + the 'GOLDEN·rabbit' mixed wordmark (paper Archivo Black + yellow Playfair italic) + the chip '바로바로 시리즈' (yellow box, ink). The covers stay. 31.14 / 31.21 (double final kick): 'goldenrabbit.co.kr' pops in a yellow label-box (IBM Plex Mono 700, ink) next to the chip, and 8 small ORIGINAL line icons (book, pencil, lightning, sparkle, chat bubble, monitor, bookmark, star; 2px yellow strokes, simple SVG — no brand logos) burst around the lockup and settle. Everything bumps once on 31.21, then holds still to 32.0 (audio fades)."
