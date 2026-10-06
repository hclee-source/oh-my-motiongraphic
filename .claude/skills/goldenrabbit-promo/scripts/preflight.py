#!/usr/bin/env python3
"""Static preflight for frame files — catches the failures that a worker's standalone test
cannot see but that break the assembled render (all observed in real builds of this project).

  python3 preflight.py videos/<name>       # exit 1 on errors
"""
import re, sys
from pathlib import Path

ERR, WARN = [], []


def check(path):
    s = path.read_text()
    fid = path.stem                     # e.g. 03-f3
    tag = fid.split("-")[-1]            # f3
    styles = "\n".join(re.findall(r"<style>(.*?)</style>", s, re.S))
    scripts = "\n".join(re.findall(r"<script>(.*?)</script>", s, re.S))
    rel = path.name

    if "<template" not in s:
        ERR.append(f"{rel}: no <template> wrapper (sub-composition content must live inside it)")
    if re.search(r"#stage\[data-composition-id", styles):
        ERR.append(f"{rel}: CSS uses #stage[data-composition-id=…] — the compiler moves that attribute to the host; use bare #stage")
    if re.search(r"visibility\s*:\s*visible", styles) or re.search(r"visibility\s*:\s*[\"']visible", scripts):
        ERR.append(f"{rel}: sets visibility:visible — it overrides the hidden host and leaks this element into every other frame; use inherit/autoAlpha")
    if not re.search(rf'data-composition-id="{re.escape(fid)}"', s):
        ERR.append(f'{rel}: root data-composition-id must be "{fid}"')
    if "__timelines[" not in scripts or not re.search(rf'["\']{re.escape(fid)}["\']', scripts):
        ERR.append(f'{rel}: timeline must be registered as window.__timelines["{fid}"] (key not found in script)')
    for bad, why in [(r"Math\.random\(", "Math.random (non-deterministic)"), (r"Date\.now\(|performance\.now\(", "wall-clock time"),
                     (r"requestAnimationFrame\(", "rAF loop"), (r"setTimeout\(|setInterval\(", "timers")]:
        if re.search(bad, scripts):
            ERR.append(f"{rel}: {why} in script")
    if re.search(r"@keyframes|animation\s*:", styles):
        WARN.append(f"{rel}: CSS animation found — must be driven by the GSAP timeline to be seek-safe")
    if re.search(r'(?:src|href)="https?://', s):
        ERR.append(f"{rel}: remote asset URL — stage it under assets/")
    if re.search(r'url\(["\']?/', styles) or re.search(r'src="/', s) or "../assets" in s:
        ERR.append(f"{rel}: asset path must be relative 'assets/…' (no leading slash / ../)")
    if "Paperlogy" in s and "Paperlogy-8ExtraBold.ttf" not in s:
        ERR.append(f"{rel}: uses Paperlogy without the @font-face rules from frame.md")
    if "Gmarket Sans" in s and "GmarketSansBold.otf" not in s:
        ERR.append(f"{rel}: uses Gmarket Sans without the @font-face rules from frame.md")
    if re.search(r"bk-(book|hinge)[^{]*\{[^}]*\b(filter|clip-path|overflow|mix-blend-mode)\s*:", styles):
        ERR.append(f"{rel}: filter/clip-path/overflow/blend on a 3D book element flattens it (see recipes/book3d.md)")
    if re.search(r'\{[^}]*\b(left|top|width|height)\s*:\s*-?[\d.]+(px|%)?\s*[,}][^}]*\b(duration|ease)\b', scripts):
        WARN.append(f"{rel}: tween animates left/top/width/height — use x/y/scale (layout props stutter in capture)")
    ids = re.findall(r'(?<![\w-])id="([^"]+)"', s)
    unpref = [i for i in ids if i not in ("stage", "root") and not re.match(rf"{tag}[_-]", i) and not i.endswith("-template")]
    if unpref:
        WARN.append(f"{rel}: {len(unpref)} ids without the '{tag}_' prefix (collide across frames): {unpref[:6]}")
    classes = set(c for cl in re.findall(r'(?<![\w-])class="([^"]+)"', s) for c in cl.split())
    unpc = [c for c in classes if not re.match(rf"{tag}[_-]", c) and c not in ("clip",)]
    if unpc:
        WARN.append(f"{rel}: classes without '{tag}-' prefix: {sorted(unpc)[:6]}")
    return ids


def main():
    proj = Path(sys.argv[1]).resolve()
    frames = sorted((proj / "compositions" / "frames").glob("*.html"))
    if not frames:
        sys.exit("✗ no frame files in compositions/frames/")
    seen = {}
    for f in frames:
        for i in check(f):
            if i not in ("stage", "root"):
                seen.setdefault(i, []).append(f.name)
    dup = {i: fs for i, fs in seen.items() if len(set(fs)) > 1}
    for i, fs in list(dup.items())[:10]:
        ERR.append(f"duplicate id '{i}' in {sorted(set(fs))} — GSAP selectors will hit the wrong frame")
    for w in WARN:
        print("⚠", w)
    for e in ERR:
        print("✗", e)
    print(f"preflight: {len(frames)} frames · {len(ERR)} error(s) · {len(WARN)} warning(s)")
    sys.exit(1 if ERR else 0)


if __name__ == "__main__":
    main()
