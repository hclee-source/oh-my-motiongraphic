#!/usr/bin/env bash
# Render a checked variant at delivery quality, verify it, build a contact sheet and record
# the output in variants/<name>.json.
#   bash finalize.sh videos/<name> [draft|delivery]
set -euo pipefail
PROJ="$(cd "$1" && pwd)"; Q="${2:-delivery}"
NAME="$(basename "$PROJ")"; ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
FPS=$(grep -oE 'fps: *[0-9]+' "$PROJ/STORYBOARD.md" | head -1 | grep -oE '[0-9]+' || echo 30)
OUT="renders/$NAME.mp4"
cd "$PROJ"
npx hyperframes check . >/tmp/gr_check_$$.log 2>&1 || { sed 's/\x1b\[[0-9;]*m//g' /tmp/gr_check_$$.log | grep -E "✗|error" | head -20; echo "✗ check failed — fix before rendering"; exit 1; }
npx hyperframes render . --skill=music-to-video -q "$Q" -o "$OUT" --fps "$FPS" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | tail -3
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
EXP=$(python3 -c "import json;print(json.load(open('audiomap.json'))['audio']['duration_sec'])")
AUD=$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$OUT")
ffmpeg -loglevel error -y -i "$OUT" -vf "fps=1/($EXP/20),scale=384:-2,tile=5x4" -frames:v 1 renders/contact-sheet.jpg
python3 - "$ROOT" "$NAME" "$PROJ/$OUT" "$DUR" "$Q" <<'EOF'
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
