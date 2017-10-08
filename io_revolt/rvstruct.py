"""
This is a module for reading and writing Re-Volt binary files.
Todo:
- Rework representations and string representations
- Rework default values based on the game's defaults
- Check for lengths on export

Supported Formats:
- .prm / .m (PRM)
- .w (World)
- .fin (Instances)
- .pan (PosNodes)

Missing Formats:
- .fan (AiNodes)
- .taz (TrackZones)
- .fob (Objects)
- .fld (ForceFields)
- .lit (Lights)
- .tri (Triggers)
"""

import struct
from math import sqrt

from . import common
from .common import *


class World:
    """
    Reads a .w file and stores all sub-structures
    All contained objects are of a similar structure.
    Usage: Objects of this class can be created to read and store .w files.
    If an opened file is supplied, it immediately starts reading from it.
    """
    def __init__(self, file=None):
        self.mesh_count = 0             # rvlong, amount of Mesh objects
        self.meshes = []                # sequence of Mesh structures

        self.bigcube_count = 0          # rvlong, amount of BigCubes
        self.bigcubes = []              # sequence of BigCubes

        self.animation_count = 0        # rvlong, amount of Texture Animations
        self.animations = []            # sequence of TexAnimation structures

        self.env_count = 0              # amount of faces with env enabled
        self.env_list = []            # an EnvList structure

        # Immediately starts reading if an opened file is supplied
        if file:
            self.read(file)

    def read(self, file):
        # Reads the mesh count (one rvlong)
        self.mesh_count = struct.unpack("<l", file.read(4))[0]

        # Reads the meshes. Gives the meshes a reference to itself so env_count
        # can be set by the Polygon objects
        for mesh in range(self.mesh_count):
            self.meshes.append(Mesh(file, self))

        # Reads the amount of bigcubes
        self.bigcube_count = struct.unpack("<l", file.read(4))[0]

        # Reads all BigCubes
        for bcube in range(self.bigcube_count):
            self.bigcubes.append(BigCube(file))

        # Reads texture animation count
        self.animation_count = struct.unpack("<l", file.read(4))[0]

        # Reads all animations
        for anim in range(self.animation_count):
            self.animations.append(TexAnimation(file))

        # Reads the environment colors
        for col in range(self.env_count):
            self.env_list.append(Color(file=file, alpha=True))

    def write(self, file):
        # Writes the mesh count
        file.write(struct.pack("<l", self.mesh_count))

        # Writes all meshes, gives reference to self for env count
        for mesh in self.meshes:
            mesh.write(file)

        # Writes the count of BigCubes
        file.write(struct.pack("<l", self.bigcube_count))

        # Writes all BigCubes
        for bcube in self.bigcubes:
            bcube.write(file)

        # Writes the count of texture animations
        file.write(struct.pack("<l", self.animation_count))

        # Writes all texture animations
        for anim in self.animations:
            anim.write(file)

        # self.env_list.write(file)
        for col in self.env_list:
            col.write(file)

    def generate_bigcubes(self):
        bb = BoundingBox()
        for mesh in self.meshes:
            for v in mesh.vertices:
                bb.xlo = v.position.x if v.position.x < bb.xlo else bb.xlo
                bb.xhi = v.position.x if v.position.x > bb.xhi else bb.xhi
                bb.ylo = v.position.y if v.position.y < bb.ylo else bb.ylo
                bb.yhi = v.position.y if v.position.y > bb.yhi else bb.yhi
                bb.zlo = v.position.z if v.position.z < bb.zlo else bb.zlo
                bb.zhi = v.position.z if v.position.z > bb.zhi else bb.zhi

        bcube = BigCube()
        bcube.center = Vector(data=(
            (bb.xlo + bb.xhi) / 2,
            (bb.ylo + bb.yhi) / 2,
            (bb.zlo + bb.zhi) / 2)
        )
        max_vert = Vector(data=(bb.xhi, bb.yhi, bb.zhi))
        bcube.size = bcube.center.get_distance_to(max_vert)

        bcube.mesh_count = len(self.meshes)
        bcube.mesh_indices = [n for n in range(0, bcube.mesh_count)]

        self.bigcube_count = 1
        self.bigcubes = [bcube]

    def __repr__(self):
        return "World"

    def as_dict(self):
        dic = {"mesh_count": self.mesh_count,
               "meshes": self.meshes,
               "bigcube_count": self.bigcube_count,
               "bigcubes": self.bigcubes,
               "animation_count": self.animation_count,
               "animations": self.animations,
               "env_count": self.env_count,
               "env_list": self.env_list
               }
        return dic

    # Uses the to-string for dumping the whole .w structure
    def dump(self):
        return ("====   WORLD   ====\n"
                "Mesh count: {}\n"
                "Meshes:\n{}\n"
                "BigCube count: {}\n"
                "BigCubes:\n{}\n"
                "Animation Count: {}\n"
                "Animations:\n{}\n"
                "ENV Count: {}\n"
                "EnvList:\n{}\n"
                "==== WORLD END ====\n"
               ).format(self.mesh_count,
               '\n'.join([str(mesh) for mesh in self.meshes]),
               self.bigcube_count,
               '\n'.join([str(bcube) for bcube in self.bigcubes]),
               self.animation_count,
               '\n'.join([str(anim) for anim in self.animations]),
               self.env_count,
               self.env_list)


class PRM:
    """
    Similar to Mesh, reads, stores and writes PRM files
    """
    def __init__(self, file=None):
        self.polygon_count = 0
        self.vertex_count = 0

        self.polygons = []
        self.vertices = []

        if file:
            self.read(file)

    def __repr__(self):
        return "PRM"

    def read(self, file):
        self.polygon_count = struct.unpack("<h", file.read(2))[0]
        self.vertex_count = struct.unpack("<h", file.read(2))[0]

        for polygon in range(self.polygon_count):
            self.polygons.append(Polygon(file))

        for vertex in range(self.vertex_count):
            self.vertices.append(Vertex(file))

    def write(self, file):
        # Writes amount of polygons/vertices and the structures themselves
        file.write(struct.pack("<h", self.polygon_count))
        file.write(struct.pack("<h", self.vertex_count))

        for polygon in self.polygons:
            polygon.write(file)
        for vertex in self.vertices:
            vertex.write(file)

    def as_dict(self):
        dic = { "polygon_count" : self.polygon_count,
                "vertex_count" : self.vertex_count,
                "polygons" : self.polygons,
                "vertices" : self.vertices
        }
        return dic

    def dump(self):
        return ("====   PRM   ====\n"
                "Polygon Count: {}\n"
                "Vertex Count: {}\n"
                "Polygons:\n{}"
                "Vertices:\n{}"
                "==== PRM END ====\n"
               ).format(self.polygon_count,
                        self.vertex_count,
                        '\n'.join([str(polygon) for polygon in self.polygons]),
                        '\n'.join([str(vertex) for vertex in self.vertices]))


class Mesh:
    """
    Reads the Meshes found in .w files from an opened file
    These are different from PRM meshes since they also contain
    bounding boxes.
    """
    def __init__(self, file=None, w=None):
        self.w = w                      # World it belongs to

        self.bound_ball_center = None   # Vector
        self.bound_ball_radius = None   # rvfloat

        self.bbox = None                # BoundingBox

        self.polygon_count = None       # rvlong
        self.vertex_count = None        # rvlong

        self.polygons = []              # Sequence of Polygon objects
        self.vertices = []              # Sequence of Vertex objects

        if file:
            self.read(file)

    def __repr__(self):
        return "Mesh"

    def from_prm(self, prm):
        self.polygon_count = prm.polygon_count
        self.vertex_count = prm.vertex_count
        self.polygons = prm.polygons
        self.vertices = prm.vertices

    def read(self, file):
        # Reads bounding "ball" center and the radius
        self.bound_ball_center = Vector(file)
        self.bound_ball_radius = struct.unpack("<f", file.read(4))[0]
        self.bbox = BoundingBox(file)

        # Reads amount of polygons/vertices and the structures themselves
        self.polygon_count = struct.unpack("<h", file.read(2))[0]
        self.vertex_count = struct.unpack("<h", file.read(2))[0]

        # Also give the polygon a reference to w so it can report if env is on
        for polygon in range(self.polygon_count):
            self.polygons.append(Polygon(file, self.w))

        for vertex in range(self.vertex_count):
            self.vertices.append(Vertex(file))

    def write(self, file):
        # Writes bounding "ball" center and the radius and then the bounding box
        self.bound_ball_center.write(file)
        file.write(struct.pack("<f", self.bound_ball_radius))
        self.bbox.write(file)

        file.write(struct.pack("<h", self.polygon_count))
        file.write(struct.pack("<h", self.vertex_count))

        # Also give the polygon a reference to w so it can write the env bit
        for polygon in self.polygons:
            polygon.write(file)
        for vertex in self.vertices:
            vertex.write(file)

    def as_dict(self):
        dic = { "bound_ball_center" : self.bound_ball_center,
                "bound_ball_radius" : self.bound_ball_radius,
                "bbox" : self.bbox,
                "polygon_count" : self.polygon_count,
                "vertex_count" : self.vertex_count,
                "polygons" : self.polygons,
                "vertices" : self.vertices,
        }
        return dic

    def dump(self):
        return ("====   MESH   ====\n"
                "Bounding Ball Center: {}\n"
                "Bounding Ball Radius: {}\n"
                "Bounding Box:\n{}\n"
                "Polygon Count: {}\n"
                "Vertex Count: {}\n"
                "Polygons:\n{}"
                "Vertices:\n{}"
                "==== MESH END ====\n"
               ).format(self.bound_ball_center,
                        self.bound_ball_radius,
                        self.bbox,
                        self.polygon_count,
                        self.vertex_count,
                        '\n'.join([str(polygon) for polygon in self.polygons]),
                        '\n'.join([str(vertex) for vertex in self.vertices]))


class BoundingBox:
    """
    Reads and stores bounding boxes found in .w meshes
    They are probably used for culling optimization, similar to BigCube
    """
    def __init__(self, file=None, data=None):
        # Lower and higher boundaries for each axis
        if data is None:
            self.xlo = 0
            self.xhi = 0
            self.ylo = 0
            self.yhi = 0
            self.zlo = 0
            self.zhi = 0
        else:
            self.xlo, self.xhi, self.ylo, self.yhi, self.zlo, self.zhi = data

        if file:
            self.read(file)

    def __repr__(self):
        return "BoundingBox"

    def read(self, file):
        # Reads boundaries
        self.xlo, self.xhi = struct.unpack("<ff", file.read(8))
        self.ylo, self.yhi = struct.unpack("<ff", file.read(8))
        self.zlo, self.zhi = struct.unpack("<ff", file.read(8))

    def write(self, file):
        # Writes all boundaries
        file.write(struct.pack("<6f", self.xlo, self.xhi, self.ylo,
                        self.yhi, self.zlo, self.zhi))

    def as_dict(self):
        dic = { "xlo": self.xlo,
                "xhi": self.xhi,
                "ylo": self.ylo,
                "yhi": self.yhi,
                "zlo": self.zlo,
                "zhi": self.zhi
        }
        return dic

    def dump(self):
        return ("xlo {}\n"
                "xhi {}\n"
                "ylo {}\n"
                "yhi {}\n"
                "zlo {}\n"
                "zhi {}\n"
                ).format(self.xlo, self.xhi, self.ylo,
                         self.yhi, self.zlo, self.zhi)


class Vector:
    """
    A very simple vector class
    """
    def __init__(self, file=None, data=None):
        if data:
            self.data = data
        else:
            self.data = None

        if file:
            self.read(file)

    def __repr__(self):
        return "Vector"

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    @property
    def z(self):
        return self.data[2]

    def get_distance_to(self, v):
        return sqrt((self.x - v.x)**2 + (self.y - v.y)**2 + (self.z - v.z)**2)

    def read(self, file):
        # Reads the coordinates
        self.data = struct.unpack("<3f", file.read(12))

    def write(self, file):
        # Writes all coordinates
        file.write(struct.pack("<3f", *self.data))

    def as_dict(self):
        dic = {"x": self.data[0],
               "y": self.data[1],
               "z": self.data[2]
               }
        return dic

    def dump(self):
        return str(self.data)

class Matrix:
    """
    A class for matrices mainly used for orientation and theoretically scale.
    If the matrix is bigger than 3x3, it will be truncated on export.
    """
    def __init__(self, file=None, data=None):
        self.data = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

        if file:
            self.read(file)

    def __repr__(self):
        return "Matrix"

    def read(self, file):
        # Reads the matrix line by line
        self.data[0] = struct.unpack("<3f", file.read(12))
        self.data[1] = struct.unpack("<3f", file.read(12))
        self.data[2] = struct.unpack("<3f", file.read(12))

    def write(self, file):
        # Writes the matrix line by line (only the firs three columns and rows)
        file.write(struct.pack("<3f", *self.data[:3][0]))
        file.write(struct.pack("<3f", *self.data[:3][1]))
        file.write(struct.pack("<3f", *self.data[:3][2]))

    def as_dict(self):
        dic = { "(0, 0)" : self.data[0][0],
                "(0, 1)" : self.data[0][1],
                "(0, 2)" : self.data[0][2],
                "(1, 0)" : self.data[1][0],
                "(1, 1)" : self.data[1][1],
                "(1, 2)" : self.data[1][2],
                "(2, 0)" : self.data[2][0],
                "(2, 1)" : self.data[2][1],
                "(2, 2)" : self.data[2][2],
        }
        return dic

    def dump(self):
        return "\n".join(str(vec) for vec in self.data)


class Polygon:
    """
    Reads a Polygon structure and stores it.
    """
    def __init__(self, file=None, w=None):
        self.w = w                  # World it belongs to

        self.type = 0               # rvshort
        self.texture = 0            # rvshort

        self.vertex_indices = []    # 4 rvshorts
        self.colors = []            # 4 unsigned rvlongs

        self.uv = []                # UV structures (4)

        if file:
            self.read(file)

    def __repr__(self):
        return "Polygon"

    def read(self, file):
        # Reads the type bitfield and the texture index
        self.type = struct.unpack("<h", file.read(2))[0]
        self.texture = struct.unpack("<h", file.read(2))[0]

        # Reads indices of the polygon's vertices and their vertex colors
        self.vertex_indices = struct.unpack("<4h", file.read(8))
        self.colors = [Color(file=file, alpha=True),
            Color(file=file, alpha=True), Color(file=file, alpha=True),
            Color(file=file, alpha=True)]

        # Reads the UV mapping
        for x in range(4):
            self.uv.append(UV(file))

        # Tells the .w if bit 11 (environment map) is enabled for this
        if self.w and self.type & 2048:
                self.w.env_count += 1

    def write(self, file):
        # Writes the type bitfield and the texture index
        file.write(struct.pack("<h", self.type))
        file.write(struct.pack("<h", self.texture))

        # Writes indices of the polygon's vertices and their vertex colors
        for ind in self.vertex_indices:
            file.write(struct.pack("<h", ind))
        for col in self.colors:
            col.write(file)
            # file.write(struct.pack("<L", col))

        # Writes the UV coordinates
        for uv in self.uv:
            uv.write(file)

    def as_dict(self):
        dic = { "type" : self.type,
                "texture" : self.texture,
                "vertex_indices" : self.vertex_indices,
                "colors" : self.colors,
                "uv" : self.uv
        }
        return dic

    def dump(self):
        return ("====   POLYGON   ====\n"
                "Type: {}\n"
                "Texture: {}\n"
                "Vertex Indices: {}\n"
                "Colors:\n{}\n"
                "UV: {}\n"
                "==== POLYGON END ====\n"
               ).format(self.type,
                        self.texture,
                        self.vertex_indices,
                        '\n'.join([str(col) for col in self.colors]),
                        '\n'.join([str(uv) for uv in self.uv]))


class Vertex:
    """
    Reads a Polygon structure and stores it
    """
    def __init__(self, file=None):
        self.position = None    # Vector
        self.normal = None      # Vector (normalized, length 1)

        if file:
            self.read(file)

    def __repr__(self):
        return "Vertex"

    def read(self, file):
        # Stores position and normal as a vector
        self.position = Vector(file)
        self.normal = Vector(file)

    def write(self, file):
        # Writes position and normal as a vector
        self.position.write(file)
        self.normal.write(file)

    def as_dict(self):
        dic = {"position": self.position.as_dict(),
               "normal": self.normal.as_dict()
               }
        return dic

    def dump(self):
        return ("====   VERTEX   ====\n"
                "Position: {}\n"
                "Normal: {}\n"
                "==== VERTEX END ====\n"
                ).format(self.position, self.normal)


class UV:
    """
    Reads UV-map structure and stores it
    """
    def __init__(self, file=None, uv=None):
        if uv:
            self.u, self.v = uv
        else:
            self.u = 0.0     # rvfloat
            self.v = 0.0     # rvfloat

        if file:
            self.read(file)

    def __repr__(self):
        return str(self.as_dict())

    def read(self, file):
        # Reads the uv coordinates
        self.u = struct.unpack("<f", file.read(4))[0]
        self.v = struct.unpack("<f", file.read(4))[0]

    def write(self, file):
        # Writes the uv coordinates
         file.write(struct.pack("<f", self.u))
         file.write(struct.pack("<f", self.v))

    def as_dict(self):
        dic = { "u" : self.u,
                "v" : self.v
        }
        return dic

    def from_dict(self, dic):
        self.u = dic["u"]
        self.v = dic["v"]

    def dump(self):
        return "({}, {})".format(self.u, self.v)


class BigCube:
    """
    Reads a BigCube structure and stores it
    BigCubes are used for in-game optimization (culling)
    """
    def __init__(self, file=None):
        self.center = None      # center/position of the cube, Vector
        self.size = 0           # rvfloat, size of the cube

        self.mesh_count = 0     # rvlong, amount of meshes
        self.mesh_indices = []  # indices of meshes that belong to the cube

        if file:
            self.read(file)

    def __repr__(self):
        return "BigCube"

    def read(self, file):
        # Reads center and size of the cube
        self.center = Vector(file)
        self.size = struct.unpack("<f", file.read(4))[0]

        # Reads amount of meshes and then the indices of the meshes
        self.mesh_count = struct.unpack("<l", file.read(4))[0]
        for mesh in range(self.mesh_count):
            self.mesh_indices.append(struct.unpack("<l", file.read(4))[0])

    def write(self, file):
        # Writes center and size of the cube
        self.center.write(file)
        file.write(struct.pack("<f", self.size))

        # Writes amount of meshes and then the indices of the meshes
        file.write(struct.pack("<l", self.mesh_count))
        for mesh in self.mesh_indices:
            file.write(struct.pack("<l", mesh))

    def as_dict(self):
        dic = { "center" : self.center.as_dict(),
                "size" : self.size,
                "mesh_count" : self.mesh_count,
                "mesh_indices": self.mesh_indices,
        }
        return dic

    def dump(self):
        return ("====   BIGCUBE   ====\n"
                "Center: {}\n"
                "Size: {}\n"
                "Mesh Count: {}\n"
                "Mesh Indices: {}\n"
                "==== BIGCUBE END ====\n"
                ).format(self.center,
                         self.size,
                         self.mesh_count,
                         self.mesh_indices)


class TexAnimation:
    """
    Reads and stores a texture animation of a .w file
    """
    def __init__(self, file=None):
        self.frame_count = 0    # rvlong, amount of frames
        self.frames = []        # Frame objects

        if file:
            self.read(file)

    def __repr__(self):
        return "TexAnimation"

    def read(self, file):
        # Reads the amount of frames
        self.frame_count = struct.unpack("<l", file.read(4))[0]

        # Reads the frames themselves
        for frame in range(self.frame_count):
            self.frames.append(Frame(file))

    def write(self, file):
        # Writes the amount of frames
        file.write(struct.pack("<l", self.frame_count))

        # Writes the frames
        for frame in self.frames:
            frame.write(file)

    def as_dict(self):
        dic = { "frame_count" : self.frame_count,
                "frames" : self.frames
        }
        return dic

    def from_dict(self, dic):
        self.frame_count = dic["frame_count"]
        for framedic in dic["frames"]:
            frame = Frame()
            frame.from_dict(framedic)
            self.frames.append(frame)

    def dump(self):
        return ("====   ANIMATION   ====\n"
                "Frame Count: {}\n"
                "Frames\n{}"
                "==== ANIMATION END ====\n"
                ).format(self.frame_count,
                         '\n'.join([str(frame) for frame in self.frames]))


class Frame:
    """
    Reads and stores exactly one texture animation frame
    """
    def __init__(self, file=None):
        self.texture = 0                    # texture id of the animated tex
        self.delay = 0                      # delay in milliseconds
        self.uv = [UV(), UV(), UV(), UV()]  # list of 4 UV coordinates

        if file:
            self.read(file)

    def __repr__(self):
        return str(self.as_dict())

    def __str__(self):
        return str(self.as_dict())

    def read(self, file):
        # Reads the texture id
        self.texture = struct.unpack("<l", file.read(4))[0]
        # Reads the delay
        self.delay = struct.unpack("<f", file.read(4))[0]

        # Reads the UV coordinates for this frame
        for uv in range(4):
            self.uv[uv] = UV(file)

    def write(self, file):
        # Writes the texture id
        file.write(struct.pack("<l", self.texture))
        # Writes the delay
        file.write(struct.pack("<f", self.delay))

        # Writes the UV coordinates for this frame
        for uv in self.uv[:4]:
            uv.write(file)

    def as_dict(self):
        dic = { "texture" : self.texture,
                "delay" : self.delay,
                "uv" : [uv.as_dict() for uv in self.uv]
        }
        return dic

    def from_dict(self, dic):
        self.texture = dic["texture"]
        self.delay = dic["delay"]
        uvs = []
        for x in range(0, 4):
            uvdict = dic["uv"][x]
            uv = UV()
            uv.from_dict(uvdict)
            uvs.append(uv)
        self.uv = uvs

    def dump(self):
        return ("====   FRAME   ====\n"
                "Texture: {}\n"
                "Delay: {}\n"
                "UV:\n{}\n"
                "==== FRAME END ====\n"
                ).format(self.texture,
                         self.delay,
                         '\n'.join([str(uv) for uv in self.uv]))


class Color:
    """
    Stores a color with optional alpha (RGB).
    """
    def __init__(self, file=None, color=(0, 0, 0), alpha=False):
        self.color = color          # RGB color
        self.alpha = alpha          # False or int from 0 to 255

        if file:
            self.read(file)

    def read(self, file):
        cols = struct.unpack("<BBB", file.read(3))
        self.color = (cols[2], cols[1], cols[0])
        # Reads alpha only when alpha == True
        if self.alpha:
            self.alpha = 255 - struct.unpack("<B", file.read(1))[0]

    def write(self, file):
        file.write(struct.pack("<3B", self.color[2],
                               self.color[1], self.color[0]))
        # Writes only if alpha is specified
        if self.alpha is not False and self.alpha is not None:
            file.write(struct.pack("<B", 255 - self.alpha))

    def as_dict(self):
        dic = { "r" : self.color[0],
                "g" : self.color[1],
                "b" : self.color[2],
                "alpha" : self.alpha
        }
        return dic

    def dump(self):
        return str("Color(Red: {}, Green: {}, Blue: {}, Alpha: {})".format(
                    self.color[0], self.color[1], self.color[2], self.alpha))

    def __repr__(self):
        return "Color"

        def __str__(self):
            return "Color ({}, {}, {}, {})".format(*self.color, self.alpha)


class Instances:
    """
    Reads and writes a list of instance objects (takes a .fin file).
    """
    def __init__(self, file=None):
        self.instance_count = 0          # number of instance objects
        self.instances = []              # list of Instance objects

        if file:
            self.read(file)

    def __repr__(self):
        return "Instances"

    def read(self, file):
        # Reads the specified amount of instances and adds it to the list
        self.instance_count = struct.unpack("<l", file.read(4))[0]
        for instance in range(self.instance_count):
            self.instances.append(Instance(file))

    def write(self, file):
        # Writes the amount of instances
        file.write(struct.pack("<l", self.instance_count))
        # Writes all instances
        for instance in self.instances:
            instance.write(file)

    def as_dict(self):
        dic = { "instance_count" : self.instance_count,
                "instances" : self.instances
        }
        return dic

    def dump(self):
        return ("====   INSTANCES   ====\n"
                "Instance Count: {}\n"
                "Instances:\n{}"
                "====   INSTANCES END   ====\n").format(
                    self.instance_count,
                    "\n".join([str(i) for i in self.instances]))

class Instance:
    """
    Reads and writes properties of an instanced object found in .fin files.
    """
    def __init__(self, file=None):
        self.name = ""                            # first 9 letters of file name
        self.color = Color(color=[0, 0, 0])       # model % RGB color
        self.env_color = Color(color=[0, 0, 0], alpha=True) # envMap color
        self.priority = 0                         # priority for multiplayer
        self.flag = 0                             # flag with properties
        self.lod_bias = 1024                      # when to load hq-meshes
        self.position = Vector(data=(0, 0, 0))    # position of the PRM
        self.or_matrix = Matrix(data=((0, 0, 0),
                                      (0, 0, 0),
                                      (0, 0, 0))) # orientation of the PRM

        if file:
            self.read(file)

    def __repr__(self):
        return "Instance"

    def read(self, file):
        # Reads the file name and cleans it up (remove whitespace and .prm)
        self.name = struct.unpack("<9s", file.read(9))[0]
        self.name = str(self.name, encoding='ascii').split('\x00', 1)[0]
        # Reads the model color and the envMap color
        self.color = Color(file)
        self.env_color = Color(file, alpha=True)
        # Reads priority and properties flag with two padded bytes
        self.priority, self.flag = struct.unpack('<BBxx', file.read(4))
        self.lod_bias = struct.unpack("<f", file.read(4))[0]
        self.position = Vector(file)
        self.or_matrix = Matrix(file)

    def write(self, file):
        # Writes the first 9 letters of the prm file name
        name = str.encode(self.name)
        file.write(struct.pack("9s", name))
        self.color.write(file)
        self.env_color.write(file)
        # Writes priority and properties flag with two padded bytes
        file.write(struct.pack('<BBxx', self.priority, self.flag))
        file.write(struct.pack('<f', self.lod_bias))
        self.position.write(file)
        self.or_matrix.write(file)

    def as_dict(self):
        dic = { "name" : self.name,
                "color" : self.color,
                "env_color" : self.env_color,
                "priority" : self.priority,
                "flag" : self.flag,
                "lod_bias" : self.lod_bias,
                "position" : self.position,
                "or_matrix" : self.or_matrix
        }
        return dic

    def dump(self):
        return ("====   INSTANCE   ====\n"
                "Name: {}\n"
                "Color: {}\n"
                "Env Color: {}\n"
                "Priority: {}\n"
                "Flag: {}\n"
                "LoD Bias: {}\n"
                "Position: {}\n"
                "Orientation:\n{}\n"
                "==== INSTANCE END ====\n"
                ).format(self.name,
                         str(self.color),
                         str(self.env_color),
                         str(self.priority),
                         str(self.flag),
                         str(self.lod_bias),
                         str(self.position),
                         str(self.or_matrix))

class PosNodes:
    """
    Position nodes level file (.pan)
    """
    def __init__(self, file=None):
        self.num_nodes = 0
        self.start_node = 0
        self.total_dist = 0
        self.nodes = []

        if file:
            self.read(file)

    def read(self, file):
        self.num_nodes = struct.unpack("<l", file.read(4))[0]
        self.start_node = struct.unpack("<l", file.read(4))[0]
        self.total_dist = struct.unpack("<f", file.read(4))[0]
        self.nodes = [PosNode(file) for n in range(self.num_nodes)]

    def as_dict(self):
        dic = { "num_nodes" : self.num_nodes,
                "start_node" : self.start_node,
                "total_dist" : self.total_dist,
                "nodes" : self.nodes
        }
        return dic

    def __repr__(self):
        return "PosNodes"

class PosNode:
    """
    Single node of PosNodes file.
    """
    def __init__(self, file=None):
        self.position = Vector()
        self.distance = 0
        self.next = [-1, -1, -1, -1]
        self.prev = [-1, -1, -1, -1]

        if file:
            self.read(file)

    def read(self, file):
        # Reads position
        self.position = Vector(file)

        # Reads distance to finish line
        self.distance = struct.unpack("<f", file.read(4))[0]

        # Reads previous connections
        for x in range(4):
            self.prev[x] = struct.unpack("<l", file.read(4))[0]

        # Reads upcoming connections
        for x in range(4):
            self.next[x] = struct.unpack("<l", file.read(4))[0]

    def as_dict(self):
        dic = { "position" : self.position,
                "distance" : self.distance,
                "next" : self.next,
                "previous": self.prev,
        }
        return dic

    def __repr__(self):
        return "PosNode"
