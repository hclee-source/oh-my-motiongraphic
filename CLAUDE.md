# oh-my-motiongraphic — 골든래빗 영상 작업 한곳 (도서 홍보 · 이벤트 쇼츠 · 개념 영상)

회사 유튜브 ‘합격빠따’에 올리는 영상 작업은 모두 이 폴더에서 한다(2026-10-30 하나로 모음).

| 갈래 | 폴더 | 먼저 읽을 것 |
|---|---|---|
| 도서 홍보 영상 | `videos/<name>/`, `variants/` | 스킬 `goldenrabbit-promo` |
| 이벤트 쇼츠(특강·시험 전 점검 등) | `notices/` → 결과 `videos/notice-<이름>/` | `notices/README.md` |
| 개념 영상(본편·쇼츠) | `concept/` (`C:\hcl\cert-channel`에서 옮김) | `concept/RULES.md`, 스킬 `cert-topics` |

- 공용: `shared/`(폰트·효과음·로고·캐릭터), `tools/`(`check_layout.mjs` 글자 배치 검사, `save_final.py` 완성본 모으기), 파이썬은 맨 위 `.venv` 하나.
- 명령은 맨 위 폴더에서 실행한다. `npx hyperframes` 검사·렌더만 각 영상 폴더 안에서.
- **완성본**: 영상 하나당 폴더 하나 — `완성본/<연-월>/<날짜> <종류> <제목>/` 안에 `<제목> - 본편.mp4`, `- 쇼츠.mp4`, `- 썸네일.png`(공지는 `- 포스터.png`), `업로드 정보.txt`(제목 후보·설명란·태그). 종류는 ‘개념 002’, ‘공지’ 등. `tools/save_final.py --title … --name … 본편=… 쇼츠=… 썸네일=… 정보=…`로 모으고, 개념 영상은 `concept/tools/collect_episode.py`가 한 번에 한다(렌더 도구가 자동 호출). 파일 이름에 ‘|’ ‘?’ 등은 못 쓰므로 실제 유튜브 제목은 업로드 정보에서 복사. 깃허브에는 안 올린다.
- **업로드는 사용자가 직접**(자동 업로드 안 함, 2026-10-30 결정). 대신 작업 스케줄러 ‘합격빠따 영상 알림’이 평일 09:00에 `tools/ready_alarm.py`를 돌려, 완성본에 새로 들어온 파일이 있으면 윈도우 알림을 띄운다(이미 알린 것은 `완성본/.알림기록.json`).

## 도서 홍보 영상
프로젝트 스킬 **`goldenrabbit-promo`**(`.claude/skills/goldenrabbit-promo/SKILL.md`)로 진행한다.
새 영상, 베리에이션(색·스타일·화면비·길이·음악·도서·시드), 레퍼런스 영상 학습이 모두 여기에 포함된다.

- `shared/`: 모든 베리에이션이 공유하는 입력. 로고, Paperlogy 폰트, 도서 카탈로그와 표지(`books/books.json`), 음원 라이브러리(`bgm/catalog.json`).
- `variants/<name>.json`: 베리에이션 스펙이자 기록. `_template.json`을 복사해서 시작한다.
- `videos/<name>/`: HyperFrames 프로젝트 하나가 베리에이션 하나다. 그 안의 CLAUDE.md는 HyperFrames 일반 규칙이다.
- `research/`: 레퍼런스 영상 분석 결과(자막, 프레임 시트, 원칙 문서).

기존 결과물:
- `videos/goldenrabbit-books-promo` (v1, editorial-gold)
- `videos/goldenrabbit-books-promo-v2` (v2, bold-beat + HUD)
- `videos/comhwal1-169-paperpop-1` (2027 빠르게 따는 컴활 1급, paper-pop: 일본 자격증 광고 문법 + 종이층 얼굴, 48s, 스카 BGM)
  - `-jpsong-1` (사용자 Suno 일본어 CM송 56.8s, 9장면 전부) / `-krsong-1` (한국어 CM송 32.7s, 훅·책·6주·클라이맥스·엔딩 5장면)
    — `scripts/retime.py`로 원본 장면을 새 곡 마디에 맞춰 시간 변환한 것. 곡 원본은 `shared/bgm/user/`.

공용 캐릭터: `shared/characters/paper/{base,worry,happy,fired}/` — `assets/`의 얼굴 아이콘을 종이층(切り絵)으로 재생성한 것(README 참고).
