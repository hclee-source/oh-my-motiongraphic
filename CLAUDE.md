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
