# 점토 캐릭터 공용 부품(블렌더). 장면 스크립트에서 sys.path에 이 폴더를 넣고 import 한다.
# 앞 = -Y, 위 = +Z, 발바닥 z = 0. 루카스 머리 가운데 높이 HEAD_Z.
import bpy, math
from mathutils import Vector

HEAD_Z = 2.78

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (1,)

_M = {}
def mat(hexcol, rough=0.6, sss=0.0, coat=0.0, sheen=0.0, bump=0.0):
    """점토·옷감 재질. sheen = 옷감의 부드러운 결, bump = 아주 미세한 표면 요철."""
    key = (hexcol, rough, sss, coat, sheen, bump)
    if key in _M: return _M[key]
    m = bpy.data.materials.new(hexcol); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = srgb(hexcol); b.inputs["Roughness"].default_value = rough
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.5, 0.25, 0.18); b.inputs["Subsurface Scale"].default_value = 0.06
    if coat:
        b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.3
    if sheen:
        b.inputs["Sheen Weight"].default_value = sheen; b.inputs["Sheen Roughness"].default_value = 0.5
    if bump:
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 180; nz.inputs["Detail"].default_value = 4
        bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = bump; bp.inputs["Distance"].default_value = 0.02
        nt.links.new(nz.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    _M[key] = m
    return m

def smooth(o):
    for p in o.data.polygons: p.use_smooth = True

def sphere(name, loc, scale, m=None, rot=(0, 0, 0), seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; o.rotation_euler = rot; smooth(o)
    if m: o.data.materials.append(m)
    return o

def torus(name, loc, R, r, scale=(1, 1, 1), rot=(0, 0, 0), m=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot, major_segments=64, minor_segments=24)
    o = bpy.context.object; o.name = name; o.scale = scale; smooth(o)
    if m: o.data.materials.append(m)
    return o

def box(name, loc, scale, m=None, bevel=0.3, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot); o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bv = o.modifiers.new("bevel", "BEVEL"); bv.width = bevel; bv.segments = 8
    o.modifiers.new("sub", "SUBSURF").levels = 2
    smooth(o)
    if m: o.data.materials.append(m)
    return o

def cyl(name, loc, r, depth, m=None, rot=(0, 0, 0), bevel=True):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=64)
    o = bpy.context.object; o.name = name; smooth(o)
    if bevel:
        bv = o.modifiers.new("bevel", "BEVEL"); bv.width = min(r, depth) * 0.3; bv.segments = 4
    if m: o.data.materials.append(m)
    return o

def capsule(name, p0, p1, r):
    """두 점을 잇는 관(양 끝 둥근). 녹여 붙이기용 덩어리 목록을 돌려준다."""
    a, b = Vector(p0), Vector(p1); d = b - a; mid = (a + b) / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=mid, vertices=48)
    c = bpy.context.object; c.name = name
    c.rotation_mode = "QUATERNION"; c.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return [c, sphere(name + "_a", tuple(a), (r, r, r), None, seg=32), sphere(name + "_b", tuple(b), (r, r, r), None, seg=32)]

def fuse(name, objs, m, voxel=0.02, iters=8, factor=0.8):
    """여러 덩어리를 하나로 녹여 붙인다(이음새 없는 점토 덩어리)."""
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True); bpy.context.view_layer.objects.active = o
        for md in list(o.modifiers): bpy.ops.object.modifier_apply(modifier=md.name)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.context.view_layer.objects.active = objs[0]
    for o in objs: o.select_set(True)
    bpy.ops.object.join()
    f = bpy.context.object; f.name = name
    rm = f.modifiers.new("remesh", "REMESH"); rm.mode = "VOXEL"; rm.voxel_size = voxel
    sm = f.modifiers.new("smooth", "SMOOTH"); sm.factor = factor; sm.iterations = iters
    bpy.ops.object.modifier_apply(modifier="remesh"); bpy.ops.object.modifier_apply(modifier="smooth")
    smooth(f); f.data.materials.clear(); f.data.materials.append(m)
    for p in f.data.polygons: p.material_index = 0
    return f

SKIN = None; HAIR = None; EYE = None; WHITE = None
def init_mats():
    global SKIN, HAIR, EYE, WHITE
    SKIN = mat("#F9DCC4", 0.5, sss=0.35, bump=0.02)
    HAIR = mat("#A35F37", 0.55, sss=0.06, coat=0.06, bump=0.03)
    EYE = mat("#151518", 0.15, coat=0.8)
    WHITE = mat("#FFFFFF", 0.2)

def build_head(origin=(0, 0, 0), ahoge=True):
    """루카스 머리. origin = 머리 가운데."""
    ox, oy, oz = origin; parts = []
    parts.append(sphere("face", (ox, oy, oz - 0.06), (1.0, 0.95, 1.0), SKIN, seg=96))
    for s in (-1, 1):
        parts.append(sphere("ear", (ox + s * 1.0, oy, oz - 0.32), (0.22, 0.15, 0.25), SKIN, seg=48))
        parts.append(sphere("eye", (ox + s * 0.28, oy - 0.875, oz - 0.3), (0.08, 0.035, 0.155), EYE, rot=(0, 0, s * 0.28), seg=48))
        # 눈 반짝임(작은 흰 점)
        parts.append(sphere("glint", (ox + s * 0.28 - 0.025, oy - 0.905, oz - 0.24), (0.022, 0.012, 0.03), WHITE, rot=(0, 0, s * 0.28), seg=24))
    def ell(name, loc, scale, rot=(0, 0, 0)):
        o = sphere(name, (ox + loc[0], oy + loc[1], oz + loc[2]), scale, None, rot=rot, seg=48)
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
    parts.append(fuse("hair", pieces, HAIR, voxel=0.018, iters=12, factor=0.9))
    if ahoge:
        cu = bpy.data.curves.new("ahoge", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.075; cu.bevel_resolution = 8; cu.use_fill_caps = True
        sp = cu.splines.new("BEZIER"); sp.bezier_points.add(3)
        for bp, p in zip(sp.bezier_points, [(0.0, 0.14, 0.98), (-0.03, 0.12, 1.28), (0.2, 0.1, 1.42), (0.38, 0.08, 1.33)]):
            bp.co = (ox + p[0], oy + p[1], oz + p[2]); bp.handle_left_type = bp.handle_right_type = "AUTO"
        ah = bpy.data.objects.new("ahoge", cu); bpy.context.scene.collection.objects.link(ah); ah.data.materials.append(HAIR)
        parts.append(ah)
    return parts

def build_body(top="#2F3F92", top_dark="#26357E", pants="#4B4F5E", hood=True, pocket=True, strings=True):
    """이음새 없는 점토 몸: 윗옷(몸통+팔+깃+밑단+소매 끝을 녹여 붙임), 바지, 손, 목, 운동화."""
    TOP = mat(top, 0.75, sheen=0.35, bump=0.04); DARK = mat(top_dark, 0.75, sheen=0.35, bump=0.04)
    PANTS = mat(pants, 0.8, sheen=0.25, bump=0.04)
    parts = []
    tp = [box("torso", (0, 0, 1.2), (0.6, 0.44, 0.5), None, bevel=0.32)]
    SH, WR = (0.56, 0.0, 1.52), (0.8, -0.03, 0.92)   # 어깨, 손목
    for s in (-1, 1):
        tp += capsule("arm", (s * SH[0], SH[1], SH[2]), (s * WR[0], WR[1], WR[2]), 0.17)
    tp.append(torus("hemband", (0, 0, 0.78), 0.5, 0.09, scale=(1.12, 0.84, 1.0)))
    if hood:
        tp.append(torus("hood", (0, 0.08, 1.68), 0.4, 0.15, scale=(1.0, 0.85, 1.0)))
    if pocket:
        tp.append(box("pocket", (0, -0.43, 1.0), (0.34, 0.05, 0.15), None, bevel=0.05))
    parts.append(fuse("top", tp, TOP))
    # 소매 끝(팔 방향을 따라 감긴 조금 진한 띠)과 손
    tilt = math.degrees(math.atan2(WR[0] - SH[0], SH[2] - WR[2]))
    for s in (-1, 1):
        parts.append(torus("cuff", (s * (WR[0] - 0.01), WR[1], WR[2] + 0.04), 0.155, 0.045, rot=(0, math.radians(-s * tilt), 0), m=DARK))
        parts.append(sphere("hand", (s * 0.83, -0.04, 0.78), (0.15, 0.15, 0.15), SKIN))
    if strings:
        for s in (-1, 1):
            parts.append(cyl("string", (s * 0.11, -0.43, 1.47), 0.025, 0.3, WHITE, bevel=False))
            parts.append(sphere("tip", (s * 0.11, -0.43, 1.31), (0.04, 0.04, 0.05), WHITE, seg=24))
    pp = [sphere("hip", (0, 0, 0.78), (0.5, 0.36, 0.2))]
    for s in (-1, 1):
        pp.append(sphere("leg", (s * 0.26, 0, 0.5), (0.2, 0.2, 0.32)))
    parts.append(fuse("pants", pp, PANTS))
    parts.append(cyl("neck", (0, 0.02, 1.86), 0.21, 0.5, SKIN))
    SHOE = mat("#F6F6F4", 0.45, bump=0.02); SOLE = mat("#D4D7DE", 0.6)
    for s in (-1, 1):
        parts.append(sphere("shoe", (s * 0.28, -0.08, 0.16), (0.25, 0.34, 0.15), SHOE))
        parts.append(sphere("sole", (s * 0.28, -0.08, 0.06), (0.27, 0.36, 0.07), SOLE))
    return parts
