---
종류: 쇼츠(9:16, 약 1분) — 본편 014 핵심 요약
제목 후보:
  - ROLLBACK은 어디까지 되돌릴까? 1분 정리
  - DDL 다음에 ROLLBACK이 안 되는 이유
위 고정 제목: ‘ROLLBACK은 어디까지’
상태: 검수 반영·장면 완성, 렌더 대기 (2026-11-06). 문장 안 ‘|’는 자막을 끊는 자리(소리에는 안 씀). 본편 과일 표는 쓰지 않고 이름 없는 행 블록으로만.
---

## 1. 처음으로 돌아갈까
> 화면: 큰 ‘ROLLBACK’ 카드 → 아래 ‘처음으로?’ 칩 → 규칙 세 칸 자리(빈 카드 세 장).

1. ROLLBACK을 하면 | 무조건 처음으로 | 돌아갈까요?
2. 그렇지 않습니다. | 규칙은 세 가지입니다.

## 2. ROLLBACK TO
> 화면: 세로로 쌓이는 행 블록(글자 없이 ‘INSERT’ 표시만) — 블록 하나 → 깃발 ‘A’ → 블록 하나 더 → ROLLBACK TO A → 뒤 블록만 사라지고 앞 블록 · 깃발 A는 남음.

3. 행 하나를 넣고 | SAVEPOINT A로 | 저장 지점을 만든 뒤, | 한 행을 더 넣었습니다.
4. 이제 ROLLBACK TO A를 하면 | A 뒤에 넣은 | 한 행만 취소됩니다.
5. A보다 앞의 작업은 | 그대로 남습니다.

## 3. 이름 없는 ROLLBACK
> 화면: ‘COMMIT’ 선 → 그 아래 변경 블록 두 개와 깃발 → ROLLBACK → COMMIT 선까지 되감기, 깃발도 사라짐 → COMMIT 선 위 블록에 자물쇠 표시.

6. 이름 없이 ROLLBACK만 하면 | 마지막 COMMIT 시점으로 | 돌아갑니다.
7. 그동안 만든 저장 지점도 | 모두 사라집니다.
8. 이미 COMMIT한 내용은 | ROLLBACK으로 되돌릴 수 없습니다.

## 4. DDL은 자동 COMMIT
> 화면: 세 줄 카드 DELETE → CREATE TABLE(옆에 ‘자동 COMMIT’ 칩) → ROLLBACK ✕ → 지운 행 블록은 돌아오지 않음.

9. 오라클에서는 CREATE, DROP 같은 | DDL을 실행하면 | 자동으로 COMMIT됩니다.
10. 그래서 DELETE 다음에 | 테이블을 하나 만들고 | ROLLBACK해도, | 지운 행은 돌아오지 않습니다.

## 5. 한 줄 정리
> 화면: 세 줄 정리 — ROLLBACK TO → 저장 지점까지 / ROLLBACK → 마지막 COMMIT까지 / DDL → 그 자리에서 COMMIT.

11. ROLLBACK TO는 저장 지점까지, | 그냥 ROLLBACK은 | 마지막 COMMIT까지, | DDL은 그 자리에서 | COMMIT입니다.
