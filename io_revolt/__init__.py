""" Marv's Add-On for Re-Volt """
import bpy
import os
import os.path
from bpy.app.handlers import persistent  # For the scene update handler
from . import common, panels, properties, tools

bl_info = {
    "name": "Re-Volt",
    "author": "Marvin Thiel",
    "version": (17, 10, 10),
    "blender": (2, 79, 0),
    "location": "File > Import-Export",
    "description": "Import and export Re-Volt file formats.",
    "wiki_url": "https://yethiel.github.io/re-volt-addon/",
    "tracker_url": "http://z3.invisionfree.com/Our_ReVolt_Pub/"
                   "index.php?showtopic=2296",
    "support": 'COMMUNITY',
    "category": "Import-Export"
}

# Reloads potentially changed modules on reload (F8 in Blender)
if "bpy" in locals():
    import imp

    imp.reload(common)
    imp.reload(panels)
    imp.reload(properties)
    imp.reload(tools)

    # Reloaded here because it's used in a class which is instanced here
    if "prm_in" in locals():
        imp.reload(prm_in)
    if "prm_out" in locals():
        imp.reload(prm_out)
    if "ncp_in" in locals():
        imp.reload(ncp_in)
    if "ncp_out" in locals():
        imp.reload(ncp_out)
    if "parameters_in" in locals():
        imp.reload(parameters_in)
    if "w_in" in locals():
        imp.reload(w_in)
    if "w_out" in locals():
        imp.reload(w_out)
    if "operators" in locals():
        imp.reload(operators)

# Makes common variables and classes directly accessible
from .common import *
from .properties import *

dprint("---\n\n\n\n")

@persistent
def edit_object_change_handler(scene):
    """Makes the edit mode bmesh available for use in GUI panels."""
    obj = scene.objects.active
    if obj is None:
        return
    # Adds an instance of the edit mode mesh to the global dict
    if obj.mode == 'EDIT' and obj.type == 'MESH':
        bm = dic.setdefault(obj.name, bmesh.from_edit_mesh(obj.data))
        return

    dic.clear()


def menu_func_import(self, context):
    """Import function for the user interface."""
    self.layout.operator("import_scene.revolt", text="Re-Volt")


def menu_func_export(self, context):
    """Export function for the user interface."""
    self.layout.operator("export_scene.revolt", text="Re-Volt")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.revolt = bpy.props.PointerProperty(type=RVSceneProperties)
    bpy.types.Object.revolt = bpy.props.PointerProperty(type=RVObjectProperties)
    bpy.types.Mesh.revolt = bpy.props.PointerProperty(type=RVMeshProperties)

    bpy.types.INFO_MT_file_import.prepend(menu_func_import)
    bpy.types.INFO_MT_file_export.prepend(menu_func_export)

    bpy.app.handlers.scene_update_post.append(edit_object_change_handler)


def unregister():
    bpy.utils.unregister_module(__name__)

    del bpy.types.Scene.revolt
    del bpy.types.Object.revolt
    del bpy.types.Mesh.revolt

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
    # bpy.app.handlers.scene_update_post.clear()


if __name__ == "__main__":
    register()
