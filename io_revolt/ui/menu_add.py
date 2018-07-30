import bpy
from ..common import *


def menu_func_add(self, context):
    self.layout.separator()
    self.layout.menu(INFO_MT_revolt_add.bl_idname, icon = "OBJECT_DATA")


class INFO_MT_revolt_add(bpy.types.Menu):
    bl_idname = "INFO_MT_revolt_add"
    bl_label = "Re-Volt"
    
    def draw(self, context):
        self.layout.operator("object.add_hull_sphere", icon="MATSPHERE")


class OBJECT_OT_add_revolt_hull_sphere(bpy.types.Operator):
    bl_idname = "object.add_hull_sphere"
    bl_label = "Hull Sphere"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        from ..hul_in import create_sphere
        obj = create_sphere(context.scene, (0, 0, 0), to_revolt_scale(0.1), "Hull Sphere")
        obj.location = bpy.context.scene.cursor_location
        obj.select = True
        bpy.context.scene.objects.active = obj

        return {'FINISHED'}