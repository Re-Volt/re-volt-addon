"""
Re-Volt Object and mesh properties and functions for setting/getting them.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)

import bpy
from ast import literal_eval
from . import common
from . import rvstruct
from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
    CollectionProperty,
    IntVectorProperty,
    FloatVectorProperty,
    PointerProperty
)

from .common import *

"""
These property getters and setters use the bmesh from the global dict that gets
updated by the scene update handler found in init.
Creating bmeshes in the panels is bad practice as it causes unexpected
behavior.
"""


def get_face_material(self):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    layer = (bm.faces.layers.int.get("revolt_material") or
             bm.faces.layers.int.new("revolt_material"))
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0 or any([face[layer] != selected_faces[0][layer] for face in selected_faces]):
        return -1
    else:
        return selected_faces[0][layer]


def set_face_material(self, value):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    layer = (bm.faces.layers.int.get("revolt_material") or
             bm.faces.layers.int.new("revolt_material"))
    for face in bm.faces:
        if face.select:
            face[layer] = value

def get_face_texture(self):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    layer = (bm.faces.layers.int.get("Texture Number") or
             bm.faces.layers.int.new("Texture Number"))
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0:
        return -3
    elif any([face[layer] != selected_faces[0][layer] for face in selected_faces]):
        return -2
    else:
        return selected_faces[0][layer]


def set_face_texture(self, value):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    layer = (bm.faces.layers.int.get("Texture Number") or
             bm.faces.layers.int.new("Texture Number"))
    for face in bm.faces:
        if face.select:
            face[layer] = value


def set_face_env(self, value):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    env_layer = (bm.loops.layers.color.get("Env") or
                 bm.loops.layers.color.new("Env"))
    env_alpha_layer = (bm.faces.layers.float.get("EnvAlpha") or
                       bm.faces.layers.float.new("EnvAlpha"))
    for face in bm.faces:
        if face.select:
            for loop in face.loops:
                loop[env_layer] = value[:3]
            face[env_alpha_layer] = value[-1]


def get_face_env(self):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    env_layer = (bm.loops.layers.color.get("Env")
                 or bm.loops.layers.color.new("Env"))
    env_alpha_layer = (bm.faces.layers.float.get("EnvAlpha")
                       or bm.faces.layers.float.new("EnvAlpha"))

    # Gets the average color for all selected faces
    selected_faces = [face for face in bm.faces if face.select]
    col = get_average_vcol(selected_faces, env_layer)

    return [*col, selected_faces[0][env_alpha_layer]]


def set_vcol(faces, layer, color):
    for face in faces:
        for loop in face.loops:
            loop[layer] = color


def get_face_property(self):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    layer = bm.faces.layers.int.get("Type") or bm.faces.layers.int.new("Type")
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) == 0:
        return 0
    prop = selected_faces[0][layer]
    for face in selected_faces:
        prop = prop & face[layer]
    return prop


def set_face_property(self, value, mask):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    layer = bm.faces.layers.int.get("Type") or bm.faces.layers.int.new("Type")
    for face in bm.faces:
        if face.select:
            face[layer] = face[layer] | mask if value else face[layer] & ~mask


def select_faces(context, prop):
    eo = bpy.context.edit_object
    bm = get_edit_bmesh(eo)
    flag_layer = (bm.faces.layers.int.get("Type") or
                  bm.faces.layers.int.new("Type"))

    for face in bm.faces:
        if face[flag_layer] & prop:
            print(face[flag_layer], prop)
            face.select = not face.select
    redraw()


def update_ta_max_slots(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    frame = props.ta_current_frame

    if props.ta_max_slots > 0:
        dprint("TexAnim: Updating max slots...")

        # Converts the texture animations from string to dict
        ta = eval(props.texture_animations)

        # Creates a new texture animation if there is none in the slot
        while len(ta) < props.ta_max_slots:
            dprint("TexAnim: Creating new animation slot... ({}/{})".format(len(ta) + 1, props.ta_max_slots))
            ta.append(rvstruct.TexAnimation().as_dict())

        # Saves the texture animation
        props.texture_animations = str(ta)

        # Updates the rest of the UI
        update_ta_current_slot(self, context)


def update_ta_max_frames(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    # frame = props.ta_current_frame

    dprint("TexAnim: Updating max frames...")
    ta = eval(props.texture_animations)
    ta[slot]["frame_count"] = props.ta_max_frames

    # Creates new empty frames if there are none for the current slot
    while len(ta[slot]["frames"]) < props.ta_max_frames:
        dprint("Creating new animation frame... ({}/{})".format(
            len(ta[slot]["frames"]) + 1, props.ta_max_frames))

        new_frame = rvstruct.Frame().as_dict()
        ta[slot]["frames"].append(new_frame)

    props.texture_animations = str(ta)


def update_ta_current_slot(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    frame = props.ta_current_frame

    dprint("TexAnim: Updating current slot...")

    # Converts the texture animations from string to dict
    ta = eval(props.texture_animations)

    # Resets the number if it's out of bounds
    if slot > props.ta_max_slots - 1:
        props.ta_current_slot = props.ta_max_slots - 1
        return

    # Saves the texture animations
    props.texture_animations = str(ta)

    # Updates the rest of the UI
    props.ta_max_frames = len(ta[slot]["frames"])
    update_ta_max_frames(self, context)
    update_ta_current_frame(self, context)


# Texture Animation
def update_ta_current_frame(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    frame = props.ta_current_frame

    dprint("TexAnim: Updating current frame...")

    # Converts the texture animations from string to dict
    ta = eval(props.texture_animations)

    # Resets the number if it's out of bounds
    if frame > props.ta_max_frames - 1:
        props.ta_current_frame = props.ta_max_frames - 1
        return

    props.ta_current_frame_tex = ta[slot]["frames"][frame]["texture"]
    props.ta_current_frame_delay = ta[slot]["frames"][frame]["delay"]
    uv = ta[slot]["frames"][frame]["uv"]
    props.ta_current_frame_uv0 = (uv[3]["u"], 1 - uv[3]["v"])
    props.ta_current_frame_uv1 = (uv[2]["u"], 1 - uv[2]["v"])
    props.ta_current_frame_uv2 = (uv[1]["u"], 1 - uv[1]["v"])
    props.ta_current_frame_uv3 = (uv[0]["u"], 1 - uv[0]["v"])


def update_ta_current_frame_tex(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    frame = props.ta_current_frame

    dprint("TexAnim: Updating current frame texture...")

    # Converts the texture animations from string to dict
    ta = eval(props.texture_animations)
    # Sets the frame's texture
    ta[slot]["frames"][frame]["texture"] = props.ta_current_frame_tex
    # Saves the string again
    props.texture_animations = str(ta)


def update_ta_current_frame_delay(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    frame = props.ta_current_frame

    dprint("TexAnim: Updating current frame delay...")

    # Converts the texture animations from string to dict
    ta = eval(props.texture_animations)
    # Sets the frame's delay/duration
    ta[slot]["frames"][frame]["delay"] = props.ta_current_frame_delay
    # Saves the string again
    props.texture_animations = str(ta)


def update_ta_current_frame_uv(context, num):
    props = bpy.context.scene.revolt
    prop_str = "ta_current_frame_uv{}".format(num)
    slot = props.ta_current_slot
    frame = props.ta_current_frame

    # Reverses the accessor since they're saved in reverse order
    num = [0, 1, 2, 3][::-1][num]

    dprint("TexAnim: Updating current frame UV for {}...".format(num))

    ta = literal_eval(props.texture_animations)
    ta[slot]["frames"][frame]["uv"][num]["u"] = getattr(props, prop_str)[0]
    ta[slot]["frames"][frame]["uv"][num]["v"] = 1 - getattr(props, prop_str)[1]
    props.texture_animations = str(ta)


def copy_uv_to_frame(context):
    props = context.scene.revolt
    # Copies over UV coordinates from the mesh
    if context.object.data:
        bm = get_edit_bmesh(context.object)
        uv_layer = bm.loops.layers.uv.get("UVMap")
        sel_face = get_active_face(bm)
        if not sel_face:
            msg_box("Please select a face first.")
            return
        if not uv_layer:
            msg_box("Please create a UV layer first.")
            return
        for lnum in range(len(sel_face.loops)):
            uv = sel_face.loops[lnum][uv_layer].uv
            if lnum == 0:
                props.ta_current_frame_uv0 = (uv[0], uv[1])
            elif lnum == 1:
                props.ta_current_frame_uv1 = (uv[0], uv[1])
            elif lnum == 2:
                props.ta_current_frame_uv2 = (uv[0], uv[1])
            elif lnum == 3:
                props.ta_current_frame_uv3 = (uv[0], uv[1])
    else:
        dprint("No object for UV anim.")


def copy_frame_to_uv(context):
    props = context.scene.revolt
    if context.object.data:
        bm = get_edit_bmesh(context.object)
        uv_layer = bm.loops.layers.uv.get("UVMap")
        sel_face = get_active_face(bm)
        if not sel_face:
            msg_box("Please select a face first.")
            return
        if not uv_layer:
            msg_box("Please create a UV layer first.")
            return
        for lnum in range(len(sel_face.loops)):
            uv0 = props.ta_current_frame_uv0
            uv1 = props.ta_current_frame_uv1
            uv2 = props.ta_current_frame_uv2
            uv3 = props.ta_current_frame_uv3
            if lnum == 0:
                sel_face.loops[lnum][uv_layer].uv = uv0
            elif lnum == 1:
                sel_face.loops[lnum][uv_layer].uv = uv1
            elif lnum == 2:
                sel_face.loops[lnum][uv_layer].uv = uv2
            elif lnum == 3:
                sel_face.loops[lnum][uv_layer].uv = uv3
    else:
        dprint("No object for UV anim.")

"""
Re-Volt object and mesh properties
"""


class RVObjectProperties(bpy.types.PropertyGroup):
    light1 = EnumProperty(
        name = "Light 1",
        items = bake_lights,
        default = "SUN",
        description = "Type of light"
    )
    light2 = EnumProperty(
        name = "Light 2",
        items = bake_lights,
        default = "HEMI",
        description = "Type of light"
    )
    light_intensity1 = FloatProperty(
        name = "Intensity 1",
        min = 0.0,
        default = 1.5,
        description = "Intensity of Light 1"
    )
    light_intensity2 = FloatProperty(
        name = "Intensity 2",
        min= 0.0,
        default = .05,
        description = "Intensity of Light 2"
    )
    light_orientation = EnumProperty(
        name = "Orientation",
        items = bake_light_orientations,
        default = "Z",
        description = "Directions of the lights"
    )
    shadow_method = EnumProperty(
        name = "Method",
        items = bake_shadow_methods,
        description = "Default (Adaptive QMC):\nFaster option, recommended "
                      "for testing the shadow settings.\n\n"
                      "High Quality:\nSlower and less grainy option, "
                      "recommended for creating the final shadow."
    )
    shadow_quality = IntProperty(
        name = "Quality",
        min = 0,
        max = 32,
        default = 15,
        description = "The amount of samples the shadow is rendered with "
                      "(number of samples taken extra)."
    )
    shadow_resolution = IntProperty(
        name = "Resolution",
        min = 32,
        max = 8192,
        default = 128,
        description = "Texture resolution of the shadow.\n"
                      "Default: 128x128 pixels."
    )
    shadow_softness = FloatProperty(
        name = "Softness",
        min = 0.0,
        max = 100.0,
        default = 1,
        description = "Softness of the shadow "
                      "(Light size for ray shadow sampling)."
    )
    shadow_table = StringProperty(
        name = "Shadowtable",
        default = "",
        description = "Shadow coordinates for use in parameters.txt of cars.\n"
                      "Click to select all, then CTRL C to copy."
    )

    # Debug Objects
    is_bcube = BoolProperty(
        name = "Object is a BigCube",
        default = False,
        description = "Makes BigCube properties visible for this object."
    )
    is_cube = BoolProperty(
        name = "Object is a Cube",
        default = False,
        description = "Makes Cube properties visible for this object."
    )
    is_bbox = BoolProperty(
        name = "Object is a Boundary Box",
        default = False,
        description = "Makes BoundBox properties visible for this object."
    )
    bcube_mesh_indices = StringProperty(
        name = "Mesh indices",
        default = "",
        description = "Indices of child meshes."
    )


class RVMeshProperties(bpy.types.PropertyGroup):
    face_material = EnumProperty(
        name = "Material",
        items = materials,
        get = get_face_material,
        set = set_face_material
    )
    face_texture = IntProperty(
        name = "Texture",
        get = get_face_texture,
        set = set_face_texture,
        default = 0,
        min = -1,
        max = 9,
        description = "Texture page number:\n-1 is none,\n"
        "0 is texture page A\n"
        "1 is texture page B\n"
        "2 is texture page C\n"
        "3 is texture page D\n"
        "4 is texture page E\n"
        "5 is texture page F\n"
        "6 is texture page G\n"
        "7 is texture page H\n"
        "8 is texture page I\n"
        "9 is texture page J\n"
        "For this number to have an effect, "
        "the \"Use Texture Number\" export settings needs to be "
        "enabled."
    )
    face_double_sided = BoolProperty(
        name = "Double sided",
        get = lambda s: bool(get_face_property(s) & FACE_DOUBLE),
        set = lambda s,v: set_face_property(s, v, FACE_DOUBLE),
        description = "The polygon will be visible from both sides in-game."
    )
    face_translucent = BoolProperty(
        name = "Translucent",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSLUCENT),
        set = lambda s,v: set_face_property(s, v, FACE_TRANSLUCENT),
        description = "Renders the polyon transparent\n(takes transparency "
                      "from the \"Alpha\" vertex color layer or the alpha "
                      "layer of the texture."
    )
    face_mirror = BoolProperty(
        name = "Mirror",
        get = lambda s: bool(get_face_property(s) & FACE_MIRROR),
        set = lambda s,v: set_face_property(s, v, FACE_MIRROR),
        description = "This polygon covers a mirror area. (?)"
    )
    face_additive = BoolProperty(
        name = "Additive blending",
        get = lambda s: bool(get_face_property(s) & FACE_TRANSL_TYPE),
        set = lambda s,v: set_face_property(s, v, FACE_TRANSL_TYPE),
        description = "Renders the polygon with additive blending (black "
                      "becomes transparent, bright colors are added to colors "
                      "beneath)."
    )
    face_texture_animation = BoolProperty(
        name = "Animated",
        get = lambda s: bool(get_face_property(s) & FACE_TEXANIM),
        set = lambda s,v: set_face_property(s, v, FACE_TEXANIM),
        description = "Uses texture animation for this poly (only in .w files)."
    )
    face_no_envmapping = BoolProperty(
        name = "No EnvMap (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_NOENV),
        set = lambda s,v: set_face_property(s, v, FACE_NOENV),
        description = "Disables the environment map for this poly (.prm only)."
    )
    face_envmapping = BoolProperty(
        name = "EnvMapping (.w)",
        get = lambda s: bool(get_face_property(s) & FACE_ENV),
        set = lambda s,v: set_face_property(s, v, FACE_ENV),
        description = "Enables the environment map for this poly (.w only).\n\n"
                      "If enabled on pickup.m, sparks will appear"
                      "around the poly."
    )
    face_cloth = BoolProperty(
        name = "Cloth effect (.prm)",
        get = lambda s: bool(get_face_property(s) & FACE_CLOTH),
        set = lambda s,v: set_face_property(s, v, FACE_CLOTH),
        description = "Enables the cloth effect used on the Mystery car."
    )
    face_skip = BoolProperty(
        name = "Do not export",
        get = lambda s: bool(get_face_property(s) & FACE_SKIP),
        set = lambda s,v: set_face_property(s, v, FACE_SKIP),
        description = "Skips the polygon when exporting (not Re-Volt related)."
    )
    face_env = FloatVectorProperty(
        name = "Environment Color",
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        soft_min = 0.0,
        soft_max = 1.0,
        get = get_face_env,
        set = set_face_env,
        description = "Color of the environment map for World meshes."
    )

class RVSceneProperties(bpy.types.PropertyGroup):
    # User interface and misc.
    last_exported_filepath = StringProperty(
        name = "Last Exported Filepath",
        default = ""
    )
    ui_fold_export_settings = BoolProperty(
        name = "Export Settings",
        default = True,
        description = "Show Export Settings"
    )
    enable_tex_mode = BoolProperty(
        name = "Texture Mode after Import",
        default = True,
        description = "Enables Texture Mode after mesh import."
    )
    vertex_color_picker = FloatVectorProperty(
        name="Object Color",
        subtype='COLOR',
        default=(0, 0, 1.0),
        min=0.0, max=1.0,
        description="Color picker for painting custom vertex colors."
    )
    envidx = IntProperty(
        name="envidx",
        default=0,
        min=0,
        description="Current env color index for importing. Internal only."
    )

    # Export properties
    triangulate_ngons = BoolProperty(
        name = "Triangulate n-gons",
        default = True,
        description = "Triangulate n-gons when exporting.\n"
                     "Re-Volt only supports tris and quads, n-gons will not be "
                     "exported correctly.\nOnly turn this off if you know what "
                     "you're doing!"
    )
    use_tex_num = BoolProperty(
        name = "Use Number for Textures",
        default = False,
        description = "Uses the texture number from the texture layer "
                      "accessible in the tool shelf in Edit mode.\n"
                      "Otherwise, it uses the texture from the texture file."
    )
    apply_scale = BoolProperty(
        name = "Apply Scale",
        default = True,
        description = "Applies the object scale on export."
    )
    apply_rotation = BoolProperty(
        name = "Apply Rotation",
        default = True,
        description = "Applies the object rotation on export."
    )


    # World Import properties
    w_parent_meshes = BoolProperty(
        name = "Parent .w meshes to Empty",
        default = False,
        description = "Parents all .w meshes to an Empty object, resulting in "
                      "less clutter in the object outliner."
    )
    w_import_bound_boxes = BoolProperty(
        name = "Import Bound Boxes",
        default = False,
        description = "Imports the boundary box of each .w mesh for debugging "
                      "purposes."
    )
    w_bound_box_layers = BoolVectorProperty(
        name = "Bound Box Layers",
        subtype = "LAYER",
        size = 20,
        default = [True]+[False for x in range(0, 19)],
        description = "Sets the layers the objecs will be be imported to. "
                      "Select multiple by dragging or holding down Shift.\n"
                      "Activate multiple layers by pressing Shift + numbers."
    )
    w_import_cubes = BoolProperty(
        name = "Import Cubes",
        default = False,
        description = "Imports the cube of each .w mesh for debugging "
                      "purposes."
    )
    w_cube_layers = BoolVectorProperty(
        name = "Cube Layers",
        subtype = "LAYER",
        size = 20,
        default = [True]+[False for x in range(0, 19)],
        description = "Sets the layers the objecs will be be imported to. "
                      "Select multiple by dragging or holding down Shift.\n"
                      "Activate multiple layers by pressing Shift + numbers."
    )
    w_import_big_cubes = BoolProperty(
        name = "Import Big Cubes",
        default = False,
        description = "Imports Big Cubes for debugging purposes."
    )
    w_big_cube_layers = BoolVectorProperty(
        name = "Big Cube Layers",
        subtype = "LAYER",
        size = 20,
        default = [True]+[False for x in range(0, 19)],
        description = "Sets the layers the objecs will be be imported to. "
                      "Select multiple by dragging or holding down Shift.\n"
                      "Activate multiple layers by pressing Shift + numbers."
    )
    # Texture Animation
    texture_animations = StringProperty(
        name = "Texture Animations",
        default = "[]",
        description = "Storage for Texture animations. Should not be changed "
                      "by hand."
    )
    ta_max_slots = IntProperty(
        name = "Slots",
        min = 0,
        max = 9,
        default = 0,
        update = update_ta_max_slots,
        description = "Total number of texture animation slots. "
                      "All higher slots will be ignored on export."
    )
    ta_current_slot = IntProperty(
        name = "Animation",
        default = 0,
        min = 0,
        max = 9,
        update = update_ta_current_slot,
        description = "Texture animation slot."
    )
    ta_max_frames = IntProperty(
        name = "Frames",
        min = 2,
        default = 2,
        update = update_ta_max_frames,
        description = "Total number of frames of the current slot. "
                      "All higher frames will be ignored on export."
    )
    ta_current_frame = IntProperty(
        name = "Frame",
        default = 0,
        min = 0,
        update = update_ta_current_frame,
        description = "Current frame."
    )
    ta_current_frame_tex = IntProperty(
        name = "Texture",
        default = 0,
        min = -1,
        max = 9,
        update = update_ta_current_frame_tex,
        description = "Texture of the current frame."
    )
    ta_current_frame_delay = FloatProperty(
        name = "Duration",
        default = 0.01,
        min = 0,
        update = update_ta_current_frame_delay,
        description = "Duration of the current frame."
    )
    ta_current_frame_uv0 = FloatVectorProperty(
        name = "UV 0",
        size = 2,
        default = (0, 0),
        min = 0.0,
        max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 0),
        description = "UV coordinate of the first vertex."
    )
    ta_current_frame_uv1 = FloatVectorProperty(
        name = "UV 1",
        size = 2,
        default = (0, 0),
        min = 0.0,
        max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 1),
        description = "UV coordinate of the second vertex."
    )
    ta_current_frame_uv2 = FloatVectorProperty(
        name = "UV 2",
        size = 2,
        default = (0, 0),
        min = 0.0,
        max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 2),
        description = "UV coordinate of the third vertex."
    )
    ta_current_frame_uv3 = FloatVectorProperty(
        name = "UV 3",
        size = 2,
        default = (0, 0),
        min = 0.0,
        max = 1.0,
        update = lambda self, context: update_ta_current_frame_uv(context, 3),
        description = "UV coordinate of the fourth vertex."
    )
    ta_sync_with_face = BoolProperty(
        name="Sync UV with Selection",
        default=False,
        description="Updates the UV mapping of the currently selected face "
                    "with the UV coordinates of the texture animation frame.\n"
                    "Texture animation needs to be enabled for the selected "
                    " face."
    )
