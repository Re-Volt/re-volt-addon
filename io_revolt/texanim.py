if "bpy" in locals():
    import imp
    imp.reload(common)

import bpy
from . import common
from . import rvstruct
from .common import *


def update_ta_max_slots(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    frame = props.ta_current_frame

    if props.ta_max_slots > 0:
        dprint("TexAnim: Updating max slots..")

        # Converts the texture animations from string to dict
        ta = eval(props.texture_animations)

        # Creates a new texture animation if there is none in the slot
        while len(ta) < props.ta_max_slots:
            dprint("TexAnim: Creating new animation slot... ({}/{})".format(
                len(ta) + 1, props.ta_max_slots)
            )
            ta.append(rvstruct.TexAnimation().as_dict())

        # Saves the texture animation
        props.texture_animations = str(ta)

        # Updates the rest of the UI
        update_ta_current_slot(self, context)


def update_ta_max_frames(self, context):
    props = context.scene.revolt
    slot = props.ta_current_slot
    # frame = props.ta_current_frame

    dprint("TexAnim: Updating max frames..")
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

    dprint("TexAnim: Updating current slot..")

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

    dprint("TexAnim: Updating current frame..")

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

    dprint("TexAnim: Updating current frame texture..")

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

    dprint("TexAnim: Updating current frame delay..")

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

    dprint("TexAnim: Updating current frame UV for {}..".format(num))

    ta = eval(props.texture_animations)
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
            msg_box("Please select a face first")
            return
        if not uv_layer:
            msg_box("Please create a UV layer first")
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
        dprint("No object for UV anim")


def copy_frame_to_uv(context):
    props = context.scene.revolt
    if context.object.data:
        bm = get_edit_bmesh(context.object)
        uv_layer = bm.loops.layers.uv.get("UVMap")
        sel_face = get_active_face(bm)
        if not sel_face:
            msg_box("Please select a face first")
            return
        if not uv_layer:
            msg_box("Please create a UV layer first")
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
        dprint("No object for UV anim")
