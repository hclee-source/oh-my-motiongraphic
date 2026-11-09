"""018 정규화 — 대본 예시 숫자 검증(화면에는 안 나옴).

실행(저장소 맨 위에서): .venv/Scripts/python.exe concept/episodes/018-model-normalization/verify_examples.py
- 정리 전 3행 → 제1정규형 5행 → 제2정규형 3개 테이블 → 제3정규형 4개 테이블을 sqlite3로 실제로 나누고,
  행·열 수, 함수 종속, 이상 현상, 저장 횟수, 다시 조인했을 때 처음 5행이 그대로 나오는지(정보 손실 0)를 확인한다.
- 오라클과 같게 하려고 주식별자 열에 NOT NULL을 적는다(sqlite는 PRIMARY KEY 열에도 NULL을 허용하는 예외가 있음).
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ok_all = True


def check(label, got, want):
    global ok_all
    mark = "OK " if got == want else "XX "
    if got != want:
        ok_all = False
    print(f"{mark}{label}: {got}" + ("" if got == want else f"  (기대 {want})"))


# ── 정리 전: 주문 한 건 = 한 행, 상품·수량 칸에 값이 여러 개 ──────────────────
PRODUCTS = {"P1": ("연필", 500), "P2": ("공책", 1500), "P3": ("지우개", 800)}
CUSTOMERS = {"C1": "민수", "C2": "지영"}
RAW = [  # 주문번호, 고객번호, 상품코드들, 수량들
    (1, "C1", "P1, P2", "2, 1"),
    (2, "C2", "P2", "3"),
    (3, "C1", "P2, P3", "1, 2"),
]
check("정리 전 행 수", len(RAW), 3)
check("값이 여러 개인 칸이 있는 행 수", sum(1 for r in RAW if "," in r[2]), 2)

# 제1정규화: 여러 값 칸을 행으로 펼친다
ROWS_1NF = []
for no, cust, codes, qtys in RAW:
    for code, qty in zip(codes.split(", "), qtys.split(", ")):
        name, price = PRODUCTS[code]
        ROWS_1NF.append((no, code, name, price, int(qty), cust, CUSTOMERS[cust]))

EXPECTED_1NF = [
    (1, "P1", "연필", 500, 2, "C1", "민수"),
    (1, "P2", "공책", 1500, 1, "C1", "민수"),
    (2, "P2", "공책", 1500, 3, "C2", "지영"),
    (3, "P2", "공책", 1500, 1, "C1", "민수"),
    (3, "P3", "지우개", 800, 2, "C1", "민수"),
]
check("제1정규형 행 수(3행 → 5행)", len(ROWS_1NF), 5)
check("제1정규형 내용 = 대본 표", ROWS_1NF, EXPECTED_1NF)

db = sqlite3.connect(":memory:")
q = lambda sql, *a: db.execute(sql, a).fetchall()
one = lambda sql, *a: db.execute(sql, a).fetchone()[0]

db.execute("""CREATE TABLE 주문1NF (
    주문번호 INTEGER NOT NULL, 상품코드 TEXT NOT NULL, 상품명 TEXT, 단가 INTEGER, 수량 INTEGER,
    고객번호 TEXT, 고객이름 TEXT, PRIMARY KEY (주문번호, 상품코드))""")
db.executemany("INSERT INTO 주문1NF VALUES (?,?,?,?,?,?,?)", ROWS_1NF)
COLS_1NF = [c[1] for c in q("PRAGMA table_info(주문1NF)")]
check("제1정규형 열 수", len(COLS_1NF), 7)

# ── 주식별자 ──────────────────────────────────────────────────────────────
check("주문번호만의 서로 다른 값 수(5행을 못 가림)", one("SELECT COUNT(DISTINCT 주문번호) FROM 주문1NF"), 3)
check("주문번호 + 상품코드 조합 수(5행 모두 구별)", one("SELECT COUNT(*) FROM (SELECT DISTINCT 주문번호, 상품코드 FROM 주문1NF)"), 5)
check("두 행인 주문(1번·3번)", [r[0] for r in q("SELECT 주문번호 FROM 주문1NF GROUP BY 주문번호 HAVING COUNT(*) = 2")], [1, 3])
check("상품코드만으로 구별되나(서로 다른 값 수)", one("SELECT COUNT(DISTINCT 상품코드) FROM 주문1NF"), 3)


# ── 함수 종속 X → Y: X가 같으면 Y가 하나뿐인가 ─────────────────────────────
def holds(table, xs, ys):
    x = ", ".join(xs)
    y = " || '/' || ".join(f"CAST({c} AS TEXT)" for c in ys)
    bad = q(f"SELECT {x} FROM {table} GROUP BY {x} HAVING COUNT(DISTINCT {y}) > 1")
    return not bad


FDS = [  # 대본의 네 화살표
    (["상품코드"], ["상품명", "단가"]),
    (["주문번호"], ["고객번호"]),
    (["고객번호"], ["고객이름"]),
    (["주문번호", "상품코드"], ["수량"]),
]
for xs, ys in FDS:
    check(f"함수 종속 {' + '.join(xs)} → {', '.join(ys)}", holds("주문1NF", xs, ys), True)
# 수량은 어느 한쪽만으로는 안 정해진다
check("상품코드 → 수량 (성립 안 해야 함)", holds("주문1NF", ["상품코드"], ["수량"]), False)
check("주문번호 → 수량 (성립 안 해야 함)", holds("주문1NF", ["주문번호"], ["수량"]), False)
check("공책(P2)의 주문별 수량", [r[0] for r in q("SELECT 수량 FROM 주문1NF WHERE 상품코드='P2' ORDER BY 주문번호")], [1, 3, 1])
check("1번 주문 안의 상품별 수량", [r[0] for r in q("SELECT 수량 FROM 주문1NF WHERE 주문번호=1 ORDER BY 상품코드")], [2, 1])
# 주문번호 → 고객이름도 성립(고객번호를 거친 이행 종속) → 주식별자 일부(주문번호)에만 종속 = 부분 종속
check("주문번호 → 고객이름 (이행으로 성립)", holds("주문1NF", ["주문번호"], ["고객이름"]), True)

# ── 이상 현상(제1정규형 테이블에서) ─────────────────────────────────────────
db.execute("SAVEPOINT a")
cur = db.execute("UPDATE 주문1NF SET 상품명 = '노트' WHERE 상품코드 = 'P2'")
check("갱신 이상: 공책 → 노트로 고칠 행 수", cur.rowcount, 3)
db.execute("ROLLBACK TO a")
try:
    db.execute("INSERT INTO 주문1NF VALUES (NULL, 'P4', '가위', 1000, NULL, NULL, NULL)")
    check("삽입 이상: 주문번호 없는 가위 넣기", "들어감", "오류")
except sqlite3.IntegrityError as e:
    check("삽입 이상: 주문번호 없는 가위 넣기", "오류", "오류")
cur = db.execute("DELETE FROM 주문1NF WHERE 주문번호 = 3")
check("삭제 이상: 3번 주문을 지우면 지워지는 행 수", cur.rowcount, 2)
check("삭제 이상: 남은 지우개(P3) 행 수", one("SELECT COUNT(*) FROM 주문1NF WHERE 상품코드 = 'P3'"), 0)
db.execute("ROLLBACK TO a")
db.execute("RELEASE a")
check("되돌린 뒤 행 수", one("SELECT COUNT(*) FROM 주문1NF"), 5)

check("저장 횟수(제1): 공책", one("SELECT COUNT(*) FROM 주문1NF WHERE 상품명 = '공책'"), 3)
check("저장 횟수(제1): 민수", one("SELECT COUNT(*) FROM 주문1NF WHERE 고객이름 = '민수'"), 4)

# ── 제2정규형: 부분 함수 종속 제거 → 3개 테이블 ─────────────────────────────
db.executescript("""
CREATE TABLE 주문상품 AS SELECT DISTINCT 주문번호, 상품코드, 수량 FROM 주문1NF;
CREATE TABLE 상품 AS SELECT DISTINCT 상품코드, 상품명, 단가 FROM 주문1NF;
CREATE TABLE 주문2NF AS SELECT DISTINCT 주문번호, 고객번호, 고객이름 FROM 주문1NF;
""")
for t, rows, cols in [("주문상품", 5, 3), ("상품", 3, 3), ("주문2NF", 3, 3)]:
    check(f"제2정규형 {t} 행 × 열", (one(f"SELECT COUNT(*) FROM {t}"), len(q(f"PRAGMA table_info({t})"))), (rows, cols))
check("제2정규형 주문 테이블 내용", q("SELECT * FROM 주문2NF ORDER BY 주문번호"), [(1, "C1", "민수"), (2, "C2", "지영"), (3, "C1", "민수")])
check("제2정규형: 상품 테이블에서 상품코드가 주식별자(중복 없음)", one("SELECT COUNT(DISTINCT 상품코드) FROM 상품"), 3)
check("제2정규형: 주문 테이블에서 주문번호가 주식별자(중복 없음)", one("SELECT COUNT(DISTINCT 주문번호) FROM 주문2NF"), 3)
check("제2정규형: 주문상품의 수량은 주문번호만으로 안 정해짐", holds("주문상품", ["주문번호"], ["수량"]), False)
check("제2정규형: 주문상품의 수량은 상품코드만으로 안 정해짐", holds("주문상품", ["상품코드"], ["수량"]), False)
check("저장 횟수(제2): 공책", one("SELECT COUNT(*) FROM 상품 WHERE 상품명 = '공책'"), 1)
check("저장 횟수(제2): 민수", one("SELECT COUNT(*) FROM 주문2NF WHERE 고객이름 = '민수'"), 2)
db.execute("SAVEPOINT b")
check("제2정규형: 공책 → 노트로 고칠 행 수", db.execute("UPDATE 상품 SET 상품명='노트' WHERE 상품코드='P2'").rowcount, 1)
db.execute("INSERT INTO 상품 VALUES ('P4', '가위', 1000)")
check("제2정규형: 주문 없이 가위 넣기 → 상품 행 수", one("SELECT COUNT(*) FROM 상품"), 4)
db.execute("DELETE FROM 주문상품 WHERE 주문번호 = 3")
db.execute("DELETE FROM 주문2NF WHERE 주문번호 = 3")
check("제2정규형: 3번 주문 지운 뒤 지우개 남음", one("SELECT COUNT(*) FROM 상품 WHERE 상품명='지우개'"), 1)
db.execute("ROLLBACK TO b")
db.execute("SAVEPOINT c")
db.execute("DELETE FROM 주문상품 WHERE 주문번호 = 2")
db.execute("DELETE FROM 주문2NF WHERE 주문번호 = 2")
check("제2정규형에 남은 삭제 이상: 2번(지영의 하나뿐인 주문) 지우면 지영 남은 수", one("SELECT COUNT(*) FROM 주문2NF WHERE 고객이름='지영'"), 0)
db.execute("ROLLBACK TO c")
db.execute("RELEASE c")
db.execute("RELEASE b")
check("되돌린 뒤 상품 행 수(표는 3행 그대로)", one("SELECT COUNT(*) FROM 상품"), 3)
check("지영의 주문 수", one("SELECT COUNT(*) FROM 주문2NF WHERE 고객번호='C2'"), 1)

# 이행 함수 종속: 주문2NF 안에서 고객번호(주식별자 아님) → 고객이름
check("이행: 주문 테이블 안 고객번호 → 고객이름", holds("주문2NF", ["고객번호"], ["고객이름"]), True)
check("이행: 고객번호는 주문 테이블의 식별자가 아님(C1이 두 번)", one("SELECT COUNT(*) FROM 주문2NF WHERE 고객번호='C1'"), 2)

# 제2정규형 재조합 = 처음 5행
J2 = """SELECT op.주문번호, op.상품코드, p.상품명, p.단가, op.수량, o.고객번호, o.고객이름
        FROM 주문상품 op JOIN 상품 p ON p.상품코드 = op.상품코드 JOIN 주문2NF o ON o.주문번호 = op.주문번호"""
check("제2정규형 다시 조인 행 수", one(f"SELECT COUNT(*) FROM ({J2})"), 5)
check("제2정규형 다시 조인 = 처음 표(빠진 행, 생긴 행)",
      (one(f"SELECT COUNT(*) FROM (SELECT * FROM 주문1NF EXCEPT {J2})"), one(f"SELECT COUNT(*) FROM ({J2} EXCEPT SELECT * FROM 주문1NF)")), (0, 0))

# ── 제3정규형: 이행 함수 종속 제거 → 4개 테이블 ─────────────────────────────
db.executescript("""
CREATE TABLE 주문 AS SELECT DISTINCT 주문번호, 고객번호 FROM 주문2NF;
CREATE TABLE 고객 AS SELECT DISTINCT 고객번호, 고객이름 FROM 주문2NF;
""")
for t, rows, cols in [("주문상품", 5, 3), ("상품", 3, 3), ("주문", 3, 2), ("고객", 2, 2)]:
    check(f"제3정규형 {t} 행 × 열", (one(f"SELECT COUNT(*) FROM {t}"), len(q(f"PRAGMA table_info({t})"))), (rows, cols))
check("제3정규형 고객 테이블 내용", q("SELECT * FROM 고객 ORDER BY 고객번호"), [("C1", "민수"), ("C2", "지영")])
check("저장 횟수(제3): 민수", one("SELECT COUNT(*) FROM 고객 WHERE 고객이름 = '민수'"), 1)
check("열 수 합: 7 → 3+3+3 → 3+3+2+2", [7, 3 + 3 + 3, 3 + 3 + 2 + 2], [7, 9, 10])
db.execute("SAVEPOINT d")
db.execute("DELETE FROM 주문상품 WHERE 주문번호 = 2")
db.execute("DELETE FROM 주문 WHERE 주문번호 = 2")
check("제3정규형: 2번 주문 지워도 지영 남음", one("SELECT COUNT(*) FROM 고객 WHERE 고객이름='지영'"), 1)
db.execute("ROLLBACK TO d")
db.execute("RELEASE d")

J3 = """SELECT op.주문번호, op.상품코드, p.상품명, p.단가, op.수량, o.고객번호, c.고객이름
        FROM 주문상품 op JOIN 상품 p ON p.상품코드 = op.상품코드
                         JOIN 주문 o ON o.주문번호 = op.주문번호
                         JOIN 고객 c ON c.고객번호 = o.고객번호"""
check("제3정규형 네 테이블 다시 조인 행 수", one(f"SELECT COUNT(*) FROM ({J3})"), 5)
check("제3정규형 다시 조인 = 처음 표(빠진 행, 생긴 행)",
      (one(f"SELECT COUNT(*) FROM (SELECT * FROM 주문1NF EXCEPT {J3})"), one(f"SELECT COUNT(*) FROM ({J3} EXCEPT SELECT * FROM 주문1NF)")), (0, 0))
check("제3정규형 다시 조인 내용", sorted(q(J3)), EXPECTED_1NF)

# BCNF 확인: 나눈 네 테이블에서 남은 결정자는 모두 각 테이블의 식별자(후보키)
for t, key, others in [("주문상품", ["주문번호", "상품코드"], ["수량"]), ("상품", ["상품코드"], ["상품명", "단가"]),
                       ("주문", ["주문번호"], ["고객번호"]), ("고객", ["고객번호"], ["고객이름"])]:
    uniq = one(f"SELECT COUNT(*) FROM (SELECT DISTINCT {', '.join(key)} FROM {t})") == one(f"SELECT COUNT(*) FROM {t}")
    check(f"BCNF: {t}의 결정자 {' + '.join(key)}가 식별자(중복 없음)", uniq, True)

# 상품 목록: 제1정규형 표는 5행을 훑어 중복을 걸러야 3개, 정규화 뒤엔 상품 테이블 3행만 읽으면 됨
check("상품 목록: 제1정규형 표에서 DISTINCT", (one("SELECT COUNT(*) FROM 주문1NF"), one("SELECT COUNT(DISTINCT 상품코드) FROM 주문1NF")), (5, 3))
check("상품 목록: 상품 테이블 행 수", one("SELECT COUNT(*) FROM 상품"), 3)

# ── 쇼츠 예시(숫자 없음): 수강(학번, 과목, 성적, 이름, 학과, 학과장)도 같은 방식으로 손실 없이 나뉘는지 ──
db.executescript("""
CREATE TABLE 수강1NF (학번 INTEGER NOT NULL, 과목 TEXT NOT NULL, 성적 TEXT, 이름 TEXT, 학과 TEXT, 학과장 TEXT, PRIMARY KEY (학번, 과목));
INSERT INTO 수강1NF VALUES (1, '수학', 'A', '하나', '경영', '김교수'), (1, '영어', 'B', '하나', '경영', '김교수'),
                           (2, '수학', 'B', '두리', '경영', '김교수'), (3, '영어', 'A', '세찬', '통계', '박교수');
CREATE TABLE 수강 AS SELECT DISTINCT 학번, 과목, 성적 FROM 수강1NF;
CREATE TABLE 학생 AS SELECT DISTINCT 학번, 이름, 학과 FROM 수강1NF;
CREATE TABLE 학과 AS SELECT DISTINCT 학과, 학과장 FROM 수강1NF;
""")
check("쇼츠: 학번 → 이름 (부분 종속)", holds("수강1NF", ["학번"], ["이름"]), True)
check("쇼츠: 학과 → 학과장 (이행 종속의 뒤쪽)", holds("수강1NF", ["학과"], ["학과장"]), True)
JS = """SELECT s.학번, s.과목, s.성적, h.이름, h.학과, d.학과장 FROM 수강 s JOIN 학생 h ON h.학번 = s.학번 JOIN 학과 d ON d.학과 = h.학과"""
check("쇼츠: 다시 조인 = 처음 표", (one(f"SELECT COUNT(*) FROM (SELECT * FROM 수강1NF EXCEPT {JS})"), one(f"SELECT COUNT(*) FROM ({JS} EXCEPT SELECT * FROM 수강1NF)")), (0, 0))

print("\n전부 일치" if ok_all else "\n불일치 있음")
sys.exit(0 if ok_all else 1)
