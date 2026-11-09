# -*- coding: utf-8 -*-
"""015 서브쿼리 — 대본 숫자 검증(화면에 쓰지 않음).

실행(저장소 맨 위): .venv/Scripts/python.exe concept/episodes/015-sql-subquery/verify_examples.py

sqlite3에는 ANY · ALL이 없어서 두 가지로 흉내 내고 서로 같은지 확인한다.
  - 끝값 방식: > ANY = > MIN, > ALL = > MAX, < ANY = < MAX, < ALL = < MIN
  - 정의 방식: x > ANY(S) = EXISTS(s in S: x > s), x > ALL(S) = NOT EXISTS(s in S: NOT (x > s))
  (예시 표에는 NULL이 없으므로 정의 방식이 오라클 의미와 같다. 결과가 0행인 S에서는
   끝값 방식이 틀린다 — MAX(빈 집합) = NULL이라 > ALL이 0행이 되지만, 오라클 > ALL은 모든 행이 참.)
오라클에서만 확인할 수 있는 것(규칙으로만 적음):
  - 단일 행 연산자(=, >, < …)에 두 행 이상 돌려주는 서브쿼리 → ORA-01427 오류.
    sqlite는 첫 행만 쓰고 오류를 내지 않으므로 여기서는 ‘서브쿼리가 2행’인 것만 확인한다.
  - 스칼라 서브쿼리가 두 행 이상 → 오류, 0행 → NULL.
  - WHERE 절 서브쿼리 안 ORDER BY → 오류(ORA-00907), 인라인 뷰 안 ORDER BY → 허용.
  - 다중 열 서브쿼리 (부서, 급여) IN (...) → 오라클 허용, SQL Server 미지원.
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

EMP = [  # 이름, 부서, 급여(만 원)
    ("민수", "영업", 300), ("지영", "영업", 500), ("현우", "영업", 700),
    ("수진", "개발", 400), ("동훈", "개발", 600),
    ("예린", "인사", 350), ("서연", "인사", 400),
]
DEPT = ["영업", "개발", "인사", "기획"]  # 기획: 직원 없음

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 직원 (이름 TEXT, 부서 TEXT, 급여 INTEGER)")
db.executemany("INSERT INTO 직원 VALUES (?, ?, ?)", EMP)
db.execute("CREATE TABLE 부서 (부서명 TEXT)")
db.executemany("INSERT INTO 부서 VALUES (?)", [(d,) for d in DEPT])

ok = True


def q(sql):
    return [r[0] if len(r) == 1 else r for r in db.execute(sql).fetchall()]


def check(label, got, want):
    global ok
    g = sorted(got, key=str) if isinstance(got, list) else got
    w = sorted(want, key=str) if isinstance(want, list) else want
    mark = "OK " if g == w else "XX "
    if g != w:
        ok = False
    n = f"{len(got)}행 " if isinstance(got, list) else ""
    print(f"{mark}{label}: {n}{got}" + ("" if g == w else f"   (기대 {want})"))


DEV = "(SELECT 급여 FROM 직원 WHERE 부서 = '개발')"
EMPTY = "(SELECT 급여 FROM 직원 WHERE 부서 = '기획')"
ORDER = " ORDER BY 급여, 이름"

print("== 표")
print(q("SELECT 이름 || ' ' || 부서 || ' ' || 급여 FROM 직원"))
check("개발 부서 급여(서브쿼리 결과)", q(f"SELECT 급여 FROM 직원 WHERE 부서 = '개발'"), [400, 600])
check("기획 부서 급여(0행)", q(f"SELECT 급여 FROM 직원 WHERE 부서 = '기획'"), [])

print("\n== 1장 훅: 급여 = (개발 급여) → 서브쿼리가 2행이라 오라클은 ORA-01427 오류")
print("   (sqlite는 첫 행 400만 써서", q(f"SELECT 이름 FROM 직원 WHERE 급여 = {DEV}"), "를 돌려줌 — 오라클과 다름, 참고만)")

print("\n== 3장 IN (= ANY)")
check("급여 IN (개발 급여)", q(f"SELECT 이름 FROM 직원 WHERE 급여 IN {DEV}{ORDER}"), ["수진", "서연", "동훈"])
check("= ANY 정의 방식(EXISTS)",
      q("SELECT 이름 FROM 직원 a WHERE EXISTS (SELECT 1 FROM 직원 b WHERE b.부서 = '개발' AND a.급여 = b.급여)"),
      ["수진", "서연", "동훈"])


def any_all(op, sub):
    """끝값 방식, 정의 방식, 파이썬 의미를 모두 계산."""
    vals = q(f"SELECT 급여 {sub[sub.index('FROM'):-1]}")
    py_any = [n for n, d, s in EMP if any(eval(f"{s} {op} {v}") for v in vals)]
    py_all = [n for n, d, s in EMP if all(eval(f"{s} {op} {v}") for v in vals)]
    agg_any = "MIN" if op in (">", ">=") else "MAX"
    agg_all = "MAX" if op in (">", ">=") else "MIN"
    inner = sub[1:-1].replace("SELECT 급여 FROM 직원 WHERE", "SELECT 1 FROM 직원 b WHERE b.")
    def_any = q(f"SELECT 이름 FROM 직원 a WHERE EXISTS ({inner} AND a.급여 {op} b.급여)")
    def_all = q(f"SELECT 이름 FROM 직원 a WHERE NOT EXISTS ({inner} AND NOT (a.급여 {op} b.급여))")
    ext_any = q(f"SELECT 이름 FROM 직원 WHERE 급여 {op} (SELECT {agg_any}(급여) {sub[sub.index('FROM'):-1]})")
    ext_all = q(f"SELECT 이름 FROM 직원 WHERE 급여 {op} (SELECT {agg_all}(급여) {sub[sub.index('FROM'):-1]})")
    return py_any, py_all, def_any, def_all, ext_any, ext_all


print("\n== 4·5장 ANY · ALL (서브쿼리 결과 400, 600)")
for op, want_any, want_all in [
    (">", ["지영", "동훈", "현우"], ["현우"]),
    ("<", ["민수", "예린", "수진", "서연", "지영"], ["민수", "예린"]),
]:
    pa, pl, da, dl, ea, el = any_all(op, DEV)
    check(f"{op} ANY 파이썬 의미", pa, want_any)
    check(f"{op} ANY 정의 방식(EXISTS)", da, want_any)
    check(f"{op} ANY 끝값 방식({'MIN' if op == '>' else 'MAX'})", ea, want_any)
    check(f"{op} ALL 파이썬 의미", pl, want_all)
    check(f"{op} ALL 정의 방식(NOT EXISTS)", dl, want_all)
    check(f"{op} ALL 끝값 방식({'MAX' if op == '>' else 'MIN'})", el, want_all)

print("\n== 5장 끝: 서브쿼리 결과가 0행(기획 부서 급여)")
pa, pl, da, dl, ea, el = any_all(">", EMPTY)
check("> ALL (0행) 파이썬 의미 = 모두 참", pl, [n for n, _, _ in EMP])
check("> ALL (0행) 정의 방식 = 7행", dl, [n for n, _, _ in EMP])
check("> ANY (0행) 파이썬 의미 = 0행", pa, [])
check("> ANY (0행) 정의 방식 = 0행", da, [])
print(f"   참고: 끝값 방식 급여 > (SELECT MAX(급여) … 기획)의 결과는 {len(el)}행 (MAX가 NULL이라 > ALL의 7행과 다름. 대본에서는 쓰지 않음)")

print("\n== 6장 연관 서브쿼리: 자기 부서 평균보다 급여가 많은 직원")
avg = dict(q("SELECT 부서, AVG(급여) FROM 직원 GROUP BY 부서"))
check("부서 평균 영업", avg["영업"], 500)
check("부서 평균 개발", avg["개발"], 500)
check("부서 평균 인사", avg["인사"], 375)
check("a.급여 > (SELECT AVG(b.급여) … b.부서 = a.부서)",
      q("SELECT a.이름 FROM 직원 a WHERE a.급여 > (SELECT AVG(b.급여) FROM 직원 b WHERE b.부서 = a.부서)"),
      ["현우", "동훈", "서연"])
print("   행별: 민수 300 vs 영업 500 → 빠짐 / 지영 500 vs 500 → 같아서 빠짐 / 서연 400 vs 인사 375 → 남음")
check("서연(400) < 지영(500)", 400 < 500, True)

print("\n== 7장 EXISTS · NOT EXISTS (부서 표 4행)")
check("EXISTS (SELECT 1 FROM 직원 b WHERE b.부서 = a.부서명)",
      q("SELECT a.부서명 FROM 부서 a WHERE EXISTS (SELECT 1 FROM 직원 b WHERE b.부서 = a.부서명)"),
      ["영업", "개발", "인사"])
check("NOT EXISTS", q("SELECT a.부서명 FROM 부서 a WHERE NOT EXISTS (SELECT 1 FROM 직원 b WHERE b.부서 = a.부서명)"),
      ["기획"])
check("SELECT 목록을 바꿔도(SELECT 이름) 같은 결과",
      q("SELECT a.부서명 FROM 부서 a WHERE EXISTS (SELECT 이름 FROM 직원 b WHERE b.부서 = a.부서명)"),
      ["영업", "개발", "인사"])
# 008(NULL 편) 연결 한 줄: 직원 부서에 NULL이 하나 섞였다고 가정
db.execute("CREATE TABLE 직원N AS SELECT * FROM 직원")
db.execute("INSERT INTO 직원N VALUES ('가정', NULL, 100)")
check("(가정) 부서 NULL 섞임 → NOT IN = 0행",
      q("SELECT 부서명 FROM 부서 WHERE 부서명 NOT IN (SELECT 부서 FROM 직원N)"), [])
check("(가정) 부서 NULL 섞임 → NOT EXISTS = 기획 그대로",
      q("SELECT a.부서명 FROM 부서 a WHERE NOT EXISTS (SELECT 1 FROM 직원N b WHERE b.부서 = a.부서명)"), ["기획"])

print("\n== 8장 자리별 이름")
check("다중 열 (부서, 급여) IN (부서별 MAX) = 부서별 최고 급여자",
      q("SELECT 이름 FROM 직원 WHERE (부서, 급여) IN (SELECT 부서, MAX(급여) FROM 직원 GROUP BY 부서)"),
      ["현우", "동훈", "서연"])
check("스칼라 서브쿼리 0행 → NULL",
      q("SELECT (SELECT 급여 FROM 직원 WHERE 부서 = '기획')"), [None])
check("인라인 뷰(ORDER BY 포함) 결과를 표처럼",
      q("SELECT 이름 FROM (SELECT 이름, 급여 FROM 직원 ORDER BY 급여 DESC) WHERE 급여 >= 600"), ["현우", "동훈"])

print("\n== 쇼츠: 서브쿼리 결과 20, 50, 80 / 비교 값 60")
S = [20, 50, 80]
check("60 > ANY (20, 50, 80) = 60 > 20", any(60 > v for v in S), True)
check("60 > ALL (20, 50, 80) = 60 > 80", all(60 > v for v in S), False)
check("> ANY 기준 = 최솟값", min(S), 20)
check("> ALL 기준 = 최댓값", max(S), 80)
check("60 < ANY = 60 < 80(최댓값)", any(60 < v for v in S), 60 < max(S))
check("60 < ALL = 60 < 20(최솟값)", all(60 < v for v in S), 60 < min(S))

print("\n모두 일치" if ok else "\n불일치 있음")
sys.exit(0 if ok else 1)
