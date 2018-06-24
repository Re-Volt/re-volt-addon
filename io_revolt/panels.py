"""
Name:    panels
Purpose: User interface of the add-on

Description:
Contains all classes for the add-on's user interface which can be found
in the toolbar and in the object properties editor.

"""


import bpy
from .common import *

class RevoltObjectPanel(bpy.types.Panel):
    bl_label = "Re-Volt Object Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"HIDE_HEADER"}


    def draw(self, context):
        layout = self.layout
        obj = context.object
        objprops = obj.revolt

        layout.label("Re-Volt Properties")

        # NCP properties
        box = layout.box()
        box.label("NCP Properties:")
        row = box.row()
        row.prop(objprops, "ignore_ncp")

        # Debug properties
        if objprops.is_bcube:
            box = layout.box()
            box.label("BigCube Properties:")
            row = box.row()
            row.prop(objprops, "bcube_mesh_indices")
        
        # Instance properties
        box = layout.box()
        box.label("Instance Properties:")
        box.prop(objprops, "is_instance")

        if objprops.is_instance:
            row = box.row(align=True)
            row.prop(context.object.revolt, "fin_model_rgb", text="Model Color")
            row.prop(context.object.revolt, "fin_col", text="")
            row = box.row(align=True)
            row.prop(context.object.revolt, "fin_env", text="EnvColor")
            row.prop(context.object.revolt, "fin_envcol", text="")
            box.prop(context.object.revolt, "fin_hide")
            box.prop(context.object.revolt, "fin_no_mirror")
            box.prop(context.object.revolt, "fin_no_lights")
            box.prop(context.object.revolt, "fin_no_cam_coll")
            box.prop(context.object.revolt, "fin_no_obj_coll")
            box.prop(context.object.revolt, "fin_priority")
            box.prop(context.object.revolt, "fin_lod_bias")


class RevoltScenePanel(bpy.types.Panel):
    """ Panel for .w properties """
    bl_label = "Re-Volt .w Properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"HIDE_HEADER"}


    def draw(self, context):
        props = context.scene.revolt
        layout = self.layout

        layout.label("Re-Volt Properties")

        layout.prop(props, "texture_animations")


class EditModeHeader(bpy.types.Panel):
    """
    Fixes the tab at the top in edit mode.
    """
    bl_label = "Edit Mode Header"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_category = "Re-Volt"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        props = context.scene.revolt
        row  = self.layout.row()
        # PRM/NCP toggle
        row.prop(props, "face_edit_mode", expand=True)

class RevoltIOToolPanel(bpy.types.Panel):
    """
    Tool panel in the left sidebar of the viewport for performing
    various operations
    """
    bl_label = "Import/Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Re-Volt"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        # i/o buttons
        props = context.scene.revolt

        row = self.layout.row(align=True)
        row.operator("import_scene.revolt", text="Import", icon="IMPORT")
        row.operator("export_scene.revolt", text="Export", icon="EXPORT")
        row.operator("export_scene.revolt_redo", text="", icon="FILE_REFRESH")




class RevoltHelpersPanelObj(bpy.types.Panel):
    bl_label = "Helpers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Re-Volt"
    bl_context = "objectmode"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label("", icon="HELP")

    def draw(self, context):

        layout = self.layout
        props = context.scene.revolt

        box = layout.box()
        box.label("3D View:")
        col = box.column(align=True)
        col.operator(
            "helpers.enable_texture_mode",
            icon="POTATO",
            text="Texture"
        )
        col.operator(
            "helpers.enable_textured_solid_mode",
            icon="TEXTURE_SHADED",
            text="Textured Solid"
        )

        box = layout.box()
        box.label("RVGL:")
        box.operator(
            "helpers.launch_rv"
        )

class RevoltHelpersPanelMesh(bpy.types.Panel):
    bl_label = "Helpers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Re-Volt"
    bl_context = "mesh_edit"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label("", icon="HELP")

    def draw(self, context):

        layout = self.layout

        box = layout.box()
        box.label("3D View:")
        col = box.column(align=True)
        col.operator(
            "helpers.enable_texture_mode",
            icon="POTATO",
            text="Texture"
        )
        col.operator(
            "helpers.enable_textured_solid_mode",
            icon="TEXTURE_SHADED",
            text="Textured Solid"
        )



class RevoltFacePropertiesPanel(bpy.types.Panel):
    bl_label = "Face Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_category = "Re-Volt"

    selection = None
    selected_face_count = None

    def draw_header(self, context):
        self.layout.label("", icon="FACESEL_HLT")

    def draw(self, context):
        props = context.scene.revolt

        if props.face_edit_mode == "prm":
            prm_edit_panel(self, context)
        elif props.face_edit_mode == "ncp":
            ncp_edit_panel(self, context)


def prm_edit_panel(self, context):
    """  """
    obj = context.object
    layout = self.layout

    props = context.scene.revolt

    mesh = obj.data
    meshprops = obj.data.revolt
    bm = get_edit_bmesh(obj)
    flags = (bm.faces.layers.int.get("Type") or
             bm.faces.layers.int.new("Type"))
    if (self.selected_face_count is None or
            self.selected_face_count != mesh.total_face_sel):
        self.selected_face_count = mesh.total_face_sel
        self.selection = [face for face in bm.faces if face.select]

    # Counts the number of faces the flags are set for
    count = [0] * len(FACE_PROPS)
    for face in self.selection:
        for x in range(len(FACE_PROPS)):
            if face[flags] & FACE_PROPS[x]:
                count[x] += 1

    row = layout.row()
    row.label("Properties:")

    row  = layout.row()
    col = row.column(align=True)
    col.prop(meshprops, "face_double_sided",
        text="{}: Double sided".format(count[1]))
    col.prop(meshprops, "face_translucent",
        text="{}: Translucent".format(count[2]))
    col.prop(meshprops, "face_mirror",
        text="{}: Mirror".format(count[3]))
    col.prop(meshprops, "face_additive",
        text="{}: Additive blending".format(count[4]))
    col.prop(meshprops, "face_texture_animation",
        text="{}: Texture animation".format(count[5]))
    col.prop(meshprops, "face_no_envmapping",
        text="{}: No EnvMap".format(count[6]))
    if meshprops.face_envmapping:
        split = col.split(percentage=.7)
        scol = split.column(align=True)
        scol.prop(meshprops, "face_envmapping",
        text="{}: EnvMap".format(count[7]))
        scol = split.column(align=True)
        scol.prop(meshprops, "face_env", text="")
    else:
        col.prop(meshprops, "face_envmapping",
        text="{}: EnvMap".format(count[7]))

    col.prop(meshprops, "face_cloth",
        text="{}: Cloth effect".format(count[8]))
    col.prop(meshprops, "face_skip",
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

    if props.use_tex_num:
        row = layout.row()
        row.label("Texture:")
        row = layout.row()
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


def ncp_edit_panel(self, context):
    props = context.scene.revolt
    obj = context.object
    meshprops = context.object.data.revolt
    layout = self.layout

    mesh = obj.data
    bm = get_edit_bmesh(obj)
    flags = (bm.faces.layers.int.get("NCPType") or
             bm.faces.layers.int.new("NCPType"))
    if (self.selected_face_count is None or
            self.selected_face_count != mesh.total_face_sel):
        self.selected_face_count = mesh.total_face_sel
        self.selection = [face for face in bm.faces if face.select]

    # Counts the number of faces the flags are set for
    count = [0] * len(NCP_PROPS)
    for face in self.selection:
        for x in range(len(NCP_PROPS)):
            if face[flags] & NCP_PROPS[x]:
                count[x] += 1

    row = layout.row()
    row.label("Properties:")
    row  = self.layout.row()
    col = row.column(align=True)
    col.prop(meshprops, "face_ncp_double",
        text="{}: Double sided".format(count[1]))
    col.prop(meshprops, "face_ncp_no_skid",
        text="{}: No Skid Marks".format(count[5]))
    col.prop(meshprops, "face_ncp_oil",
        text="{}: Oil".format(count[6]))
    col.prop(meshprops, "face_ncp_object_only",
        text="{}: Object Only".format(count[2]))
    col.prop(meshprops, "face_ncp_camera_only",
        text="{}: Camera Only".format(count[3]))
    col.prop(meshprops, "face_ncp_nocoll",
        text="{}: No Collision".format(count[7]))


    col = row.column(align=True)
    col.scale_x = 0.15
    col.operator("ncpfaceprops.select", text="sel").prop = NCP_DOUBLE
    col.operator("ncpfaceprops.select", text="sel").prop = NCP_NO_SKID
    col.operator("ncpfaceprops.select", text="sel").prop = NCP_OIL
    col.operator("ncpfaceprops.select", text="sel").prop = NCP_OBJECT_ONLY
    col.operator("ncpfaceprops.select", text="sel").prop = NCP_CAMERA_ONLY
    col.operator("ncpfaceprops.select", text="sel").prop = NCP_NOCOLL

    row = layout.row()
    row.label("Material:")

    # Warns if texture mode is not enabled
    widget_texture_mode(self)

    row = layout.row(align=True)
    col = row.column(align=True)
    # Dropdown list of the current material
    col.prop(meshprops, "face_material", text="Set")
    col = row.column(align=True)
    col.scale_x = 0.15
    col.operator("ncpmaterial.select")

    # Dropdown list for selecting materials
    row = layout.row()
    row.prop(props, "select_material", text="Select all")


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

    def draw_header(self, context):
        self.layout.label("", icon="COLOR")

    @classmethod
    def poll(self, context):
        # Only shows up in NPC mode
        props = context.scene.revolt
        return props.face_edit_mode != "ncp"

    def draw(self, context):


        obj = context.object
        row = self.layout.row(align=True)

        # Warns if texture mode is not enabled
        widget_texture_mode(self)

        bm = get_edit_bmesh(obj)
        vc_layer = bm.loops.layers.color.get("Col")

        if widget_vertex_color_channel(self, obj):
            pass # No vertex color channel and the panel can't be used

        else:
            box = self.layout.box()
            row = box.row()
            row.template_color_picker(context.scene.revolt,
                                      "vertex_color_picker",
                                      value_slider=True)
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(context.scene.revolt, "vertex_color_picker", text = '')
            row = col.row(align=True)
            row.operator("vertexcolor.set", icon="PASTEDOWN").number=-1
            row.operator("vertexcolor.copycolor", icon="COPYDOWN")
            row = self.layout.row(align=True)
            row.operator("vertexcolor.set", text="Grey 50%").number=50
            row = self.layout.row()
            col = row.column(align=True)
            # col.alignment = 'EXPAND'
            col.operator("vertexcolor.set", text="Grey 45%").number=45
            col.operator("vertexcolor.set", text="Grey 40%").number=40
            col.operator("vertexcolor.set", text="Grey 35%").number=35
            col.operator("vertexcolor.set", text="Grey 30%").number=30
            col.operator("vertexcolor.set", text="Grey 20%").number=20
            col.operator("vertexcolor.set", text="Grey 10%").number=10
            col.operator("vertexcolor.set", text="Black").number=0
            col = row.column(align=True)
            # col.alignment = 'EXPAND'
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
        return context.object and len(context.selected_objects) >= 1 and context.object.type == "MESH"

    def draw_header(self, context):
        self.layout.label("", icon="RENDER_STILL")

    def draw(self, context):
        view = context.space_data
        obj = context.object
        props = context.scene.revolt

        # Warns if texture mode is not enabled
        widget_texture_mode(self)

        if obj and obj.select:
            # Checks if the object has a vertex color layer
            if widget_vertex_color_channel(self, obj):
                pass
            else:
                # Light orientation selection
                box = self.layout.box()
                box.label(text="Shade Object")
                row = box.row()
                row.prop(props, "light_orientation", text="Orientation")
                if props.light_orientation == "X":
                    dirs = ["Left", "Right"]
                if props.light_orientation == "Y":
                    dirs = ["Front", "Back"]
                if props.light_orientation == "Z":
                    dirs = ["Top", "Bottom"]
                # Headings
                row = box.row()
                row.label(text="Direction")
                row.label(text="Light")
                row.label(text="Intensity")
                # Settings for the first light
                row = box.row(align=True)
                row.label(text=dirs[0])
                row.prop(props, "light1", text="")
                row.prop(props, "light_intensity1", text="")
                # Settings for the second light
                row = box.row(align=True)
                row.label(text=dirs[1])
                row.prop(props, "light2", text="")
                row.prop(props, "light_intensity2", text="")
                # Bake button
                row = box.row()
                row.operator("lighttools.bakevertex",
                             text="Generate Shading",
                             icon="LIGHTPAINT")

            # Shadow tool
            box = self.layout.box()
            box.label(text="Generate Shadow Texture")
            row = box.row()
            row.prop(props, "shadow_method")
            col = box.column(align=True)
            col.prop(props, "shadow_quality")
            col.prop(props, "shadow_softness")
            col.prop(props, "shadow_resolution")
            row = box.row()
            row.operator("lighttools.bakeshadow",
                         text="Generate Shadow",
                         icon="LAMP_SPOT")
            row = box.row()
            row.prop(props, "shadow_table", text="Table")

            # Batch baking tool
            box = self.layout.box()
            box.label(text="Batch Bake Light")
            box.prop(props, "batch_bake_model_rgb")
            box.prop(props, "batch_bake_model_env")
            box.operator("helpers.batch_bake_model")


class RevoltInstancesPanel(bpy.types.Panel):
    bl_label = "Instances"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Re-Volt"
    bl_options = {"DEFAULT_CLOSED"}

    # @classmethod
    # def poll(self, context):
    #     return context.object and len(context.selected_objects) >= 1 and context.object.type == "MESH"

    def draw_header(self, context):
        self.layout.label("", icon="OUTLINER_OB_GROUP_INSTANCE")

    def draw(self, context):
        view = context.space_data
        obj = context.object
        props = context.scene.revolt
        layout = self.layout

        layout.label("Instances: {}/1024".format(len([obj for obj in context.scene.objects if obj.revolt.is_instance])))
        layout.operator("helpers.select_by_data")
        col = layout.column(align=True)
        col.prop(props, "rename_all_name", text="")
        col.operator("helpers.rename_all_objects")
        col.operator("helpers.select_by_name")

        col = layout.column(align=True)
        col.operator("helpers.set_instance_property")
        col.operator("helpers.rem_instance_property")


class MenuAnimModes(bpy.types.Menu):
    bl_idname = "texanim.modemenu"
    bl_label = "Animation Mode"

    def draw(self, context):
        layout = self.layout

        layout.operator("texanim.transform", icon="ARROW_LEFTRIGHT")
        layout.operator("texanim.grid", icon="MESH_GRID")


class RevoltAnimationPanel(bpy.types.Panel):
    bl_label = "Texture Animation (.w)"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_category = "Re-Volt"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        # Only shows up in NPC mode
        props = context.scene.revolt
        return props.face_edit_mode == "prm"

    def draw_header(self, context):
        self.layout.label("", icon="CAMERA_DATA")

    def draw(self, context):
        obj = context.object
        props = context.scene.revolt

        # Total slots
        row = self.layout.row(align=True)
        row.prop(props, "ta_max_slots", text="Total Slots")

        # Current slot
        row = self.layout.row(align=True)
        row.active = (props.ta_max_slots > 0)
        column = row.column(align=True)
        column.label("Animation Slot:")
        column.prop(props, "ta_current_slot", text="Slot")
        column.prop(props, "ta_max_frames")

        # Current frame
        framecol = self.layout.column(align=True)
        framecol.active = (props.ta_max_slots > 0)
        framecol.label("Animation Frame:")
        framecol.prop(props, "ta_current_frame")

        # Texture animation preview
        row = framecol.row(align=True)
        row.active = (props.ta_max_slots > 0)
        column = row.column(align=True)
        column.scale_x = 2.4
        column.operator("texanim.prev_prev", text="", icon="FRAME_PREV")
        column = row.column(align=True)
        column.operator("texanim.copy_frame_to_uv", text="Preview", icon="VIEWZOOM")
        column = row.column(align=True)
        column.scale_x = 2.4
        column.operator("texanim.prev_next", text="", icon="FRAME_NEXT")

        row = framecol.row(align=True)
        row.prop(props, "ta_current_frame_tex", icon="TEXTURE")
        row.prop(props, "ta_current_frame_delay", icon="PREVIEW_RANGE")

        # Texture animation operators
        row = self.layout.row()
        row.active = (props.ta_max_slots > 0)
        row.menu("texanim.modemenu", text="Animate...", icon="ANIM")


        # UV Coords
        row = self.layout.row()
        row.active = (props.ta_max_slots > 0)
        row.label("UV Coordinates:")

        row = self.layout.row(align=True)
        row.active = (props.ta_max_slots > 0)
        row.operator("texanim.copy_uv_to_frame", icon="COPYDOWN")

        row = self.layout.row()
        row.active = (props.ta_max_slots > 0)
        column = row.column()
        column.prop(props, "ta_current_frame_uv0")
        column.prop(props, "ta_current_frame_uv1")

        column = row.column()
        column.prop(props, "ta_current_frame_uv2")
        column.prop(props, "ta_current_frame_uv3")




class RevoltSettingsPanel(bpy.types.Panel):
    """

    """
    bl_label = "Add-On Settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Re-Volt"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label("", icon="SCRIPTWIN")

    def draw(self, context):
        props = context.scene.revolt
        layout = self.layout

        # General settings
        
        layout.label("Re-Volt Directory:")
        box = self.layout.box()
        box.prop(props, "revolt_dir", text="")
        if props.revolt_dir == "":
            box.label("No directory specified", icon="INFO")
        elif os.path.isdir(props.revolt_dir):
            if "rvgl.exe" in os.listdir(props.revolt_dir):
                box.label(
                    "Folder exists (RVGL for Windows)",
                    icon="FILE_TICK"
                )
            elif "rvgl" in os.listdir(props.revolt_dir):
                box.label(
                    "Folder exists (RVGL for Linux)",
                    icon="FILE_TICK"
                )
            else:
                box.label(
                    "Folder exists, RVGL not found",
                    icon="INFO"
                )

        else:
            box.label("Not found", icon="ERROR")


        layout.label("General:")
        layout.prop(props, "prefer_tex_solid_mode")
        layout.separator()

        # General import settings
        layout.label("Import:")
        layout.prop(props, "enable_tex_mode")
        layout.separator()

        # General export settings
        layout.label("Export:")
        layout.prop(props, "triangulate_ngons")
        layout.prop(props, "use_tex_num")
        layout.separator()

        # PRM Export settings
        layout.label("Export PRM (.prm/.m):")
        layout.prop(props, "apply_scale")
        layout.prop(props, "apply_rotation")
        layout.separator()

        # World Import settings
        layout.label("Import World (.w):")
        layout.prop(props, "w_parent_meshes")
        layout.prop(props, "w_import_bound_boxes")
        if props.w_import_bound_boxes:
            layout.prop(props, "w_bound_box_layers")
        layout.prop(props, "w_import_cubes")
        if props.w_import_cubes:
            layout.prop(props, "w_cube_layers")
        layout.prop(props, "w_import_big_cubes")
        if props.w_import_big_cubes:
            layout.prop(props, "w_big_cube_layers")
        layout.separator()

        # NCP Export settings
        layout.label("Export Collision (.ncp):")
        layout.prop(props, "ncp_export_selected")
        layout.prop(props, "ncp_export_collgrid")
        layout.prop(props, "ncp_collgrid_size")







"""
Widgets are little panel snippets that generally warn users if something isn't
set up correctly to use a feature. They return true if something isn't right.
They return false if everything is alright.
"""

def widget_texture_mode(self):
    if not texture_mode_enabled():
        props = bpy.context.scene.revolt
        box = self.layout.box()
        box.label(text="Texture Mode is not enabled.", icon='INFO')
        row = box.row()
        if props.prefer_tex_solid_mode:
            row.operator("helpers.enable_textured_solid_mode",
                         text="Enable Texture Mode",
                         icon="POTATO")
        else:
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
