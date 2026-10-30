# 앞·옆·뒤 그림에서 캐릭터 실루엣(가면)을 뽑는다. 사용: python segment.py
# 먼저 npx hyperframes remove-background 로 out/cut_{front,side,back}.png 를 만들어 둔다.
import cv2, numpy as np, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "refs", "lucas")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

def mask_of(path):
    # 배경 지우기 모델(hyperframes remove-background) 결과 out/cut_<이름>.png 의 투명도로 가면을 만든다
    img = cv2.imread(path)
    h, w = img.shape[:2]
    name = os.path.splitext(os.path.basename(path))[0]
    cut = cv2.imread(os.path.join(OUT, f"cut_{name}.png"), cv2.IMREAD_UNCHANGED)
    alpha = cv2.resize(cut[:, :, 3], (w, h))
    fg = (alpha > 128).astype(np.uint8)
    # 가장 큰 덩어리만 남기고 구멍 메우기
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg, 8)
    big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    fg = (lab == big).astype(np.uint8)
    inv = (1 - fg).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 4)
    for i in range(1, n):
        x, y, ww, hh, a = st[i]
        if x > 0 and y > 0 and x + ww < w and y + hh < h:
            fg[lab == i] = 1
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    return img, fg

info = {}
for name in ["front", "side", "back"]:
    img, m = mask_of(os.path.join(REF, name + ".png"))
    cv2.imwrite(os.path.join(OUT, f"mask_{name}.png"), m * 255)
    over = img.copy()
    over[m == 0] = (over[m == 0] * 0.35 + np.array([255, 0, 255]) * 0.65).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"maskview_{name}.jpg"), cv2.resize(over, (1024, 1024)))
    ys, xs = np.nonzero(m)
    info[name] = dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()))
print(json.dumps(info, indent=1))
