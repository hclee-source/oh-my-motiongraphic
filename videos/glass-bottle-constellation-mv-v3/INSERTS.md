# 유리병 별자리 v2 — footage inserts

v2 mixes the user's 10 footage clips (felt-doll girl in a Korean hillside neighbourhood at night, a glass jar of stars;
silent, 1920×1080 24fps upscales in `assets/footage/`) into the v1 lyric MV.

**Rule of the mix: the real night = footage, the inner world = graphics.** Verses, pre-chorus 2, the middle of the final
chorus and the outro are footage with kinetic lyrics on top; choruses, bridge, build, intro and ending stay the v1 motion
graphics (`compositions/frames/*`, unchanged). Each footage stretch is ONE insert sub-composition mounted on track 2 with
`z-index: 600` ABOVE the v1 frames (the v1 frame under it keeps running but is fully covered by opaque video).
`compositions/overlay.html` (grain + vignette, z 1050) stays on top of everything, so footage and graphics share one film texture.

Lyric timing truth = `lyrics.json` (track seconds). local_t = track_t − insert start.

| insert | file / composition id | track span | covers v1 |
|---|---|---|---|
| A | `compositions/inserts/ia-verse1.html` · `ia-verse1` | 11.10 → 31.70 (20.60) | f2 entirely |
| B | `compositions/inserts/ib-verse2.html` · `ib-verse2` | 66.70 → 86.55 (19.85) | f5 + f6 entirely |
| C | `compositions/inserts/ic-final.html` · `ic-final` | 144.30 → 155.00 (10.70) | f10 tail + f11 head |
| D | `compositions/inserts/id-outro.html` · `id-outro` | 170.05 → 180.75 (10.70) | f12 + first 0.15 s of f13 |

## Insert A — ia-verse1 (verse 1, calm, voice + piano; band enters at 22.70)
Clips (local seconds; `data-media-start` = offset into the source):
| clip | local span | media-start | what happens (source time) |
|---|---|---|---|
| `c01-falling-star.mp4` | 0.00 → 5.40 | 0.60 | wide: girl from behind on the hilltop, a shooting star streaks down and LANDS as a glowing star on the grass at source 3.0 (= local 2.40 = track 13.50); she turns her head ~source 4.5–5.5 |
| `c03-wall-sit.mp4` | 5.40 → 14.90 | 0.30 | she sits on a stone wall at the edge of the hill holding a small star; from ~source 5.5 she reaches to the jar beside her and puts the star in (camera slowly orbits) |
| `c02-jar-closeup.mp4` | 14.90 → 20.60 | 0.00 | close-up: her hands holding the glass jar full of glowing stars, camera pulls back |
Cuts: 0.5 s cross-dissolves centred on 5.40 and 14.90 (phrase_flow — no hard cuts). Slow push on each clip (scale 1 → 1.05).
Lyrics: L1 11.45 · L2 16.54 · L3 21.77 · L4 26.02 (to 30.75) — VERTICAL columns exactly like v1 verse 1 (frame.md `vertical`,
52px, weight 300, tracking .2em, keyword 별/언덕/유리병/불빛 1.4× gold). Place each column in the emptiest dark area of the
clip at that moment (sky / dark rooftops), never over her face, the jar or the landing star; give the column a soft dark scrim.
Accents (graphics on footage): at local 2.40 a small sparkle burst + soft ring exactly where the footage star lands; when she
drops the star in the jar (~band entry 22.70) a soft glow pulse at the jar; during c02 10–14 tiny gold motes drift up around the jar.
**Exit = match cut:** at the end of c02 the jar sits lower-left (≈x 630, y 810). In the last ~1.2 s ease the footage framing so
the jar lands near x≈560, y≈700 (where v1 f3's graphic glass bottle sits), then fade the footage to opacity 0 over the last 0.3 s
so the real jar dissolves into the graphic bottle underneath. Lyric columns gone by local 20.5.

## Insert B — ib-verse2 (verse 2 with band → pre-chorus 2)
| clip | local span | media-start | what happens |
|---|---|---|---|
| `c06-window-pass.mp4` | 0.00 → 2.90 | 1.40 | from behind, she walks past a house whose warm window shows a silhouette inside; dotted constellation in the sky |
| `c07-hug-jar.mp4` | 2.90 → 5.45 | 0.50 | on a grassy slope she hugs the glowing jar to her chest, looking down at the city |
| `c05-wave-walk.mp4` | 5.45 → 10.20 | 0.00 | she waves by a lit window (source 0–1.5), turns and walks away down a wet alley; from source ≈4.0 (= track 76.15) each footstep leaves a glowing star |
| `c02-jar-closeup.mp4` | 10.20 → 14.90 | 5.60 | wider shot of her holding the jar, she smiles with closed eyes |
| `c09-room-window.mp4` | 14.90 → 19.85 | 1.23 | from behind, in her room, she pulls the curtain and looks at the night sky; ONE star flares brightly at source 4.25 (= track 84.62, the word 하나) |
Cuts: hard cuts at 2.90 / 5.45 / 10.20 (band, on the line onsets); 0.3 s dissolve at 14.90 (pre-chorus is calmer).
Lyrics: L15 67.05 · L16 69.64 · L17 72.22 · L18 74.86 · L19 77.15 · L20 81.67 (to 86.45) — HORIZONTAL, lower third
(v1 verse-2 style: Noto Serif KR 400, 68–72px, one line at a time, bottom scrim). Keywords: 창가 amber, 별 gold, 빛 gold.
Accents: on 별이 70.42 / 뜨거워져 70.94 a warm amber glow pulse over the jar in c07; small twinkles on the footprint stars
in c05 after track 76.15; on 하나 84.62 a graphic 4-point flare (sparkle path + long thin cross rays + halo, like v1 f6)
placed EXACTLY over the footage star, settling and pulsing once on 늘어 85.98. Exit hard cut at 19.85 (track 86.55).

## Insert C — ic-final (final chorus middle: 落ちサビ swell → band slam 150.90)
| clip | local span | media-start | what happens |
|---|---|---|---|
| `c04-stone-steps.mp4` | 0.00 → 5.25 | 2.00 | low angle on stone steps scattered with glowing stars, camera tilts up to her standing on the steps holding the glowing jar; a constellation appears in the sky |
| `c10-reach-sky.mp4` | 5.25 → 10.70 | 3.50 | on the hill she holds the EMPTY open jar and reaches her hand to the sky; camera pushes in to her face looking up at one bright star |
Entry: footage fades in over the first 0.3 s (dissolve from f10's fountain underneath). Cut at 5.25 (track 149.55) is hard.
Lyrics: L35 144.44 · L36 147.20 · L37 149.69 · L38 152.29 (to 155.01) — horizontal centred, lower area (y≈780–900) with scrim,
hero size 88–96px; 빛 / 별 gold (별 in L38 1.5×).
Accents: on 비춰 148.24 a soft vertical light beam rises from the jar through the line. **150.90 BAND SLAM**: graphic burst of
60–90 sparkles flying outward over the footage + a small camera kick on the footage wrapper (1.04 → 1). L38: a graphic
brightest-star flare (big sparkle + long thin cross flares + gold halo, like v1 f11) grows over the footage's bright star
(빛나는 153.11) and peaks on 별 154.21.
**Exit = match cut into v1 f11:** by local 10.70 the overlay flare must sit at (960, 300) at about f11's size (sparkle scale ≈52,
horizontal flare ≈900px, vertical ≈500px) — f11 shows its star there with the empty name brackets starting at 155.13. Fade the
footage + lyric to 0 over the last 0.3 s; keep the flare to the end.

## Insert D — id-outro (outro, solo piano; band slams back at 180.75)
| clip | local span | media-start | what happens |
|---|---|---|---|
| `c08-empty-jar-walk.mp4` | 0.00 → 10.70 | 0.60 | she walks along the hill path with the now EMPTY jar, a fallen star glows on the ground nearby; she smiles with eyes closed |
Hard cut in at 0.00 (right after the last hit 169.97). Slow push 1 → 1.06.
Lyrics: L41 170.22 · L42 175.34 (to 178.85) — VERTICAL columns, callback to insert A (same style), in the dark sky/city area
away from her, with scrim. 별 1.4× gold.
Accent: on 가벼워 177.29 a few tiny light motes rise from the empty jar (lighter). 178.85–180.5 a still (piano alone),
columns fade out by 180.6. Exit hard cut at 10.70 (track 180.75) into f13's band-slam constellation + title.
