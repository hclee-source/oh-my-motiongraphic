"""016 ROWNUM과 Top N — 대본 예시 숫자 검증(화면에는 쓰지 않음).

실행(저장소 맨 위에서): .venv/Scripts/python.exe concept/episodes/016-sql-topn/verify_examples.py
- sqlite3에는 ROWNUM·FETCH FIRST가 없으므로:
  · ROWNUM은 오라클 규칙대로 파이썬에서 흉내 낸다 — 행을 읽을 때마다 지금 차례의 번호(1부터)를 붙여 보고,
    WHERE를 통과하면 번호가 확정되고 다음 번호로 넘어간다. 버려지면 번호는 그대로.
  · ‘ORDER BY 없이 읽는 순서’는 보장되지 않으므로, 대본의 가정(저장된 순서대로 읽힘)을 rowid 순으로 흉내 낸다.
  · FETCH FIRST n ROWS ONLY = ORDER BY … LIMIT n, OFFSET m ROWS FETCH NEXT n ROWS ONLY = LIMIT n OFFSET m,
    FETCH FIRST n ROWS WITH TIES = RANK() OVER (ORDER BY …) <= n (마지막 행과 정렬 값이 같은 행까지).
- 동점(400 두 명)의 앞뒤는 정해지지 않으므로, 두 가지 순서를 모두 돌려 ‘급여 값’이 같은지 확인한다.
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ── 본편: 직원 7행, 저장된 순서 ──
EMP = [("지영", 300), ("민수", 400), ("수진", 250), ("현우", 500), ("예린", 400), ("동훈", 450), ("태호", 350)]

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE 직원 (이름 TEXT, 급여 INTEGER)")
con.executemany("INSERT INTO 직원 VALUES (?, ?)", EMP)

ok_all = True


def check(label, got, want):
    global ok_all
    ok = got == want
    ok_all &= ok
    print(f"{'OK ' if ok else 'XX '} {label}: {got}" + ("" if ok else f"  (기대 {want})"))


def rownum_filter(rows, pred):
    """오라클 ROWNUM 흉내: pred(번호)가 참이면 통과·번호 증가, 거짓이면 버림·번호 그대로."""
    out, n = [], 1
    for r in rows:
        if pred(n):
            out.append((n, *r))
            n += 1
    return out


physical = con.execute("SELECT 이름, 급여 FROM 직원 ORDER BY rowid").fetchall()  # 저장된 순서대로 읽힌다고 가정
check("저장된 순서", physical, EMP)

# 정렬 결과(동점 두 가지 순서 모두)
sorted_a = con.execute("SELECT 이름, 급여 FROM 직원 ORDER BY 급여 DESC, rowid").fetchall()       # 민수 먼저
sorted_b = con.execute("SELECT 이름, 급여 FROM 직원 ORDER BY 급여 DESC, rowid DESC").fetchall()  # 예린 먼저
check("급여 내림차순(값)", [s for _, s in sorted_a], [500, 450, 400, 400, 350, 300, 250])
check("급여 내림차순(이름, 민수 먼저인 경우)", [n for n, _ in sorted_a], ["현우", "동훈", "민수", "예린", "태호", "지영", "수진"])
rank = con.execute("SELECT 이름, 급여, RANK() OVER (ORDER BY 급여 DESC) FROM 직원 ORDER BY 급여 DESC, rowid").fetchall()
check("RANK(민수·예린 공동 3등)", [(n, r) for n, _, r in rank if n in ("민수", "예린")], [("민수", 3), ("예린", 3)])

# ① 함정: WHERE ROWNUM <= 3 ORDER BY 급여 DESC → 먼저 읽힌 3행을 정렬
step = rownum_filter(physical, lambda n: n <= 3)
check("① WHERE ROWNUM <= 3 (번호, 이름, 급여)", step, [(1, "지영", 300), (2, "민수", 400), (3, "수진", 250)])
wrong = sorted([(nm, s) for _, nm, s in step], key=lambda r: -r[1])
check("① 이어서 ORDER BY 급여 DESC", wrong, [("민수", 400), ("지영", 300), ("수진", 250)])
check("① 현우 500이 빠졌는가", "현우" not in [nm for nm, _ in wrong], True)
# 같은 결과를 SQL로(앞 3행 LIMIT → 정렬)
wrong_sql = con.execute("SELECT * FROM (SELECT 이름, 급여 FROM 직원 ORDER BY rowid LIMIT 3) ORDER BY 급여 DESC").fetchall()
check("① sqlite 흉내(LIMIT 3 뒤 정렬)", wrong_sql, wrong)
# 현우부터는 받을 번호가 계속 4 → 모두 탈락
trace, n = [], 1
for nm, s in physical:
    passed = n <= 3
    trace.append((nm, n, passed))
    n += passed
check("① 행마다 붙여 본 번호", [(nm, k) for nm, k, _ in trace],
      [("지영", 1), ("민수", 2), ("수진", 3), ("현우", 4), ("예린", 4), ("동훈", 4), ("태호", 4)])

# ROWNUM 특정 번호
check("ROWNUM = 1", rownum_filter(physical, lambda n: n == 1), [(1, "지영", 300)])
check("ROWNUM = 2 → 0행", len(rownum_filter(physical, lambda n: n == 2)), 0)
check("ROWNUM > 1 → 0행", len(rownum_filter(physical, lambda n: n > 1)), 0)
check("ROWNUM >= 4 → 0행", len(rownum_filter(physical, lambda n: n >= 4)), 0)
check("ROWNUM BETWEEN 4 AND 6 → 0행", len(rownum_filter(physical, lambda n: 4 <= n <= 6)), 0)
check("ROWNUM < 4 → 3행", len(rownum_filter(physical, lambda n: n < 4)), 3)

# ② 인라인 뷰: 정렬 뒤 바깥에서 ROWNUM <= 3
for tag, srt in (("민수 먼저", sorted_a), ("예린 먼저", sorted_b)):
    top = rownum_filter(srt, lambda n: n <= 3)
    check(f"② 인라인 뷰 + ROWNUM <= 3 급여({tag})", [s for _, _, s in top], [500, 450, 400])
    print(f"    이름: {[nm for _, nm, _ in top]}")

# ③ 구간: 가운데에서 ROWNUM AS 순번 → 바깥에서 순번 BETWEEN 4 AND 6
for tag, srt in (("민수 먼저", sorted_a), ("예린 먼저", sorted_b)):
    mid = rownum_filter(srt, lambda n: True)  # 가운데 SELECT ROWNUM AS 순번, … (조건 없음 → 전부 번호)
    page = [r for r in mid if 4 <= r[0] <= 6]
    check(f"③ 순번 BETWEEN 4 AND 6 ({tag})", [(k, s) for k, _, s in page], [(4, 400), (5, 350), (6, 300)])
    print(f"    이름: {[nm for _, nm, _ in page]}")

# ④ FETCH FIRST 3 ROWS ONLY / WITH TIES
only = con.execute("SELECT 이름, 급여 FROM 직원 ORDER BY 급여 DESC LIMIT 3").fetchall()
check("④ FETCH FIRST 3 ROWS ONLY 급여", [s for _, s in only], [500, 450, 400])
ties = con.execute("""SELECT 이름, 급여 FROM (SELECT 이름, 급여, RANK() OVER (ORDER BY 급여 DESC) AS r FROM 직원)
                      WHERE r <= 3 ORDER BY 급여 DESC, 이름""").fetchall()
check("④ FETCH FIRST 3 ROWS WITH TIES", ties, [("현우", 500), ("동훈", 450), ("민수", 400), ("예린", 400)])
check("④ WITH TIES 행 수", len(ties), 4)
# WITH TIES 정의대로도 확인: 앞 3행 + 마지막 행(3번째)과 급여가 같은 행
last = sorted_a[2][1]
ties_def = sorted_a[:3] + [r for r in sorted_a[3:] if r[1] == last]
check("④ WITH TIES(정의대로) 행 수", len(ties_def), 4)

# ⑤ OFFSET 3 ROWS FETCH NEXT 3 ROWS ONLY
off = con.execute("SELECT 이름, 급여 FROM 직원 ORDER BY 급여 DESC LIMIT 3 OFFSET 3").fetchall()
check("⑤ OFFSET 3 ROWS FETCH NEXT 3 ROWS ONLY 급여", [s for _, s in off], [400, 350, 300])

# ⑥ SQL Server TOP(3) … ORDER BY: 정렬 뒤 자름 → ④와 같음, WITH TIES → 4행
check("⑥ TOP(3) = FETCH FIRST 3 (급여)", [s for _, s in only], [500, 450, 400])

# ── 쇼츠: 점수 카드 5장, 읽히는 순서 ──
SH = [60, 70, 95, 90, 90]  # 검수 반영: 앞 두 장을 60, 70으로 — 정렬하면 자리가 바뀌어 보이게
con.execute("CREATE TABLE 점수표 (점수 INTEGER)")
con.executemany("INSERT INTO 점수표 VALUES (?)", [(v,) for v in SH])
ph = [r for r in con.execute("SELECT 점수 FROM 점수표 ORDER BY rowid").fetchall()]
s1 = rownum_filter(ph, lambda n: n <= 2)
check("쇼츠 WHERE ROWNUM <= 2 (읽힌 순서)", [v for _, v in s1], [60, 70])
check("쇼츠 이어서 ORDER BY 점수 DESC", sorted([v for _, v in s1], reverse=True), [70, 60])
srt = [r for r in con.execute("SELECT 점수 FROM 점수표 ORDER BY 점수 DESC").fetchall()]
check("쇼츠 정렬", [v for (v,) in srt], [95, 90, 90, 70, 60])
check("쇼츠 인라인 뷰 + ROWNUM <= 2", [v for _, v in rownum_filter(srt, lambda n: n <= 2)], [95, 90])
check("쇼츠 ROWNUM = 2 → 0행", len(rownum_filter(ph, lambda n: n == 2)), 0)
check("쇼츠 FETCH FIRST 2 ROWS ONLY", [v for (v,) in con.execute("SELECT 점수 FROM 점수표 ORDER BY 점수 DESC LIMIT 2")], [95, 90])
sh_ties = [v for (v,) in con.execute(
    "SELECT 점수 FROM (SELECT 점수, RANK() OVER (ORDER BY 점수 DESC) r FROM 점수표) WHERE r <= 2 ORDER BY 점수 DESC")]
check("쇼츠 FETCH FIRST 2 ROWS WITH TIES", sh_ties, [95, 90, 90])
check("쇼츠 본편과 숫자 겹침 없음", set(SH) & {s for _, s in EMP}, set())

print("\n모두 일치" if ok_all else "\n불일치 있음")
sys.exit(0 if ok_all else 1)
