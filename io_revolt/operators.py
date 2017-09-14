if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(properties)

import bpy
from . import common
from . import properties

from .common import *
from .properties import *

class ButtonSelectFaceProp(bpy.types.Operator):
    bl_idname = "faceprops.select"
    bl_label = "sel"
    prop = bpy.props.IntProperty()

    def execute(self, context):
        select_faces(context, self.prop)
        return{'FINISHED'}
