"""013 윈도우 함수 2탄 — 대본 예시 숫자 검증 (sqlite3로 실제 실행, 화면에는 안 나옴).

실행(저장소 맨 위에서): .venv/Scripts/python.exe concept/episodes/013-sql-window-agg/verify_examples.py
- 오라클 기준과 sqlite가 같은 점: ORDER BY만 적으면 기본 범위 RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  (같은 정렬 값의 행 = 함께 포함), ROWS/RANGE 범위, LAG/LEAD(열, n, 기본값), FIRST_VALUE/LAST_VALUE, NTILE,
  PERCENT_RANK, CUME_DIST.
- RATIO_TO_REPORT는 오라클 전용이라 급여 / SUM(급여) OVER ()로 같은 값을 계산한다.
- 동점(지영·현우 300) 사이 순서는 정해지지 않으므로, ROWS·LAG·LEAD는 ‘위치별 값’이 동점 순서와 상관없이 같은지
  동점 순서를 두 가지로 바꿔 확인한다.
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 직원 (사번 INTEGER, 이름 TEXT, 부서 TEXT, 급여 INTEGER)")
db.executemany("INSERT INTO 직원 VALUES (?, ?, ?, ?)", [
    (1, "민수", "영업", 200),
    (2, "지영", "영업", 300),
    (3, "현우", "개발", 300),
    (4, "수진", "개발", 500),
    (5, "동훈", "영업", 700),
])

fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'OK ' if ok else 'FAIL'} {name}: {got}" + ("" if ok else f"  (기대 {want})"))


def col(sql):
    return [r[0] for r in db.execute(sql)]


def positional(expr, frame="", tie="ASC"):
    """급여 순 위치(1~5)별 값. 동점 순서를 tie(이름 ASC/DESC)로 바꿔 가며 같은지 본다."""
    sql = f"""
        SELECT v FROM (
          SELECT ROW_NUMBER() OVER w AS rn, {expr} OVER (w {frame}) AS v
          FROM 직원
          WINDOW w AS (ORDER BY 급여, 이름 {tie})
        ) ORDER BY rn"""
    return col(sql)


def positional_any_tie(name, expr, want, frame=""):
    a, b = positional(expr, frame, "ASC"), positional(expr, frame, "DESC")
    check(name + " (동점 순서 A)", a, want)
    check(name + " (동점 순서 B)", b, want)


# ── 1·3·4장: ORDER BY만 적은 누적합 = 기본 범위 RANGE ─────────────────────────────
# 동점 사이 순서와 무관하게 같은 값이 나오는지: 창 정의에 ORDER BY 급여만 둔다.
check("급여(급여 순)", col("SELECT 급여 FROM 직원 ORDER BY 급여"), [200, 300, 300, 500, 700])
check("SUM OVER (ORDER BY 급여) 기본 범위",
      col("SELECT SUM(급여) OVER (ORDER BY 급여) FROM 직원 ORDER BY 급여"), [200, 800, 800, 1300, 2000])
check("명시한 RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW = 기본과 같음",
      col("SELECT SUM(급여) OVER (ORDER BY 급여 RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM 직원 ORDER BY 급여"),
      [200, 800, 800, 1300, 2000])
check("지영·현우(300) 누적", col("SELECT SUM(급여) OVER (ORDER BY 급여) FROM 직원 WHERE 1 ORDER BY 급여")[1:3], [800, 800])

# ── 2장: 괄호를 비운 OVER(), PARTITION BY 부서 ─────────────────────────────────────
check("SUM OVER () 모든 행", col("SELECT SUM(급여) OVER () FROM 직원"), [2000] * 5)
check("행 수(줄지 않음)", len(col("SELECT SUM(급여) OVER () FROM 직원")), 5)
check("SUM OVER (PARTITION BY 부서)",
      [tuple(r) for r in db.execute("SELECT 이름, SUM(급여) OVER (PARTITION BY 부서) FROM 직원 ORDER BY 사번")],
      [("민수", 1200), ("지영", 1200), ("현우", 800), ("수진", 800), ("동훈", 1200)])

# ── 5장: ROWS 누적 ─────────────────────────────────────────────────────────────
positional_any_tie("ROWS UNBOUNDED PRECEDING ~ CURRENT ROW", "SUM(급여)", [200, 500, 800, 1300, 2000],
                   "ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW")
# 동점 순서에 따라 이름별 값은 바뀐다(지영 500·현우 800 또는 반대) — 대본: ‘누가 먼저인지는 정해져 있지 않음’
for tie in ("ASC", "DESC"):
    rows = list(db.execute(f"""SELECT 이름, SUM(급여) OVER (ORDER BY 급여, 이름 {tie}
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM 직원 ORDER BY 급여, 이름 {tie}"""))
    print(f"     (참고) 동점 순서 이름 {tie}: {rows[1:3]}")

# ── 6장: PARTITION BY 부서 ORDER BY 급여 → 부서마다 누적이 다시 시작 ──────────────────
part = [tuple(r) for r in db.execute(
    "SELECT 부서, 이름, SUM(급여) OVER (PARTITION BY 부서 ORDER BY 급여) FROM 직원 ORDER BY 부서 DESC, 급여")]
check("부서별 누적(영업 → 개발)", part,
      [("영업", "민수", 200), ("영업", "지영", 500), ("영업", "동훈", 1200), ("개발", "현우", 300), ("개발", "수진", 800)])
part_rows = [tuple(r) for r in db.execute(
    "SELECT 부서, 이름, SUM(급여) OVER (PARTITION BY 부서 ORDER BY 급여 ROWS UNBOUNDED PRECEDING) FROM 직원 ORDER BY 부서 DESC, 급여")]
check("부서 안에는 동점 없음 → ROWS도 같음", part_rows, part)

# ── 7장: 앞뒤 한 행씩(ROWS) ────────────────────────────────────────────────────────
# (검수 반영: RANGE 값 차이 예시는 대본에서 뺐음)
positional_any_tie("ROWS 1 PRECEDING ~ 1 FOLLOWING", "SUM(급여)", [500, 800, 1100, 1500, 1200],
                   "ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING")
check("  첫 행 200 + 300", 200 + 300, 500)
check("  마지막 행 500 + 700", 500 + 700, 1200)

# ── 8장: LAG · LEAD ─────────────────────────────────────────────────────────────
positional_any_tie("LAG(급여)", "LAG(급여)", [None, 200, 300, 300, 500])
positional_any_tie("LAG(급여, 2, 0)", "LAG(급여, 2, 0)", [0, 0, 200, 300, 300])
positional_any_tie("LEAD(급여)", "LEAD(급여)", [300, 300, 500, 700, None])

# ── 9장: FIRST_VALUE · LAST_VALUE ────────────────────────────────────────────────
check("FIRST_VALUE(급여) OVER (ORDER BY 급여)",
      col("SELECT FIRST_VALUE(급여) OVER (ORDER BY 급여) FROM 직원 ORDER BY 급여"), [200] * 5)
check("LAST_VALUE(급여) OVER (ORDER BY 급여) = 자기 급여",
      col("SELECT LAST_VALUE(급여) OVER (ORDER BY 급여) FROM 직원 ORDER BY 급여"), [200, 300, 300, 500, 700])
check("LAST_VALUE ... ROWS UNBOUNDED PRECEDING ~ UNBOUNDED FOLLOWING",
      col("""SELECT LAST_VALUE(급여) OVER (ORDER BY 급여 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
             FROM 직원 ORDER BY 급여"""), [700] * 5)

# ── 10장: 비율 함수 ──────────────────────────────────────────────────────────────
check("RATIO_TO_REPORT(급여) OVER () (= 급여 / 합계)",
      col("SELECT ROUND(급여 * 1.0 / SUM(급여) OVER (), 4) FROM 직원 ORDER BY 급여"), [0.1, 0.15, 0.15, 0.25, 0.35])
check("  수진 500 / 2000", 500 / 2000, 0.25)
check("RANK OVER (ORDER BY 급여)", col("SELECT RANK() OVER (ORDER BY 급여) FROM 직원 ORDER BY 급여"), [1, 2, 2, 4, 5])
check("PERCENT_RANK = (순위 - 1) / (행 수 - 1)",
      col("SELECT PERCENT_RANK() OVER (ORDER BY 급여) FROM 직원 ORDER BY 급여"), [0.0, 0.25, 0.25, 0.75, 1.0])
check("CUME_DIST = 나 이하 행 / 행 수",
      col("SELECT CUME_DIST() OVER (ORDER BY 급여) FROM 직원 ORDER BY 급여"), [0.2, 0.6, 0.6, 0.8, 1.0])
positional_any_tie("NTILE(2) (5행 → 3행 + 2행)", "NTILE(2)", [1, 1, 1, 2, 2])

# 시험장 체크용 참고: 10행 NTILE(4) → 3, 3, 2, 2
db.execute("CREATE TABLE t (x INTEGER)")
db.executemany("INSERT INTO t VALUES (?)", [(i,) for i in range(1, 11)])
sizes = [r[1] for r in db.execute("SELECT g, COUNT(*) FROM (SELECT NTILE(4) OVER (ORDER BY x) g FROM t) GROUP BY g ORDER BY g")]
check("(참고) 10행 NTILE(4) 묶음 크기", sizes, [3, 3, 2, 2])

# ── 쇼츠: 40, 50, 50, 60 (본편 숫자와 겹치지 않음) ─────────────────────────────────
db.execute("CREATE TABLE s (k INTEGER, 값 INTEGER)")
db.executemany("INSERT INTO s VALUES (?, ?)", [(1, 40), (2, 50), (3, 50), (4, 60)])
check("쇼츠 ORDER BY만(RANGE)", col("SELECT SUM(값) OVER (ORDER BY 값) FROM s ORDER BY 값"), [40, 140, 140, 200])
check("쇼츠 LAST_VALUE 기본 범위 = 자기 값", col("SELECT LAST_VALUE(값) OVER (ORDER BY 값) FROM s ORDER BY 값"), [40, 50, 50, 60])
check("쇼츠 LAST_VALUE ... UNBOUNDED FOLLOWING", col("""SELECT LAST_VALUE(값) OVER (ORDER BY 값
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) FROM s ORDER BY 값"""), [60] * 4)
for tie in ("ASC", "DESC"):
    check(f"쇼츠 ROWS (동점 순서 {tie})", col(f"""SELECT v FROM (SELECT ROW_NUMBER() OVER w rn,
            SUM(값) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) v FROM s
            WINDOW w AS (ORDER BY 값, k {tie})) ORDER BY rn"""), [40, 90, 140, 200])
    check(f"쇼츠 LAG (동점 순서 {tie})", col(f"""SELECT v FROM (SELECT ROW_NUMBER() OVER w rn, LAG(값) OVER w v FROM s
            WINDOW w AS (ORDER BY 값, k {tie})) ORDER BY rn"""), [None, 40, 50, 50])
    check(f"쇼츠 LEAD (동점 순서 {tie})", col(f"""SELECT v FROM (SELECT ROW_NUMBER() OVER w rn, LEAD(값) OVER w v FROM s
            WINDOW w AS (ORDER BY 값, k {tie})) ORDER BY rn"""), [50, 50, 60, None])

print(f"\n{'모두 맞음' if not fails else f'틀림 {fails}건'} (sqlite {sqlite3.sqlite_version})")
sys.exit(1 if fails else 0)
