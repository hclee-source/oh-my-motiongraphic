# 루카스 6명(주인공 + 에이전트 5명) 단체 사진. 사용: blender -b -P lucas_group.py -- <출력 png>
# 머리는 lucas_head.py와 같은 방식으로 한 번 만들고 복사해 쓴다. 앞 = -Y, 위 = +Z, 발바닥 z = 0.
import bpy, math, sys
from mathutils import Vector

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "lucas_group.png"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.render.filepath = OUT
sc.view_settings.view_transform = "Standard"

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (1,)
MATS = {}
def mat(hexcol, rough=0.6, sss=0.0, coat=0.0):
    key = (hexcol, rough, sss, coat)
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(hexcol); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = srgb(hexcol); b.inputs["Roughness"].default_value = rough
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.4, 0.2, 0.15); b.inputs["Subsurface Scale"].default_value = 0.05
    if coat:
        b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.35
    MATS[key] = m
    return m
SKIN = mat("#F9DCC4", 0.55, sss=0.25)
HAIR = mat("#A35F37", 0.6, sss=0.05, coat=0.05)
EYE = mat("#1A1A1E", 0.2, coat=0.6)

def smooth(o):
    for p in o.data.polygons: p.use_smooth = True
def sphere(name, loc, scale, m, rot=(0, 0, 0), seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; o.rotation_euler = rot; smooth(o)
    if m: o.data.materials.append(m)
    return o
def pillow(name, loc, scale, m, bevel=0.3):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bv = o.modifiers.new("bevel", "BEVEL"); bv.width = bevel; bv.segments = 8
    o.modifiers.new("sub", "SUBSURF").levels = 2
    smooth(o); o.data.materials.append(m)
    return o
def cyl(name, loc, r, depth, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=48)
    o = bpy.context.object; o.name = name; smooth(o); o.data.materials.append(m)
    bv = o.modifiers.new("bevel", "BEVEL"); bv.width = min(r, depth) * 0.3; bv.segments = 4
    return o

# ───── 머리(원점 = 머리 가운데) ─────
def build_head():
    parts = []
    parts.append(sphere("face", (0, 0, -0.06), (1.0, 0.95, 1.0), SKIN, seg=64))
    for s in (-1, 1):
        parts.append(sphere("ear", (s * 1.0, 0.0, -0.32), (0.22, 0.15, 0.25), SKIN, seg=32))
        e = sphere("eye", (s * 0.28, -0.875, -0.3), (0.08, 0.035, 0.155), EYE, rot=(0, 0, s * 0.28), seg=32)
        parts.append(e)
    def ell(name, loc, scale, rot=(0, 0, 0)):
        o = sphere(name, loc, scale, None, rot=rot)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        return o
    dome = ell("dome", (0, 0.1, 0.24), (1.18, 1.06, 0.95))
    cut = ell("cut", (0, -0.95, -0.66), (1.08, 1.0, 0.76))
    bm = dome.modifiers.new("cut", "BOOLEAN"); bm.operation = "DIFFERENCE"; bm.object = cut; bm.solver = "EXACT"
    bpy.context.view_layer.objects.active = dome; bpy.ops.object.modifier_apply(modifier="cut"); bpy.data.objects.remove(cut)
    pieces = [dome]
    for i, (x, y, z, sx, sz, tilt) in enumerate([(-0.8, -0.62, 0.18, 0.24, 0.42, 18), (-0.44, -0.82, 0.29, 0.26, 0.4, 8),
                                                  (-0.06, -0.88, 0.33, 0.27, 0.37, -4), (0.34, -0.84, 0.29, 0.26, 0.41, -10), (0.76, -0.64, 0.18, 0.24, 0.43, -18)]):
        pieces.append(ell(f"bang{i}", (x, y, z), (sx, 0.12, sz), rot=(0, math.radians(tilt), 0)))
    for s in (-1, 1):
        pieces.append(ell("side", (s * 1.04, -0.18, 0.02), (0.2, 0.34, 0.36), rot=(0, math.radians(-s * 12), 0)))
    bpy.ops.object.select_all(action="DESELECT")
    for o in pieces: o.select_set(True)
    bpy.context.view_layer.objects.active = dome; bpy.ops.object.join()
    hair = bpy.context.object; hair.name = "hair"
    rm = hair.modifiers.new("remesh", "REMESH"); rm.mode = "VOXEL"; rm.voxel_size = 0.022
    sm = hair.modifiers.new("smooth", "SMOOTH"); sm.factor = 0.9; sm.iterations = 12
    bpy.ops.object.modifier_apply(modifier="remesh"); bpy.ops.object.modifier_apply(modifier="smooth")
    smooth(hair); hair.data.materials.clear(); hair.data.materials.append(HAIR)
    parts.append(hair)
    cu = bpy.data.curves.new("ahoge", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.075; cu.bevel_resolution = 6; cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER"); sp.bezier_points.add(3)
    for bp, p in zip(sp.bezier_points, [(0.0, 0.14, 0.98), (-0.03, 0.12, 1.28), (0.2, 0.1, 1.42), (0.38, 0.08, 1.33)]):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
    ah = bpy.data.objects.new("ahoge", cu); sc.collection.objects.link(ah); ah.data.materials.append(HAIR)
    parts.append(ah)
    return parts

HEAD = build_head()
HEAD_Z = 2.78   # 머리 가운데 높이(턱과 옷깃 사이에 목이 살짝 보이게)

def place_head(root):
    out = []
    for o in HEAD:
        c = o.copy(); sc.collection.objects.link(c); c.parent = root; c.location = o.location + Vector((0, 0, HEAD_Z)); c.hide_render = False
        out.append(c)
    return out

# ───── 몸(짧고 통통) ─────
def body(root, top, pants, shoes="#F4F4F2", short_sleeve=False):
    P = lambda o: (setattr(o, "parent", root), o)[1]
    torso = P(pillow("torso", (0, 0, 1.18), (0.6, 0.44, 0.5), mat(top, 0.7)))
    P(cyl("neck", (0, 0.02, 1.86), 0.21, 0.5, SKIN))
    for s in (-1, 1):
        if short_sleeve:
            P(sphere("sleeve", (s * 0.6, 0, 1.46), (0.22, 0.22, 0.2), mat(top, 0.7)))
            P(sphere("arm", (s * 0.7, 0, 1.12), (0.15, 0.15, 0.36), SKIN, rot=(0, math.radians(s * 10), 0)))
        else:
            P(sphere("arm", (s * 0.7, 0, 1.18), (0.18, 0.18, 0.42), mat(top, 0.7), rot=(0, math.radians(s * 10), 0)))
        P(sphere("hand", (s * 0.78, -0.02, 0.74), (0.16, 0.16, 0.16), SKIN))
        P(sphere("leg", (s * 0.27, 0, 0.48), (0.21, 0.21, 0.32), mat(pants, 0.7)))
        P(sphere("shoe", (s * 0.28, -0.08, 0.13), (0.25, 0.33, 0.15), mat(shoes, 0.5)))
    return torso

def make(kind, x, y=0.0, turn=0.0):
    root = bpy.data.objects.new(f"lucas_{kind}", None); sc.collection.objects.link(root)
    root.location = (x, y, 0); root.rotation_euler = (0, 0, math.radians(turn))
    head = place_head(root)
    hide_ahoge = False
    P = lambda o: (setattr(o, "parent", root), o)[1]
    if kind == "main":            # 주인공: 남색 후드 + 커피
        body(root, "#2F3F92", "#4B4F5E")
        P(pillow("hood", (0, 0.12, 1.72), (0.48, 0.34, 0.14), mat("#3B50A6", 0.7), bevel=0.12))
        P(cyl("cup", (0.86, -0.18, 0.86), 0.14, 0.3, mat("#FFFFFF", 0.4)))
        P(cyl("coffee", (0.86, -0.18, 1.01), 0.12, 0.02, mat("#6B3E22", 0.3)))
    elif kind == "plan":          # ① 기획: GOOGLE 회색 반팔 티
        body(root, "#9EA3AD", "#3E4A68", short_sleeve=True)
        cu = bpy.data.curves.new("google", "FONT"); cu.body = "GOOGLE"; cu.size = 0.2; cu.extrude = 0.012; cu.align_x = "CENTER"
        t = bpy.data.objects.new("google", cu); sc.collection.objects.link(t); t.parent = root
        t.location = (0, -0.47, 1.2); t.rotation_euler = (math.radians(90), 0, 0); t.data.materials.append(mat("#2B2B33", 0.6))
    elif kind == "edit":          # ② 편집: 빨간 야구 모자
        body(root, "#8EC5E8", "#4B4F5E")
        P(sphere("cap", (0, 0.05, HEAD_Z + 0.38), (1.2, 1.14, 0.78), mat("#D64545", 0.55)))
        P(cyl("brim", (0, -1.12, HEAD_Z + 0.34), 0.68, 0.09, mat("#C23B3B", 0.55), rot=(math.radians(30), 0, 0)))
        P(sphere("button", (0, 0.05, HEAD_Z + 1.16), (0.09, 0.09, 0.06), mat("#D64545", 0.55)))
        hide_ahoge = True
    elif kind == "design":        # ③ 디자인: 베레모 + 태블릿
        body(root, "#E9B44C", "#4B4F5E")
        P(sphere("beret", (0.15, 0.05, HEAD_Z + 1.02), (1.0, 0.95, 0.3), mat("#8E2F3E", 0.65), rot=(0, math.radians(14), 0)))
        P(pillow("tablet", (-0.82, -0.32, 0.92), (0.26, 0.03, 0.34), mat("#2C2F38", 0.3), bevel=0.04))
        hide_ahoge = True
    elif kind == "mkt":           # ④ 마케팅: 헤드셋
        body(root, "#5CBF8F", "#4B4F5E")
        # 머리띠: 한쪽 귀에서 정수리를 넘어 다른 쪽 귀까지(반원)
        bc = bpy.data.curves.new("band", "CURVE"); bc.dimensions = "3D"; bc.bevel_depth = 0.075; bc.bevel_resolution = 6; bc.use_fill_caps = True
        bsp = bc.splines.new("BEZIER"); bsp.bezier_points.add(4)
        for bp, q in zip(bsp.bezier_points, [(-1.16, 0.02, HEAD_Z - 0.3), (-1.3, 0.04, HEAD_Z + 0.55), (0.0, 0.06, HEAD_Z + 1.3), (1.3, 0.04, HEAD_Z + 0.55), (1.16, 0.02, HEAD_Z - 0.3)]):
            bp.co = q; bp.handle_left_type = bp.handle_right_type = "AUTO"
        band = bpy.data.objects.new("band", bc); sc.collection.objects.link(band); band.data.materials.append(mat("#2B2B33", 0.4)); band.parent = root
        for s in (-1, 1):
            P(cyl("cupset", (s * 1.12, 0.0, HEAD_Z - 0.32), 0.26, 0.16, mat("#2B2B33", 0.4), rot=(0, math.radians(90), 0)))
        P(cyl("mic", (-0.72, -0.62, HEAD_Z - 0.62), 0.035, 0.7, mat("#2B2B33", 0.4), rot=(0, math.radians(70), math.radians(-40))))
        P(sphere("micball", (-0.42, -0.86, HEAD_Z - 0.72), (0.08, 0.08, 0.08), mat("#2B2B33", 0.4)))
    elif kind == "sched":         # ⑤ 일정: 흰 셔츠 + 넥타이 + 클립보드
        body(root, "#F2F2F0", "#273A5C")
        P(pillow("tie", (0, -0.47, 1.18), (0.07, 0.02, 0.32), mat("#273A8C", 0.5), bevel=0.02))
        P(pillow("knot", (0, -0.47, 1.52), (0.09, 0.03, 0.07), mat("#273A8C", 0.5), bevel=0.02))
        P(pillow("clip", (-0.84, -0.3, 0.95), (0.3, 0.03, 0.38), mat("#B9834F", 0.6), bevel=0.04))
        P(pillow("paper", (-0.84, -0.335, 0.92), (0.24, 0.01, 0.3), mat("#FFFFFF", 0.6), bevel=0.01))
    for o in head:
        if o.name.startswith("ahoge") and hide_ahoge: o.hide_render = True
    return root

for o in HEAD: o.hide_render = True   # 원본 머리는 숨기고 복사본만 쓴다

lineup = [("plan", -6.6), ("edit", -3.95), ("main", -1.3 + 0.0), ("design", 1.35), ("mkt", 4.0), ("sched", 6.65)]
for kind, x in lineup:
    make(kind, x, y=(-0.6 if kind == "main" else 0.0), turn=(-x * 1.6))

# 바닥과 배경
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0)); fl = bpy.context.object; fl.data.materials.append(mat("#E8ECF4", 0.8))
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 12, 10), rotation=(math.radians(90), 0, 0)); wl = bpy.context.object; wl.data.materials.append(mat("#DDE3EF", 0.9))
def area(loc, energy, size, rot):
    bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object
    l.data.energy = energy; l.data.size = size; l.rotation_euler = rot
area((-8, -12, 12), 3200, 12, (math.radians(50), 0, math.radians(-30)))
area((10, -9, 5), 1100, 10, (math.radians(70), 0, math.radians(45)))
area((0, 8, 9), 1500, 10, (math.radians(-40), 0, math.radians(180)))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = srgb("#DDE3EF"); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.5

bpy.ops.object.camera_add(location=(0, -25, 3.7)); cam = bpy.context.object; cam.data.lens = 52
cam.rotation_euler = (math.radians(87.5), 0, 0); sc.camera = cam
bpy.ops.render.render(write_still=True)
print("RENDER_OK", OUT)
