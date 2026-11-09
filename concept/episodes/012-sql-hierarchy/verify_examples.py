"""012 계층형 질의와 셀프 조인 — 대본 숫자 검증(화면에는 안 나옴).

sqlite 재귀 CTE로 오라클 CONNECT BY를 흉내 낸다.
- PRIOR 쪽 = 이미 읽은 행(h), 반대쪽 = 새로 이을 행(c).
- ORDER SIBLINGS BY 사원번호 = 출발점부터의 사원번호 경로(0 채운 문자열)로 정렬 → 깊이 우선(전위) 순서.
- WHERE는 다 펼친 뒤 행마다 거르고, CONNECT BY의 AND 조건은 잇는 단계(c)에서 걸러 그 아래 가지가 통째로 사라진다.
- 시작 행(START WITH)에는 CONNECT BY 조건이 적용되지 않는다(오라클 규칙).
파이썬 깊이 우선 탐색으로 한 번 더 따로 계산해 두 결과를 대조한다.

실행: .venv/Scripts/python.exe concept/episodes/012-sql-hierarchy/verify_examples.py
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROWS = [  # 사원번호, 이름, 관리자번호
    (1, "김대표", None),
    (2, "이부장", 1),
    (3, "박부장", 1),
    (4, "최과장", 2),
    (5, "정대리", 2),
    (6, "한사원", 4),
    (7, "윤과장", 3),
]

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 사원 (사원번호 INTEGER, 이름 TEXT, 관리자번호 INTEGER)")
db.executemany("INSERT INTO 사원 VALUES (?, ?, ?)", ROWS)

DOWN = "h.사원번호 = c.관리자번호"   # CONNECT BY PRIOR 사원번호 = 관리자번호 (순방향)
UP = "h.관리자번호 = c.사원번호"     # CONNECT BY PRIOR 관리자번호 = 사원번호 (역방향)


def connect_by(start, link, extra="1=1", where="1=1"):
    sql = f"""
    WITH RECURSIVE h(사원번호, 이름, 관리자번호, lvl, k, root, path) AS (
      SELECT 사원번호, 이름, 관리자번호, 1, printf('%03d', 사원번호), 이름, '/' || 이름
      FROM 사원 WHERE {start}
      UNION ALL
      SELECT c.사원번호, c.이름, c.관리자번호, h.lvl + 1, h.k || '.' || printf('%03d', c.사원번호),
             h.root, h.path || '/' || c.이름
      FROM h JOIN 사원 c ON {link} AND ({extra.replace('사원번호', 'c.사원번호')})
    )
    SELECT lvl, 이름, 사원번호,
           CASE WHEN EXISTS (SELECT 1 FROM 사원 c WHERE {link.replace('h.', 'x.')}
                             AND ({extra.replace('사원번호', 'c.사원번호')}))
                THEN 0 ELSE 1 END AS isleaf,
           root, path
    FROM h AS x
    WHERE {where}
    ORDER BY k
    """
    return db.execute(sql).fetchall()


# 파이썬으로 따로: 깊이 우선 전위 순회
def dfs(start_ids, direction, cut=None, drop=None):
    by_id = {r[0]: r for r in ROWS}
    out = []

    def nxt(r):
        if direction == "down":
            kids = [x for x in ROWS if x[2] is not None and x[2] == r[0]]
        else:
            kids = [x for x in ROWS if r[2] is not None and x[0] == r[2]]
        kids = [x for x in kids if cut is None or x[0] != cut]
        return sorted(kids, key=lambda x: x[0])  # ORDER SIBLINGS BY 사원번호

    def walk(r, lvl):
        out.append((lvl, r[1]))
        for k in nxt(r):
            walk(k, lvl + 1)

    for s in start_ids:
        walk(by_id[s], 1)
    return [x for x in out if drop is None or x[1] != drop]


def show(title, rows, check):
    got = [(r[0], r[1]) for r in rows]
    assert got == check, (title, got, check)
    print(f"{title} → {len(rows)}행")
    for r in rows:
        print("   LEVEL", r[0], r[1])


print("사원 7행:", ", ".join(f"{a} {b} {c if c else 'NULL'}" for a, b, c in ROWS))
print()

# 1장·3장·4장: 순방향, 김대표에서 출발
fw = connect_by("관리자번호 IS NULL", DOWN)
show("START WITH 관리자번호 IS NULL / CONNECT BY PRIOR 사원번호 = 관리자번호 / ORDER SIBLINGS BY 사원번호",
     fw, dfs([1], "down"))
assert [r[0] for r in fw] == [1, 2, 3, 4, 3, 2, 3]
assert [r[1] for r in fw] == ["김대표", "이부장", "최과장", "한사원", "정대리", "박부장", "윤과장"]

# 1장·5장: 같은 출발점, PRIOR를 관리자번호 쪽으로 → 김대표 위에 상사가 없어 1행
rv0 = connect_by("관리자번호 IS NULL", UP)
show("START WITH 관리자번호 IS NULL / CONNECT BY PRIOR 관리자번호 = 사원번호", rv0, dfs([1], "up"))
assert len(rv0) == 1

# 5장: 역방향, 한사원(6)에서 출발 → 위로 4행
rv = connect_by("사원번호 = 6", UP)
show("START WITH 사원번호 = 6 / CONNECT BY PRIOR 관리자번호 = 사원번호", rv, dfs([6], "up"))
assert [(r[0], r[1]) for r in rv] == [(1, "한사원"), (2, "최과장"), (3, "이부장"), (4, "김대표")]

# 6장: WHERE 사원번호 <> 2 → 다 펼친 뒤 이부장 한 행만 빠짐(부하 셋은 LEVEL 그대로) 6행
w = connect_by("관리자번호 IS NULL", DOWN, where="사원번호 <> 2")
show("WHERE 사원번호 <> 2 (나머지 같음)", w, dfs([1], "down", drop="이부장"))
assert len(w) == 6 and [(r[0], r[1]) for r in w if r[1] == "최과장"] == [(3, "최과장")]

# 6장: CONNECT BY ... AND 사원번호 <> 2 → 이부장 가지(이부장·최과장·한사원·정대리) 통째로 빠짐 3행
c = connect_by("관리자번호 IS NULL", DOWN, extra="사원번호 <> 2")
show("CONNECT BY PRIOR 사원번호 = 관리자번호 AND 사원번호 <> 2", c, dfs([1], "down", cut=2))
assert [r[1] for r in c] == ["김대표", "박부장", "윤과장"]

# 7장: 전용 함수(순방향 결과 기준)
print()
print("CONNECT_BY_ISLEAF / CONNECT_BY_ROOT 이름 / SYS_CONNECT_BY_PATH(이름, 빗금)")
for r in fw:
    print(f"   {r[1]}  ISLEAF {r[3]}  ROOT {r[4]}  PATH {r[5]}")
assert [r[3] for r in fw] == [0, 0, 0, 1, 1, 0, 1]
assert {r[1] for r in fw if r[3] == 1} == {"한사원", "정대리", "윤과장"}
assert all(r[4] == "김대표" for r in fw)
assert dict((r[1], r[5]) for r in fw)["한사원"] == "/김대표/이부장/최과장/한사원"

# 8장: 셀프 조인 — 별칭 부하(각 사원), 상사
print()
inner = db.execute("""SELECT 부하.이름, 상사.이름 FROM 사원 부하 JOIN 사원 상사 ON 부하.관리자번호 = 상사.사원번호
                      ORDER BY 부하.사원번호""").fetchall()
left = db.execute("""SELECT 부하.이름, 상사.이름 FROM 사원 부하 LEFT OUTER JOIN 사원 상사 ON 부하.관리자번호 = 상사.사원번호
                     ORDER BY 부하.사원번호""").fetchall()
print(f"셀프 조인 INNER (부하.관리자번호 = 상사.사원번호) → {len(inner)}행:", ", ".join(f"{a}-{b}" for a, b in inner))
print(f"셀프 조인 LEFT OUTER → {len(left)}행:", ", ".join(f"{a}-{b if b else 'NULL'}" for a, b in left))
assert len(inner) == 6 and "김대표" not in [a for a, _ in inner]
assert len(left) == 7 and left[0] == ("김대표", None)
assert inner == [("이부장", "김대표"), ("박부장", "김대표"), ("최과장", "이부장"),
                 ("정대리", "이부장"), ("한사원", "최과장"), ("윤과장", "박부장")]

# 쇼츠: 본편과 다른 작은 상품 분류 나무 — 식품(맨 위), 과일 · 채소(식품 아래), 사과(과일 아래)
# 형제 순서는 ORDER SIBLINGS BY 분류(가나다순: 과일 < 채소). 경로 정렬은 형제 순번(0 채움)으로.
print()
s = sqlite3.connect(":memory:")
s.execute("CREATE TABLE t (분류 TEXT, 상위분류 TEXT)")
s.executemany("INSERT INTO t VALUES (?, ?)", [("식품", None), ("과일", "식품"), ("채소", "식품"), ("사과", "과일")])
assert sorted(["채소", "과일"]) == ["과일", "채소"]  # 유니코드 순 = 가나다순


def tree(link, start, extra="1=1", where="1=1"):
    return s.execute(f"""
    WITH RECURSIVE h(분류, 상위분류, lvl, k) AS (
      SELECT 분류, 상위분류, 1, 분류 FROM t WHERE {start}
      UNION ALL
      SELECT c.분류, c.상위분류, h.lvl + 1, h.k || char(1) || c.분류
      FROM h JOIN t c ON {link} AND ({extra})
    ) SELECT lvl, 분류 FROM h WHERE {where} ORDER BY k""").fetchall()


down = tree("h.분류 = c.상위분류", "상위분류 IS NULL")                        # PRIOR 분류 = 상위분류
up = tree("h.상위분류 = c.분류", "분류 = '사과'")                             # PRIOR 상위분류 = 분류
sw = tree("h.분류 = c.상위분류", "상위분류 IS NULL", where="분류 <> '과일'")
sc = tree("h.분류 = c.상위분류", "상위분류 IS NULL", extra="c.분류 <> '과일'")
print("쇼츠 순방향(PRIOR 분류 = 상위분류):", down)
print("쇼츠 역방향(사과에서, PRIOR 상위분류 = 분류):", up)
print("쇼츠 WHERE 분류 <> '과일':", sw)
print("쇼츠 CONNECT BY ... AND 분류 <> '과일':", sc)
assert down == [(1, "식품"), (2, "과일"), (3, "사과"), (2, "채소")]
assert up == [(1, "사과"), (2, "과일"), (3, "식품")]
assert sw == [(1, "식품"), (3, "사과"), (2, "채소")]
assert sc == [(1, "식품"), (2, "채소")]

print()
print("모든 검증 통과")
