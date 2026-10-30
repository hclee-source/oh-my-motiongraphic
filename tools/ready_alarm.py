"""평일 아침 알림: 완성본/에 새로 들어온 파일(올릴 영상·포스터)이 있으면 윈도우 알림으로 알려 준다.

작업 스케줄러 '합격빠따 영상 알림'이 평일 09:00에 실행한다(그 시각에 컴퓨터가 꺼져 있었으면 켤 때 실행).
이미 알린 파일은 완성본/.알림기록.json에 적어 두고 다시 알리지 않는다. 새 파일이 없으면 알리지 않는다.
알림을 누르면 완성본 폴더가 열린다.

사용(저장소 맨 위에서): python tools/ready_alarm.py [--dry]   (--dry: 알림·기록 없이 목록만 보기)
"""
import argparse, datetime, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOX = ROOT / "완성본"
LOG = BOX / ".알림기록.json"
sys.path.insert(0, str(ROOT / "notices"))
from notify import notify  # noqa: E402

VIDEO = {".mp4", ".mov"}
IMAGE = {".png", ".jpg", ".jpeg"}


def main():
    if sys.stdout:  # pythonw로 돌 때는 출력 창이 없다
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {"알린 파일": [], "기록": []}
    seen = set(log["알린 파일"])
    files = sorted(p for p in BOX.glob("*/*") if p.suffix.lower() in VIDEO | IMAGE) if BOX.exists() else []
    new = [p for p in files if p.relative_to(BOX).as_posix() not in seen]
    if not new:
        if sys.stdout:
            print("새로 준비된 파일 없음")
        return

    videos = [p for p in new if p.suffix.lower() in VIDEO]
    images = [p for p in new if p.suffix.lower() in IMAGE]
    title = f"합격빠따 · 올릴 영상 {len(videos)}개 준비됨" + (f" (포스터 {len(images)}장)" if images else "")
    names = [p.stem[11:] or p.stem for p in videos or images]  # 앞의 날짜(2026-10-30_)를 뗀 이름
    body = " · ".join(names[:3]) + (f" 외 {len(names) - 3}개" if len(names) > 3 else "")
    if sys.stdout:
        print(title)
        for p in new:
            print(" ", p.relative_to(ROOT))
    if a.dry:
        return

    notify(title, body, BOX)
    log["알린 파일"] = sorted(seen | {p.relative_to(BOX).as_posix() for p in new})
    log["기록"].append({"시각": datetime.datetime.now().isoformat(timespec="seconds"),
                       "파일": [p.relative_to(BOX).as_posix() for p in new]})
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
