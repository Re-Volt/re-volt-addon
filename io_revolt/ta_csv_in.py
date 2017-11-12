if "common" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)

from . import common
from . import rvstruct

from .common import *

def import_file(filepath, scene):
    props = scene.revolt

    f = open(filepath, "r")
    lines = f.readlines()

    if not TA_CSV_HEADER in lines[0]:
        msg_box(
            "File does not include texture animation header."
            "ERROR"
        )
    # Removes the header
    lines = lines[1:]

    # Resets the texture animations
    props.texture_animations = "[]"

    animations = {}

    for line in lines:
        if line == "\n":
            continue
        values = line.split(",")
        slot_num = int(values[0])
        frame_num = int(values[1])
        frame_tex = int(values[2])
        frame_delay = float(values[3])
        u0, v0, u1, v1, u2, v2, u3, v3 = [float(c) for c in values[4:12]]

        if not slot_num in animations:
            animations[slot_num] = rvstruct.TexAnimation()

        frame = rvstruct.Frame()
        frame.texture = frame_tex
        frame.delay = frame_delay
        uv0 = rvstruct.UV(uv=(u0, v0))
        uv1 = rvstruct.UV(uv=(u1, v1))
        uv2 = rvstruct.UV(uv=(u2, v2))
        uv3 = rvstruct.UV(uv=(u3, v3))
        frame.uv = [uv0, uv1, uv2, uv3]

        animations[slot_num].frames.insert(frame_num, frame)

        animations[slot_num].frame_count = len(animations[slot_num].frames)

    props.texture_animations = str([a.as_dict() for a in animations.values()])

    props.ta_max_slots = len(animations)
