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


    # Converts the bmesh back to a mesh and frees resources
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()

    ob = bpy.data.objects.new(filename, me)
    scene.objects.link(ob)
    scene.objects.active = ob


def import_file(filepath, scene):
    return import_hull(filepath, scene)
