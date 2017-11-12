if "bpy" in locals():
    import imp
    imp.reload(common)

import bpy
import bmesh
import mathutils
from math import pi
import time

from . import common
from .common import *


def bake_shadow(self, context):
    # This will create a negative shadow (Re-Volt requires a neg. texture)
    rd = context.scene.render
    rd.use_bake_to_vertex_color = False
    rd.use_textures = False

    shade_obj = context.object
    scene = bpy.context.scene
    props = scene.revolt

    resolution = props.shadow_resolution
    quality = props.shadow_quality
    method = props.shadow_method
    softness = props.shadow_softness

    # create hemi (positive)
    lamp_data_pos = bpy.data.lamps.new(name="ShadePositive", type="HEMI")
    lamp_positive = bpy.data.objects.new(name="ShadePositive", object_data=lamp_data_pos)

    lamp_data_neg = bpy.data.lamps.new(name="ShadeNegative", type="SUN")
    # create sun light (negative)
    lamp_data_neg.use_negative = True
    lamp_data_neg.shadow_method = "RAY_SHADOW"
    lamp_data_neg.shadow_ray_samples = quality
    lamp_data_neg.shadow_ray_sample_method = method
    lamp_data_neg.shadow_soft_size = softness
    lamp_negative = bpy.data.objects.new(name="ShadeNegative", object_data=lamp_data_neg)

    # link objects to the scene
    scene.objects.link(lamp_positive)
    scene.objects.link(lamp_negative)

    # create a texture
    shadow_tex = bpy.data.images.new(name="Shadow", width=resolution, height=resolution)

    all_objs = [ob_child for ob_child in context.scene.objects if ob_child.parent == shade_obj] + [shade_obj]

    # get the bounds taking in account all child objects (wheels, etc.)
    # using the world matrix here to get positions from child objects
    far_left = min([min([(ob.matrix_world[0][3] + ob.bound_box[i][0] * shade_obj.scale[0]) for i in range(0, 8)]) for ob in all_objs])
    far_right = max([max([(ob.matrix_world[0][3] + ob.bound_box[i][0] * shade_obj.scale[0]) for i in range(0, 8)]) for ob in all_objs])
    far_front = max([max([(ob.matrix_world[1][3] + ob.bound_box[i][1] * shade_obj.scale[1]) for i in range(0, 8)]) for ob in all_objs])
    far_back = min([min([(ob.matrix_world[1][3] + ob.bound_box[i][1] * shade_obj.scale[1]) for i in range(0, 8)]) for ob in all_objs])
    far_top = max([max([(ob.matrix_world[2][3] + ob.bound_box[i][2] * shade_obj.scale[2]) for i in range(0, 8)]) for ob in all_objs])
    far_bottom = min([min([(ob.matrix_world[2][3] + ob.bound_box[i][2] * shade_obj.scale[2]) for i in range(0, 8)]) for ob in all_objs])

    # get the dimensions to set the scale
    dim_x = abs(far_left - far_right)
    dim_y = abs(far_front - far_back)

    # location for the shadow plane
    loc = ((far_right + far_left)/2,
           (far_front + far_back)/2,
            far_bottom)

    # create the shadow plane and map it
    bpy.ops.mesh.primitive_plane_add(location=loc, enter_editmode=True)
    bpy.ops.uv.unwrap()
    bpy.ops.object.mode_set(mode='OBJECT')
    shadow_plane = context.object

    # scale the shadow plane
    scale = max(dim_x, dim_y)
    shadow_plane.scale[0] = scale/1.5
    shadow_plane.scale[1] = scale/1.5

    # unwrap the shadow plane
    for uv_face in context.object.data.uv_textures.active.data:
        uv_face.image = shadow_tex

    bpy.ops.object.bake_image()

    # And finally select it and delete it
    shade_obj.select = False
    shadow_plane.select = False
    lamp_positive.select = True
    lamp_negative.select = True
    bpy.ops.object.delete()

    # select the other object again
    shade_obj.select = True
    scene.objects.active = shade_obj

    # space between the car body center and the edge of the shadow plane
    sphor = (shadow_plane.location[0] - (shadow_plane.dimensions[0]/2))
    spver = ((shadow_plane.dimensions[1]/2) - shadow_plane.location[1])

    # Generates shadowtable
    sleft = (sphor - shade_obj.location[0]) * 100
    sright = (shade_obj.location[0] - sphor) * 100
    sfront = (spver - shade_obj.location[1]) * 100
    sback = (shade_obj.location[1] - spver) * 100
    sheight = (far_bottom - shade_obj.location[2]) * 100
    shtable = ";)SHADOWTABLE {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}".format(
        sleft, sright, sfront, sback, sheight
    )
    props.shadow_table = shtable


def bake_vertex(self, context):
    # Set scene to render to vertex color
    rd = context.scene.render
    rd.use_bake_to_vertex_color = True
    rd.use_textures = False

    shade_obj = context.object
    scene = bpy.context.scene
    props = scene.revolt

    if props.light1 != "None":
        # Creates new lamp datablock
        lamp_data1 = bpy.data.lamps.new(
            name="ShadeLight1",
            type=props.light1
        )
        # Creates new object with our lamp datablock
        lamp_object1 = bpy.data.objects.new(
            name="ShadeLight1",
            object_data=lamp_data1
        )
        lamp_object1.data.energy = props.light_intensity1
        # Links lamp object to the scene so it'll appear in this scene
        scene.objects.link(lamp_object1)

        # Rotates light
        if props.light_orientation == "X":
            lamp_object1.location = (-1.0, 0, 0)
            lamp_object1.rotation_euler = (0, -pi/2, 0)
        elif props.light_orientation == "Y":
            lamp_object1.location = (0, 1.0, 0)
            lamp_object1.rotation_euler = (-pi/2, 0, 0)
        elif props.light_orientation == "Z":
            lamp_object1.location = (0, 0, 1.0)

    if props.light2 != "None":
        lamp_data2 = bpy.data.lamps.new(
            name="ShadeLight2",
            type=props.light2
        )
        lamp_object2 = bpy.data.objects.new(
            name="ShadeLight2",
            object_data=lamp_data2
        )
        lamp_object2.data.energy = props.light_intensity2
        scene.objects.link(lamp_object2)

        # rotate light
        if props.light_orientation == "X":
            lamp_object2.location = (1.0, 0, 0)
            lamp_object2.rotation_euler = (0, pi/2, 0)
        elif props.light_orientation == "Y":
            lamp_object2.location = (0, -1.0, 0)
            lamp_object2.rotation_euler = (pi/2, 0, 0)
        elif props.light_orientation == "Z":
            lamp_object2.location = (0, 0, -1.0)
            lamp_object2.rotation_euler = (pi, 0, 0)

    # bake the image
    bpy.ops.object.bake_image()

    # select lights and delete them
    shade_obj.select = False
    if props.light1 != "None":
        lamp_object1.select = True
    if props.light2 != "None":
        lamp_object2.select = True
    bpy.ops.object.delete()

    # select the other object again
    shade_obj.select = True
    scene.objects.active = shade_obj
    redraw()
