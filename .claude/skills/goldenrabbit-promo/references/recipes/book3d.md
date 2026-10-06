# Recipe — CSS-3D book (verified render, 2026-10-02)

A real book object with a front cover (the actual JPG), spine (title set vertically), page block (top and fore-edge
with page lines), back cover and an opening hinge. It is seek-safe (GSAP transforms only) and was verified with
`hyperframes snapshot`: the entry turn, a 360° spin showing the back, spine and pages, and the cover opening onto page 1.

Replace `fN` with the frame tag. Sizes are for a 420×574 book (cover ratio ≈ 0.73), thickness T = 48. Scale the
whole object with GSAP `scale` on `#fN_book`; don't change the face math.

## Rules
- Never put `filter`, `opacity < 1`, `overflow`, `clip-path` or `mix-blend-mode` on `.fN-bk-book`, `.fN-bk-hinge` or
  anything between them and `.fN-bk-scene`. Any of those flattens 3D. Fade the book in by scaling it from 0, by
  sliding it in from off-frame, or by fading the **scene** wrapper from outside the 3D chain.
- The contact shadow is a separate flat div (it may use `filter: blur`). Animate its scaleX/opacity with the book.
- Rest pose: `rotationY: -28, rotationX: 8` (spine side away). For a spine-first pose use `rotationY: 62`.
- Spine color = the scene's `deep` color from `cover_palette.py`; the spine title is in Gmarket Sans 700, cream.

## Markup (inside the frame's group)
```html
<div class="fN-bk-scene">                       <!-- position: absolute at the book's center; perspective -->
  <div class="fN-bk-shadow" id="fN_bk_shadow"></div>
  <div class="fN-bk-book" id="fN_book">
    <div class="fN-bk-back"></div>
    <div class="fN-bk-spine">바로바로 클로드</div>
    <div class="fN-bk-edge"></div>
    <div class="fN-bk-top"></div>
    <div class="fN-bk-bottom"></div>
    <div class="fN-bk-page">바로 배워<br />바로 쓰는!</div>   <!-- page 1, seen when the cover opens -->
    <div class="fN-bk-hinge" id="fN_bk_hinge">
      <img class="fN-bk-front" src="assets/covers/<isbn>.jpg" />
      <div class="fN-bk-inside"></div>
    </div>
  </div>
</div>
```

## CSS
```css
.fN-bk-scene { position: absolute; left: 960px; top: 540px; width: 0; height: 0; perspective: 2200px; }
.fN-bk-shadow { position: absolute; left: -260px; top: 250px; width: 520px; height: 70px; border-radius: 50%;
  background: rgba(40, 25, 15, 0.30); filter: blur(22px); }
.fN-bk-book { position: absolute; left: -210px; top: -287px; width: 420px; height: 574px; transform-style: preserve-3d; }
.fN-bk-book > div, .fN-bk-hinge > div { position: absolute; }
.fN-bk-back   { inset: 0; background: DEEP; transform: rotateY(180deg) translateZ(24px); }
.fN-bk-spine  { left: 186px; top: 0; width: 48px; height: 574px; background: DEEP; transform: rotateY(-90deg) translateZ(210px);
  display: flex; align-items: center; justify-content: center; color: #F4EFE6; font: 700 22px "Gmarket Sans"; writing-mode: vertical-rl; }
.fN-bk-edge   { left: 186px; top: 0; width: 48px; height: 574px; transform: rotateY(90deg) translateZ(210px);
  background: repeating-linear-gradient(90deg, #FBF8F2 0 2px, #E4DCCD 2px 3px); }
.fN-bk-top    { left: 0; top: 263px; width: 420px; height: 48px; transform: rotateX(90deg) translateZ(287px);
  background: repeating-linear-gradient(0deg, #FBF8F2 0 2px, #E4DCCD 2px 3px); }
.fN-bk-bottom { left: 0; top: 263px; width: 420px; height: 48px; transform: rotateX(-90deg) translateZ(287px); background: #E9E1D2; }
.fN-bk-page   { inset: 0; background: #FBF8F2; transform: translateZ(22px); display: flex; align-items: center; justify-content: center;
  color: DEEP; font: 700 44px/1.25 "Gmarket Sans"; text-align: center; }
.fN-bk-hinge  { inset: 0; transform-origin: 0% 50%; transform: translateZ(24px); transform-style: preserve-3d; }
.fN-bk-front  { inset: 0; width: 420px; height: 574px; object-fit: cover; backface-visibility: hidden; }
.fN-bk-inside { inset: 0; background: #F4EFE6; transform: rotateY(180deg); backface-visibility: hidden; }
```

## Motion vocabulary (GSAP, frame-local seconds; set every start state at 0)
```js
tl.set("#fN_book", { x: 900, z: -900, rotationY: -120, rotationX: 18 }, 0);   // off to the right, edge-on
tl.set("#fN_bk_hinge", { rotationY: 0 }, 0);
// ENTER (turn in from the side, landing on a hit)
tl.to("#fN_book", { x: 0, z: 0, rotationY: -28, rotationX: 8, duration: 0.7, ease: "expo.out" }, HIT1 - 0.12);
tl.fromTo("#fN_bk_shadow", { scaleX: 0.3, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.7, ease: "expo.out", immediateRender: false }, HIT1 - 0.12);
// SPIN (shows back, spine, pages — 1.0–1.4s across a bar)
tl.to("#fN_book", { rotationY: 332, duration: 1.2, ease: "power3.inOut" }, HIT2);
// OPEN (cover swings on the hinge, landing on a kick) — then HOLD ≥ 1.5s for the "beautiful still"
tl.to("#fN_bk_hinge", { rotationY: -155, duration: 0.6, ease: "power3.out" }, HIT3);
tl.to("#fN_book", { rotationY: -12, rotationX: 4, duration: 0.6, ease: "power3.out" }, HIT3);
// FLOAT (idle life while held): tiny y bob, at most ±6px over 2 beats, yoyo via explicit tweens (no repeat:-1)
```

## Variations
- **Spine stack (finale):** 4 books with `rotationY: 90` and `rotationZ: 90`, stacked with z/y offsets. Each one turns
  to the front on its own kick.
- **Book in sentence:** a small book (scale 0.45) sits in the gap between two words and does a full spin while the words
  slide apart to make room.
- **Shelf:** books stand spine-out (`rotationY: 62`) in a row. On a hit one book slides out (z+) and turns to its front.
