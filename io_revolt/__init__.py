"""
- Marv's Re-Volt Blender add-on -

This Blender Add-On is heavily inspired by the one for 2.73 made by Jigebren.
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


if "bpy" in locals():
    import imp

    # imp.reload(common)

    if "io_prm" in locals(): imp.reload(io_prm)

import bpy
import os
import os.path
import time


"""
Supported File Formats
"""
FORMAT_UNK   = -1
FORMAT_BMP   =  0
FORMAT_CAR   =  1
FORMAT_FIN   =  2
FORMAT_FOB   =  3
FORMAT_HUL   =  4
FORMAT_LIT   =  5
FORMAT_NCP   =  6
FORMAT_NCP_W =  7
FORMAT_PRM   =  8
FORMAT_RIM   =  9
FORMAT_RTU   = 10
FORMAT_TAZ   = 11
FORMAT_VIS   = 12
FORMAT_W     = 13

file_formats = {
    FORMAT_UNK   : "Unknown Format",
    FORMAT_BMP   : "BMP",
    FORMAT_CAR   : "Parameters.txt",
    FORMAT_FIN   : "FIN",
    FORMAT_FOB   : "FOB",
    FORMAT_HUL   : "HUL",
    FORMAT_LIT   : "LIT",
    FORMAT_NCP   : "NCP (Object)",
    FORMAT_NCP_W : "NCP (World)",
    FORMAT_PRM   : "PRM/M",
    FORMAT_RIM   : "RIM",
    FORMAT_RTU   : "RTU",
    FORMAT_TAZ   : "TAZ",
    FORMAT_VIS   : "VIS",
    FORMAT_W     : "W",
}

def get_format(fstr):
    """ Gets the format by the ending and returns an int (see enum above)"""
    fname, ext = os.path.splitext(fstr)

    if ext.startswith(".bm"):
        return FORMAT_BMP
    elif ext == ".txt":
        return FORMAT_CAR
    elif ext in [".prm", ".m"]:
        return FORMAT_PRM
    else:
        return FORMAT_UNK

class RVObjectProperties(bpy.types.PropertyGroup):

    is_fin = bpy.props.BoolProperty(
            # name="Object is an Instance",
            description="Object is an Instance",
            # description="Only Instance objects are exported to the .fin file (and automatically rejected from World and World NCP file)",
            )

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
            from . import io_prm
            io_prm.import_file(self.filepath, scene)
        else:
            print(format)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func_import(self, context):
    self.layout.operator("import_scene.revolt", text="Re-Volt")

def register():
    bpy.utils.register_module(__name__)

    #bpy.utils.register_class(RV_SettingsScene)
    #bpy.utils.register_class(RVObjectProperties)
    # bpy.types.Scene.revolt = bpy.props.PointerProperty(type=RV_SettingsScene)
    bpy.types.Object.revolt = bpy.props.PointerProperty(type=RVObjectProperties)

    bpy.types.INFO_MT_file_import.prepend(menu_func_import)
    # bpy.types.INFO_MT_file_export.prepend(menu_func_export)

def unregister():
    bpy.utils.unregister_module(__name__)

    # del bpy.types.Scene.revolt
    del bpy.types.Object.revolt

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    # bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
