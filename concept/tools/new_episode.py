"""새 편 폴더 뼈대를 001편에서 복사해 만든다(본편 video/ + 쇼츠 shorts/video/).

사용(저장소 맨 위에서): python concept/tools/new_episode.py <편 폴더 이름> <제목> [--sql]
  예: python concept/tools/new_episode.py 002-roc-auc "ROC 곡선과 AUC"
복사하는 것: 프로젝트 설정, 공용 틀(scene.css), 페이퍼로지 글꼴, 효과음. 장면·대본은 새로 쓴다.
--sql: SQL 편(SQLD)이면 SQL 카드·결과 표 모양(concept/tools/sql_scene.css)을 scene.css 끝에 붙인다.
"""
import datetime, json, shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

EPS = Path(__file__).resolve().parent.parent / "episodes"
BASE = EPS / "001-precision-recall"
FILES = ["hyperframes.json", "package.json", "CLAUDE.md", "AGENTS.md", "assets/scene.css"]


def skeleton(src, dst, meta_id, name):
    for f in FILES:
        if (src / f).exists():
            (dst / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src / f, dst / f)
    (dst / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    for f in (src / "assets" / "fonts").glob("Paperlogy-*.woff2"):
        shutil.copy2(f, dst / "assets" / "fonts" / f.name)
    shutil.copytree(src / "assets" / "sfx", dst / "assets" / "sfx", dirs_exist_ok=True)
    (dst / "compositions").mkdir(exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    (dst / "meta.json").write_text(json.dumps({"id": meta_id, "name": name, "createdAt": now}, ensure_ascii=False, indent=2),
                                   encoding="utf-8")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    folder, title = args[0], args[1]
    ep = EPS / folder
    if ep.exists():
        sys.exit(f"이미 있습니다: {ep}")
    no = folder.split("-")[0]
    skeleton(BASE / "video", ep / "video", "video", f"{no} {title}")
    skeleton(BASE / "shorts" / "video", ep / "shorts" / "video", "shorts", f"{no} {title} 쇼츠")
    if "--sql" in sys.argv:
        sql = (Path(__file__).resolve().parent / "sql_scene.css").read_text(encoding="utf-8")
        for v in (ep / "video", ep / "shorts" / "video"):
            with open(v / "assets" / "scene.css", "a", encoding="utf-8") as f:
                f.write(sql)
    print(f"만듦: {ep.relative_to(EPS.parent.parent)}")


if __name__ == "__main__":
    main()
