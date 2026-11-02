"""한 편의 본편·쇼츠·썸네일·업로드 정보를 완성본의 영상 폴더 하나로 모은다(tools/save_final.py 사용).

사용(저장소 맨 위에서): python concept/tools/collect_episode.py concept/episodes/<편> "<제목>" [--date 2026-10-30]
  → 완성본/<연-월>/<날짜> 개념 <번호> <제목>/<제목> - 본편.mp4 · - 쇼츠.mp4 · - 썸네일.png · 업로드 정보.txt
최종 영상은 renders/<번호>-<제목>.mp4(쇼츠는 -쇼츠)를 먼저 찾고, 없으면 renders 안에서 한글 이름인 가장 새 mp4를 쓴다.
"""
import argparse, re, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
HANGUL = re.compile(r"[가-힣]")


def final_mp4(renders, expected):
    if (renders / expected).is_file():
        return renders / expected
    cands = [p for p in renders.glob("*.mp4") if HANGUL.search(p.stem)]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("title")
    ap.add_argument("--date")
    a = ap.parse_args()
    ep = Path(a.episode).resolve()
    no = ep.name.split("-")[0]
    base = f"{no}-{a.title.replace(' ', '-')}"
    items = []
    main_v = final_mp4(ep / "video" / "renders", f"{base}.mp4")
    short_v = final_mp4(ep / "shorts" / "video" / "renders", f"{base}-쇼츠.mp4")
    for kind, p in [("본편", main_v), ("쇼츠", short_v), ("썸네일", ep / "thumbnail.png"),
                    ("정보", ep / "youtube.md"), ("정보", ep / "shorts" / "youtube.md")]:
        if p and Path(p).is_file():
            items.append(f"{kind}={p}")
    cmd = [sys.executable, str(ROOT / "tools" / "save_final.py"), "--title", f"개념 {no} {a.title}", "--name", a.title, *items]
    if a.date:
        cmd += ["--date", a.date]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
