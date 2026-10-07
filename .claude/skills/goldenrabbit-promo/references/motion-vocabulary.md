# Motion vocabulary & the anti-sameness system

Written 2026-10-02 after the user said every promo "comes out the same". The audit found that v1, v2 and the first
바로바로 cut all shared:
- the same music track (Mixkit 470)
- one Korean font family
- flat 2D only
- 0ms hard cuts
- 10 primitives used in every video: palette-flip, overlay-pop, braam-punch, staggered-exit, screen-shake,
  particle-burst, kinetic-letter-in, freeze-hold, blur-resolve and radial-burst-lines

Sources:
- web research: Buff Motion showreel 2025, the JKR Burger King rebrand intro, the Penguin English Library film, and
  book trailers from TASCHEN, Phaidon, 한빛미디어 and others
- frame analysis of the Buff reel in `research/buff-showreel-2025/`
- a HyperFrames capability inventory: registry, animation rules, keyframes, audio

## 1. The variety system (enforced by `new_variant.py`)
1. **Small fixed core, everything else variable.** The fixed core is the logo lockup, `goldenrabbit.co.kr`, the gold
   mark and real covers. Everything else is a treatment choice.
2. **Treatment card**, with axes style · music · palette · transition · camera · hero · hud. The scaffolder prints the
   card against the most recent variant and **warns if ≥ 3 axes repeat**. Change at least two of style, music,
   transition, camera and hero between consecutive videos.
3. **One hero device per scene, never the previous video's.** Patterns used by the last variant are deprioritized
   automatically (rationing). Each style owns its own pattern pool (`STYLE_PATTERNS`).
4. **Rotate music genre and tempo.**
   - Used so far: 470 EDM 129 BPM (v1, v2, baro-boldbeat), 1142 synthpop 117.5 (baro-softstudio), 780 ska ~155 (comhwal1-paperpop,
     silent cold open + bar-aligned splice into the song's real ending via `bgm.preroll` / `bgm.segments`).
   - Analyzed and ready: 780 ska 152, 989 funk 117.5, 167 electronica 117.5, 1062/836 house.
5. **Pacing quota.** At least one hold of 1.5 s or more on a beautiful still, at least one continuous (shape) transition, and
   every video gets a sound-design layer (`sfx.py`).
6. **Rationed defaults.** Label boxes, confetti, outline marquees, the HUD and full-screen color flips belong to
   `bold-beat`. Don't carry them into other styles.

## 2. Technique menu (what to reach for, by axis)
| axis | technique | how in this pipeline |
|---|---|---|
| Camera/depth | **CSS-3D book**: turn in, 360° spin, open on hinge, spine stack, shelf | `references/recipes/book3d.md` (verified render) |
| | 2.5D parallax: KV window card whose image drifts slower than the card | soft-studio f1 |
| | object between words: the sentence parts and a spinning book drops into the gap | `OBJECT-IN-SENTENCE` |
| Transitions | iris / blinds / stripes / wipe that hide every hard cut | `transition_out:` + `make_transitions.py` (overlay, track 3) |
| | velocity-matched exits/entries (power2.in out, power2.out in, same direction) | frame-worker instruction |
| | match cut on a shape (the book becomes the next window) | plan it across two frames' `intent` |
| Texture | paper grain jittered at 12 fps (seek-safe) | automatic in soft-studio (`texture: grain`) |
| | static seamless washi/paper-fibre overlay | automatic in paper-pop (`texture: paper`) |
| Character | user's avatars regenerated as layered paper-cut faces with expressions (worry/happy/fired) | `shared/characters/` (OpenAI image edit, base → expression) |
| | print/halftone/dither on covers | `npx hyperframes media-treatment --capability print` (render cost unmeasured) |
| | stop-motion "on twos" | stepped eases / `tl.set` at 1/12 s |
| Typography | type-as-window (the KV seen through letters) | `background-clip: text` with the KV image |
| | depth-sorted type (a huge word BEHIND the book) | z-order, `data-layout-allow-overlap` |
| | light/bold contrast pairs (300 vs 700) instead of scale slams | soft-studio type ramp |
| | hand-drawn scribble / underline / circle | SVG path + stroke-dashoffset |
| Layout/info | original chat-window mockup, code-editor mockup | `CHAT-UI`, `CODE-UI` (never copy real product UIs) |
| | dotted stat ring + count-up ("82가지 실습", "45개 실습") | `STAT-RING` |
| Pacing | hold and release (≥ 1.5 s still), speed ramp after a hold | storyboard `intent` |
| Sound | silent cold open with clock ticks (`tick`/`tock`), the band entering on a hit (`bat-crack`) | `bgm.preroll` + `- sfx:` cues (comhwal1-paperpop) |
| Sound | whoosh on transitions, pop on landings, typing on UI, chime on lockup, impact on the climax | `- sfx:` cues + `sfx.py` (shared/sfx, Pixabay licence) |
| Narrative | character as guide (KV avatars inside the UI), "a question → an answer per book" | copy + avatars |
| Color | cover-derived pastel per scene | `cover_palette.py`, written to `scene_color` automatically |

## 3. Not usable here (verified)
- **Registry shader blocks** (`light-leak`, `glitch`, …): self-contained 4 s demos that can't see our frames. Use them as GLSL
  reference only.
- **`HyperShader` across frame hosts:** untested, and roughly triples capture cost.
- **WebGPU / liquid-glass blocks:** they need Chrome Canary.
- **`grain-overlay` block:** uses infinite CSS keyframes, which is not seek-safe. Use our generated grain instead.
- **Variable-font animation:** our Korean fonts are static weights.
- **`split-flap-board`:** has no Hangul.
- **HeyGen SFX:** needs a login, so only the 19 bundled files are available.
