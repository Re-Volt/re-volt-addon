"""
PRM
Meshes used for cars, game objects and track instances.
"""

# Reloads potentially changed modules on reload
if 'bpy' in locals():
    import imp
    imp.reload(common)

import os
import bpy
import bmesh
from mathutils import Vector

from . import common
from .rvstruct import PRM

# Makes global constants and helpers accessible
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
            # Reversed list of UVs
            uvs = poly.uv[::-1]
        else:
            verts = (bm.verts[indices[2]], bm.verts[indices[1]],
                     bm.verts[indices[0]])
            # Reversed list of UVs without the last element
            uvs = poly.uv[2::-1]

        # Tries to create a face and yells at you when the face already exists
        try:
            face = bm.faces.new(verts)
        except Exception as e:
            print(e)
            continue

        # Assigns the UV mapping
        for l in range(num_loops):
            face.loops[l][uv_layer].uv = (uvs[l].u, 1-uvs[l].v)


    # Converts the bmesh back to a mesh and frees resources
    # bm.normal_update() # not needed?
    bm.to_mesh(me)
    bm.free()

    # Links the object to the scene and sets it active
    ob = bpy.data.objects.new(filename, me)
    scene.objects.link(ob)
    scene.objects.active = ob
