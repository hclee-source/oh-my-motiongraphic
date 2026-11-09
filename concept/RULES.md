# 채널 규칙 (자격증 개념 해설 채널)

매일 자동으로 대본·화면을 만들 때 이 파일을 먼저 읽고 따른다. 사용자가 정한 규칙이 생길 때마다 여기에 더한다.

- 위치: `C:\hcl\oh-my-motiongraphic\concept\`(2026-10-30 `C:\hcl\cert-channel`에서 옮김). 명령은 모두 저장소 맨 위 폴더(`oh-my-motiongraphic`)에서 실행한다. 파이썬은 맨 위의 `.venv/Scripts/python.exe`.
- 이 파일과 `topics/topics.json`에 적힌 `episodes/...` 경로는 `concept/` 기준이다.
- 글자 배치 검사 도구는 이벤트 쇼츠와 함께 쓰므로 맨 위 `tools/check_layout.mjs`에 있다.
- 다 만든 것은 영상 하나당 폴더 하나로 모은다: `완성본/<연-월>/<날짜> 개념 <번호> <제목>/`에 `<제목> - 본편.mp4`, `- 쇼츠.mp4`, `- 썸네일.png`, `업로드 정보.txt`(youtube.md 본편+쇼츠). 도구 `concept/tools/collect_episode.py concept/episodes/<편> "<제목>"`(렌더 도구가 끝에 자동 호출, 썸네일·업로드 정보를 나중에 만들었으면 한 번 더 돌린다).

## 제작 체계 (2026-10-29 확정)
역할 다섯 개만 둔다. 댓글 관리는 하지 않는다.
1. 소재 목록: 출제기준 기반 개념 목록·진행표, 다음 주제 고르기
2. 대본 쓰기: 본편·쇼츠 대본, 읽는 법(say.json)
3. 대본 검수: 계산 재확인, 정의 대조, 이 파일 규칙 위반 검사(쓴 역할과 따로)
   → 사용자 확인 ①: 대본 승인
4. 화면·편집: 장면 → 음성 → 조립 → 배치 검사 → 렌더 → 소리 크기
5. 제목·썸네일: 업로드 정보, 썸네일 이미지
   → 사용자 확인 ②: 완성본 보고 직접 업로드

역할별 스킬(맨 위 `.claude/skills/`): 1번 소재 목록 = `cert-topics`(목록 `concept/topics/topics.json`, 진행표 `concept/topics/진행표.md`).

4번 화면·편집 명령(맨 위 폴더에서, 2026-10-30 002~006 다섯 편을 만들며 정리):
- 새 편 뼈대: `.venv/Scripts/python.exe concept/tools/new_episode.py <번호>-<id> "<제목>"` (본편·쇼츠 프로젝트 설정·글꼴·효과음·공용 틀 복사)
- 한 번에: 조립+검사 `bash concept/tools/check_episode.sh concept/episodes/<편>` → 장마다 한 장 `concept/tools/sheet.py concept/episodes/<편> [--shorts]`(boards/review/sheet.jpg를 눈으로 확인) → 렌더·소리 크기·완성본 `concept/tools/render_episode.py concept/episodes/<편> "<제목>"` → 업로드 정보 `concept/tools/youtube_info.py <정보 JSON>` → 썸네일(아래) → 마지막에 `collect_episode.py`로 완성본 영상 폴더를 다시 채운다
- 썸네일(5번 역할, 2026-10-30 사용자 선택 = 함정 경고형 d): 바탕은 주제 묶음별 색(thumb.html의 GROUP, 모델 평가 = 노랑, 연관분석 = 하늘, 군집분석 = 연두 …, 새 편은 EPG에 묶음을 적는다), 위에 빨간 ‘ADsP · 빅분기’ 표(SQLD 편은 ‘SQLD’, 바탕은 SQL 기본 = 민트, SQL 활용 = 주황), 윗줄(9자 안팎) + 흔한 오해 한 마디(물음표 포함 4자 안팎, 흰 글자·검은 테두리)에 가는 빨간 ✕, 오른쪽 작은 그림, 아래 검은 띠에 노란 한 줄(14자 안팎). 근거 없는 숫자(‘99%가 틀림’ 등)는 쓰지 않는다. 글자·그림은 `concept/thumbnails/thumb.html`의 EP에 편마다 적고 `.venv/Scripts/python.exe concept/thumbnails/shoot.py <번호> d --badge` → 편 폴더 `thumbnail.png`로 복사(완성본에는 `collect_episode.py`가 넣는다). 쇼츠는 따로 만들지 않는다(영상 한 장면을 표지로).
- 렌더 중에는 배치 검사(브라우저를 띄움)를 같이 돌리지 않는다(메모리 부족으로 렌더가 죽은 적 있음).
- 무거운 명령(배치 검사·사진·받아 적기·음성·렌더)은 줄 세우기 도구 앞에 붙여 하나씩만 돌린다: `.venv/Scripts/python.exe tools/heavy.py --wait 900 <명령…>`(차례가 안 오면 종료 코드 75 → 같은 명령을 다시). 뒤에서 돌리는 창은 메모리가 모자라면 강제 종료되니 앞에서 돌린다.
- 한 번에 한 편씩 만든다(2026-11-09 결정). 2026-11-05에 열두 편을 동시에 돌렸더니 줄 다툼으로 기다림이 길어지고, 작업자마다 토큰을 35만~44만씩 써서 사용 한도로 18시간 멈췄다. 한 편씩 하면 장면 만들기 40분 안팎 + 렌더 12~14분(본편 5분 기준)이다. 렌더는 토큰을 쓰지 않으니 다음 편 장면 만들기와 겹쳐 돌린다.
- 본편 길이는 3~4분을 목표로 쓴다. 5~6분이면 장면·검사·렌더 시간이 1.5배로 는다(2026-11 SQLD 012~023편 실측).
- 음성: `.venv/Scripts/python.exe concept/tools/tts_episode.py concept/episodes/<편>`
- 조립: `.venv/Scripts/python.exe concept/tools/build_video.py concept/episodes/<편>`
- 배치 검사: `node tools/check_layout.mjs concept/episodes/<편>`
- 렌더: `concept/episodes/<편>/video`에서 `npx hyperframes render -o renders/<편>.mp4 --workers 2`
- 소리 크기: 같은 폴더에서 `ffmpeg -i renders/<편>.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k renders/<번호>-<한글 제목>.mp4`
- 모으기: `.venv/Scripts/python.exe concept/tools/collect_episode.py concept/episodes/<편> "<제목>"`

## 내용
- 주제: ADsP·빅데이터분석기사 필기 공통 개념부터, 개념 하나 = 한 편.
- SQLD 편(2026-11-02부터, 007~011): 시험이 다가오면 SQLD 개념을 소재 목록 앞으로 당겨 만든다. 정답 기준은 시험과 같은 오라클 문법이고, SQL Server와 다른 점은 한 줄로만 짚는다. 예시는 작은 표 하나를 놓고 SQL을 한 단계씩 실행해 결과 행을 세어 보이는 방식. 화면은 어두운 SQL 카드(예약어만 #A68CFF, 지금 처리하는 줄만 밝게) + 흰 결과 표(행 수를 표 머리에 표시). 새 편은 `new_episode.py ... --sql`로 만들면 SQL 모양이 붙고, 007 장면들이 본보기다.
- SQL 편의 읽는 법은 `concept/tools/say_auto.py concept/episodes/<편> concept/episodes/<편>/shorts`로 자동으로 만든다(SELECT → 셀렉트, NULL → 널, ‘5행’ → 다섯 행 등). 자동이 어색한 문장만 편 폴더 `say_manual.json`에 적는다. 새 SQL 낱말은 say_auto.py의 WORDS에 더한다.
- 채널: 개념 영상·기출문제 풀이 영상 모두 회사 유튜브(골든래빗 ‘합격빠따’)에 올린다(2026-10-29 사용자 결정, 처음엔 개인 채널 계획이었음).
- 원재료: 공개된 출제기준이 뼈대. 회사 채널이므로 골든래빗 책의 원고·기출문제 자료도 쓸 수 있다. 쓸 때도 숫자·정답은 3번 역할(검수)에서 다시 계산·확인한다.
- 대본에 나오는 숫자 계산은 전부 다시 계산해 확인한다. 성립할 수 없는 예시(정밀도 1·재현율 0 같은 것)는 쓰지 않는다.
- 다음 편 예고 문장은 넣지 않는다.
- 영상 안(화면·자막·내레이션)에는 시험 이름(ADsP, 빅데이터분석기사 필기 등)을 넣지 않는다. 시험 이름은 업로드 정보(제목·설명란·태그)에서 검색용으로만 쓴다.
- 화면에 편 번호(‘개념 001’ 등)를 넣지 않는다. 주제 순서는 바뀔 수 있다.
- 화면에는 내레이션을 돕는 글자만 둔다. 설명이 끝난 그림(앞 장면에서 넘어온 막대 등)은 다시 쓰일 때까지 흐리게 둔다.

## 표기
- 강조·인용에는 홑따옴표 ‘ ’만 쓴다. 쌍따옴표(" ", “ ”)는 화면·자막·대본·썸네일·설명란 어디에도 쓰지 않는다.
- 말투: ‘~입니다’체, 한 문장은 소리 내어 읽기 편한 길이로.

## 형식
- 매일: 본편 4~6분(16:9) + 쇼츠 1~2개(9:16).
- 목소리: 지금은 AI 음성(Microsoft 인준 ko-KR-InJoonNeural, 기본 속도·높이). 나중에 사용자 본인 녹음 → 목소리 복제로 바꿀 수 있음. 업로드는 사용자가 직접.
- AI 음성이 읽을 문장은 `say.json`에 따로 적는다: 숫자는 고유어 단위에 맞게(20통→스무 통, 10명→열 명), 영문 약어는 한글 소리로(TP→티피, F1→에프원, ADsP→에이디에스피). 자막은 script.md 그대로.
- 배경음악 없음. 효과음은 작게(카드 등장 ‘톡’, 강조 이동 ‘딸깍’, 장면 전환 ‘휙’).

## 화면
- 배경 연회색 #F1F2F5 + 흰 카드. 따뜻한 아이보리·크림 배경 금지(클로드 화면색과 겹침).
- 강조색 바이올렛 #6B3FE6 하나, 한 화면에 초점 하나. 어두운 수식 카드(#18181B) 위에서는 #A68CFF.
- 글꼴 페이퍼로지(Paperlogy, OFL).
- 움직임 속도: 본편은 느긋하게(배율 1.6), 쇼츠는 빠르게(배율 1.0).
- 연출: 장면끼리 이어지는 변신, 여는 제목 장면, 효과음. 핵심 숫자 확대·형광펜 연출은 쓰지 않는다.
- 세부 수치는 각 편 `video/SPEC.md`.

## 쇼츠
- 본편 핵심을 1분 안팎으로 요약한 새 대본(본편 잘라 붙이기 아님). 본편의 계산 예시·심화 내용은 뺀다. 끝에 ‘본편 보러 오세요’ 같은 문장은 넣지 않고, 업로드 때 ‘관련 동영상’으로 본편을 연결한다.
- 폴더 `episodes/<편>/shorts/`(script.md, say.json, build.json, video/). 세로 1080×1920, 같은 색·글꼴·카드, 움직임 배율 1.0.
- 위쪽에 주제 이름(‘정밀도 vs 재현율’ 같은)을 영상 내내 고정.
- 가림 자리 피하기: 위 0~140px(쇼츠 메뉴), 아래 1450px부터(채널 이름·설명), 오른쪽 960px부터·1000px 아래(좋아요 버튼). 그림은 y 300~1250, 자막은 y 1300~1380.
- 자막은 짧게 끊는다. 대본 문장 안에 ‘|’로 끊을 자리를 적는다(소리에는 안 쓰임). 말 덩어리(‘암 검진’, ‘네 칸짜리’) 중간에서 끊지 않는다.
- 음성: `concept/tools/tts_episode.py concept/episodes/<편>/shorts --title-dur 0 --sent-gap 0.2 --chapter-gap 0.45 --tail 1.0`.

## 음성 검증(2026-11-02 SQLD 편에서 AI 음성 결함을 찾은 뒤 추가, 음성을 만든 뒤 반드시)
- `.venv/Scripts/python.exe concept/tools/listen_episode.py concept/episodes/<편> concept/episodes/<편>/shorts`: 문장마다 받아 적어(음성 인식 large-v3-turbo) 읽을 말과 대조 → `listen/report.txt`의 ▲(일치 0.9 미만)를 하나씩 본다. 받아 적기가 소리가 같은 다른 글자로 적은 것(널을→너를, 소계→소개, 조인은→조이는)은 괜찮고, 음절·숫자가 빠졌거나 다른 말로 들리면 대본을 고친다(say_auto.py 머리말의 확인된 결함 목록 참고). 바뀐 문장만 다시 듣는다. 받아 적기는 빠른 방식(beam_size=1, 2026-11-05부터)이라 ▲가 조금 더 뜰 수 있다. 하나씩 판단한다. 받아 적은 뒤에 대본 문장을 고쳤으면 그 문장을 다시 들은 뒤 시각 맞추기를 한다(안 그러면 옛 문장의 시각이 남는다).
- 화면 장면이 대본 ‘> 화면:’과 맞는지, 오답 칩에 ✕가 있는지, 맞는 문장 옆에 ✕를 잘못 붙이지 않았는지 사진으로 확인한다(2026-11-09 020 쇼츠 ‘-3’ 칩, 021 ‘존재성’ 카드에서 발견).
- `.venv/Scripts/python.exe concept/tools/verify_episode.py --no-pops --write-times concept/episodes/<편>`: 그림 시각(build.json extra)·자막 나눔을 실제 말 시각과 대조하고 `word_times.json`을 만든다 → 다시 조립하면 그림·자막이 실제 말에 맞춰진다. 자동으로 못 찾은 낱말은 `word_times.manual.json`에 직접 적는다. 장면 안에 숫자를 하나씩 찍는 연출은 `listen/words.json`의 실제 시각을 넣는다(글자 수·고정 간격 추정 금지).
- 렌더 뒤: `verify_episode.py concept/episodes/<편>`로 최종 영상의 소리 찢어짐·박자 밀림·조용한 구간 잡음·화면 번쩍임을 본다.

## 검사(렌더 전에 반드시)
- `node tools/check_layout.mjs concept/episodes/<편>`: 영상을 0.2초마다 넘기며 글자끼리 겹침, 자막과 겹침, 글자와 도형 겹침, 카드·화면 밖 넘침, 카드끼리 겹침, 잘린 글자, 너무 붙은 글자(글자 크기의 1/4 또는 10px 미만), 카드 가장자리·다른 카드에 16px 미만으로 붙은 글자를 찾는다. ‘확실’ 0건이어야 렌더한다. 장면이 바뀌는 0.2초 동안 흐릿하게 스치는 ‘잠깐’은 괜찮다.
- 그다음 `npx hyperframes check`(오류 0건), 고친 자리는 사진(snapshot)으로 눈 확인.
