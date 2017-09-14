# Prevents it from being reloaded
if not "bpy" in locals():
    # Global dict to hold the mesh for edit mode
    dic = {}

import bpy
import bmesh

# Scale used for importing (multiplicative)
IMPORT_SCALE = 0.01

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
FORMAT_UNK   = -1
FORMAT_BMP   =  0
FORMAT_CAR   =  1
FORMAT_FIN   =  2
FORMAT_FOB   =  3
FORMAT_HUL   =  4
FORMAT_LIT   =  5
FORMAT_NCP   =  6
FORMAT_NCP_W =  7
FORMAT_PRM   =  8
FORMAT_RIM   =  9
FORMAT_RTU   = 10
FORMAT_TAZ   = 11
FORMAT_VIS   = 12
FORMAT_W     = 13

file_formats = {
    FORMAT_UNK   : "Unknown Format",
    FORMAT_BMP   : "BMP",
    FORMAT_CAR   : "Parameters.txt",
    FORMAT_FIN   : "FIN",
    FORMAT_FOB   : "FOB",
    FORMAT_HUL   : "HUL",
    FORMAT_LIT   : "LIT",
    FORMAT_NCP   : "NCP (Object)",
    FORMAT_NCP_W : "NCP (World)",
    FORMAT_PRM   : "PRM/M",
    FORMAT_RIM   : "RIM",
    FORMAT_RTU   : "RTU",
    FORMAT_TAZ   : "TAZ",
    FORMAT_VIS   : "VIS",
    FORMAT_W     : "W",
}

"""
Conversion functions for Re-Volt structures.
Axes are saved differently and many indices are saved in reverse order.
"""

def to_blender_axis(vec):
    return (vec[0], vec[2], -vec[1])

def reverse_quad(quad, tri=False):
    if tri:
        return quad[2::-1]
    else:
        return quad[::-1]

"""
Blender helpers
"""

def redraw():
    bpy.context.area.tag_redraw()
