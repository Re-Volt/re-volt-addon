"""
PRM
Meshes used for cars, game objects and track instances.
"""

# Reloads potentially changed modules on reload (F8 in Blender)
if 'bpy' in locals():
    import imp
    imp.reload(common)
    imp.reload(rvfiles)
    imp.reload(rvstruct)
    imp.reload(img_in)

import os
import bpy
import bmesh
from mathutils import Color, Vector

from . import common
from . import rvfiles
from . import rvstruct
from . import img_in

# Makes classes, variables and functions more accessible
from .rvstruct import PRM
from .common import *

def import_file(filepath, scene):
    """
    Imports a .prm/.m file and links it to the scene as a Blender object.
    """
    # Imports the PRM file
    meshes = []

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
            bname, number = me.name.split(".")
            me.name = "{}|q{}".format(bname, meshes.index(prm))

        # Assigns the highest quality mesh to an object and links it to the scn
        if meshes.index(prm) == 0:
            print("Creating Blender object for{}...".format(filename))
            ob = bpy.data.objects.new(filename, me)
            scene.objects.link(ob)
            scene.objects.active = ob

def import_mesh(prm, scene, filepath):
    """
    Creates a mesh from an rvstruct object and returns it.
    """
    filename = os.path.basename(filepath)
    # Creates a new mesh and bmesh
    me = bpy.data.meshes.new(filename)
    bm = bmesh.new()
    bm.from_mesh(me)

    uv_layer = bm.loops.layers.uv.new("UVMap")
    tex_layer = bm.faces.layers.tex.new("UVMap")
    vc_layer = bm.loops.layers.color.new("Col")
    va_layer = bm.loops.layers.color.new("Alpha")
    type_layer = bm.faces.layers.int.new("Type")

    for vert in prm.vertices:
        position = to_blender_axis(vert.position.data)
        normal = to_blender_axis(vert.normal.data)

        # Creates vertices
        bm.verts.new(Vector((position[0], position[1], position[2])))
        # vert.normal = Vector(normal) # Blender doesn't use vertex normals

        # Ensures lookup table (puts out an error otherwise)
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
            continue # Skips this face

        # Assigns the texture to the face
        texture_path = rvfiles.get_texture_path(filepath, poly.texture)
        img = img_in.import_file(texture_path)
        face[tex_layer].image = img

        # Assigns the UV mapping, colors and alpha
        for l in range(num_loops):
            # Converts the colors to float (req. by Blender)
            alpha = float(colors[l].alpha) / 255
            color = [float(c)/255 for c in colors[l].color]

            face.loops[l][uv_layer].uv = (uvs[l].u, 1-uvs[l].v)
            face.loops[l][vc_layer] = Color(color)
            face.loops[l][va_layer] = Color((alpha, alpha, alpha))

    # Converts the bmesh back to a mesh and frees resources
    # bm.normal_update() # not needed?
    bm.to_mesh(me)
    bm.free()

    return me
