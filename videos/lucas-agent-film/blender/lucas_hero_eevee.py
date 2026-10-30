# 주인공 루카스 한 명 고급 렌더 시험(사이클). 사용: blender -b -P lucas_hero.py -- <출력 png> [samples]
import bpy, math, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import clay_lib as C

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = args[0] if args else "lucas_hero.png"
SAMPLES = int(args[1]) if len(args) > 1 else 96

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
try:
    sc.eevee.use_raytracing = True
    sc.eevee.ray_tracing_options.resolution_scale = "1"
    sc.eevee.use_shadows = True
    sc.eevee.shadow_ray_count = 3
    sc.eevee.shadow_step_count = 12
    sc.eevee.taa_render_samples = 64
    sc.eevee.fast_gi_method = "GLOBAL_ILLUMINATION"
except Exception as ex:
    print("EEVEE_OPT", ex)
sc.render.resolution_x, sc.render.resolution_y = 1080, 1350
sc.render.filepath = OUT
sc.view_settings.view_transform = "Standard"

C.init_mats()
C.build_head(origin=(0, 0, C.HEAD_Z))
C.build_body()
# 테이크아웃 컵(뚜껑·종이 슬리브)
cup = C.cyl("cup", (0.9, -0.26, 0.92), 0.13, 0.36, C.mat("#FFFFFF", 0.35))
C.cyl("sleeve", (0.9, -0.26, 0.9), 0.135, 0.14, C.mat("#B9834F", 0.7))
C.cyl("lid", (0.9, -0.26, 1.12), 0.14, 0.05, C.mat("#F1EEE8", 0.4))

# 무대: 바닥과 둥근 뒷벽(이음새 없이 휘어진 배경)
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); fl = bpy.context.object
fl.data.materials.append(C.mat("#DCE3F0", 0.85))
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 9, 8), rotation=(math.radians(90), 0, 0)); wl = bpy.context.object
wl.data.materials.append(C.mat("#CBD5EA", 0.9))

def area(loc, energy, size, rot, color=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc); l = bpy.context.object
    l.data.energy = energy; l.data.size = size; l.rotation_euler = rot; l.data.color = color
area((-4.5, -6.0, 6.5), 650, 6.0, (math.radians(48), 0, math.radians(-35)), (1.0, 0.97, 0.93))
area((5.0, -4.5, 2.5), 300, 5.0, (math.radians(70), 0, math.radians(48)), (0.9, 0.94, 1.0))
area((0.0, 5.0, 6.0), 450, 4.0, (math.radians(-45), 0, math.radians(180)), (1.0, 0.95, 0.9))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = C.srgb("#C7D2EA"); w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45

bpy.ops.object.camera_add(location=(0.9, -10.5, 2.6)); cam = bpy.context.object
cam.data.lens = 70
cam.rotation_euler = (math.radians(87), 0, math.radians(5))
cam.data.dof.use_dof = True; cam.data.dof.focus_distance = 10.4; cam.data.dof.aperture_fstop = 4.0
sc.camera = cam
bpy.ops.render.render(write_still=True)
print("RENDER_OK", OUT)
