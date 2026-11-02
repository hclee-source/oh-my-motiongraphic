"""다 만든 영상·썸네일·업로드 정보를 영상 하나당 폴더 하나로 모은다(올릴 파일 찾는 곳).

완성본/<연-월>/<날짜> <제목>/<이름> - <종류>.<확장자>
  예: 완성본/2026-10/2026-10-30 개념 002 ROC 곡선과 AUC/ROC 곡선과 AUC - 본편.mp4

사용(저장소 맨 위에서):
  python tools/save_final.py --title "개념 002 ROC 곡선과 AUC" --name "ROC 곡선과 AUC" 본편=<파일> 쇼츠=<파일> 썸네일=<파일> 정보=<글 파일> [--date 2026-10-30]
  python tools/save_final.py <파일> [<파일> ...]   (예전 방식: 제목·이름 = 파일 이름, 종류 없음)
- ‘정보’는 글 파일을 합쳐 ‘업로드 정보.txt’로 쓴다(여러 개면 순서대로 이어 붙임).
- 같은 제목의 폴더가 이미 있으면(날짜가 달라도) 그 폴더를 다시 쓰고, 같은 이름 파일은 새것으로 덮는다.
- 완성본/은 깃허브에 올리지 않는다(원본은 각 작업 폴더에).
"""
import argparse, datetime, re, shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BOX = ROOT / "완성본"
BAD = re.compile(r'[\\/:*?"<>|]')  # 윈도우 파일 이름에 못 쓰는 글자


def clean(s):
    return BAD.sub(" ", s).strip()


def folder_for(title, day):
    for p in sorted(BOX.glob(f"*/* {title}")):
        if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2} ", p.name):
            return p
    return BOX / f"{day:%Y-%m}" / f"{day.isoformat()} {title}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="+", help="종류=파일 또는 파일")
    ap.add_argument("--title")
    ap.add_argument("--name")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    day = datetime.date.fromisoformat(a.date)

    if not a.title:  # 예전 방식: 파일마다 제목 = 파일 이름
        for f in map(Path, a.items):
            if not f.is_file():
                sys.exit(f"파일이 없습니다: {f}")
            d = folder_for(clean(f.stem), day)
            d.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, d / f.name)
            print(f"모음: {(d / f.name).relative_to(ROOT)}")
        return

    title, name = clean(a.title), clean(a.name or a.title)
    d = folder_for(title, day)
    d.mkdir(parents=True, exist_ok=True)
    info = []
    for it in a.items:
        kind, _, path = it.partition("=")
        f = Path(path)
        if not f.is_file():
            print(f"건너뜀(파일 없음): {kind} {f}")
            continue
        if kind == "정보":
            info.append(f.read_text(encoding="utf-8").strip())
            continue
        dest = d / f"{name} - {kind}{f.suffix.lower()}"
        shutil.copy2(f, dest)
        print(f"모음: {dest.relative_to(ROOT)}")
    if info:
        (d / "업로드 정보.txt").write_text("\n\n────────────\n\n".join(info) + "\n", encoding="utf-8-sig")
        print(f"모음: {(d / '업로드 정보.txt').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
