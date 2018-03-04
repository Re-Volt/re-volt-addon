"""
Name:    fin_in
Purpose: Imports Re-Volt instance files (.fin)

Description:
Imports Instance files.

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

from .rvstruct import Instances, Instance, Vector
from .common import *
from mathutils import Color


def export_file(filepath, scene):
    fin = Instances()

    # Gathers list of instance objects
    objs = [obj for obj in scene.objects if obj.revolt.is_instance]

    for obj in objs:
        instance = Instance()




