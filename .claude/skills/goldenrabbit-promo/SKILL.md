---
name: goldenrabbit-promo
description: "골든래빗(goldenrabbit.co.kr) 도서 홍보 모션그래픽 영상을 음악 비트에 맞춘 키네틱 타이포 방식으로 만들고, 스타일·팔레트·화면비·길이·음악 구간·도서 구성·패턴 시드를 바꿔 베리에이션을 뽑는 프로젝트 워크플로. 트리거: 골든래빗 홍보영상, 도서 모션그래픽, 신간 티저, 시리즈 홍보, 쇼츠/릴스용 세로 버전, 베리에이션/AB 버전/색만 바꾼 버전, 'v2처럼', 'v1 스타일로'. HyperFrames music-to-video 위에서 동작하며 v1·v2 실제 제작에서 검증된 스크립트와 함정 대응을 포함한다."
---

# goldenrabbit-promo — beat-synced book promos, with variations

This skill runs the pipeline that produced `videos/goldenrabbit-books-promo` (v1, calm gold) and
`videos/goldenrabbit-books-promo-v2` (v2, bold yellow), so that any later cut is **a new variant
from a spec**, not a hand-rebuild. The design rules are in `references/principles.md`. Read it once per session.

`SKILL` = `.claude/skills/goldenrabbit-promo`, `ROOT` = this project folder. Python that needs librosa
runs as `.venv/bin/python`; every other script runs on plain `python3`.

## 0. Setup (once per machine)
```bash
bash SKILL/scripts/setup.sh          # .venv + librosa, HyperFrames skills, Chrome
```
Shared, reusable inputs live in `ROOT/shared/`: `brand/` (logo), `fonts/` (Paperlogy), `books/` (catalog +
covers), `bgm/` (analyzed tracks). Variant specs live in `ROOT/variants/`; projects in `ROOT/videos/<name>/`.

## Anti-sameness (read before every new video)
Earlier videos all felt the same: one track, one font, flat 2D, hard cuts, and the same 10 primitives. Before planning, read
`references/motion-vocabulary.md`, then:
- **Change at least two treatment axes vs the previous variant:** style, music genre/tempo, transition family, camera
  (flat / 2.5D / 3D) and hero device. `new_variant.py` prints the treatment card and warns on ≥ 3 repeats.
- **Styles:**
  - `bold-beat`: loud, flat, register flips, HUD
  - `editorial-gold`: calm, gold
  - `soft-studio`: cover-derived pastels, CSS-3D books, shape transitions, grain, UI mockups, SFX
- **Every video gets:** at least one ≥1.5s hold, at least one non-hard-cut transition (`transition_out:`), and SFX cues (`- sfx:`).

## 1. Intake → a variant spec
Decide which axes change (`references/variation-axes.md`). Ask only what the request doesn't answer, in
**one** AskUserQuestion round:
- style (`bold-beat` = v2 loud / `editorial-gold` = v1 calm)
- aspect (16:9 YouTube · 9:16 Shorts/Reels · 1:1 feed)
- length / music
- which books or series
- how many variants (seed sweep, palette A/B, platform pack)

Copy `variants/_template.json` → `variants/<name>.json` and fill it in. If the user wants N variants,
write N specs that differ only along the chosen axes, and give each a distinct `seed`.

Cheapest path: if the request is only "the same video in another color", skip to **§9 Retint**.

## 2. Books
```bash
.venv/bin/python SKILL/scripts/fetch_books.py            # refresh catalog from the site (adds new books)
.venv/bin/python SKILL/scripts/fetch_books.py --list     # pick ISBNs (badges NEW/BEST, series, date)
.venv/bin/python SKILL/scripts/fetch_books.py --isbn <isbn>   # add a book not on the home page today
```
Group the books into `series[]` (2–5 books each) and use the exact ISBNs/slugs from the catalog.

## 3. Music
```bash
B=".venv/bin/python SKILL/scripts/bgm.py"
$B list                                   # analyzed library (470 "Golden Storm" is the house track)
$B search --tags upbeat,electronic,house  # new candidates from Mixkit (free license, no attribution)
$B fetch <id> && $B analyze <id> && $B vocal <id>     # keep: instrumental, pulse > 0.09, 115–135 BPM
$B windows <id> --length <seconds>        # bar-aligned windows that end on a strong hit
```
Put the chosen `{id, start, duration}` into the spec's `bgm`. Each window of the same track is a valid,
different variant.

## 4. Scaffold
```bash
.venv/bin/python SKILL/scripts/new_variant.py variants/<name>.json
```
This creates `videos/<name>/` with:
- assets (covers, logo, fonts, cut BGM)
- `frame.md` from the style preset (palette tokens, type scaled for the aspect, safe zones)
- `audiomap.json` from the canonical analyzer
- a **STORYBOARD.md skeleton**: frames tiled on the music (intro · one per series · finale; boundaries snapped out of hi-hat rolls), each with its `pacing`/`feel`, `hud_label`, `book:` lines and a seeded `pattern_hint`; the frame with the strongest surge also gets the climax

Show the user the printed frame table. To see a different arrangement, change `seed` and re-run with
`--force`. That rewrites only the skeleton and leaves any built frames alone.

### 4b. User-supplied key visual / illustration (if any)
Store the original in `shared/keyvisuals/`, list it in the spec's `extra_assets`, and turn it into layers:
```bash
.venv/bin/python SKILL/scripts/kv_assets.py shared/keyvisuals/<kv>.png videos/<name>/assets/keyvisual \
  --sprite <name>:x,y,w,h … --card full:0,0,W,H        # read boxes off a 100px grid drawn over the KV
```
- On dark renders, **don't use the AI cutout** (`hyperframes remove-background`): it drops low-contrast props.
- Use the feathered layers on the INK register, with the spec's `palette.ink` set to the printed `suggested_ink`.
- On accent/paper registers, use `card-*.jpg`.
- Pair one character sprite with each book. Put the full KV on the hook/reveal and on the finale.
- Add a build note to STORYBOARD.md saying the KV is the user's artwork: place it, never redraw it.

Reference build: `videos/baro-series-169-boldbeat-1` (바로바로 series, 2026-10-02).

## 5. Plan (fill every `### Groups`)
Read `references/scene-patterns.md`, the skeleton, `frame.md`, and the matching reference frames in
`SKILL/examples/`. For each frame, replace `- TBD (Step 3)` with groups in music-to-video format. Each group
is exactly one of `template` / `free_design` / `asset` (see
`~/.claude/skills/music-to-video/references/storyboard-format.md`), and carries:
- real audiomap anchor seconds
- the exact Korean copy (pair chips, label-box words)
- an `intent` paragraph detailed enough to build from

Keep the `hud_label` / `book:` / `pattern_hint` lines. Then validate:
```bash
node ~/.claude/skills/music-to-video/scripts/validate-plan.mjs --storyboard videos/<name>/STORYBOARD.md \
  --audiomap videos/<name>/audiomap.json --templates ~/.claude/skills/music-to-video/references/templates
```
Gate on the brief's `storyboard`: `yes` → present the frame-by-frame plan and wait for approval; `no` →
post it as a heads-up and continue.

## 6. Build — one frame worker per frame, in parallel
Follow `references/worker-dispatch.md` **exactly**: role file verbatim + dispatch context + project notes.
The project notes encode the bugs that broke real builds; leaving them out reproduces those bugs.
While the workers run, nothing else needs doing: the HUD is generated in step 7.

## 7. Assemble (+ HUD)
```bash
python3 SKILL/scripts/assemble.py videos/<name>
```
This runs `preflight.py` first and stops on any error (re-dispatch that frame's worker with the
findings). Then it runs `assemble-index.mjs` and adds whichever of these apply:
- if `hud` is on: `make_hud.py` + HUD injection on track 2
- if any frame has `transition_out:`: `make_transitions.py`, a shape-transition and grain overlay on track 3 that covers
  every hard cut (the cover color is the next frame's `scene_color`)
- `sfx.py`: root `<audio>` clips from each frame's `- sfx: name@track_seconds` cues, plus an automatic whoosh before
  every transition

Frames in a transition style must start on their `scene_color` ground and keep essential reads out of the first ~0.37s and
the last ~0.29s.

## 8. QA → render
```bash
(cd videos/<name> && npx hyperframes check .)       # must pass: lint/runtime/layout/motion/contrast
python3 SKILL/scripts/review.py videos/<name>        # snapshots at every frame start/mid/end + key moments
```
**Read every contact sheet.** Look for:
- an element repeated in the same spot across frames (a leak, pitfall 2)
- serif Korean (pitfall 1)
- text over a cover, or under the HUD
- blank frames

Fix with the cheapest safe edit in the frame file, re-check, re-review. Triage layout-checker findings
with `references/pitfalls.md` §7. Then:
```bash
bash SKILL/scripts/finalize.sh videos/<name>         # delivery render, ffprobe check, contact sheet, logs output in variants/<name>.json
```
Report the MP4 path, its duration, and whether audio is present, and show the contact sheet.

## 9. Retint (palette variation, no rebuild)
```bash
python3 SKILL/scripts/retint.py videos/<src> <new-name> --accent "#3DF5B0"   # also --ink/--paper
(cd videos/<new-name> && npx hyperframes check .) && python3 SKILL/scripts/review.py videos/<new-name>
bash SKILL/scripts/finalize.sh videos/<new-name>
```

## 10. Learning from a new reference video
```bash
bash SKILL/scripts/research_reference.sh <youtube-url> [slug]
```
This writes the transcript plus 1-fps timestamped frame sheets. Read the sheets for every music-only span:
the visual techniques are shown there, not in the captions. Add new rules to `references/principles.md`,
and new patterns to `references/scene-patterns.md` (plus `PATTERNS` in `new_variant.py`).

## Rules that keep variants on-brand
- Gold `#CEAE73` appears on the logo mark (`assets/brand/icon.png`) and in editorial-gold UI only. In bold-beat it is never a UI color.
- Real covers are never cropped, tinted or covered with text. Korean is set in Paperlogy.
- Borrow techniques from references, never their copy, names or layouts.
- Never overwrite a rendered variant; make a new name. Keep `variants/<name>.json` as the record.
