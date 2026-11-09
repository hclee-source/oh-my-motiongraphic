"""017 집합 연산자 — 대본 숫자 검증(화면에는 안 나옴).

sqlite3로 UNION ALL · UNION · INTERSECT · EXCEPT(오라클 MINUS)를 실제로 실행해 행 수를 확인한다.
실행(저장소 맨 위에서): .venv/Scripts/python.exe concept/episodes/017-sql-set/verify_examples.py
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

con = sqlite3.connect(":memory:")
cur = con.cursor()

# ── 본편: 봄응모 4행(지영 두 번), 여름응모 3행(수진 두 번), 양쪽에 현우 ──
SPRING = ["민수", "지영", "지영", "현우"]
SUMMER = ["현우", "수진", "수진"]
cur.execute("CREATE TABLE 봄응모 (이름 TEXT)")
cur.execute("CREATE TABLE 여름응모 (이름 TEXT)")
cur.executemany("INSERT INTO 봄응모 (이름) VALUES (?)", [(n,) for n in SPRING])
cur.executemany("INSERT INTO 여름응모 (이름) VALUES (?)", [(n,) for n in SUMMER])

checks = []


def run(label, sql, expect_rows):
    rows = [r[0] for r in cur.execute(sql).fetchall()]
    ok = sorted(rows) == sorted(expect_rows)
    checks.append(ok)
    print(f"{'OK ' if ok else 'NG '} {label}: {len(rows)}행 {sorted(rows)}  (기대 {len(expect_rows)}행)")
    return rows


A = "SELECT 이름 FROM 봄응모"
B = "SELECT 이름 FROM 여름응모"
print("== 본편 ==")
print(f"봄응모 {len(SPRING)}행 {SPRING} / 여름응모 {len(SUMMER)}행 {SUMMER}")
run("UNION ALL", f"{A} UNION ALL {B}", SPRING + SUMMER)                      # 7
run("UNION", f"{A} UNION {B}", ["민수", "지영", "현우", "수진"])              # 4
run("INTERSECT", f"{A} INTERSECT {B}", ["현우"])                            # 1
run("봄 MINUS 여름 (EXCEPT)", f"{A} EXCEPT {B}", ["민수", "지영"])           # 2
run("여름 MINUS 봄 (EXCEPT)", f"{B} EXCEPT {A}", ["수진"])                   # 1
# UNION으로 빠지는 행 = 7 - 4 = 3 (지영 하나, 현우 하나, 수진 하나)
assert len(SPRING) + len(SUMMER) - 4 == 3

# 문장 26: 현우가 봄에 두 번 응모했더라도 INTERSECT는 1행
cur.execute("CREATE TABLE 봄응모2 AS SELECT * FROM 봄응모")
cur.execute("INSERT INTO 봄응모2 (이름) VALUES ('현우')")
run("가정: 봄에 현우 두 번 → INTERSECT", f"SELECT 이름 FROM 봄응모2 INTERSECT {B}", ["현우"])

# 순서를 바꿔도 같은 것(UNION ALL · UNION · INTERSECT) — 나오는 행이 같다
for op in ["UNION ALL", "UNION", "INTERSECT"]:
    r1 = sorted(r[0] for r in cur.execute(f"{A} {op} {B}"))
    r2 = sorted(r[0] for r in cur.execute(f"{B} {op} {A}"))
    checks.append(r1 == r2)
    print(f"{'OK ' if r1 == r2 else 'NG '} {op} 위아래 바꿔도 같은 행: {r1 == r2}")

# 결과 열 이름은 첫 번째 SELECT의 별칭(응모자)
cur.execute("SELECT 이름 AS 응모자 FROM 봄응모 UNION SELECT 이름 AS 고객 FROM 여름응모")
name = cur.description[0][0]
checks.append(name == "응모자")
print(f"{'OK ' if name == '응모자' else 'NG '} 결과 열 이름 = {name}")

# 열 개수가 다르면 오류
try:
    cur.execute("SELECT 이름, '봄' FROM 봄응모 UNION SELECT 이름 FROM 여름응모")
    checks.append(False)
    print("NG  열 개수 다름 → 오류가 안 남")
except sqlite3.OperationalError as e:
    checks.append(True)
    print(f"OK  열 개수 다름 → 오류: {e}")

# ORDER BY는 맨 끝에 한 번 — 첫 번째 SELECT 뒤에 적으면 오류
try:
    cur.execute("SELECT 이름 FROM 봄응모 ORDER BY 이름 UNION SELECT 이름 FROM 여름응모")
    checks.append(False)
    print("NG  첫 SELECT 뒤 ORDER BY → 오류가 안 남")
except sqlite3.OperationalError as e:
    checks.append(True)
    print(f"OK  첫 SELECT 뒤 ORDER BY → 오류: {e}")

# 맨 끝 ORDER BY: 첫 SELECT 별칭 / 열 순서 번호 → 전체 결과 정렬
r_alias = [r[0] for r in cur.execute(
    "SELECT 이름 AS 응모자 FROM 봄응모 UNION SELECT 이름 AS 고객 FROM 여름응모 ORDER BY 응모자")]
r_pos = [r[0] for r in cur.execute(
    "SELECT 이름 AS 응모자 FROM 봄응모 UNION SELECT 이름 AS 고객 FROM 여름응모 ORDER BY 1")]
ok = r_alias == r_pos == sorted(r_alias) and len(r_alias) == 4
checks.append(ok)
print(f"{'OK ' if ok else 'NG '} 맨 끝 ORDER BY 응모자 / ORDER BY 1 → {r_alias}")

# NULL: 집합 연산자는 NULL끼리 같은 행으로 본다(등호 비교와 다름)
n_union = cur.execute("SELECT NULL UNION SELECT NULL").fetchall()
n_inter = cur.execute("SELECT NULL INTERSECT SELECT NULL").fetchall()
n_minus = cur.execute("SELECT NULL EXCEPT SELECT NULL").fetchall()
n_eq = cur.execute("SELECT COUNT(*) FROM (SELECT NULL AS x) WHERE x = NULL").fetchone()[0]
ok = len(n_union) == 1 and len(n_inter) == 1 and len(n_minus) == 0 and n_eq == 0
checks.append(ok)
print(f"{'OK ' if ok else 'NG '} NULL: UNION {len(n_union)}행, INTERSECT {len(n_inter)}행, "
      f"MINUS {len(n_minus)}행, 등호 비교 NULL = NULL → {n_eq}행")

# ── 쇼츠: 본편과 다른 값(가~바). A 3행, B 6행(바 두 번), 겹친 값 나 · 다 ──
print("\n== 쇼츠 ==")
SA = ["가", "나", "다"]
SB = ["나", "다", "라", "마", "바", "바"]
cur.execute("CREATE TABLE SA (v TEXT)")
cur.execute("CREATE TABLE SB (v TEXT)")
cur.executemany("INSERT INTO SA VALUES (?)", [(x,) for x in SA])
cur.executemany("INSERT INTO SB VALUES (?)", [(x,) for x in SB])
print(f"A {len(SA)}행 {SA} / B {len(SB)}행 {SB}")
qa, qb = "SELECT v FROM SA", "SELECT v FROM SB"
run("UNION ALL", f"{qa} UNION ALL {qb}", SA + SB)                         # 9
run("UNION", f"{qa} UNION {qb}", ["가", "나", "다", "라", "마", "바"])      # 6
run("INTERSECT", f"{qa} INTERSECT {qb}", ["나", "다"])                    # 2
run("A MINUS B", f"{qa} EXCEPT {qb}", ["가"])                              # 1
run("B MINUS A", f"{qb} EXCEPT {qa}", ["라", "마", "바"])                  # 3

print("\n모두 통과" if all(checks) else f"\n실패 {checks.count(False)}건")
sys.exit(0 if all(checks) else 1)
