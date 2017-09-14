"""
- Marv's Re-Volt Blender add-on -

This Blender Add-On is inspired by the one for 2.73 made by Jigebren.
I wrote a class (rvstruct) for handling Re-Volt files which I am using here.
"""

bl_info = {
    "name": "Re-Volt",
    "author": "Marvin Thiel",
    "version": (17, 9, 12),
    "blender": (2, 78, 0),
    "location": "File > Import-Export",
    "description": "Import and export Re-Volt file formats.",
    "warning": "Experimental",
    "wiki_url": "http://learn.re-volt.io/blender-docs",
    "tracker_url": "http://z3.invisionfree.com/Our_ReVolt_Pub/"
                   "index.php?showtopic=2296",
    "category": "Import-Export",
    }

# Reloads potentially changed modules on reload (F8 in Blender)
if "bpy" in locals():
    import imp

    imp.reload(common)
    imp.reload(panels)
    imp.reload(properties)

    if "prm_in" in locals(): imp.reload(prm_in)

import bpy
import os
import os.path
import time
from bpy.app.handlers import persistent # For the scene update handler
from . import common, panels, properties

# Makes common variables and classes directly accessible
from .common import *
from .properties import *


def get_format(fstr):
    """ Gets the format by the ending and returns an int (see enum in common)"""
    fname, ext = os.path.splitext(fstr)

    if ext.startswith(".bm"):
        return FORMAT_BMP
    elif ext == ".txt":
        return FORMAT_CAR
    elif ext in [".prm", ".m"]:
        return FORMAT_PRM
    else:
        return FORMAT_UNK

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

def menu_func_import(self, context):
    self.layout.operator("import_scene.revolt", text="Re-Volt")

@persistent
def edit_object_change_handler(scene):
    obj = scene.objects.active
    if obj is None:
        return None
    # Adds an instance of the edit mode mesh to the global dict
    if obj.mode == 'EDIT' and obj.type == 'MESH':
        bm = dic.setdefault(obj.name, bmesh.from_edit_mesh(obj.data))
        return None

    dic.clear()
    return None

def register():
    bpy.utils.register_module(__name__)

    #bpy.utils.register_class(RV_SettingsScene)
    #bpy.utils.register_class(RVObjectProperties)
    # bpy.types.Scene.revolt = bpy.props.PointerProperty(type=RV_SettingsScene)
    bpy.types.Object.revolt = bpy.props.PointerProperty(type=RVObjectProperties)
    bpy.types.Mesh.revolt = bpy.props.PointerProperty(type=RVMeshProperties)

    bpy.types.INFO_MT_file_import.prepend(menu_func_import)
    # bpy.types.INFO_MT_file_export.prepend(menu_func_export)

    # bpy.app.handlers.scene_update_post.clear()
    bpy.app.handlers.scene_update_post.append(edit_object_change_handler)

def unregister():
    bpy.utils.unregister_module(__name__)

    # del bpy.types.Scene.revolt
    del bpy.types.Object.revolt
    del bpy.types.Mesh.revolt

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    # bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
