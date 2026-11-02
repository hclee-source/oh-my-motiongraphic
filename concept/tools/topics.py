"""소재 목록 관리: topics/topics.json(개념 목록·진행 상태)과 topics/blueprint.json(공식 출제기준)

사용(저장소 맨 위에서):
  python concept/tools/topics.py check              목록 검사(출제기준 번호·선수 개념·중복) + 출제기준 빈 곳
  python concept/tools/topics.py next [개수]         다음에 만들 주제(대기 중, 선수 개념이 먼저 나온 것)
  python concept/tools/topics.py set <id> <상태> [폴더]   상태 바꾸기(폴더는 concept/ 기준 편 폴더, 예: episodes/002-roc-auc)
  python concept/tools/topics.py table              topics/진행표.md 다시 만들기(check·set 뒤에 자동)
상태: 대기 → 대본 → 검수 통과 → 영상 완성 → 업로드 완료
"""
import json, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "topics" / "topics.json"
BLUEPRINT = ROOT / "topics" / "blueprint.json"
TABLE = ROOT / "topics" / "진행표.md"
STATES = ["대기", "대본", "검수 통과", "영상 완성", "업로드 완료"]
EXAMS = {"adsp": "ADsP", "bigdata": "빅분기", "sqld": "SQLD"}  # topics.json 칸 이름 → 시험 이름(칸이 없으면 빈 목록)

def load():
    return json.loads(TOPICS.read_text(encoding="utf-8")), json.loads(BLUEPRINT.read_text(encoding="utf-8"))

def save(data):
    TOPICS.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

def codes(t, exam):
    return t.get(exam) or []

def exam_of(t):
    if codes(t, "sqld"):
        return "SQLD"
    a, b = bool(codes(t, "adsp")), bool(codes(t, "bigdata"))
    return "공통" if a and b else "ADsP" if a else "빅분기"

def path_of(bp, exam, code):
    items = bp[exam]["items"]
    parts = code.split(".")
    return " > ".join(items[".".join(parts[:i])] for i in range(1, len(parts) + 1))

def leaves(bp, exam):
    """출제기준의 가장 아래 항목(ADsP는 세부항목, 빅분기는 세세항목)."""
    codes = list(bp[exam]["items"])
    return [c for c in codes if not any(o.startswith(c + ".") for o in codes)]

def check(data, bp):
    ts = data["topics"]
    errs = []
    ids = Counter(t["id"] for t in ts)
    errs += [f"id 중복: {i}" for i, n in ids.items() if n > 1]
    orders = Counter(t["order"] for t in ts)
    errs += [f"순서 중복: {o}" for o, n in orders.items() if n > 1]
    by_id = {t["id"]: t for t in ts}
    for t in ts:
        if t["status"] not in STATES:
            errs.append(f"{t['id']}: 알 수 없는 상태 ‘{t['status']}’")
        if not any(codes(t, e) for e in EXAMS):
            errs.append(f"{t['id']}: 출제기준 번호가 없음")
        for exam in EXAMS:
            for code in codes(t, exam):
                if code not in bp[exam]["items"]:
                    errs.append(f"{t['id']}: {EXAMS[exam]} 출제기준에 없는 번호 {code}")
        for p in t["prereq"]:
            if p not in by_id:
                errs.append(f"{t['id']}: 없는 선수 개념 {p}")
            elif by_id[p]["order"] > t["order"]:
                errs.append(f"{t['id']}: 선수 개념 {p}가 더 뒤 순서({by_id[p]['order']})에 있음")
    # 출제기준 빈 곳: 가장 아래 항목마다 다루는 주제가 있는지(위 항목 번호로 걸어 둔 것도 인정)
    gaps = {}
    for exam in EXAMS:
        used = {c for t in ts for c in codes(t, exam)}
        gaps[exam] = [c for c in leaves(bp, exam)
                      if not any(c == u or c.startswith(u + ".") for u in used)]
    return errs, gaps

def next_topics(data, n=1):
    ts = sorted(data["topics"], key=lambda t: t["order"])
    by_id = {t["id"]: t for t in ts}
    out = []
    for t in ts:
        if t["status"] != "대기":
            continue
        waiting = [p for p in t["prereq"] if by_id[p]["status"] == "대기"]
        out.append((t, waiting))
        if len(out) >= n:
            break
    return out

def table(data, bp):
    ts = sorted(data["topics"], key=lambda t: t["order"])
    cnt = Counter(t["status"] for t in ts)
    ex = Counter(exam_of(t) for t in ts)
    lines = [
        "# 소재 진행표",
        "",
        "`tools/topics.py`가 만드는 파일입니다. 직접 고치지 말고 topics.json을 고친 뒤 `python tools/topics.py table`.",
        "",
        f"- 전체 {len(ts)}개: 공통 {ex['공통']} · ADsP만 {ex['ADsP']} · 빅분기만 {ex['빅분기']} · SQLD {ex['SQLD']}",
        "- 상태: " + " · ".join(f"{s} {cnt[s]}" for s in STATES),
        f"- 출제기준: ADsP({bp['adsp']['checked']} 확인), 빅분기({bp['bigdata']['period']}), SQLD({bp['sqld']['checked']} 확인)",
        "",
        "| 순서 | 개념 | 시험 | 묶음 | 계산 | 상태 | 폴더 |",
        "|---:|---|---|---|:---:|---|---|",
    ]
    for t in ts:
        lines.append(f"| {t['order']} | {t['title']} | {exam_of(t)} | {t['group']} | {'○' if t['calc'] else ''} | {t['status']} | {t.get('folder', '')} |")
    lines += ["", "## 출제기준 위치", ""]
    for t in ts:
        locs = [f"{EXAMS[e]} {path_of(bp, e, c)}" for e in EXAMS for c in codes(t, e)]
        lines.append(f"- **{t['title']}** — " + " / ".join(locs))
    TABLE.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    data, bp = load()
    if cmd == "check":
        errs, gaps = check(data, bp)
        print(f"주제 {len(data['topics'])}개 — 문제 {len(errs)}건")
        for e in errs:
            print("  ✗", e)
        for exam, g in gaps.items():
            print(f"{EXAMS[exam]} 출제기준 중 다루는 주제가 없는 항목 {len(g)}개" + ("" if not g else ":"))
            for c in g:
                print("  ·", path_of(bp, exam, c))
        table(data, bp)
        sys.exit(1 if errs else 0)
    elif cmd == "next":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        for t, waiting in next_topics(data, n):
            note = f"  (먼저 필요: {', '.join(waiting)})" if waiting else ""
            print(f"{t['order']:>3}. {t['id']} — {t['title']} [{exam_of(t)}{', 계산' if t['calc'] else ''}]{note}")
            print(f"     다룰 것: {t['cover']}")
    elif cmd == "set":
        tid, state = sys.argv[2], sys.argv[3]
        if state not in STATES:
            sys.exit(f"상태는 {' / '.join(STATES)} 중 하나")
        t = next((x for x in data["topics"] if x["id"] == tid), None)
        if t is None:
            sys.exit(f"없는 id: {tid}")
        t["status"] = state
        if len(sys.argv) > 4:
            t["folder"] = sys.argv[4]
        save(data)
        table(data, bp)
        print(f"{t['title']} → {state}")
    elif cmd == "table":
        table(data, bp)
        print(f"{TABLE} 다시 만듦")
    else:
        sys.exit(__doc__)

if __name__ == "__main__":
    main()
