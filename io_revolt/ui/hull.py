import bpy
from ..common import *
from .. import tools

class RevoltHullPanel(bpy.types.Panel):
    bl_label = "Hulls"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Re-Volt"
    bl_options = {"DEFAULT_CLOSED"}

    # @classmethod
    # def poll(self, context):
    #     return context.object and len(context.selected_objects) >= 1 and context.object.type == "MESH"

    def draw_header(self, context):
        self.layout.label("", icon="BBOX")

    def draw(self, context):
        view = context.space_data
        obj = context.object
        props = context.scene.revolt
        layout = self.layout

        layout.operator("hull.generate")

    
class ButtonHullGenerate(bpy.types.Operator):
    bl_idname = "hull.generate"
    bl_label = "Generate Convex Hull"
    bl_description = (
        "yes"
    )

    def execute(self, context):
        tools.generate_chull(context)
        return{"FINISHED"}