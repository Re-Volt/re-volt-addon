"""
WORLD EXPORT
Level files that contain optimized meshes (.w).
"""
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)
    imp.reload(img_in)
    imp.reload(prm_out)

import os
import bpy
import bmesh
from mathutils import Color, Vector
from . import common
from . import rvstruct
from . import img_in
from . import prm_out

from .common import *
from .prm_out import export_mesh


def export_file(filepath, scene):
    # Creates an empty world object to put the scene into
    world = rvstruct.World()

    objs = [obj for obj in scene.objects if obj.data]

    # Goes through all objects from the scene and exports them to PRM/Mesh
    for obj in objs:
        me = obj.data
        print("Exporting mesh for {}".format(obj.name))
        mesh = export_mesh(me, obj, scene, filepath, world=world)
        world.meshes.append(mesh)
        world.mesh_count = len(world.meshes)

    # Writes the world to a file
    with open(filepath, "wb") as file:
        world.write(file)
