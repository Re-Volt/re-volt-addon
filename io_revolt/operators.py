if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(properties)

import bpy
from . import common
from . import properties

from .common import *
from .properties import *

"""
Import Operator for all file types
"""
class ImportRV(bpy.types.Operator):
    bl_idname = "import_scene.revolt"
    bl_label = "Import Re-Volt Files"
    bl_description = "Import Re-Volt game files"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        scene = context.scene

        format = get_format(self.filepath)

        print("Importing {}".format(self.filepath))

        if format == FORMAT_UNK:
            print("Unsupported format.")
        elif format == FORMAT_PRM:
            from . import prm_in
            prm_in.import_file(self.filepath, scene)
        else:
            print(format)
        print("Import done.")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ExportRV(bpy.types.Operator):
    bl_idname = "export_scene.revolt"
    bl_label = "Export Re-Volt Files"
    bl_description = "Export Re-Volt game files"

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        scene = context.scene
        # props = context.scene.revolt

        start_time = time.time()

        # call the export function corresponding to the file extension
        format = get_format(self.filepath)

        if format == FORMAT_UNK:
            msg_box("Not supported for export: {}".format(file_formats[format]))
        else:
            context.window.cursor_set('WAIT')
            # turn off undo for better performance
            use_global_undo = bpy.context.user_preferences.edit.use_global_undo
            bpy.context.user_preferences.edit.use_global_undo = False

            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode='OBJECT')

            # save filepath
            # props.last_exported_filepath = self.filepath

            if format == FORMAT_PRM:
                from . import prm_out
                prm_out.export_file(self.filepath, scene)
            else:
                print("Format is not PRM {}".format(file_formats[format]))

            print("Export done.")

            # turn undo back on
            bpy.context.user_preferences.edit.use_global_undo = use_global_undo

            context.window.cursor_set('DEFAULT')
            print(time.time() - start_time)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        pass

class ButtonSelectFaceProp(bpy.types.Operator):
    bl_idname = "faceprops.select"
    bl_label = "sel"
    prop = bpy.props.IntProperty()

    def execute(self, context):
        select_faces(context, self.prop)
        return{'FINISHED'}
