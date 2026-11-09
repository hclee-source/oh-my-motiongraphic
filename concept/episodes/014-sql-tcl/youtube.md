# 014 업로드용 정보

## 제목 (하나 고르기)
- ROLLBACK을 세 번 했는데 왜 4행일까? COMMIT · ROLLBACK · SAVEPOINT | SQLD
- ROLLBACK TO는 어디까지 되돌릴까? SAVEPOINT 따라가기 | SQLD
- DDL 다음 ROLLBACK이 안 되는 이유, 오라클 자동 커밋 | SQLD

## 설명란

과일 표 하나에 명령 열 줄을 차례로 실행하며 행 수를 셉니다. ROLLBACK TO 저장점이 되돌리는 범위, 그 뒤에 만든 저장점이 사라지는 이유, 이름 없는 ROLLBACK은 마지막 COMMIT까지만 돌아간다는 점, 같은 이름의 SAVEPOINT, 오라클에서 DDL을 실행하면 자동으로 COMMIT되는 함정과 SQL Server와의 차이를 정리합니다.

0:00 ROLLBACK을 세 번 하면
0:31 트랜잭션과 세 명령
1:18 INSERT와 SAVEPOINT A
1:43 UPDATE, SAVEPOINT B, DELETE
2:02 ROLLBACK TO B
2:20 ROLLBACK TO A
2:45 COMMIT 다음의 ROLLBACK
3:13 같은 이름의 SAVEPOINT
3:37 DDL은 자동으로 COMMIT
4:25 시험장 체크
4:50 한 줄 정리

#SQLD #SQL개발자 #TCL #COMMIT #ROLLBACK

## 태그
SQLD, SQL 개발자, TCL, 트랜잭션, COMMIT, ROLLBACK, SAVEPOINT, 자동 커밋, 데이터 자격증

## 썸네일
- 완성본 영상 폴더의 ‘… - 썸네일.png’(작업 폴더에서는 thumbnail.png)
