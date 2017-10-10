# Prevents it from being reloaded
if "bpy" not in locals():
    # Global dict to hold the mesh for edit mode
    dic = {}

import bpy
import bmesh
import os
import mathutils
from math import sqrt
from .parameters import read_parameters

# If True, more debug messages will be printed
DEBUG = False

# Scale used for importing (multiplicative)
IMPORT_SCALE = 0.01
EXPORT_SCALE = 100

FACE_QUAD = 1               # 0x1
FACE_DOUBLE = 2             # 0x2
FACE_TRANSLUCENT = 4        # 0x4
FACE_MIRROR = 128           # 0x80
FACE_TRANSL_TYPE = 256      # 0x100
FACE_TEXANIM = 512          # 0x200
FACE_NOENV = 1024           # 0x400
FACE_ENV = 2048             # 0x800
FACE_CLOTH = 4096           # 0x1000
FACE_SKIP = 8192            # 0x2000

# Used to unmask unsupported flags (FACE_SKIP)
FACE_PROP_MASK = (
    FACE_QUAD | FACE_DOUBLE | FACE_TRANSLUCENT | FACE_MIRROR |
    FACE_TRANSL_TYPE | FACE_TEXANIM | FACE_NOENV | FACE_ENV |
    FACE_CLOTH
)
FACE_PROPS = [FACE_QUAD,
              FACE_DOUBLE,
              FACE_TRANSLUCENT,
              FACE_MIRROR,
              FACE_TRANSL_TYPE,
              FACE_TEXANIM,
              FACE_NOENV,
              FACE_ENV,
              FACE_CLOTH,
              FACE_SKIP]

materials = [
    ("MATERIAL_NONE", "None", "None", "", -1),
    ("MATERIAL_DEFAULT", "Default", "None", "", 0),
    ("MATERIAL_MARBLE", "Marble", "None", "", 1),
    ("MATERIAL_STONE", "Stone", "None", "", 2),
    ("MATERIAL_WOOD", "Wood", "None", "", 3),
    ("MATERIAL_SAND", "Sand", "None", "", 4),
    ("MATERIAL_PLASTIC", "Plastic", "None", "", 5),
    ("MATERIAL_CARPETTILE", "Carpet tile", "None", "", 6),
    ("MATERIAL_CARPETSHAG", "Carpet shag", "None", "", 7),
    ("MATERIAL_BOUNDARY", "Boundary", "None", "", 8),
    ("MATERIAL_GLASS", "Glass", "None", "", 9),
    ("MATERIAL_ICE1", "Ice 1", "None", "", 10),
    ("MATERIAL_METAL", "Metal", "None", "", 11),
    ("MATERIAL_GRASS", "Grass", "None", "", 12),
    ("MATERIAL_BUMPMETAL", "Bump metal", "None", "", 13),
    ("MATERIAL_PEBBLES", "Pebbles", "None", "", 14),
    ("MATERIAL_GRAVEL", "Gravel", "None", "", 15),
    ("MATERIAL_CONVEYOR1", "Conveyor 1", "None", "", 16),
    ("MATERIAL_CONVEYOR2", "Conveyor 2", "None", "", 17),
    ("MATERIAL_DIRT1", "Dirt 1", "None", "", 18),
    ("MATERIAL_DIRT2", "Dirt 2", "None", "", 19),
    ("MATERIAL_DIRT3", "Dirt 3", "None", "", 20),
    ("MATERIAL_ICE2", "Ice 2", "None", "", 21),
    ("MATERIAL_ICE3", "Ice 3", "None", "", 22),
    ("MATERIAL_WOOD2", "Wood 2", "None", "", 23),
    ("MATERIAL_CONVEYOR_MARKET1", "Conveyor Market 1", "None", "", 24),
    ("MATERIAL_CONVEYOR_MARKET2", "Conveyor Market 2", "None", "", 25),
    ("MATERIAL_PAVING", "Paving", "None", "", 26)
]

"""
Supported File Formats
"""
FORMAT_UNK = -1
FORMAT_BMP = 0
FORMAT_CAR = 1
FORMAT_FIN = 2
FORMAT_FOB = 3
FORMAT_HUL = 4
FORMAT_LIT = 5
FORMAT_NCP = 6
FORMAT_NCP_W = 7
FORMAT_PRM = 8
FORMAT_RIM = 9
FORMAT_RTU = 10
FORMAT_TAZ = 11
FORMAT_VIS = 12
FORMAT_W = 13

file_formats = {
    FORMAT_UNK: "Unknown Format",
    FORMAT_BMP: "BMP",
    FORMAT_CAR: "parameters.txt",
    FORMAT_FIN: "FIN",
    FORMAT_FOB: "FOB",
    FORMAT_HUL: "HUL",
    FORMAT_LIT: "LIT",
    FORMAT_NCP: "NCP (Object)",
    FORMAT_NCP_W: "NCP (World)",
    FORMAT_PRM: "PRM/M",
    FORMAT_RIM: "RIM",
    FORMAT_RTU: "RTU",
    FORMAT_TAZ: "TAZ",
    FORMAT_VIS: "VIS",
    FORMAT_W: "W",
}

# Colors for debug objects
COL_CUBE = mathutils.Color((0.7, 0.08, 0))
COL_BBOX = mathutils.Color((0, 0, 0.05))
COL_BCUBE = mathutils.Color((0, 0.7, 0.08))


def dprint(str):
    if DEBUG:
        print(str)


"""
Constants for the tool shelf functions
"""

bake_lights = [
    ("None", "None", "", -1),
    ("HEMI", "Soft", "", 0),
    ("SUN", "Hard", "", 1)
]

bake_light_orientations = [
    ("X", "X (Horizontal)", "", 0),
    ("Y", "Y (Horizontal)", "", 1),
    ("Z", "Z (Vertical)", "", 2)
]
bake_shadow_methods = [
    ("ADAPTIVE_QMC", "Default (fast)", "", 0),
    ("CONSTANT_QMC", "High Quality (slow)", "", 1)
]

"""
Conversion functions for Re-Volt structures.
Axes are saved differently and many indices are saved in reverse order.
"""


def to_blender_axis(vec):
    return (vec[0], vec[2], -vec[1])


def to_blender_coord(vec):
    return (vec[0] * IMPORT_SCALE,
            vec[2] * IMPORT_SCALE,
            -vec[1] * IMPORT_SCALE)


def to_blender_scale(num):
    return num * IMPORT_SCALE


def to_revolt_coord(vec):
    return (vec[0] * EXPORT_SCALE,
            -vec[2] * EXPORT_SCALE,
            vec[1] * EXPORT_SCALE)


def to_revolt_axis(vec):
    return (vec[0], -vec[2], vec[1])


def rvbbox_from_bm(bm):
    """ The bbox of Blender objects has all edge coordinates. RV just stores the
    mins and max for each axis. """
    # bbox = obj.bound_box
    xlo = min(v.co[0] for v in bm.verts) * EXPORT_SCALE
    xhi = max(v.co[0] for v in bm.verts) * EXPORT_SCALE
    ylo = -min(v.co[2] for v in bm.verts) * EXPORT_SCALE
    yhi = -max(v.co[2] for v in bm.verts) * EXPORT_SCALE
    zlo = min(v.co[1] for v in bm.verts) * EXPORT_SCALE
    zhi = max(v.co[1] for v in bm.verts) * EXPORT_SCALE
    return(xlo, xhi, ylo, yhi, zlo, zhi)


def get_distance(v1, v2):
    return sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + (v1[2] - v2[2])**2)


def center_from_rvbbox(rvbbox):
    return (
        (rvbbox[0] + rvbbox[1]) / 2,
        (rvbbox[2] + rvbbox[3]) / 2,
        (rvbbox[4] + rvbbox[5]) / 2,
    )


def radius_from_bmesh(bm, center):
    """ Gets the radius measured from the furthest vertex."""
    radius = max([get_distance(center, to_revolt_coord(v.co)) for v in bm.verts])
    return radius


def reverse_quad(quad, tri=False):
    if tri:
        return quad[2::-1]
    else:
        return quad[::-1]


def texture_to_int(string):
    if string == "car.bmp":
        return 0
    elif ".bmp" in string:
        num = ord(string[-5]) - 97
        if num > 9 or num < 0:
            return 0
        return num
    else:
        return 0


def create_material(name, diffuse, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_intensity = 1.0
    mat.alpha = alpha
    if alpha:
        mat.use_transparency = True
    return mat


"""
Blender helpers
"""
def get_average_vcol(faces, layer):
    """ Gets the average vertex color of all loops of given faces """
    for face in faces:
        cols = [loop[layer] for loop in face.loops]
        r = sum([c[0] for c in cols]) / 4
        g = sum([c[1] for c in cols]) / 4
        b = sum([c[2] for c in cols]) / 4
        return (r, g, b)


def get_active_face(bm):
    if bm.select_history:
        elem = bm.select_history[-1]
        if isinstance(elem, bmesh.types.BMFace):
            return elem
    return None


def get_edit_bmesh(obj):
    try:
        bm = dic[obj.name]
        bm.faces.layers.int.get("Type")
        return bm
    except Exception as e:
        # print("Bmesh is gone, creating new one...")
        del dic[obj.name]
        bm = dic.setdefault(obj.name, bmesh.from_edit_mesh(obj.data))
        return bm


class DialogOperator(bpy.types.Operator):
    bl_idname = 'revolt.dialog'
    bl_label = 'Re-Volt Add-On Notification'

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        global dialog_message
        column = self.layout.column()
        for line in str.split(dialog_message, '\n'):
            column.label(line)


def msg_box(message):
    global dialog_message
    print(message)
    dialog_message = message
    bpy.ops.revolt.dialog('INVOKE_DEFAULT')


def redraw():
    # bpy.context.area.tag_redraw()
    redraw_3d()
    redraw_uvedit()


def redraw_3d():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
                break


def redraw_uvedit():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.tag_redraw()
                break


def enable_texture_mode():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.viewport_shade = 'TEXTURED'
    return


def texture_mode_enabled():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.viewport_shade == 'TEXTURED':
                        return True
    return False


def get_all_lod(namestr):
    """ Gets all LoD meshes belonging to a mesh (including that mesh) """
    meshes = []
    for me in bpy.data.meshes:
        if "|q" in me.name and namestr in me.name:
            meshes.append(me)
    return meshes


def triangulate_ngons(bm):
    """ Triangulates faces for exporting """
    triangulate = []
    for face in bm.faces:
        if len(face.verts) > 4:
            triangulate.append(face)
    if triangulate:
        bmesh.ops.triangulate(bm, faces=triangulate,
                              quad_method=0, ngon_method=0)
    return len(triangulate)


"""
Non-Blender helper functions
"""


def get_texture_path(filepath, tex_num):
    """ Gets the full texture path when given a file and its
        polygon texture number. """
    path, fname = filepath.rsplit(os.sep, 1)
    folder = filepath.split(os.sep)[-2]

    if not os.path.isdir(path):
        return None

    # The file is part of a car
    if "parameters.txt" in os.listdir(path):
        params = read_parameters(os.path.join(path, "parameters.txt"))
        tpage = params["tpage"].replace("\\", os.sep).split(os.sep)[-1]
        return os.path.join(path, tpage)
    # The file is part of a track
    elif is_track_folder(path):
        tpage = filepath.split(os.sep)[-2].lower() + chr(97 + tex_num) + ".bmp"
        return os.path.join(path, tpage)
    else:
        return os.path.join(path, "dummy{}.bmp".format(chr(97 + tex_num)))


def is_track_folder(path):
    for f in os.listdir(path):
        if ".inf" in f:
            return True


def get_format(fstr):
    """
    Gets the format by the ending and returns an int (see enum in common)
    """
    fname, ext = os.path.splitext(fstr)

    if ext.startswith(".bm"):
        return FORMAT_BMP
    elif ext == ".txt":
        return FORMAT_CAR
    elif ext in [".prm", ".m"]:
        return FORMAT_PRM
    elif ext == ".w":
        return FORMAT_W
    else:
        return FORMAT_UNK
