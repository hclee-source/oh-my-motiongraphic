"""한 편의 본편과 쇼츠를 차례로 렌더하고, 소리 크기를 -14 LUFS로 맞춘 뒤 완성본/에 모은다.

사용(저장소 맨 위에서): python concept/tools/render_episode.py concept/episodes/<편> <제목> [--only main|shorts]
  예: python concept/tools/render_episode.py concept/episodes/002-roc-auc "ROC 곡선과 AUC"
결과: video/renders/<번호>-<제목>.mp4, shorts/video/renders/<번호>-<제목>-쇼츠.mp4
      + 완성본/<연-월>/<날짜> 개념 <번호> <제목>/ (concept/tools/collect_episode.py)
렌더 기록은 renders/render.log. 렌더 전에 배치 검사(check_layout)와 hyperframes check를 먼저 통과시킬 것.
"""
import argparse, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
NPX = "npx.cmd" if sys.platform == "win32" else "npx"


def render(video, final):
    r = video / "renders"
    r.mkdir(exist_ok=True)
    raw = r / "raw.mp4"
    with open(r / "render.log", "w", encoding="utf-8") as log:
        subprocess.run([NPX, "--yes", "hyperframes@0.8.214", "render", "-o", "renders/raw.mp4", "--workers", "2"],
                       cwd=video, check=True, stdout=log, stderr=subprocess.STDOUT)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(raw), "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", str(final)], check=True)
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(final)],
                         capture_output=True, text=True).stdout.strip()
    print(f"완성: {final.relative_to(ROOT)} ({float(dur):.1f}초)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("title")
    ap.add_argument("--only", choices=["main", "shorts"])
    a = ap.parse_args()
    ep = Path(a.episode).resolve()
    no = ep.name.split("-")[0]
    name = f"{no}-{a.title.replace(' ', '-')}"
    if a.only != "shorts":
        render(ep / "video", ep / "video" / "renders" / f"{name}.mp4")
    if a.only != "main":
        render(ep / "shorts" / "video", ep / "shorts" / "video" / "renders" / f"{name}-쇼츠.mp4")
    # 완성본의 영상 폴더로 모으기(썸네일·업로드 정보가 이미 있으면 함께)
    subprocess.run([sys.executable, str(ROOT / "concept" / "tools" / "collect_episode.py"), str(ep), a.title], check=True)


if __name__ == "__main__":
    main()
