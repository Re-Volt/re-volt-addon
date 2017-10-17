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
from math import ceil
from mathutils import Color, Matrix
from . import common
from . import rvstruct

from .common import *
from .rvstruct import (
    BoundingBox,
    LookupGrid,
    LookupList,
    NCP,
    Plane,
    Polyhedron,
    Vector
)


def export_file(filepath, scene):
    print("Exporting NCP to {}...".format(filepath))
    props = scene.revolt

    # Collects objects for export
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

    if objs == []:
        msg_box("No suitable objects in scene.")
        return

    # Creates a mesh for the entire scene
    bm = objects_to_bmesh(objs)

    if props.triangulate_ngons:
        num_ngons = triangulate_ngons(bm)
        if scene.revolt.triangulate_ngons > 0:
            print("Triangulated {} n-gons".format(num_ngons))

    # Material and type layers. The preview layer will be ignored.
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

            poly.planes.append(Plane(n=Vector(data=pnormal), d=distance))

        # Writes remaining empty planes
        for i in range(4 - vcount):
            poly.planes.append(Plane())

        # Creates a bbox and adds the poly to the ncp
        poly.bbox = BoundingBox(data=rvbbox_from_verts(verts))
        ncp.polyhedra.append(poly)

    # Sets length of polyhedron list
    ncp.polyhedron_count = len(ncp.polyhedra)

    grid = LookupGrid()
    grid.size = NCP_GRID_SIZE

    bbox = BoundingBox(data=(
        min([poly.bbox.xlo for poly in ncp.polyhedra]),
        max([poly.bbox.xhi for poly in ncp.polyhedra]),
        0,
        0,
        min([poly.bbox.zlo for poly in ncp.polyhedra]),
        max([poly.bbox.zhi for poly in ncp.polyhedra]))
    )

    grid.xsize = ceil((bbox.xhi - bbox.xlo) / grid.size)
    grid.zsize = ceil((bbox.zhi - bbox.zlo) / grid.size)

    grid.x0 = (bbox.xlo + bbox.xhi - grid.xsize * grid.size) / 2
    grid.z0 = (bbox.zlo + bbox.zhi - grid.zsize * grid.size) / 2

    for z in range(grid.zsize):
        zlo = grid.z0 + z * grid.size - 150
        zhi = grid.z0 + (z + 1) * grid.size + 150

        for x in range(grid.xsize):
            xlo = grid.x0 + x * grid.size - 150
            xhi = grid.x0 + (x + 1) * grid.size + 150

            lookup = LookupList()
            for i, poly in enumerate(ncp.polyhedra):
                if (poly.bbox.zhi > zlo and poly.bbox.zlo < zhi and
                        poly.bbox.xhi > xlo and poly.bbox.xlo < xhi):
                    lookup.polyhedron_idcs.append(i)

            lookup.length = len(lookup.polyhedron_idcs)
            grid.lists.append(lookup)
    ncp.lookup_grid = grid

    # Writes the NCP to file
    with open(filepath, "wb") as f:
        ncp.write(f)

    # Frees the bmesh
    bm.free()
