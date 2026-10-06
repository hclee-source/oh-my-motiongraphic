# Pitfalls (each one broke a real build here)

`scripts/preflight.py` statically catches 1–5. 6–10 only show up in assembled snapshots (`review.py`).

1. **`#stage[data-composition-id="…"]` in CSS = an unstyled frame.** The compiler scopes every frame's
   CSS by itself and moves `data-composition-id` onto the host div, so that compound selector matches
   nothing. v1 symptoms: Korean fell back to a serif font, and the finale frame rendered black.
   → Write plain `#stage { … }`.
2. **`visibility: visible` on any frame element leaks it into every other frame.** An explicit
   `visible` overrides the hidden host. v2 symptom: a typewriter caret from frame 7 showed as a
   yellow bar through the whole video. → Use `inherit` / GSAP `autoAlpha`.
3. **Unprefixed ids/classes collide.** All frames share one DOM, so `#g1_title` in frame 4 and in
   frame 6 animate each other. → Use `f<N>_` ids and `f<N>-` classes everywhere.
4. **Non-deterministic code.** Math.random, Date.now, rAF, timers and CSS @keyframes all break seek-safe
   rendering. → Derive variation from indices and drive everything with the one paused timeline.
5. **Missing fonts.** Paperlogy is not bundled, so every frame (and the HUD) must declare the three
   `@font-face` rules. Asset paths are `assets/…` relative to the project root.
6. **Workers' self-tests are not proof.** A standalone page has no compiler scoping, no siblings and
   no HUD. Only `npx hyperframes check` + `review.py` snapshots of the assembled project count.
7. **Layout-checker false alarms vs. real bugs.** Mega type under the HUD, outline-only marquee text and
   the odometer strips are intentional → mark them `data-layout-allow-overlap` / `data-layout-allow-occlusion`
   / `data-layout-ignore` / `data-layout-allow-overflow`. Overlapping captions, or a counter on top
   of the HUD chip, are real bugs → move them.
8. **`assemble-index.mjs` rewrites index.html, which drops the HUD.** Always assemble with `scripts/assemble.py`,
   which re-injects the HUD.
9. **Layout properties in tweens** (`left/top/width`) stutter in capture → animate x/y/scale. The odometer
   uses transform strips + 0ms sets (onUpdate text writes may not fire on seek).
10. **Stylized type can't read in time.** Captions held under 3 beats only work as texture. Put the book
    title in the label box that stays on screen.
11. **Audio:** HeyGen BGM needs a login. This project uses Mixkit (Mixkit Stock Music Free License,
    commercial use, no attribution needed — re-check the license page before publishing). Always run
    `bgm.py vocal` because vocals fight on-screen type.
13. **AI background removal fails on dark clay/3D key visuals.** The matte dropped a grey laptop, the books
    and both chat bubbles, and punched holes in a face. → Use `kv_assets.py` feathered layers on an ink
    register matched to the KV's black. Never redraw characters or logos from a supplied KV; only place the files.
14. **Series pages beat the home page.** `goldenrabbit.co.kr/books?series=<name>` lists every book in a series.
    Grep its `/books/<isbn>` links and pass them to `fetch_books.py --isbn`. Cover titles can differ from catalog
    titles (e.g. 9791124516157 is "바로바로 제미나이 구글 AI" on the cover), so use the cover title in copy.
15. **A whole-track "roll" breaks the skeleton.** Synthpop tracks with constant hi-hats came back from the analyzer as one
    26s `sustained-fill`, so every boundary candidate was discarded and the frames collapsed to length 0. → `new_variant.py`
    now ignores rolls longer than 4 bars and clamps the intro (10–32% of the track) and the finale.
16. **OTF fonts must be staged too.** Gmarket Sans ships as `.otf`; the scaffolder copies `*.ttf` and `*.otf` from `shared/fonts`.
17. **3D flattens silently.** `filter`, `opacity<1`, `overflow`, `clip-path` or `mix-blend-mode` anywhere on a 3D book chain
    turns it into a flat card. Preflight flags the obvious cases; also check the review snapshots.
18. **SVG draw-on with `pathLength="1"` doesn't animate.** GSAP rounds `strokeDashoffset` to integers, so the stroke
    jumps from hidden to fully drawn. → Use `pathLength="1000"` with `stroke-dasharray: 1000` and tween `strokeDashoffset`
    from 1000 to 0.
19. **Overlays need their own z-index.** Frame hosts are not stacking contexts, so a z-indexed card inside a frame painted
    OVER the transition overlay. → `assemble.py` mounts every overlay with `style="z-index: 900 + track*50"`.
20. **Fine grain explodes file size.** Per-pixel noise jittered at 12 fps made a 30s render 252 MB (40 Mbps even at CRF 20).
    → Soft, slightly coarse grain (192px noise blurred, shown at 384px), 8 fps jitter, opacity 0.10. The same render dropped to 44 MB.
21. **Iris reveals must open from the middle.** A filled circle shrinking to a point hides the center last, so the climax
    slogan appeared in fragments. → SVG mask hole: close onto a point (cover), then open from the point (reveal).
12. **Homepage catalog rotates.** `fetch_books.py` only discovers what's linked today; add older titles
    with `--isbn`. Pre-order books use a slug (e.g. `pre_aiyle0zs`) instead of an ISBN.
