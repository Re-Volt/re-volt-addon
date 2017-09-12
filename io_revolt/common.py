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

def to_blender_axis(vec):
    return (vec[0], vec[2], -vec[1])
