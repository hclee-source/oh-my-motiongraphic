# 공지 쇼츠·포스터 (합격빠따 채널용)

특강 이벤트·CBT 업로드·스터디 모집 같은 공지, 시험 직전 점검 같은 짧은 내용 쇼츠를 같은 틀로 빠르게 만든다. 입력 한 장 → 세로 쇼츠(+ 틀이 있으면 포스터 이미지).

## 만드는 법
1. `notices/data/`에 입력 파일을 만든다. 기존 파일(`adsp-51-lecture.json`)을 복사해 날짜·문구만 바꾸면 된다.
   - 요일은 적지 않는다. 날짜에서 자동으로 계산한다.
   - 화면 한 줄은 12자 안팎(넘으면 경고).
2. 폴더 만들기: `PYTHONUTF8=1 .venv/Scripts/python.exe notices/build_notice.py notices/data/<이름>.json`
   → `videos/notice-<이름>/`(쇼츠), `videos/notice-<이름>/poster/`(포스터)
3. 검사(렌더 전에 반드시):
   - `node tools/check_layout.mjs videos/notice-<이름> --step 0.1` — 0.1초마다 글자 겹침·붙음·쇼츠 가림 자리를 잰다. ‘확실’ 0건이어야 한다.
   - 그 폴더에서 `npx hyperframes check`
4. 렌더:
   - 쇼츠: 그 폴더에서 `npx hyperframes render -o renders/raw.mp4 --workers 2`
   - 효과음 키우기: `ffmpeg -i renders/raw.mp4 -c:v copy -af volume=8dB -c:a aac -b:a 192k renders/<이름>-shorts.mp4`
   - 포스터: `poster/`에서 `npx hyperframes snapshot --at 0.5`
5. 모으기: `.venv/Scripts/python.exe tools/save_final.py --title "공지 <쇼츠 이름>" --name "<쇼츠 이름>" 쇼츠=videos/notice-<이름>/renders/<이름>-shorts.mp4 [포스터=…png] [정보=<제목 적은 글 파일>]` → `완성본/<연-월>/<날짜> 공지 <쇼츠 이름>/` (예: ‘공지 ADsP 51회 시험 전 30초 점검’)

명령은 모두 저장소 맨 위 폴더(`oh-my-motiongraphic`)에서 실행한다(`npx hyperframes` 검사·렌더·효과음 키우기만 그 영상 폴더에서).

## 틀
- 특강 이벤트 `lecture-event`(15초): `templates/lecture-event.html`(쇼츠), `templates/lecture-event-poster.html`(포스터)
  - 장면: 훅 → 특강 이름(표지) → 일시(달력) → 대상 체크 3개 → 참여 방법(좋아요·댓글 입력) + 마지막 3초 멈춤
- 시험 전 30초 점검 `exam-check`(30초, 포스터 없음): `templates/exam-check.html`, 예시 입력 `data/adsp-51-check.json`
  - 장면: 훅 3줄 → ① 분포 모양 개념(곡선이 그려지고 표시 3개가 꽂힘, 답 + 도장 + 반대 경우) → ② 계수 해석 개념(공식 카드 → 틀린 보기 ✗ → 맞는 보기 ✓ → 핵심 한 줄) → 마무리(특강 연결 또는 응원)
  - 화면 위 초시계가 29초 동안 30→0으로 줄고 마지막 1초는 0에서 멈춘다.
  - 글자 약식 표기: `|` 줄바꿈, `^0.7` 위첨자(빈칸 전까지), `_0` 아래첨자(한 글자). 개념 내용(부등호 방향, 숫자)은 렌더 전에 다시 확인한다.
  - ①은 곡선 모양이 ‘오른쪽 꼬리’로 고정이다. 다른 모양의 개념을 넣으려면 틀에 그림을 새로 더한다.
- 하우스 깔끔형: 노랑 #FFE500 · 남색 #1E2687 · 종이 #F2F0EA, 금색은 로고에만. 음악 없음, 효과음만 작게.
- 효과음 목록(`build_notice.py`의 `SFX`) 항목 = [이름, 시각, 길이, 음량, (소리 시작점)]. 앞이 조용한 소리(error·chime 등)는 시작점을 준다(`shared/sfx/peaks.json`의 최고점 직전). 겹치는 소리는 자동으로 다른 트랙에 놓인다.
- 글자 위에 일부러 긋는 도형(취소선 등)은 글자와 도형을 함께 감싼 요소에 `data-layout-allow-overlap`을 붙인다. 검사 도구가 그 안의 겹침만 세지 않는다.
- 첫 화면부터 보이는 것(첫 줄, 초시계)에는 0초 뒤에 시작하는 등장 효과를 걸지 않는다. 첫 프레임에 보였다가 사라지며 깜빡인다. 나중에 들어오는 글자는 CSS로 처음부터 숨겨 둔다.
- 쇼츠 가림 자리에는 글자를 두지 않는다: 위 0~140px, 아래 1450px부터, 오른쪽 960px부터·1000px 아래
- 장면마다 `data-layout-cover`가 붙어 있다. 다음 장면이 덮으며 들어올 때 검사 도구가 겹침으로 오해하지 않게 하는 표시다.
- 들어오는 글자에는 `in`(처음엔 숨김), 강조 상자에는 `sx`(처음엔 접힘)를 붙인다. 이게 없으면 등장 효과 전에 글자가 먼저 비친다.

## 다음에 만들 틀
CBT 업로드 안내, 온라인 스터디 모집, 도서 소개, 합격 후기. `type`을 새로 정하고 틀 두 장(쇼츠·포스터)과 `build_notice.py`의 `DURATION`·`SFX`에 항목을 더한다.
