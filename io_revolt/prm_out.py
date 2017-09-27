"""
PRM EXPORT
Meshes used for cars, game objects and track instances.
"""
if "bpy" in locals():
    import imp
    imp.reload(common)
    imp.reload(rvstruct)
    imp.reload(img_in)

import os
import bpy
import bmesh
from mathutils import Color, Vector
from . import common
from . import rvstruct
from . import img_in

from .common import *


def export_file(filepath, scene):
    obj = scene.objects.active
    print("Exporting PRM for {}...".format(obj.name))
    meshes = []

    # Checks if other LoDs are present
    if "|q" in obj.data.name:
        print("LODs present.")
        meshes = get_all_lod(obj.data.name.split('|')[0])
        print([m.name for m in meshes])
    else:
        print("No LOD present.")
        meshes.append(obj.data)

    # Exports all meshes to the PRM file
    with open(filepath, "wb") as file:
        for me in meshes:
            print("Exporting mesh {} of {}".format(
                meshes.index(me), len(meshes)))
            # Exports the mesh as a PRM object
            prm = export_mesh(me, obj, scene, filepath)
            # Writes the PRM object to a file
            prm.write(file)


def export_mesh(me, obj, scene, filepath):
    props = scene.revolt
    # Creates a bmesh from the supplied mesh
    bm = bmesh.new()
    bm.from_mesh(me)

    # Applies the object scale if enabled
    if props.apply_scale:
        bmesh.ops.scale(
            bm,
            vec=obj.scale,
            space=obj.matrix_world,
            verts=bm.verts
        )

    # Applies the object rotation if enabled
    if props.apply_rotation:
        bmesh.ops.rotate(
            bm,
            cent=obj.location,
            matrix=obj.rotation_euler.to_matrix(),
            space=obj.matrix_world,
            verts=bm.verts
        )

    num_ngons = triangulate_ngons(bm)
    if scene.revolt.triangulate_ngons > 0:
        print("Triangulated {} n-gons".format(num_ngons))

    # Gets layers
    uv_layer = bm.loops.layers.uv.get("UVMap")
    tex_layer = bm.faces.layers.tex.get("UVMap")
    vc_layer = bm.loops.layers.color.get("Col")
    va_layer = bm.loops.layers.color.get("Alpha")
    texnum_layer = bm.faces.layers.int.get("Texture Number")
    type_layer = (bm.faces.layers.int.get("Type") or
                  bm.faces.layers.int.new("Type"))

    # Creates an empty PRM structure
    prm = rvstruct.PRM()

    prm.polygon_count = len(bm.faces)
    prm.vertex_count = len(bm.verts)

    for face in bm.faces:
        poly = rvstruct.Polygon()
        is_quad = len(face.verts) > 3

        # Sets the quad flag on the polygon
        if is_quad:
            face[type_layer] |= FACE_QUAD

        poly.type = face[type_layer] & FACE_PROP_MASK

        # Gets the texture number from the integer layer if setting enabled
        # use_tex_num is the only way to achieve no texture
        if scene.revolt.use_tex_num and texnum_layer:
            poly.texture = face[texnum_layer]
        # Falls back to texture if not enabled or texnum layer not found
        elif tex_layer and face[tex_layer] and face[tex_layer].image:
            poly.texture = texture_to_int(face[tex_layer].image.name)
        # Uses 'A' texture instead
        else:
            poly.texture = 0

        # Sets vertex indices for the polygon
        vert_order = [2, 1, 0, 3] if not is_quad else [3, 2, 1, 0]
        for i in vert_order:
            if i < len(face.verts):
                poly.vertex_indices.append(face.verts[i].index)
            else:
                # Fills up unused indices with 0s
                poly.vertex_indices.append(0)

        # write the vertex colors
        for i in vert_order:
            if i < len(face.verts):
                # Gets color from the channel or falls back to a default value
                white = Color((1, 1, 1))
                color = face.loops[i][vc_layer] if vc_layer else white
                alpha = face.loops[i][va_layer] if va_layer else white
                col = rvstruct.Color(color=(int(color.r * 255),
                                            int(color.g * 255),
                                            int(color.b * 255)),
                                     alpha=int((alpha.v) * 255))
                poly.colors.append(col)
            else:
                # Writes opaque white
                col = rvstruct.Color(color=(255, 255, 255), alpha=255)
                poly.colors.append(col)

        # Writes the UV
        for i in vert_order:
            if i < len(face.verts) and uv_layer:
                uv = face.loops[i][uv_layer].uv
                poly.uv.append(rvstruct.UV(uv=(uv[0], 1 - uv[1])))
            else:
                poly.uv.append(rvstruct.UV())

        prm.polygons.append(poly)

    # export vertex positions and normals
    for vertex in bm.verts:
        coord = to_revolt_coord((vertex.co[0],
                                 vertex.co[1],
                                 vertex.co[2]))
        normal = to_revolt_axis((vertex.normal[0],
                                 vertex.normal[1],
                                 vertex.normal[2]))
        rvvert = rvstruct.Vertex()
        rvvert.position = rvstruct.Vector(data=coord)
        rvvert.normal = rvstruct.Vector(data=normal)
        prm.vertices.append(rvvert)

    return prm
