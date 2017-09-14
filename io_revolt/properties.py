"""
Re-Volt Object and mesh properties and functions for setting/getting them.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)

import bpy
from . import common
from bpy.props import (
BoolProperty,
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

"""
These property getters and setters use the bmesh from the global dict that gets
updated by the scene update handler found in init.
Creating bmeshes in the panels is bad practice as it causes unexpected behavior.
"""

def get_face_material(self):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("revolt_material")
             or bm.faces.layers.int.new("revolt_material"))
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0 or any([face[layer] != selected_faces[0][layer] for face in selected_faces]):
        return -1
    else:
        return selected_faces[0][layer]

def set_face_material(self, value):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("revolt_material")
             or bm.faces.layers.int.new("revolt_material"))
    for face in bm.faces:
        if face.select:
            face[layer] = value

def get_face_texture(self):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("Texture Number")
             or bm.faces.layers.int.new("Texture Number"))
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0 or any([face[layer] != selected_faces[0][layer] for face in selected_faces]):
        return -1
    else:
        return selected_faces[0][layer]

def set_face_texture(self, value):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = (bm.faces.layers.int.get("Texture Number")
             or bm.faces.layers.int.new("Texture Number"))
    for face in bm.faces:
        if face.select:
            face[layer] = value

def get_face_property(self):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = bm.faces.layers.int.get("Type") or bm.faces.layers.int.new("Type")
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0:
        return 0
    prop = selected_faces[0][layer]
    for face in selected_faces:
        prop = prop & face[layer]
    return prop

def set_face_property(self, value, mask):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    layer = bm.faces.layers.int.get("Type") or bm.faces.layers.int.new("Type")
    for face in bm.faces:
        if face.select:
            face[layer] = face[layer] | mask if value else face[layer] & ~mask

def select_faces(context, prop):
    eo = bpy.context.edit_object
    bm = dic.setdefault(eo.name, bmesh.from_edit_mesh(eo.data))
    flag_layer = (bm.faces.layers.int.get("Type")
                  or bm.faces.layers.int.new("Type"))

    for face in bm.faces:
        if face[flag_layer] & prop:
            face.select = not face.select
    redraw()

"""
Re-Volt object and mesh properties
"""

class RVObjectProperties(bpy.types.PropertyGroup):

    is_fin = BoolProperty(
            # name="Object is an Instance",
            description="Object is an Instance",
            # description="Only Instance objects are exported to the .fin file (and automatically rejected from World and World NCP file)",
            )

class RVMeshProperties(bpy.types.PropertyGroup):
    face_material = EnumProperty(
        name = "Material",
        items = materials,
        get = get_face_material,
        set = set_face_material
    )
    face_texture = IntProperty(
        name = "Texture",
        get = get_face_texture,
        set = set_face_texture
    )
    face_double_sided = BoolProperty(
        name = "Double sided",
        get = lambda s: bool(get_face_property(s) & FACE_DOUBLE),
        set = lambda s,v: set_face_property(s, v, FACE_DOUBLE)
    )
    face_translucent = BoolProperty(
        name = "Translucent",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSLUCENT),
        set = lambda s,v: set_face_property(s, v, FACE_TRANSLUCENT)
    )
    face_mirror = BoolProperty(
        name = "Mirror",
        get = lambda s: bool(get_face_property(s) & FACE_MIRROR),
        set = lambda s,v: set_face_property(s, v, FACE_MIRROR)
    )
    face_additive = BoolProperty(
        name = "Additive blending",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSL_TYPE),
        set = lambda s,v: set_face_property(s, v, FACE_TRANSL_TYPE)
    )
    face_texture_animation = BoolProperty(
        name = "Animated",
        get = lambda s: bool(get_face_property(s) & FACE_TEXANIM),
        set = lambda s,v: set_face_property(s, v, FACE_TEXANIM)
    )
    face_no_envmapping = BoolProperty(
        name = "No EnvMap (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_NOENV),
        set = lambda s,v: set_face_property(s, v, FACE_NOENV)
    )
    face_envmapping = BoolProperty(
        name = "EnvMapping (.w)",
        get = lambda s: bool(get_face_property(s) & FACE_ENV),
        set = lambda s,v: set_face_property(s, v, FACE_ENV)
    )
    face_cloth = BoolProperty(
        name = "Cloth effect (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_CLOTH),
        set = lambda s,v: set_face_property(s, v, FACE_CLOTH)
    )
    face_skip = BoolProperty(
        name = "Do not export",
        get = lambda s: bool(get_face_property(s) & FACE_SKIP),
        set = lambda s,v: set_face_property(s, v, FACE_SKIP)
    )
