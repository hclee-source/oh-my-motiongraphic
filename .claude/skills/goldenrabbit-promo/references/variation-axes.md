# Variation axes

A variant is one spec in `variants/<name>.json` (see `variants/_template.json`). Change any axis below
and you get a new variant. The cost column says how much of the pipeline has to re-run.

| axis | spec field | values | cost | notes |
|---|---|---|---|---|
| Palette | `palette.accent/ink/paper` | any hex (see `styles/*/style.json` → `accent_alternatives`) | **cheapest**: `retint.py` copies a finished variant and swaps colors, with no rebuild | Logo gold never changes. Recheck contrast with `check`. |
| Style preset | `style` | `bold-beat` (loud, v2) · `editorial-gold` (calm, v1) | replan + rebuild | Each preset ships FRAME.md tokens + HUD defaults. |
| Pattern seed | `seed` | any int | replan + rebuild | Same music and books, different scene patterns per frame + register order. |
| Intensity | `intensity` | `calm` · `standard` · `hype` | replan + rebuild | calm: 2–3 beats per word, few flips. hype: 1 beat per word, flips on every strong hit, more confetti/marquee. |
| Aspect | `aspect` | `16:9` · `9:16` · `1:1` | rebuild | The scaffolder scales type (×0.85 / ×0.8) and sets the safe zones. 9:16 keeps content in y 250–1540 (platform UI). |
| Length / music window | `bgm.start`, `bgm.duration` | from `bgm.py windows <id> --length N` | rebuild | Each window has a different section map (intro, roll, surge, finale), so frames re-tile. |
| Track | `bgm.id` | any analyzed instrumental in `shared/bgm` | rebuild | Must be instrumental (`bgm.py vocal`). Pulse > 0.09 and 115–135 BPM suit word-per-beat type. |
| Books / series | `series[]` | ISBNs from `shared/books/books.json` | rebuild | Keep 2–5 books per series and ≤ 1 book per ~1.5s of series time. |
| Copy | `copy.hook`, `copy.finale` | Korean lines | replan the affected frames | Hook words should be 1–3 syllables per beat in hype mode. |
| Key visual | `extra_assets[]` + `scripts/kv_assets.py` | the user's illustration | replan + rebuild | Feathered sprites on the ink register, cards on accent/paper. One character per book. |
| Single-book frames | one `series[]` entry per book | label `BARO 01…` | – | A single series becomes one frame per book (see `variants/baro-series-169-boldbeat-1.json`). |
| HUD | `hud` | true/false | assemble only | `make_hud.py` + `assemble.py`; off for a calmer, cleaner look. |

## Ready-made variation recipes
1. **A/B palette test:** finish one variant, then run `retint.py` twice (e.g. yellow → mint, yellow → orange). Three videos for one build.
2. **Platform pack:** the same spec with `aspect` 16:9, 9:16 and 1:1, each with its own seed so the vertical cut isn't a squeezed copy.
3. **Teaser + full:** a 15–20s window (`bgm.py windows 470 --length 18`) with 1–2 series, plus the 45s full version.
4. **Single-series launch:** one series with 4–6 books. Use COUNT-IN or GRID-SWAP, and give the climax to that series.
5. **New-release reel:** filter the catalog for `badges` containing NEW (`fetch_books.py --list`), with one series per release month.
6. **Seed sweep:** the same spec with seeds 1–3 → three distinct storyboards. Show the user the three skeleton tables before building them all.

## Naming
`<scope>-<aspect>-<style>-<n>`, e.g. `newbooks-916-boldbeat-1`, `ppatta-169-editorial-2`. One spec file per variant. Never overwrite a rendered variant: make a new name.
