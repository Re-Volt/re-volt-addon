import os
import rvstruct

filepath = "test.csv"

f = open(filepath, "r")

animations = {}

# tex_anim = rvstruct.TexAnim()

lines = f.readlines()

# header =

for line in lines:
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


    # print("Slot: {}, Frame: {}, Tex: {}, Delay: {}".format(
    #     slot_num, frame_num, frame_tex, frame_delay
    # ))
    # print(u0, v0, u1, v1, u2, v2, u3, v3)
    # frame = rvstruct.Frame()
