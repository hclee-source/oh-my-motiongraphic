"""timeline.json(문장별 음성 시각)을 읽어 영상 조립 파일을 만든다.

- video/index.html: 장면 배치(장면마다 문장 시작 시각 전달), 내레이션, 효과음, 영상 내내 떠 있는 겹침 장면
- video/compositions/captions.html: 문장 자막(긴 문장은 나눔)

사용(저장소 맨 위에서): python concept/tools/build_video.py concept/episodes/<편>   (쇼츠: .../<편>/shorts)
장면 목록·효과음 위치·화면 크기·자막 모양은 편 폴더의 build.json에서 읽는다.
build.json의 "format"을 비우면 본편(가로 1920×1080) 기본값.
"""
import html, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SFX_VOL = {"pop": 0.22, "click-soft": 0.3, "whoosh-short": 0.2, "chime": 0.18}
SFX_LEN = {"pop": 0.72, "click-soft": 0.37, "whoosh-short": 0.57, "chime": 2.5}

# 본편 기본값. 쇼츠는 build.json의 "format"으로 덮어쓴다.
FORMAT = {
    "width": 1920, "height": 1080, "resolution": "landscape",
    "caption": {"max": 28, "deep": False, "bottom": 108, "size": 46, "weight": 600, "width": 1536},
}

VARS = [
    ("color-ground", "color", "배경", "#F1F2F5"),
    ("color-card", "color", "카드", "#FFFFFF"),
    ("color-line", "color", "카드 테두리", "#E3E5EA"),
    ("color-hair", "color", "가는 선", "#D3D6DD"),
    ("color-dot", "color", "점(보통)", "#CDD0D8"),
    ("color-shadow", "color", "카드 그림자", "rgba(20,24,40,0.06)"),
    ("color-ink", "color", "글자", "#18181B"),
    ("color-ink2", "color", "보조 글자", "#71717A"),
    ("color-accent", "color", "강조색", "#6B3FE6"),
    ("color-accent-dark", "color", "어두운 카드 위 강조색", "#A68CFF"),
    ("color-anchor", "color", "수식 카드", "#18181B"),
    ("font-main", "string", "글꼴", "Paperlogy"),
]
FONT_FACES = "\n".join(
    f'      @font-face {{ font-family: "Paperlogy"; src: url("assets/fonts/Paperlogy-{f}.woff2") format("woff2"); font-weight: {w}; }}'
    for f, w in [("4Regular", 400), ("6SemiBold", 600), ("7Bold", 700), ("8ExtraBold", 800), ("9Black", 900)])

def split_caption(text, cap_max, deep=False):
    """긴 문장을 쉼표 또는 띄어쓰기에서 둘로 나눈다(양쪽 길이가 비슷하게). deep이면 나눈 조각도 길 때 다시 나눈다."""
    if len(text) <= cap_max:
        return [text]
    mid = len(text) / 2
    best = None
    for m in re.finditer(r", |\s", text):
        cut = m.end()
        score = abs(cut - mid) - (6 if m.group().startswith(",") else 0)
        if best is None or score < best[0]:
            best = (score, cut)
    if best is None:
        return [text]
    cut = best[1]
    if not deep:
        return [text[:cut].strip(), text[cut:].strip()]
    return split_caption(text[:cut].strip(), cap_max, True) + split_caption(text[cut:].strip(), cap_max, True)

def chapter_list(sc):
    ch = sc.get("chapter")
    if ch is None:
        return []
    return ch if isinstance(ch, list) else [ch]

def main():
    ep = Path(sys.argv[1])
    tl = json.loads((ep / "timeline.json").read_text(encoding="utf-8"))
    cfg = json.loads((ep / "build.json").read_text(encoding="utf-8"))
    if (ep / "word_times.json").exists():
        WORD_TIMES.update({k: v for k, v in json.loads((ep / "word_times.json").read_text(encoding="utf-8")).items()
                           if not k.startswith("_")})
    fmt = {**FORMAT, **cfg.get("format", {})}
    cap = {**FORMAT["caption"], **cfg.get("format", {}).get("caption", {})}
    W, H = fmt["width"], fmt["height"]
    total = tl["total"]
    chapters = {c["n"]: c for c in tl["chapters"]}
    half_gap = 0.45

    # 장면 배치
    hosts, starts = [], []
    for sc in cfg["scenes"]:
        chs = chapter_list(sc)
        if not chs:
            start = 0.0
        elif chs[0] == 1:
            start = max(0.0, tl["title_dur"] - 0.2)
        else:
            start = chapters[chs[0]]["start"] - half_gap
        starts.append(round(start, 3))
    for i, sc in enumerate(cfg["scenes"]):
        start = starts[i]
        end = starts[i + 1] if i + 1 < len(starts) else total
        sc["start"], sc["dur"] = start, round(end - start, 3)
        vals = {"dur": sc["dur"]}
        chs = chapter_list(sc)
        if chs:
            cues = [round(s["start"] - start, 3) for n in chs for s in chapters[n]["sentences"]]
            vals["cues"] = json.dumps(cues)
            vals["exit"] = sc.get("exit", True)
            sc["cues"] = cues
        if sc.get("extra"):
            for k, v in sc["extra"].items():
                vals[k] = eval_extra(v, chapters, start)
        hosts.append(
            f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["file"]}"\n'
            f'        data-start="{start}" data-duration="{sc["dur"]}" data-track-index="1" data-track-kind="graphics"\n'
            f'        data-width="{W}" data-height="{H}" style="z-index: 1"\n'
            f"        data-variable-values='{html.escape(json.dumps(vals, ensure_ascii=False), quote=False)}'></div>")

    # 영상 내내 떠 있는 겹침 장면(쇼츠 위쪽 제목 등)
    for ov in cfg.get("overlays", []):
        vals = {"dur": total}
        for k, v in ov.get("extra", {}).items():
            vals[k] = eval_extra(v, chapters, 0.0)
        hosts.append(
            f'      <div id="{ov["id"]}" data-composition-id="{ov["id"]}" data-composition-src="compositions/{ov["file"]}"\n'
            f'        data-start="0" data-duration="{total}" data-track-index="0" data-track-kind="graphics"\n'
            f'        data-width="{W}" data-height="{H}" style="z-index: 3"\n'
            f"        data-variable-values='{html.escape(json.dumps(vals, ensure_ascii=False), quote=False)}'></div>")

    # 효과음
    sfx_tags, n = [], 0
    by_id = {sc["id"]: sc for sc in cfg["scenes"]}
    events = []
    for sid, items in cfg.get("sfx", {}).items():
        sc = by_id[sid]
        for it in items:
            name, cue, off = it[0], it[1], it[2]
            events.append((sc["start"] + (sc["cues"][cue] if cue is not None else 0) + off, name))
    lane_end = {}  # 겹치는 효과음은 다른 트랙으로
    for t, name in sorted(events):
        dur = SFX_LEN.get(name, 1.0)
        lane = next(k for k in range(4, 20) if lane_end.get(k, -1) <= t)
        lane_end[lane] = t + dur
        n += 1
        sfx_tags.append(f'      <audio id="sfx-{n:03d}" class="clip" src="assets/sfx/{name}.mp3" data-start="{t:.3f}" '
                        f'data-duration="{dur}" data-track-index="{lane}" data-volume="{SFX_VOL.get(name, 0.25)}"></audio>')

    # 자막
    caps = []
    sents = [s for c in tl["chapters"] for s in c["sentences"]]
    for k, s in enumerate(sents):
        nxt = sents[k + 1]["start"] if k + 1 < len(sents) else total
        end = min(s["start"] + s["dur"] + 0.25, nxt - 0.05)
        # 대본에 ‘|’로 끊을 자리를 적었으면 그대로 따르고, 아니면 길이로 나눈다
        parts = [x.strip() for x in s["text"].split("|")] if "|" in s["text"] else split_caption(s["text"], cap["max"], cap["deep"])
        weights = [len(p.replace(" ", "")) for p in parts]
        # 조각이 바뀌는 시각: 잰 말 시각(word_times.json의 cap|문장|조각)이 있으면 그것, 없으면 글자 수 비례
        cuts = [s["start"]]
        for j in range(1, len(parts)):
            est = s["start"] + s["dur"] * sum(weights[:j]) / sum(weights)
            got = WORD_TIMES.get(f'cap|{s["n"]}|{j}')
            real = s["start"] + got - 0.05 if got is not None else None
            cuts.append(real if real is not None and cuts[-1] + 0.3 < real < end - 0.3 else est)
        cuts.append(end)
        t = s["start"]
        for j, p in enumerate(parts):
            span = cuts[j + 1] - cuts[j]
            caps.append(f'    <div id="cap-{s["n"]:02d}{"abcdefgh"[j]}" class="cap clip" data-start="{t:.3f}" data-duration="{span:.3f}"><span>{html.escape(p)}</span></div>')
            t += span

    var_json = "[\n" + ",\n".join(f'    {{"id":"{i}","type":"{t}","label":"{l}","default":"{d}"}}' for i, t, l, d in VARS) + "\n  ]"
    root_vars = "".join(f'        --{i}: {chr(34) + d + chr(34) if t == "string" else d};\n' for i, t, l, d in VARS)
    index = f"""<!doctype html>
<html
  lang="ko"
  data-resolution="{fmt["resolution"]}"
  data-composition-variables='{var_json}'
>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
{FONT_FACES}
      :root {{
{root_vars}      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: var(--color-ground); }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #bg {{ position: absolute; inset: 0; background: var(--color-ground); }}
    </style>
  </head>
  <body>
    <!-- tools/build_video.py가 만든 파일. 손으로 고치지 말고 build.json·timeline.json을 고친 뒤 다시 만든다. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
      <div id="bg"></div>
{chr(10).join(hosts)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{total}" data-track-index="2" data-track-kind="captions"
        data-width="{W}" data-height="{H}" style="z-index: 2"></div>
      <audio id="vo" class="clip" src="assets/vo/narration.wav" data-start="0" data-track-index="3" data-volume="1"></audio>
{chr(10).join(sfx_tags)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    captions = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: var(--font-main, "Paperlogy"), sans-serif; }}
    .cap {{ position: absolute; left: 0; right: 0; bottom: {cap["bottom"]}px; text-align: center; overflow: visible;
      font-size: {cap["size"]}px; font-weight: {cap["weight"]}; line-height: 1.35; letter-spacing: 0; color: var(--color-ink, #18181B); }}
    .cap span {{ display: inline-block; max-width: {cap["width"]}px; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
{chr(10).join(caps)}
  </div>
  <script>
    window.__timelines["captions"] = gsap.timeline({{ paused: true }});
  </script>
</template>
"""
    video = ep / "video"
    (video / "compositions").mkdir(parents=True, exist_ok=True)
    (video / "index.html").write_text(index, encoding="utf-8")
    (video / "compositions" / "captions.html").write_text(captions, encoding="utf-8")
    print(f"장면 {len(hosts)}개, 자막 {len(caps)}묶음, 효과음 {len(sfx_tags)}개, 전체 {total:.1f}초")

WORD_TIMES = {}  # 편 폴더의 word_times.json(받아 적기로 잰 실제 말 시각, verify_episode.py --write-times)

def eval_extra(spec, chapters, start):
    """build.json의 extra 값: {"sentence": 73, "at": "재현율"} → 그 낱말이 나오는 시각(장면 기준).
    word_times.json에 잰 시각이 있으면 그것을, 없으면 글자 수 비례로 추정한다."""
    s = next(x for c in chapters.values() for x in c["sentences"] if x["n"] == spec["sentence"])
    key = f'{spec["sentence"]}|{spec["at"]}'
    if key in WORD_TIMES and WORD_TIMES[key] <= s["dur"]:
        return round(s["start"] - start + WORD_TIMES[key], 3)
    pos = s["text"].find(spec["at"])
    frac = len(s["text"][:pos].replace(" ", "")) / max(1, len(s["text"].replace(" ", "")))
    return round(s["start"] - start + s["dur"] * frac, 3)

if __name__ == "__main__":
    main()
