---
compositionId: bgm
duration_s: 189.96 # == audiomap.audio.duration_sec
canvas: { w: 1920, h: 1080, fps: 30 }
style:
  font: "Noto Serif KR (variable 200–900) / Cormorant Garamond Italic (title-en only)"
  palette: ["#0B1230", "#1B1F4E", "#FFF4D6", "#FFD27A", "#DCEBFF", "#F4F1EA"]
assets: "no user media. Shared motifs: assets/motifs/bottle.svg (inline it), assets/motifs/sparkle.svg (path). Fonts in assets/fonts/."
build_notes:
  - "one paused timeline per frame; #stage background TRANSPARENT — compositions/sky.html (track 0) paints the sky, stars, hill and camera tilt under every frame; compositions/overlay.html (track 3) adds vignette + grain on top"
  - "lyric timing truth = PROJECT_DIR/lyrics.json (track seconds). A line must be fully legible at its onset and stay through vocal_end"
  - "no HUD, no section names, no frame numbers, no timers/progress, no BPM, no credits besides the song title"
  - "no remote assets; fonts via the @font-face rules in frame.md"
avoid: ["generic slideshow", "tiny unreadable lyrics", "text over text", "rotating gimmicks", "full-frame white flashes", "drawing your own sky or star field"]
---

# 유리병 별자리 — lyric MV storyboard

Song: Korean band, J-pop-style ballad-rock, 92 BPM, 3:10 (Suno). One night on a hill, from the first star to almost-dawn.
Section map (measured): intro band hits 1.25 / 3.75 · verse 1 vocals 11.45, band enters 22.7 · chorus "빛나라" sung in a
band STOP (42.9–43.5), band slams 43.5 · verse 2 66.7 · chorus 2 stop 87.1–87.8, slam 87.8 · wordless vocalise 113–116.5 ·
bridge piano-only 119.1–129.3 · build 129.3 · final chorus starts as a 落ちサビ (band drops 139.8), band slams back 150.9 ·
held "불러 줘~" to 169.6, last hit 169.97 · outro piano 171–180.7 · band ending 180.75, stop 186.75, final hit 188.5, end 189.2.

## Frame 1 — f1

- src: compositions/frames/01-f1.html
- duration: 11.1s
- span_sec: [0.0, 11.1]
- pacing: beat_cut
- mood: [dreamy, cinematic]
- feel: solo piano riff (0.25–1.2), one full-band hit at 1.25, piano again, band locks in at 3.75 and drives to 11.4; no vocals
- lyrics: none

### Groups

- **g1** — free_design
  - span_sec: [0.0, 11.1]
  - free_design: { dominant_system: "first star → title lit char by char → title dissolves into the sky", primitives: ["negative-space-hold", "particle-burst", "kinetic-letter-in", "staggered-exit"], density_topology: "build" }
  - anchors: [0.30, 1.25, 2.10, 3.75, 6.56, 8.36, 10.40]
  - copy: ["유리병 별자리", "Glass-Bottle Constellation"]
  - intent: >
      0–1.25 the sky layer is black. At 0.30 (first piano note) ONE sparkle star (sparkle path, ~16px) fades in at
      (1180, 380) and breathes gently on the riff. At 1.25 (band hit) that star flares: scale burst + soft radial glow ring
      expanding to ~300px and fading (no full-frame flash) — the sky layer switches on its stars at the same moment.
      2.10–3.10 the title "유리병 별자리" is set VERTICALLY (writing-mode: vertical-rl; text-orientation: upright),
      Noto Serif KR 300, 64px, letter-spacing .42em, column centered at x≈1180 starting y≈300 (just under the first star,
      as if hanging from it): each character lights like a star being switched on (blur 10→0, opacity 0→1, gold text-shadow
      peaking then settling to text-soft), 0.14s apart. 3.20 the English line "Glass-Bottle Constellation"
      (Cormorant Garamond italic 40px, glass color, tracking .06em) fades/slides 12px up, horizontal, placed to the LEFT of the
      column, baseline aligned near the column's middle (x≈700–1120, y≈560).
      3.75 (band locks in): a falling star crosses the frame top-right → bottom-left in ~0.8s (frame.md falling-star) and the
      title chars twinkle once in sequence. Whole group slowly pushes in (scale 1→1.05 over the frame).
      6.56 accent: a second, smaller falling star on another diagonal.
      8.36 → 10.40: the title dissolves: each character shrinks into a dot of light (scale .15 + strong glow) and drifts
      up-right to join the sky, staggered; the English line fades with blur. 10.4–11.1 clean sky (the sky layer is tilting
      down to reveal the hill from ~10.0) — nothing else on screen at 11.1.

## Frame 2 — f2

- src: compositions/frames/02-f2.html
- duration: 20.6s
- span_sec: [11.1, 31.7]
- pacing: phrase_flow
- mood: [dreamy, elegant]
- feel: band drops out at 11.5 — voice + soft piano; the band re-enters at 22.7 on "유리병"; calm 4-line verse
- lyrics (track s): L1 11.45 "떨어진 별을 줍는 게 내 일이야" (별을 12.87, 일이야 14.75; to 16.42) · L2 16.54 "밤마다 언덕 끝에 앉아서" (언덕 17.82, 앉아서 19.15; to 21.65) · L3 21.77 "작은 유리병 속에 하나씩" (유리병 22.47, 하나씩 24.41; to 25.90) · L4 26.02 "불빛을 모아 두곤 해" (모아 27.68, 두곤 29.00, 해 30.18; to 30.75)

### Groups

- **g1** — free_design
  - span_sec: [11.1, 31.7]
  - free_design: { dominant_system: "vertical poem columns written by falling stars (縦書き monologue)", primitives: ["kinetic-letter-in", "mask-reveal", "staggered-reveal", "blur-resolve"], density_topology: "accumulate" }
  - anchors: [11.45, 12.87, 16.54, 17.82, 21.77, 22.70, 26.02, 27.68, 29.00, 30.18]
  - copy: ["떨어진 별을 줍는 게 내 일이야", "밤마다 언덕 끝에 앉아서", "작은 유리병 속에 하나씩", "불빛을 모아 두곤 해"]
  - intent: >
      Intimate monologue, the hill is visible at the bottom (sky layer). Lyrics are VERTICAL columns read right→left, like a
      Japanese lyric sheet: Noto Serif KR 300, 52px, letter-spacing .2em, color text with text-soft glow. A line longer than
      ~11 characters wraps into TWO adjacent columns at a word boundary (the second column to the left of the first);
      keep every column ≤ 740px tall, top at y≈150. Column positions drift leftward line by line: L1 at x≈1560, L2 ≈1400,
      L3 ≈1240, L4 ≈1080 (adjust for two-column lines). When a new line starts, the previous one dims to text-dim at
      .45 opacity; a line two steps back fades out — never more than 2 lines on screen.
      Keyword rule: 별 (in 별을), 언덕, 유리병, 불빛 are 1.4× size, weight 500, gold-glow.
      L1 (11.45): a falling star drops from the top-right at ~11.0 and lands at the head of L1's column; the characters reveal
      top→bottom in the star's wake, synced to the word onsets (each word's characters appear 0.05s apart starting at the
      word time; blur 6→0, y −10→0). Every line uses this "written by light" reveal, but only L1 and L3 get a visible falling star.
      L2 (16.54): on 언덕 (17.82) a tiny warm light (6px, amber halo) appears on the hill crest at (820, 975) — the narrator
      sitting there — and stays, softly breathing, through the frame.
      L3 (21.77) + band entry 22.70: on 유리병 the GLASS BOTTLE appears: inline assets/motifs/bottle.svg at the "home"
      placement — SVG width 311px, height 420px, left 404px, top 480px (center x 560, bottom y 900). The glass outline draws
      on (stroke-dashoffset, pathLength=1000 on #fN_glass) 22.6→23.5, then shine + cork fade in. Fill stays 0.
      L4 (26.02): on 불빛을 the two characters 불 and 빛 each emit a glowing dot that arcs over (curved path, ~0.9s) and
      drops into the bottle mouth at 27.68 (모아), becoming sparkles inside #fN_stars; 2 more tiny falling stars from the
      sky drop into the bottle at 29.00 and 30.18. Bottle fill scaleY 0 → 0.12, glow opacity 0 → 0.35 by 30.5.
      30.75–31.7 hold: columns dim, bottle glowing. EXIT STATE at 31.7 (f3 continues it): bottle exactly at home placement,
      fill 0.12, glow 0.35, ~6 sparkles inside; all lyric columns faded out by 31.6; the hill light still on.

## Frame 3 — f3

- src: compositions/frames/03-f3.html
- duration: 10.7s
- span_sec: [31.7, 42.4]
- pacing: phrase_flow
- mood: [dreamy, tense]
- feel: pre-chorus, band steady and rising, two long sung lines, tension building into the chorus stop
- lyrics (track s): L5 32.20 "반짝이는 이유는 묻지 마" (이유는 34.33, 묻지 35.19, 마 36.01; to 37.31) · L6 37.43 "나도 아직 이름을 몰라" (아직 38.37, 이름을 39.54, 몰라 40.24; to 41.05)

### Groups

- **g1** — free_design
  - span_sec: [31.7, 42.4]
  - free_design: { dominant_system: "horizontal lines that twinkle on + the empty name brackets; camera pushes toward the bottle", primitives: ["neon-flicker", "staggered-reveal", "staggered-exit"], density_topology: "build" }
  - anchors: [32.20, 34.33, 35.19, 36.01, 37.43, 39.54, 40.24, 41.90]
  - copy: ["반짝이는 이유는 묻지 마", "나도 아직 이름을 몰라"]
  - intent: >
      ENTRY STATE at 31.7 = f2's exit: bottle at home placement (311×420, left 404, top 480), fill 0.12, glow 0.35, ~6
      sparkles inside, and the tiny warm hill light at (820, 975). Over the frame the bottle slowly grows/drifts toward the
      viewer (scale 1 → 1.18 about its base center, x +40) — rising tension. Sparkles inside swirl faster as the frame goes.
      Lyrics switch to HORIZONTAL (contrast with verse 1): Noto Serif KR 400, 76px, text color, right of the bottle,
      left-aligned at x≈980, L5 at y≈420, L6 at y≈560.
      L5 (32.20): 반짝이는 — each character twinkles on like a star (deterministic flicker per char: 0→1→.3→1 over ~0.4s,
      0.1s apart); the rest of the line fades in on its word times; at 묻지 마 (35.19–36.01) the letter-spacing of "묻지 마"
      settles from .3em to .02em (a hush).
      L6 (37.43): L5 dims to .45. On 이름을 (39.54) first two thin corner brackets 「 」 (SVG strokes, glass color) open
      around an EMPTY slot, then '이름' fades into the slot, 1.4× size, gold-glow — the unnamed thing. Keep the brackets
      afterwards (they come back in the final chorus).
      From 38.5 to 41.8 small foreground sparkles appear around the text one by one (6 → 18), brightness rising, bottle
      fill 0.12 → 0.22.
      41.90–42.35: staggered exit — lines lift 30px and blur out, bottle and sparkles blur/fade out, hill light fades. Stage
      is empty at 42.4 (the chorus opens from nothing).

## Frame 4 — f4

- src: compositions/frames/04-f4.html
- duration: 24.3s
- span_sec: [42.4, 66.7]
- pacing: beat_cut
- mood: [hype, warm, cinematic]
- feel: chorus — first word sung in a dead band stop (42.9–43.5), band slams at 43.5; 8 lines ~2.7s each; band stops at 63.5 and a light interlude of single hits (64.38, 65.04, 65.69, 66.01, 66.34) leads into verse 2
- lyrics (track s): L7 42.64 "빛나라 저 하늘 너머로" (저 43.66, 하늘 44.00, 너머로 44.64) · L8 45.38 "삼켜 둔 별들이 흘러가" (별들이 46.27, 흘러가 47.11) · L9 48.17 "목 끝에 걸린 작은 빛이" (걸린 49.21, 빛이 50.35) · L10 50.95 "밤새 뜨겁게 타올라" (뜨겁게 51.43, 타올라 52.29) · L11 53.23 "괜찮아 아무도 모르게" (아무도 54.18, 모르게 55.06) · L12 55.90 "오늘도 병 속에 담을게" (병 56.68, 담을게 57.52) · L13 58.64 "언젠가 넘쳐 버린다면" (넘쳐 59.64, 버린다면 60.26) · L14 62.17 "그땐 날려 보낼게" (날려 62.69, 보낼게 63.51; to 64.40)

### Groups

- **g1** — free_design
  - span_sec: [42.4, 66.7]
  - free_design: { dominant_system: "one visual idea per line, escalating: mega word from a point of light → river of stars → throat light → heat → whisper → words fall into the bottle → overflow → release", primitives: ["braam-punch", "particle-burst", "radial-burst-lines", "content-swap", "staggered-exit"], density_topology: "escalate then release" }
  - anchors: [42.64, 43.50, 45.38, 46.27, 48.17, 50.95, 52.29, 53.23, 55.90, 57.52, 58.64, 59.64, 62.17, 62.69, 63.51, 64.38, 65.04, 65.69, 66.01, 66.34]
  - copy: ["빛나라 저 하늘 너머로", "삼켜 둔 별들이 흘러가", "목 끝에 걸린 작은 빛이", "밤새 뜨겁게 타올라", "괜찮아 아무도 모르게", "오늘도 병 속에 담을게", "언젠가 넘쳐 버린다면", "그땐 날려 보낼게"]
  - intent: >
      The camera has tilted up (sky layer): no hill, chorus sky. Big type now. Each line replaces the previous one
      (content-swap on the line onset, outgoing line exits in ≤0.25s). Line text default: Noto Serif KR 600, 96px, centered,
      y≈560 unless stated; keywords (하늘, 별들이, 빛이, 병, 날려) 1.3×, gold-glow.
      L7: at 42.64 (in the band STOP) a single bright point at center grows and "빛나라" (mega 220px, weight 800) lights
      up out of it — blur 20→0, letter-spacing .5em→0 — finishing ~43.3. At 43.50 (BAND SLAM): radial light rays + ~24
      sparkles burst out from the word (particle-burst / radial-burst-lines, light colors only, no white-out), small
      camera kick (scale 1.04→1). "저 하늘 너머로" (76px) rises in below at 43.66; "빛나라" floats up slowly until 45.3.
      L8 (45.38): a RIVER OF STARS — ~60 dots/sparkles flowing right→left along a gentle sine band through y 500–640,
      and the line rides on top of it, drifting right→left 40px; 별들이 sparkles.
      L9 (48.17): river clears; ONE small light at (960, 400) pulses like a heartbeat on each beat (≈48.8, 49.4, 50.0, 50.6);
      the line sits under it at y≈600; 빛이 gold.
      L10 (50.95): that light grows and heats — starlight → gold → amber (#FFB45C), glow radius ×3; the characters warm to
      amber and shimmer upward a few px (deterministic sine jitter); 타올라 scales 1→1.15 at 52.29.
      L11 (53.23): BREATH — the light shrinks back to a point; the line is a whisper: 44px, weight 300, text-dim, lower-left
      (x≈300, y≈760). Nothing else moves.
      L12 (55.90): the bottle returns at center (inline bottle.svg, ~380px tall, centered x 960, bottom y 900; glass draws in
      fast, 0.4s), the line above it at y≈300; at 57.52 (담을게) the characters drop one by one into the bottle mouth
      (gravity, power2.in, 0.06 stagger) becoming sparkles; fill 0.2 → 0.45.
      L13 (58.64): line to the right of the bottle (x≈1220, 76px); fill rises to the brim 0.45 → 1.0 over 59.6–61.8; small
      sparkles overflow the neck and slide down the outside of the glass; 넘쳐 wobbles like liquid.
      L14 (62.17): on 날려 (62.69) twelve sparkles fly out of the bottle mouth in arcs; on 보낼게 (63.51) the line's letters
      lift off upward and fade (released). Band stops at 63.5.
      Interlude (64.40–66.70): on each light hit (64.38, 65.04, 65.69, 66.01, 66.34) one released sparkle settles into the
      sky as a new star and twinkles once. Bottle sinks 60px and fades out by 66.4. Stage empty at 66.7.

## Frame 5 — f5

- src: compositions/frames/05-f5.html
- duration: 10.2s
- span_sec: [66.7, 76.9]
- pacing: phrase_flow
- mood: [warm, playful]
- feel: verse 2 with band, four quick lines (~2.6s each), walking past someone's window
- lyrics (track s): L15 67.05 "너의 창가를 지나칠 때면" (창가를 67.39, 지나칠 68.07) · L16 69.64 "주머니 속 별이 또 뜨거워져" (별이 70.42, 뜨거워져 70.94) · L17 72.22 "손을 흔들고 돌아서는 길" (흔들고 72.70, 돌아서는 73.30, 길 74.42) · L18 74.86 "발자국마다 빛이 떨어져" (빛이 75.87, 떨어져 76.47; to 77.00)

### Groups

- **g1** — free_design
  - span_sec: [66.7, 76.9]
  - free_design: { dominant_system: "lateral walk: a house with your lit window pans past; footprints of light", primitives: ["staggered-reveal", "directional-fill", "blur-resolve"], density_topology: "travel" }
  - anchors: [67.05, 67.39, 69.64, 70.42, 70.94, 72.22, 73.30, 74.86, 75.87, 76.47]
  - copy: ["너의 창가를 지나칠 때면", "주머니 속 별이 또 뜨거워져", "손을 흔들고 돌아서는 길", "발자국마다 빛이 떨어져"]
  - intent: >
      The hill is back (sky layer, warm sky with amber glow bottom-right). A simple flat silhouette of a small house sits on
      the hill at the right (dark #070C20 shapes, roof + chimney, ~360×300px, base on y≈990), with ONE window (70×90)
      glowing amber (#FFB45C + soft halo). The house pans right→left across the frame (x 1560 → 1180 over the frame,
      linear) — we are walking past it. Lyrics HORIZONTAL, lower-left, Noto Serif KR 400, 70px, left-aligned at x≈170,
      y≈720, one line at a time (previous line slides 40px left and fades as the next arrives — walking direction).
      L15: on 창가를 (67.39) the window brightens (halo ×1.6); 창가 in amber glow.
      L16: a warm amber glow pulses up from the bottom-left corner (the pocket) on 별이 (70.42) and again on 뜨거워져
      (70.94); 별 gets the gold keyword treatment; 뜨거워져 turns amber and shimmers.
      L17: on 돌아서는 (73.30) the window light dims back to normal (turning away); the line sways gently once.
      L18: FOOTPRINTS OF LIGHT — eight small glowing dots appear one after another left→right along the hill crest
      (y≈ 975–1000, slight up/down alternation like steps, x 180 → 1100) between 74.9 and 76.8, each staying and
      twinkling; 빛이 gold. At 76.6–76.9 the line fades; footprints remain to the cut.

## Frame 6 — f6

- src: compositions/frames/06-f6.html
- duration: 9.65s
- span_sec: [76.9, 86.55]
- pacing: phrase_flow
- mood: [dreamy, tense]
- feel: pre-chorus 2, two long lines, band building; ends right before the chorus stop
- lyrics (track s): L19 77.15 "모르는 척 웃어 넘기면" (척 79.11, 웃어 79.87, 넘기면 80.29) · L20 81.67 "하늘엔 별이 또 하나 늘어" (별이 83.36, 또 84.12, 하나 84.62, 늘어 85.98; to 86.45)

### Groups

- **g1** — free_design
  - span_sec: [76.9, 86.55]
  - free_design: { dominant_system: "one new star is born with a cross flare", primitives: ["staggered-reveal", "spotlight-sweep", "blur-resolve"], density_topology: "build" }
  - anchors: [77.15, 79.11, 79.87, 81.67, 83.36, 84.62, 85.98]
  - copy: ["모르는 척 웃어 넘기면", "하늘엔 별이 또 하나 늘어"]
  - intent: >
      Hill visible, pre-chorus sky. Lyrics horizontal, centered, Noto Serif KR 400, 80px, y≈640.
      L19: "모르는 척" appears then glances away (x −14 → 0 with a 3° skew settling) — playful pretending; 웃어 in a warm
      tint; the line holds through 81.55.
      L20 (81.67) replaces it (same position). At 하나 (84.62) A NEW STAR IS BORN at (1480, 250): a big 4-point sparkle
      (scale 0 → 34) with long thin horizontal + vertical flare rays (1px lines 0→420px, fading at the tips) and a halo,
      then it settles to a bright star (scale 18) that keeps twinkling; on 늘어 (85.98) it pulses once. 별 in the line is
      1.4× gold. Small foreground sparkles increase through the frame (rising tension).
      86.25–86.50 the line blurs out quickly; the new star stays bright until the cut at 86.55.

## Frame 7 — f7

- src: compositions/frames/07-f7.html
- duration: 32.05s
- span_sec: [86.55, 118.6]
- pacing: beat_cut
- mood: [cinematic, warm, elegant]
- feel: chorus 2 — first word in a band stop (87.1–87.8), slam at 87.8; 8 lines; last line held 105.5–111.25; then 7s of band with a wordless vocalise (113–116.5) and falling snare hits (113.45, 117.03, 117.35, 117.68, 118.00, 118.33) before the piano bridge
- lyrics (track s): L21 86.92 "빛나라 저 하늘 너머로" (저 87.90, 하늘 88.24, 너머로 88.90) · L22 89.64 "숨겨 둔 별들이 흘러가" (별들이 90.53, 흘러가 91.35) · L23 92.47 "입술 끝에 머문 빛들이" (머문 93.75, 빛들이 94.43) · L24 95.19 "별자리가 되어 가" (별자리가 95.23, 되어 96.51, 가 97.03) · L25 97.48 "괜찮아 너는 몰라도 돼" (몰라도 98.98, 돼 99.80) · L26 100.16 "이 밤이 대신 기억할 테니" (기억할 101.28, 테니 102.04) · L27 102.86 "언젠가 고개 들어 본다면" (고개 103.86, 들어 104.20, 본다면 104.52) · L28 105.45 "그거면 충분해" (충분해 107.71; held to 111.25)

### Groups

- **g1** — free_design
  - span_sec: [86.55, 118.6]
  - free_design: { dominant_system: "the title constellation forms — keywords ignite star nodes and edges connect into the glass-bottle constellation; lyrics live inside it", primitives: ["outline-to-fill", "particle-burst", "staggered-reveal", "negative-space-hold"], density_topology: "accumulate → hold → disperse" }
  - anchors: [86.92, 87.80, 89.64, 90.53, 91.35, 92.47, 94.43, 95.19, 95.23, 96.51, 97.03, 97.48, 100.16, 102.86, 103.86, 105.45, 107.71, 111.25, 113.45, 117.03, 117.35, 117.68, 118.00, 118.33]
  - copy: ["빛나라 저 하늘 너머로", "숨겨 둔 별들이 흘러가", "입술 끝에 머문 빛들이", "별자리가 되어 가", "괜찮아 너는 몰라도 돼", "이 밤이 대신 기억할 테니", "언젠가 고개 들어 본다면", "그거면 충분해"]
  - intent: >
      Different devices from chorus 1. Uses frame.md `bottle-constellation` (nodes A–I, edges) at full size.
      L21: at 86.92 "빛나라" appears as an OUTLINE only (mega 220px, weight 800, transparent fill, 2px starlight
      -webkit-text-stroke, faint glow) centered; at 87.80 (BAND SLAM) it FILLS with light (outline-to-fill, gold-glow peak
      then settle) with a burst of ~20 sparkles; "저 하늘 너머로" (76px) appears below at 87.90. Both exit by 89.5
      (the mega word shrinks up into node A's position and becomes node A's star).
      From L22 on, lyric lines sit INSIDE the constellation (the words are inside the bottle): centered x 960, y≈600,
      Noto Serif KR 500, 76px (L24 '별자리가' hero 118px), one line at a time, keywords gold.
      Node ignition (sparkle pops scale 0→1 with halo, back.out): A at 89.64 (already there from 빛나라), B 90.53,
      C 91.35 · D 92.47, E 94.43 (edges A-B, A-C, B-D, C-E draw on, 0.6s each) · F 95.23, G 95.6, H 96.51, I 97.03
      with edges D-F, E-G, F-H, G-I, H-I drawing so the bottle constellation COMPLETES exactly at 97.03 (가).
      L25 whisper size (52px, text-dim) inside; L26 normal; the edges brighten .6 → .9 opacity during L26.
      L27: on 고개 들어 (103.86–104.2) the whole constellation + text group eases to scale .92, y +40 (we look up).
      L28 (105.45): "그거면 충분해" (hero 96px, weight 500) centered in the constellation belly; held note → a ≥3s
      beautiful still: nodes twinkling, very slow push (scale .92→.95), nothing else moving. 111.0–111.4 the text fades.
      AFTERGLOW 111.25–118.6 (no lyrics; vocalise 113–116.5): the constellation slowly turns (rotation 0 → −8° about its
      center) and recedes (scale → .7, edges fade). On the snare hits 113.45, 117.03, 117.35, 117.68, 118.00, 118.33 one node
      at a time DETACHES and falls as a falling star (down-left, out of frame) — the stars fall back to earth. By 118.5
      everything is gone; the sky layer has darkened to near-black for the bridge.

## Frame 8 — f8

- src: compositions/frames/08-f8.html
- duration: 10.1s
- span_sec: [118.6, 128.7]
- pacing: phrase_flow
- mood: [dark, dreamy]
- feel: bridge — piano only, soft voice, near silence at 120; two slow lines with long holds
- lyrics (track s): L29 118.77 "가득 찬 유리병을 열면" (가득 118.80, 찬 120.05, 유리병을 120.77, 열면 122.05; to 123.15) · L30 123.27 "전부 쏟아질까 무서웠어" (전부 123.31, 쏟아질까 123.87, 무서웠어 126.58; to 128.25)

### Groups

- **g1** — free_design
  - span_sec: [118.6, 128.7]
  - free_design: { dominant_system: "negative space: the full bottle alone in the dark, two whispered vertical columns framing it", primitives: ["negative-space-hold", "blur-resolve", "text-wave-distort"], density_topology: "reset → hold" }
  - anchors: [118.77, 120.05, 120.77, 122.05, 123.27, 123.87, 126.58]
  - copy: ["가득 찬 유리병을 열면", "전부 쏟아질까 무서웠어"]
  - intent: >
      INFORMATION RESET. Near-black sky. The bottle alone at center: inline bottle.svg, SVG 459×620px, left 730.5, top 250
      (center 960, 560). It fades up from darkness 118.6→119.6 already FULL: fill 0.92, glow 0.7, halo 0.35, ~30
      sparkles inside drifting slowly (deterministic orbits). A slow light sweep crosses the glass once (~121–123).
      Whole stage in a camera wrapper (#f8_cam) pushing in slowly: scale 1 → 1.06 about (960,540) over the frame.
      Lyrics are tiny vertical whispers: Noto Serif KR 250, 40px, tracking .45em, text-dim, vertical-rl upright.
      L29 column at x≈1340 (right of the bottle), top y≈260, each word fading in slowly (0.8s) on its onset.
      L30 column at x≈560 (left of the bottle), top y≈260. On 쏟아질까 (123.87) the bottle trembles (x ±2px, rotation ±0.6°,
      deterministic, ~1.2s) and the inside sparkles agitate; on 무서웠어 (126.58) the glow dims .7 → .35 like holding a
      breath, then recovers a little.
      128.2–128.7 both columns fade. EXIT STATE at 128.7: #f8_cam at scale 1.06; bottle at the placement above, fill .92,
      glow ≈.5, sparkles inside. (f9 starts from exactly this.)

## Frame 9 — f9

- src: compositions/frames/09-f9.html
- duration: 10.3s
- span_sec: [128.7, 139.0]
- pacing: beat_cut
- mood: [tense, cinematic]
- feel: build — band re-enters at 129.3 and accelerates; snare run 137.18, 137.67, 138.16, 138.48, 138.81 into the final chorus
- lyrics (track s): L31 128.84 "그래도 오늘 밤만큼은" (그래도 128.88, 오늘 131.30, 밤만큼은 131.82; to 133.61) · L32 133.73 "뚜껑을 열어 볼게" (뚜껑을 133.77, 열어 134.49, 볼게 136.53; to 138.65)

### Groups

- **g1** — free_design
  - span_sec: [128.7, 139.0]
  - free_design: { dominant_system: "light leaking around the cork, rays multiply on the beat, the cork pops", primitives: ["screen-shake", "spotlight-sweep", "flash-cut"], density_topology: "accelerate → release" }
  - anchors: [128.84, 129.30, 131.30, 131.82, 133.73, 134.49, 136.53, 137.18, 137.67, 138.16, 138.48, 138.81]
  - copy: ["그래도 오늘 밤만큼은", "뚜껑을 열어 볼게"]
  - intent: >
      ENTRY STATE at 128.7 = f8 exit (camera wrapper scale 1.06; bottle 459×620 at left 730.5 / top 250, fill .92, glow ≈.5,
      sparkles inside). 128.7–130.0 the camera eases back (1.06 → 1) and the bottle rises a little (top 250 → 200) to make
      room for the text below.
      Lyrics horizontal, centered under the bottle at y≈930, Noto Serif KR 500, 64px (keywords 오늘 밤, 뚜껑 1.3× gold).
      L31 (128.84) and L32 (133.73) replace each other.
      LIGHT LEAKS: from 129.3 thin rays (2–3px, starlight→transparent, 120–420px long) escape from around the cork; their
      number grows on the beats (2 at 129.3, 4 at 131.3, 6 at 133.7, 9 at 136.5) and they rotate slowly. The glow and halo
      rise steadily. The cork jiggles on each snare of the run (137.18, 137.67, 138.16, 138.48, 138.81) with increasing
      amplitude; tiny screen-shake on the last two.
      138.86–139.0: the cork POPS — it shoots up-right and spins out of frame (the only big rotation in the video), a burst
      of light blooms from the bottle mouth (radial gradient bloom covering ~70% of the frame, NOT a flat white frame).
      Hard cut to f10 at 139.0.

## Frame 10 — f10

- src: compositions/frames/10-f10.html
- duration: 10.55s
- span_sec: [139.0, 149.55]
- pacing: phrase_flow
- mood: [dreamy, cinematic]
- feel: final chorus as 落ちサビ — key change, the band drops away at 139.8, voice + soft keys, light percussion creeps back from 145, a swell into the band slam at 150.9
- lyrics (track s): L33 139.13 "날아가 저 하늘 너머로" (날아가 139.17, 저 139.89, 하늘 140.25, 너머로 140.92) · L34 141.68 "모아 둔 별들아 전부 다" (별들아 142.54, 전부 143.36, 다 143.84) · L35 144.44 "한 번도 꺼내지 못했던" (꺼내지 145.38, 못했던 146.44) · L36 147.20 "그 빛을 비춰 줘" (빛을 147.58, 비춰 148.24, 줘 149.20; to 149.57)

### Groups

- **g1** — free_design
  - span_sec: [139.0, 149.55]
  - free_design: { dominant_system: "weightless release — a slow fountain of stars rising out of the open bottle into the dawn-edged sky", primitives: ["kinetic-letter-in", "particle-burst", "spotlight-sweep"], density_topology: "release → swell" }
  - anchors: [139.13, 139.17, 139.80, 140.25, 141.68, 142.54, 144.44, 147.20, 148.24, 149.20]
  - copy: ["날아가 저 하늘 너머로", "모아 둔 별들아 전부 다", "한 번도 꺼내지 못했던", "그 빛을 비춰 줘"]
  - intent: >
      Not an explosion — the opposite: everything floats. The camera looks up (sky layer: dawn rose/peach horizon,
      milky band). The OPEN bottle (no cork) is at the bottom center, cropped by the frame edge: inline bottle.svg at
      SVG 518×700px, left 701, top 760 (only the neck and shoulders visible), fill .7, glow .8, halo .5. From its mouth a
      steady FOUNTAIN of ~90 sparkles rises: each with its own deterministic curved path (sine sway), start time staggered
      across the whole frame, size 6–16px, fading and shrinking near the top — stars going home. Density thickens after 145.
      Lyrics horizontal, upper middle (y≈330–520), centered:
      L33: "날아가" mega (200px, weight 800) — each character rises individually from below (y +80 → 0, opacity 0→1,
      0.18s stagger) and keeps floating up slowly while visible; "저 하늘 너머로" 72px below it on its word times.
      L34: hero 104px, 별들아 gold. L35: 76px, weight 400, gentle. L36: 96px; on 비춰 (148.24) a vertical beam of light
      sweeps up from the bottle mouth through the text (spotlight-sweep, soft, additive look).
      149.2–149.55: inhale — the whole stage eases to scale .97 and the fountain thins, ready for the slam in f11.

## Frame 11 — f11

- src: compositions/frames/11-f11.html
- duration: 20.5s
- span_sec: [149.55, 170.05]
- pacing: beat_cut
- mood: [hype, warm, cinematic]
- feel: full band slams back at 150.9; climax lines; "네가 불러 줘" held 158.6 → 169.6 over driving band (downbeats 158.99, 161.56, 164.17, 166.77, 169.37), last hit 169.97
- lyrics (track s): L37 149.69 "보이니 네 머리 위에서" (보이니 149.69, 네 150.49, 머리 150.81, 위에서 151.47) · L38 152.29 "가장 밝게 빛나는 그 별" (밝게 152.63, 빛나는 153.11, 그 153.93, 별 154.21) · L39 155.13 "이름은 붙이지 않을게" (붙이지 156.04, 않을게 157.14) · L40 158.62 "네가 불러 줘" (네가 158.62, 불러 159.24, 줘 165.11; held to 169.60)

### Groups

- **g1** — free_design
  - span_sec: [149.55, 170.05]
  - free_design: { dominant_system: "the brightest star overhead and its EMPTY name — the emotional peak, then a long held still", primitives: ["braam-punch", "particle-burst", "negative-space-hold", "freeze-hold"], density_topology: "explode → focus → hold" }
  - anchors: [149.69, 150.49, 150.90, 152.29, 153.11, 154.21, 155.13, 157.14, 158.62, 159.24, 158.99, 161.56, 164.17, 165.11, 166.77, 169.37, 169.97]
  - copy: ["보이니 네 머리 위에서", "가장 밝게 빛나는 그 별", "이름은 붙이지 않을게", "네가 불러 줘"]
  - intent: >
      L37 (149.69): "보이니 네 머리 위에서" 88px centered y≈640. At 150.90 (BAND SLAM) ~140 sparkles burst from the center
      and fly outward, settling across the whole frame as new stars that keep twinkling (the sky is now full); camera kick
      (scale 1.05 → 1); text holds.
      L38 (152.29): THE BRIGHTEST STAR rises into place at (960, 300): a large sparkle (scale grows to 40 on 빛나는 153.11,
      peak 52 on 별 154.21) with long thin cross flares (horizontal 900px, vertical 500px, 1–2px, fading tips), a gold halo,
      slow rotation of the flares ≤ 4°. Line below at y≈700, hero 104px; 별 1.5× gold.
      L39 (155.13): from the star a fine leader line (1.5px glass color) draws to the right and ends in the EMPTY name
      brackets 「　」 (the same corner brackets as f3) — nothing written inside. Line text below as before.
      L40 (158.62): "네가 불러 줘" hero 132px, weight 700, centered y≈720; 불러 (159.24) brightens; during the long hold
      the star pulses on each downbeat (158.99, 161.56, 164.17, 166.77, 169.37), the empty brackets glow softly, the
      settled sky sparkles twinkle, and a slow push-in runs (scale 1 → 1.08). On 줘 (165.11) the line turns gold-glow.
      This is the ≥1.5s still of the video — keep motion subtle, no new elements after 160.
      169.97 (last hit): a soft bloom from the star; 170.0–170.05 hold for the cut (text still visible is fine).

## Frame 12 — f12

- src: compositions/frames/12-f12.html
- duration: 10.55s
- span_sec: [170.05, 180.6]
- pacing: phrase_flow
- mood: [warm, dreamy]
- feel: outro — band rings out, then solo piano; two quiet lines; pre-dawn; 2s of piano alone at the end
- lyrics (track s): L41 170.22 "떨어진 별을 줍는 밤" (별을 171.74, 줍는 172.52, 밤 173.22; to 175.22) · L42 175.34 "오늘은 조금 가벼워" (조금 176.59, 가벼워 177.29; to 178.85)

### Groups

- **g1** — free_design
  - span_sec: [170.05, 180.6]
  - free_design: { dominant_system: "vertical callback to verse 1; the now-empty bottle on the hill grows light and lifts", primitives: ["kinetic-letter-in", "negative-space-hold", "blur-resolve"], density_topology: "settle → hold" }
  - anchors: [170.22, 171.74, 173.22, 175.34, 176.59, 177.29, 178.85]
  - copy: ["떨어진 별을 줍는 밤", "오늘은 조금 가벼워"]
  - intent: >
      Pre-dawn sky, the hill returns (sky layer tilts down 170–174). The bottle sits on the hill crest at the left — EMPTY:
      inline bottle.svg 222×300px, left 409, top 690 (center x 520, bottom 990), fill 0, glow 0, open (cork hidden), ONE tiny
      sparkle inside. It fades in 170.1–171.0.
      Lyrics VERTICAL again (callback to f2): Noto Serif KR 300, 52px, letter-spacing .2em, text with text-soft glow; same
      top→bottom "written by light" character reveal on word onsets, but calm — NO falling star.
      L41 column at x≈1500 (top y≈200), 별 1.4× gold. L42 (175.34) column at x≈1360; L41 dims to .45.
      On 가벼워 (177.29) the bottle lifts off the hill (y −70 over 2.2s, sine.out), tilts 4°, and the three characters of
      가벼워 drift up 12px — lighter.
      178.85–180.2 a still (piano alone): columns + floating bottle, only breathing motion. 180.2–180.6 columns fade out;
      the bottle stays to the cut.

## Frame 13 — f13

- src: compositions/frames/13-f13.html
- duration: 9.36s
- span_sec: [180.6, 189.96]
- pacing: beat_cut
- mood: [cinematic, warm]
- feel: band ending — full band slam at 180.75 for 6s, dead stop 186.75–188.4, final hit 188.5, music ends 189.2, silence after
- lyrics: none

### Groups

- **g1** — free_design
  - span_sec: [180.6, 189.96]
  - free_design: { dominant_system: "title reprise: the bottle constellation ignites with the band, title card, freeze on the stop, last hit, black", primitives: ["system-replace", "staggered-reveal", "freeze-hold", "flash-cut"], density_topology: "ignite → hold → end" }
  - anchors: [180.75, 182.60, 185.25, 186.75, 188.50, 189.20]
  - copy: ["유리병 별자리", "Glass-Bottle Constellation"]
  - intent: >
      180.60–180.75: the f12 bottle (same placement: 222×300 at left 409, top 620 i.e. lifted) is visible; at 180.75 (BAND
      SLAM) it bursts into light and disappears while the BOTTLE CONSTELLATION (frame.md coordinates, the whole group
      scaled .62 about (960,540) then translated to center x≈1390) ignites all at once: nodes pop (stagger .03), edges draw
      fast (180.8–181.5), a ring of sparkles bursts out.
      Title card on the left: "유리병 별자리" horizontal, Noto Serif KR 700, 118px, x≈180, y≈470, characters lighting in
      0.06s apart from 180.85; "Glass-Bottle Constellation" (Cormorant italic 44px, glass color) under it at 181.4.
      182.60 and 185.25 (downbeats): the constellation twinkles in sequence A→I.
      186.75 (band STOP): freeze — everything holds perfectly still (freeze-hold), the title dims slightly (.85).
      188.50 (FINAL HIT): a soft bloom from node A, the title returns to full glow. 189.10–189.60 everything fades out
      (the sky layer fades to black from 189.2). Black from 189.6 to the end.
