---
compositionId: bgm
duration_s: 46.6 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
mode: autonomous # flow: automation × storyboard: no
message: "더 탁월한 가치를 제공하는 콘텐츠 — 골든래빗의 시리즈별 대표 도서"
track_read: "129 BPM instrumental EDM excerpt (Mixkit 'Golden Storm', 34.99–81.59s of the original). Sparse breakdown 0–8 → synth surge 8–10 → silence 10–11 → dense kick/snare + hi-hat rolls 11–40 (peaks 17–19, 25–28, 34–36) → drop to silence 41 → three final hits 42.49 / 42.96 / 45.33 → fade."
style:
  font: "Paperlogy 800/500/400 (embedded @font-face, Korean) / Montserrat 600 (wordmark) / IBM Plex Mono 500 (Latin chrome)"
  palette: ["#0F0E0C", "#F4EFE6", "#CEAE73", "#1A1814", "#8C877E"]
assets: "assets/covers/ has 16 book-cover JPGs (goldenrabbit.co.kr); assets/brand/icon.png = gold logo mark; assets/fonts/ = Paperlogy TTFs"
build_notes:
  - "one paused timeline per frame; frame-local time = track_t − span_sec[0]"
  - "no remote assets; every path is relative to the project root (assets/...)"
  - "declare frame.md's three Paperlogy @font-face rules inside each frame's <template><style>"
  - "book covers: real JPG, never cropped / tinted / text-overlaid; radius 6px; shadow per frame.md book-cover"
  - "cover exits follow a PARABOLIC ARC (x travel + y arc + slight rotation) — never a flat linear slide"
  - "shapes (gold ring, disc, hairline, stub bar, sparkle, burst lines) move ON anchors — they are the percussion"
  - "readable Korean lines hold ≥ 3 beats (~1.4s); shorter = texture only"
avoid: ["generic left-to-right slideshow", "gradients or a 4th UI color", "tiny unreadable captions", "text over covers", "copying any reference video's exact look"]
---

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 11.0s
- span_sec: [0.0, 11.0]
- pacing: phrase_flow
- mood: [cinematic, elegant]
- feel: sparse breakdown — isolated kick pairs at 1.39/1.86, 3.27–4.23, 6.11, 7.06; synth surge 8.0–10.0 (downbeat 8.52); onset desert 10.0–11.0

### Groups

- **g1** — free_design
  - span_sec: [0.0, 8.52]
  - free_design: { dominant_system: "held kinetic statement on the dark register — three lines stack one per energy hit, then the question takes over", primitives: ["kinetic-letter-in", "mask-reveal", "negative-space-hold"], density_topology: "accumulate then replace" }
  - anchors: [1.39, 3.27, 6.11, 7.06]
  - copy: ["세상은 매일 바뀌고,", "배울 건 끝없이 쏟아진다.", "무엇부터 읽을까?"]
  - intent: "1.39: a 1px cream hairline draws across the lower third, and line 1 (h2, cream) letter-ins above it. 3.27: line 2 (h2, cream-muted → cream) letter-ins under line 1. 6.11: both lines clear upward and line 3 lands centered as h1 (150px). Its '?' is gold, with a gold ring (3px stroke, ~220px) scaling out behind it. 7.06: the ring pulses once and a few small 4-point gold sparkles (logo motif) blink on around the line. Ease every entrance (phrase_flow); nothing hard-cuts on the grid."
- **g2** — free_design
  - span_sec: [8.52, 11.0]
  - free_design: { dominant_system: "brand reveal — the gold logo mark is born from an iris ring and the lockup holds through the silence", primitives: ["iris-open", "braam-punch", "negative-space-hold"], density_topology: "single hero" }
  - anchors: [8.52, 9.4, 10.0]
  - copy: { mark: "assets/brand/icon.png", wordmark: "GOLDEN RABBIT", name: "골든래빗", tagline: "더 탁월한 가치를 제공하는 콘텐츠" }
  - intent: "8.52 (surge downbeat): a gold ring irises open from center and the logo mark (~300px) punches in with a weight slam (overshoot scale), centered above. Right after, '골든래빗' (h2, cream) and the 'GOLDEN RABBIT' wordmark (Montserrat, gold, wide tracking) rise in under the mark. 9.4: the tagline (lead, cream-muted) fades up. 10.0–11.0 (onset desert): everything holds dead still (negative-space-hold), with only a very slow ring breathe."

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 5.6s
- span_sec: [11.0, 16.6]
- pacing: beat_cut
- mood: [hype, playful]
- feel: dense kick/snare stream with short hi-hat fills 11.08–13.42, then a sustained hi-hat fill 13.68–16.49 building toward the 17s surge

### Groups

- **g1** — free_design
  - span_sec: [11.0, 16.6]
  - free_design: { dominant_system: "split stage — giant series title left, one hero cover at a time right; covers swap on strong hits and leave on a parabolic arc", primitives: ["braam-punch", "overlay-pop", "staggered-exit", "content-swap"], density_topology: "replace one-at-a-time" }
  - anchors: [11.31, 12.24, 13.68, 15.07, 16.02]
  - copy: { kicker: "SERIES 01", title: "이게 되네?", sub: "AI 미친 활용법", books: [ { cover: "assets/covers/gemini81.jpg", title: "제미나이 완전 미친 활용법 81제", author: "오힘찬", badge: "BEST" }, { cover: "assets/covers/openclaw50.jpg", title: "오픈클로 미친 활용법 50제", author: "한준구", badge: "BEST" }, { cover: "assets/covers/ai-product-image.jpg", title: "AI 상품 이미지 만들기", author: "박상균", badge: "NEW" } ] }
  - intent: "Hard cut in from f1's still lockup. 11.31: '이게 되네?' slams in left (display ~200px, cream, the '?' in gold) with the kicker 'SERIES 01' (mono, gold) and the sub (lead, cream-muted) under a gold stub bar. 12.24: cover 1 pops up on the right (~520px tall) with an overshoot, a gold ring kicks out behind it, and a caption block (title + author, plus a small gold BEST/NEW chip) pops beside it. 13.68: cover 1 leaves on a parabolic arc (up-right, rotating) as cover 2 pops in, and the caption swaps at 0ms. 15.07: same move for cover 3. 16.02: a gold ring pulse plus a slight push-in on the whole stage to lead into the surge. The title stays put the whole time; only the right side changes."

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 6.38s
- span_sec: [16.6, 22.98]
- pacing: beat_cut
- mood: [hype]
- feel: surge at 17 into an accelerating hi-hat roll 17.69–22.85 — a tightening onset stream with strong kicks at 16.97, 18.39, 19.81, 20.73, 21.69

### Groups

- **g1** — template: `card-flyby`
  - span_sec: [16.6, 22.98]
  - params: { theme: "mono", bgColor: "#0F0E0C", yaw: -12, cards: "[{tag:'SERIES 02', title:'바로 배워 바로 쓰는', meta:'바로바로', color:'#CEAE73'}, {tag:'BEST', title:'바로바로 클로드', meta:'차진우', cover:'assets/covers/baro-claude.jpg'}, {tag:'바로바로', title:'챗GPT X 덕테이프 X 코덱스', meta:'박현규', cover:'assets/covers/baro-chatgpt-codex.jpg'}, {tag:'AI 비서', title:'유튜브 AI 비서 고용하기', meta:'조현정', cover:'assets/covers/youtube-ai-secretary.jpg'}, {tag:'돈이 되네?', title:'네이버 블로그', meta:'정소희', cover:'assets/covers/naver-blog.jpg'}]", landings: "[16.97, 18.39, 19.81, 20.73, 21.69]" }
  - role_bindings: { landing: { times: [16.97, 18.39, 19.81, 20.73, 21.69] }, hold: { from: 21.69, to: 22.98 } }
  - copy: "바로 배워 바로 쓰는 — 바로바로"
  - intent: "Fork card-flyby, keep its depth-column flyby + solid wipe + accelerating dwell, and re-skin it in the brand. Card 1 is a type card: a gold field with '바로 배워 바로 쓰는' in ink-black (h2) and 'SERIES 02' as mono tag. Cards 2–5 are BOOK cards: dark card (#1A1814) with the real cover on the left (~70% of the card height) and the title (h3, cream), author (caption, cream-muted) and tag chip (gold) on the right. Wipes alternate gold and ink-black. The last card (네이버 블로그) is the held final card through 22.98."

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 4.72s
- span_sec: [22.98, 27.7]
- pacing: beat_cut
- mood: [cinematic, hype]
- feel: short roll 23.13–23.80, LOW dip 24–25, then HIGH 25–28 over a sustained fill 24.06–26.86 with kicks 24.54, 25.47, 26.42

### Groups

- **g1** — free_design
  - span_sec: [22.98, 27.7]
  - free_design: { dominant_system: "register flip — the gold field states the series, then the dark stage stages a two-cover face-off", primitives: ["system-replace", "palette-flip", "overlay-pop", "screen-shake"], density_topology: "statement → pair" }
  - anchors: [22.98, 24.06, 24.54, 25.47, 26.42]
  - copy: { kicker: "SERIES 03", title: "요즘 개발", sub: "현업이 쓰는 진짜 AI 개발", books: [ { cover: "assets/covers/danggeun-ai.jpg", title: "요즘 당근 AI 개발", author: "당근 팀", badge: "BEST" }, { cover: "assets/covers/vibe-harness.jpg", title: "요즘 바이브 코딩 하네스 with 클로드 코드", author: "조성진" } ] }
  - intent: "22.98: a 0ms system-replace into the GOLD register: '요즘 개발' as display (~220px, ink-black), kicker 'SERIES 03' and sub (lead, ink 70%). 24.06: the title shrinks and snaps to the top-left (h2) while the ground flips back to ink-black at 0ms (palette-flip), and the title turns cream with a gold sub. 24.54: cover 1 (danggeun-ai, ~500px) arcs in from bottom-left to the left-center slot with an overshoot, and its caption pops under it. 25.47: cover 2 (vibe-harness) arcs in from bottom-right to the right-center slot, caption under it. A thin gold 'VS'-style hairline with a small disc sits between them. 26.42: subtle screen-shake (≤8px) and a gold ring burst behind both. Hold to 27.7."

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 8.77s
- span_sec: [27.7, 36.47]
- pacing: beat_cut
- mood: [hype, aggressive]
- feel: MEDIUM–HIGH dense kick/snare stream with short fills 27.84–32.55, then a sustained fill 32.81–35.39 driving the track's biggest SURGE (energy 0.91 at 34), hard stop at 36

### Groups

- **g1** — free_design
  - span_sec: [27.7, 32.68]
  - free_design: { dominant_system: "count-in stack — four exam books fan in one per strong kick while a mono counter ticks 01→04", primitives: ["staggered-reveal", "overlay-pop", "content-swap"], density_topology: "accumulate" }
  - anchors: [28.3, 29.26, 30.19, 31.14, 32.09]
  - copy: { kicker: "SERIES 04", title: "빠따", sub: "빠르게 따는 자격증", books: [ { cover: "assets/covers/ppatta-computer1.jpg", title: "컴퓨터활용능력 1급 필기+실기", author: "이강용(컴활킹)", badge: "NEW" }, { cover: "assets/covers/ppatta-computer2.jpg", title: "컴퓨터활용능력 2급 필기+실기", author: "이강용(컴활킹)", badge: "NEW" }, { cover: "assets/covers/ppatta-bigdata-written.jpg", title: "빅데이터분석기사 필기", author: "이유성, 조영훈" }, { cover: "assets/covers/ppatta-bigdata-practical.jpg", title: "빅데이터분석기사 실기", author: "조영훈, 이유성", badge: "NEW" } ] }
  - intent: "28.3: kicker 'SERIES 04', '빠따' (display, cream) and the sub (h3, gold) land top-left, and a mono counter '00/04' appears top-right. 29.26 / 30.19 / 31.14 / 32.09: one cover each pops into a fanned row across the lower 2/3 (each ~400px tall, slight alternating rotation −4°..+4°, overlapping ~20%). The counter ticks 01→04 at 0ms, and a one-line caption (caption size, cream) for the newest book swaps under the row at 0ms."
- **g2** — free_design
  - span_sec: [32.68, 36.47]
  - free_design: { dominant_system: "climax slam — the fan compresses during the roll, then the statement slams on the surge in the gold register", primitives: ["dolly-zoom", "braam-punch", "radial-burst-lines", "screen-shake", "freeze-hold"], density_topology: "build → slam → freeze" }
  - anchors: [32.81, 33.97, 34.97, 35.88]
  - copy: "합격까지, 빠르게."
  - intent: "32.81–33.97 (sustained fill): the four-cover fan slides together into a tight stack and the stage slowly pushes in (a macro build, eased). 33.97 (SURGE onset): a 0ms flip to the GOLD register, '합격까지, 빠르게.' slams in as display (ink-black, ~200px) with a weight punch and radial burst lines in ink, and the stacked covers shrink to sit below the line. 34.97: a second hit with a screen-shake (≤10px) and a gold-deep ring burst. 35.88: freeze-hold everything (hard stop at 36) until 36.47."

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
  - free_design: { dominant_system: "shelf conveyor — a gold hairline shelf draws, three covers settle onto it one per kick, then all arc away before the silence", primitives: ["directional-fill", "staggered-reveal", "staggered-exit"], density_topology: "accumulate → clear" }
  - anchors: [36.83, 37.76, 38.71, 39.66, 40.12, 40.59]
  - copy: { kicker: "INSIGHT", title: "생각을 넓히는 책", books: [ { cover: "assets/covers/ai-gukburon.jpg", title: "AI 국부론", author: "이승현" }, { cover: "assets/covers/ai-literacy.jpg", title: "AI는 생각하지 않는다, AI 리터러시", author: "이제현", badge: "COMING SOON" }, { cover: "assets/covers/f1-glossary.jpg", title: "F1 용어집 1211", author: "윤재수" } ] }
  - intent: "Hard cut from f5's frozen gold slam to the dark register. 36.47: kicker 'INSIGHT' (mono, gold) and '생각을 넓히는 책' (h2, cream) top-left, and a 1px gold shelf line draws left→right across the lower third (directional-fill). 36.83 / 37.76 / 38.71: covers drop onto the shelf left / center / right (~420px tall), each with a short settle bounce and its caption (title + author) popping under it. 39.66: a gold ring pulse behind the center cover. 40.12: all three covers leave on staggered parabolic arcs (up and outward, rotating). 40.59: the title and shelf wipe out, so the frame is nearly empty by 41.0 and hands off to the silence."

## Frame 7 — f7

- src: compositions/frames/07-f7.html
- duration: 5.6s
- span_sec: [41.0, 46.6]
- pacing: phrase_flow
- mood: [cinematic, warm]
- feel: drop to near-silence 41–42, then three isolated final hits 42.49 / 42.96 / 45.33 over a short HIGH swell 43–44, fading out 45.6–46.6

### Groups

- **g1** — free_design
  - span_sec: [41.0, 46.6]
  - free_design: { dominant_system: "finale pop — a quiet line in the silence, then every book bursts out at once on the hits and resolves into the logo lockup", primitives: ["negative-space-hold", "mosaic-pack", "particle-burst", "blur-resolve"], density_topology: "empty → full burst → single mark" }
  - anchors: [41.0, 42.49, 42.96, 43.42, 45.33]
  - copy: { line: "당신의 다음 한 권", mark: "assets/brand/icon.png", wordmark: "GOLDEN RABBIT", name: "골든래빗", url: "goldenrabbit.co.kr", covers: ["assets/covers/gemini81.jpg", "assets/covers/openclaw50.jpg", "assets/covers/ai-product-image.jpg", "assets/covers/baro-claude.jpg", "assets/covers/baro-chatgpt-codex.jpg", "assets/covers/youtube-ai-secretary.jpg", "assets/covers/naver-blog.jpg", "assets/covers/danggeun-ai.jpg", "assets/covers/vibe-harness.jpg", "assets/covers/ppatta-computer1.jpg", "assets/covers/ppatta-computer2.jpg", "assets/covers/ppatta-bigdata-written.jpg", "assets/covers/ppatta-bigdata-practical.jpg", "assets/covers/ai-gukburon.jpg", "assets/covers/ai-literacy.jpg", "assets/covers/f1-glossary.jpg"] }
  - intent: "41.0–42.49 (silence): '당신의 다음 한 권' (h2, cream) fades up centered in empty black (negative-space-hold). 42.49 (kick): the line scales away, and all 16 covers POP out from the center into a 8×2 grid (~200px tall each) with staggered overshoot (stagger from the center outward, the burst finishes by ~42.9), plus a gold sparkle burst. This is the reference's '팡' moment. 42.96 (kick): a second pulse, where every cover bumps +6% and a gold ring wave sweeps out. 43.42: the grid recedes (scales to ~0.85, dims to ~35%), and the logo lockup resolves center over it with blur-resolve: mark (~200px), '골든래빗' (h2, cream), 'GOLDEN RABBIT' wordmark (gold). 45.33 (final kick): 'goldenrabbit.co.kr' (mono/label at ~30px, gold) pops under the lockup, and a gold disc pulse sits behind the mark. Hold perfectly still to 46.6 while the audio fades."
