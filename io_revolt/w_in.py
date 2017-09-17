"""
WORLD IMPORT
Imports level files which include meshes and other structures for optimization.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)
    imp.reload(img_in)
    imp.reload(prm_in)

import os
import bpy
import bmesh
from mathutils import Color, Vector
from . import common
from . import rvstruct
from . import img_in
from . import prm_in

from .rvstruct import World
from .common import *
from .prm_in import import_mesh

def import_file(filepath, scene):
    """
    Imports a .w file and links it to the scene as a Blender object.
    """

    props = scene.revolt

    with open(filepath, 'rb') as file:
        filename = os.path.basename(filepath)
        world = World(file)

    meshes = world.meshes
    print("Imported {} ({} meshes)".format(filename, len(meshes)))

    # Creates an empty object to parent meshes to if enabled in settings
    if props.w_parent_meshes:
        main_w = bpy.data.objects.new(bpy.path.basename(filename), None)
        bpy.context.scene.objects.link(main_w)
    for rvmesh in meshes:
        # Creates a mesh from rv data and links it to the scene as an object
        me = import_mesh(rvmesh, scene, filepath)
        ob = bpy.data.objects.new(filename, me)
        scene.objects.link(ob)
        scene.objects.active = ob

        # Parents the mesh to the main .w object
        if props.w_parent_meshes:
            ob.parent = main_w

        # Imports bound box for each mesh if enabled in settings
        if props.w_import_bound_boxes:
            bbox = create_bound_box(scene, rvmesh.bbox, filepath)
            bbox.parent = ob

def create_bound_box(scene, bbox, filepath):
    filename = os.path.basename(filepath)
    # Creates a new mesh and bmesh
    me = bpy.data.meshes.new(filename)
    bm = bmesh.new()
    bm.from_mesh(me)

    coords = [
        to_blender_coord((bbox.xlo, bbox.ylo, bbox.zhi)),
        to_blender_coord((bbox.xhi, bbox.ylo, bbox.zhi)),
        to_blender_coord((bbox.xlo, bbox.yhi, bbox.zhi)),
        to_blender_coord((bbox.xhi, bbox.yhi, bbox.zhi)),
        to_blender_coord((bbox.xlo, bbox.ylo, bbox.zlo)),
        to_blender_coord((bbox.xhi, bbox.ylo, bbox.zlo)),
        to_blender_coord((bbox.xlo, bbox.yhi, bbox.zlo)),
        to_blender_coord((bbox.xhi, bbox.yhi, bbox.zlo))
    ]
    for co in coords:
        bm.verts.new(co)
    bm.verts.ensure_lookup_table()

    faces = [
        # Front
        (bm.verts[0], bm.verts[1], bm.verts[3], bm.verts[2]),
        # Back
        (bm.verts[6], bm.verts[7], bm.verts[5], bm.verts[4]),
        # Left
        (bm.verts[0], bm.verts[2], bm.verts[6], bm.verts[4]),
        # Right
        (bm.verts[5], bm.verts[7], bm.verts[3], bm.verts[1]),
        # Top
        (bm.verts[4], bm.verts[5], bm.verts[1], bm.verts[0]),
        # Bottom
        (bm.verts[2], bm.verts[3], bm.verts[7], bm.verts[6])
    ]

    # Creates faces of the bbox
    for f in faces:
        bm.faces.new(f)

    bm.normal_update()
    bm.to_mesh(me)
    ob = bpy.data.objects.new("bbox_{}".format(filename), me)
    scene.objects.link(ob)
    scene.objects.active = ob
    return ob
