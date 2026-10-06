#!/usr/bin/env python3
"""Turn a user-supplied key visual into video-ready layers.

Dark-background illustrations (clay/3D renders on black) don't cut out well with the AI matte
(it drops low-contrast props like a grey laptop). Instead, this makes FEATHERED layers that dissolve
into an ink register whose color matches the KV background:

  kv-full.png        whole KV, edges feathered to transparent (hero on the ink register)
  spr-<name>.png     a crop per character/prop, elliptically feathered (pop-ins next to covers)
  card-<name>.png    hard-edged crop (a "photo card" to toss onto accent/paper registers)
  kv-layers.json     boxes + suggested ink color (KV corner average)

  .venv/bin/python kv_assets.py shared/keyvisuals/baro-kv-01.png videos/<name>/assets/keyvisual \
      --sprite green:1000,80,420,380 --sprite robot:60,500,400,410 --card full:0,0,1536,1024 [--feather 70]

Boxes are x,y,w,h in source pixels. Draw a 100px grid over the KV first to read them off.
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


def feather_mask(w, h, f, ellipse=True):
    """Alpha that reaches exactly 0 at the box edge (inset = f, blur sigma = f/3 → ~0 at the border),
    then hard-clamped to 0 on the outer 2px so no faint rectangle can ever show on the ink ground."""
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    inset = f
    if ellipse:
        d.ellipse([inset, inset, w - inset, h - inset], fill=255)
    else:
        d.rounded_rectangle([inset, inset, w - inset, h - inset], radius=f, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(f / 3))
    ImageDraw.Draw(m).rectangle([0, 0, w - 1, h - 1], outline=0, width=2)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kv"); ap.add_argument("out")
    ap.add_argument("--sprite", action="append", default=[], help="name:x,y,w,h (feathered ellipse)")
    ap.add_argument("--card", action="append", default=[], help="name:x,y,w,h (hard crop)")
    ap.add_argument("--feather", type=int, default=70)
    ap.add_argument("--full-feather", type=int, default=140)
    a = ap.parse_args()
    src = Image.open(a.kv).convert("RGBA")
    W, H = src.size
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    meta = {"source": str(a.kv), "size": [W, H], "layers": {}}

    corners = [src.getpixel(p)[:3] for p in [(4, 4), (W - 5, 4), (4, H - 5), (W - 5, H - 5)]]
    ink = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    meta["suggested_ink"] = "#%02X%02X%02X" % ink

    full = src.copy()
    full.putalpha(feather_mask(W, H, a.full_feather, ellipse=False))
    full.save(out / "kv-full.png")
    meta["layers"]["kv-full"] = {"box": [0, 0, W, H], "file": "kv-full.png", "kind": "feathered-full"}

    for spec in a.sprite:
        name, box = spec.split(":")
        x, y, w, h = map(int, box.split(","))
        crop = src.crop((x, y, x + w, y + h))
        crop.putalpha(feather_mask(w, h, a.feather, ellipse=True))
        crop.save(out / f"spr-{name}.png")
        meta["layers"][f"spr-{name}"] = {"box": [x, y, w, h], "file": f"spr-{name}.png", "kind": "feathered-sprite",
                                         "center": [x + w / 2, y + h / 2]}
    for spec in a.card:
        name, box = spec.split(":")
        x, y, w, h = map(int, box.split(","))
        src.crop((x, y, x + w, y + h)).convert("RGB").save(out / f"card-{name}.jpg", quality=92)
        meta["layers"][f"card-{name}"] = {"box": [x, y, w, h], "file": f"card-{name}.jpg", "kind": "card"}

    (out / "kv-layers.json").write_text(json.dumps(meta, indent=2))
    print(f"✓ {out} · {len(meta['layers'])} layers · suggested ink {meta['suggested_ink']}")
    for k, v in meta["layers"].items():
        print(f"   {k:16s} box={v['box']}  {v['kind']}")


if __name__ == "__main__":
    main()
