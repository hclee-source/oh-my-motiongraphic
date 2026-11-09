# 013 업로드용 정보

## 제목 (하나 고르기)
- 같은 급여 두 명, 누적합이 똑같은 이유? ROWS와 RANGE | SQLD
- LAST_VALUE가 마지막 값이 아닌 이유, 윈도우 함수 기본 범위 | SQLD
- 누적합부터 LAG · LEAD까지, 윈도우 함수 범위 한 번에 | SQLD

## 설명란

직원 다섯 명의 급여로 윈도우 함수의 범위를 직접 계산합니다. OVER 안에 ORDER BY를 넣으면 누적합이 되는 이유, 생략된 기본 범위가 RANGE라서 같은 값끼리 누적합이 같아지는 함정, ROWS와의 차이, PARTITION BY, 앞뒤 한 행만 더하는 이동 합, LAG·LEAD, LAST_VALUE의 함정, 그리고 RATIO_TO_REPORT·PERCENT_RANK·CUME_DIST·NTILE까지 정리합니다.

0:00 같은 급여, 같은 누적합
0:35 집계 함수에 OVER
1:02 ORDER BY를 넣으면 누적
1:23 생략된 범위, RANGE
1:55 한 행씩 세는 ROWS
2:20 부서마다 다시 시작
2:40 앞뒤 몇 행만
3:05 LAG와 LEAD
3:41 LAST_VALUE의 함정
4:12 비율 함수
4:54 시험장 체크
5:25 한 줄 정리

#SQLD #SQL개발자 #윈도우함수 #ROWS #RANGE

## 태그
SQLD, SQL 개발자, 윈도우 함수, 누적합, ROWS, RANGE, LAG, LEAD, LAST_VALUE, NTILE, 데이터 자격증

## 썸네일
- 완성본 영상 폴더의 ‘… - 썸네일.png’(작업 폴더에서는 thumbnail.png)
