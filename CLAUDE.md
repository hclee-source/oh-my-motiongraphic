# oh-my-motiongraphic — 골든래빗 도서 홍보 모션그래픽

이 폴더의 영상 작업은 프로젝트 스킬 **`goldenrabbit-promo`**(`.claude/skills/goldenrabbit-promo/SKILL.md`)로 진행한다.
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
