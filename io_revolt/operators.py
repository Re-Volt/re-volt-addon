if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(properties)
    imp.reload(tools)

import bpy
import time
from . import common
from . import properties
from . import tools

from .common import *
from .properties import *


class ImportRV(bpy.types.Operator):
    """
    Import Operator for all file types
    """
    bl_idname = "import_scene.revolt"
    bl_label = "Import Re-Volt Files"
    bl_description = "Import Re-Volt game files"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        scene = context.scene
        props = scene.revolt
        frmt = get_format(self.filepath)

        start_time = time.time()

        context.window.cursor_set("WAIT")

        print("Importing {}".format(self.filepath))

        if frmt == FORMAT_UNK:
            msg_box("Unsupported format.")

        elif frmt == FORMAT_PRM:
            from . import prm_in
            prm_in.import_file(self.filepath, scene)
            # Enables texture mode after import
            if props.enable_tex_mode:
                enable_texture_mode()

        elif frmt == FORMAT_CAR:
            from . import parameters_in
            parameters_in.import_file(self.filepath, scene)
            # Enables texture mode after import
            if props.enable_tex_mode:
                enable_texture_mode()

        elif frmt == FORMAT_NCP:
            from . import ncp_in
            ncp_in.import_file(self.filepath, scene)

        elif frmt == FORMAT_W:
            from . import w_in
            w_in.import_file(self.filepath, scene)
            # Enables texture mode after import
            if props.enable_tex_mode:
                enable_texture_mode()

        else:
            msg_box("Not yet supported: {}".format(FORMATS[frmt]))

        end_time = time.time() - start_time
        print("Import done in {0:.3f} seconds.".format(end_time))

        context.window.cursor_set("DEFAULT")

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class ExportRV(bpy.types.Operator):
    bl_idname = "export_scene.revolt"
    bl_label = "Export Re-Volt Files"
    bl_description = "Export Re-Volt game files"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        scene = context.scene
        props = context.scene.revolt

        start_time = time.time()
        context.window.cursor_set("WAIT")

        # Gets the format from the file path
        frmt = get_format(self.filepath)

        if frmt == FORMAT_UNK:
            msg_box("Not supported for export: {}".format(FORMATS[frmt]))
        else:
            # Turns off undo for better performance
            use_global_undo = bpy.context.user_preferences.edit.use_global_undo
            bpy.context.user_preferences.edit.use_global_undo = False

            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="OBJECT")

            # Saves filepath for re-exporting the same file
            props.last_exported_filepath = self.filepath

            if frmt == FORMAT_PRM:
                # Checks if a file can be exported
                if not tools.check_for_export(scene.objects.active):
                    return {"FINISHED"}

                from . import prm_out
                prm_out.export_file(self.filepath, scene)

            elif frmt == FORMAT_NCP:
                from . import ncp_out
                print("Exporting to .ncp...")
                ncp_out.export_file(self.filepath, scene)

            elif frmt == FORMAT_W:
                from . import w_out
                print("Exporting to .w...")
                w_out.export_file(self.filepath, scene)

            else:
                print("Format not yet supported {}".format(FORMATS[frmt]))

            # Re-enables undo
            bpy.context.user_preferences.edit.use_global_undo = use_global_undo

        context.window.cursor_set("DEFAULT")

        end_time = time.time() - start_time
        print("Export done in {0:.3f} seconds.".format(end_time))

        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def draw(self, context):
        props = context.scene.revolt
        layout = self.layout
        space = context.space_data

        layout.prop(props, "triangulate_ngons")
        layout.prop(props, "use_tex_num")


""" BUTTONS
    Button operators for the user interface
"""


class ButtonCopyUvToFrame(bpy.types.Operator):
    bl_idname = "texanim.copy_uv_to_frame"
    bl_label = "UV to Frame"
    bl_description = "Copies the UV coordinates of the currently selected face to the texture animation frame"

    def execute(self, context):
        copy_uv_to_frame(context)
        redraw()
        return{"FINISHED"}

class ButtonCopyFrameToUv(bpy.types.Operator):
    bl_idname = "texanim.copy_frame_to_uv"
    bl_label = "Frame to UV"
    bl_description = "Copies the UV coordinates of the frame to the currently selected face"

    def execute(self, context):
        copy_frame_to_uv(context)
        redraw()
        return{"FINISHED"}

class ButtonSelectFaceProp(bpy.types.Operator):
    bl_idname = "faceprops.select"
    bl_label = "sel"
    bl_description = "Select or delesect all polygons with this property"
    prop = bpy.props.IntProperty()

    def execute(self, context):
        select_faces(context, self.prop)
        return{"FINISHED"}

class ButtonSelectNCPFaceProp(bpy.types.Operator):
    bl_idname = "ncpfaceprops.select"
    bl_label = "sel"
    bl_description = "Select or delesect all polygons with this property"
    prop = bpy.props.IntProperty()

    def execute(self, context):
        select_ncp_faces(context, self.prop)
        return{"FINISHED"}

class ButtonSelectNCPMaterial(bpy.types.Operator):
    bl_idname = "ncpmaterial.select"
    bl_label = "sel"
    bl_description = "Select all faces of the same material"

    def execute(self, context):
        props = context.scene.revolt
        meshprops = context.object.data.revolt
        props.select_material = meshprops.face_material
        return{"FINISHED"}

# VERTEX COLORS

class ButtonVertexColorSet(bpy.types.Operator):
    bl_idname = "vertexcolor.set"
    bl_label = "Set Color"
    bl_description = "Apply color to selected faces"
    number = bpy.props.IntProperty()

    def execute(self, context):
        tools.set_vertex_color(context, self.number)
        return{"FINISHED"}

class ButtonVertexColorCreateLayer(bpy.types.Operator):
    bl_idname = "vertexcolor.create_layer"
    bl_label = "Create Vertex Color Layer"
    bl_description = "Creates a vertex color layer"

    def execute(self, context):
        create_color_layer(context)
        return{"FINISHED"}

class ButtonVertexAlphaCreateLayer(bpy.types.Operator):
    bl_idname = "alphacolor.create_layer"
    bl_label = "Create Alpha Color Layer"

    def execute(self, context):
        create_alpha_layer(context)
        return{"FINISHED"}

class ButtonEnableTextureMode(bpy.types.Operator):
    bl_idname = "helpers.enable_texture_mode"
    bl_label = "Enable Texture Mode"
    bl_description = "Enables texture mode so textures can be seen"

    def execute(self, context):
        enable_texture_mode()
        return{"FINISHED"}

class ButtonEnableTexturedSolidMode(bpy.types.Operator):
    bl_idname = "helpers.enable_textured_solid_mode"
    bl_label = "Enable Textured Solid Mode"
    bl_description = "Enables texture mode so textures can be seen"

    def execute(self, context):
        enable_textured_solid_mode()
        return{"FINISHED"}

class ButtonBakeShadow(bpy.types.Operator):
    bl_idname = "lighttools.bakeshadow"
    bl_label = "Bake Shadow"
    bl_description = "Creates a shadow plane beneath the selected object"

    def execute(self, context):
        tools.bake_shadow(self, context)
        return{"FINISHED"}

class ButtonBakeLightToVertex(bpy.types.Operator):
    bl_idname = "lighttools.bakevertex"
    bl_label = "Bake light"
    bl_description = "Bakes the light to the active vertex color layer"

    def execute(self, context):
        tools.bake_vertex(self, context)
        return{"FINISHED"}
