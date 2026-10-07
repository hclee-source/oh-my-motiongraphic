#!/usr/bin/env bash
# One-time environment setup for the goldenrabbit-promo skill.
# - project-local Python venv (.venv) with librosa for beat analysis
# - HyperFrames workflow skills (music-to-video + core domains)
# - Chrome for headless snapshots/renders
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"

case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) VPY=.venv/Scripts/python.exe ;; *) VPY=.venv/bin/python ;; esac

if [ ! -x "$VPY" ]; then
  echo "▸ creating .venv (python 3.12 via uv)"
  uv venv -q --python 3.12 .venv
fi
echo "▸ installing librosa / numpy / soundfile / pillow"
uv pip install -q --python "$VPY" librosa numpy soundfile pillow
"$VPY" -c "import librosa, PIL; print('  librosa', librosa.__version__)"

echo "▸ refreshing HyperFrames skills (music-to-video + core)"
npx -y hyperframes skills update music-to-video >/dev/null 2>&1 && echo "  ok" || echo "  ⚠ skills update failed — run: npx hyperframes skills update music-to-video"

echo "▸ ensuring render browser"
npx -y hyperframes browser ensure >/dev/null 2>&1 && echo "  ok" || echo "  ⚠ run: npx hyperframes browser ensure"

for bin in ffmpeg ffprobe yt-dlp uv node; do
  command -v "$bin" >/dev/null && echo "  ✓ $bin" || echo "  ✗ missing: $bin"
done
echo "done. ROOT=$ROOT"
