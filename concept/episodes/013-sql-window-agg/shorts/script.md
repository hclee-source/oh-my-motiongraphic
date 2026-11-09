---
종류: 쇼츠(9:16, 약 1분) — 본편 013 핵심 요약
제목 후보:
  - ROWS와 RANGE 차이, 1분 정리
  - 같은 값이면 누적합도 같다? 기본 범위 RANGE
위 고정 제목: ‘ROWS와 RANGE’
상태: 검수 반영·장면 완성, 렌더 대기 (2026-11-09). 문장 안 ‘|’는 자막을 끊는 자리(소리에는 안 씀). 본편 예시(급여 200~700)는 쓰지 않음.
예시 숫자(검수용): 값 40, 50, 50, 60 → SUM(값) OVER (ORDER BY 값) = 기본 RANGE 40, 140, 140, 200 (40 + 50 + 50 = 140) / ROWS 누적 40, 90, 140, 200 / LAST_VALUE(값) OVER (ORDER BY 값) 40, 50, 50, 60 (자기 값), + ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING → 60 × 4 / LAG(값) NULL, 40, 50, 50 / LEAD(값) 50, 50, 60, NULL (verify_examples.py로 확인)
---

## 1. 같은 값, 같은 누적합
> 화면: 작은 SQL 카드 ‘SUM(값) OVER (ORDER BY 값)’ → 숫자 카드 40 · 50 · 50 · 60 → 아래에 누적 40 · 140 · 140 · 200이 차례로 → 140 두 장을 한 테두리로 묶고 위에 ‘?’.

1. SUM(값) | OVER (ORDER BY 값)으로 | 40, 50, 50, 60을 누적하면 | 40, 140, 140, 200입니다.
2. 같은 50인 두 행이 | 똑같이 140을 받습니다.

## 2. 기본 범위는 RANGE
> 화면: 생략된 줄 ‘RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW’ → 칩 ‘처음부터 현재 행까지’ → 50 두 장을 한 테두리로, 칩 ‘같은 값 = 함께’.

3. ORDER BY만 적으면 | 기본 범위는 RANGE, | 처음부터 현재 행까지입니다.
4. RANGE는 값으로 범위를 정해서, | 같은 값의 행을 | 함께 더합니다.

## 3. ROWS
> 화면: RANGE가 ROWS로 바뀌고 누적이 40 · 90 · 140 · 200으로 → 50 두 장 아래 90 / 140으로 갈림.

5. ROWS로 적으면 | 실제 행을 하나씩 세서 | 40, 90, 140, 200입니다.
6. 같은 50이어도 | 먼저 오는 행은 90, | 다음 행은 140입니다.

## 4. LAST_VALUE
> 화면: SQL 카드 ‘LAST_VALUE(값) OVER (ORDER BY 값)’ → 결과 40 · 50 · 50 · 60(위 숫자 카드와 똑같음) → 카드에 ‘ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING’이 붙으면 60 · 60 · 60 · 60.

7. LAST_VALUE는 | 맨 끝 값을 가져오는데, | 기본 범위가 현재 행에서 끝나서 | 자기 값이 나옵니다.
8. 맨 끝 값을 보려면 | 범위를 | UNBOUNDED FOLLOWING까지 | 넓혀야 합니다.

## 5. LAG와 LEAD
> 화면: 40 · 50 · 50 · 60 카드 아래 두 줄 — LAG(한 칸 앞 화살표) NULL · 40 · 50 · 50 / LEAD(한 칸 뒤 화살표) 50 · 50 · 60 · NULL.

9. LAG는 바로 앞 행의 값, | LEAD는 바로 뒤 행의 값을 가져오고, | 가져올 행이 없으면 NULL입니다.

## 6. 한 줄 정리
> 화면: 두 줄 정리 — ‘ORDER BY만 → RANGE, 같은 값은 함께’ / ‘한 행씩 → ROWS’.

10. ORDER BY만 적으면 RANGE라서 | 같은 값은 함께 더하고, | 한 행씩 더하려면 | ROWS를 적습니다.
