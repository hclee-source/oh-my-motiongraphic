#!/usr/bin/env python3
"""Derive a per-book color set from each cover, so every scene can live in its own palette
(cover-derived color is a publishing classic and kills the "same three colors every video" problem).

  .venv/bin/python cover_palette.py <isbn> [<isbn> …] [--cream "#F4EFE6"] [--json out.json]

For each cover: `base` (most prominent saturated color), `tint` (pastel ground, base mixed into cream),
`deep` (dark shade for text/shapes on the tint), `pop` (2nd saturated color, for accents).
"""
import argparse, colorsys, json, sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import load_books, ROOT, hex_rgb  # noqa: E402


def hexs(rgb):
    return "#%02X%02X%02X" % tuple(int(round(c)) for c in rgb)


def mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def saturated_colors(path, k=12):
    im = Image.open(path).convert("RGB")
    im.thumbnail((240, 240))
    q = im.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: k * 3]
    counts = sorted(q.getcolors(), reverse=True)
    out = []
    for n, idx in counts:
        rgb = tuple(pal[idx * 3: idx * 3 + 3])
        h, l, s = colorsys.rgb_to_hls(*[c / 255 for c in rgb])
        if s > 0.35 and 0.18 < l < 0.82:
            out.append((n * (0.5 + s), rgb, h))
    out.sort(reverse=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("isbns", nargs="+")
    ap.add_argument("--cream", default="#F4EFE6")
    ap.add_argument("--json")
    a = ap.parse_args()
    books = load_books()
    cream = hex_rgb(a.cream)
    res = {}
    for i in a.isbns:
        cols = saturated_colors(ROOT / books[i]["cover"])
        if not cols:
            continue
        base = cols[0][1]
        pop = next((c[1] for c in cols[1:] if abs(c[2] - cols[0][2]) > 0.08), base)
        h, l, s = colorsys.rgb_to_hls(*[c / 255 for c in base])
        deep = tuple(c * 255 for c in colorsys.hls_to_rgb(h, 0.22, min(0.75, s)))
        res[i] = {"title": books[i].get("title", ""), "base": hexs(base), "tint": hexs(mix(cream, base, 0.22)),
                  "deep": hexs(deep), "pop": hexs(pop)}
        print(f'{i}  base {res[i]["base"]}  tint {res[i]["tint"]}  deep {res[i]["deep"]}  pop {res[i]["pop"]}  {res[i]["title"][:30]}')
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
