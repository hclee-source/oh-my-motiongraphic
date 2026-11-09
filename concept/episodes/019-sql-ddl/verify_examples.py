"""019 DELETE · TRUNCATE · DROP과 제약 조건 — 대본 예시 숫자 확인(화면에는 쓰지 않음).

실행(저장소 맨 위에서): .venv/Scripts/python.exe concept/episodes/019-sql-ddl/verify_examples.py

sqlite3로 확인할 수 있는 것: DELETE(WHERE 유무)·ROLLBACK, 제약 조건 INSERT 여섯 번, 부모 행 삭제(기본·CASCADE·SET NULL),
UNIQUE 열의 NULL 여러 개.
sqlite3로 확인할 수 없는 것(오라클 규칙, 대본 예시 숫자에 적어 둠):
  · 오라클에서 TRUNCATE·DROP은 DDL → 실행 앞뒤로 자동 커밋 → 뒤이은 ROLLBACK은 되돌릴 것이 없다.
    (sqlite는 DDL도 트랜잭션 안에서 되돌릴 수 있어 오라클과 다르다. 그래서 아래에서는 ‘DDL 뒤 자동 커밋’을
     COMMIT을 직접 불러 흉내 낸다. sqlite에는 TRUNCATE가 없어 WHERE 없는 DELETE + COMMIT으로 흉내 낸다.)
  · DROP 뒤 조회 → ORA-00942(표 또는 뷰가 존재하지 않음).
  · 오라클 기본 FK(ON DELETE 절 없음)에서 자식 있는 부모 삭제 → ORA-02292. sqlite 기본(NO ACTION)도 실패로 같다.
  · 오라클 PK는 NOT NULL을 포함한다. sqlite는 INTEGER가 아닌 PK에 NULL을 허용하는 옛 동작이 있어 NOT NULL을 따로 적었다.
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ORDERS = [(101, 120), (102, 80), (103, 250), (104, 60), (105, 300)]


def orders_db():
    db = sqlite3.connect(":memory:", isolation_level=None)  # 트랜잭션은 BEGIN/COMMIT/ROLLBACK으로 직접
    db.execute("CREATE TABLE 주문 (주문번호 NUMBER PRIMARY KEY NOT NULL, 금액 NUMBER)")
    db.executemany("INSERT INTO 주문 VALUES (?, ?)", ORDERS)
    return db


def count(db, t):
    return db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]


print("== 1부: 주문 표 5행 ==")
# DELETE(WHERE 없음) → ROLLBACK
db = orders_db()
db.execute("BEGIN")
db.execute("DELETE FROM 주문")
after_delete = count(db, "주문")
db.execute("ROLLBACK")
print(f"DELETE FROM 주문 → {after_delete}행, ROLLBACK → {count(db, '주문')}행")
assert (after_delete, count(db, "주문")) == (0, 5)

# DELETE ... WHERE 금액 < 100
db.execute("BEGIN")
gone = [r for r in db.execute("SELECT 주문번호, 금액 FROM 주문 WHERE 금액 < 100 ORDER BY 주문번호")]
db.execute("DELETE FROM 주문 WHERE 금액 < 100")
left = [r for r in db.execute("SELECT 주문번호, 금액 FROM 주문 ORDER BY 주문번호")]
db.execute("ROLLBACK")
print(f"DELETE … WHERE 금액 < 100 → 지워진 행 {gone}, 남은 {len(left)}행 {left}")
assert gone == [(102, 80), (104, 60)] and len(left) == 3

# TRUNCATE 흉내: 전부 지우고 곧바로 커밋(오라클 DDL 자동 커밋) → ROLLBACK
db = orders_db()
db.execute("BEGIN")
db.execute("DELETE FROM 주문")
db.execute("COMMIT")  # 오라클: TRUNCATE는 DDL이라 자동 커밋
db.execute("BEGIN")
db.execute("ROLLBACK")
cols = [r[1] for r in db.execute("PRAGMA table_info(주문)")]
print(f"TRUNCATE(흉내) → ROLLBACK → {count(db, '주문')}행, 표 구조 남음 {cols}")
assert count(db, "주문") == 0 and cols == ["주문번호", "금액"]

# DROP: 구조째 삭제 + 자동 커밋 → ROLLBACK 뒤 조회하면 오류
db = orders_db()
db.execute("DROP TABLE 주문")  # isolation_level=None이라 바로 확정(오라클 자동 커밋과 같은 결과)
db.execute("BEGIN")
db.execute("ROLLBACK")
try:
    db.execute("SELECT * FROM 주문")
    raise AssertionError("표가 남아 있으면 안 됨")
except sqlite3.OperationalError as e:
    print(f"DROP → ROLLBACK → 조회 오류: {e}  (오라클 ORA-00942)")

print()
print("== 2부: 부서(부모) · 사원(자식) ==")


def emp_db(on_delete=""):
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("CREATE TABLE 부서 (부서번호 NUMBER PRIMARY KEY NOT NULL, 부서명 VARCHAR(20) UNIQUE)")
    db.execute(f"""CREATE TABLE 사원 (
        사번 NUMBER PRIMARY KEY NOT NULL,
        이름 VARCHAR(20) NOT NULL,
        급여 NUMBER CHECK (급여 > 0),
        부서번호 NUMBER REFERENCES 부서(부서번호) {on_delete})""")
    db.executemany("INSERT INTO 부서 VALUES (?, ?)", [(10, "영업"), (20, "개발")])
    db.executemany("INSERT INTO 사원 VALUES (?, ?, ?, ?)",
                   [(1, "민수", 300, 10), (2, "지영", 400, 20), (3, "현우", 350, 10)])
    return db


INSERTS = [
    (4, "수진", 380, 20),    # ① 성공
    (4, "동훈", 300, 10),    # ② PK 중복
    (5, None, 300, 10),      # ③ NOT NULL
    (5, "동훈", 0, 10),      # ④ CHECK (급여 > 0)
    (5, "동훈", 300, 30),    # ⑤ FK: 부서 30 없음
    (5, "동훈", 300, None),  # ⑥ 성공: FK 열은 NULL 허용
]
EXPECT = ["성공", "실패", "실패", "실패", "실패", "성공"]


def run_inserts(db, verbose=False):
    results = []
    for i, v in enumerate(INSERTS, 1):
        try:
            db.execute("INSERT INTO 사원 VALUES (?, ?, ?, ?)", v)
            results.append("성공")
            msg = "성공"
        except sqlite3.IntegrityError as e:
            results.append("실패")
            msg = f"실패 ({e})"
        if verbose:
            print(f"  {'①②③④⑤⑥'[i - 1]} VALUES {v} → {msg} → 사원 {count(db, '사원')}행")
    return results


db = emp_db()
print(f"시작: 부서 {count(db, '부서')}행, 사원 {count(db, '사원')}행")
res = run_inserts(db, verbose=True)
assert res == EXPECT, res
print(f"성공 {res.count('성공')}번, 실패 {res.count('실패')}번 → 사원 {count(db, '사원')}행")
assert count(db, "사원") == 5
print("  사원:", list(db.execute("SELECT * FROM 사원 ORDER BY 사번")))

# 부모 행 삭제 — 기본(ON DELETE 절 없음)
try:
    db.execute("DELETE FROM 부서 WHERE 부서번호 = 20")
    raise AssertionError("자식이 있으면 실패해야 함")
except sqlite3.IntegrityError as e:
    print(f"기본: DELETE FROM 부서 WHERE 부서번호 = 20 → 실패 ({e})  (오라클 ORA-02292)")
print(f"  자식: {list(db.execute('SELECT 이름 FROM 사원 WHERE 부서번호 = 20 ORDER BY 사번'))}")
assert count(db, "부서") == 2 and count(db, "사원") == 5

# ON DELETE CASCADE
db = emp_db("ON DELETE CASCADE")
run_inserts(db)
db.execute("DELETE FROM 부서 WHERE 부서번호 = 20")
emps = list(db.execute("SELECT 이름, 부서번호 FROM 사원 ORDER BY 사번"))
print(f"CASCADE: 부서 20 삭제 성공 → 부서 {count(db, '부서')}행, 사원 {len(emps)}행 {emps}")
assert count(db, "부서") == 1 and len(emps) == 3 and [e[0] for e in emps] == ["민수", "현우", "동훈"]

# ON DELETE SET NULL
db = emp_db("ON DELETE SET NULL")
run_inserts(db)
db.execute("DELETE FROM 부서 WHERE 부서번호 = 20")
emps = list(db.execute("SELECT 이름, 부서번호 FROM 사원 ORDER BY 사번"))
nulls = [e[0] for e in emps if e[1] is None]
print(f"SET NULL: 부서 20 삭제 성공 → 부서 {count(db, '부서')}행, 사원 {len(emps)}행 {emps}, 부서번호 NULL {nulls}")
assert count(db, "부서") == 1 and len(emps) == 5 and nulls == ["지영", "수진", "동훈"]

print()
print("== 곁가지: UNIQUE와 NULL(부서명 UNIQUE) ==")
db = emp_db()
try:
    db.execute("INSERT INTO 부서 VALUES (30, '영업')")
except sqlite3.IntegrityError as e:
    print(f"부서명 ‘영업’ 한 번 더 → 실패 ({e})")
db.execute("INSERT INTO 부서 VALUES (30, NULL)")
db.execute("INSERT INTO 부서 VALUES (40, NULL)")
print(f"부서명 NULL 두 행 → 둘 다 성공, 부서 {count(db, '부서')}행 (오라클도 단일 열 UNIQUE에 NULL 여러 개 허용, SQL Server는 하나만)")
assert count(db, "부서") == 4

print()
print("모든 확인 통과")
