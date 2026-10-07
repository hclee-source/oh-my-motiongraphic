"""Shared helpers for the goldenrabbit-promo skill scripts."""
import json, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
SHARED = ROOT / "shared"
VIDEOS = ROOT / "videos"
VARIANTS = ROOT / "variants"
PY = ROOT / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
M2V = Path.home() / ".claude" / "skills" / "music-to-video"

# Canvas + layout per aspect. "content" = where readable frame content may sit when the HUD is on.
ASPECTS = {
    "16:9": {"w": 1920, "h": 1080, "scale": 1.0, "side": 96,
             "content": [104, 984],
             "hud": {"box_top": 28, "box_h": 40, "edge": 40, "chip_top": 76, "band_top": 1000, "band_h": 80,
                     "brand_px": 18, "tc_px": 19, "ticker_px": 22}},
    "9:16": {"w": 1080, "h": 1920, "scale": 0.85, "side": 64,
             "content": [250, 1540],   # keeps clear of Shorts/Reels top UI and the caption/CTA zone
             "hud": {"box_top": 120, "box_h": 44, "edge": 48, "chip_top": 172, "band_top": 1572, "band_h": 96,
                     "brand_px": 20, "tc_px": 22, "ticker_px": 26}},
    "1:1": {"w": 1080, "h": 1080, "scale": 0.8, "side": 64,
            "content": [96, 1000],
            "hud": {"box_top": 24, "box_h": 34, "edge": 28, "chip_top": 64, "band_top": 1016, "band_h": 64,
                    "brand_px": 15, "tc_px": 16, "ticker_px": 19}},
}


def aspect_cfg(aspect):
    if aspect not in ASPECTS:
        raise SystemExit(f"✗ aspect must be one of {list(ASPECTS)}")
    return ASPECTS[aspect]


def load_style(name):
    d = SKILL / "styles" / name
    if not d.exists():
        raise SystemExit(f"✗ unknown style '{name}' — available: {[p.name for p in (SKILL / 'styles').iterdir() if p.is_dir()]}")
    return json.loads((d / "style.json").read_text()), (d / "FRAME.md").read_text()


def render_tokens(text, tokens, scale=1.0):
    """{{name}} → tokens[name]; {{px:240}} → round(240*scale)."""
    text = re.sub(r"\{\{px:(\d+(?:\.\d+)?)\}\}", lambda m: str(round(float(m.group(1)) * scale)), text)
    return re.sub(r"\{\{([a-z0-9_]+)\}\}", lambda m: str(tokens.get(m.group(1), m.group(0))), text)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load_books():
    p = SHARED / "books" / "books.json"
    if not p.exists():
        raise SystemExit("✗ no catalog — run scripts/fetch_books.py")
    return {b["isbn"]: b for b in json.loads(p.read_text())}


def parse_storyboard(path):
    """Minimal parser: frontmatter text + frames [{n, id, src, span:[a,b], fields{...}}]."""
    s = Path(path).read_text()
    frames = []
    for m in re.finditer(r"^## Frame (\d+) — (\S+)\n(.*?)(?=^## Frame |\Z)", s, re.S | re.M):
        body = m.group(3)
        f = {"n": int(m.group(1)), "id": m.group(2), "fields": {}}
        for fm in re.finditer(r"^- ([a-z_]+): (.*)$", body, re.M):
            f["fields"][fm.group(1)] = fm.group(2).split(" #")[0].strip()
        sp = re.search(r"\[([\d.]+),\s*([\d.]+)\]", f["fields"].get("span_sec", ""))
        if sp:
            f["span"] = [float(sp.group(1)), float(sp.group(2))]
        f["src"] = f["fields"].get("src", "")
        frames.append(f)
    return frames
