# 유리병 별자리 v3 — lyric layers over footage (no graphic illustrations)

User (2026-10-03): "모든 곳에 영상 조각 써. SVG로 병 만든거 쓰지마 너무 짜침" — use the footage clips everywhere; never the drawn bottle.

v3 layers: `compositions/footage.html` (track 1, z 100, generated from `.work/edl.json`, every second that is not an insert),
the 4 v2 inserts (track 2, z 600 — they carry their own footage + lyrics), then **one transparent lyric layer per remaining
section** (track 3, z 700, `compositions/lyrics/<id>.html`), then grain/vignette (z 1050). Lyric timing truth = `lyrics.json`.

## Hard rules for every lyric layer
- **Typography + light only.** Allowed: lyric text (frame.md tokens, Noto Serif KR), soft dark scrims for legibility, and LIGHT
  accents tied to real light in the footage — glows, small sparkle points, soft lens flares, thin light rays, warm blooms,
  drifting light motes. **Forbidden: any drawn object or illustration** — no SVG bottle/jar/cork, no hill, house, window, sky
  gradients, star fields, constellation diagrams, empty-bottle graphics. (Exception: thin corner brackets 「 」 as typography,
  and in chorus 2 an optional very faint line linking the REAL stars already visible in shot s06e.)
- Accents must sit on the footage's real light sources (measure them on the reference stills). Keep them restrained.
- `#stage` transparent. Text readable over footage: dark scrim + dark text-shadow + frame.md glow; keep text off faces and off
  the jar/star when possible (check the stills). Safe area x 140–1780, y 110–960.
- A line is fully legible at its `onset` and stays until `vocal_end`; never two lines on top of each other.

## Sections (track spans; local_t = track_t − start)
| id | span | lyrics (see lyrics.json) | intent |
|---|---|---|---|
| s01-intro | 0.00 → 11.10 | — (title only) | Title "유리병 별자리" (vertical, frame.md, like v1 f1) + "Glass-Bottle Constellation" (Cormorant italic). Light-up per character from the band lock-in 3.75; at 1.25 (band hit) a soft bloom on the window star of s01a; title dissolves into light points 8.4–10.4 over s01d; clean by 10.9. |
| s03-pre1 | 31.70 → 42.40 | L5 32.20 · L6 37.43 | Horizontal lines. 반짝이는 chars twinkle on; "묻지 마" hush (tracking closes); on 이름을 thin 「 」 brackets open around an empty slot, then 이름 fades in gold. Small sparkle points multiply toward the end (rising tension); everything gone by 42.35. |
| s04-chorus1 | 42.40 → 66.70 | L7–L14 | Big type. L7 "빛나라" mega emerging from the defocused bokeh of s04a in the band stop, then at 43.50 (SLAM) a burst of light from the landing star in s04b (mirrored: star ≈ (858, 890)); "저 하늘 너머로" below. L8 rides over the glowing steps (s04c); L9 near the jar glow at her chest; L10 warms to amber with heat shimmer; L11 tiny whisper; L12 on 담을게 the letters fall toward the jar on the wall (s04g jar ≈ (1360, 800)) and vanish into its glow; L13 넘쳐 wobbles over the packed jar; L14 on 날려 letters lift off toward the shooting star of s04i. Interlude 64.40–66.70: one light point pops on each hit (64.38, 65.04, 65.69, 66.01, 66.34) on real stars in s04j. |
| s06-chorus2 | 86.55 → 118.60 | L21–L28 | Different devices from chorus 1. L21 "빛나라" outline → fill at the 87.80 SLAM; L22 over the footprints; L23 near the jar by her chin; L24 "별자리가 되어 가" over the real constellation of s06e (optionally a very faint line linking those real stars); L25 whisper; L26; L27 "언젠가 고개 들어 본다면" over the window shot looking up; L28 "그거면 충분해" a calm ≥3 s still over her smile (s06i). Afterglow 111.25 → 118.60 (no lyrics, vocalise): only a few slow light motes, fade to nothing. |
| s07-bridge | 118.60 → 128.70 | L29 · L30 | Information reset. Tiny vertical whispers (frame.md whisper, vertical-rl) framing the jar; on 쏟아질까 the text trembles; on 무서웠어 the jar's glow (footage) is answered by a dimming of the text glow. Long holds. |
| s08-build | 128.70 → 139.00 | L31 · L32 | Text lower-centre. Light leaking from the jar LID in s08c (lid ≈ (900, 640)): thin rays multiplying on the beats; the snare run 137.18–138.81 is a rapid montage — keep text steady; at 138.86 a warm light bloom (radial, NOT a flat white frame) from the jar in s08h, gone by 139.00. |
| s09-finalA | 139.00 → 144.30 | L33 · L34 | 落ちサビ, weightless. "날아가" mega, characters rising and floating up; light motes drifting up from her empty jar into the sky (s09a). Everything gone by 144.25 (the next insert begins). |
| s11-finalB | 155.00 → 170.05 | L39 · L40 | L39 "이름은 붙이지 않을게" beside the flaring window star of s11a (star ≈ (922, 122)) — a thin leader line from the star to EMPTY 「 」 brackets; L40 "네가 불러 줘" held to 169.60 over s11b and s11c — pulse its glow on downbeats 158.99, 161.56, 164.17, 166.77, 169.37; s11c's shooting star lands at ≈169.83 (star ≈ (1062, 890)) → a soft bloom there on the last hit 169.97. |
| s13-ending | 180.75 → 189.96 | — (title) | Band ending. Title "유리병 별자리" horizontal (Noto Serif KR 700, 118px) + "Glass-Bottle Constellation", lighting char by char from 180.85 over the montage; 186.75 STOP = freeze (everything still, title dims .85); 188.50 final hit = title glows full + small bloom at the landing star of s13e; fade out 189.10 → 189.60. |

#### shots — intro
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s01a | 0.00 → 1.25 | c09-room-window | 6.1 | 1.0 | 1.9→2.0 about (920,150) |  | .work/ref/frame-00-at-0.62s.png |
| s01b | 1.25 → 3.75 | c06-window-pass | 4.4 | 1.0 | 1.0→1.04 about (960,540) |  | .work/ref/frame-01-at-2.5s.png |
| s01c | 3.75 → 6.56 | c04-stone-steps | 0.0 | 0.7 | 1.0→1.05 about (1040,600) |  | .work/ref/frame-02-at-5.15s.png |
| s01d | 6.56 → 11.10 | c07-hug-jar | 4.5 | 1.0 | 1.0→1.08 about (960,400) |  | .work/ref/frame-03-at-8.83s.png |

#### shots — pre1
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s03a | 31.70 → 35.30 | c03-wall-sit | 1.2 | 0.8 | 1.7→1.8 about (980,460) |  | .work/ref/frame-04-at-33.5s.png |
| s03b | 35.30 → 37.43 | c05-wave-walk | 3.7 | 1.1 | 1.0→1.06 about (820,820) |  | .work/ref/frame-05-at-36.36s.png |
| s03c | 37.43 → 40.10 | c09-room-window | 5.6 | 0.78 | 1.2→1.25 about (920,300) |  | .work/ref/frame-06-at-38.77s.png |
| s03d | 40.10 → 42.40 | c06-window-pass | 6.5 | 0.67 | 1.0→1.3 about (1240,160) |  | .work/ref/frame-07-at-41.25s.png |

#### shots — chorus1
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s04a | 42.40 → 43.50 | c02-jar-closeup | 6.0 | 1.0 | 1.2→1.25 about (940,800) |  | .work/ref/frame-08-at-42.95s.png |
| s04b | 43.50 → 45.38 | c01-falling-star | 2.55 | 1.0 | 1.15→1.2 about (1062,890) | yes | .work/ref/frame-09-at-44.44s.png |
| s04c | 45.38 → 48.17 | c04-stone-steps | 0.0 | 0.72 | 1.35→1.45 about (1040,600) | yes | .work/ref/frame-10-at-46.78s.png |
| s04d | 48.17 → 50.95 | c07-hug-jar | 3.05 | 1.0 | 1.35→1.42 about (940,480) |  | .work/ref/frame-11-at-49.56s.png |
| s04e | 50.95 → 53.23 | c07-hug-jar | 5.83 | 1.0 | 1.65→1.72 about (900,470) |  | .work/ref/frame-12-at-52.09s.png |
| s04f | 53.23 → 55.90 | c06-window-pass | 0.0 | 0.52 | 1.1→1.14 about (960,600) |  | .work/ref/frame-13-at-54.56s.png |
| s04g | 55.90 → 58.64 | c03-wall-sit | 7.9 | 1.0 | 1.55→1.6 about (1360,800) |  | .work/ref/frame-14-at-57.27s.png |
| s04h | 58.64 → 62.17 | c02-jar-closeup | 0.0 | 0.75 | 1.7→1.8 about (960,660) |  | .work/ref/frame-15-at-60.41s.png |
| s04i | 62.17 → 64.40 | c01-falling-star | 0.26 | 1.0 | 1.5→1.55 about (560,280) |  | .work/ref/frame-16-at-63.29s.png |
| s04j | 64.40 → 66.70 | c09-room-window | 0.0 | 0.4 | 1.3→1.36 about (900,160) |  | .work/ref/frame-17-at-65.55s.png |

#### shots — chorus2
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s06a | 86.55 → 87.80 | c04-stone-steps | 7.25 | 0.63 | 1.1→1.13 about (920,600) |  | .work/ref/frame-18-at-87.17s.png |
| s06b | 87.80 → 89.64 | c06-window-pass | 4.3 | 1.0 | 1.45→1.5 about (1240,160) |  | .work/ref/frame-19-at-88.72s.png |
| s06c | 89.64 → 92.47 | c05-wave-walk | 3.7 | 0.82 | 1.3→1.35 about (820,820) | yes | .work/ref/frame-20-at-91.06s.png |
| s06d | 92.47 → 95.19 | c02-jar-closeup | 2.65 | 1.0 | 1.5→1.55 about (900,700) |  | .work/ref/frame-21-at-93.83s.png |
| s06e | 95.19 → 97.48 | c04-stone-steps | 4.95 | 1.0 | 1.25→1.3 about (300,240) |  | .work/ref/frame-22-at-96.34s.png |
| s06f | 97.48 → 100.16 | c03-wall-sit | 3.3 | 1.0 | 1.0→1.04 about (960,540) |  | .work/ref/frame-23-at-98.82s.png |
| s06g | 100.16 → 102.86 | c01-falling-star | 4.43 | 0.59 | 1.0→1.04 about (1400,600) |  | .work/ref/frame-24-at-101.51s.png |
| s06h | 102.86 → 105.45 | c09-room-window | 5.7 | 0.9 | 1.0→1.05 about (920,200) |  | .work/ref/frame-25-at-104.16s.png |
| s06i | 105.45 → 111.25 | c08-empty-jar-walk | 7.9 | 0.517 | 1.3→1.4 about (760,400) |  | .work/ref/frame-00-at-108.35s.png |
| s06j | 111.25 → 114.65 | c06-window-pass | 0.21 | 0.35 | 1.0→1.06 about (960,500) |  | .work/ref/frame-27-at-112.95s.png |
| s06k | 114.65 → 118.60 | c02-jar-closeup | 8.0 | 0.58 | 1.25→1.32 about (1100,450) |  | .work/ref/frame-28-at-116.62s.png |

#### shots — bridge
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s07a | 118.60 → 123.20 | c02-jar-closeup | 0.0 | 0.5 | 2.2→2.35 about (960,680) |  | .work/ref/frame-29-at-120.9s.png |
| s07b | 123.20 → 128.70 | c07-hug-jar | 0.5 | 0.5 | 1.25→1.32 about (900,480) |  | .work/ref/frame-30-at-125.95s.png |

#### shots — build
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s08a | 128.70 → 131.30 | c03-wall-sit | 0.0 | 1.0 | 1.1→1.15 about (980,460) |  | .work/ref/frame-31-at-130s.png |
| s08b | 131.30 → 133.73 | c05-wave-walk | 1.5 | 1.0 | 1.0→1.05 about (900,500) |  | .work/ref/frame-32-at-132.51s.png |
| s08c | 133.73 → 136.53 | c02-jar-closeup | 4.0 | 1.0 | 1.7→1.85 about (900,640) |  | .work/ref/frame-33-at-135.13s.png |
| s08d | 136.53 → 137.18 | c07-hug-jar | 8.3 | 1.0 | 1.4→1.42 about (840,460) |  | .work/ref/frame-34-at-136.86s.png |
| s08e | 137.18 → 137.67 | c01-falling-star | 0.0 | 1.0 | 1.5→1.52 about (560,260) |  | .work/ref/frame-35-at-137.43s.png |
| s08f | 137.67 → 138.16 | c06-window-pass | 2.5 | 1.0 | 1.3→1.32 about (1360,540) |  | .work/ref/frame-36-at-137.91s.png |
| s08g | 138.16 → 138.48 | c01-falling-star | 2.55 | 1.0 | 1.2→1.22 about (1062,890) |  | .work/ref/frame-37-at-138.32s.png |
| s08h | 138.48 → 139.00 | c02-jar-closeup | 1.0 | 1.0 | 2.3→2.45 about (960,640) |  | .work/ref/frame-38-at-138.74s.png |

#### shots — finalA
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s09a | 139.00 → 144.60 | c10-reach-sky | 0.0 | 0.62 | 1.0→1.06 about (960,400) |  | .work/ref/frame-39-at-141.8s.png |

#### shots — finalB
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s11a | 155.00 → 158.62 | c09-room-window | 3.4 | 0.5 | 1.5→1.6 about (922,122) |  | .work/ref/frame-40-at-156.81s.png |
| s11b | 158.62 → 164.17 | c06-window-pass | 4.3 | 0.674 | 1.0→1.15 about (1240,200) |  | .work/ref/frame-41-at-161.39s.png |
| s11c | 164.17 → 170.05 | c01-falling-star | 0.1 | 0.452 | 1.0→1.05 about (1062,890) |  | .work/ref/frame-42-at-167.11s.png |

#### shots — ending
| shot | track span | clip | media-start | rate | scale (about origin) | mirror | ref still (rendered, mid-shot) |
|---|---|---|---|---|---|---|---|
| s13a | 180.75 → 182.65 | c04-stone-steps | 0.0 | 1.0 | 1.0→1.05 about (1040,600) |  | .work/ref/frame-43-at-181.7s.png |
| s13b | 182.65 → 185.25 | c05-wave-walk | 3.7 | 0.9 | 1.15→1.2 about (820,820) |  | .work/ref/frame-01-at-183.95s.png |
| s13c | 185.25 → 186.75 | c10-reach-sky | 0.0 | 1.0 | 1.0→1.03 about (960,400) |  | .work/ref/frame-45-at-186s.png |
| s13d | 186.75 → 188.50 | c10-reach-sky | 1.5 | 0.05 | 1.03→1.03 about (960,400) |  | .work/ref/frame-46-at-187.62s.png |
| s13e | 188.50 → 189.96 | c01-falling-star | 2.62 | 1.0 | 1.0→1.03 about (1062,890) |  | .work/ref/frame-47-at-189.23s.png |
