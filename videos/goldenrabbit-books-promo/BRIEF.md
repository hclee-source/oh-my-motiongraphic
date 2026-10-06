---
workflow: music-to-video
flow: automation
storyboard: no
message: "더 탁월한 가치를 제공하는 콘텐츠 — 골든래빗의 시리즈별 대표 도서"
destination: youtube
aspect: 1920x1080
language: ko
audience: "IT·AI·자격증 도서를 찾는 한국 독자"
length: 45s
angle: kinetic-promo
---

## Intent

골든래빗(goldenrabbit.co.kr) 주요 도서를 시리즈별로 소개하는 45초 무(無)내레이션 모션그래픽 홍보영상.
유튜브 영상 「초간단 명령어로 차원이 다른 모션그래픽 만들기」(쌩초 컴퓨터실) 자막에서 도출한 원칙을 그대로 적용한다:
키네틱 타이포그래피 중심 + 도형 혼합, 지정 팔레트 3색(베이스 2 + 포인트 1), 음악 먼저 확보 후 비트에 모션 동기화,
씬별 계획(스토리보드) 후 30fps 렌더, 마지막은 음악 싱크에 맞춰 요소가 "팡" 튀어나오는 피날레.

## Assets

- assets/covers/*.jpg — goldenrabbit.co.kr 홈페이지에서 수집한 도서 표지(사용자 소속 출판사 자산). 시리즈별 섹션에서 비트 컷으로 사용.

## Customizations

- 시리즈 구성(12권+): 이게 되네?(AI 활용) · 바로바로(입문) · 요즘 개발/요즘 바이브 코딩 · 빠따(자격증) · 단행본(AI 국부론, F1 용어집 등).
- BGM: 상업적으로 무료인 로열티프리 카탈로그에서 경쾌한 일렉트로닉/팝 트랙, 45초에 맞춤.
- 피날레: 표지 그리드 + 골든래빗 로고/URL이 비트에 맞춰 팝.

## Notes

- 원칙 설계 문서: ../../research/MOTION_DESIGN_PRINCIPLES.md
- 원본 자막: ../../research/transcript.txt
- 레퍼런스의 교훈 "그대로 따라하지 말고 분위기만 참조·변형" — 특정 영상의 룩을 복제하지 않는다.
- BGM: Mixkit 「Golden Storm」 — Diego Nava (Mixkit Stock Music Free License, 상업 사용 가능·출처표기 불필요). 원곡 34.99–81.59s 구간, 129 BPM, 보컬 없음(whisper 확인). HeyGen 카탈로그는 미로그인 상태라 사용 불가 → 자율 모드로 Mixkit에서 직접 확보.
- frame.md: 셸에 들어 있는 프리셋 중 블랙·골드 브랜드에 맞는 것이 없어서, 로고에서 직접 추출한 골드(#CEAE73)로 골든래빗 전용 스펙을 만들었다(구조는 broadside 프리셋 기반). 한글 서체는 Paperlogy(OFL)를 @font-face로 임베드했다.
