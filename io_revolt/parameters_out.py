"""
Name:    parameters_out
Purpose: Exporting cars parameters useful for the parameters.txt files

Description:
Prints most valuable car parameters into clipboard.

"""

if "bpy" in locals():
    import imp
    imp.reload(common)

import os
import bpy
from bpy import context
from . import common

from .common import * 

def export_file(filepath = None, scene = None):
    """
    This function builds a parameters string for wheels and antenna locations 
    and puts it into clipboard.
    """
    params = ""
    # Proceed if there is main car body
    if "body.prm" in bpy.data.objects:
        body = bpy.data.objects["body.prm"]
        for child in body.children:
            location = to_revolt_coord(child.location)
            if "wheel" in child.name:
                w_num = 0
                if "wheelfr.prm" in child.name:
                    w_num = 1
                elif "wheelbl.prm" in child.name:
                    w_num = 2
                elif "wheelbr.prm" in child.name:
                    w_num = 3
                params += "WHEEL %d {\n" % w_num
                params += "Offset1\t %f %f %f \n}\n" % location
            elif "aerial" in child.name:
                params += "AERIAL {\n"
                params += "Offset\t %f %f %f \n}\n" % location
    
    bpy.context.window_manager.clipboard = params
