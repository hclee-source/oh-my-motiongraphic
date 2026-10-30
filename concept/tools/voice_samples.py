"""목소리 후보 미리듣기: 1장 대본으로 남자 목소리 후보를 만든다."""
import asyncio, sys
from pathlib import Path
import edge_tts

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
TEXT = ("정확도 99%인 질병 진단 모델이 있습니다. 그런데 이 모델은 환자를 한 명도 찾아내지 못합니다. "
        "어떻게 이런 일이 생길까요? 오늘은 이 함정을 피하게 해 주는 두 숫자, 정밀도와 재현율을 알아보겠습니다.")
CANDIDATES = [
    ("A-인준-기본", "ko-KR-InJoonNeural", "+0%", "+0Hz"),
    ("B-인준-낮게", "ko-KR-InJoonNeural", "-6%", "-12Hz"),
    ("C-현수-기본", "ko-KR-HyunsuMultilingualNeural", "+0%", "+0Hz"),
    ("D-현수-낮게", "ko-KR-HyunsuMultilingualNeural", "-6%", "-12Hz"),
]

async def main():
    for name, voice, rate, pitch in CANDIDATES:
        await edge_tts.Communicate(TEXT, voice, rate=rate, pitch=pitch).save(str(OUT / f"{name}.mp3"))
        print("만듦", name)

asyncio.run(main())
