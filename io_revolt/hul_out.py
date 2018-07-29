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


def export_hull(filepath, scene):

    objs = [obj for obj in sce.objects if obj.revolt.is_hull_convex]

    hull = rvstruct.Hull()

    hull.chull_count = len(objs)

    for obj in objs:

        chull = rvstruct.ConvexHull()
    
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        # Applies rotation and scale
        apply_trs(obj, bm, transform=False)

        for face in bm.faces:

            plane = rvstruct.Plane()

            bm.faces.ensure_lookup_table()

            normal = rvstruct.Vector(data=to_revolt_axis(face.normal))
            normal.normalize()
            normal = normal * -1

            vec = rvstruct.Vector(data=to_revolt_coord(face.verts[0].co))
            distance = -normal.dot(vec)

            plane.normal = normal
            plane.distance = distance

            chull.faces.append(plane)
            chull.face_count += 1
            rim.num_mirror_planes += 1

        chull.bbox = rvstruct.BoundingBox(data=rvbbox_from_verts(bm.verts))

        bm.free()




def export_file(filepath, scene):
    return export_hull(filepath, scene)
