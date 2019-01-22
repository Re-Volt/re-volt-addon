"""
Name:    taz_out
Purpose: Exports Re-Volt level track zone files (.taz)

Description:
Zone files contain numbered boxes to identify tracks space.

"""


import os
import bpy
import mathutils

from . import (
    common,
    rvstruct,
)
from .common import *
from .rvstruct import TrackZones


def export_file(filepath, scene):
    # Collect all zones
    zones = TrackZones()
    
    # Find all boxes and add them as a zone
    for obj in bpy.data.groups['TRACK_ZONES'].objects:
        if not obj.revolt.is_track_zone:
            continue
        # Get a name of object and zone id from it
        zid = int(obj.name.split(".", 1)[0][1:])
        zones.append(zid, *coords_blend_to_rv(obj.location, obj.rotation_euler, obj.scale))
    
    # Exports all zones to the TAZ file
    with open(filepath, "wb") as file:
        zones.write(file)

def coords_blend_to_rv(location, rotation_euler = (0,0,0), scale = (1,1,1)):
    """
    This function takes blender's order coordinates parameters values and converts
    them to values ready for export
    """
    location = mathutils.Vector((location[0],-location[2],location[1])) * 1/SCALE
    rotation_euler = (rotation_euler[0], -rotation_euler[2], rotation_euler[1])
    rotation_matrix = mathutils.Euler(rotation_euler, 'XZY').to_matrix()
    rotation_matrix.transpose()
    scale = mathutils.Vector((scale[0],scale[2],scale[1])) * 1/SCALE
    return location, rotation_matrix, scale
