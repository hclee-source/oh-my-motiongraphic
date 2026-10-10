#!/usr/bin/env bash
# Render a checked variant at delivery quality, verify it, build a contact sheet and record
# the output in variants/<name>.json.
#   bash finalize.sh videos/<name> [draft|delivery]
set -euo pipefail
PROJ="$(cd "$1" && pwd)"; Q="${2:-delivery}"; SDIR="$(cd "$(dirname "$0")" && pwd)"
NAME="$(basename "$PROJ")"; ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
# a working python (on Windows `python3` can be the Microsoft Store stub that only prints "Python" and exits)
PY=python3; "$PY" -c "import sys" >/dev/null 2>&1 || PY=python
FPS=$(grep -oE 'fps: *[0-9]+' "$PROJ/STORYBOARD.md" | head -1 | grep -oE '[0-9]+' || echo 30)
OUT="renders/$NAME.mp4"
cd "$PROJ"
npx hyperframes check . >/tmp/gr_check_$$.log 2>&1 || { sed 's/\x1b\[[0-9;]*m//g' /tmp/gr_check_$$.log | grep -E "✗|error" | head -20; echo "✗ check failed — fix before rendering"; exit 1; }
npx hyperframes render . --skill=music-to-video -q "$Q" -o "$OUT" --fps "$FPS" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | tail -3
# Loudness: two-pass loudnorm to -14 LUFS / -1.5 dBTP (YouTube reference) so every cut plays at the same level
# (renders varied from -18.4 to -12.0 LUFS before this). Video stream is copied untouched. Skip with GR_LOUDNORM=0.
if [ "${GR_LOUDNORM:-1}" != "0" ]; then
  LN=$(ffmpeg -hide_banner -i "$OUT" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  ARGS=$(printf '%s' "$LN" | "$PY" -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
  ffmpeg -loglevel error -y -i "$OUT" -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:$ARGS,aresample=48000" -c:a aac -b:a 192k "${OUT%.mp4}.ln.mp4"
  mv -f "${OUT%.mp4}.ln.mp4" "$OUT"
  LUFS=$(ffmpeg -hide_banner -i "$OUT" -af ebur128 -f null - 2>&1 | grep -E '^\s+I:' | tail -1 | tr -s ' ')
  echo "  loudness →${LUFS}"
fi
# One-frame glitch scan on the delivered file (findings are advisory; read each POP)
"$PY" "$SDIR/pop_scan.py" "$PROJ" "$OUT" || true
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
EXP=$("$PY" -c "import json;print(json.load(open('audiomap.json'))['audio']['duration_sec'])")
AUD=$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$OUT")
ffmpeg -loglevel error -y -i "$OUT" -vf "fps=1/($EXP/20),scale=384:-2,tile=5x4" -frames:v 1 renders/contact-sheet.jpg
"$PY" - "$ROOT" "$NAME" "$PROJ/$OUT" "$DUR" "$Q" <<'EOF'
import json, sys, datetime
from pathlib import Path
root, name, out, dur, q = sys.argv[1:]
p = Path(root) / "variants" / f"{name}.json"
if p.exists():
    d = json.loads(p.read_text())
    d.setdefault("outputs", []).append({"file": str(Path(out).relative_to(root)), "duration": float(dur), "quality": q,
                                        "rendered": datetime.datetime.now().isoformat(timespec="seconds")})
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
EOF
echo "✓ $PROJ/$OUT · ${DUR}s (expected ${EXP}s) · audio=${AUD:-MISSING} · sheet renders/contact-sheet.jpg"
