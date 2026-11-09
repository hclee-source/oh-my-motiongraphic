"""021 식별자와 관계 — 대본 예시 확인(화면에는 안 나옴).

1) 인조식별자(주문상품번호) 주식별자: 4행 모두 들어감, 1행과 4행이 (주문번호, 상품코드) 중복
2) 본질식별자(주문번호, 상품코드) 주식별자: 4행째 거부 → 3행
3) 인조식별자 + UNIQUE(주문번호, 상품코드): 인덱스 2개(주식별자 + UNIQUE). 오라클도 UNIQUE 제약에 유일 인덱스를 자동 생성
4) 비식별자 관계(고객–주문): 주문상품에는 고객번호가 없어서 고객별 주문상품은 주문과 조인해야 함
5) 식별자 관계 사슬: 주문상품 아래 배송 주식별자 = 주문번호 + 상품코드 + 배송순번 (3칸)
6) 주문상품 최소성: 주문번호만, 상품코드만으로는 유일하지 않음
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROWS = [(1, 1001, "P01", 2), (2, 1001, "P02", 1), (3, 1002, "P01", 3), (4, 1001, "P01", 2)]


def load(ddl):
    con = sqlite3.connect(":memory:")
    con.execute(ddl)
    ok = 0
    rejected = []
    for r in ROWS:
        try:
            con.execute("INSERT INTO 주문상품 VALUES (?, ?, ?, ?)", r)
            ok += 1
        except sqlite3.IntegrityError as e:
            rejected.append((r, str(e)))
    return con, ok, rejected


# 1) 인조식별자
con, ok, rej = load("CREATE TABLE 주문상품 (주문상품번호 INTEGER PRIMARY KEY, 주문번호 INT, 상품코드 TEXT, 수량 INT)")
dups = con.execute("SELECT 주문번호, 상품코드, COUNT(*) FROM 주문상품 GROUP BY 주문번호, 상품코드 HAVING COUNT(*) > 1").fetchall()
print("1) 인조식별자 PK: 들어간 행", ok, "/ 거부", len(rej), "/ 중복 (주문번호, 상품코드)", dups)
assert ok == 4 and dups == [(1001, "P01", 2)]

# 2) 본질식별자
con, ok, rej = load("CREATE TABLE 주문상품 (주문상품번호 INT, 주문번호 INT, 상품코드 TEXT, 수량 INT, PRIMARY KEY (주문번호, 상품코드))")
print("2) 본질식별자 PK: 들어간 행", ok, "/ 거부", [r for r, _ in rej])
assert ok == 3 and rej[0][0][0] == 4

# 3) 인조식별자 + UNIQUE → 인덱스 2개 (sqlite는 INTEGER PRIMARY KEY가 rowid라 인덱스를 안 만들므로 오라클처럼 별도 PK 인덱스를 두는 형태로 확인)
con, ok, rej = load("CREATE TABLE 주문상품 (주문상품번호 INT PRIMARY KEY, 주문번호 INT, 상품코드 TEXT, 수량 INT, UNIQUE (주문번호, 상품코드))")
idx = con.execute("SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = '주문상품'").fetchall()
print("3) 인조식별자 + UNIQUE: 인덱스", len(idx), "개", idx, "/ 들어간 행", ok)
assert len(idx) == 2 and ok == 3

# 4) 비식별자 관계: 고객번호는 주문의 일반 속성, 주문상품에는 없음 → 조인 필요
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE 고객 (고객번호 TEXT PRIMARY KEY, 이메일 TEXT UNIQUE, 이름 TEXT);
CREATE TABLE 주문 (주문번호 INT PRIMARY KEY, 주문일자 TEXT, 고객번호 TEXT NOT NULL REFERENCES 고객);
CREATE TABLE 상품 (상품코드 TEXT PRIMARY KEY, 상품명 TEXT, 가격 INT);
CREATE TABLE 주문상품 (주문번호 INT REFERENCES 주문, 상품코드 TEXT REFERENCES 상품, 수량 INT, PRIMARY KEY (주문번호, 상품코드));
INSERT INTO 고객 VALUES ('C01', 'a@x.kr', '민수'), ('C02', 'b@x.kr', '지영');
INSERT INTO 주문 VALUES (1001, '2026-11-01', 'C01'), (1002, '2026-11-02', 'C02');
INSERT INTO 상품 VALUES ('P01', '펜', 1000), ('P02', '공책', 2000);
INSERT INTO 주문상품 VALUES (1001, 'P01', 2), (1001, 'P02', 1), (1002, 'P01', 3);
""")
cols = [c[1] for c in con.execute("PRAGMA table_info(주문상품)")]
print("4) 주문상품 열", cols, "→ 고객번호 없음:", "고객번호" not in cols)
assert "고객번호" not in cols
rows = con.execute("""SELECT op.주문번호, op.상품코드 FROM 주문상품 op JOIN 주문 o ON o.주문번호 = op.주문번호
                      WHERE o.고객번호 = 'C01' ORDER BY 1, 2""").fetchall()
print("   고객 C01의 주문상품(주문을 거쳐 조인)", rows)
assert rows == [(1001, "P01"), (1001, "P02")]

# 5) 식별자 관계 사슬: 배송 주식별자 3칸
con.execute("""CREATE TABLE 배송 (주문번호 INT, 상품코드 TEXT, 배송순번 INT, 배송일자 TEXT,
               PRIMARY KEY (주문번호, 상품코드, 배송순번), FOREIGN KEY (주문번호, 상품코드) REFERENCES 주문상품)""")
pk = [c[1] for c in con.execute("PRAGMA table_info(배송)") if c[5] > 0]
print("5) 배송 주식별자", pk, len(pk), "칸")
assert len(pk) == 3

# 6) 주문상품 최소성: 한 속성만으로는 유일하지 않음
by_order = con.execute("SELECT COUNT(*) FROM 주문상품 GROUP BY 주문번호 HAVING COUNT(*) > 1").fetchall()
by_item = con.execute("SELECT COUNT(*) FROM 주문상품 GROUP BY 상품코드 HAVING COUNT(*) > 1").fetchall()
print("6) 주문번호만 중복 묶음", len(by_order), "/ 상품코드만 중복 묶음", len(by_item), "→ 둘 다 필요")
assert by_order and by_item

print("모두 확인")
