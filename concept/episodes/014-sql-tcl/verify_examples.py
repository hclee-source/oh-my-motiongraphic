# -*- coding: utf-8 -*-
"""014 TCL 편 예시 확인(화면에는 안 나옴). 실행: .venv/Scripts/python.exe concept/episodes/014-sql-tcl/verify_examples.py

sqlite3로 SAVEPOINT / ROLLBACK TO / COMMIT / ROLLBACK 순서를 실제로 돌려 표 상태를 확인한다.
sqlite와 오라클의 차이(오라클 규칙은 문서 기준으로 따로 적음):
- 오라클은 첫 DML에서 트랜잭션이 저절로 시작된다 → sqlite에서는 COMMIT 뒤에 BEGIN을 직접 넣어 흉내.
- 오라클은 DDL(CREATE·ALTER·DROP·TRUNCATE·RENAME) 앞뒤로 자동 COMMIT → sqlite는 DDL도 트랜잭션 안에서 되돌려지므로
  oracle_ddl()에서 DDL 앞뒤에 COMMIT을 넣어 흉내. (sqlite 그대로의 동작 = SQL Server의 BEGIN TRANSACTION 안 동작과 같음)
- 같은 이름 SAVEPOINT: 오라클은 앞의 것을 지운다. sqlite는 둘 다 쌓아 두고 ROLLBACK TO는 가장 최근 것으로 간다
  → 이 편 예시(한 번만 ROLLBACK TO A)에서는 결과가 같다.
- ROLLBACK TO A 뒤 B는 지워짐(오라클 ORA-01086, sqlite ‘no such savepoint’), COMMIT 뒤 저장 지점 모두 사라짐 — 둘이 같다.
"""
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ORDER = {"사과": 1, "배": 2, "귤": 3, "감": 4, "포도": 5, "키위": 6}


def state(con):
    rows = con.execute("SELECT 이름, 수량 FROM 과일").fetchall()
    return sorted(rows, key=lambda r: ORDER.get(r[0], 99))


def show(label, con):
    rows = state(con)
    print(f"{label:<34} {len(rows)}행  " + ", ".join(f"{n} {q}" for n, q in rows))
    return rows


def fresh():
    con = sqlite3.connect(":memory:", isolation_level=None)  # 트랜잭션은 직접 제어
    con.execute("CREATE TABLE 과일 (이름 TEXT PRIMARY KEY, 수량 INTEGER)")
    con.execute("BEGIN")
    con.executemany("INSERT INTO 과일 VALUES (?, ?)", [("사과", 10), ("배", 20), ("귤", 30)])
    con.execute("COMMIT")
    return con


def expect(rows, want, what):
    assert rows == want, f"{what}: {rows} != {want}"


def must_fail(con, sql, what):
    try:
        con.execute(sql)
    except sqlite3.OperationalError as e:
        print(f"  {what}: 오류 ({e})")
        return
    raise AssertionError(f"{what}: 오류가 나야 함")


print("== 본편: 커밋된 3행에서 명령 열 줄 ==")
con = fresh()
expect(show("시작(커밋됨)", con), [("사과", 10), ("배", 20), ("귤", 30)], "시작")
con.execute("BEGIN")  # 오라클: 첫 DML에서 트랜잭션 시작
con.execute("INSERT INTO 과일 VALUES ('감', 40)")
expect(show("① INSERT 감 40", con), [("사과", 10), ("배", 20), ("귤", 30), ("감", 40)], "①")
con.execute("SAVEPOINT A")
show("② SAVEPOINT A", con)
con.execute("UPDATE 과일 SET 수량 = 15 WHERE 이름 = '사과'")
expect(show("③ UPDATE 사과 15", con), [("사과", 15), ("배", 20), ("귤", 30), ("감", 40)], "③")
con.execute("SAVEPOINT B")
show("④ SAVEPOINT B", con)
con.execute("DELETE FROM 과일 WHERE 이름 = '배'")
expect(show("⑤ DELETE 배", con), [("사과", 15), ("귤", 30), ("감", 40)], "⑤")
con.execute("ROLLBACK TO B")
expect(show("⑥ ROLLBACK TO B", con), [("사과", 15), ("배", 20), ("귤", 30), ("감", 40)], "⑥")
con.execute("ROLLBACK TO A")
expect(show("⑦ ROLLBACK TO A", con), [("사과", 10), ("배", 20), ("귤", 30), ("감", 40)], "⑦")
con.execute("COMMIT")
expect(show("⑧ COMMIT", con), [("사과", 10), ("배", 20), ("귤", 30), ("감", 40)], "⑧")
con.execute("BEGIN")  # 오라클: 다음 DML에서 새 트랜잭션
con.execute("DELETE FROM 과일 WHERE 이름 = '귤'")
expect(show("⑨ DELETE 귤", con), [("사과", 10), ("배", 20), ("감", 40)], "⑨")
con.execute("ROLLBACK")
final = show("⑩ ROLLBACK", con)
expect(final, [("사과", 10), ("배", 20), ("귤", 30), ("감", 40)], "⑩")
print(f"  답: {len(final)}행, 사과 수량 {dict(final)['사과']}")

print("\n== ⑦ 다음 ROLLBACK TO B / ⑧ 다음 ROLLBACK TO A → 둘 다 오류 ==")
con = fresh()
con.execute("BEGIN")
con.execute("INSERT INTO 과일 VALUES ('감', 40)")
con.execute("SAVEPOINT A")
con.execute("UPDATE 과일 SET 수량 = 15 WHERE 이름 = '사과'")
con.execute("SAVEPOINT B")
con.execute("DELETE FROM 과일 WHERE 이름 = '배'")
con.execute("ROLLBACK TO B")
con.execute("ROLLBACK TO A")
must_fail(con, "ROLLBACK TO B", "ROLLBACK TO A 다음 ROLLBACK TO B")
con.execute("ROLLBACK TO A")  # A 자체는 남아 있다
print("  ROLLBACK TO A 다시: 정상(A는 남아 있음)")
con.execute("COMMIT")
must_fail(con, "ROLLBACK TO A", "COMMIT 다음 ROLLBACK TO A")

print("\n== 같은 이름 SAVEPOINT (위 4행 확정 상태에서) ==")
con = fresh()
con.execute("INSERT INTO 과일 VALUES ('감', 40)")  # 자동 확정(4행 출발점 만들기)
con.execute("BEGIN")
con.execute("SAVEPOINT A")
con.execute("INSERT INTO 과일 VALUES ('포도', 50)")
con.execute("SAVEPOINT A")  # 오라클: 앞의 A 지워지고 여기가 A
con.execute("INSERT INTO 과일 VALUES ('키위', 60)")
show("  SAVEPOINT A, 포도, SAVEPOINT A, 키위", con)
con.execute("ROLLBACK TO A")
rows = show("  ROLLBACK TO A", con)
names = [n for n, _ in rows]
assert "포도" in names and "키위" not in names, names
print("  → 키위만 취소, 포도 남음")
con.execute("ROLLBACK")

print("\n== DDL 함정 (4행 확정 상태에서 UPDATE 귤 0 → CREATE TABLE → ROLLBACK) ==")
DDL = ("CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME")


def oracle_exec(con, sql):
    """오라클 흉내: DDL이면 앞뒤로 자동 COMMIT, DML이면 트랜잭션이 없을 때 새로 시작."""
    if sql.split()[0].upper() in DDL:
        if con.in_transaction:
            con.execute("COMMIT")  # DDL 앞 자동 COMMIT → 앞의 UPDATE 확정
        con.execute(sql)  # sqlite는 자동 확정 모드라 DDL도 바로 확정(DDL 뒤 COMMIT)
    elif sql.upper() in ("COMMIT", "ROLLBACK"):
        if con.in_transaction:
            con.execute(sql)
    else:
        if not con.in_transaction:
            con.execute("BEGIN")
        con.execute(sql)


con = fresh()
con.execute("INSERT INTO 과일 VALUES ('감', 40)")
oracle_exec(con, "UPDATE 과일 SET 수량 = 0 WHERE 이름 = '귤'")
show("  UPDATE 귤 0", con)
oracle_exec(con, "CREATE TABLE 주문 (번호 INTEGER, 이름 TEXT)")
oracle_exec(con, "ROLLBACK")
rows = show("  CREATE TABLE → ROLLBACK (오라클)", con)
assert dict(rows)["귤"] == 0
print("  → 귤 0 그대로(30으로 안 돌아감)")

# 참고: sqlite 그대로(= SQL Server BEGIN TRANSACTION 안)라면 DDL까지 함께 취소된다
con = fresh()
con.execute("INSERT INTO 과일 VALUES ('감', 40)")
con.execute("BEGIN")
con.execute("UPDATE 과일 SET 수량 = 0 WHERE 이름 = '귤'")
con.execute("CREATE TABLE 주문 (번호 INTEGER, 이름 TEXT)")
con.execute("ROLLBACK")
rows = show("  참고: 트랜잭션 안 DDL도 취소(SQL Server식)", con)
has = con.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = '주문'").fetchone()[0]
assert dict(rows)["귤"] == 30 and has == 0
print("  → 귤 30, 주문 표도 없음")

print("\n== 쇼츠 ==")
con = sqlite3.connect(":memory:", isolation_level=None)
con.execute("CREATE TABLE T (C INTEGER)")
con.execute("BEGIN")
con.execute("INSERT INTO T VALUES (1)")
con.execute("SAVEPOINT A")
con.execute("INSERT INTO T VALUES (2)")
con.execute("ROLLBACK TO A")
n = con.execute("SELECT COUNT(*) FROM T").fetchone()[0]
print(f"  행 넣기 → SAVEPOINT A → 행 넣기 → ROLLBACK TO A: {n}행(앞의 한 행 남음)")
assert n == 1
con.execute("COMMIT")
con.execute("BEGIN")
con.execute("SAVEPOINT A")
con.execute("UPDATE T SET C = 9")
con.execute("INSERT INTO T VALUES (3)")
con.execute("ROLLBACK")
rows = con.execute("SELECT C FROM T").fetchall()
print(f"  COMMIT 뒤 변경들 → ROLLBACK: {rows} (마지막 COMMIT 상태)")
assert rows == [(1,)]
must_fail(con, "ROLLBACK TO A", "  ROLLBACK 다음 ROLLBACK TO A")
oracle_exec(con, "DELETE FROM T")
oracle_exec(con, "CREATE TABLE U (C INTEGER)")
oracle_exec(con, "ROLLBACK")
n = con.execute("SELECT COUNT(*) FROM T").fetchone()[0]
print(f"  DELETE → CREATE TABLE → ROLLBACK (오라클): {n}행(지운 행 안 돌아옴)")
assert n == 0

print("\n모든 확인 통과")
