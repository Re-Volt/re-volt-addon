import bpy

from . import common

if "bpy" in locals():
    import imp
    imp.reload(common)

from .common import *

class ButtonSelectFaceProp(bpy.types.Operator):
    bl_idname = "faceprops.select"
    bl_label = "sel"
    prop = bpy.props.IntProperty()

    def execute(self, context):
        select_faces(context, self.prop)
        return{'FINISHED'}
