"""
Name:    hul_in
Purpose: Imports hull collision files.

Description:


"""

if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)

import bpy
import bmesh
import mathutils

from . import common
from . import rvstruct
from . import prm_in

from .rvstruct import Hull
from .common import *
from mathutils import Color, Vector


def get_plane(x, y, z):
    vector1 = [x[1] - x[0], y[1] - y[0], z[1] - z[0]]
    vector2 = [x[2] - x[0], y[2] - y[0], z[2] - z[0]]

    normal = vector1.cross(vector2)

    distance = - (normal[0] * x[0] + normal[1] * y[0] + normal[2] * z[0])


def import_hull(filepath, scene):
    # Reads the full file
    with open(filepath, "rb") as fd:
        hull = Hull(fd)

    # Imports the convex hulls
    for chull in hull.chulls:
        import_chull(chull, scene, filepath.rsplit(os.sep, 1)[1])


def import_chull(chull, scene, filename):
    dprint("Importing convex hull...")

    me = bpy.data.meshes.new(filename)
    bm = bmesh.new()

    for vert in chull.vertices:
        position = to_blender_coord(vert)

        # Creates vertices
        bm.verts.new(Vector((position[0], position[1], position[2])))

        bm.verts.ensure_lookup_table()

    for edge in chull.edges:
        bm.edges.new([bm.verts[edge[0]], bm.verts[edge[1]]])

    for face in chull.faces:
        print("FACE-----------------")
        verts = []
        for vert in chull.vertices:
            if face.contains_vertex(vert):
                position = to_blender_coord(vert)
                # Creates vertices
                v = bm.verts.new(Vector((position[0], position[1], position[2])))
                verts.append(v)
        if len(verts) > 2:
            bm.faces.new(verts)



    # Converts the bmesh back to a mesh and frees resources
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()

    ob = bpy.data.objects.new(filename, me)
    scene.objects.link(ob)
    scene.objects.active = ob


def import_file(filepath, scene):
    return import_hull(filepath, scene)
