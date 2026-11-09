"""공지 쇼츠·포스터 만들기: 공지 내용(JSON) → HyperFrames 프로젝트(쇼츠, 포스터 틀이 있는 종류는 포스터 1장도)
종류(type): lecture-event(특강 이벤트 15초 + 포스터), exam-check(시험 전 30초 점검)

사용:
  python notices/build_notice.py notices/data/<이름>.json
만들어지는 곳:
  videos/notice-<이름>/          쇼츠(세로 1080×1920)  → 렌더: 그 폴더에서 npx hyperframes render -o renders/<이름>.mp4
  videos/notice-<이름>/poster/   포스터               → npx hyperframes snapshot --at 0.5 로 PNG
요일은 날짜에서 계산한다(입력에 적지 않는다). 입력이 이상하면(지난 날짜, 안내가 특강보다 늦음, 줄이 너무 김) 경고한다.
"""
import datetime as dt
import html
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = Path(__file__).resolve().parent / "templates"
HF_VERSION = "0.8.214"
WEEK = "월화수목금토일"
DURATION = {"lecture-event": 15, "exam-check": 30, "exam-check-sql": 30}
SFX = {  # [이름, 시각, 길이, 음량, (소리 시작점)] — 음악 없이 효과음만 작게. 앞이 조용한 소리는 시작점(shared/sfx/peaks.json 최고점 직전)을 준다
    "lecture-event": [
        ["pop", 0.45, 0.6, 0.22], ["click-soft", 0.8, 0.37, 0.28],
        ["pop", 2.35, 0.6, 0.22], ["whoosh-short", 2.75, 0.57, 0.18],
        ["whoosh-short", 4.3, 0.57, 0.18], ["pop", 4.8, 0.6, 0.2], ["click-soft", 5.5, 0.37, 0.28],
        ["pop", 7.05, 0.6, 0.2], ["click-soft", 7.85, 0.37, 0.3], ["click-soft", 8.65, 0.37, 0.3], ["click-soft", 9.45, 0.37, 0.3],
        ["whoosh-short", 10.35, 0.57, 0.18], ["click", 11.25, 0.3, 0.3], ["typing", 11.65, 0.5, 0.25],
        ["pop", 12.0, 0.6, 0.2], ["pop", 12.5, 0.6, 0.18],
    ],
    "exam-check": [
        ["tick", 1.0, 0.09, 0.18], ["pop", 0.4, 0.6, 0.2], ["pop", 0.85, 0.6, 0.2], ["click-soft", 1.1, 0.37, 0.26], ["pop", 1.8, 0.6, 0.2], ["tick", 2.0, 0.09, 0.18],
        ["whoosh-short", 2.9, 0.57, 0.18], ["pop", 3.35, 0.6, 0.2], ["click-soft", 3.65, 0.37, 0.24], ["click-soft", 3.9, 0.37, 0.24],
        ["whoosh-short", 4.65, 0.57, 0.12], ["pop", 6.05, 0.6, 0.2], ["pop", 6.75, 0.6, 0.2], ["pop", 7.45, 0.6, 0.22],
        ["whoosh-short", 8.3, 0.57, 0.14], ["click", 9.65, 0.3, 0.28], ["click", 10.8, 0.3, 0.3], ["chime", 10.85, 1.2, 0.2, 0.36], ["pop", 12.25, 0.6, 0.18],
        ["whoosh-short", 14.85, 0.57, 0.18], ["pop", 15.35, 0.6, 0.2], ["click-soft", 15.65, 0.37, 0.24], ["click-soft", 15.9, 0.37, 0.24],
        ["click-soft", 16.85, 0.37, 0.26], ["pop", 18.05, 0.6, 0.2], ["error", 18.7, 0.7, 0.2, 0.6],
        ["pop", 19.95, 0.6, 0.2], ["chime", 20.5, 1.2, 0.22, 0.36], ["pop", 21.85, 0.6, 0.18], ["click", 23.0, 0.3, 0.28],
        ["whoosh-short", 25.85, 0.57, 0.18], ["pop", 26.25, 0.6, 0.2], ["pop", 26.5, 0.6, 0.2], ["sparkle", 26.85, 1.0, 0.18], ["ping", 29.0, 0.8, 0.16, 0.25],
    ],
}
# SQL판(2026-11-05): 장면 시각이 exam-check와 같아서 효과음도 그대로 쓴다. ① 표 칸이 채워지는 시각(6.0·6.7·7.4·7.85)에 pop이 맞는다
SFX["exam-check-sql"] = SFX["exam-check"] + [["pop", 7.9, 0.6, 0.18]]

def when(date_s, time_s):
    d = dt.date.fromisoformat(date_s)
    h, m = map(int, time_s.split(":"))
    ampm = "오전" if h < 12 else "오후"
    h12 = h % 12 or 12
    t = f"{ampm} {h12}시" + (f" {m}분" if m else "")
    wd = WEEK[d.weekday()]
    return d, f"{d.month}/{d.day}({wd})", t, wd

def words(text, box=None):
    out = []
    for w in text.split(" "):
        inner = html.escape(w)
        if box and w.startswith(box):
            inner = f'<span class="box">{html.escape(box)}</span>{html.escape(w[len(box):])}'
        out.append(f'<span class="w">{inner}</span>')
    return " ".join(out)

def sfx_html(items):
    """효과음 목록 → <audio> 태그. 항목 = [이름, 시각, 길이, 음량, (소리 시작점)]. 겹치는 소리는 다른 트랙에 놓는다."""
    ends, tags = [], []
    for i, it in enumerate(sorted(items, key=lambda x: x[1])):
        n, t, d, v = it[:4]
        ms = it[4] if len(it) > 4 else 0
        tr = next((k for k, e in enumerate(ends) if e <= t + 1e-6), len(ends))
        if tr == len(ends):
            ends.append(0)
        ends[tr] = t + d
        extra = f' data-media-start="{ms}"' if ms else ""
        tags.append(f'      <audio id="sfx-{i:02d}" class="clip" src="assets/sfx/{n}.mp3" data-start="{t}" data-duration="{d}"{extra} data-track-index="{4 + tr}" data-volume="{v}"></audio>')
    return "\n".join(tags)

def rich(text):
    """화면 글자 약식 표기: | = 줄바꿈, ^0.7 = 위첨자(빈칸이나 | 전까지), _0 = 아래첨자(한 글자)"""
    s = html.escape(text)
    s = re.sub(r"\^([^\s|&]+)", r"<sup>\g<1></sup>", s)   # 첨자를 먼저(줄바꿈 태그나 &lt; 같은 표기를 삼키지 않게)
    s = re.sub(r"_([0-9a-z])", r"<sub>\g<1></sub>", s)
    s = s.replace("|", "<br />")
    return s

def fill(template, values):
    s = template
    for k, v in values.items():
        s = s.replace("{{{" + k + "}}}", v)                 # 이미 만든 HTML
        s = s.replace("{{" + k + "}}", html.escape(v))      # 글자
    left = re.search(r"\{\{\{?[A-Z_0-9]+\}\}", s)
    if left:
        raise SystemExit(f"틀에 채우지 못한 자리: {left.group()}")
    return s

def project_files(dest, name, w, h, duration, comp_id, comp_file, sfx_tags=""):
    dest.mkdir(parents=True, exist_ok=True)
    for sub in ["compositions", "assets/fonts", "assets/sfx", "renders"]:
        (dest / sub).mkdir(parents=True, exist_ok=True)
    (dest / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": True}, "authoringSkill": "hyperframes"}, ensure_ascii=False, indent=2), encoding="utf-8")
    (dest / "package.json").write_text(json.dumps({
        "name": name, "private": True, "type": "module",
        "scripts": {k: f"npx --yes hyperframes@{HF_VERSION} {k if k != 'dev' else 'preview'}" for k in ["dev", "check", "render", "publish"]}},
        indent=2), encoding="utf-8")
    (dest / "meta.json").write_text(json.dumps({"id": name, "name": name}, ensure_ascii=False, indent=2), encoding="utf-8")
    fonts = "\n".join(
        f'      @font-face {{ font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-{f}.ttf") format("truetype"); font-weight: {wgt}; font-display: block; }}'
        for f, wgt in [("4Regular", 400), ("5Medium", 500), ("7Bold", 700), ("8ExtraBold", 800)])
    for f in ["4Regular", "5Medium", "7Bold", "8ExtraBold"]:
        shutil.copy(ROOT / "shared" / "fonts" / f"Paperlogy-{f}.ttf", dest / "assets" / "fonts")
    (dest / "index.html").write_text(f"""<!doctype html>
<html lang="ko" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={w}, height={h}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
{fonts}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {w}px; height: {h}px; overflow: hidden; background: #1E2687; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <!-- notices/build_notice.py가 만든 파일. 고칠 때는 notices/data의 입력이나 notices/templates의 틀을 고친 뒤 다시 만든다. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="{w}" data-height="{h}">
      <div id="{comp_id}-host" data-composition-id="{comp_id}" data-composition-src="compositions/{comp_file}"
        data-start="0" data-duration="{duration}" data-track-index="1" data-width="{w}" data-height="{h}"></div>
{sfx_tags}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")

def main():
    src = Path(sys.argv[1])
    data = json.loads(src.read_text(encoding="utf-8"))
    kind = data["type"]
    name = data["name"]
    warn = []

    if kind in ("exam-check", "exam-check-sql"):
        values = check_values(data, warn)
    else:
        values = lecture_values(data, warn)

    values["FONTFACES"] = "\n".join(
        f'    @font-face {{ font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-{f}.ttf") format("truetype"); font-weight: {wgt}; font-display: block; }}'
        for f, wgt in [("4Regular", 400), ("5Medium", 500), ("7Bold", 700), ("8ExtraBold", 800)])

    cover = ROOT / "shared" / "books" / "covers" / f"{data['book']}.jpg" if data.get("book") else None
    icon = ROOT / "shared" / "brand" / "icon.png"

    # 쇼츠
    dest = ROOT / "videos" / f"notice-{name}"
    dur = DURATION[kind]
    sfx_tags = sfx_html(SFX[kind])
    project_files(dest, f"notice-{name}", 1080, 1920, dur, "notice", "notice.html", sfx_tags)
    (dest / "compositions" / "notice.html").write_text(fill((TEMPLATES / f"{kind}.html").read_text(encoding="utf-8"), values), encoding="utf-8")
    for n in {s[0] for s in SFX[kind]}:
        shutil.copy(ROOT / "shared" / "sfx" / f"{n}.mp3", dest / "assets" / "sfx")
    if cover:
        shutil.copy(cover, dest / "assets" / "cover.jpg")
    shutil.copy(icon, dest / "assets" / "icon.png")
    shutil.copy(src, dest / "notice.json")

    # 포스터(틀이 있는 종류만)
    ptpl = TEMPLATES / f"{kind}-poster.html"
    if ptpl.exists():
        pdest = dest / "poster"
        project_files(pdest, f"notice-{name}-poster", 1080, 1920, 1, "poster", "poster.html")
        (pdest / "compositions" / "poster.html").write_text(fill(ptpl.read_text(encoding="utf-8"), values), encoding="utf-8")
        if cover:
            shutil.copy(cover, pdest / "assets" / "cover.jpg")
        shutil.copy(icon, pdest / "assets" / "icon.png")

    print(f"만듦: {dest}")
    for w in warn:
        print("  ⚠", w)

def check_values(data, warn):
    """시험 전 점검(exam-check): 훅 3줄 → ① 분포형 개념 → ② 계수 해석형 개념 → 마무리"""
    exam_d = dt.date.fromisoformat(data["exam_date"])
    if exam_d < dt.date.today():
        warn.append(f"시험 날짜 {data['exam_date']}가 이미 지났습니다")
    for line in data["hook"][:2] + data["outro"][:2]:
        if len(line.replace(" ", "")) > 12:
            warn.append(f"화면 한 줄이 깁니다(12자 넘음): {line}")
    if len(data["items"]) != 2:
        raise SystemExit(f"exam-check는 개념이 정확히 2개여야 합니다(지금 {len(data['items'])}개)")
    a, b = data["items"]
    box = data.get("hook_box")
    if box and not any(w.startswith(box) for w in data["hook"][2].split(" ")):
        warn.append(f"훅 강조 상자 ‘{box}’가 셋째 줄에 없습니다")
    v = {
        "HOOK1": words(data["hook"][0]), "HOOK2": words(data["hook"][1]), "HOOK3": words(data["hook"][2], data.get("hook_box")),
        "SUB": data["sub"],
        "I1_NO": a["no"], "I1_TOPIC": a["topic"], "I1_ASK1": rich(a["ask"][0]), "I1_ASK2": rich(a["ask"][1]),
        "I1_TIP": a["tip"],
        "I1_ANSWER": rich(a["answer"]), "I1_STAMP": rich(a["stamp"]), "I1_REVERSE": rich(a["reverse"]),
        "I2_NO": b["no"], "I2_TOPIC": b["topic"], "I2_ASK1": rich(b["ask"][0]), "I2_ASK2": rich(b["ask"][1]),
        "I2_FORMULA": rich(b["formula"]), "I2_LEAD": rich(b["lead"]), "I2_WRONG": rich(b["wrong"]), "I2_RIGHT": rich(b["right"]),
        "I2_NOTE": rich(b["note"]), "I2_KEY": rich(b["key"]),
        "OUT1": data["outro"][0], "OUT2": data["outro"][1], "OUT3": data["outro"][2], "CHEER": data["cheer"],
        "TIMER_DIGITS": "".join(f'<span class="dg" id="dg{k}">{k}</span>' for k in range(30, -1, -1)),
    }
    if data["type"] == "exam-check-sql":
        # ① 결과 표: table = {"head": [열 이름 셋], "rows": [[값 셋], ...]} — 마지막 행의 둘째·셋째 칸을 빨간 상자로
        t = a["table"]
        if len(t["rows"]) > 5:
            warn.append("① 표는 5행까지만 화면에 들어갑니다")
        h = [html.escape(str(x)) for x in t["head"]]
        out = [f'        <div class="tr th"><div class="c1">{h[0]}</div><div class="c2">{h[1]}</div><div class="c3">{h[2]}</div></div>']
        for i, row in enumerate(t["rows"]):
            c1, c2, c3 = (html.escape(str(x)) for x in row)
            last = i == len(t["rows"]) - 1
            out.append(f'        <div class="tr"><div class="c1">{c1}</div>'
                       f'<div class="c2"><span class="v {"c2b hl" if last else "c2a"}">{c2}</span></div>'
                       f'<div class="c3"><span class="v {"c3b hl" if last else "c3a"}">{c3}</span></div></div>')
        v["I1_TABLE"] = "\n".join(out)
    else:
        v.update({"I1_L1": a["marks"][0], "I1_L2": a["marks"][1], "I1_L3": a["marks"][2]})
    lec = data.get("lecture")
    if lec:
        lec_d, lec_md, lec_t, _ = when(lec["date"], lec["time"])
        if lec_d < dt.date.today():
            warn.append(f"마무리에 넣은 특강 {lec['date']}가 이미 지났습니다")
        v["FOOT"] = f"{lec['title']} · {lec_md} {lec_t}"
    else:
        v["FOOT"] = data.get("foot", "합격빠따")
    return v

def lecture_values(data, warn):
    lec_d, lec_md, lec_t, lec_wd = when(data["lecture"]["date"], data["lecture"]["time"])
    gd_d, gd_md, gd_t, _ = when(data["guide"]["date"], data["guide"]["time"])
    if lec_d < dt.date.today():
        warn.append(f"특강 날짜 {data['lecture']['date']}가 이미 지났습니다")
    if (gd_d, data["guide"]["time"]) > (lec_d, data["lecture"]["time"]):
        warn.append("참여 방법 안내 시각이 특강보다 늦습니다")
    for line in data["hook"] + data["title"] + data["targets"]:
        if len(line.replace(" ", "")) > 12:
            warn.append(f"화면 한 줄이 깁니다(12자 넘음): {line}")
    print(f"  특강 {lec_md} {lec_t} · 안내 {gd_md} {gd_t} {data['guide']['where']}")

    values = {
        "HOOK1": words(data["hook"][0]),
        "HOOK2": words(data["hook"][1], data.get("hook_box")),
        "TITLE1": data["title"][0], "TITLE2": data["title"][1], "EXAM": data["exam"],
        "CAL_TOP": f"{lec_d.year}년 {lec_d.month}월", "DAY": str(lec_d.day), "WEEKDAY_FULL": f"{lec_wd}요일",
        "TIME": lec_t, "LECTURE_SHORT": f"{lec_md} {lec_t}", "LECTURE_LONG": f"{lec_md} {lec_t}",
        "TARGET1": data["targets"][0], "TARGET2": data["targets"][1], "TARGET3": data["targets"][2],
        "TARGETL1": data["targets_long"][0], "TARGETL2": data["targets_long"][1], "TARGETL3": data["targets_long"][2],
        "COMMENT": data["join"]["comment"],
        "TYPED": "".join(f"<span>{html.escape(c)}</span>" for c in data["join"]["comment"]),
        "GUIDE": f"{gd_md} {gd_t} {data['guide']['where']}",
    }
    return values

if __name__ == "__main__":
    main()
