import os
import bpy
import bmesh
from mathutils import Color, Vector
from . import common
from . import rvstruct
from . import img_in
from . import prm_in

from .rvstruct import World
from .common import *
from .prm_in import import_mesh
"""
WORLD IMPORT
Imports level files which include meshes and other structures for optimization.s
"""
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)
    imp.reload(img_in)
    imp.reload(prm_in)


def import_file(filepath, scene):
    """
    Imports a .w file and links it to the scene as a Blender object.
    """

    props = scene.revolt

    with open(filepath, 'rb') as file:
        filename = os.path.basename(filepath)
        world = World(file)

    meshes = world.meshes
    print("Imported {} ({} meshes)".format(filename, len(meshes)))

    # Creates an empty object to parent meshes to if enabled in settings
    if props.w_parent_meshes:
        main_w = bpy.data.objects.new(bpy.path.basename(filename), None)
        bpy.context.scene.objects.link(main_w)
    for rvmesh in meshes:
        # Creates a mesh from rv data and links it to the scene as an object
        me = import_mesh(rvmesh, scene, filepath, world.env_list)
        ob = bpy.data.objects.new(filename, me)
        scene.objects.link(ob)
        scene.objects.active = ob

        # Parents the mesh to the main .w object
        if props.w_parent_meshes:
            ob.parent = main_w

        # Imports bound box for each mesh if enabled in settings
        if props.w_import_bound_boxes:
            bbox = create_bound_box(scene, rvmesh.bbox, filename)
            bbox.layers = props.w_bound_box_layers
            bbox.parent = ob

        # Imports bound ball for each mesh if enabled in settings
        if props.w_import_bound_balls:
            radius = rvmesh.bound_ball_radius
            center = rvmesh.bound_ball_center.data
            bsphere = create_sphere(
                scene, "BOUNDBALL", center, radius, filename
            )
            bsphere.layers = props.w_bound_ball_layers
            bsphere.parent = ob

    # Creates the big cubes (spheres) around multiple meshes if enabled
    if props.w_import_big_cubes:
        for cube in world.bigcubes:
            radius = cube.size
            center = cube.center.data
            bcube = create_sphere(
                scene, "BIGCUBE", center, radius, filename
            )
            m_indices = ", ".join([str(c) for c in cube.mesh_indices])
            bcube.revolt.bcube_mesh_indices = m_indices
            bcube.revolt.is_bcube = True
            bcube.layers = props.w_big_cube_layers
            bcube.parent = main_w

    props.texture_animations = str([a.as_dict() for a in world.animations])
    props.ta_max_slots = len(world.animations)


def create_bound_box(scene, bbox, filename):
    # Creates a new mesh and bmesh
    me = bpy.data.meshes.new("RVBBox_{}".format(filename))
    bm = bmesh.new()

    coords = [
        to_blender_coord((bbox.xlo, bbox.ylo, bbox.zhi)),
        to_blender_coord((bbox.xhi, bbox.ylo, bbox.zhi)),
        to_blender_coord((bbox.xlo, bbox.yhi, bbox.zhi)),
        to_blender_coord((bbox.xhi, bbox.yhi, bbox.zhi)),
        to_blender_coord((bbox.xlo, bbox.ylo, bbox.zlo)),
        to_blender_coord((bbox.xhi, bbox.ylo, bbox.zlo)),
        to_blender_coord((bbox.xlo, bbox.yhi, bbox.zlo)),
        to_blender_coord((bbox.xhi, bbox.yhi, bbox.zlo))
    ]
    for co in coords:
        bm.verts.new(co)
    bm.verts.ensure_lookup_table()

    faces = [
        # Front
        (bm.verts[0], bm.verts[1], bm.verts[3], bm.verts[2]),
        # Back
        (bm.verts[6], bm.verts[7], bm.verts[5], bm.verts[4]),
        # Left
        (bm.verts[0], bm.verts[2], bm.verts[6], bm.verts[4]),
        # Right
        (bm.verts[5], bm.verts[7], bm.verts[3], bm.verts[1]),
        # Top
        (bm.verts[4], bm.verts[5], bm.verts[1], bm.verts[0]),
        # Bottom
        (bm.verts[2], bm.verts[3], bm.verts[7], bm.verts[6])
    ]

    # Creates faces of the bbox
    for f in faces:
        bm.faces.new(f)

    bm.normal_update()
    bm.to_mesh(me)
    bm.free()

    # Gets or creates a transparent material for the boxes
    mat = bpy.data.materials.get("RVBBox")
    if not mat:
        mat = create_material("RVBBox", COL_BBOX, 0.3)
    me.materials.append(mat)

    ob = bpy.data.objects.new("RVBBox_{}".format(filename), me)
    scene.objects.link(ob)

    # Makes the object transparent
    ob.show_transparent = True
    ob.draw_type = "SOLID"
    ob.show_wire = True

    return ob


def create_sphere(scene, sptype, center, radius, filename):
    if sptype == "BOUNDBALL":
        mname = "RVBoundSphere"
        col = COL_BSPHERE
    elif sptype == "BIGCUBE":
        mname = "RVBigCube"
        col = COL_BCUBE

    center = to_blender_coord(center)
    radius = to_blender_scale(radius)
    if mname not in bpy.data.meshes:
        me = bpy.data.meshes.new(mname)
        bm = bmesh.new()
        # Creates a sphere with the given radius
        bmesh.ops.create_icosphere(bm, subdivisions=3, diameter=1)
        bm.to_mesh(me)
        bm.free()
        # Creates a transparent material for the object
        me.materials.append(create_material(mname, col, 0.3))
        # Makes polygons smooth
        for poly in me.polygons:
            poly.use_smooth = True
    else:
        me = bpy.data.meshes[mname]

    # Links the object and sets position and scale
    ob = bpy.data.objects.new("{}_{}".format(mname, filename), me)
    scene.objects.link(ob)
    ob.location = center
    ob.scale = (radius, radius, radius)

    # Makes the object transparent
    ob.show_transparent = True
    ob.draw_type = "SOLID"
    # ob.show_wire = True

    return ob
