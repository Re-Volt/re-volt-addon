"""
PRM IMPORT
Meshes used for cars, game objects and track instances.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)
    imp.reload(img_in)

import os
import bpy
import bmesh
from mathutils import Color, Vector
from . import common
from . import rvstruct
from . import img_in

from .rvstruct import PRM
from .common import *


def import_file(filepath, scene):
    """
    Imports a .prm/.m file and links it to the scene as a Blender object.
    It also imports all LoDs of a PRM file, which can be sequentially written
    to the file. There is no indicator for it, the file end has to be checked.
    """
    meshes = []

    common.TEXTURES = {}

    with open(filepath, 'rb') as file:
        filename = os.path.basename(filepath)

        # Finds out the file end
        file_start = file.tell()
        file.seek(0, os.SEEK_END)
        file_end = file.tell()
        file.seek(file_start, os.SEEK_SET)

        # Reads meshes until the file ends
        while file.tell() < file_end:
            meshes.append(PRM(file))

    print("Imported {} ({} meshes)".format(filename, len(meshes)))

    for prm in meshes:
        me = import_mesh(prm, scene, filepath)

        if len(meshes) > 1:
            # Fake user if there are multiple LoDs so they're kept when saving
            me.use_fake_user = True

            # Append a quality suffix to meshes
            bname, number = me.name.rsplit(".", 1)
            me.name = "{}|q{}".format(bname, meshes.index(prm))

        # Assigns the highest quality mesh to an object and links it to the scn
        if meshes.index(prm) == 0:
            print("Creating Blender object for {}...".format(filename))
            ob = bpy.data.objects.new(filename, me)
            scene.objects.link(ob)
            scene.objects.active = ob

    return ob


def import_mesh(prm, scene, filepath, envlist=None):
    """
    Creates a mesh from an rvstruct object and returns it.
    """
    props = scene.revolt
    filename = os.path.basename(filepath)
    # Creates a new mesh and bmesh
    me = bpy.data.meshes.new(filename)
    bm = bmesh.new()

    # Adds the prm data to the bmesh
    add_rvmesh_to_bmesh(prm, bm, filepath, envlist)

    # Converts the bmesh back to a mesh and frees resources
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()

    return me


def add_rvmesh_to_bmesh(prm, bm, filepath, envlist=None):
    """
    Adds PRM data to an existing bmesh. Returns the resulting bmesh.
    """
    props = bpy.context.scene.revolt
    uv_layer = bm.loops.layers.uv.new("UVMap")
    tex_layer = bm.faces.layers.tex.new("UVMap")
    vc_layer = bm.loops.layers.color.new("Col")
    env_layer = bm.loops.layers.color.new("Env")
    env_alpha_layer = bm.faces.layers.float.new("EnvAlpha")
    va_layer = bm.loops.layers.color.new("Alpha")

    # This currently breaks UV unwrap reset, it is a Blender bug.
    # https://developer.blender.org/T52723
    texnum_layer = bm.faces.layers.int.new("Texture Number")
    type_layer = bm.faces.layers.int.new("Type")

    for vert in prm.vertices:
        position = to_blender_coord(vert.position.data)
        normal = to_blender_axis(vert.normal.data)

        # Creates vertices
        bm.verts.new(Vector((position[0], position[1], position[2])))

        # Ensures lookup table (potentially puts out an error otherwise)
        bm.verts.ensure_lookup_table()

    for poly in prm.polygons:
        is_quad = poly.type & FACE_QUAD
        num_loops = 4 if is_quad else 3
        indices = poly.vertex_indices

        if is_quad:
            verts = (bm.verts[indices[3]], bm.verts[indices[2]],
                     bm.verts[indices[1]], bm.verts[indices[0]])
            # Reversed list of UVs and colors
            uvs = reverse_quad(poly.uv)
            colors = reverse_quad(poly.colors)

        else:
            verts = (bm.verts[indices[2]], bm.verts[indices[1]],
                     bm.verts[indices[0]])
            # Reversed list of UVs and colors without the last element
            uvs = reverse_quad(poly.uv, tri=True)
            colors = reverse_quad(poly.colors, tri=True)

        # Tries to create a face and yells at you when the face already exists
        try:
            face = bm.faces.new(verts)
        except Exception as e:
            print(e)
            continue  # Skips this face

        # Assigns the texture to the face
        if poly.texture >= 0:
            texture_path = get_texture_path(filepath, poly.texture)
            if not texture_path in common.TEXTURES.keys():
                img = img_in.import_file(texture_path)
                face[tex_layer].image = img
                common.TEXTURES[texture_path] = img
            else:
                face[tex_layer].image = common.TEXTURES[texture_path]

        # Assigns the face properties (bit field, one int per face)
        face[type_layer] = poly.type
        face[texnum_layer] = poly.texture

        # Assigns env alpha to face. Colors are on a vcol layer
        if envlist and (poly.type & FACE_ENV):
            env_col_alpha = envlist[props.envidx].alpha
            face[env_alpha_layer] = float(env_col_alpha) / 255

        # Assigns the UV mapping, colors and alpha
        for l in range(num_loops):
            # Converts the colors to float (req. by Blender)
            alpha = float(colors[l].alpha) / 255
            color = [float(c) / 255 for c in colors[l].color]
            if envlist and (poly.type & FACE_ENV):
                env_col = [float(c) / 255 for c in envlist[props.envidx].color]
                face.loops[l][env_layer] = env_col

            face.loops[l][uv_layer].uv = (uvs[l].u, 1 - uvs[l].v)
            face.loops[l][vc_layer] = Color(color)
            face.loops[l][va_layer] = Color((alpha, alpha, alpha))

        # Enables smooth shading for that face
        face.smooth = True
        if envlist and (poly.type & FACE_ENV):
            props.envidx += 1
