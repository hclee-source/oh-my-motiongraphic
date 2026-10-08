#!/usr/bin/env python3
"""Scaffold one promo variant from a spec (variants/<name>.json).

Creates videos/<name>/ as a HyperFrames music-to-video project:
  init → BRIEF.md → assets (covers, logo, fonts, bgm cut) → frame.md (style preset + tokens)
  → audiomap.json (canonical beat analyzer) → STORYBOARD.md skeleton (frames tiled on the
  music, series/books assigned, HUD labels, seeded scene-pattern hints) → variant.json

  python3 new_variant.py variants/<name>.json            # scaffold
  python3 new_variant.py variants/<name>.json --force    # re-generate frame.md/STORYBOARD skeleton (keeps frames/)
  python3 new_variant.py variants/<name>.json --dry-run  # print the plan only

The seed changes which scene patterns / register order each frame gets, so the same books +
music can yield several genuinely different variants.
"""
import argparse, json, random, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gr_common import (ROOT, SHARED, VIDEOS, PY, M2V, SKILL, aspect_cfg, load_style,  # noqa: E402
                       render_tokens, load_books)

_FLAT = {  # see references/scene-patterns.md
    "intro": ["HOOK-SLAM", "HOOK-TYPE", "HOOK-MARQUEE"],
    "series": ["SERIES-TOSS", "MEGA-SPLIT", "COUNT-IN", "SHELF", "CARD-FLYBY", "GRID-SWAP"],
    "climax": ["CLIMAX-SLAM"],
    "finale": ["FINALE-BURST", "FINALE-STACK"],
}
STYLE_PATTERNS = {  # each style owns its own vocabulary, so styles never converge on the same moves
    "bold-beat": _FLAT,
    "editorial-gold": _FLAT,
    "soft-studio": {
        "intro": ["TYPE-WINDOW", "KV-PARALLAX", "HOOK-IN-SENTENCE"],
        "series": ["BOOK3D-OPEN", "BOOK3D-SPIN", "CHAT-UI", "CODE-UI", "OBJECT-IN-SENTENCE", "DEPTH-TYPE", "STAT-RING", "SHELF-PULL"],
        "climax": ["SLOGAN-WEIGHT"],
        "finale": ["SPINE-STACK", "SHELF-LOCKUP"],
    },
    "launch-keynote": {   # product-launch grammar: one sentence, one object, slow light
        "intro": ["COLD-LINE", "DARK-REVEAL"],
        "series": ["PRODUCT-TURN", "MACRO-PUSH", "DEVICE-PAIR", "LIVE-DOT", "QUIET-STAT"],
        "climax": ["HERO-LINE"],
        "finale": ["PRODUCT-LOCKUP"],
    },
    "paper-pop": {   # Japanese qualification-ad grammar in paper (references/scene-patterns.md § Paper-pop)
        "intro": ["COLD-OPEN-GRID", "TARGET-CALL", "BAT-CRACK"],
        "series": ["RED-SHEET", "PROGRESS-WALK", "TRI-PANEL", "SCORE-CARD", "BUBBLE-POP", "STEP-PILLS", "CHAT-BUBBLES"],
        "climax": ["TAPE-BACK"],
        "finale": ["SEARCH-CTA"],
    },
}
PATTERNS = _FLAT
REGISTERS = {"bold-beat": ["yellow", "ink", "paper"], "editorial-gold": ["ink", "gold"], "soft-studio": ["cream", "scene-tint", "ink"],
             "paper-pop": ["paper", "yellow", "navy"], "launch-keynote": ["night", "white"]}
TRANSITIONS = ["iris", "blinds", "wipe", "stripes"]
STYLE_TRANSITIONS = {"paper-pop": ["rings", "tear", "paper"]}
TREATMENT_AXES = ["style", "music", "palette", "transition", "camera", "hero", "hud"]


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"✗ {' '.join(map(str, cmd))}\n{r.stdout[-800:]}\n{r.stderr[-800:]}")
    return r.stdout


def roll_safe(t, rolls, tol=0.6):
    """Move t out of any hi-hat roll (frame boundaries must not split a roll)."""
    for r in rolls:
        if r["start"] < t < r["end"]:
            a, b = r["start"] - 0.05, r["end"] + 0.05
            nt = a if t - a <= b - t else b
            return nt if abs(nt - t) <= tol else None
    return t


def skeleton(am, n_series, min_len=3.0):
    D = am["audio"]["duration_sec"]
    bar = 240.0 / float(am.get("tempo", {}).get("bpm") or 120)
    # a "roll" longer than 4 bars is the track's groove (continuous hi-hats), not a fill — boundaries may cross it
    rolls = [r for r in am.get("rolls", []) if r["end"] - r["start"] <= 4 * bar]
    sils = am.get("silences", [])
    cand = set()
    for s in sils:
        cand.update([s["start"], s["end"]])
    cand.update(k["t"] for k in am.get("key_moments", []))
    cand.update(h["t"] if isinstance(h, dict) else h for h in am.get("hard_stops", []))
    cand.update(p["start"] for p in am.get("phrases", []))
    cand.update(am["grid"].get("downbeats_sec", []))
    cand = sorted({round(c2, 2) for c in cand if 2.5 < c < D - 2.5 for c2 in [roll_safe(c, rolls)] if c2 is not None})
    # intro end: first silence end in 12–30% of the track, else candidate nearest 20%
    intro_end = next((s["end"] for s in sils if 0.12 * D <= s["end"] <= 0.30 * D), None)
    intro_end = roll_safe(intro_end, rolls) if intro_end else None
    if intro_end is None or not (0.10 * D <= intro_end <= 0.32 * D):
        pool = [c for c in cand if 0.10 * D <= c <= 0.32 * D] or cand
        intro_end = min(pool, key=lambda c: abs(c - 0.2 * D))
    # finale start: last silence start in the last 25%, leaving ≥ 4s
    fin = [s["start"] for s in sils if 0.75 * D <= s["start"] <= D - 4]
    finale = roll_safe(fin[-1], rolls) if fin else None
    if finale is None or finale - intro_end < n_series * min_len:
        pool = [c for c in cand if intro_end + n_series * min_len <= c <= D - 4] or [D - 4.5]
        finale = min(pool, key=lambda c: abs(c - (D - 5.5)))
    bounds = [0.0, round(intro_end, 2)]
    span = finale - intro_end
    for i in range(1, n_series):
        ideal = intro_end + span * i / n_series
        opts = [c for c in cand if bounds[-1] + min_len <= c <= finale - min_len * (n_series - i)]
        bounds.append(round(min(opts, key=lambda c: abs(c - ideal)) if opts else ideal, 2))
    bounds += [round(finale, 2), round(D, 3)]
    return bounds


def describe(am, a, b):
    ph = [p for p in am["energy_phases"] if p["end"] > a and p["start"] < b]
    levels = "→".join(dict.fromkeys(p["level"] for p in ph))
    rolls = [r for r in am.get("rolls", []) if r["end"] > a and r["start"] < b]
    km = [f'{k["kind"]}@{k["t"]}' for k in am.get("key_moments", []) if a <= k["t"] < b]
    hits = [round(e["t"], 2) for e in am["events"] if a <= e["t"] < b and e["drum"] in ("kick", "snare") and e["energy"] >= 0.1]
    dense = sum(1 for p in ph if p.get("density") == "dense")
    pacing = "beat_cut" if (rolls or dense or len(hits) >= 2) else "phrase_flow"
    accel = any(r.get("kind") == "accel-roll" for r in rolls)
    feel = f"{levels} energy; {len(rolls)} roll(s){' incl. accel-roll' if accel else ''}; key {', '.join(km) or 'none'}; strong hits {hits[:10]}"
    peak = max((p.get("energy", 0) for p in ph), default=0)
    return pacing, feel, accel, peak, hits


def choose_patterns(roles, frames_info, books_per, rng, patterns=None, avoid=()):
    patterns = patterns or PATTERNS
    out, prev = [], None
    for i, role in enumerate(roles):
        pool = list(patterns["series" if role.startswith("series") else role])
        if role.startswith("series"):
            nb = books_per[i]
            if not frames_info[i]["accel"] and "CARD-FLYBY" in pool:
                pool.remove("CARD-FLYBY")
            if nb > 2 and "MEGA-SPLIT" in pool:
                pool.remove("MEGA-SPLIT")
            if not 3 <= nb <= 5 and "COUNT-IN" in pool:
                pool.remove("COUNT-IN")
            if nb < 4 and "GRID-SWAP" in pool:
                pool.remove("GRID-SWAP")
            if frames_info[i]["accel"] and "CARD-FLYBY" in pool:
                pool += ["CARD-FLYBY"]  # weight it up when the music literally accelerates
        rng.shuffle(pool)
        pool.sort(key=lambda p: (p in avoid or p in out))   # rationing: last variant's patterns and repeats go last
        pick = next((p for p in pool if p != prev), pool[0])
        if frames_info[i].get("climax"):
            pick = f"{pick} + {patterns['climax'][0]} (on the strongest surge)"
        out.append(pick)
        prev = pick
    return out


def treatment_of(spec, style):
    t = dict(spec.get("treatment", {}))
    t.setdefault("style", spec.get("style", "bold-beat"))
    t.setdefault("music", str(spec.get("bgm", {}).get("id", "?")))
    t.setdefault("palette", ",".join(f"{k}={v}" for k, v in sorted(spec.get("palette", {}).items())) or "preset")
    t.setdefault("transition", {"soft-studio": "shape", "paper-pop": "paper-shape"}.get(t["style"], "hard-cut"))
    t.setdefault("camera", {"soft-studio": "3d", "paper-pop": "2.5d-paper"}.get(t["style"], "flat"))
    t.setdefault("hero", {"soft-studio": "book3d", "bold-beat": "tossed-cover", "paper-pop": "paper-faces"}.get(t["style"], "cover-prop"))
    t.setdefault("hud", str(spec.get("hud", style.get("hud", {}).get("default", True))).lower())
    return t


def freshness(spec, style, name):
    """Compare this variant's treatment card with the most recent other variant; warn on ≥3 shared axes."""
    from gr_common import VARIANTS
    mine = treatment_of(spec, style)
    others = sorted((p for p in VARIANTS.glob("*.json") if p.stem not in (name, "_template")), key=lambda p: p.stat().st_mtime)
    if not others:
        return mine, set()
    prev = json.loads(others[-1].read_text())
    try:
        pstyle, _ = load_style(prev.get("style", "bold-beat"))
    except SystemExit:
        pstyle = {}
    theirs = treatment_of(prev, pstyle)
    same = [a for a in TREATMENT_AXES if mine.get(a) == theirs.get(a)]
    print(f"  treatment card vs '{others[-1].stem}': " + " · ".join(f"{a}={'=' if a in same else '≠'}" for a in TREATMENT_AXES))
    if len(same) >= 3:
        print(f"  ⚠ {len(same)} axes repeat the previous variant ({', '.join(same)}) — change at least two (style/music/transition/camera/hero) or the series will feel the same")
    prev_pats = set()
    for ph in (prev.get("resolved", {}) or {}).get("patterns", []):
        prev_pats.update(x.split(" (")[0].strip() for x in ph.split(" + "))
    pv = VIDEOS / prev.get("name", "") / "variant.json"
    if pv.exists():
        for ph in json.loads(pv.read_text()).get("resolved", {}).get("patterns", []):
            prev_pats.update(x.split(" (")[0].strip() for x in ph.split(" + "))
    return mine, prev_pats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    spec_path = Path(a.spec).resolve()
    spec = json.loads(spec_path.read_text())
    name = spec["name"]
    style_name = spec.get("style", "bold-beat")
    style, frame_tpl = load_style(style_name)
    asp = aspect_cfg(spec.get("aspect", "16:9"))
    fps = spec.get("fps", 30)
    books = load_books()
    rng = random.Random(spec.get("seed", 1))

    # ---- series / books
    series = spec.get("series", [])
    if not series:
        sys.exit("✗ spec.series is empty — list [{label,name,books:[isbn…]}]")
    for s in series:
        for i in s["books"]:
            if i not in books:
                sys.exit(f"✗ book {i} not in shared/books/books.json (run fetch_books.py --isbn {i})")
            if not books[i].get("cover"):
                sys.exit(f"✗ book {i} has no cover file")

    proj = VIDEOS / name
    print(f"▸ variant '{name}' · style {style_name} · {spec.get('aspect','16:9')} {asp['w']}×{asp['h']} · seed {spec.get('seed',1)}")
    if a.dry_run:
        print(json.dumps(spec, ensure_ascii=False, indent=2)); return

    # ---- project
    if not (proj / "hyperframes.json").exists():
        sh([("npx.cmd" if sys.platform == "win32" else "npx"), "-y", "hyperframes", "init", str(proj), "--non-interactive", "--example=blank", "--skill=music-to-video"])
        print(f"  ✓ hyperframes init {proj.relative_to(ROOT)}")
    for d in ("assets/covers", "assets/brand", "assets/fonts", "renders", "compositions/frames"):
        (proj / d).mkdir(parents=True, exist_ok=True)

    # ---- assets
    for s in series:
        for i in s["books"]:
            shutil.copy2(ROOT / books[i]["cover"], proj / "assets/covers" / f"{i}.jpg")
    for f in (SHARED / "brand").glob("*.png"):
        shutil.copy2(f, proj / "assets/brand" / f.name)
    for f in [*(SHARED / "fonts").glob("*.ttf"), *(SHARED / "fonts").glob("*.otf")]:
        shutil.copy2(f, proj / "assets/fonts" / f.name)
    extras = []
    if spec.get("faces"):   # paper-cut character faces (shared/characters/paper/<expr>/<slug>.png) → 512px + 160px crowd copies
        from PIL import Image
        fc = spec["faces"]
        for expr in fc.get("expressions", ["base", "worry", "happy"]):
            for f in sorted((SHARED / "characters/paper" / expr).glob("*.png")):
                for sub, px in ((expr, 512), (f"sm/{expr}", 160)):
                    if sub.startswith("sm/") and expr not in fc.get("crowd", ["worry", "happy"]):
                        continue
                    d = proj / "assets/faces" / sub / f.name
                    d.parent.mkdir(parents=True, exist_ok=True)
                    if not d.exists():
                        Image.open(f).resize((px, px), Image.LANCZOS).save(d, optimize=True)
        for f in fc.get("props", []):
            d = proj / "assets/props" / Path(f).name
            d.parent.mkdir(parents=True, exist_ok=True)
            if not d.exists():
                im = Image.open(SHARED / "characters/props" / f)
                im.thumbnail((768, 768), Image.LANCZOS)
                im.save(d, optimize=True)
        extras.append("assets/faces/{" + ",".join(fc.get("expressions", [])) + "}/<slug>.png — paper-cut character faces (512px; sm/ = 160px crowd copies)")
    for ex in spec.get("extra_assets", []):   # user-supplied visuals: [{"src": path, "dest": "assets/…", "role": "…"}]
        s = Path(ex["src"]).expanduser()
        s = s if s.is_absolute() else ROOT / s
        if not s.exists():
            sys.exit(f"✗ extra asset not found: {s}")
        d = proj / ex["dest"]
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        extras.append(f'{ex["dest"]} — {ex.get("role", "user-supplied visual")}')
    bg = spec["bgm"]
    src = SHARED / "bgm" / f'{bg["id"]}.mp3'
    if not src.exists():
        sys.exit(f"✗ shared/bgm/{bg['id']}.mp3 missing — bgm.py fetch {bg['id']}")
    dur = float(bg["duration"])
    fade = bg.get("fade", 1.0)
    if bg.get("segments"):
        # composed bed: optional silent pre-roll (cold open) + bar-aligned segments joined with a 12ms crossfade.
        # Cut points should sit on matching downbeats of repeated material (check chroma per bar first).
        segs, pre = bg["segments"], float(bg.get("preroll", 0))
        parts, labels = [], []
        for k, (a0, a1) in enumerate(segs):
            parts.append(f"[0]atrim=start={a0}:end={a1},asetpts=PTS-STARTPTS[s{k}]")
            labels.append(f"s{k}")
        chain, cur = [], labels[0]
        for k, lab in enumerate(labels[1:], 1):
            chain.append(f"[{cur}][{lab}]acrossfade=d=0.012:c1=tri:c2=tri[x{k}]")
            cur = f"x{k}"
        # real silent samples (adelay's leading silence is dropped by the MP3 encoder)
        sil = f"aevalsrc=0|0:d={pre}:s=44100:channel_layout=stereo[sil];[{cur}]afade=t=in:st=0:d=0.01[mus];[sil][mus]concat=n=2:v=0:a=1[cat]" if pre > 0 else f"[{cur}]anull[cat]"
        tail = sil + f";[cat]afade=t=out:st={max(0, dur - fade)}:d={fade}[out]"
        sh(["ffmpeg", "-loglevel", "error", "-y", "-i", str(src), "-filter_complex", ";".join(parts + chain + [tail]),
            "-map", "[out]", "-t", str(dur), "-c:a", "libmp3lame", "-b:a", "256k", str(proj / "assets/bgm.mp3")])
        desc = f"pre-roll {pre}s + " + " + ".join(f"[{a0}–{a1}]" for a0, a1 in segs)
    else:
        sh(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(bg["start"]), "-t", str(dur), "-i", str(src),
            "-af", f"afade=t=in:st=0:d=0.08,afade=t=out:st={max(0, dur - fade)}:d={fade}",
            "-c:a", "libmp3lame", "-b:a", "256k", str(proj / "assets/bgm.mp3")])
        desc = f"[{bg['start']}s +{dur}s]"
    print(f"  ✓ assets: {sum(len(s['books']) for s in series)} covers, logo, fonts, bgm {bg['id']} {desc}")

    # ---- audiomap
    if not PY.exists():
        sys.exit("✗ .venv missing — run scripts/setup.sh")
    sh([str(PY), str(M2V / "scripts/analyze-beatgrid.py"), str(proj / "assets/bgm.mp3"), "-o", str(proj / "audiomap.json")])
    am = json.loads((proj / "audiomap.json").read_text())
    D = am["audio"]["duration_sec"]
    print(f"  ✓ audiomap: {D}s · {am['tempo'].get('bpm')} BPM · {len(am.get('rolls',[]))} rolls · key moments {[(k['kind'],k['t']) for k in am.get('key_moments',[])][:6]}")

    # ---- frame.md from the style preset
    tokens = dict(style["tokens"])
    tokens.update(spec.get("palette", {}))
    tokens.update({"canvas_w": asp["w"], "canvas_h": asp["h"], "aspect": spec.get("aspect", "16:9"),
                   "safe_top": asp["content"][0], "safe_bottom": asp["content"][1], "side": asp["side"],
                   "hud_note": ("a separate HUD overlay (compositions/hud.html) owns the corner chrome and the bottom band — "
                                f"keep readable content in y {asp['content'][0]}–{asp['content'][1]}") if spec.get("hud", style.get("hud", {}).get("default", True))
                   else f"no HUD in this variant — keep readable content in y {asp['side']}–{asp['h'] - asp['side']}"})
    fm = proj / "frame.md"
    if a.force or not fm.exists() or "{{" in fm.read_text() or fm.stat().st_size < 400:
        fm.write_text(render_tokens(frame_tpl, tokens, asp["scale"]))
        print(f"  ✓ frame.md ← styles/{style_name} (scale {asp['scale']})")

    # ---- skeleton
    bounds = skeleton(am, len(series))
    roles = ["intro"] + [f"series{i}" for i in range(len(series))] + ["finale"]
    info = []
    for i in range(len(roles)):
        p, feel, accel, peak, hits = describe(am, bounds[i], bounds[i + 1])
        info.append({"pacing": p, "feel": feel, "accel": accel, "peak": peak, "hits": hits})
    mids = list(range(1, len(roles) - 1))
    if mids:
        info[max(mids, key=lambda i: info[i]["peak"])]["climax"] = True
    books_per = [0] + [len(s["books"]) for s in series] + [0]
    card, prev_pats = freshness(spec, style, name)
    pats = choose_patterns(roles, info, books_per, rng, STYLE_PATTERNS.get(style_name, PATTERNS), prev_pats)
    regs = REGISTERS.get(style_name, ["ink"])[:]
    # per-frame ground color + transition (shape-transition styles only)
    scene_colors, trans = [], []
    if card["transition"] != "hard-cut":
        from cover_palette import saturated_colors, mix, hexs
        from gr_common import hex_rgb
        base_hex = tokens.get("cream", tokens.get("paper", "#F4EFE6"))
        cream = hex_rgb(base_hex)
        for role in roles:
            if role.startswith("series"):
                cols = saturated_colors(ROOT / books[series[int(role[6:])]["books"][0]]["cover"])
                scene_colors.append(hexs(mix(cream, cols[0][1], 0.24)) if cols else base_hex)
            else:
                scene_colors.append(base_hex)
        last = None
        for i in range(len(roles)):
            if i == len(roles) - 1:
                trans.append("none"); break
            opts = [t for t in STYLE_TRANSITIONS.get(style_name, TRANSITIONS) if t != last]
            last = opts[rng.randrange(len(opts))]
            trans.append(last)
    rng.shuffle(regs)

    sb = proj / "STORYBOARD.md"
    if sb.exists() and not a.force and "TBD (Step 3)" not in sb.read_text():
        print("  • STORYBOARD.md already planned — kept (use --force to regenerate the skeleton)")
    else:
        L = ["---", "compositionId: bgm", f"duration_s: {D} # == audiomap.audio.duration_sec",
             f"canvas: {{ w: {asp['w']}, h: {asp['h']}, fps: {fps} }}", "mode: autonomous",
             f'message: "{spec.get("message", "골든래빗 — 시리즈별 대표 도서")}"',
             f"variant: {{ name: {name}, style: {style_name}, aspect: \"{spec.get('aspect','16:9')}\", seed: {spec.get('seed',1)}, intensity: {spec.get('intensity','standard')} }}",
             "style:", f'  font: "{style["font_line"]}"',
             f"  palette: {json.dumps([tokens[k] for k in style['palette_keys']])}",
             f"assets: \"assets/covers/<isbn>.jpg × {sum(len(s['books']) for s in series)}; assets/brand/icon.png (logo); assets/fonts/ Paperlogy"
             + "".join(f"; {e}" for e in extras) + "\"",
             "build_notes:",
             "  - \"follow references/worker-dispatch.md project notes (bare #stage, f<N>_ prefixes, no visibility:visible, transforms only)\"",
             f"  - \"{tokens['hud_note']}\"",
             f"  - \"register order hint for this seed: {' → '.join(regs)}\"",
             "avoid: [\"text over covers\", \"gradients/glows\", \"copying reference videos' copy or layouts\"]",
             "---", ""]
        for i, role in enumerate(roles):
            a0, a1 = bounds[i], bounds[i + 1]
            fid = f"f{i+1}"
            L += [f"## Frame {i+1} — {fid}", "",
                  f"- src: compositions/frames/{i+1:02d}-{fid}.html",
                  f"- duration: {round(a1 - a0, 3)}s",
                  f"- span_sec: [{a0}, {a1}]",
                  f"- pacing: {info[i]['pacing']}",
                  f"- mood: [{'hype' if info[i]['peak'] > 0.6 else 'cinematic'}]",
                  f"- feel: {info[i]['feel']}",
                  f"- role: {role}",
                  f"- pattern_hint: {pats[i]}"]
            if scene_colors:
                L += [f"- scene_color: {scene_colors[i]}", f"- transition_out: {trans[i]}"]
            if role.startswith("series"):
                s = series[int(role[6:])]
                L.append(f"- hud_label: {s['label']} · {s['name']}")
                for isbn in s["books"]:
                    b = books[isbn]
                    L.append(f"- book: {isbn} | {b.get('title','')} | {', '.join(b.get('authors', [])) or b.get('author_card','')} | {','.join(b.get('badges', []))} | assets/covers/{isbn}.jpg")
            if role == "intro":
                L.append(f"- copy_hint: {json.dumps(spec.get('copy', {}).get('hook', []), ensure_ascii=False)}")
            if role == "finale":
                L.append(f"- copy_hint: {json.dumps(spec.get('copy', {}).get('finale', {}), ensure_ascii=False)}")
            L += ["", "### Groups", "", "- TBD (Step 3)", ""]
        sb.write_text("\n".join(L))
        print("  ✓ STORYBOARD.md skeleton:")
        for i, role in enumerate(roles):
            print(f"      {i+1:02d} {role:8s} [{bounds[i]:6.2f} → {bounds[i+1]:6.2f}]  {info[i]['pacing']:11s} {pats[i]}")

    # ---- BRIEF + variant record
    br = proj / "BRIEF.md"
    if a.force or not br.exists() or "goldenrabbit-promo" not in br.read_text():
        br.write_text("\n".join([
            "---", "workflow: music-to-video", "flow: automation", f"storyboard: {spec.get('storyboard','no')}",
            f'message: "{spec.get("message", "골든래빗 — 시리즈별 대표 도서")}"',
            f"destination: {spec.get('destination','youtube')}", f"aspect: {asp['w']}x{asp['h']}", "language: ko",
            f"length: {D}s", "angle: kinetic-promo", "---", "",
            "## Intent", "", f"goldenrabbit-promo variant `{name}` (style {style_name}, seed {spec.get('seed',1)}). "
            "Built with the project skill .claude/skills/goldenrabbit-promo — principles in references/principles.md.", "",
            "## Assets", "", "- assets/covers/<isbn>.jpg — book covers from shared/books (goldenrabbit.co.kr)",
            "- assets/brand/icon.png — gold logo mark", *[f"- {e}" for e in extras], f"- assets/bgm.mp3 — shared/bgm/{bg['id']}.mp3 [{bg['start']}s +{dur}s] ({spec.get('bgm',{}).get('license','Mixkit Stock Music Free License')})", "",
            "## Notes", "", f"- {spec.get('notes','')}", ""]))
    rec = dict(spec)
    rec.setdefault("hud", spec.get("hud", style.get("hud", {}).get("default", True)))
    rec["resolved"] = {"duration": D, "bounds": bounds, "patterns": pats, "registers": regs, "project": str(proj.relative_to(ROOT)),
                       "treatment": card, "scene_colors": scene_colors, "transitions": trans}
    (proj / "variant.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2))
    print(f"  ✓ variant.json · next: plan groups in {sb.relative_to(ROOT)} (see SKILL.md step 5)")


if __name__ == "__main__":
    main()
