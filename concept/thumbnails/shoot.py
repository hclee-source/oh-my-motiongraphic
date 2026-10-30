"""썸네일 틀(thumb.html)을 Chrome 화면 없이 찍어 PNG로 저장한다.

사용(저장소 맨 위에서): python concept/thumbnails/shoot.py <편 번호> <스타일 a|b|c> [--badge] [--out 파일.png]
기본 저장 위치: concept/thumbnails/out/<편>-<스타일>[-badge].png
"""
import argparse, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("style")
    ap.add_argument("--badge", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--group", help="색만 미리 보기: 다른 주제 묶음의 바탕색으로 찍는다")
    a = ap.parse_args()
    out = Path(a.out) if a.out else HERE / "out" / f"{a.ep}-{a.style}{'-badge' if a.badge else ''}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    url = (HERE / "thumb.html").as_uri() + f"?ep={a.ep}&style={a.style}&badge={1 if a.badge else 0}"
    if a.group:
        from urllib.parse import quote
        url += "&group=" + quote(a.group)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1280,720", "--virtual-time-budget=4000", f"--screenshot={out}", url],
                   check=True, capture_output=True)
    print(out)


if __name__ == "__main__":
    main()
