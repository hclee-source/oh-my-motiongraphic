#!/usr/bin/env bash
# Study a reference video BY EAR AND BY EYE (captions alone miss the visual demos — the
# music-only spans are exactly where the motion design is shown).
#   bash research_reference.sh <youtube-url> [slug]
# → research/<slug>/transcript.txt, reference.mp4, frames/sheet_NN.jpg (1 fps, 30 per sheet, timestamped)
set -euo pipefail
URL="$1"; ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
SLUG="${2:-$(yt-dlp --get-id "$URL" 2>/dev/null)}"
OUT="$ROOT/research/$SLUG"; mkdir -p "$OUT/frames"; cd "$OUT"
yt-dlp -q --skip-download --write-auto-subs --sub-langs "ko-orig,ko,en" --sub-format json3 -o "transcript.%(ext)s" "$URL" 2>/dev/null || true
J=$(ls transcript.*.json3 2>/dev/null | head -1 || true)
if [ -n "$J" ]; then
python3 - "$J" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1])); out = []
for ev in d.get("events", []):
    t = "".join(s.get("utf8", "") for s in ev.get("segs", [])).strip().replace("\n", " ")
    if t:
        ms = ev.get("tStartMs", 0); out.append(f"[{ms//60000:02d}:{(ms//1000)%60:02d}] {t}")
open("transcript.txt", "w").write("\n".join(out) + "\n")
mus = [l for l in out if "[음악]" in l or "[Music]" in l]
print(f"transcript: {len(out)} lines · {len(mus)} music-only cues (→ look at those spans in the frame sheets!)")
EOF
fi
yt-dlp -q -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" --merge-output-format mp4 -o "reference.%(ext)s" "$URL" 2>/dev/null
ffmpeg -loglevel error -y -i reference.mp4 -vf "fps=1,scale=320:180,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=13:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x5" -start_number 1 frames/sheet_%02d.jpg 2>/dev/null \
 || ffmpeg -loglevel error -y -i reference.mp4 -vf "fps=1,scale=320:180,tile=6x5" -start_number 1 frames/sheet_%02d.jpg
echo "✓ $OUT · $(ls frames | wc -l | tr -d ' ') sheets · sheet_NN covers (NN-1)×30s … NN×30s, 6 frames per row = 6 s (timestamps are burned in only if ffmpeg has drawtext)."
echo "  Read every sheet that covers a demo / music-only span (see the [음악] cues in transcript.txt)."
