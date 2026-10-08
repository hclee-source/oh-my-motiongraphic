#!/usr/bin/env python3
"""Cut characters out of an image whose "transparent" background is a BAKED-IN grey/white checkerboard
(common with AI image generators). The AI matte (`hyperframes remove-background`) erodes white clothing and
leaves checker scraps; a plain light-colour flood leaks into white trousers (they even carry a faint copy of the
checker). So classify the checker *grid cells* instead:

  1. find the tile size (auto: the period of brightness flips along the top row; or --tile)
  2. a cell is background when it is light + neutral + flat inside AND differs from its 4 neighbours by
     ≥ --contrast levels (real checker: 10–17; the faint pattern on clothing: 3–6)
  3. grow the background ≤ one tile into light-neutral pixels to reach cells the art only partly covers
  4. erode 1 px + soften 0.8 px so the light fringe doesn't halo on dark grounds

  .venv/bin/python checker_cutout.py <in.png> <out.png> [--tile 10.667] [--contrast 8] [--preview navy.jpg]
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def detect_tile(lum):
    """Tile size from the brightness flips along the top rows, snapped so a whole number of tiles spans the width
    (generators draw the checker on a grid that divides the canvas)."""
    W = lum.shape[1]
    gaps = []
    for r in (2, 4, 6):
        row = lum[r, :min(600, W)]
        edges = [i for i in range(1, len(row)) if abs(row[i] - row[i - 1]) > 8]
        gaps += [b - a for a, b in zip(edges, edges[1:]) if 6 <= b - a <= 40]
    if len(gaps) < 8:
        raise SystemExit("✗ could not detect a checker period on the top rows — pass --tile")
    base = float(np.median(gaps))                      # some flips are missed → gaps of 2–3 tiles; count them as such
    est = sum(gaps) / sum(max(1, round(g / base)) for g in gaps)
    H = lum.shape[0]
    # snap: a whole number of tiles should span the width AND the height; stay within ±3% of the estimate
    cands = [k for k in range(max(1, int(W / est) - 6), int(W / est) + 7) if abs(W / k - est) <= 0.03 * est]
    n = min(cands or [round(W / est)], key=lambda k: (round(abs(H * k / W - round(H * k / W)), 2), abs(W / k - est)))
    return W / n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--tile", type=float, help="checker tile size in px (default: auto)")
    ap.add_argument("--light", type=int, default=226, help="min channel value for a light pixel")
    ap.add_argument("--chroma", type=int, default=12, help="max channel spread for a neutral pixel")
    ap.add_argument("--contrast", type=float, default=8.0, help="min brightness step to neighbouring cells")
    ap.add_argument("--preview", help="also write a JPG composited on navy for checking")
    a = ap.parse_args()

    rgb = np.asarray(Image.open(a.src).convert("RGB")).astype(np.int16)
    H, W, _ = rgb.shape
    lum = rgb.mean(2)
    light = (rgb.min(2) >= a.light) & ((rgb.max(2) - rgb.min(2)) <= a.chroma)
    t = a.tile or detect_tile(lum)
    nx, ny = int(round(W / t)), int(round(H / t))
    xs = [int(round(i * W / nx)) for i in range(nx + 1)]
    ys = [int(round(j * H / ny)) for j in range(ny + 1)]
    mean = np.full((ny, nx), np.nan)
    ok = np.zeros((ny, nx), bool)
    for j in range(ny):
        for i in range(nx):
            y0, y1, x0, x1 = ys[j] + 2, ys[j + 1] - 2, xs[i] + 2, xs[i + 1] - 2
            if y1 <= y0 or x1 <= x0:
                continue
            c = lum[y0:y1, x0:x1]
            if light[y0:y1, x0:x1].mean() > 0.95 and c.std() < 4.0:
                mean[j, i] = c.mean()
                ok[j, i] = True
    # neighbour contrast (only against neighbours that are themselves flat light cells)
    steps = []
    for dj, di in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nb = np.roll(np.roll(mean, dj, 0), di, 1)
        steps.append(np.abs(mean - nb))
    st = np.stack(steps)
    with np.errstate(all="ignore"):
        import warnings; warnings.simplefilter("ignore", RuntimeWarning)
        contrast = np.nanmedian(st, axis=0)
    cell_bg = ok & (np.nan_to_num(contrast) >= a.contrast)
    bg = np.zeros((H, W), bool)
    for j, i in zip(*np.nonzero(cell_bg)):
        bg[ys[j]:ys[j + 1], xs[i]:xs[i + 1]] = True
    bg = ndimage.binary_dilation(bg, mask=light, iterations=int(round(t)) + 1)
    fg = ndimage.binary_opening(~bg, iterations=1)
    fg = ndimage.binary_erosion(fg, iterations=1)
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    out = Image.open(a.src).convert("RGBA")
    out.putalpha(alpha)
    out.save(a.dst)
    if a.preview:
        bgimg = Image.new("RGBA", out.size, (30, 38, 135, 255))
        bgimg.alpha_composite(out)
        bgimg.convert("RGB").save(a.preview, quality=88)
    print(f"✓ {a.dst} · tile {t:.3f}px ({nx}×{ny} cells) · {cell_bg.sum()} background cells · bg {bg.mean():.1%}")


if __name__ == "__main__":
    main()
