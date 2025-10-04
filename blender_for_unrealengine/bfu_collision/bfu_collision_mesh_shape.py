# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
import numpy
import bmesh
import mathutils
from typing import Any, List, Optional



def calculate_mvbb(coords: numpy.ndarray[Any, numpy.dtype[numpy.float64]]) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]:
    # Calculate the minimum-volume bounding box (MVBB) for the given object.
    # This is a placeholder implementation and should be replaced with actual MVBB calculation logic.
    
    # Center data
    mean = coords.mean(axis=0)
    coords_centered = coords - mean

    # PCA (use transpose so covariance is 3x3)
    cov = numpy.cov(coords_centered.T) # type: ignore
    _, eigvecs = numpy.linalg.eigh(cov) # type: ignore
    
    # Rotation matrix (principal axes)
    rot = eigvecs.T  # shape (3,3)

    # Rotate points into PCA frame
    coords_rot = coords_centered @ rot.T  # shape (N,3)

    # Bounding box in PCA frame
    mins = coords_rot.min(axis=0)
    maxs = coords_rot.max(axis=0)

    # Bounding box in PCA space
    mins = coords_rot.min(axis=0)
    maxs = coords_rot.max(axis=0)

    # 8 corners in PCA space
    corners: numpy.ndarray[Any, numpy.dtype[numpy.float64]] = numpy.array([
        [x, y, z]
        for x in [mins[0], maxs[0]]
        for y in [mins[1], maxs[1]]
        for z in [mins[2], maxs[2]]
    ])

    # Back to original space
    corners_world = corners @ rot + mean
    return corners_world

def apply_mvbb(src_bm: bmesh.types.BMesh, target_bm: bmesh.types.BMesh) -> None:

    # Calculate the minimum-volume bounding box (MVBB) and add its faces to the target BMesh.
    coords: numpy.ndarray[Any, numpy.dtype[numpy.float64]] = numpy.array([v.co for v in src_bm.verts])
    corners_world: numpy.ndarray[Any, numpy.dtype[numpy.float64]] = calculate_mvbb(coords)
    
    # Create verts at corners
    verts = [target_bm.verts.new(corner) for corner in corners_world] # type: ignore
    target_bm.verts.ensure_lookup_table()

    # Define faces by indices of verts (each face = quad)
    faces_idx = [
        (0,2,3,1),  # bottom
        (4,5,7,6),  # top
        (0,1,5,4),  # front
        (2,6,7,3),  # back
        (0,4,6,2),  # left
        (1,3,7,5),  # right
    ]

    new_bound_faces: List[bmesh.types.BMFace] = []
    for f in faces_idx:
        new_bound_faces.append(target_bm.faces.new([verts[i] for i in f]))
    bmesh.ops.recalc_face_normals(target_bm, faces=new_bound_faces)  # type: ignore

def convert_to_box_shape(obj: bpy.types.Object, use_world_space: bool = True, keep_original: bool = False) -> None:
    # Convert obj to Box Shape.
    # keep_original: If True, keep the original mesh vertices and replace them with the box corners.
    # Unreal don't detect the shape as an box if it not perfectly a box.
    # Calculate the minimum-volume bounding box (MVBB) and replace vertices with the box corners.
    mesh = obj.data
    if not isinstance(mesh, bpy.types.Mesh):
        print("Object does not have a mesh, cannot convert to box shape.")
        return
    if mesh.is_editmode:
        print("Object is in edit mode, cannot convert to box shape.")
        return

    src_bm = bmesh.new()
    src_bm.from_mesh(mesh)

    inv_world_matrix: Optional[mathutils.Matrix] = None
    if use_world_space:
        # === Transform vertices into world space ===
        world_matrix = obj.matrix_world.copy()
        inv_world_matrix = world_matrix.inverted()
        for v in src_bm.verts:
            v.co = world_matrix @ v.co

    # === Compute MVBB in world space ===
    if keep_original:
        apply_mvbb(src_bm, src_bm)
        bm = src_bm
    else:
        bm = bmesh.new()
        apply_mvbb(src_bm, bm)

    if use_world_space and inv_world_matrix:
        # === Transform back to local space ===
        for v in bm.verts:
            v.co = inv_world_matrix @ v.co

    # Write back to mesh
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

def convert_to_convex_hull_shape(obj: bpy.types.Object, keep_original: bool = False) -> None:
    # Convert obj to Convex Hull Shape.
    # keep_original: If True, keep the original mesh vertices and add the convex hull around them.
    mesh = obj.data
    if not isinstance(mesh, bpy.types.Mesh):
        print("Object has no mesh, cannot compute convex hull.")
        return
    if obj.mode != 'OBJECT':
        print("Object must be in OBJECT mode.")
        return

    bm = bmesh.new()
    bm.from_mesh(mesh)

    result = bmesh.ops.convex_hull(
        bm,
        input=bm.verts, # type: ignore
        use_existing_faces=False
    )

    if not keep_original:
        # The convex hull operation may leave the original vertices, but since we are
        # using a clean bmesh, only the hull faces exist. Still, let's ensure cleanup.
        geom = set(result.get("geom", []))
        all_geom = set(bm.verts) | set(bm.edges) | set(bm.faces)
        extra_geom = all_geom - geom
        if extra_geom:
            bmesh.ops.delete(bm, geom=list(extra_geom), context='VERTS') # type: ignore

    if bm.faces:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces) # type: ignore

    # Write back to mesh
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
