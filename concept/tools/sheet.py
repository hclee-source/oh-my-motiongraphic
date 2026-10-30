"""장마다 끝나기 직전 화면을 한 장씩 찍어 한 장짜리 모음(contact sheet)으로 만든다. 렌더 전 눈 확인용.

사용(저장소 맨 위에서): python concept/tools/sheet.py concept/episodes/<편> [--shorts] [--extra 12.5,40]
결과: <영상 폴더>/boards/review/sheet.jpg
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--shorts", action="store_true")
    ap.add_argument("--extra", default="")
    a = ap.parse_args()
    ep = Path(a.episode) / ("shorts" if a.shorts else "")
    video = ep / "video"
    tl = json.loads((ep / "timeline.json").read_text(encoding="utf-8"))
    times = [round(c["end"] - 0.4, 2) for c in tl["chapters"]]
    times += [float(x) for x in a.extra.split(",") if x]
    times = sorted(set(times))
    out = video / "snapshots"
    shutil.rmtree(out, ignore_errors=True)
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    subprocess.run([npx, "--yes", "hyperframes@0.8.214", "snapshot", "--at", ",".join(map(str, times)), "--no-end", "-o", "snapshots"],
                   cwd=video, check=True, capture_output=True)
    pngs = sorted(out.glob("*.png"))
    review = video / "boards" / "review"
    review.mkdir(parents=True, exist_ok=True)
    cols = 5 if not a.shorts else 4
    rows = -(-len(pngs) // cols)
    w = 384 if not a.shorts else 270
    inputs = []
    for p in pngs:
        inputs += ["-i", str(p)]
    n = len(pngs)
    filt = "".join(f"[{i}:v]scale={w}:-2[v{i}];" for i in range(n))
    filt += "".join(f"[v{i}]" for i in range(n)) + f"xstack=inputs={n}:layout="
    h = int(w * (1080 / 1920 if not a.shorts else 1920 / 1080))
    filt += "|".join(f"{(i % cols) * w}_{(i // cols) * h}" for i in range(n)) + ":fill=white"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", filt, str(review / "sheet.jpg")], check=True)
    print(review / "sheet.jpg", "·", ", ".join(map(str, times)))


if __name__ == "__main__":
    main()
