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
