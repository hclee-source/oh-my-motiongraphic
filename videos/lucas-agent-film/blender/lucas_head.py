# 루카스 머리 점토 질감 시험(블렌더). 사용: blender -b -P lucas_head.py -- <출력 png>
# 앞 = -Y, 위 = +Z. 머리카락은 서로 녹아 붙는 메타볼 덩어리로 만든다.
import bpy, math, sys

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "lucas_head.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x = sc.render.resolution_y = 1080
sc.render.filepath = OUT
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.render.film_transparent = False

def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (1,)

def mat(name, hexcol, rough=0.5, sss=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = srgb(hexcol)
    b.inputs["Roughness"].default_value = rough
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.4, 0.2, 0.15)
        b.inputs["Subsurface Scale"].default_value = 0.05
    if coat:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.35
    return m

SKIN = mat("skin", "#F9DCC4", 0.55, sss=0.25)
HAIR = mat("hair", "#A35F37", 0.6, sss=0.05, coat=0.05)
EYE = mat("eye", "#1A1A1E", 0.2, coat=0.6)

def smooth(o):
    for p in o.data.polygons: p.use_smooth = True

def blob(name, loc, scale, m, seg=64):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; smooth(o)
    o.data.materials.append(m)
    return o

# 얼굴(살짝 넓적한 떡 모양)과 귀
blob("face", (0, 0, -0.06), (1.0, 0.95, 1.0), SKIN)
for s in (-1, 1):
    blob("ear", (s * 1.0, 0.0, -0.32), (0.22, 0.15, 0.25), SKIN, 32)
# 눈: 세로로 긴 검은 콩
for s in (-1, 1):
    e = blob("eye", (s * 0.28, -0.875, -0.3), (0.08, 0.035, 0.155), EYE, 32)
    e.rotation_euler[2] = s * 0.28   # 얼굴 곡면을 따라 정면을 보게

# 머리카락: 덮개(앞아래를 파낸 큰 구) + 앞머리·옆머리 덩어리를 합친 뒤, 하나로 녹여 붙이고(복셀 다시 짜기) 매끈하게 다듬는다
def ell(name, loc, scale, seg=48, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return o
dome = ell("dome", (0, 0.1, 0.24), (1.18, 1.06, 0.95))
cut = ell("cut", (0, -0.95, -0.66), (1.08, 1.0, 0.76))
bm = dome.modifiers.new("cut", "BOOLEAN"); bm.operation = "DIFFERENCE"; bm.object = cut; bm.solver = "EXACT"
bpy.context.view_layer.objects.active = dome; bpy.ops.object.modifier_apply(modifier="cut")
bpy.data.objects.remove(cut)
pieces = [dome]
# 앞머리 4뭉치(가운데가 조금 길게), 옆머리 2뭉치
# 앞머리는 얼굴 앞에 얇게 얹힌 껍데기처럼(앞으로 내밀고 얇게), 가운데 두 뭉치가 조금 짧게
# 길이·기울기가 제각각인 납작한 앞머리 다섯 뭉치(끝이 살짝 뾰족하게 모이도록 세로로 길게)
for i, (x, y, z, sx, sz, tilt) in enumerate([(-0.8, -0.62, 0.18, 0.24, 0.42, 18), (-0.44, -0.82, 0.29, 0.26, 0.4, 8),
                                              (-0.06, -0.88, 0.33, 0.27, 0.37, -4), (0.34, -0.84, 0.29, 0.26, 0.41, -10), (0.76, -0.64, 0.18, 0.24, 0.43, -18)]):
    pieces.append(ell(f"bang{i}", (x, y, z), (sx, 0.12, sz), rot=(0, math.radians(tilt), 0)))
for s_ in (-1, 1):
    pieces.append(ell("side", (s_ * 1.04, -0.18, 0.02), (0.2, 0.34, 0.36), rot=(0, math.radians(-s_ * 12), 0)))
bpy.ops.object.select_all(action="DESELECT")
for o in pieces: o.select_set(True)
bpy.context.view_layer.objects.active = dome
bpy.ops.object.join()
hair = bpy.context.object; hair.name = "hair"
rm = hair.modifiers.new("remesh", "REMESH"); rm.mode = "VOXEL"; rm.voxel_size = 0.022
smm = hair.modifiers.new("smooth", "SMOOTH"); smm.factor = 0.9; smm.iterations = 12
bpy.ops.object.modifier_apply(modifier="remesh"); bpy.ops.object.modifier_apply(modifier="smooth")
smooth(hair)
hair.data.materials.clear(); hair.data.materials.append(HAIR)
for poly in hair.data.polygons: poly.material_index = 0
print("HAIR_MATS", [m.name for m in hair.data.materials], len(hair.data.polygons))

# 정수리 한 가닥(휘어진 관)
cu = bpy.data.curves.new("ahoge", "CURVE"); cu.dimensions = "3D"
cu.bevel_depth = 0.075; cu.bevel_resolution = 6; cu.use_fill_caps = True
sp = cu.splines.new("BEZIER"); sp.bezier_points.add(3)
pts = [(0.0, 0.14, 0.98), (-0.03, 0.12, 1.28), (0.2, 0.1, 1.42), (0.38, 0.08, 1.33)]
for bp, p in zip(sp.bezier_points, pts):
    bp.co = p; bp.handle_left_type = bp.handle_right_type = "AUTO"
ah = bpy.data.objects.new("ahoge", cu); sc.collection.objects.link(ah); ah.data.materials.append(HAIR)

# 조명: 큰 면 조명(주광) + 보조광 + 뒤쪽 테두리광 + 은은한 환경광
def area(loc, energy, size, rot):
    bpy.ops.object.light_add(type="AREA", location=loc)
    l = bpy.context.object; l.data.energy = energy; l.data.size = size; l.rotation_euler = rot
    return l
area((-2.6, -3.6, 3.0), 380, 4.0, (math.radians(50), 0, math.radians(-35)))
area((3.2, -2.6, 0.8), 120, 3.0, (math.radians(75), 0, math.radians(50)))
area((0.0, 3.2, 3.2), 260, 2.5, (math.radians(-45), 0, math.radians(180)))
area((0.0, -3.0, -2.2), 90, 4.0, (math.radians(125), 0, 0))   # 턱 밑을 살짝 밝히는 아래 반사광
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs["Color"].default_value = srgb("#13224F"); bg.inputs["Strength"].default_value = 0.6

# 카메라: 정면 살짝 위
bpy.ops.object.camera_add(location=(0, -7.2, 0.55))
cam = bpy.context.object; cam.data.lens = 85
cam.rotation_euler = (math.radians(86), 0, 0)
sc.camera = cam
bpy.ops.render.render(write_still=True)
print("RENDER_OK", OUT)
