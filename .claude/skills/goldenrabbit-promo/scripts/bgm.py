#!/usr/bin/env python3
"""Royalty-free BGM library for promo variants (Mixkit Stock Music Free License:
commercial use OK, no attribution required — re-check https://mixkit.co/license/ before shipping).

All state lives in shared/bgm/catalog.json; audio files in shared/bgm/<id>.mp3.

  bgm.py search --tags upbeat,electronic,house [--genre EDM] [--min 80]   # list candidates
  bgm.py fetch 470 1062                                                    # download mp3s
  bgm.py analyze 470 1062        # bpm, onset pulse, 5s energy profile   (needs .venv / librosa)
  bgm.py vocal 470               # whisper tiny.en word count (vocals → avoid for kinetic type)
  bgm.py windows 470 --length 30 # best start/end windows on bar lines, ending on a strong hit
  bgm.py cut 470 --start 34.99 --dur 46.6 --out videos/<name>/assets/bgm.mp3
  bgm.py list                    # catalog table
"""
import argparse, json, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
LIB = ROOT / "shared" / "bgm"
CAT = LIB / "catalog.json"
PY = ROOT / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
ANALYZER = Path.home() / ".claude/skills/music-to-video/scripts/analyze-beatgrid.py"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"}


def load():
    return json.loads(CAT.read_text()) if CAT.exists() else {}


def save(c):
    LIB.mkdir(parents=True, exist_ok=True)
    CAT.write_text(json.dumps(c, ensure_ascii=False, indent=2))


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return r.read()


def cmd_search(a):
    cat = load()
    rows = {}
    for tag in a.tags.split(","):
        page = get(f"https://mixkit.co/free-stock-music/tag/{tag.strip()}/").decode("utf-8", "ignore")
        for m in re.finditer(r'\{"@id":"[^"]+","@type":"MusicRecording","name":"([^"]+)","genre":"([^"]*)","byArtist":"([^"]*)","duration":"PT(?:(\d+)M)?(\d+)S","url":"(https://assets\.mixkit\.co/music/(\d+)/\d+\.mp3)"', page):
            name, genre, artist, mi, se, url, tid = m.groups()
            dur = int(mi or 0) * 60 + int(se)
            r = rows.setdefault(tid, {"id": tid, "title": name.encode().decode("unicode_escape", "ignore") if "\\u" in name else name,
                                      "genre": genre.replace("\\u0026", "&"), "artist": artist, "duration": dur, "url": url,
                                      "source": "mixkit", "license": "Mixkit Stock Music Free License", "tags": []})
            r["tags"].append(tag.strip())
    for tid, r in rows.items():
        cat.setdefault(tid, {}).update({k: v for k, v in r.items() if k != "tags"})
        cat[tid]["tags"] = sorted(set(cat[tid].get("tags", []) + r["tags"]))
    save(cat)
    sel = [r for r in rows.values() if r["duration"] >= a.min and (not a.genre or a.genre.lower() in r["genre"].lower())]
    for r in sorted(sel, key=lambda r: (r["genre"], r["title"])):
        mark = "↓" if (LIB / f'{r["id"]}.mp3').exists() else " "
        print(f'{mark} {r["id"]:>5}  {r["duration"]:4d}s  {r["genre"][:20]:20s}  {r["title"][:32]:32s}  {r["artist"][:22]}')
    print(f"{len(sel)} candidates (↓ = already downloaded) · catalog: {CAT.relative_to(ROOT)}")


def cmd_fetch(a):
    cat = load()
    for tid in a.ids:
        dest = LIB / f"{tid}.mp3"
        if not dest.exists():
            url = cat.get(tid, {}).get("url") or f"https://assets.mixkit.co/music/{tid}/{tid}.mp3"
            dest.write_bytes(get(url))
        cat.setdefault(tid, {"id": tid, "source": "mixkit", "license": "Mixkit Stock Music Free License"})
        cat[tid]["file"] = str(dest.relative_to(ROOT))
        print(f"✓ {tid} → {dest.relative_to(ROOT)}")
    save(cat)


def _need_venv():
    if not PY.exists():
        sys.exit("✗ .venv missing — run: bash .claude/skills/goldenrabbit-promo/scripts/setup.sh")


def cmd_analyze(a):
    _need_venv()
    cat = load()
    code = r'''
import sys, json, librosa, numpy as np
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
oenv = librosa.onset.onset_strength(y=y, sr=sr)
rms = librosa.feature.rms(y=y)[0]; t = librosa.times_like(rms, sr=sr)
seg = [float(np.mean(rms[(t >= s) & (t < s + 5)])) for s in range(0, int(t[-1]), 5)]
mx = max(seg) or 1
print(json.dumps({"duration": round(len(y) / sr, 2), "bpm": round(float(np.atleast_1d(tempo)[0]), 1),
  "pulse": round(float(np.mean(librosa.util.normalize(oenv))), 3),
  "energy5s": "".join(" .:-=+*#%@"[min(9, int(9 * v / mx))] for v in seg)}))
'''
    for tid in a.ids:
        f = LIB / f"{tid}.mp3"
        if not f.exists():
            print(f"✗ {tid}: not downloaded (bgm.py fetch {tid})"); continue
        out = subprocess.run([str(PY), "-c", code, str(f)], capture_output=True, text=True)
        try:
            res = json.loads(out.stdout.strip().splitlines()[-1])
        except Exception:  # noqa: BLE001
            print(f"✗ {tid}: {out.stderr[-300:]}"); continue
        cat.setdefault(tid, {"id": tid}).update(res)
        r = cat[tid]
        print(f'{tid:>5}  {r.get("title","")[:24]:24s} dur={res["duration"]:6.1f}  bpm={res["bpm"]:6.1f}  pulse={res["pulse"]:.3f}  energy/5s=[{res["energy5s"]}]')
    save(cat)
    print("pulse > 0.09 + steady bpm 115–135 suits word-per-beat kinetic type.")


def cmd_vocal(a):
    cat = load()
    import tempfile
    for tid in a.ids:
        f = LIB / f"{tid}.mp3"
        with tempfile.TemporaryDirectory() as td:
            wav = Path(td) / "a.wav"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(f), "-ar", "16000", "-ac", "1", str(wav)], check=True)
            subprocess.run(["npx", "hyperframes", "transcribe", str(wav), "-d", td, "-m", "tiny.en", "--json"], capture_output=True, text=True)
            tj = Path(td) / "transcript.json"
            words = []
            if tj.exists():
                d = json.loads(tj.read_text())
                w = d if isinstance(d, list) else d.get("words", d.get("segments", []))
                words = [x.get("text", "") for x in w if isinstance(x, dict)]
        real = [w for w in words if re.search(r"[A-Za-z]{2,}", w or "")]
        cat.setdefault(tid, {"id": tid})["vocal_words"] = len(real)
        verdict = "instrumental ✓" if len(real) <= 3 else f"VOCALS ({len(real)} words) — avoid under kinetic type"
        print(f"{tid:>5}  {verdict}  sample: {' '.join(real[:8])}")
    save(cat)


def full_audiomap(tid):
    f = LIB / f"{tid}.mp3"
    am = LIB / f"{tid}.audiomap.json"
    if not am.exists():
        _need_venv()
        subprocess.run([str(PY), str(ANALYZER), str(f), "-o", str(am)], check=True, capture_output=True)
    return json.loads(am.read_text())


def cmd_windows(a):
    d = full_audiomap(a.id)
    dur = d["audio"]["duration_sec"]
    downs = d["grid"].get("downbeats_sec") or d["grid"]["beats_sec"][::4]
    hits = [e for e in d["events"] if e["drum"] in ("kick", "snare") and e["energy"] >= 0.12]
    phases = d["energy_phases"]

    def energy_at(t):
        for p in phases:
            if p["start"] <= t < p["end"]:
                return p.get("energy", 0)
        return 0

    sils = d.get("silences", [])
    cands = []
    for s in downs:
        for h in hits:
            L = h["t"] - s
            if not (a.length * 0.9 <= L <= a.length * 1.1):
                continue
            # prefer: quieter start (room for a hook), a strong last hit followed by lower energy, a silence inside the last third (finale breath)
            score = (1 - energy_at(s + 0.5)) * 1.0 + h["energy"] * 2.0 + (1 - energy_at(h["t"] + 1.2)) * 0.8
            score += 0.6 if any(s + L * 0.6 < x["start"] < h["t"] for x in sils) else 0
            score -= abs(L - a.length) / a.length
            cands.append((round(score, 3), round(s, 2), round(h["t"], 2), round(L + a.tail, 2)))
    cands.sort(reverse=True)
    seen = []
    print(f"track {a.id}: {dur:.1f}s · {d['tempo'].get('bpm')} BPM · target {a.length}s (+{a.tail}s tail)")
    for sc, s, e, L in cands:
        if any(abs(s - x) < 3 for x in seen):
            continue
        seen.append(s)
        print(f"  score {sc:5.2f}  start {s:6.2f}  last-hit {e:6.2f}  → cut --start {s} --dur {L}")
        if len(seen) >= a.top:
            break
    if not seen:
        print("  no window found — relax --length or pick another track")


def cmd_cut(a):
    f = LIB / f"{a.id}.mp3"
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fo = max(0.0, a.dur - a.fade)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a.start), "-t", str(a.dur), "-i", str(f),
                    "-af", f"afade=t=in:st=0:d=0.08,afade=t=out:st={fo}:d={a.fade}", "-c:a", "libmp3lame", "-b:a", "256k", str(out)], check=True)
    print(f"✓ {out} ({a.dur}s from {a.start}s of {a.id})")


def cmd_list(a):
    for tid, r in sorted(load().items(), key=lambda kv: kv[0]):
        mark = "↓" if (LIB / f"{tid}.mp3").exists() else " "
        print(f'{mark} {tid:>5}  {r.get("title","?")[:24]:24s} {r.get("genre","")[:12]:12s} {r.get("duration","?")!s:>6}s  bpm={r.get("bpm","-")}  pulse={r.get("pulse","-")}  vocal={r.get("vocal_words","?")}  [{r.get("energy5s","")}]')


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("search"); p.add_argument("--tags", default="upbeat,electronic,house"); p.add_argument("--genre", default=""); p.add_argument("--min", type=int, default=60); p.set_defaults(fn=cmd_search)
    p = sp.add_parser("fetch"); p.add_argument("ids", nargs="+"); p.set_defaults(fn=cmd_fetch)
    p = sp.add_parser("analyze"); p.add_argument("ids", nargs="+"); p.set_defaults(fn=cmd_analyze)
    p = sp.add_parser("vocal"); p.add_argument("ids", nargs="+"); p.set_defaults(fn=cmd_vocal)
    p = sp.add_parser("windows"); p.add_argument("id"); p.add_argument("--length", type=float, default=45); p.add_argument("--tail", type=float, default=0.8); p.add_argument("--top", type=int, default=5); p.set_defaults(fn=cmd_windows)
    p = sp.add_parser("cut"); p.add_argument("id"); p.add_argument("--start", type=float, required=True); p.add_argument("--dur", type=float, required=True); p.add_argument("--fade", type=float, default=1.0); p.add_argument("--out", required=True); p.set_defaults(fn=cmd_cut)
    p = sp.add_parser("list"); p.set_defaults(fn=cmd_list)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
