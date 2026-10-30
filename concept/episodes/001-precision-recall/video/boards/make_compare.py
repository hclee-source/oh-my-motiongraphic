"""비교용 정지 컷: index.html의 변수 기본값(:root와 변수 목록 둘 다)만 바꿔 같은 장면을 찍는다.

사용: python -I boards/make_compare.py <세트 이름>
"""
import re, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
BACKUP = ROOT / "boards" / ".index.before-compare.html"

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

SETS = {
    # 바이올렛 강조색에서 배경만 바꿔 본다
    "bg": {
        "times": "11.5,17.5",
        "variants": [
            ("g1-gray", {}),
            ("g2-lavender", {"color-ground": "#F3F1FA", "color-line": "#E5E1F3", "color-hair": "#D6D0EA",
                             "color-dot": "#D0CAE3", "color-shadow": "rgba(40,20,90,0.06)"}),
            ("g3-white", {"color-ground": "#FFFFFF", "color-card": "#F5F5F7", "color-line": "#ECECF0",
                          "color-hair": "#DADAE0", "color-dot": "#C8C8D2", "color-shadow": "rgba(0,0,0,0)"}),
        ],
    },
}

def apply(html, overrides):
    for key, val in overrides.items():
        html = re.sub(rf"(--{key}: )[^;]+;", lambda m: m.group(1) + (f'"{val}"' if key.startswith("font") else val) + ";", html, count=1)
        html = re.sub(rf'("id":"{key}",[^}}]*"default":")[^"]*"', lambda m: m.group(1) + val + '"', html, count=1)
    return html

def main(set_name):
    spec = SETS[set_name]
    shutil.copy(INDEX, BACKUP)
    base = INDEX.read_text(encoding="utf-8")
    try:
        for name, overrides in spec["variants"]:
            acc = overrides.get("color-accent", re.search(r"--color-accent: (#[0-9A-Fa-f]{6});", base).group(1))
            ground = overrides.get("color-ground", re.search(r"--color-ground: (#[0-9A-Fa-f]{6});", base).group(1))
            print(f"{name}: 강조색 대비 {contrast(acc, ground):.2f}")
            INDEX.write_text(apply(base, overrides), encoding="utf-8")
            out = ROOT / "boards" / "compare" / name
            subprocess.run(["npx.cmd", "hyperframes", "snapshot", "--at", spec["times"], "--no-end",
                            "--describe", "false", "-o", str(out)], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        shutil.copy(BACKUP, INDEX)
    print("완료")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bg")
