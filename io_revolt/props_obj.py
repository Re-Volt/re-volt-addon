import bpy

from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
    CollectionProperty,
    IntVectorProperty,
    FloatVectorProperty,
    PointerProperty
)
from .common import *


class RVObjectProperties(bpy.types.PropertyGroup):

    # Debug Objects
    is_bcube = BoolProperty(
        name = "Object is a BigCube",
        default = False,
        description = "Makes BigCube properties visible for this object"
    )
    is_cube = BoolProperty(
        name = "Object is a Cube",
        default = False,
        description = "Makes Cube properties visible for this object"
    )
    is_bbox = BoolProperty(
        name = "Object is a Boundary Box",
        default = False,
        description = "Makes BoundBox properties visible for this object"
    )
    ignore_ncp = BoolProperty(
        name = "Ignore Collision (.ncp)",
        default = False,
        description = "Ignores the object when exporting to NCP"
    )
    bcube_mesh_indices = StringProperty(
        name = "Mesh indices",
        default = "",
        description = "Indices of child meshes"
    )
