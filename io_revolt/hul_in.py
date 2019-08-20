"""
Name:    hul_in
Purpose: Imports hull collision files.

Description:


"""

if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)

import os
import subprocess
import re
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

    script_file = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_file)

    qhull_in = os.path.join(script_dir, "hull", "qhull_in.txt")
    qhull_out = os.path.join(script_dir, "hull", "qhull_out.txt")

    if os.name == "nt":
        qhull_exe = os.path.join(script_dir, "hull", "qhull.exe")
    else:
        qhull_exe = "qhull"

    filename = os.path.basename(filepath)

    for chull in hull.chulls:

        # If the bbox is not centered, center it and update the offset.
        # TODO: Add center() function and bbox + vector operator for BoundingBox.
        offset = rvstruct.Vector(data=(
                (chull.bbox.xlo + chull.bbox.xhi) / 2,
                (chull.bbox.ylo + chull.bbox.yhi) / 2,
                (chull.bbox.zlo + chull.bbox.zhi) / 2
            )
        )

        dprint("Fixing convex hull offset: {} {} {}".format(*offset))

        chull.bbox_offset += offset
        chull.bbox.xlo -= offset[0]
        chull.bbox.xhi -= offset[0]
        chull.bbox.ylo -= offset[1]
        chull.bbox.yhi -= offset[1]
        chull.bbox.zlo -= offset[2]
        chull.bbox.zhi -= offset[2]

        bm = bmesh.new()
        me = bpy.data.meshes.new(filename)
        with open(qhull_in, "w") as file:
            # TODO: Document this. I'm relying on what jig did here
            file.write("3 1\n")
            file.write("{} {} {}\n".format(*chull.bbox_offset))
            file.write("4\n")
            file.write("{}\n".format(len(chull.faces)))
            for face in chull.faces:
                file.write("{} {} {} {}\n".format(*face.normal, face.distance))

        subprocess.Popen([qhull_exe, "H", "Fp", "FN", "E0.0001", "TI", qhull_in, "TO", qhull_out]).wait()

        with open(qhull_out, "r") as file:
            if not file.readline(): # ignores first line
                continue

            num_verts = int(file.readline())

            for i in range(num_verts):
                bm.verts.new(to_blender_coord([float(s) for s in re.match("\\s*(\\S+)?\\s*(\\S+)?\\s*(\\S+)?", file.readline()).groups("0")]))

            bm.verts.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            num_faces = int(file.readline())
            for i in range(num_faces):
                face = [int(s) for s in re.findall("\\S+", file.readline())][:0:-1]
                if len(face) > 2:
                    bm.faces.new([bm.verts[i] for i in face])
                    continue

        os.remove(qhull_in)
        os.remove(qhull_out)

        me.materials.append(create_material("RVHull", COL_HULL, 0.3))

        # bm.normal_update()
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        ob = bpy.data.objects.new(filename, me)
        ob.show_transparent = True
        ob.show_wire = True
        ob.revolt.is_hull_convex = True
        scene.objects.link(ob)
        scene.objects.active = ob

    for sphere in hull.interior.spheres:
        create_sphere(scene, sphere.center, sphere.radius, filename)



def import_chull(chull, scene, filename):
    # Note: unused
    dprint("Importing convex hull...")

    me = bpy.data.meshes.new(filename)
    bm = bmesh.new()

    dprint("verts:", len(chull.vertices))
    dprint("edges:", len(chull.edges))
    dprint("faces:", len(chull.faces))

    for vert in chull.vertices:
        position = to_blender_coord(vert)
        dprint("vertex position:", position)

        # Creates vertices
        bm.verts.new(Vector((position[0], position[1], position[2])))

        bm.verts.ensure_lookup_table()

    for edge in chull.edges:
        e = bm.edges.new([bm.verts[edge[0]], bm.verts[edge[1]]])
        if e is None:
            dprint("could not create edge")
    for face in chull.faces:
        dprint("FACE-----------------")
        verts = []
        for vert in chull.vertices:
            if face.contains_vertex(vert):
                position = to_blender_coord(vert)
                # Creates vertices
                v = bm.verts.new(Vector((position[0], position[1], position[2])))
                verts.append(v)
        if len(verts) > 2:
            # bm.faces.append(bmesh.ops.contextual_create(bm, verts, 0, False)["faces"])
            bmesh.ops.contextual_create(bm, geom=verts, use_smooth=True)
            # bm.faces.new(verts)




    # Converts the bmesh back to a mesh and frees resources
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()

    ob = bpy.data.objects.new(filename, me)
    scene.objects.link(ob)
    scene.objects.active = ob


def create_sphere(scene, center, radius, filename):
    col = COL_SPHERE
    center = to_blender_coord(center)
    radius = to_blender_scale(radius)
    mname = "RVSphere"
    if mname not in bpy.data.meshes:
        me = bpy.data.meshes.new(mname)
        bm = bmesh.new()
        # Creates a box
        bmesh.ops.create_uvsphere(bm, diameter=1, u_segments= 16, v_segments=8, calc_uvs=True)
        bm.to_mesh(me)
        bm.free()
        # Creates a transparent material for the object
        me.materials.append(create_material(mname, col, 0))
        # Makes polygons smooth
        for poly in me.polygons:
            poly.use_smooth = True
    else:
        me = bpy.data.meshes[mname]

    # Links the object and sets position and scale
    ob = bpy.data.objects.new("{}_{}".format(mname, filename), me)
    scene.objects.link(ob)
    ob.location = center
    ob.scale = (radius, radius, radius)
    ob.draw_type = "SOLID"
    ob.revolt.is_hull_sphere = True
    return ob

def import_file(filepath, scene):
    return import_hull(filepath, scene)
