# -*- coding: utf-8 -*-
"""023 정규 표현식 함수 — 대본(본편·쇼츠)의 예시 결과를 파이썬 re와 sqlite3로 다시 계산해 확인한다.

실행(저장소 맨 위에서): .venv/Scripts/python.exe concept/episodes/023-sql-regex/verify_examples.py

오라클 함수를 파이썬 re로 흉내 낸 규칙(이 편의 패턴 범위에서는 의미가 같음):
- REGEXP_LIKE(s, p[, 'i'])      = re.search(p, s) 가 있으면 참(문자열 어느 부분이든 맞으면 참, LIKE와 달리 전체 일치가 아님)
- REGEXP_SUBSTR(s, p, pos, occ) = pos(1부터)에서 시작해 겹치지 않게 찾은 occ번째 일치. 없으면 NULL(None)
                                  (오라클은 빈 문자열도 NULL — 이 편 예시에는 빈 일치가 없음)
- REGEXP_INSTR(s, p, pos, occ)  = occ번째 일치의 시작 위치(1부터). 없으면 0
- REGEXP_COUNT(s, p, pos)       = 겹치지 않게 센 일치 개수(re.findall과 같음). 없으면 0
- REGEXP_REPLACE(s, p[, r])     = 기본 occurrence 0 = 맞는 부분 모두 바꿈(re.sub count=0). r 생략(NULL)이면 맞는 부분 삭제.
                                  결과가 빈 문자열이면 오라클은 NULL
- 'i' = 대소문자 무시(re.IGNORECASE). 생략하면 구분(NLS_SORT 기본 BINARY 기준)
- 탐욕(가장 길게) 기본, 반복 기호 뒤 ? 는 가장 짧게 — 오라클(10gR2부터 펄 확장)과 파이썬이 같음
- 차이 메모: 파이썬 $ 는 끝의 줄바꿈 앞에서도 맞지만 오라클 $ 는 문자열 끝(줄바꿈 없는 이 편 예시에서는 같음).
  \\d 는 파이썬에서 유니코드 숫자까지 맞지만 이 편 예시는 [0-9]만 씀. 빈 일치를 세는 방식은 다를 수 있으나 이 편 예시에는 없음.
"""
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
FAIL = []


def flags_of(opt):
    return re.IGNORECASE if opt and "i" in opt else 0


def regexp_like(s, p, opt=None):
    return re.search(p, s, flags_of(opt)) is not None


def _matches(s, p, pos=1, opt=None):
    return list(re.compile(p, flags_of(opt)).finditer(s, pos - 1))


def regexp_substr(s, p, pos=1, occ=1, opt=None):
    ms = _matches(s, p, pos, opt)
    if len(ms) < occ:
        return None
    v = ms[occ - 1].group(0)
    return v if v != "" else None  # 오라클: 빈 문자열 = NULL


def regexp_instr(s, p, pos=1, occ=1, opt=None):
    ms = _matches(s, p, pos, opt)
    return ms[occ - 1].start() + 1 if len(ms) >= occ else 0


def regexp_count(s, p, pos=1, opt=None):
    return len(_matches(s, p, pos, opt))


def regexp_replace(s, p, r=None, opt=None):
    v = re.sub(p, "" if r is None else r, s, flags=flags_of(opt))
    return v if v != "" else None


def check(label, got, want):
    ok = got == want
    print(f"{'OK ' if ok else 'XX '} {label} → {got!r}" + ("" if ok else f"   (대본: {want!r})"))
    if not ok:
        FAIL.append(label)


print("== 본편 ==")
# 1·5장: 코드 표 6행, REGEXP_LIKE 행 수 — sqlite3에 오라클처럼 동작하는 REGEXP_LIKE를 붙여 실제 SQL로 센다
codes = ["A101", "205", "B30", "4096", "77C", "310"]
con = sqlite3.connect(":memory:")
con.create_function("REGEXP_LIKE", 2, lambda s, p: int(regexp_like(s, p)))
con.create_function("REGEXP_LIKE", 3, lambda s, p, o: int(regexp_like(s, p, o)))
con.execute("CREATE TABLE 상품 (코드 TEXT)")
con.executemany("INSERT INTO 상품 VALUES (?)", [(c,) for c in codes])


def rows(where, *args):
    return [r[0] for r in con.execute(f"SELECT 코드 FROM 상품 WHERE {where}", args)]


check("REGEXP_LIKE(코드, '[0-9]{3}') 행", rows("REGEXP_LIKE(코드, ?)", "[0-9]{3}"), ["A101", "205", "4096", "310"])
check("  A101에서 맞는 부분", re.search("[0-9]{3}", "A101").group(0), "101")
check("  4096에서 맞는 부분", re.search("[0-9]{3}", "4096").group(0), "409")
check("REGEXP_LIKE(코드, '^[0-9]{3}') 행", rows("REGEXP_LIKE(코드, ?)", "^[0-9]{3}"), ["205", "4096", "310"])
check("REGEXP_LIKE(코드, '^[0-9]{3}$') 행", rows("REGEXP_LIKE(코드, ?)", "^[0-9]{3}$"), ["205", "310"])
check("REGEXP_LIKE(코드, '^b') 행", rows("REGEXP_LIKE(코드, ?)", "^b"), [])
check("REGEXP_LIKE(코드, '^b', 'i') 행", rows("REGEXP_LIKE(코드, ?, ?)", "^b", "i"), ["B30"])
# LIKE는 전체 일치: 숫자 세 자리라는 뜻으로 ‘___’를 써도 글자 세 개 전체가 맞아야 함(참고용, 대본에는 숫자 없음)
check("(참고) LIKE '___' 행", [r[0] for r in con.execute("SELECT 코드 FROM 상품 WHERE 코드 LIKE '___'")], ["205", "B30", "77C", "310"])

# 4장: 기호 설명
check("휴대폰 패턴 '^[0-9]{3}-[0-9]{4}-[0-9]{4}$' ~ 010-1234-5678", regexp_like("010-1234-5678", "^[0-9]{3}-[0-9]{4}-[0-9]{4}$"), True)
check("'^ab+$' 가 a / ab / abb / abab", [regexp_like(x, "^ab+$") for x in ["a", "ab", "abb", "abab"]], [False, True, True, False])
check("'^(ab)+$' 가 a / ab / abb / abab", [regexp_like(x, "^(ab)+$") for x in ["a", "ab", "abb", "abab"]], [False, True, False, True])
check("'^ab*$' 가 a / ab / abb", [regexp_like(x, "^ab*$") for x in ["a", "ab", "abb"]], [True, True, True])
check("'^ab?$' 가 a / ab / abb", [regexp_like(x, "^ab?$") for x in ["a", "ab", "abb"]], [True, True, False])
check("[0-9] 와 \\d 같은 결과(2026년)", re.findall(r"[0-9]", "2026년") == re.findall(r"\d", "2026년"), True)
check("[^0-9] 가 맞는 글자(2026년)", re.findall(r"[^0-9]", "2026년"), ["년"])

# 6장: REGEXP_SUBSTR
d = "2026년 11월 5일"
check(f"REGEXP_SUBSTR('{d}', '[0-9]+')", regexp_substr(d, "[0-9]+"), "2026")
check("  숫자 덩어리 전체", re.findall("[0-9]+", d), ["2026", "11", "5"])
check(f"REGEXP_SUBSTR('{d}', '[0-9]+', 1, 2)", regexp_substr(d, "[0-9]+", 1, 2), "11")
check(f"REGEXP_SUBSTR('{d}', '[0-9]{{5}}')", regexp_substr(d, "[0-9]{5}"), None)

# 7장: REGEXP_REPLACE
t = "010-1234-5678"
check(f"REGEXP_REPLACE('{t}', '[0-9]{{4}}$', '****')", regexp_replace(t, "[0-9]{4}$", "****"), "010-1234-****")
check(f"REGEXP_REPLACE('{t}', '[0-9]{{4}}', '****')", regexp_replace(t, "[0-9]{4}", "****"), "010-****-****")
check(f"REGEXP_REPLACE('{t}', '[^0-9]')", regexp_replace(t, "[^0-9]"), "01012345678")
check("  남은 숫자 개수", len(regexp_replace(t, "[^0-9]")), 11)

# 8장: REGEXP_COUNT, REGEXP_INSTR
check("REGEXP_COUNT('banana', 'a')", regexp_count("banana", "a"), 3)
check("REGEXP_COUNT('banana', 'ana')", regexp_count("banana", "ana"), 1)
check("  겹치게 세면(참고) ana", len(re.findall("(?=ana)", "banana")), 2)
check("  ana 첫 일치 위치(2~4번째)", (regexp_instr("banana", "ana"), regexp_instr("banana", "ana") + 2), (2, 4))
check("REGEXP_INSTR('banana', 'n')", regexp_instr("banana", "n"), 3)
check("REGEXP_INSTR('banana', '[0-9]') 없음", regexp_instr("banana", "[0-9]"), 0)
check("REGEXP_COUNT('banana', '[0-9]') 없음", regexp_count("banana", "[0-9]"), 0)
check("REGEXP_SUBSTR('banana', '[0-9]') 없음", regexp_substr("banana", "[0-9]"), None)

# 9장: 가장 길게 / 가장 짧게
h = "<b>굵게</b>"
check(f"REGEXP_SUBSTR('{h}', '<.*>')", regexp_substr(h, "<.*>"), "<b>굵게</b>")
check(f"REGEXP_SUBSTR('{h}', '<.*?>')", regexp_substr(h, "<.*?>"), "<b>")
check(f"REGEXP_REPLACE('{h}', '<.*?>')", regexp_replace(h, "<.*?>"), "굵게")
check(f"  (참고) REGEXP_REPLACE('{h}', '<.*>') → 빈 문자열 = 오라클 NULL", regexp_replace(h, "<.*>"), None)

print("\n== 쇼츠 ==")
check("REGEXP_LIKE('사과나무', '나무')", regexp_like("사과나무", "나무"), True)
check("REGEXP_LIKE('사과나무', '^나무')", regexp_like("사과나무", "^나무"), False)
s2 = "사과 12개 배 7개"
check(f"REGEXP_SUBSTR('{s2}', '[0-9]+')", regexp_substr(s2, "[0-9]+"), "12")
check(f"REGEXP_SUBSTR('{s2}', '[0-9]+', 1, 2)", regexp_substr(s2, "[0-9]+", 1, 2), "7")
check("REGEXP_REPLACE('홍 길 동', ' ')", regexp_replace("홍 길 동", " "), "홍길동")
check("  지워진 공백 개수", regexp_count("홍 길 동", " "), 2)
check("REGEXP_COUNT('토마토', '토')", regexp_count("토마토", "토"), 2)
check("REGEXP_INSTR('토마토', '토')", regexp_instr("토마토", "토"), 1)
check("REGEXP_SUBSTR('하나 둘 하나 둘', '하나.*둘')", regexp_substr("하나 둘 하나 둘", "하나.*둘"), "하나 둘 하나 둘")
check("REGEXP_SUBSTR('하나 둘 하나 둘', '하나.*?둘')", regexp_substr("하나 둘 하나 둘", "하나.*?둘"), "하나 둘")
# 쇼츠 1장: WHERE 조건으로 — 이름 표 한 행
con.execute("CREATE TABLE 식물 (이름 TEXT)")
con.execute("INSERT INTO 식물 VALUES ('사과나무')")
check("WHERE REGEXP_LIKE(이름, '나무') 행", [r[0] for r in con.execute("SELECT 이름 FROM 식물 WHERE REGEXP_LIKE(이름, '나무')")], ["사과나무"])
check("WHERE REGEXP_LIKE(이름, '^나무') 행", [r[0] for r in con.execute("SELECT 이름 FROM 식물 WHERE REGEXP_LIKE(이름, '^나무')")], [])

print("\n== 대본 표기 검사 ==")
main = (HERE / "script.md").read_text(encoding="utf-8")
shorts = (HERE / "shorts" / "script.md").read_text(encoding="utf-8")


def body(text):
    return text.split("\n---\n", 1)[1]


for name, text in [("본편", main), ("쇼츠", shorts)]:
    b = body(text)
    narr = [l for l in b.splitlines() if re.match(r"^\d+\. ", l)]
    screen = [l for l in b.splitlines() if l.startswith("> 화면")]
    check(f"{name}: 쌍따옴표 없음", any(q in text for q in ['"', "“", "”"]), False)
    check(f"{name}: 화면 줄에 ‘|’ 없음", any("|" in l for l in screen), False)
    if name == "본편":
        check(f"{name}: 내레이션에 ‘|’ 없음", any("|" in l for l in narr), False)
    check(f"{name}: 화면·내레이션에 시험 이름 없음",
          any(w in l for l in narr + screen for w in ["SQLD", "ADsP", "빅데이터분석기사", "빅분기"]), False)
    syl = sum(len(re.findall(r"[가-힣A-Za-z0-9]", re.sub(r"^\d+\. ", "", l).replace("|", ""))) for l in narr)
    print(f"   {name}: 문장 {len(narr)}개, 글자 약 {syl}자 → 말하기 약 {syl / 6.5:.0f}초(쉼 제외)")

# 쇼츠가 본편 예시를 다시 쓰지 않는지
for w in ["A101", "4096", "2026", "010-1234", "banana", "<b>"]:
    check(f"쇼츠에 본편 예시 ‘{w}’ 없음", w in body(shorts), False)

print("\n결과:", "모두 일치" if not FAIL else f"불일치 {len(FAIL)}건 — {FAIL}")
sys.exit(1 if FAIL else 0)
