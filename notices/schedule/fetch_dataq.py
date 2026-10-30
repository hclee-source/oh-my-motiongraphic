"""데이터자격검정(dataq.or.kr) 시험 일정 받아 오기 → notices/schedule/exams.json

ADsP(데이터분석 준전문가), SQLD(SQL 개발자), 빅데이터분석기사 필기·실기만 옮긴다.
이미 있는 회차는 날짜가 바뀌었을 때만 고치고, 확인 표시(confirmed)는 날짜가 바뀌면 지운다(다시 확인받아야 함).
새 회차·바뀐 회차를 출력한다(매일 실행에서 메일로 알림).

사용: python notices/schedule/fetch_dataq.py [--html 저장된페이지.html]
"""
import datetime as dt
import html as H
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

URL = "https://www.dataq.or.kr/www/accept/schedule.do"
OUT = Path(__file__).resolve().parent / "exams.json"
NAMES = {"데이터분석 준전문가": ("ADsP", ""), "SQL 개발자": ("SQLD", ""), "빅데이터 분석기사": ("빅분기", None)}

def cells(row):
    out = []
    for attrs, body in re.findall(r"<t[hd]([^>]*)>(.*?)</t[hd]>", row, re.S):
        span = re.search(r'rowspan="(\d+)"', attrs)
        text = " ".join(H.unescape(re.sub(r"<[^>]+>", " ", body)).split())
        out.append((text, int(span.group(1)) if span else 1))
    return out

def parse_table(page):
    """첫 표(회차별 일정)를 rowspan을 풀어 행 목록으로."""
    table = re.search(r"<table.*?</table>", page, re.S).group(0)
    rows = re.findall(r"<tr.*?</tr>", table, re.S)
    ncols = 9
    carry = {}  # 열 번호 → [남은 행 수, 값]
    grid = []
    for row in rows[1:]:
        cs = cells(row)
        need = ncols - len(cs)  # 이 행이 위에서 물려받아야 할 칸 수(표의 rowspan이 실제 행 수보다 클 때를 막음)
        line, col, it = [], 0, iter(cs)
        while True:
            if need > 0 and col in carry and carry[col][0] > 0:
                line.append(carry[col][1]); carry[col][0] -= 1; col += 1; need -= 1; continue
            try:
                text, span = next(it)
            except StopIteration:
                break
            line.append(text)
            if span > 1:
                carry[col] = [span - 1, text]
            col += 1
        grid.append(line)
    return grid

def md(s, year, after=None):
    """'9.28' → date. after(시작일)보다 앞이면 다음 해."""
    m, d = map(int, re.match(r"(\d+)\.(\d+)", s).groups())
    x = dt.date(year, m, d)
    if after and x < after:
        x = dt.date(year + 1, m, d)
    return x

def period(s, year):
    """'9.28~10.2', '3.3~9', '9.18~9.22' → (시작, 끝)"""
    a, b = [p.strip() for p in s.split("~")]
    start = md(a, year)
    if "." in b:
        end = md(b, year, start)
    else:
        end = dt.date(start.year, start.month, int(b))
    return start, end

def fetch(html_path=None):
    if html_path:
        page = Path(html_path).read_text(encoding="utf-8")
    else:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    year = int(re.search(r"(20\d\d)년 국가공인 데이터 관련 자격증 시험 일정표", page).group(1))
    rounds = []
    for line in parse_table(page):
        if len(line) < 8 or line[0] not in NAMES:
            continue
        exam, _ = NAMES[line[0]]
        rno = int(re.search(r"\d+", line[1]).group())
        stage = "" if line[2] in ("-", "") else line[2]
        a0, a1 = period(line[3], year)
        test = md(line[5], year, a0)
        result = md(line[7], year, test)
        rounds.append({
            "exam": exam, "round": rno, "stage": stage, "year": year,
            "apply_start": a0.isoformat(), "apply_end": a1.isoformat(),
            "exam_date": test.isoformat(), "result": result.isoformat(),
            "source": URL,
        })
    if not rounds:
        raise SystemExit("일정표를 읽지 못했습니다(페이지 모양이 바뀌었을 수 있음)")
    return year, rounds

def key(r):
    return f"{r['exam']}|{r['round']}|{r['stage']}"

def main():
    html_path = sys.argv[sys.argv.index("--html") + 1] if "--html" in sys.argv else None
    year, rounds = fetch(html_path)
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"rounds": []}
    old = {key(r): r for r in data["rounds"]}
    new, changed = [], []
    for r in rounds:
        k = key(r)
        if k not in old:
            r["confirmed"] = False
            old[k] = r
            new.append(r)
        else:
            o = old[k]
            diff = [f for f in ("apply_start", "apply_end", "exam_date", "result") if o.get(f) != r[f]]
            if diff:
                changed.append((r, {f: (o.get(f), r[f]) for f in diff}))
                o.update(r)
                o["confirmed"] = False
    data["rounds"] = sorted(old.values(), key=lambda r: (r["exam_date"], r["exam"]))
    data["dataq_checked"] = dt.date.today().isoformat()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"데이터자격검정 {year}년 일정 {len(rounds)}회차 읽음 — 새 회차 {len(new)}, 바뀐 회차 {len(changed)}")
    for r in new:
        print(f"  새: {r['exam']} 제{r['round']}회{(' ' + r['stage']) if r['stage'] else ''} 접수 {r['apply_start']}~{r['apply_end']} 시험 {r['exam_date']}")
    for r, d in changed:
        print(f"  바뀜: {r['exam']} 제{r['round']}회 {d}")

if __name__ == "__main__":
    main()
