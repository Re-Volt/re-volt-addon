"""
Panels for editing object and face properties.
"""

if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(properties)
    imp.reload(operators)

import bpy
from . import common
from . import operators
from . import properties

from .common import *
from .operators import *
from .properties import *

class RevoltObjectPanel(bpy.types.Panel):
    bl_label = "Re-Volt Object Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj.revolt.is_bcube:
            layout.label("BigCube Properties:")
            layout.prop(obj.revolt, "bcube_mesh_indices")

"""
Tool panel in the left sidebar of the viewport for performing
various operations
"""
class RevoltIOToolPanel(bpy.types.Panel):
    bl_label = "Import/Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Re-Volt"

    def draw(self, context):
        # i/o buttons
        props = context.scene.revolt
        fold_s = props.ui_fold_export_settings

        row = self.layout.row(align=True)
        row.operator(ImportRV.bl_idname, text="Import", icon="IMPORT")
        row.operator(ExportRV.bl_idname, text="Export", icon="EXPORT")
        row = self.layout.row(align=True)
        row.prop(
            props,
            "ui_fold_export_settings",
            icon = "TRIA_DOWN" if not fold_s else "TRIA_RIGHT",
            text = "Show Settings" if fold_s else "Hide Settings"
        )
        if not fold_s:
            box = self.layout.box()
            box.label("Export")
            box.prop(props, "triangulate_ngons")
            box.prop(props, "use_tex_num")
            box.prop(props, "apply_scale")
            box.prop(props, "apply_rotation")

            box = self.layout.box()
            box.label("Import World (.w)")
            box.prop(props, "w_parent_meshes")
            box.prop(props, "w_import_bound_boxes")
            if props.w_import_bound_boxes:
                box.prop(props, "w_bound_box_layers")
            box.prop(props, "w_import_bound_balls")
            if props.w_import_bound_balls:
                box.prop(props, "w_bound_ball_layers")
            box.prop(props, "w_import_big_cubes")
            if props.w_import_big_cubes:
                box.prop(props, "w_big_cube_layers")

class RevoltFacePropertiesPanel(bpy.types.Panel):
    bl_label = "Face Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_category = "Re-Volt"

    selection = None
    selected_face_count = None

    def draw(self, context):
        obj = context.object
        mesh = obj.data
        bm = dic.setdefault(obj.name, bmesh.from_edit_mesh(obj.data))
        flags = (bm.faces.layers.int.get("Type")
                 or bm.faces.layers.int.new("Type"))
        if (self.selected_face_count is None
            or self.selected_face_count != mesh.total_face_sel):
            self.selected_face_count = mesh.total_face_sel
            self.selection = [face for face in bm.faces if face.select]

        # count the number of faces the flags are set for
        count = [0] * len(FACE_PROPS)
        # if len(self.selection) > 1:
        for face in self.selection:
            for x in range(len(FACE_PROPS)):
                if face[flags] & FACE_PROPS[x]:
                    count[x] += 1

        # self.layout.prop(context.object.data.revolt, "face_material",
        #     text="Material".format(""))
        row  = self.layout.row()
        col = row.column(align=True)
        col.prop(context.object.data.revolt, "face_double_sided",
            text="{}: Double sided".format(count[1]))
        col.prop(context.object.data.revolt, "face_translucent",
            text="{}: Translucent".format(count[2]))
        col.prop(context.object.data.revolt, "face_mirror",
            text="{}: Mirror".format(count[3]))
        col.prop(context.object.data.revolt, "face_additive",
            text="{}: Additive blending".format(count[4]))
        col.prop(context.object.data.revolt, "face_texture_animation",
            text="{}: Texture animation".format(count[5]))
        col.prop(context.object.data.revolt, "face_no_envmapping",
            text="{}: No EnvMap".format(count[6]))
        if context.object.data.revolt.face_envmapping:
            split = col.split(percentage=.7)
            scol = split.column(align=True)
            scol.prop(context.object.data.revolt, "face_envmapping",
            text="{}: EnvMap".format(count[7]))
            scol = split.column(align=True)
            scol.prop(context.object.data.revolt, "face_env", text="")
        else:
            col.prop(context.object.data.revolt, "face_envmapping",
            text="{}: EnvMap".format(count[7]))

        col.prop(context.object.data.revolt, "face_cloth",
            text="{}: Cloth effect".format(count[8]))
        col.prop(context.object.data.revolt, "face_skip",
            text="{}: Do not export".format(count[9]))
        col = row.column(align=True)
        col.scale_x = 0.15
        col.operator("faceprops.select", text="sel").prop = FACE_DOUBLE
        col.operator("faceprops.select", text="sel").prop = FACE_TRANSLUCENT
        col.operator("faceprops.select", text="sel").prop = FACE_MIRROR
        col.operator("faceprops.select", text="sel").prop = FACE_TRANSL_TYPE
        col.operator("faceprops.select", text="sel").prop = FACE_TEXANIM
        col.operator("faceprops.select", text="sel").prop = FACE_NOENV
        col.operator("faceprops.select", text="sel").prop = FACE_ENV
        col.operator("faceprops.select", text="sel").prop = FACE_CLOTH
        col.operator("faceprops.select", text="sel").prop = FACE_SKIP

        row = self.layout.row()
        if len(self.selection) > 1:
            if context.object.data.revolt.face_texture == -2:
                row.prop(context.object.data.revolt, "face_texture",
                    text="Texture (different numbers)")
            else:
                row.prop(context.object.data.revolt, "face_texture",
                    text="Texture (set for all)")
        elif len(self.selection) == 0:
            row.prop(context.object.data.revolt, "face_texture",
                text="Texture (no selection)")
        else:
            row.prop(context.object.data.revolt, "face_texture",
                text="Texture".format(""))
        row.active = context.object.data.revolt.face_texture != -3

"""
Panel for setting vertex colors in Edit Mode.
If there is no vertex color layer, the user will be prompted to create one.
It includes buttons for setting vertex colors in different shades of grey and
a custom color which is chosen with a color picker.
"""
class RevoltVertexPanel(bpy.types.Panel):
    bl_label = "Vertex Colors"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_category = "Re-Volt"

    selection = None
    selected_face_count = None

    def draw(self, context):
        obj = context.object
        row = self.layout.row(align=True)

        # warn if texture mode is not enabled
        widget_texture_mode(self)

        bm = dic.setdefault(obj.name, bmesh.from_edit_mesh(obj.data))
        vc_layer = bm.loops.layers.color.get("Col")

        if widget_vertex_color_channel(self, obj):
            pass # there is not vertex color channel and the panel can't be used

        else:
            box = self.layout.box()
            row = box.row()
            row.template_color_picker(context.scene.revolt,
                                      "vertex_color_picker",
                                      value_slider=True)
            row = box.row(align=True)
            row.prop(context.scene.revolt, "vertex_color_picker", text = '')
            row.operator("vertexcolor.set").number=-1
            row = self.layout.row(align=True)
            row.operator("vertexcolor.set", text="Grey 50%").number=50
            row = self.layout.row()
            col = row.column(align=True)
            col.alignment = 'EXPAND'
            col.operator("vertexcolor.set", text="Grey 45%").number=45
            col.operator("vertexcolor.set", text="Grey 40%").number=40
            col.operator("vertexcolor.set", text="Grey 35%").number=35
            col.operator("vertexcolor.set", text="Grey 30%").number=30
            col.operator("vertexcolor.set", text="Grey 20%").number=20
            col.operator("vertexcolor.set", text="Grey 10%").number=10
            col.operator("vertexcolor.set", text="Black").number=0
            col = row.column(align=True)
            col.alignment = 'EXPAND'
            col.operator("vertexcolor.set", text="Grey 55%").number=55
            col.operator("vertexcolor.set", text="Grey 60%").number=60
            col.operator("vertexcolor.set", text="Grey 65%").number=65
            col.operator("vertexcolor.set", text="Grey 70%").number=70
            col.operator("vertexcolor.set", text="Grey 80%").number=80
            col.operator("vertexcolor.set", text="Grey 90%").number=90
            col.operator("vertexcolor.set", text="White").number=100


class RevoltLightPanel(bpy.types.Panel):
    bl_label = "Light and Shadow"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Re-Volt"

    @classmethod
    def poll(self, context):
        return (context.scene.objects.active is not None)

    def draw(self, context):
        view = context.space_data
        obj = context.object
        # warn if texture mode is not enabled
        widget_texture_mode(self)

        if obj and obj.select:
            # Cheks if the object has a vertex color layer
            if widget_vertex_color_channel(self, obj):
                pass
            else:
                # light orientation selection
                box = self.layout.box()
                box.label(text="Shade Object")
                row = box.row()
                row.prop(context.object.revolt,
                         "light_orientation",
                         text="Orientation")
                if obj.revolt.light_orientation == "X":
                    dirs = ["Left", "Right"]
                if obj.revolt.light_orientation == "Y":
                    dirs = ["Front", "Back"]
                if obj.revolt.light_orientation == "Z":
                    dirs = ["Top", "Bottom"]
                # headings
                row = box.row()
                row.label(text="Direction")
                row.label(text="Light")
                row.label(text="Intensity")
                # settings for the first light
                row = box.row(align=True)
                row.label(text=dirs[0])
                row.prop(context.object.revolt, "light1", text="")
                row.prop(context.object.revolt, "light_intensity1", text="")
                # settings for the second light
                row = box.row(align=True)
                row.label(text=dirs[1])
                row.prop(context.object.revolt, "light2", text="")
                row.prop(context.object.revolt, "light_intensity2", text="")
                # bake button
                row = box.row()
                row.operator("lighttools.bakevertex",
                             text="Generate Shading",
                             icon="LIGHTPAINT")

            box = self.layout.box()
            box.label(text="Generate Shadow Texture")
            row = box.row()
            row.prop(context.object.revolt, "shadow_method")
            col = box.column(align=True)
            col.prop(context.object.revolt, "shadow_quality")
            col.prop(context.object.revolt, "shadow_softness")
            col.prop(context.object.revolt, "shadow_resolution")
            row = box.row()
            row.operator("lighttools.bakeshadow",
                         text="Generate Shadow",
                         icon="LAMP_SPOT")
            row = box.row()
            row.prop(context.object.revolt, "shadow_table", text="Table")


"""
Widgets are little panel snippets that generally warn users if something isn't
set up correctly to use a feature. They return true if something isn't right.
They return false if everything is alright.
"""

def widget_texture_mode(self):
    if not texture_mode_enabled():
        box = self.layout.box()
        box.label(text="Texture Mode is not enabled.", icon='INFO')
        row = box.row()
        row.operator("helpers.enable_texture_mode",
                     text="Enable Texture Mode",
                     icon="POTATO")
        return True
    return False

def widget_vertex_color_channel(self, obj):
    if not obj.data.vertex_colors:
        box = self.layout.box()
        box.label(text="No Vertex Color Layer.", icon='INFO')
        row = box.row()
        row.operator("mesh.vertex_color_add", icon='PLUS',
                     text="Create Vertex Color Layer")
        return True
    return False
