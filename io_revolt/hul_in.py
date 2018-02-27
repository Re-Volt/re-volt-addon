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
from mathutils import Color

def import_hull(filepath):
    with open(filepath, "rb") as fd:
        hull = Hull(fd)
    

def import_file(filepath, scene):
    return import_hull(filepath)
