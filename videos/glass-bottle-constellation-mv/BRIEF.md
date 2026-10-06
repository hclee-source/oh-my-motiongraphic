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
