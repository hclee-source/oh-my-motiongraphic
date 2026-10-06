# Frame-worker dispatch (SKILL.md step 6)

Use one subagent per frame, all in parallel (Agent tool, `subagent_type: general-purpose`, background).
Each prompt has exactly three parts, in this order:

1. **The full text of** `~/.claude/skills/music-to-video/sub-agents/frame-worker.md`, verbatim. Read
   it fresh each run; don't paraphrase it.
2. **The dispatch context block** (fill the `<…>`):

```text
PROJECT_DIR: <abs path to videos/<name>>
frame_id: <NN-fN>
Your block: the `## Frame N — fN` block in PROJECT_DIR/STORYBOARD.md
audiomap: PROJECT_DIR/audiomap.json
frame.md: PROJECT_DIR/frame.md
Materials: ~/.claude/skills/music-to-video/references/motion-primitives/{<ids>}/scene.html
           (+ templates/card-flyby/index.html for CARD-FLYBY)
           + reference implementation: <abs path>/.claude/skills/goldenrabbit-promo/examples/<bold-beat-45s|editorial-gold-46s>/frames/<file>.html
           (see references/scene-patterns.md for which file matches the pattern)
           ; staged assets/covers/<isbn>.jpg …, assets/brand/icon.png, assets/fonts/*.ttf
Contracts: ~/.claude/skills/hyperframes-core/references/sub-compositions.md + determinism-rules.md (+ data-attributes.md)
Canvas: <w>×<h>   Pacing: <beat_cut|phrase_flow>
Write to: PROJECT_DIR/compositions/frames/<NN-fN>.html
```

3. **The project notes below**, verbatim, with `fN` replaced by the frame tag:

```text
Project notes (each rule comes from a real broken build):
- CSS root rule: style the root as plain `#stage { … }`. NEVER `#stage[data-composition-id="…"]`.
  The compiler scopes CSS itself and moves that attribute to the host, so the selector matches
  nothing and the frame renders unstyled. A standalone test page will NOT show this bug.
- Never set `visibility: visible` (CSS or GSAP). It overrides the hidden host and leaks the
  element into every other frame. Use `autoAlpha` / `visibility: inherit`.
- Prefix EVERY id with `fN_` and EVERY class with `fN-`. All frames share one DOM. Look up
  elements only by those ids.
- HUD: if frame.md says a HUD overlay is on, keep readable content inside the safe band it
  states. Mega type may crop past edges as texture; mark it `data-layout-allow-overlap`.
  Outline-only text gets `data-layout-ignore`.
- Fonts and paths: write asset/font URLs as `assets/...`. Korean = Paperlogy, so declare
  frame.md's three @font-face rules inside your <style>. Archivo Black / IBM Plex Mono /
  Montserrat are bundled. For Playfair Display italic, write `font-family:"Playfair Display";
  font-style:italic; font-weight:700`.
- Covers, confetti and icons are plain elements animated by GSAP (not timed .clip elements).
  Animate transforms only (x/y/scale/rotation/opacity). Marquee offsets are timeline tweens.
  No Math.random / Date.now / CSS animations.
- Book covers: real JPG; never crop, tint or overlay text. Titles go in label boxes or captions
  next to the cover, and hold ≥ 3 beats.
- Use exactly the storyboard copy. The `pattern_hint` + `### Groups` define WHAT; you decide HOW.
- Do not run the hyperframes CLI. Reply with a 3-line summary plus any deviations.
```

After all workers return: confirm every `compositions/frames/NN-fN.html` exists (re-dispatch a missing
one once), then run `scripts/assemble.py` (it runs preflight first). If preflight fails, re-dispatch
the offending frame's worker with the preflight lines pasted under "lint/check feedback from a prior pass".
