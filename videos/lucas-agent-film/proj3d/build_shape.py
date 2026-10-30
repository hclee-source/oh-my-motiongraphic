# 앞·옆 실루엣으로 입체를 세우고, 앞·뒤·옆 그림을 어느 면에 얼마나 입힐지(가중치) 계산한다.
# 사용: python build_shape.py   (먼저 segment.py) → out/lucas_shape.npz, out/tex_{front,side,back}.png
import cv2, numpy as np, os, json
from scipy import ndimage as ndi
from skimage import measure

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "refs", "lucas")
OUT = os.path.join(HERE, "out")
STEP = 4          # 복셀 한 칸 = 그림 4픽셀
P_BODY = 2.4      # 단면 둥글기(2=타원, 클수록 네모)
P_ARM = 2.2
K = 0.001         # 그림 1픽셀 = 1mm (키 약 1.8)

def load(name):
    # 윤곽의 1픽셀 들쭉날쭉을 살짝 뭉개 단면 물결을 줄인다
    m = cv2.imread(os.path.join(OUT, f"mask_{name}.png"), 0).astype(np.float32) / 255
    return cv2.GaussianBlur(m, (0, 0), 3) > 0.5

F, S, B = load("front"), load("side"), load("back")
H, W = F.shape

def runs(row):
    d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
    return list(zip(np.nonzero(d == 1)[0], np.nonzero(d == -1)[0] - 1))

ysF, xsF = np.nonzero(F)
ysS, xsS = np.nonzero(S)
zb = ysF.max()                    # 발바닥(앞 그림 기준)
sdz = ysS.max() - zb              # 옆 그림 세로 어긋남
cx = (xsF.min() + xsF.max()) / 2

# 팔 띠: 전체 폭이 엉덩이 폭보다 크게 넓어지는 줄
width = np.array([(r.max() - r.min()) if r.size else 0 for r in (np.nonzero(F[z])[0] for z in range(H))])
hip_rows = [z for z in range(H) if width[z] > 0]
hip_w = np.median(width[int(zb - 0.42 * (zb - ysF.min())):int(zb - 0.30 * (zb - ysF.min()))])
arm = np.nonzero(width > hip_w * 1.45)[0]
az0, az1 = arm.min(), arm.max()
below = [z for z in range(az1 + 4, az1 + 40)]
tx0 = min(np.nonzero(F[z])[0].min() for z in below)
tx1 = max(np.nonzero(F[z])[0].max() for z in below)
# 몸통 앞뒤 중심(옆 그림): 배 높이 줄의 가운데
belly = int(az1 + 0.25 * (zb - az1))
srow = np.nonzero(S[belly + sdz])[0]
uc = (srow.min() + srow.max()) / 2
# 팔 앞뒤 중심: 옆 그림에서 팔 띠 높이 줄의 앞쪽 경계~몸통 가운데 사이
uarm = uc - 25
print(dict(zb=int(zb), sdz=int(sdz), cx=cx, arm=(int(az0), int(az1)), torso=(int(tx0), int(tx1)), uc=uc, belly=belly))

# 인물별 설정(귀 위치 등)
CFG = json.load(open(os.path.join(REF, "shape.json"), encoding="utf-8"))

def edge(z):
    r = np.nonzero(F[z])[0]; return (r.min(), r.max()) if r.size else (None, None)

# 귀: 귀가 튀어나온 줄에서는 위·아래 끝을 잇는 곧은 선을 얼굴 가장자리로 보고, 바깥은 납작한 귀로 따로 만든다
EAR = {}
if CFG.get("ears"):
    ze0, ze1 = CFG["ears"]
    (l0, r0), (l1, r1) = edge(ze0), edge(ze1)
    for z in range(ze0, ze1 + 1):
        t = (z - ze0) / (ze1 - ze0)
        x0, x1 = edge(z)
        EAR[z] = (x0, max(x0, l0 + (l1 - l0) * t), min(x1, r0 + (r1 - r0) * t), x1)
U_EAR, HU_EAR = CFG.get("u_ear", uc), CFG.get("hu_ear", 50)

# 턱·목: 옆 그림 앞쪽 경계가 가장 안쪽으로 들어간 줄 = 목, 그 위에서 앞 폭이 가장 좁은 줄 = 턱 시작
side_front = {z: (np.nonzero(S[z + sdz])[0].min() if S[z + sdz].any() else 10 ** 6) for z in range(az0 - 140, az0 - 4)}
neck = max(side_front, key=lambda z: side_front[z]); u_neck = side_front[neck]
chin0 = min(range(neck - 100, neck), key=lambda z: width[z])
cap = int(0.75 * (neck - chin0))
print(dict(neck=neck, u_neck=int(u_neck), chin0=chin0, cap=cap))

# 복셀 격자 (그림 좌표 단위)
xs = np.arange(xsF.min() - 8, xsF.max() + 9, STEP)
zs = np.arange(ysF.min() - 8, zb + 9, STEP)
us = np.arange(xsS.min() - 8, xsS.max() + 9, STEP)
vol = np.zeros((len(xs), len(us), len(zs)), np.float32)
U = us[None, :]
CHIN = None

for iz, z in enumerate(zs):
    if z < 0 or z >= H: continue
    frow = F[z].copy()
    zs_side = int(np.clip(z + sdz, 0, H - 1))
    srun = runs(S[zs_side])
    if not srun: continue
    in_arm_band = az0 - 6 <= z <= az1 + 2
    if in_arm_band:
        frow[:tx0] = False; frow[tx1 + 1:] = False
    rr = runs(frow)
    if z in EAR and len(rr) == 1:
        x0, xl, xr, x1 = EAR[z]
        for (e0, e1) in [(x0, xl + 30), (xr - 30, x1)]:
            if e1 - e0 < 40: continue
            sel = (xs >= e0) & (xs <= e1)
            ex = np.abs((xs[sel] - (e0 + e1) / 2) / ((e1 - e0) / 2))[:, None]
            ev = np.abs((U - U_EAR) / HU_EAR)
            vol[sel, :, iz] = np.maximum(vol[sel, :, iz], (ex ** 2 + ev ** 2) <= 1)
        rr = [(int(xl), int(xr))]
    if chin0 < z <= neck + 20:
        # 후드 깃 줄: 몸통 단면은 목 앞부터(턱이 후드에 뭉치지 않게)
        srun = [(max(u0, u_neck), u1) for (u0, u1) in srun if u1 > u_neck + 8]
    if z <= chin0 and rr:
        (cx0, cx1) = rr[0]; cu = runs(S[zs_side])[0]; CHIN = (cx0, cx1, cu[0], cu[1])  # 턱 시작 직전 줄의 단면
    for (x0, x1) in rr:
        sel = (xs >= x0) & (xs <= x1)
        if not sel.any(): continue
        hx = max((x1 - x0) / 2, 1); xc = (x0 + x1) / 2
        u_ = np.abs((xs[sel] - xc) / hx)[:, None]
        for (u0, u1) in srun:
            hu = max((u1 - u0) / 2, 1); ucc = (u0 + u1) / 2
            v_ = np.abs((U - ucc) / hu)
            inside = (u_ ** P_BODY + v_ ** P_BODY) <= 1
            vol[sel, :, iz] = np.maximum(vol[sel, :, iz], inside)
    if chin0 < z <= chin0 + cap:
        # 턱 밑: 턱 시작 줄의 단면을 둥글게 오므려 마감
        cx0, cx1, cu0, cu1 = CHIN
        f = np.sqrt(max(1 - ((z - chin0) / cap) ** 2, 0))
        hx = (cx1 - cx0) / 2 * f; hu = (cu1 - cu0) / 2 * f
        if hx > 2 and hu > 2:
            sel = np.abs(xs - (cx0 + cx1) / 2) <= hx
            u_ = np.abs((xs[sel] - (cx0 + cx1) / 2) / hx)[:, None]
            v_ = np.abs((U - (cu0 + cu1) / 2) / hu)
            vol[sel, :, iz] = np.maximum(vol[sel, :, iz], (u_ ** P_BODY + v_ ** P_BODY) <= 1)

# 팔: 앞 그림의 세로 두께를 원형 단면으로
for ix, x in enumerate(xs):
    if tx0 <= x <= tx1: continue
    col = F[:, x].copy()
    col[:az0 - 6] = False; col[az1 + 3:] = False
    for (z0, z1) in runs(col):
        hz = max((z1 - z0) / 2, 1); zc = (z0 + z1) / 2
        hu = hz * 1.0
        Zg = zs[None, :]
        inside = (np.abs((U.T - uarm) / hu) ** P_ARM + np.abs((Zg - zc) / hz) ** P_ARM) <= 1
        vol[ix] = np.maximum(vol[ix], inside)

vol = ndi.gaussian_filter(vol, 1.6)
verts, faces, normals, _ = measure.marching_cubes(vol, 0.5)
# 복셀 → 그림 좌표
gx = xs[0] + verts[:, 0] * STEP
gu = us[0] + verts[:, 1] * STEP
gz = zs[0] + verts[:, 2] * STEP
# 그림 좌표 → 블렌더 좌표 (정면이 -Y, 위가 +Z, 루카스 오른손이 -X)
P = np.stack([(gx - cx) * K, (gu - uc) * K, (zb - gz) * K], 1).astype(np.float32)
faces = faces[:, ::-1].copy()  # 축 뒤집힘 보정(바깥쪽이 앞면)

# 표면 다듬기(타우빈 평활: 부피는 거의 그대로, 층층이 결만 지움)
from scipy import sparse
n = len(P)
e = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
A = sparse.coo_matrix((np.ones(len(e) * 2), (np.r_[e[:, 0], e[:, 1]], np.r_[e[:, 1], e[:, 0]])), shape=(n, n)).tocsr()
A.data[:] = 1
deg = np.asarray(A.sum(1)).ravel()[:, None]
for _ in range(30):
    for f in (0.5, -0.53):
        P = P + f * (A @ P / deg - P)
P = P.astype(np.float32)

# 꼭짓점 법선(블렌더 좌표)
def vnormals(P, faces):
    fn = np.cross(P[faces[:, 1]] - P[faces[:, 0]], P[faces[:, 2]] - P[faces[:, 0]])
    vn = np.zeros_like(P)
    for k in range(3): np.add.at(vn, faces[:, k], fn)
    return vn / (np.linalg.norm(vn, axis=1, keepdims=True) + 1e-12)
N = vnormals(P, faces)
if (N * (P - P.mean(0))).sum(1).mean() < 0:
    faces = faces[:, ::-1].copy(); N = -N

# 보이는지 판정: 각 방향에서 본 깊이 지도
occ = vol > 0.5
def depth_map(axis, take_min):
    idx = np.arange(occ.shape[axis]).reshape([-1 if a == axis else 1 for a in range(3)])
    big = np.where(occ, idx, 10 ** 6 if take_min else -1)
    return big.min(axis) if take_min else big.max(axis)
vi = np.stack([(gx - xs[0]) / STEP, (gu - us[0]) / STEP, (gz - zs[0]) / STEP], 1)
ri = np.clip(np.round(vi).astype(int), 0, np.array(occ.shape) - 1)
tol = 2.5
front_d = depth_map(1, True);  vis_F = vi[:, 1] <= front_d[ri[:, 0], ri[:, 2]] + tol
back_d = depth_map(1, False);  vis_B = vi[:, 1] >= back_d[ri[:, 0], ri[:, 2]] - tol
left_d = depth_map(0, False);  vis_L = vi[:, 0] >= left_d[ri[:, 1], ri[:, 2]] - tol   # +X 쪽(왼쪽 옆, 옆 그림 시점)
right_d = depth_map(0, True);  vis_R = vi[:, 0] <= right_d[ri[:, 1], ri[:, 2]] + tol  # -X 쪽(옆 그림을 그대로 재사용)

# 방향은 수평 성분만 본다(앞머리 밑처럼 아래를 향한 면도 앞 그림을 쓰게).
# 얼굴이 있는 앞 그림을 가장 믿고, 옆 그림은 정말 옆을 향한 곳에만.
PW = 5.0
Nh = N[:, :2] / (np.linalg.norm(N[:, :2], axis=1, keepdims=True) + 1e-6)
BOOST = np.array([6.0, 2.0, 1.0, 1.0])
wF = BOOST[0] * np.clip(-Nh[:, 1], 0, 1) ** PW * vis_F
wB = BOOST[1] * np.clip(Nh[:, 1], 0, 1) ** PW * vis_B
wL = BOOST[2] * np.clip(Nh[:, 0], 0, 1) ** PW * vis_L
wR = BOOST[3] * np.clip(-Nh[:, 0], 0, 1) ** PW * vis_R
Wt = np.stack([wF, wB, wL, wR], 1)
s = Wt.sum(1)
# 어느 쪽에서도 안 보이는 곳(겨드랑이 등): 방향만으로 나눔
fall = BOOST * np.stack([np.clip(-Nh[:, 1], 0, 1), np.clip(Nh[:, 1], 0, 1), np.clip(Nh[:, 0], 0, 1), np.clip(-Nh[:, 0], 0, 1)], 1) ** PW
Wt = np.where((s < 1e-4)[:, None], fall, Wt)
Wt = Wt / (Wt.sum(1, keepdims=True) + 1e-9)

np.savez_compressed(os.path.join(OUT, "lucas_shape.npz"), verts=P, faces=faces.astype(np.int32), w=Wt.astype(np.float32))

# 입힐 그림: 가장자리 섞인 픽셀을 조금 깎고, 바깥은 가장 가까운 캐릭터 색으로 번지게
def bleed(name, mask):
    img = cv2.imread(os.path.join(REF, name + ".png"))
    m = cv2.erode(mask.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    _, (iy, ix) = ndi.distance_transform_edt(~m, return_indices=True)
    out = img[iy, ix]
    if name == "side":
        hz0, hz1 = int(ysS.min() + 0.25 * (az0 - ysS.min())), int(az0)
        u_front = int(np.nonzero(S[(hz0 + hz1) // 2])[0].min())
        reg = np.zeros(mask.shape, np.uint8)
        sub = out[hz0:hz1, u_front:u_front + 90].astype(int).sum(2) < 260
        reg[hz0:hz1, u_front:u_front + 90] = sub
        reg = cv2.dilate(reg, np.ones((15, 15), np.uint8))
        out = cv2.inpaint(out, reg, 9, cv2.INPAINT_TELEA)
        print("side eye px", int(reg.sum()))
    cv2.imwrite(os.path.join(OUT, f"tex_{name}.png"), out)
for n, m in [("front", F), ("side", S), ("back", B)]:
    bleed(n, m)

meta = dict(cx=float(cx), uc=float(uc), zb=int(zb), sdz=int(sdz), K=K, size=[W, H],
            back_shift=float(cx - (W - 1 - (np.nonzero(B)[1].min() + np.nonzero(B)[1].max()) / 2)),
            nverts=int(len(P)), nfaces=int(len(faces)))
json.dump(meta, open(os.path.join(OUT, "lucas_shape.json"), "w"), indent=1)
print(meta)
