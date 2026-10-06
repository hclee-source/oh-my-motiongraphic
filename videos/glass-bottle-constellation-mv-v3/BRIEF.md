---
workflow: music-to-video
flow: automation
storyboard: no
message: "유리병에 모아 둔 말 못 한 마음(별)이, 마지막에 별자리가 되어 날아간다"
destination: youtube
aspect: "16:9"
language: ko
length: 189.96s (full song)
---

## Intent
J-pop을 지향하는 한국 밴드의 곡 「유리병 별자리」(Suno, 92 BPM, 3:10) 전체를 키네틱 타이포그래피 뮤직비디오로.
사용자 요청: "웹 검색을 통해 이런 노래를 어떻게 뮤직비디오로 표현해야 하는지 찾아보고 만들어봐라."
"뮤직비디오에 집중하고 텍스트에 몇번째 슬라이드인지, 타이머가 어떻게 흘러가는지 등의 잡다한 정보는 빼라."

## Decisions (inferred, with receipts)
- 16:9 YouTube — standard MV deliverable; user's previous runs were 16:9.
- One-shot automation, no storyboard gate — "만들어봐라" + recorded preference.
- No HUD / slide index / timers / section labels / credits — explicit user instruction.
- Mincho-style serif (Noto Serif KR) — J-pop literary lyric-video convention (vertical/horizontal switching, kanji-size emphasis).
- Lyrics synced by forced alignment (MMS_FA on a Demucs vocal stem) → lyrics.json; Whisper alone hallucinated on the mix.

## Research applied (web, 2026-10-03)
- Readability first; line on screen with the first syllable, held through held notes.
- Reset information density at each section (A-melo/B-melo/sabi); escalate verse → pre → chorus; bridge = visual reset; last chorus (key change) = max.
- Alternate vertical/horizontal writing by scene; vertical small + wide tracking; key nouns 1.4–1.5×.
- Keep something slowly moving at all times; combine ≥2 properties per entrance; avoid cheap rotation.

## Assets
- assets/bgm.mp3 — the user's track (유리병 별자리.mp3).
- assets/motifs/bottle.svg, sparkle.svg — drawn for this MV. assets/fonts — Noto Serif KR VF (subset), Cormorant Garamond Italic VF (subset).

## v2 (2026-10-03) — footage mix
User: "뮤직비디오에 쓸 영상 조각들도 10개 넣었는데 뮤비에 섞는 방식으로 재작업해서 영상으로 만들어봐라. 영상 조각에는 음악이 없는 말 그대로 영상만 있는것임"
- 10 silent Higgsfield clips (felt-doll girl, hillside neighbourhood at night, jar of stars) → assets/footage/c01…c10 (1080p lanczos upscale).
- Mix rule: real night = footage (verse 1, verse 2 + pre-chorus 2, final-chorus middle, outro); inner world = v1 motion graphics (intro, pre-chorus 1, choruses, bridge, build, ending). All 10 clips used. Plan: INSERTS.md.
- Footage stretches are insert sub-compositions on track 2 (z 600) over the unchanged v1 frames; grain/vignette overlay stays on top of both.

## v3 (2026-10-03) — footage everywhere
User: "모든 곳에 영상 조각 써 SVG로 병 만든거 쓰지마 너무 짜침"
- No v1 graphic frames, no sky layer, no SVG bottle/hill/house/constellation drawings anywhere.
- compositions/footage.html (generated from .work/edl.json, 48 shots: reused clips with punch-ins, mirroring, slow motion) covers every non-insert second; the 4 v2 inserts stay (exits rewritten to dissolve into footage).
- Lyric layers per section (compositions/lyrics/*.html): typography + light accents on real light only. Spec: LYRICS_V3.md.
