"""020 단일 행 함수 결과 맞히기 — 대본(본편·쇼츠)에 나오는 결과를 모두 다시 계산해 확인한다(화면에는 안 나옴).

오라클 규칙을 파이썬으로 그대로 구현해 단언하고, 규칙이 같은 것은 sqlite3로 한 번 더 실행해 교차 확인한다.
- 파이썬 기본 동작을 그대로 쓰면 틀리는 곳: round()는 은행가 반올림(round(125, -1) = 120), 문자열 위치는 0부터.
  그래서 아래 함수들은 오라클 규칙을 직접 적는다. (MOD 문항은 검수 반영으로 대본에서 뺐다.)
- 오라클은 빈 문자열 ''을 NULL로 본다 → 결과가 ''이면 None(NULL)을 돌려준다.

실행(저장소 맨 위에서): .venv/Scripts/python.exe concept/episodes/020-sql-functions/verify_examples.py
"""
import math
import sqlite3
import sys
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
NULL = None


def _null_if_empty(s):
    return None if s is None or s == "" else s


# ---------- 문자 함수 (오라클 규칙) ----------
def SUBSTR(s, pos, length=None):
    """위치는 1부터, 0은 1로 취급, 음수면 뒤에서 센다. 길이 생략 = 끝까지, 길이 < 1 = NULL."""
    s = _null_if_empty(s)
    if s is None:
        return None
    n = len(s)
    if pos == 0:
        pos = 1
    start = pos - 1 if pos > 0 else n + pos      # 0부터 세는 파이썬 위치로
    if start < 0 or start >= n:
        return None
    if length is None:
        return _null_if_empty(s[start:])
    if length < 1:
        return None
    return _null_if_empty(s[start:start + length])


def INSTR(s, sub, pos=1, occ=1):
    """찾은 위치(1부터), 없으면 0. pos > 0이면 pos부터 앞으로 찾고 occ번째로 나온 것."""
    assert pos > 0 and occ > 0     # 대본에 쓰는 경우만 구현
    i = pos - 1
    for _ in range(occ):
        i = s.find(sub, i)
        if i < 0:
            return 0
        found = i
        i += 1
    return found + 1


def LENGTH(s):
    s = _null_if_empty(s)
    return None if s is None else len(s)       # 글자 수(한글 한 음절 = 1)


def _pad(s, n, pad, left):
    if len(s) >= n:
        return s[:n]                           # 길면 왼쪽부터 n글자만 남김
    fill = (pad * n)[: n - len(s)]
    return fill + s if left else s + fill


def LPAD(s, n, pad=" "):
    return _null_if_empty(_pad(s, n, pad, True))


def RPAD(s, n, pad=" "):
    return _null_if_empty(_pad(s, n, pad, False))


def LTRIM(s, chars=" "):
    return _null_if_empty(s.lstrip(chars))


def RTRIM(s, chars=" "):
    return _null_if_empty(s.rstrip(chars))


def TRIM(s, ch=" "):
    return _null_if_empty(s.strip(ch))


def REPLACE(s, search, rep=None):
    """세 번째 인수를 생략(또는 NULL)하면 찾은 문자를 모두 지운다."""
    if search is None:
        return s
    return _null_if_empty(s.replace(search, "" if rep is None else rep))


# ---------- 숫자 함수 (오라클 규칙) ----------
def _quant(d):
    """자릿수 d → quantize 단위. d = 1 → 0.1, d = 0 → 1, d = -1 → 1E+1(십의 자리)."""
    return Decimal(1).scaleb(-d)


def ROUND(x, d=0):
    """0.5는 0에서 먼 쪽으로(ROUND_HALF_UP = ties away from zero)."""
    return Decimal(str(x)).quantize(_quant(d), rounding=ROUND_HALF_UP)


def TRUNC(x, d=0):
    """반올림 없이 0 쪽으로 버린다."""
    return Decimal(str(x)).quantize(_quant(d), rounding=ROUND_DOWN)


def CEIL(x):
    return math.ceil(Decimal(str(x)))


def FLOOR(x):
    return math.floor(Decimal(str(x)))


# ---------- 날짜 (오라클 DATE: 하루 = 1, 초 단위까지) ----------
def DATE_ADD(d, days):
    secs = Fraction(days) * 86400
    return d + timedelta(seconds=round(secs))


def DATE_SUB(d1, d2):
    return Fraction(int((d1 - d2).total_seconds()), 86400)


def TO_DATE(s, fmt):
    assert fmt == "YYYYMMDD"
    return datetime.strptime(s, "%Y%m%d")


# ---------- 조건 ----------
def DECODE(expr, *args):
    """짝(search, result)을 차례로 비교, 같으면 result. 짝이 끝나고 하나 남으면 기본값, 없으면 NULL.
    (DECODE는 NULL끼리도 같다고 보지만 대본에는 안 씀)"""
    pairs, default = (args[:-1], args[-1]) if len(args) % 2 else (args, None)
    for i in range(0, len(pairs), 2):
        if expr == pairs[i]:
            return pairs[i + 1]
    return default


def CASE_SIMPLE(value, whens, else_=None):
    for w, t in whens:
        if value is not None and value == w:
            return t
    return else_


def CASE_SEARCHED(whens, else_=None):
    for cond, t in whens:          # 위에서부터, 처음 참인 WHEN에서 멈춘다
        if cond:
            return t
    return else_


# ---------- 확인 ----------
checks = 0


def check(label, got, want):
    global checks
    ok = got == want
    shown = format(got, "f") if isinstance(got, Decimal) else repr(got)
    print(f"{'OK ' if ok else 'XX '} {label} = {shown}" + ("" if ok else f"   (기대 {want!r})"))
    assert ok, label
    checks += 1


print("== 본편 ==")
# 1장
check("ROUND(125, -1)", ROUND(125, -1), Decimal(130))
# 2장 SUBSTR
check("SUBSTR('ABCDE', 2, 3)", SUBSTR("ABCDE", 2, 3), "BCD")
check("SUBSTR('ABCDE', -3, 2)", SUBSTR("ABCDE", -3, 2), "CD")
check("  음수 시작 위치 = 길이 5 − 3 + 1", 5 - 3 + 1, 3)
check("  SUBSTR('ABCDE', 0, 2) (0은 1로)", SUBSTR("ABCDE", 0, 2), "AB")
# 3장 INSTR · LENGTH
check("INSTR('BANANA', 'A', 1, 2)", INSTR("BANANA", "A", 1, 2), 4)
check("  INSTR('BANANA', 'A') (첫 A)", INSTR("BANANA", "A"), 2)
check("  INSTR('BANANA', 'X') (없으면 0)", INSTR("BANANA", "X"), 0)
check("LENGTH('SQL 함수')", LENGTH("SQL 함수"), 6)
check("LENGTH('') (오라클 '' = NULL)", LENGTH(""), NULL)
# 4장 LPAD · LTRIM · REPLACE
check("LPAD('7', 3, '0')", LPAD("7", 3, "0"), "007")
check("  붙은 0의 개수 = 3 − 1", 3 - len("7"), 2)
check("LTRIM('xxAxx', 'x')", LTRIM("xxAxx", "x"), "Axx")
check("  RTRIM('xxAxx', 'x')", RTRIM("xxAxx", "x"), "xxA")
check("  TRIM('x' FROM 'xxAxx')", TRIM("xxAxx", "x"), "A")
check("REPLACE('S-Q-L', '-')", REPLACE("S-Q-L", "-"), "SQL")
# 5장 ROUND · TRUNC
check("ROUND(123.456, 1)", ROUND(123.456, 1), Decimal("123.5"))
check("TRUNC(129, -1)", TRUNC(129, -1), Decimal(120))
check("  ROUND(129, -1) (반올림이면 130 — 함정 답)", ROUND(129, -1), Decimal(130))
# 6장 CEIL · FLOOR
check("CEIL(-1.5)", CEIL(-1.5), -1)
check("FLOOR(-1.5)", FLOOR(-1.5), -2)
# 7장 날짜 (SYSDATE를 2026-11-05 09:00으로 가정)
sysdate = datetime(2026, 11, 5, 9, 0)
check("SYSDATE + 1", DATE_ADD(sysdate, 1), datetime(2026, 11, 6, 9, 0))
check("SYSDATE + 1/24", DATE_ADD(sysdate, Fraction(1, 24)), datetime(2026, 11, 5, 10, 0))
check("TO_DATE('20261105') − TO_DATE('20261101')",
      DATE_SUB(TO_DATE("20261105", "YYYYMMDD"), TO_DATE("20261101", "YYYYMMDD")), 4)
# 8장 DECODE · 단순 CASE
check("DECODE(30, 10, '영업', 20, '개발')", DECODE(30, 10, "영업", 20, "개발"), NULL)
check("DECODE(30, 10, '영업', 20, '개발', '기타')", DECODE(30, 10, "영업", 20, "개발", "기타"), "기타")
check("CASE 30 WHEN 10 THEN '영업' WHEN 20 THEN '개발' END",
      CASE_SIMPLE(30, [(10, "영업"), (20, "개발")]), NULL)
# 9장 검색 CASE, 점수 95
점수 = 95
check("CASE WHEN 점수 >= 80 THEN '보통' WHEN 점수 >= 90 THEN '우수' ELSE '노력' END (95)",
      CASE_SEARCHED([(점수 >= 80, "보통"), (점수 >= 90, "우수")], "노력"), "보통")

print("== 쇼츠 ==")
check("SUBSTR('DATABASE', -4)", SUBSTR("DATABASE", -4), "BASE")
check("  시작 = 8 − 4 + 1", 8 - 4 + 1, 5)
check("RPAD('AB', 5, '*')", RPAD("AB", 5, "*"), "AB***")
check("TRUNC(987, -2)", TRUNC(987, -2), Decimal(900))
check("CEIL(-2.7)", CEIL(-2.7), -2)
check("SYSDATE + 0.5 (12시간 뒤)", DATE_ADD(sysdate, Fraction(1, 2)) - sysdate, timedelta(hours=12))
점수 = 50
check("CASE WHEN 점수 >= 60 THEN '합격' END (50)", CASE_SEARCHED([(점수 >= 60, "합격")]), NULL)

print("== 파이썬 기본 동작과 다른 점(그래서 직접 구현) ==")
check("파이썬 round(125, -1) (은행가 반올림)", round(125, -1), 120)

print("== sqlite3 교차 확인(규칙이 같은 것만) ==")
con = sqlite3.connect(":memory:")
q = lambda sql: con.execute(sql).fetchone()[0]
check("sqlite substr('ABCDE', 2, 3)", q("SELECT substr('ABCDE', 2, 3)"), "BCD")
check("sqlite substr('ABCDE', -3, 2)", q("SELECT substr('ABCDE', -3, 2)"), "CD")
check("sqlite substr('DATABASE', -4)", q("SELECT substr('DATABASE', -4)"), "BASE")
check("sqlite 두 번째 A 위치(instr 두 번)",
      q("SELECT instr('BANANA','A') + instr(substr('BANANA', instr('BANANA','A') + 1), 'A')"), 4)
check("sqlite instr('BANANA', 'X')", q("SELECT instr('BANANA', 'X')"), 0)
check("sqlite length('SQL 함수')", q("SELECT length('SQL 함수')"), 6)
check("sqlite length('') (sqlite는 0 — 오라클은 NULL, 다른 점)", q("SELECT length('')"), 0)
check("sqlite ltrim('xxAxx', 'x')", q("SELECT ltrim('xxAxx', 'x')"), "Axx")
check("sqlite rtrim('xxAxx', 'x')", q("SELECT rtrim('xxAxx', 'x')"), "xxA")
check("sqlite trim('xxAxx', 'x')", q("SELECT trim('xxAxx', 'x')"), "A")
check("sqlite replace('S-Q-L', '-', '')", q("SELECT replace('S-Q-L', '-', '')"), "SQL")
check("sqlite 날짜 + 1", q("SELECT datetime(julianday('2026-11-05 09:00') + 1)"), "2026-11-06 09:00:00")
check("sqlite 날짜 + 1/24", q("SELECT datetime(julianday('2026-11-05 09:00') + 1.0/24)"), "2026-11-05 10:00:00")
check("sqlite 날짜 + 0.5", q("SELECT datetime(julianday('2026-11-05 09:00') + 0.5)"), "2026-11-05 21:00:00")
check("sqlite 날짜 − 날짜", q("SELECT julianday('2026-11-05') - julianday('2026-11-01')"), 4.0)
check("sqlite 단순 CASE(ELSE 없음)", q("SELECT CASE 30 WHEN 10 THEN '영업' WHEN 20 THEN '개발' END"), None)
check("sqlite DECODE를 CASE로(기본값 '기타')",
      q("SELECT CASE 30 WHEN 10 THEN '영업' WHEN 20 THEN '개발' ELSE '기타' END"), "기타")
check("sqlite 검색 CASE(95)",
      q("SELECT CASE WHEN 95 >= 80 THEN '보통' WHEN 95 >= 90 THEN '우수' ELSE '노력' END"), "보통")
check("sqlite 검색 CASE(50, ELSE 없음)", q("SELECT CASE WHEN 50 >= 60 THEN '합격' END"), None)
try:
    check("sqlite ceil(-1.5)", q("SELECT ceil(-1.5)"), -1)
    check("sqlite floor(-1.5)", q("SELECT floor(-1.5)"), -2)
    check("sqlite ceil(-2.7)", q("SELECT ceil(-2.7)"), -2)
except sqlite3.OperationalError:
    print("--  sqlite에 ceil/floor가 없음(수학 함수 미포함 빌드) — 건너뜀")

print(f"\n모두 {checks}건 확인.")
