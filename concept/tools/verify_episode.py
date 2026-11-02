"""완성된 한 편(본편·쇼츠)을 코드로 검증한다: 소리 신호, 최종 영상의 박자·잡음, 화면 번쩍임, (있으면) 받아 적기 대조.

사용(저장소 맨 위에서): python concept/tools/verify_episode.py concept/episodes/<편> [...] [--write-times] [--no-pops]
  받아 적기 결과(<프로젝트>/listen/words.json, listen_episode.py)가 있으면 대본 대조·그림·자막 시각 대조도 한다.
  --words: <폴더>/<편 이름>[-shorts].*.words.json(받아 적은 낱말 [시작, 끝, 낱말])이 있으면 대본 대조·시각 대조도 한다.

검사
 1) 내레이션(narration.wav): 소리 찢어짐(꽉 찬 표본), 문장 끝 잘림(마지막 20ms가 큼), 문장 안 긴 멈춤(0.7초 넘게 조용),
    말 빠르기(음절/초)가 그 편 가운데값에서 크게 벗어난 문장(빠뜨리거나 덧붙여 읽은 의심), 문장 사이 쉼이 완전히 조용한지.
 2) 최종 영상(renders/<번호>-<제목>.mp4): 내레이션과 박자 어긋남(처음·끝 30초에서 따로 재서 밀림까지),
    효과음도 말도 없는 구간의 잡음·‘딱’ 소리, 가장 큰 소리.
 3) 화면 번쩍임: 앞뒤 프레임과 모두 다른 한 프레임(pop_scan.py와 같은 기준).
 4) 받아 적기(있을 때): 문장마다 읽어야 할 말과 받아 적은 말의 일치도, 그림 시각(build.json extra)·자막 나눔이 실제 말 시각과 얼마나 다른지.
"""
import argparse, difflib, html, json, re, subprocess, sys
from pathlib import Path
import numpy as np
import soundfile as sf

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from say_auto import WORDS  # noqa: E402

SR = 48000


# ───────── 숫자 → 한자어 읽기(음절 수·대조용) ─────────
DIG = "영일이삼사오육칠팔구"
def sino(n):
    if n == 0:
        return "영"
    out, units = "", [(10000, "만"), (1000, "천"), (100, "백"), (10, "십")]
    for u, name in units:
        q, n = divmod(n, u)
        if q:
            out += ("" if q == 1 and u != 10000 else sino(q) if u == 10000 else DIG[q]) + name
    return out + (DIG[n] if n else "")

def read_digits(s):
    s = re.sub(r"(\d+)\.(\d+)", lambda m: sino(int(m.group(1))) + "점" + "".join(DIG[int(c)] for c in m.group(2)), s)
    return re.sub(r"\d+", lambda m: sino(int(m.group(0))), s)

INV = sorted(((k.upper(), v) for k, v in WORDS.items()), key=lambda kv: -len(kv[0]))
NATIVE = {"한": 1, "두": 2, "세": 3, "네": 4, "다섯": 5, "여섯": 6, "일곱": 7, "여덟": 8, "아홉": 9, "열": 10,
          "열한": 11, "열두": 12, "스무": 20}
COUNT = "행|명|개|묶음|가지|번|등|점|분|건|장"
def norm(s):
    """대조용: 고유어 수+단위는 숫자로 바꾼 뒤 모든 숫자를 한자어로, 영어 SQL 낱말은 한글 소리로, 한글만 남긴다.
    받아 적기는 ‘여덟 행’을 ‘8 행’, ‘셀렉트’를 ‘SELECT’처럼 적기도 하므로 양쪽을 같은 꼴로 맞춘다."""
    s = s.upper()
    for k, v in INV:
        s = re.sub(rf"(?<![A-Z_]){re.escape(k)}(?![A-Z_])", v, s)
    s = re.sub(rf"(?<![가-힣])({'|'.join(sorted(NATIVE, key=len, reverse=True))})\s*({COUNT})",
               lambda m: f"{NATIVE[m.group(1)]}{m.group(2)}", s)
    s = read_digits(s)
    s = s.replace("셋째", "세째")
    return fold(re.sub(r"[^가-힣]", "", s))


# 소리가 같은 모음은 하나로: ㅔ→ㅐ, ㅖ→ㅒ, ㅚ·ㅞ→ㅙ (‘해빙/헤빙’, ‘웨어/외어’를 같은 말로 본다)
VFOLD = {5: 1, 7: 3, 11: 10, 15: 10}
def fold(s):
    out = []
    for c in s:
        k = ord(c) - 0xAC00
        if 0 <= k < 11172:
            l, v, t = k // 588, (k % 588) // 28, k % 28
            c = chr(0xAC00 + l * 588 + VFOLD.get(v, v) * 28 + t)
        out.append(c)
    return "".join(out)


def rms_db(x):
    r = float(np.sqrt(np.mean(np.square(x, dtype=np.float64)))) if len(x) else 0.0
    return 20 * np.log10(r + 1e-12)


def frames_db(x, win):
    n = len(x) // win
    if n == 0:
        return np.array([])
    f = x[: n * win].reshape(n, win).astype(np.float64)
    return 20 * np.log10(np.sqrt((f ** 2).mean(axis=1)) + 1e-12)


def load_audio(path):
    if path.suffix.lower() == ".wav":
        x, sr = sf.read(path, dtype="float32")
    else:
        # ffmpeg의 -ac 1은 두 채널을 더해 1을 넘길 수 있으므로, 채널 그대로 받아 평균 낸다
        ch = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=channels",
                                 "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip() or 1)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ar", str(SR), "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        x, sr = np.frombuffer(raw, dtype=np.float32).reshape(-1, ch), SR
    if x.ndim > 1:
        x = x.mean(axis=1)
    assert sr == SR, f"표본률 {sr}"
    return x


def sentences(tl):
    return [s for c in tl["chapters"] for s in c["sentences"]]


# ───────── 1) 내레이션 ─────────
def check_narration(proj, tl, out):
    x = load_audio(proj / "video/assets/vo/narration.wav")
    clip = int((np.abs(x) >= 0.999).sum())
    if clip:
        out.append(("확실", f"내레이션에 꽉 찬 표본 {clip}개(소리 찢어짐)"))
    ss = sentences(tl)
    rates = []
    for s in ss:
        a, b = int(s["start"] * SR), int((s["start"] + s["dur"]) * SR)
        seg = x[a:b]
        say = re.sub(r"\s*\|\s*", " ", s["say"])
        syl = len(re.sub(r"[^가-힣]", "", read_digits(say)))
        fdb = frames_db(seg, int(0.02 * SR))
        peak = fdb.max() if len(fdb) else -120
        # 말 빠르기는 쉼표·마침표에서 쉬는 시간을 빼고 소리가 나는 시간으로 잰다
        voiced = max(0.1, float((fdb > peak - 35).sum()) * 0.02)
        rate = syl / voiced
        rates.append(rate)
        # 문장 끝 잘림: 마지막 20ms가 문장 최대보다 25dB 이상 작지 않으면 말이 끊긴 채 끝난 것
        tail = rms_db(seg[-int(0.02 * SR):])
        if tail > peak - 25:
            out.append(("의심", f"{s['n']}번 문장 끝이 잘렸을 수 있음(마지막 20ms {tail:.0f}dB, 최대 {peak:.0f}dB) — {s['text'][:30]}"))
        head = rms_db(seg[: int(0.01 * SR)])
        if head > peak - 25:
            out.append(("의심", f"{s['n']}번 문장 시작이 잘렸을 수 있음(처음 10ms {head:.0f}dB) — {s['text'][:30]}"))
        # 문장 안 긴 멈춤
        quiet = fdb < peak - 40
        run, best = 0, 0
        for q in quiet:
            run = run + 1 if q else 0
            best = max(best, run)
        # 쉼표·마침표가 없는데 0.7초 넘게 멈추거나, 있어도 1.5초 넘게 멈추면 이상
        inner = len(re.findall(r"[,.?!]", say.rstrip(" .?!")))
        if (best * 0.02 > 0.7 and inner == 0) or best * 0.02 > 1.5:
            out.append(("의심", f"{s['n']}번 문장 안에 {best * 0.02:.1f}초 멈춤 — {s['text'][:30]}"))
        s["_rate"] = rate
    med = float(np.median(rates))
    for s in ss:
        r = s["_rate"]
        if r < med * 0.75 or r > med * 1.3:
            out.append(("의심", f"{s['n']}번 말 빠르기 {r:.1f}음절/초(소리 나는 시간 기준, 가운데값 {med:.1f}) — "
                                f"빠뜨리거나 덧붙여 읽었는지 확인: {s['text'][:34]}"))
    # 문장 사이 쉼은 완전히 조용해야 한다
    edges = [(0.0, ss[0]["start"])] + [(p["start"] + p["dur"], q["start"]) for p, q in zip(ss, ss[1:])] + \
            [(ss[-1]["start"] + ss[-1]["dur"], tl["total"])]
    # 시각은 0.001초로 반올림돼 있으므로 양 끝 2ms는 빼고, 문장 꼬리에 남겨 둔 -50dB 아래 숨소리 수준은 허용
    m = int(0.002 * SR)
    loud = [(a, b) for a, b in edges if b - a > 0.01 and np.abs(x[int(a * SR) + m: int(b * SR) - m]).max(initial=0) > 10 ** (-50 / 20)]
    if loud:
        out.append(("의심", f"문장 사이 쉼에 소리가 남은 곳 {len(loud)}군데(처음 {loud[0][0]:.2f}초)"))
    return x, med


# ───────── 2) 최종 영상 소리 ─────────
def sfx_windows(proj):
    idx = (proj / "video/index.html").read_text(encoding="utf-8")
    win = []
    for m in re.finditer(r'<audio id="sfx-\d+"[^>]*data-start="([\d.]+)"[^>]*data-duration="([\d.]+)"', idx):
        a, d = float(m.group(1)), float(m.group(2))
        win.append((a, a + d))
    return win


def env(x, hop):
    n = len(x) // hop
    return np.abs(x[: n * hop]).reshape(n, hop).max(axis=1)


def offset_ms(a, b, t0, span=30.0, maxlag=0.5):
    """b(최종)가 a(내레이션)보다 몇 ms 늦은지: 1ms 단위 포락선 상관."""
    hop = SR // 1000
    i0, i1 = int(t0 * SR), int((t0 + span) * SR)
    ea, eb = env(a[i0:i1], hop), env(b[i0:i1], hop)
    n = min(len(ea), len(eb))
    ea, eb = ea[:n] - ea[:n].mean(), eb[:n] - eb[:n].mean()
    L = int(maxlag * 1000)
    best, lag = -1e18, 0
    for k in range(-L, L + 1):
        v = float(np.dot(ea[max(0, -k): n - max(0, k)], eb[max(0, k): n - max(0, -k)]))
        if v > best:
            best, lag = v, k
    return lag


def check_final(proj, tl, narr, mp4, out):
    if not mp4 or not mp4.exists():
        out.append(("확실", "최종 영상이 없음"))
        return
    y = load_audio(mp4)
    dur = len(y) / SR
    if abs(dur - tl["total"]) > 0.2:
        out.append(("의심", f"최종 소리 길이 {dur:.2f}초 ≠ 내레이션 {tl['total']:.2f}초"))
    # 박자: 처음과 끝에서 각각
    first = offset_ms(narr, y, 0.0, min(30.0, tl["total"] / 2))
    last = offset_ms(narr, y, max(0.0, tl["total"] - 31.0), 30.0)
    tag = "확실" if max(abs(first), abs(last)) > 60 else "참고"
    out.append((tag, f"최종 영상 소리가 내레이션보다 처음 {first:+d}ms, 끝 {last:+d}ms 밀림"))
    clip = int((np.abs(y) >= 0.999).sum())
    if clip:
        out.append(("확실", f"최종 영상에 꽉 찬 표본 {clip}개"))
    # 말도 효과음도 없는 구간은 조용해야 한다(최종본은 소리 크기를 키웠으므로 -45dB 기준)
    ss = sentences(tl)
    busy = [(s["start"] - 0.05, s["start"] + s["dur"] + 0.05) for s in ss] + [(a - 0.03, b + 0.3) for a, b in sfx_windows(proj)]
    busy.sort()
    free, t = [], 0.0
    for a, b in busy:
        if a > t + 0.1:
            free.append((t, a))
        t = max(t, b)
    if dur > t + 0.1:
        free.append((t, dur))
    noisy = []
    for a, b in free:
        seg = y[int(a * SR): int(b * SR)]
        if not len(seg):
            continue
        pk = 20 * np.log10(np.abs(seg).max() + 1e-12)
        if pk > -45:
            k = int(np.abs(seg).argmax())
            noisy.append((a + k / SR, pk))
    for t0, pk in noisy[:6]:
        out.append(("의심", f"말·효과음 없는 구간 {t0:.2f}초에 소리 {pk:.0f}dB(잡음·딱 소리 의심)"))
    if len(noisy) > 6:
        out.append(("의심", f"… 같은 곳 {len(noisy) - 6}군데 더"))


# ───────── 3) 화면 번쩍임 ─────────
def check_pops(mp4, out, w=64, h=36):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    f = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h * w).astype(np.int16)
    d = np.abs(np.diff(f, axis=0)).mean(axis=1)          # d[i] = |f[i+1]-f[i]|
    skip = np.abs(f[2:] - f[:-2]).mean(axis=1)            # |f[i+2]-f[i]|
    n = 0
    for i in range(1, len(f) - 1):
        dp, dn, ds = d[i - 1], d[i], skip[i - 1]
        lo, hi = max(0, i - 15), min(len(d), i + 15)
        med = float(np.median(d[lo:hi])) + 0.3
        if dp >= 3 * med and dn >= 3 * med and min(dp, dn) >= 4 and ds < 0.5 * min(dp, dn):
            n += 1
            if n <= 5:
                out.append(("의심", f"화면 번쩍임 {i / 30:.2f}초(한 프레임만 앞뒤와 다름, Δ{min(dp, dn):.1f})"))
    return len(f)


# ───────── 4) 받아 적기 대조 ─────────
def check_words(proj, tl, words, out, detail):
    ss = sentences(tl)
    low = []
    for s in ss:
        a, b = s["start"] - 0.15, s["start"] + s["dur"] + 0.15
        got = "".join(w[2] for w in words if a <= (w[0] + w[1]) / 2 <= b)
        want = re.sub(r"\s*\|\s*", " ", s["say"])
        r = difflib.SequenceMatcher(None, norm(want), norm(got)).ratio()
        s["_heard"], s["_ratio"] = got.strip(), r
        if r < 0.86:
            low.append(s)
    for s in low:
        out.append(("확인", f"{s['n']}번 일치 {s['_ratio']:.2f} — 읽을 말: {re.sub(r'[|]', '', s['say'])} / 받아 적음: {s['_heard']}"))
    detail["ratios"] = [round(s["_ratio"], 2) for s in ss]
    times = {}
    # 그림 시각(extra)과 실제 말 시각: 조립된 index.html에 실제로 들어간 값과 비교한다
    cfg = json.loads((proj / "build.json").read_text(encoding="utf-8"))
    idx = (proj / "video/index.html").read_text(encoding="utf-8")
    built = {}
    for m in re.finditer(r'<div id="([^"]+)" data-composition-id="[^"]+"[^>]*?data-start="([\d.]+)"[^>]*?data-variable-values=\'([^\']*)\'', idx, re.S):
        built[m.group(1)] = (float(m.group(2)), json.loads(html.unescape(m.group(3))))
    byn = {s["n"]: s for s in ss}
    for sc in cfg["scenes"]:
        for k, spec in (sc.get("extra") or {}).items():
            s = byn.get(spec["sentence"])
            if not s:
                continue
            pos = s["text"].find(spec["at"])
            est = s["start"] + s["dur"] * len(s["text"][:pos].replace(" ", "")) / max(1, len(s["text"].replace(" ", "")))
            if sc["id"] in built and k in built[sc["id"]][1]:
                est = built[sc["id"]][0] + float(built[sc["id"]][1][k])
            real = locate(words, s, spec["at"], est)
            if real is None:
                out.append(("참고", f"{sc['id']}.{k}: ‘{spec['at']}’을 받아 적기에서 못 찾음(글자 수 추정 그대로)"))
                continue
            times[f"{s['n']}|{spec['at']}"] = round(real - s["start"], 3)
            gap = est - real
            if abs(gap) > 0.45:
                out.append(("의심", f"{sc['id']}.{k}: 그림이 ‘{spec['at']}’ 말보다 {gap:+.2f}초({'빠름' if gap < 0 else '늦음'}) — 추정 {est:.2f} / 실제 {real:.2f}"))
    # 자막 나눔(‘|’ 또는 길이로 나눈 둘째 조각부터)과 실제 말 시각
    cap = (proj / "video/compositions/captions.html").read_text(encoding="utf-8")
    for m in re.finditer(r'id="cap-(\d+)([b-h])"[^>]*data-start="([\d.]+)"[^>]*><span>(.*?)</span>', cap):
        n, part, t0, txt = int(m.group(1)), m.group(2), float(m.group(3)), html.unescape(m.group(4))
        s = byn.get(n)
        if not s:
            continue
        head = " ".join(txt.split()[:2])
        real = locate(words, s, head, t0)
        if real is None:
            continue
        times[f"cap|{n}|{'abcdefgh'.index(part)}"] = round(real - s["start"], 3)
        if abs(t0 - real) > 0.5:
            out.append(("의심", f"자막 {n}{part} ‘{txt[:16]}’이 말보다 {t0 - real:+.2f}초 — 자막 {t0:.2f} / 실제 {real:.2f}"))
    detail["times"] = times


def locate(words, s, phrase, est):
    """문장 s 안에서 phrase(대본 글자)가 실제로 시작된 시각. 받아 적은 낱말 1~4개를 이어 붙여 가장 비슷한 곳(0.6 이상)."""
    target = norm(phrase)
    if not target:
        return None
    ws = [w for w in words if s["start"] - 0.2 <= w[0] <= s["start"] + s["dur"] + 0.2]
    best = None
    for i in range(len(ws)):
        raw = ""
        for j in range(i, min(i + 4, len(ws))):
            raw += ws[j][2]  # ‘GROUP’ ‘BY’처럼 나뉘어 적힌 영어 낱말도 이어 붙인 뒤 한글 소리로 바꾼다
            acc = norm(raw)
            if not acc:
                continue
            r = difflib.SequenceMatcher(None, target, acc[: len(target) + 1]).ratio()
            if r >= 0.6:
                key = (round(r, 2), -abs(ws[i][0] - est))
                if best is None or key > best[0]:
                    best = (key, ws[i][0])
            if len(acc) >= len(target) + 1:
                break
    return best[1] if best else None


def final_mp4(proj, title_hint=None):
    r = proj / "video" / "renders"
    c = [p for p in r.glob("*.mp4") if p.name != "raw.mp4"]
    return max(c, key=lambda p: p.stat().st_mtime) if c else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("--words")
    ap.add_argument("--no-pops", action="store_true")
    ap.add_argument("--write-times", action="store_true", help="잰 말 시각을 <프로젝트>/word_times.json으로 저장(build_video.py가 씀)")
    a = ap.parse_args()
    for ep in map(Path, a.episodes):
        for proj, tag in [(ep, ""), (ep / "shorts", "-shorts")]:
            tl = json.loads((proj / "timeline.json").read_text(encoding="utf-8"))
            out, detail = [], {}
            narr, med = check_narration(proj, tl, out)
            mp4 = final_mp4(proj)
            check_final(proj, tl, narr, mp4, out)
            if not a.no_pops and mp4:
                check_pops(mp4, out)
            words = None
            lw = proj / "listen" / "words.json"
            if lw.exists():  # listen_episode.py 결과(문장 시작 기준) → 지금 timeline 기준 시각으로
                lis = json.loads(lw.read_text(encoding="utf-8"))
                words = []
                for s in sentences(tl):
                    e = lis.get(str(s["n"]))
                    if e and e["say"] == re.sub(r"\s*\|\s*", " ", s["say"]):
                        words += [[s["start"] + w[0], s["start"] + w[1], w[2]] for w in e["words"]]
                    else:
                        out.append(("참고", f"{s['n']}번은 받아 적은 뒤 읽을 말이 바뀜 — listen_episode.py를 다시 돌릴 것"))
            elif a.words:
                wf = sorted(Path(a.words).glob(f"{ep.name}{tag}.*.words.json"))
                if wf:
                    words = json.loads(wf[-1].read_text(encoding="utf-8"))
            if words is not None:
                check_words(proj, tl, words, out, detail)
                if a.write_times:
                    # 받아 적기가 다르게 적어 자동으로 못 찾은 낱말은 word_times.manual.json에 직접 잰 값을 적어 둔다(우선)
                    man = proj / "word_times.manual.json"
                    manual = {k: v for k, v in json.loads(man.read_text(encoding="utf-8")).items() if not k.startswith("_")} if man.exists() else {}
                    (proj / "word_times.json").write_text(json.dumps(
                        {"_설명": "받아 적기로 잰 실제 말 시각(문장 시작 기준 초). verify_episode.py --write-times가 만든다(손으로 고치지 말고 "
                                  "word_times.manual.json에). ‘문장|낱말’ = build.json extra, ‘cap|문장|조각’ = 자막 둘째 조각부터의 시작.",
                         **detail["times"], **manual}, ensure_ascii=False, indent=1), encoding="utf-8")
            name = f"{ep.name}{' 쇼츠' if tag else ''}"
            n_bad = sum(1 for k, _ in out if k in ("확실", "의심", "확인"))
            print(f"=== {name}: 문장 {len(sentences(tl))}개, 말 빠르기 가운데값 {med:.1f}음절/초 — 볼 것 {n_bad}건")
            for k, msg in out:
                print(f"  [{k}] {msg}")


if __name__ == "__main__":
    main()
