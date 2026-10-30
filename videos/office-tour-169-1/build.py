"""사무실 투어 영상 조립: 인형 코드를 장면에 넣고, 자산을 복사하고, 효과음이 든 index.html을 만든다.
사용: python videos/office-tour-169-1/build.py
"""
import json, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DUR = 42

def main():
    tpl = (HERE / "src" / "tour.tpl.html").read_text(encoding="utf-8")
    js = (ROOT / "shared" / "characters" / "puppets" / "ppatta-duo.js").read_text(encoding="utf-8")
    (HERE / "compositions" / "tour.html").write_text(tpl.replace("/*PUPPETS*/", js), encoding="utf-8")

    a = HERE / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True); (a / "sfx").mkdir(exist_ok=True)
    for f in ["Paperlogy-8ExtraBold.ttf", "Paperlogy-5Medium.ttf"]:
        shutil.copy(ROOT / "shared" / "fonts" / f, a / "fonts")
    covers = {"adsp": "9791194383697", "bigdata": "9791124516317", "bigdata2": "9791124516539", "comhwal1": "9791124516614", "comhwal2": "9791124516638"}
    for k, isbn in covers.items():
        shutil.copy(ROOT / "shared" / "books" / "covers" / f"{isbn}.jpg", a / f"cover-{k}.jpg")
    shutil.copy(ROOT / "shared" / "brand" / "icon.png", a / "icon.png")

    # 효과음: [이름, 시각, 길이, 음량]
    sfx = [["ping", 0.45, 1.3, 0.35], ["whoosh-short", 0.6, 0.57, 0.15],
           ["pop", 6.45, 0.6, 0.3], ["whoosh-short", 7.6, 0.57, 0.18], ["tock", 8.35, 0.1, 0.35],
           ["click", 13.9, 0.3, 0.3], ["pop", 14.2, 0.6, 0.2], ["sparkle", 14.4, 1.2, 0.15], ["pop", 15.55, 0.6, 0.22],
           ["pop", 22.2, 0.6, 0.25], ["whoosh-short", 29.3, 0.57, 0.2], ["sparkle", 30.85, 1.2, 0.25],
           ["pop", 37.55, 0.6, 0.25], ["sparkle", 37.75, 1.2, 0.3], ["chime", 38.6, 2.5, 0.25]]
    # 수험생 발소리: tour.tpl.html의 walk()와 같은 계산(0.32초 보폭)
    walks = [(1.5, 2.4), (3.8, 9.25), (9.8, 13.8), (17.0, 21.73), (23.93, 28.66), (32.46, 37.28)]
    for t0, t1 in walks:
        n = max(2, round((t1 - t0) / 0.32)); d = (t1 - t0) / n
        for i in range(n):
            sfx.append(["tick" if i % 2 else "tock", round(t0 + i * d, 3), 0.1, 0.12])
    used = sorted({x[0] for x in sfx})
    for n in used:
        shutil.copy(ROOT / "shared" / "sfx" / f"{n}.mp3", a / "sfx")
    sfx.sort(key=lambda x: x[1])
    lanes, tags = {}, []
    for i, (n, t, d, v) in enumerate(sfx):
        lane = next(k for k in range(3, 30) if lanes.get(k, -1) <= t)
        lanes[lane] = t + d
        tags.append(f'      <audio id="sfx-{i:03d}" class="clip" src="assets/sfx/{n}.mp3" data-start="{t}" data-duration="{d}" data-track-index="{lane}" data-volume="{v}"></audio>')

    (HERE / "index.html").write_text(f"""<!doctype html>
<html lang="ko" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-8ExtraBold.ttf") format("truetype"); font-weight: 800; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #FFF1C8; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <!-- build.py가 만든 파일. src/tour.tpl.html이나 build.py를 고친 뒤 다시 만든다. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      <div id="tour-host" data-composition-id="tour" data-composition-src="compositions/tour.html"
        data-start="0" data-duration="{DUR}" data-track-index="1" data-width="1920" data-height="1080"></div>
{chr(10).join(tags)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")
    for f, body in [("hyperframes.json", (ROOT / "videos" / "notice-adsp-51-lecture" / "hyperframes.json").read_text(encoding="utf-8")),
                    ("package.json", json.dumps({"name": "office-tour-169-1", "private": True, "type": "module",
                        "scripts": {k: f"npx --yes hyperframes@0.8.214 {'preview' if k == 'dev' else k}" for k in ["dev", "check", "render"]}}, indent=2)),
                    ("meta.json", json.dumps({"id": "office-tour-169-1", "name": "빠따 캐릭터 사무실 투어"}, ensure_ascii=False, indent=2))]:
        (HERE / f).write_text(body, encoding="utf-8")
    print(f"만듦: 효과음 {len(tags)}개(발소리 포함), {DUR}초")

if __name__ == "__main__":
    main()
