# Scene pattern library

`new_variant.py` writes one `pattern_hint` per frame, chosen with the variant's seed from the pool
that fits the frame's role, book count and music. Planning (SKILL.md step 5) turns each hint into
concrete `### Groups` in STORYBOARD.md. A hint is a recommendation: override it if the music says
otherwise, but say why in the frame's `feel`.

Reference implementations live in `examples/` (`bold-beat-45s/frames/0N-fN.html` = BB-N,
`editorial-gold-46s/frames/0N-fN.html` = EG-N). Point frame workers at the matching file as
**Materials** next to the music-to-video primitives.

| id | role | music fit | books | what happens | reference |
|---|---|---|---|---|---|
| **HOOK-SLAM** | intro | sparse breakdown with real kick pairs | 0 | One hook word per measured kick; the ground flips at 0ms on each kick; pair chips under the words. Ends with a MEGA word cropped off the frame. | BB-1 g1 |
| **HOOK-TYPE** | intro | calm, few onsets | 0 | Lines stack on a hairline and letter-in on energy hits. A question lands with a gold/accent ring. Eased, phrase paced. | EG-1 g1 |
| **HOOK-MARQUEE** | intro | build / roll into the surge | 0 | One hero word, then 3–4 marquee rows of the hook phrase (outline/filled, opposite directions) that accelerate into the surge. | BB-1 7.06s |
| **LOGO-IRIS** | intro tail | surge downbeat + silence | 0 | System-replace to ink. The logo mark punches in through an iris ring, followed by the wordmark (mixed face), the 골든래빗 chip and the tagline. Hold still through the silence. | BB-1 g2, EG-1 g2 |
| **SERIES-TOSS** | series | dense kick/snare, 4–7s | 2–4 | Series title in two slams (label box on the key word + pair chip). Covers are tossed in one per strong hit and arc out, with a register flip on each, over an outline marquee of the series name. | BB-2 |
| **CARD-FLYBY** | series | accelerating roll (accel-roll) | 3–5 | Template `card-flyby`: a depth deck lands one card per kick with shrinking dwell. Card 1 is a type card, the rest are book cards. A counter 01→N ticks. | BB-3, EG-3 |
| **MEGA-SPLIT** | series | statement then 2 hits, 4–5s | 2 | MEGA series word whips in cropped, then a register flip; the title rotates to a vertical rail; two covers face off around a big ✕ or VS disc; screen shake on the last kick. | BB-4 |
| **COUNT-IN** | series | steady kicks | 3–5 | Giant outline numerals 01→N punch in, one per kick. Covers fan into a stack, the ground flips each number, and the caption swaps at 0ms. | BB-5 g1 |
| **SHELF** | series | fill into a drop | 3 | Editorial paper register with a vertical cropped word. One verb per kick, each bringing a cover into a collage. Everything clears on parabolic arcs before the silence. | BB-6, EG-6 |
| **GRID-SWAP** | series | very dense, many books | 4–6 | 2×2 or 3×2 cover grid where cells swap or recolor per onset (color-grid-shuffle), then one cover zooms forward with its caption. | primitives: color-grid-shuffle, mosaic-pack |
| **CLIMAX-SLAM** | add-on | strongest SURGE + hard stop | – | Marquee rows build during the roll. On the surge, a 0ms flip and a statement slam with weight contrast (400 + 800), burst lines and confetti. A second hit adds a label box and a shake; freeze on the hard stop. | BB-5 g2 |
| **FINALE-BURST** | finale | silence + 2–3 final hits | all | A question types in during the silence. On the hit, all covers burst into a grid with confetti; the grid parts; the logo lockup resolves; on the last hit the URL label box and an icon burst. | BB-7, EG-7 |
| **FINALE-STACK** | finale | silence + final hits | all | Same beats as FINALE-BURST, but covers drop as one tall staggered stack (deck) that fans open behind the logo. Calmer; good for 9:16. | variation of BB-7 |

## Soft-studio patterns (STYLE_PATTERNS["soft-studio"]); reference build `videos/baro-series-169-softstudio-1`
| id | role | music fit | books | what happens |
|---|---|---|---|---|
| **TYPE-WINDOW** | intro | song intro / first downbeats | 0 | A question types in. A giant word becomes a window onto the key visual (`background-clip:text`), then opens into a rounded KV window card with parallax. |
| **KV-PARALLAX** | intro | calm build | 0 | KV layers inside a dark window drift at different speeds (2.5D push) while the hook types beside it. |
| **HOOK-IN-SENTENCE** | intro | steady beats | 0 | Hook sentence with a gap. An object (the KV window or a book) drops into the gap. |
| **BOOK3D-OPEN** | series | 2–3 strong hits + a breath | 1 | 3D book turns in, spins (spine/back/pages), opens on its hinge. Page 1 carries a stat or quote. Hold ≥ 1.5 s. |
| **BOOK3D-SPIN** | series | steady | 1–2 | Book turns in and does a slow 360°. Title and author settle beside it. A huge word sits behind it (DEPTH-TYPE). |
| **CHAT-UI** | series | steady, beat-typed | 1 | Original chat window: the user types a question, a KV avatar "types", and the reply is the book (3D book lands beside the window). |
| **CODE-UI** | series | steady, beat-typed | 1 | Original code editor: lines type per beat, ▶ run, terminal ✓, the book flies out toward camera. |
| **OBJECT-IN-SENTENCE** | series | downbeat + beats | 1 | A one-line title splits and a small spinning 3D book drops into the gap. |
| **DEPTH-TYPE** | series | any | 1 | A Latin word ~430px at 14% opacity sits behind the book, which overlaps it. |
| **STAT-RING** | series | roll → downbeat | 1 | Dotted ring fills while a number counts up, locking on a downbeat ("82가지 실습"). |
| **SHELF-PULL** | series | steady | 2–4 | Books stand spine-out on a shelf; on each hit one slides out and turns to its front. |
| **SLOGAN-WEIGHT** | climax | strongest surge | – | Light/bold pair ("바로 배워," 300 / "바로 쓴다." 700), revealed by the transition, with a weight pulse and a hand-drawn underline. |
| **SPINE-STACK** | finale | beats into a downbeat | all | Books drop one per beat into a pile of spines, then stand up and turn to the front into a row. Slogan, then logo lockup. |
| **SHELF-LOCKUP** | finale | calm end | all | Books slide onto a shelf spine-out. The logo lockup sits above. The last book turns to its front on the final hit. |

## Paper-pop patterns (STYLE_PATTERNS["paper-pop"]); reference build `videos/comhwal1-169-paperpop-1`
Japanese qualification-ad grammar in paper (research: `research/jp-exam-ads/PRINCIPLES.md`). Building blocks: `styles/paper-pop/kit.html`.
A single-book promo tiles **one `series[]` entry per selling point** (or hand-write the frame table, as the reference build did).

| id | role | music fit | what happens |
|---|---|---|---|
| **COLD-OPEN-GRID** | intro | silent pre-roll (`bgm.preroll`) + tick SFX | Target call on one worried face → pull back to a 10×10 board of faces → stat slam with ※ source → most faces FALL off (떨어지다) → pain bubbles on accelerating ticks. |
| **TARGET-CALL** | intro | first bars | "○○ 준비 중이세요?" on a face, then one stat. Shorter version of the above. |
| **BAT-CRACK** | reveal | the band's first downbeat | Manga impact: concentration lines + onomatopoeia; the book is batted into frame and lands as a white-rimmed sticker; shout line + title cushion. |
| **RED-SHEET** | point | 3 bars | Notebook telop; red-pen ✕ over the wrong idea; the answer hidden under a 赤シート slides out; hanamaru; face worry → happy. |
| **PROGRESS-WALK** | point | 6–8 beats | Week tiles drop per beat; a fired-up (headband) face hops tile to tile at 12 fps to a 합격 sign. |
| **TRI-PANEL** | point | 3 bars | Three paper panels slide up (Japanese 3-split) with faces + count-ups; the sum slams on a tilted cushion. |
| **SCORE-CARD** | point | 3 bars | Original paper grading card: file drops in, score bars pass a red 70 line, hanamaru; telop one word per beat; ※화면은 연출. |
| **BUBBLE-POP** | bundle | 6 beats + downbeat | Gingham ground, book centre, six feature bubbles pop one per beat, faces cling to bubbles; ＼ shout ／. |
| **STEP-PILLS** | point | steady | FOM-style STEP 1–3 pills stacked per beat, current step at 100%, others 40%. (unused so far) |
| **CHAT-BUBBLES** | point | steady | Faces ask questions in bubbles, the author/book answers (community / Q&A). (unused so far) |
| **TAPE-BACK** | climax | strongest chorus | Callback to the cold-open board: fallen faces are slapped back with masking tape in beat waves (붙다 = stick/pass), mega pun line, ≥1.5 s hold. |
| **SEARCH-CTA** | finale | stop-time ending hits | Book + vertical slogan (縦書き) → generic search bar typed on the stop hits → cursor click → logo on the final hit, hold. |

## Timing rules every pattern obeys
- Hard hits are 0ms `tl.set`. Eased entrances run 0.3–0.5s; macro builds run 0.8–2s across a roll.
- Lead the anchor: a move that must land on a beat starts 40–190ms early.
- Texture words hold 1 beat (0.47s at 129 BPM). Readable lines and book titles hold at least 3 beats.
- Frame boundaries never split a hi-hat roll (`new_variant.py` already snaps them).
- The climax goes on the frame with the highest-energy SURGE (`new_variant.py` marks it).
