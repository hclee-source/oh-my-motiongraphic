"""022 PIVOT · UNPIVOT 예시 숫자 확인(화면에는 안 나옴).

sqlite3에는 PIVOT이 없으므로
- PIVOT  = 오라클 규칙(PIVOT 절에 나오지 않은 모든 열로 암묵적 GROUP BY, IN 목록 값만 열, 없는 칸 NULL)을
           파이썬으로 그대로 재현한 것 + sqlite3의 SUM(CASE …) GROUP BY 꼴, 두 가지가 같은지 본다.
- UNPIVOT = 파이썬 재현(기본 EXCLUDE NULLS / INCLUDE NULLS) + sqlite3의 UNION ALL 꼴.
실행: .venv/Scripts/python.exe concept/episodes/022-sql-pivot/verify_examples.py
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ── 본편 실적 표 7행 ──────────────────────────────────────────────
COLS = ["부서", "분기", "매출", "담당자"]
실적 = [
    ("영업", 1, 90, "민수"),
    ("영업", 1, 60, "지영"),
    ("영업", 2, 120, "민수"),
    ("영업", 3, 110, "민수"),
    ("영업", 4, 130, "민수"),
    ("개발", 1, 70, "현우"),
    ("개발", 3, 80, "현우"),
]


def oracle_pivot(rows, cols, agg, val_col, for_col, in_list):
    """오라클 PIVOT 재현: PIVOT 절(집계 열·FOR 열)에 나오지 않은 모든 열로 묶는다.
    in_list = [(값, 별칭)]. IN 목록에 없는 값은 어떤 칸에도 들어가지 않는다(묶음 자체는 생긴다).
    칸에 해당하는 행이 없으면 NULL(None)."""
    keys = [c for c in cols if c not in (val_col, for_col)]
    ki = [cols.index(c) for c in keys]
    vi, fi = cols.index(val_col), cols.index(for_col)
    groups = {}
    for r in rows:
        g = groups.setdefault(tuple(r[i] for i in ki), {a: [] for _, a in in_list})
        for v, a in in_list:
            if r[fi] == v:
                g[a].append(r[vi])
    out = []
    for k, cells in groups.items():
        out.append(k + tuple(agg(cells[a]) if cells[a] else None for _, a in in_list))
    return keys + [a for _, a in in_list], out


def oracle_unpivot(rows, cols, val_name, for_name, in_cols, include_nulls=False):
    """오라클 UNPIVOT 재현: IN 목록 열마다 한 행. 기본(EXCLUDE NULLS)은 값이 NULL인 칸을 버린다.
    결과 열 순서 = 나머지 열, FOR 열, 값 열. FOR 열에는 원래 열 이름이 문자로 들어간다."""
    keep = [c for c in cols if c not in in_cols]
    out = []
    for r in rows:
        d = dict(zip(cols, r))
        for c in in_cols:
            if d[c] is None and not include_nulls:
                continue
            out.append(tuple(d[k] for k in keep) + (c, d[c]))
    return keep + [for_name, val_name], out


IN = [(1, "Q1"), (2, "Q2"), (3, "Q3")]
ok = True


def check(name, got, want):
    global ok
    same = sorted(got, key=str) == sorted(want, key=str)
    ok &= same
    print(f"{'OK ' if same else 'XX '} {name}: {len(got)}행")
    for r in sorted(got, key=str):
        print("      ", r)
    if not same:
        print("    기대:", sorted(want, key=str))


# 1) 인라인 뷰(부서, 분기, 매출)로 고른 뒤 PIVOT → 남은 열 = 부서 → 2행
inline = [(d, q, s) for d, q, s, _ in 실적]
h, piv2 = oracle_pivot(inline, ["부서", "분기", "매출"], sum, "매출", "분기", IN)
print("열:", h)
check("인라인 뷰 PIVOT", piv2, [("영업", 150, 120, 110), ("개발", 70, None, 80)])

# 2) 실적에 바로 PIVOT → 남은 열 = 부서, 담당자 → 3행
h, piv3 = oracle_pivot(실적, COLS, sum, "매출", "분기", IN)
print("열:", h)
check("실적에 바로 PIVOT", piv3,
      [("영업", "민수", 90, 120, 110), ("영업", "지영", 60, None, None), ("개발", "현우", 70, None, 80)])

# 3) sqlite3 — SUM(CASE …) 꼴(오라클에서도 같은 결과)
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 실적 (부서 TEXT, 분기 INTEGER, 매출 INTEGER, 담당자 TEXT)")
db.executemany("INSERT INTO 실적 VALUES (?, ?, ?, ?)", 실적)
CASES = """SUM(CASE WHEN 분기 = 1 THEN 매출 END) AS Q1,
           SUM(CASE WHEN 분기 = 2 THEN 매출 END) AS Q2,
           SUM(CASE WHEN 분기 = 3 THEN 매출 END) AS Q3"""
check("CASE + GROUP BY 부서 (6장)", db.execute(f"SELECT 부서, {CASES} FROM 실적 GROUP BY 부서").fetchall(), piv2)
check("CASE + GROUP BY 부서, 담당자 (= 바로 PIVOT)",
      db.execute(f"SELECT 부서, 담당자, {CASES} FROM 실적 GROUP BY 부서, 담당자").fetchall(), piv3)
# 4분기 130이 어느 칸에도 없는지
assert all(130 not in r for r in piv2 + piv3)
print("OK  4분기 130은 IN 목록에 없어 결과에 없음")
# 영업 1분기 = 90 + 60
assert 90 + 60 == 150

# 4) UNPIVOT — 4장 결과를 분기실적(부서, Q1, Q2, Q3)으로
db.execute("CREATE TABLE 분기실적 (부서 TEXT, Q1 INTEGER, Q2 INTEGER, Q3 INTEGER)")
db.executemany("INSERT INTO 분기실적 VALUES (?, ?, ?, ?)", piv2)
cells = len(piv2) * 3
nulls = sum(v is None for r in piv2 for v in r[1:])
print(f"칸 {len(piv2)} × 3 = {cells}개, NULL {nulls}개")
h, un5 = oracle_unpivot(piv2, ["부서", "Q1", "Q2", "Q3"], "매출", "분기", ["Q1", "Q2", "Q3"])
print("열:", h)
want5 = [("영업", "Q1", 150), ("영업", "Q2", 120), ("영업", "Q3", 110), ("개발", "Q1", 70), ("개발", "Q3", 80)]
check("UNPIVOT (기본 EXCLUDE NULLS)", un5, want5)
_, un6 = oracle_unpivot(piv2, ["부서", "Q1", "Q2", "Q3"], "매출", "분기", ["Q1", "Q2", "Q3"], include_nulls=True)
check("UNPIVOT INCLUDE NULLS", un6, want5 + [("개발", "Q2", None)])
UNION = " UNION ALL ".join(f"SELECT 부서, '{c}' AS 분기, {c} AS 매출 FROM 분기실적" for c in ["Q1", "Q2", "Q3"])
check("sqlite3 UNION ALL + 매출 IS NOT NULL", db.execute(f"SELECT * FROM ({UNION}) WHERE 매출 IS NOT NULL").fetchall(), want5)
check("sqlite3 UNION ALL (NULL 포함)", db.execute(f"SELECT * FROM ({UNION})").fetchall(), un6)
assert len(un5) == cells - nulls == 5 and len(un6) == cells == 6
assert len(un5) != len(실적)
print(f"OK  PIVOT 뒤 UNPIVOT = {len(un5)}행 ≠ 원래 {len(실적)}행 (150은 다시 안 나뉨, 4분기 130 없음)")

# ── 쇼츠 성적 표 3행(본편과 다른 숫자) ──────────────────────────
print("\n[쇼츠]")
성적 = [("서연", "국어", 85), ("서연", "영어", 95), ("도윤", "국어", 75)]
h, sp = oracle_pivot(성적, ["이름", "과목", "점수"], max, "점수", "과목", [("국어", "국어"), ("영어", "영어")])
print("열:", h)
check("쇼츠 PIVOT", sp, [("서연", 85, 95), ("도윤", 75, None)])
_, su = oracle_unpivot(sp, ["이름", "국어", "영어"], "점수", "과목", ["국어", "영어"])
check("쇼츠 UNPIVOT (기본)", su, [("서연", "국어", 85), ("서연", "영어", 95), ("도윤", "국어", 75)])
_, su4 = oracle_unpivot(sp, ["이름", "국어", "영어"], "점수", "과목", ["국어", "영어"], include_nulls=True)
assert len(su4) == 4
print("OK  쇼츠 UNPIVOT INCLUDE NULLS: 4행")
main_nums = {v for r in 실적 for v in r if isinstance(v, int) and v > 4} | {150}
short_nums = {v for r in 성적 for v in r if isinstance(v, int)}
assert not (main_nums & short_nums), main_nums & short_nums
print("OK  쇼츠 숫자가 본편 숫자와 겹치지 않음")

print("\n모두 일치" if ok else "\n불일치 있음")
sys.exit(0 if ok else 1)
