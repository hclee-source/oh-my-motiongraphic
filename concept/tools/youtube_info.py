"""업로드 정보(youtube.md)를 만든다: 제목 후보, 설명란(장 목록 시각은 timeline.json에서 자동), 태그. 본편과 쇼츠 둘 다.

사용(저장소 맨 위에서): python concept/tools/youtube_info.py <정보 JSON>
정보 JSON: {"<편 폴더>": {"titles": [...], "desc": "...", "hashtags": "#...", "tags": [...],
                         "shorts": {"titles": [...], "desc": "...", "tags": [...]}}}
"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def stamp(sec):
    s = max(0, int(sec))
    return f"{s // 60}:{s % 60:02d}"


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for folder, info in spec.items():
        ep = Path(folder)
        tl = json.loads((ep / "timeline.json").read_text(encoding="utf-8"))
        chapters = [f"{'0:00' if i == 0 else stamp(c['start'] - 0.45)} {c['title']}" for i, c in enumerate(tl["chapters"])]
        md = [f"# {ep.name.split('-')[0]} 업로드용 정보", "", "## 제목 (하나 고르기)", *[f"- {t}" for t in info["titles"]], "",
              "## 설명란", "", info["desc"], "", *chapters, "", info["hashtags"], "", "## 태그", ", ".join(info["tags"]), ""]
        if (ep / "thumbnail.png").exists():
            md += ["## 썸네일", "- 이 폴더의 thumbnail.png(완성본 폴더에도 같은 그림, 파일 이름 끝이 ‘-썸네일’)", ""]
        (ep / "youtube.md").write_text("\n".join(md), encoding="utf-8")
        s = info["shorts"]
        md = [f"# {ep.name.split('-')[0]} 쇼츠 업로드용 정보", "", "## 제목 (하나 고르기)", *[f"- {t}" for t in s["titles"]], "",
              "## 설명란", "", s["desc"], "", info["hashtags"], "", "## 태그", ", ".join(s["tags"]), "",
              "## 올릴 때", "- ‘관련 동영상’에 본편을 연결한다(공식 업로드 창구로는 지정할 수 없어 스튜디오에서 직접).", ""]
        (ep / "shorts" / "youtube.md").write_text("\n".join(md), encoding="utf-8")
        print("만듦:", ep / "youtube.md", "+ shorts")


if __name__ == "__main__":
    main()
