#!/usr/bin/env bash
# 한 편(본편 + 쇼츠)을 조립하고 검사한다: 조립 → hyperframes check → 글자 배치 검사.
#   bash concept/tools/check_episode.sh concept/episodes/<편> [...]   (저장소 맨 위에서)
# 결과 요약만 찍는다. ‘확실’ 0건, 오류 0건이어야 렌더한다.
export PYTHONUTF8=1
PY=.venv/Scripts/python.exe
for E in "$@"; do
  echo "=== $E"
  for P in "$E" "$E/shorts"; do
    "$PY" concept/tools/build_video.py "$P" | tail -1
    (cd "$P/video" && npx --yes hyperframes@0.8.214 check 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -E "✗|Check passed|[1-9][0-9]* error" | head -12)
    node tools/check_layout.mjs "$P" 2>&1 | grep -E "^검사|^\[|확실" | head -12
  done
done
