"""읽는 법(say.json)을 자동으로 만든다: 대본 문장 속 영어 SQL 낱말을 한글 소리로, ‘숫자+행’을 고유어 수로 바꾼다.

사용(저장소 맨 위에서): python concept/tools/say_auto.py concept/episodes/<편> [concept/episodes/<편>/shorts ...]
- 바뀌는 문장만 say.json에 적는다(자막은 script.md 그대로).
- 편 폴더에 say_manual.json({"문장 번호": "읽을 문장"})이 있으면 그 문장은 그대로 쓴다(자동보다 우선).
- 낱말 사전은 아래 WORDS. 새 SQL 낱말이 나오면 여기에 더한다(긴 것이 먼저 바뀌게 순서 상관없이 길이순으로 처리).
- AI 음성(인준)이 잘못 읽는 것으로 확인된 것(2026-11-02, listen_episode.py로 받아 적어 찾음):
  · 쉼표 사이에 홀로 있는 한 음절(‘프, 웨, 그’의 웨, ‘1, 2, 3, 4’의 1·2)을 소리 없이 빠뜨린다 → 대본에서 ‘1번, 2번’처럼
    단위를 붙이거나 ‘…오입니다.’처럼 끝을 붙여 쓴다(이 도구가 고쳐 주지 않음, 대본을 고칠 것).
  · ‘1번’을 ‘한 번’(횟수)으로 읽는다 → 이 도구가 ‘일 번’으로 바꿔 준다.
  · ‘~에 씁니다/쓰면’이 ‘~했습니다/했으면’처럼 들린다 → 대본에서 ‘적습니다’, ‘~에서 쓰면’으로.
"""
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

WORDS = {
    "SQL Server": "에스큐엘 서버", "SQL": "에스큐엘",
    "SELECT": "셀렉트", "FROM": "프롬", "WHERE": "웨어", "GROUP BY": "그룹 바이", "HAVING": "해빙",
    "ORDER BY": "오더 바이", "DESC": "디센딩", "ASC": "어센딩",
    "COUNT(*)": "카운트 스타", "COUNT": "카운트", "AVG": "에이브이지", "SUM": "썸", "MAX": "맥스", "MIN": "민",
    "NVL2": "엔브이엘 투", "NVL": "엔브이엘", "COALESCE": "코알레스", "NULLIF": "널 이프",
    "IS NOT NULL": "이즈 낫 널", "IS NULL": "이즈 널", "NOT IN": "낫 인", "IN": "인", "NULL": "널",
    "AND": "앤드", "OR": "오어", "CASE": "케이스",
    "INNER": "이너", "LEFT": "레프트", "RIGHT": "라이트", "FULL": "풀", "OUTER": "아우터", "CROSS": "크로스",
    "JOIN": "조인", "NATURAL": "내추럴", "USING": "유징",
    "RANK": "랭크", "DENSE_RANK": "덴스 랭크", "DENSE": "덴스", "ROW_NUMBER": "로우 넘버", "OVER": "오버",
    "PARTITION BY": "파티션 바이",
    "ROLLUP": "롤업", "CUBE": "큐브", "GROUPING SETS": "그루핑 세츠", "GROUPING": "그루핑",
    "A": "에이", "B": "비", "C": "씨",
    # 2026-11-05 SQLD 012~023편용으로 미리 더함
    "CONNECT BY": "커넥트 바이", "START WITH": "스타트 위드", "PRIOR": "프라이어", "LEVEL": "레벨",
    "ORDER SIBLINGS BY": "오더 시블링스 바이", "SIBLINGS": "시블링스", "CONNECT_BY_ROOT": "커넥트 바이 루트",
    "CONNECT_BY_ISLEAF": "커넥트 바이 이즈리프", "SYS_CONNECT_BY_PATH": "시스 커넥트 바이 패스", "NOCYCLE": "노사이클",
    "ROWS": "로우즈", "RANGE": "레인지", "BETWEEN": "비트윈", "UNBOUNDED": "언바운디드", "PRECEDING": "프리시딩",
    "FOLLOWING": "팔로잉", "CURRENT ROW": "커런트 로우", "LAG": "래그", "LEAD": "리드", "FIRST_VALUE": "퍼스트 밸류",
    "LAST_VALUE": "라스트 밸류", "NTILE": "엔타일", "RATIO_TO_REPORT": "레이쇼 투 리포트", "CUME_DIST": "큠 디스트",
    "PERCENT_RANK": "퍼센트 랭크",
    "COMMIT": "커밋", "ROLLBACK": "롤백", "SAVEPOINT": "세이브포인트", "TO": "투", "BEGIN TRANSACTION": "비긴 트랜잭션",
    "INSERT": "인서트", "UPDATE": "업데이트", "DELETE": "딜리트", "MERGE": "머지", "TRUNCATE": "트렁케이트",
    "DROP": "드롭", "CREATE": "크리에이트", "ALTER": "얼터", "RENAME": "리네임", "TABLE": "테이블", "MODIFY": "모디파이",
    "COLUMN": "칼럼", "ADD": "애드", "INTO": "인투", "VALUES": "밸류즈", "SET": "셋", "GRANT": "그랜트", "REVOKE": "리보크",
    "PRIMARY KEY": "프라이머리 키", "FOREIGN KEY": "포린 키", "UNIQUE": "유니크", "CHECK": "체크", "NOT NULL": "낫 널",
    "DEFAULT": "디폴트", "CASCADE": "캐스케이드", "ON DELETE": "온 딜리트", "REFERENCES": "레퍼런시스",
    "CONSTRAINT": "컨스트레인트", "WITH GRANT OPTION": "위드 그랜트 옵션", "WITH ADMIN OPTION": "위드 어드민 옵션",
    "DDL": "디디엘", "DML": "디엠엘", "DCL": "디씨엘", "TCL": "티씨엘", "PK": "피케이", "FK": "에프케이",
    "EXISTS": "이그지스츠", "NOT EXISTS": "낫 이그지스츠", "ANY": "애니", "ALL": "올", "SOME": "썸",
    "ROWNUM": "로우넘", "FETCH": "페치", "FIRST": "퍼스트", "NEXT": "넥스트", "ONLY": "온리", "WITH TIES": "위드 타이즈",
    "TOP": "탑", "OFFSET": "오프셋", "PERCENT": "퍼센트",
    "UNION ALL": "유니온 올", "UNION": "유니온", "INTERSECT": "인터섹트", "MINUS": "마이너스", "EXCEPT": "익셉트",
    "DISTINCT": "디스팅트", "LIKE": "라이크", "DUAL": "듀얼", "VIEW": "뷰", "ON": "온",
    "SUBSTR": "섭스트링", "INSTR": "인스트링", "LENGTH": "렝스", "LPAD": "엘패드", "RPAD": "알패드", "TRIM": "트림",
    "LTRIM": "엘트림", "RTRIM": "알트림", "REPLACE": "리플레이스", "UPPER": "어퍼", "LOWER": "로워", "CONCAT": "컨캣",
    "ROUND": "라운드", "TRUNC": "트렁크", "CEIL": "실", "FLOOR": "플로어", "MOD": "모드", "ABS": "앱스",
    "DECODE": "디코드", "SYSDATE": "시스데이트", "TO_CHAR": "투 차", "TO_DATE": "투 데이트", "TO_NUMBER": "투 넘버",
    "ADD_MONTHS": "애드 먼스", "WHEN": "웬", "THEN": "덴", "ELSE": "엘스", "END": "엔드",
    "PIVOT": "피벗", "UNPIVOT": "언피벗", "FOR": "포", "INCLUDE NULLS": "인클루드 널스",
    "REGEXP_LIKE": "레젝스 라이크", "REGEXP_SUBSTR": "레젝스 섭스트링", "REGEXP_REPLACE": "레젝스 리플레이스",
    "REGEXP_INSTR": "레젝스 인스트링", "REGEXP_COUNT": "레젝스 카운트",
    "BCNF": "비씨엔에프", "ERD": "이알디", "D": "디",
}
SIGNS = {"(+)": "플러스 기호", " = ": " 이퀄 ", " >= ": " 크거나 같음 ", " <> ": " 같지 않음 "}
NATIVE = {0: "영", 1: "한", 2: "두", 3: "세", 4: "네", 5: "다섯", 6: "여섯", 7: "일곱", 8: "여덟", 9: "아홉", 10: "열",
          11: "열한", 12: "열두", 13: "열세", 14: "열네", 15: "열다섯", 16: "열여섯", 20: "스무"}
COUNTERS = ["행", "명", "묶음", "개"]
# ‘번호’로 읽어야 하는 단위: 음성이 ‘1번’을 ‘한 번’(횟수)으로 읽는 일이 있어(2026-11-02 확인) 한자어로 적어 준다
SINO_COUNTERS = ["번"]
DIG = "영일이삼사오육칠팔구"


def sino(n):
    if n == 0:
        return "영"
    out = ""
    for u, name in [(1000, "천"), (100, "백"), (10, "십")]:
        q, n = divmod(n, u)
        if q:
            out += ("" if q == 1 else DIG[q]) + name
    return out + (DIG[n] if n else "")


def speak(text):
    s = text.replace("|", " ")
    for k, v in SIGNS.items():
        s = s.replace(k, v)
    for k in sorted(WORDS, key=len, reverse=True):
        s = re.sub(rf"(?<![A-Za-z_]){re.escape(k)}(?![A-Za-z_])", WORDS[k], s)
    # 함수 괄호는 소리 내지 않는다: ‘카운트(점수)’ → ‘카운트 점수’
    s = re.sub(r"\s*\(\s*", " ", s).replace(")", "")
    s = re.sub(rf"(?<![\d.])(\d+)\s?({'|'.join(COUNTERS)})", lambda m: f"{NATIVE.get(int(m.group(1)), m.group(1))} {m.group(2)}"
               if int(m.group(1)) in NATIVE else m.group(0), s)
    s = re.sub(rf"(?<![\d.])(\d{{1,4}})\s?({'|'.join(SINO_COUNTERS)})(?!호|째)", lambda m: f"{sino(int(m.group(1)))} {m.group(2)}", s)
    return re.sub(r"\s{2,}", " ", s).replace(" ,", ",").replace(" .", ".").strip()


def main():
    for ep in map(Path, sys.argv[1:]):
        out = {"_설명": "AI 음성이 읽을 문장(자막은 script.md 그대로). say_auto.py가 만든다 — 손으로 고칠 문장은 say_manual.json에."}
        manual = json.loads((ep / "say_manual.json").read_text(encoding="utf-8")) if (ep / "say_manual.json").exists() else {}
        for line in (ep / "script.md").read_text(encoding="utf-8").splitlines():
            m = re.match(r"^(\d+)\. (.+)$", line)
            if not m:
                continue
            n, text = m.group(1), m.group(2).strip()
            if n in manual:
                out[n] = manual[n]
                continue
            s = speak(text)
            if s != re.sub(r"\s*\|\s*", " ", text).strip():
                out[n] = s
        (ep / "say.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{ep}: 읽는 법 {len(out) - 1}문장")


if __name__ == "__main__":
    main()
