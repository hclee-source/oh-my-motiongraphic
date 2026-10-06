#!/usr/bin/env python3
"""Cheapest variation: copy a finished variant and swap its palette — no rebuild, no agents.

Replaces the style's token colors (hex in any case + matching rgb()/rgba() triples) across
compositions/, frame.md, STORYBOARD.md and variant.json. The logo mark is an image, so the
brand gold of the logo itself never changes.

  python3 retint.py videos/<src> <new-name> --accent "#3DF5B0" [--ink "#0B0B0B"] [--paper "#F2F0EA"]
then: assemble is NOT needed (index.html is copied); run check → review → finalize.
"""
import argparse, json, re, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import ROOT, VARIANTS, VIDEOS, hex_rgb, load_style  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("name")
    for k in ("accent", "ink", "paper", "muted"):
        ap.add_argument(f"--{k}")
    a = ap.parse_args()
    src = Path(a.src).resolve()
    dst = VIDEOS / a.name
    if dst.exists():
        sys.exit(f"✗ {dst} exists")
    spec = json.loads((src / "variant.json").read_text()) if (src / "variant.json").exists() else {"style": "bold-beat"}
    style, _ = load_style(spec.get("style", "bold-beat"))
    old = dict(style["tokens"]); old.update(spec.get("palette", {}))
    new = {k: getattr(a, k) for k in ("accent", "ink", "paper", "muted") if getattr(a, k)}
    if not new:
        sys.exit("✗ pass at least one of --accent/--ink/--paper/--muted")
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("renders", "snapshots", ".backup", "node_modules"))
    (dst / "renders").mkdir(exist_ok=True)
    pairs = [(old[k], v) for k, v in new.items() if k in old and old[k].lower() != v.lower()]
    files = list((dst / "compositions").rglob("*.html")) + [dst / "frame.md", dst / "STORYBOARD.md"]
    total = 0
    for f in files:
        if not f.exists():
            continue
        s = f.read_text()
        for o, n in pairs:
            s, c1 = re.subn(re.escape(o), n, s, flags=re.I)
            ro, rn = hex_rgb(o), hex_rgb(n)
            s, c2 = re.subn(rf"rgba?\(\s*{ro[0]}\s*,\s*{ro[1]}\s*,\s*{ro[2]}\s*([,)])", lambda m: f"rgba({rn[0]}, {rn[1]}, {rn[2]}{m.group(1)}" if m.group(1) == "," else f"rgb({rn[0]}, {rn[1]}, {rn[2]})", s)
            total += c1 + c2
        f.write_text(s)
    spec["name"] = a.name
    spec.setdefault("palette", {}).update(new)
    spec["retinted_from"] = src.name
    (dst / "variant.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2))
    VARIANTS.mkdir(exist_ok=True)
    (VARIANTS / f"{a.name}.json").write_text(json.dumps({k: v for k, v in spec.items() if k != "resolved"}, ensure_ascii=False, indent=2))
    m = dst / "meta.json"
    if m.exists():
        d = json.loads(m.read_text()); d["id"] = d["name"] = a.name; m.write_text(json.dumps(d, indent=2))
    print(f"✓ {dst.relative_to(ROOT)} · {total} color replacements · {pairs}")
    print("next: (cd that project && npx hyperframes check .) → review.py → finalize.sh")


if __name__ == "__main__":
    main()
