---
workflow: music-to-video
flow: automation
storyboard: no
message: "골든래빗 — 시리즈별 대표 도서 16권, 비트에 맞춰 과감하게"
destination: youtube
aspect: 1920x1080
language: ko
audience: "IT·AI·자격증 도서를 찾는 한국 독자"
length: 46.6s
angle: kinetic-promo
---

## Intent

v1(블랙·골드, 차분한 에디토리얼)의 v2. 사용자가 "레퍼런스처럼 과감하게"를 선택했다.
레퍼런스 영상(쌩초 컴퓨터실, qi3DHzhUSjs)의 데모 화면을 분석해 얻은 시각 원칙 E1–E13
(../../research/MOTION_DESIGN_PRINCIPLES.md §E)을 적용한다. 고채도 옐로, 비트마다 배경 플립,
라벨 박스, 영문/한글 짝, 서체 섞기, HUD 크롬, 마퀴, 도형 컨페티, 단어 단위 컷이다.
골드는 로고에만 쓴다. 레퍼런스의 카피·브랜딩·레이아웃은 복제하지 않고 기법만 차용한다.

## Assets

- assets/covers/*.jpg — 도서 표지 16장 (goldenrabbit.co.kr)
- assets/brand/icon.png — 골드 로고 마크
- assets/bgm.mp3 — v1과 동일 (Mixkit 「Golden Storm」, Diego Nava, 34.99–81.59s, 129 BPM)

## Customizations

- HUD 오버레이 컴포지션(compositions/hud.html)이 전 구간 위에 올라간다. 모서리 라벨, 타임코드, 시리즈 인디케이터, 하단 티커 띠와 눈금자를 맡는다.
- 프레임 구간·도서 배치·음악은 v1과 동일하다.

## Notes

- 서브컴포지션 CSS는 `#stage` 그대로 쓴다(`#stage[data-composition-id=…]` 금지 — 컴파일러가 스코프를 붙이며 이 형태는 매칭이 깨진다). id/class는 프레임 접두사(f1_ …)를 붙인다.
