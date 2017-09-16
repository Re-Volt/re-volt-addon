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
    for rvmesh in meshes:
        me = import_mesh(rvmesh, scene, filepath)
        ob = bpy.data.objects.new(filename, me)
        scene.objects.link(ob)
        scene.objects.active = ob

        create_bound_box(rvmesh.bbox, )

def create_bound_box(scene, bbox, center):
    # Creates a new mesh and bmesh
    me = bpy.data.meshes.new(filename)
    bm = bmesh.new()
    bm.from_mesh(me)

    coords =
    bm.verts.new(bbox.xlo, )
