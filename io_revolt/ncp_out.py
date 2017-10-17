"""
PRM EXPORT
Meshes used for cars, game objects and track instances.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)

import os
import bpy
import bmesh
from mathutils import Color, Matrix
from . import common
from . import rvstruct

from .common import *
from .rvstruct import BoundingBox, NCP, Plane, Polyhedron, Vector


def export_file(filepath, scene):
    print("Exporting NCP to {}...".format(filepath))
    props = scene.revolt

    # Collect objects for exporting
    objs = []
    for obj in scene.objects:
        conditions = (
            obj.data and
            obj.type == "MESH" and
            not obj.revolt.is_cube and
            not obj.revolt.is_bcube and
            not obj.revolt.is_bbox and
            not obj.revolt.ignore_ncp
        )
        if conditions:
            objs.append(obj)

    # Creates a mesh for the entire scene
    bm = objects_to_bmesh(objs)

    if props.triangulate_ngons:
        num_ngons = triangulate_ngons(bm)
        if scene.revolt.triangulate_ngons > 0:
            print("Triangulated {} n-gons".format(num_ngons))

    material_layer = (bm.faces.layers.int.get("Material") or
                      bm.faces.layers.int.new("Material"))
    type_layer = (bm.faces.layers.int.get("NCPType") or
                  bm.faces.layers.int.new("NCPType"))

    ncp = NCP()

    for face in bm.faces:
        poly = Polyhedron()

        # Doesn't export if material is NONE
        if face[material_layer] < 0:
            continue

        # Sets polyhedron properties
        poly.material = face[material_layer]
        poly.type = face[type_layer]

        verts = face.verts

        # Determines normal and distance for main plane
        normal = Vector(data=to_revolt_axis(face.normal))
        normal.normalize()

        vec = Vector(data=to_revolt_coord(verts[0].co))
        distance = -normal.dot(vec)
        # distance = -vec.x * normal.x - vec.y * normal.y - vec.z * normal.z

        # Creates main plane
        poly.planes.append(Plane(n=normal, d=distance))

        if len(face.verts) == 4:
            # Sets the quad flag because the poly has 4 vertices
            poly.type |= NCP_QUAD

        # Writes the cutting planes
        vcount = len(verts[:4])
        for i in range(vcount - 1, -1, -1):
            vec0 = Vector(data=to_revolt_coord(verts[i].co))
            vec1 = Vector(data=to_revolt_coord(verts[(i + 1) % vcount].co))

            pnormal = normal.cross(vec0 - vec1)
            pnormal.normalize()
            distance = -pnormal.dot(vec0)
            # distance = -vec0.x * pnormal.x - vec0.y * pnormal.y - vec0.z * pnormal.z

            poly.planes.append(Plane(n=Vector(data=pnormal), d=distance))

        # Writes remaining empty planes
        for i in range(4 - vcount):
            poly.planes.append(Plane())

        # Creates a bbox and adds the poly to the ncp
        poly.bbox = BoundingBox(data=rvbbox_from_verts(verts))
        ncp.polyhedra.append(poly)

    # Sets length of polyhedron list
    ncp.polyhedron_count = len(ncp.polyhedra)

    # Writes the NCP to file
    with open(filepath, "wb") as f:
        ncp.write(f)


    # me = bpy.data.meshes.new("test")
    # bm.to_mesh(me)
    # ob = bpy.data.objects.new("testoutput", me)
    # scene.objects.link(ob)
    # scene.objects.active = ob

    # Frees the bmesh
    bm.free()
