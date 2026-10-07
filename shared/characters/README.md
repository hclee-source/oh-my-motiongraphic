# 종이층(paper-cut) 캐릭터 얼굴

`assets/`의 낙서풍 얼굴 아이콘 13명(에스더는 앞머리 없는 버전 사용)을 OpenAI 이미지 편집 API(`.env`의 `OPENAI_IMAGE_MODEL`)로
겹겹이 쌓인 색 카드지(切り絵/페이퍼크래프트) 스타일로 재생성한 것. 1024×1024 투명 PNG.

| 폴더 | 내용 | 프롬프트 |
|---|---|---|
| `paper/base/` | 기본 표정 (원본 → 재생성) | `prompt_base.txt` |
| `paper/worry/` | 시험 걱정: 八자 눈썹, 지그재그 입, 하늘색 땀방울 | `prompt_worry.txt` (base를 입력으로 편집) |
| `paper/happy/` | 합격 기쁨: ^^ 눈, 크게 웃는 입, 노란 반짝이 | `prompt_happy.txt` (base를 입력으로 편집) |

slug ↔ 원본: p=P, rei=레이, lucas=루카스, bible=바이블, benny=베니, cindy=신디, esther=에스더, alice=엘리스,
ian=이안, jini=지니, kate=케이트, thomas=토마스, toynbee=토인비.

표정 변형은 항상 base 이미지를 입력으로 넣어 만든다(캐릭터 일관성). 재생성:
`.venv/bin/python -I shared/characters/gen_paper.py <in.png> --out <out.png> --prompt <prompt.txt>` (동시 4개 이하 권장, 7개 동시엔 요청이 멈췄다).
