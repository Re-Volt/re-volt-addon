import bpy

from . import common
from . import operators

if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(operators)

from .common import *
from .operators import *

class RevoltFacePropertiesPanel(bpy.types.Panel):
    bl_label = "Face Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_category = "Re-Volt"

    selection = None
    selected_face_count = None

    @classmethod
    def poll(self, context):
        return (context.object is not None)

    def draw(self, context):
        obj = context.object
        mesh = obj.data
        bm = dic.setdefault(obj.name, bmesh.from_edit_mesh(obj.data))
        # bm = dic[obj.name]
        flags = bm.faces.layers.int.get("Type") or bm.faces.layers.int.new("Type")
        if self.selected_face_count is None or self.selected_face_count != mesh.total_face_sel:
            self.selected_face_count = mesh.total_face_sel
            self.selection = [face for face in bm.faces if face.select]

        # count the number of faces the flags are set for
        count = [0] * len(FACE_PROPS)
        # if len(self.selection) > 1:
        for face in self.selection:
            for x in range(len(FACE_PROPS)):
                if face[flags] & FACE_PROPS[x]:
                    count[x] += 1

        self.layout.prop(context.object.data.revolt, "face_material", text="Material".format(""))
        row  = self.layout.row()
        col = row.column(align = True)
        col.prop(context.object.data.revolt, "face_double_sided", text="{}: Double sided".format(count[1]))
        col.prop(context.object.data.revolt, "face_translucent", text="{}: Translucent".format(count[2]))
        col.prop(context.object.data.revolt, "face_mirror", text="{}: Mirror".format(count[3]))
        col.prop(context.object.data.revolt, "face_additive", text="{}: Additive blending".format(count[4]))
        col.prop(context.object.data.revolt, "face_texture_animation", text="{}: Texture animation".format(count[5]))
        col.prop(context.object.data.revolt, "face_no_envmapping", text="{}: No EnvMap".format(count[6]))
        col.prop(context.object.data.revolt, "face_envmapping", text="{}: EnvMap".format(count[7]))
        col.prop(context.object.data.revolt, "face_cloth", text="{}: Cloth effect".format(count[8]))
        col.prop(context.object.data.revolt, "face_skip", text="{}: Do not export".format(count[9]))
        col = row.column(align=True)
        col.scale_x = 0.15
        col.operator("faceprops.select", text="sel").prop = FACE_DOUBLE
        col.operator("faceprops.select", text="sel").prop = FACE_TRANSLUCENT
        col.operator("faceprops.select", text="sel").prop = FACE_MIRROR
        col.operator("faceprops.select", text="sel").prop = FACE_TRANSL_TYPE
        col.operator("faceprops.select", text="sel").prop = FACE_TEXANIM
        col.operator("faceprops.select", text="sel").prop = FACE_NOENV
        col.operator("faceprops.select", text="sel").prop = FACE_CLOTH
        col.operator("faceprops.select", text="sel").prop = FACE_CLOTH
        col.operator("faceprops.select", text="sel").prop = FACE_SKIP


        if len(self.selection) > 1:
            self.layout.prop(context.object.data.revolt, "face_texture", text="Texture (multiple)")
            self.layout.label(text="(Texture will be applied to all selected faces.)")
        else:
            self.layout.prop(context.object.data.revolt, "face_texture", text="Texture".format(""))
