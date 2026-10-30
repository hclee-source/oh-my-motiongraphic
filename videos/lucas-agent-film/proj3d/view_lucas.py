# build_shape.py 결과(입체+가중치)를 블렌더로 불러와 앞·옆·뒤 그림을 입히고 렌더한다.
# 사용: blender -b -P view_lucas.py -- stills <출력폴더>
#       blender -b -P view_lucas.py -- turn <출력폴더> [프레임수]
import bpy, bmesh, math, sys, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
MODE = args[0] if args else "stills"
DST = os.path.abspath(args[1]) if len(args) > 1 else os.path.join(OUT, "render")
NFR = int(args[2]) if len(args) > 2 else 96
os.makedirs(DST, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
try:
    sc.eevee.use_raytracing = True
    sc.eevee.ray_tracing_options.resolution_scale = "1"
    sc.eevee.use_shadows = True
    sc.eevee.shadow_ray_count = 3
    sc.eevee.shadow_step_count = 12
    sc.eevee.taa_render_samples = 64 if MODE == "stills" else 24
    sc.eevee.fast_gi_method = "GLOBAL_ILLUMINATION"
except Exception as ex:
    print("EEVEE_OPT", ex)
sc.view_settings.view_transform = "Standard"

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple([(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c] + [1.0])

# ── 입체 불러오기
meta = json.load(open(os.path.join(OUT, "lucas_shape.json")))
d = np.load(os.path.join(OUT, "lucas_shape.npz"))
V, Fc, Wt = d["verts"], d["faces"], d["w"]
me = bpy.data.meshes.new("lucas")
me.vertices.add(len(V)); me.vertices.foreach_set("co", V.ravel())
me.loops.add(Fc.size); me.loops.foreach_set("vertex_index", Fc.ravel())
me.polygons.add(len(Fc))
me.polygons.foreach_set("loop_start", np.arange(0, Fc.size, 3))
me.polygons.foreach_set("loop_total", np.full(len(Fc), 3))
me.update(); me.validate()
me.polygons.foreach_set("use_smooth", np.ones(len(Fc), bool))
for i, nm in enumerate(["wF", "wB", "wL", "wR"]):
    a = me.attributes.new(nm, "FLOAT", "POINT"); a.data.foreach_set("value", Wt[:, i].copy())
ob = bpy.data.objects.new("lucas", me); sc.collection.objects.link(ob)

# ── 재질: 그림 세 장을 방향별 가중치로 섞어 입힌다
W, H = meta["size"]; K = meta["K"]; cx = meta["cx"]; uc = meta["uc"]; zb = meta["zb"]; sdz = meta["sdz"]; bs = meta["back_shift"]
mat = bpy.data.materials.new("lucas_proj"); mat.use_nodes = True
nt = mat.node_tree; N = nt.nodes; L = nt.links
for n in list(N): N.remove(n)
tc = N.new("ShaderNodeTexCoord"); sep = N.new("ShaderNodeSeparateXYZ"); L.new(tc.outputs["Object"], sep.inputs[0])

def lin(src, a, b):  # src*a + b
    m = N.new("ShaderNodeMath"); m.operation = "MULTIPLY_ADD"
    L.new(src, m.inputs[0]); m.inputs[1].default_value = a; m.inputs[2].default_value = b
    return m.outputs[0]

def tex(name, u, v):
    c = N.new("ShaderNodeCombineXYZ"); L.new(u, c.inputs[0]); L.new(v, c.inputs[1])
    t = N.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(os.path.join(OUT, f"tex_{name}.png"))
    t.extension = "EXTEND"; t.interpolation = "Cubic"
    L.new(c.outputs[0], t.inputs["Vector"])
    return t.outputs["Color"]

X, Y, Z = sep.outputs[0], sep.outputs[1], sep.outputs[2]
vF = lin(Z, 1 / (K * H), 1 - zb / H)
cF = tex("front", lin(X, 1 / (K * W), cx / W), vF)
cB = tex("back", lin(X, -1 / (K * W), (W - 1 - cx + bs) / W), vF)
cS = tex("side", lin(Y, 1 / (K * W), uc / W), lin(Z, 1 / (K * H), 1 - (zb + sdz) / H))

def attr(nm):
    a = N.new("ShaderNodeAttribute"); a.attribute_name = nm; return a.outputs["Fac"]
def scale(col, f):
    m = N.new("ShaderNodeVectorMath"); m.operation = "SCALE"; L.new(col, m.inputs[0]); L.new(f, m.inputs["Scale"]); return m.outputs[0]
def add(a, b):
    m = N.new("ShaderNodeVectorMath"); m.operation = "ADD"; L.new(a, m.inputs[0]); L.new(b, m.inputs[1]); return m.outputs[0]
wS = N.new("ShaderNodeMath"); wS.operation = "ADD"; L.new(attr("wL"), wS.inputs[0]); L.new(attr("wR"), wS.inputs[1])
col = add(add(scale(cF, attr("wF")), scale(cB, attr("wB"))), scale(cS, wS.outputs[0]))

bsdf = N.new("ShaderNodeBsdfPrincipled")
L.new(col, bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.62
bsdf.inputs["Specular IOR Level"].default_value = 0.25
L.new(col, bsdf.inputs["Emission Color"]); bsdf.inputs["Emission Strength"].default_value = 0.08
outn = N.new("ShaderNodeOutputMaterial"); L.new(bsdf.outputs[0], outn.inputs[0])
me.materials.append(mat)

# ── 무대·빛
def plain(hexc, rough=0.9):
    m = bpy.data.materials.new(hexc); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]; p.inputs["Base Color"].default_value = srgb(hexc); p.inputs["Roughness"].default_value = rough
    return m
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); fl = bpy.context.object; fl.data.materials.append(plain("#D9DBE1"))
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 9, 8), rotation=(math.radians(90), 0, 0)); wl = bpy.context.object; wl.data.materials.append(plain("#E3E5EA"))

def area(loc, energy, size, color=(1, 1, 1), target=(0, 0, 0.9)):
    bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object
    l.data.energy = energy; l.data.size = size; l.data.color = color
    dvec = (np.array(target) - np.array(loc)); dvec /= np.linalg.norm(dvec)
    l.rotation_euler = (0, 0, 0); l.rotation_mode = "QUATERNION"
    from mathutils import Vector
    l.rotation_quaternion = Vector(dvec.tolist()).to_track_quat("-Z", "Y")
area((-3.0, -4.0, 4.0), 300, 4.0, (1.0, 0.97, 0.93))
area((3.5, -2.5, 1.8), 120, 4.0, (0.93, 0.95, 1.0))
area((0.5, 4.0, 3.5), 260, 3.0, (1.0, 0.96, 0.92))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = srgb("#E6E8EE"); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55

tgt = bpy.data.objects.new("tgt", None); sc.collection.objects.link(tgt); tgt.location = (0, 0, 0.9)
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 70
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
tr = cam.constraints.new("TRACK_TO"); tr.target = tgt; tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"

def place(az_deg, dist=5.2, h=1.25):
    a = math.radians(az_deg)   # 0 = 정면(-Y 쪽에서 봄), 90 = 루카스 왼쪽(+X)
    cam.location = (dist * math.sin(a), -dist * math.cos(a), h)

if MODE == "face":
    # 얼굴 확대: 머리 높이에서 망원으로
    sc.render.resolution_x, sc.render.resolution_y = 800, 800
    tgt.location = (0, 0, 1.46); cam_d.lens = 135
    for nm, az in [("f_front", 0), ("f_34L", -35), ("f_34R", 35), ("f_side", 90)]:
        a = math.radians(az); cam.location = (5.0 * math.sin(a), -5.0 * math.cos(a), 1.52)
        sc.render.filepath = os.path.join(DST, nm + ".png")
        bpy.ops.render.render(write_still=True); print("RENDER_OK", nm)
elif MODE == "stills":
    sc.render.resolution_x, sc.render.resolution_y = 900, 1100
    for nm, az in [("a_front", 0), ("b_34", -32), ("c_side", 90), ("d_back34", 150)]:
        place(az); sc.render.filepath = os.path.join(DST, nm + ".png")
        bpy.ops.render.render(write_still=True); print("RENDER_OK", nm)
else:
    sc.render.resolution_x, sc.render.resolution_y = 720, 880
    sc.frame_start, sc.frame_end = 1, NFR
    sc.render.fps = 24
    place(-20)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    ob.rotation_mode = "XYZ"
    ob.rotation_euler = (0, 0, 0); ob.keyframe_insert("rotation_euler", index=2, frame=1)
    ob.rotation_euler = (0, 0, math.radians(360) * NFR / (NFR + 1)); ob.keyframe_insert("rotation_euler", index=2, frame=NFR)
    sc.render.filepath = os.path.join(DST, "f_")
    sc.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(animation=True); print("RENDER_OK turn")
