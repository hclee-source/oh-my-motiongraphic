"""다 만든 영상(올릴 파일)을 완성본 폴더 한곳에 모은다.

사용(저장소 맨 위에서): python tools/save_final.py <파일> [<파일> ...] [--date 2026-10-30]
  → 완성본/<연-월>/<날짜>_<파일 이름> 으로 복사한다. 날짜를 안 주면 오늘.
  같은 날 같은 이름이면 새것으로 덮는다(같은 날 다시 렌더한 경우).
  다른 날짜에 같은 이름의 복사본이 있으면 지우지 않고 알려만 준다.
완성본/은 깃허브에 올리지 않는다(원본은 각 작업 폴더의 renders/).
"""
import argparse, datetime, shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BOX = ROOT / "완성본"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    day = datetime.date.fromisoformat(a.date)

    for f in map(Path, a.files):
        if not f.is_file():
            sys.exit(f"파일이 없습니다: {f}")
        out_dir = BOX / f"{day:%Y-%m}"
        out_dir.mkdir(parents=True, exist_ok=True)
        dest = out_dir / f"{day.isoformat()}_{f.name}"
        shutil.copy2(f, dest)
        print(f"모음: {dest.relative_to(ROOT)}")
        older = [p for p in BOX.glob(f"*/*_{f.name}") if p != dest and p.name[10:] == dest.name[10:]]
        for p in sorted(older):
            print(f"  같은 이름의 예전 것도 있습니다: {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
