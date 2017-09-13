"""
PRM
Meshes used for cars, game objects and track instances.
"""

# Reloads potentially changed modules on reload
if 'bpy' in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)

import os
import bpy
import bmesh
from mathutils import Color, Vector

from . import common
from . import rvstruct

# Makes global constants and helpers accessible
from .rvstruct import PRM
from .common import *

def import_file(filepath, scene):
    """
    Imports a .prm/.m file and links it to the scene as a Blender object.
    """
    filename = os.path.basename(filepath)

    # Imports the PRM file
    with open(filepath, 'rb') as file:
        prm = PRM(file)
        print("Imported {}".format(filename))

    print("Creating Blender object...")

    # Creates a new mesh and bmesh
    me = bpy.data.meshes.new(filename)
    bm = bmesh.new()
    bm.from_mesh(me)

    uv_layer = bm.loops.layers.uv.new("UVMap")
    vc_layer = bm.loops.layers.color.new("Col")
    va_layer = bm.loops.layers.color.new("Alpha")
    flag_layer = bm.faces.layers.int.new("Flags")

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
            continue

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

    # Links the object to the scene and sets it active
    ob = bpy.data.objects.new(filename, me)
    scene.objects.link(ob)
    scene.objects.active = ob
