"""
Name:    init
Purpose: Init file for the Blender Add-On

Description:
Marv's Add-On for Re-Volt 

"""

import bpy
import os
import os.path
import imp
from bpy.app.handlers import persistent  # For the scene update handler

from . import (
    common,
    layers,
    panels,
    props_mesh,
    props_obj,
    props_scene,
    operators,
    texanim,
    tools
)

# Reloads potentially changed modules on reload (F8 in Blender)
imp.reload(common)
imp.reload(layers)
imp.reload(panels)
imp.reload(props_mesh)
imp.reload(props_obj)
imp.reload(props_scene)
imp.reload(operators)
imp.reload(texanim)
imp.reload(tools)

# Reloaded here because it's used in a class which is instanced here
if "hul_in" in locals():
    imp.reload(hul_in)
if "img_in" in locals():
    imp.reload(img_in)
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
if "ta_csv_in" in locals():
    imp.reload(ta_csv_in)
if "ta_csv_out" in locals():
    imp.reload(ta_csv_out)
if "w_in" in locals():
    imp.reload(w_in)
if "w_out" in locals():
    imp.reload(w_out)
if "fin_in" in locals():
    imp.reload(fin_in)

# Makes common variables and classes directly accessible
from .common import *
from .props_mesh import *
from .props_obj import *
from .props_scene import *
from .texanim import *

dprint("---\n\n\n\n")

bl_info = {
"name": "Re-Volt",
"author": "Marvin Thiel",
"version": (18, 2, 26),
"blender": (2, 79, 1),
"location": "File > Import-Export",
"description": "Import and export Re-Volt file formats.",
"wiki_url": "https://yethiel.github.io/re-volt-addon/",
"tracker_url": "https://github.com/Yethiel/re-volt-addon/issues",
"support": 'COMMUNITY',
"category": "Import-Export"
}

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

    bpy.types.Scene.revolt = bpy.props.PointerProperty(
        type=RVSceneProperties
    )
    bpy.types.Object.revolt = bpy.props.PointerProperty(
        type=RVObjectProperties
    )
    bpy.types.Mesh.revolt = bpy.props.PointerProperty(
        type=RVMeshProperties
    )

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


if __name__ == "__main__":
    register()

dprint("Re-Volt add-on registered.")

