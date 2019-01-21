"""
Name:    taz_in
Purpose: Imports Re-Volt level track zone files (.taz)

Description:
Zone files contain numbered boxes to identify tracks space.

""" 
import bpy
import os
from . import common
from . import rvstruct

from .rvstruct import TrackZones
from .common import *

def import_file(filepath, scene):
    """
    Imports a .taz file and links it to the scene as a Blender object.
    """
    with open(filepath, 'rb') as file:
        filename = os.path.basename(filepath)
        tzones = TrackZones(file)
    
    zones = tzones.zones
    
    if not bpy.data.groups.get('TRACK_ZONES'):
        bpy.ops.group.create(name="TRACK_ZONES")
    
    # Create an cubes representing each zone
    for zone in zones:
        # Position and size
        loc = zone.pos.scale(SCALE)
        size = zone.size.scale(SCALE)
        # Rotation
        matrix = Matrix(zone.matrix.data)
        matrix.transpose()
        rot = matrix.to_euler("XZY")
        
        # Add to scene
        bpy.ops.mesh.primitive_cube_add(location=(loc[0],loc[2],-loc[1]))
        ob = bpy.context.object
        ob.name = "%d" % zone.id
        bpy.ops.object.group_link(group="TRACK_ZONES")
        ob.draw_type = 'WIRE'
        ob.show_x_ray = True
        ob.show_name = True
        bpy.ops.transform.resize(value=(size[0],size[2],size[1]))
        ob.rotation_mode = 'XYZ'
        ob.rotation_euler = (rot[0],rot[2],-rot[1])

        
