# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

import string
from pathlib import Path
from typing import Set
import bpy
import shutil
import bmesh
from mathutils import Vector, Euler

def RemoveFolderTree(folder: str) -> None:
    dirpath = Path(folder)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath, ignore_errors=True)

def get_root_bone_parent(bone: bpy.types.Bone) -> bpy.types.Bone:
    if bone.parent is not None:  # type: ignore
        return get_root_bone_parent(bone.parent)
    return bone

def get_first_deform_bone_parent(bone: bpy.types.Bone) -> bpy.types.Bone:
    if bone.parent is not None:  # type: ignore
        if bone.use_deform is True:
            return bone
        else:
            return get_first_deform_bone_parent(bone.parent)
    return bone

def SetCollectionUse(collection: bpy.types.Collection) -> None:
    # Set if collection is hide and selectable
    collection.hide_viewport = False
    collection.hide_select = False
    if bpy.context.view_layer:
        layer_collection = bpy.context.view_layer.layer_collection
        if collection.name in layer_collection.children:
            layer_collection.children[collection.name].hide_viewport = False
        else:
            print(collection.name, " not found in view_layer.layer_collection")


def convert_to_convex_hull_shape(obj: bpy.types.Object, recalc_face_normals: bool = False) -> None:
    # Convert obj to Convex Hull
    mesh = obj.data
    if isinstance(mesh, bpy.types.Mesh):
        if not mesh.is_editmode:
            bm = bmesh.new()
            bm.from_mesh(mesh)  # Mesh to Bmesh
            bmesh.ops.convex_hull(
                bm, input=bm.verts,  # type: ignore
                use_existing_faces=True
            )
            if recalc_face_normals:
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces)  # type: ignore
            bm.to_mesh(mesh)  # BMesh to Mesh

def convert_to_box_shape(obj: bpy.types.Object) -> None:
    # Convert obj to Box Shape.
    # Calculate the bounding box of the mesh and replace all mesh with a perfect box.
    if not isinstance(obj.data, bpy.types.Mesh):
        return

    if obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Sauvegarder la rotation actuelle
    original_rotation = obj.rotation_euler.copy()

    # Appliquer la rotation temporairement
    obj.rotation_euler = Euler((0.0, 0.0, 0.0), 'XYZ')

    # Calcul du bounding box en local (plus fiable maintenant)
    bbox = [Vector(corner) for corner in obj.bound_box]
    min_corner = Vector((min(v[0] for v in bbox),
                         min(v[1] for v in bbox),
                         min(v[2] for v in bbox)))
    max_corner = Vector((max(v[0] for v in bbox),
                         max(v[1] for v in bbox),
                         max(v[2] for v in bbox)))
    size = max_corner - min_corner
    center = (min_corner + max_corner) * 0.5

    # Générer un cube parfait
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(obj.data)
    bm.free()

    # Positionner l'objet
    obj.location += center
    obj.scale = size



    # Restaurer la rotation d'origine
    obj.rotation_euler = original_rotation




def verifi_dirs(directory: Path) -> bool:
    # Check and create a folder if it does not exist
    if not directory.exists():
        directory.mkdir()
        return True
    return False


def valid_folder_name(directory: str) -> str:
    # https://gist.github.com/seanh/93666
    # Normalizes string, removes non-alpha characters
    # File name use

    illegal_chars = r':*?"<>|'
    directory = ''.join(c for c in directory if c not in illegal_chars)

    return directory


def valid_file_name(filename: str) -> str:
    # https://gist.github.com/seanh/93666
    # Normalizes string, removes non-alpha characters
    # File name use

    illegal_chars = r'\/:*?"<>|'
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    filename = ''.join(c for c in filename if c not in illegal_chars)
    filename = ''.join(c for c in filename if c in valid_chars)

    return filename


def get_if_action_can_associate_str_set(action: bpy.types.Action, bone_names: Set[str]) -> bool:
    # for group in action.groups:
    #    for fcurve in group.channels:
    for fcurve in action.fcurves:
        s = fcurve.data_path
        start = s.find('["')
        end = s.rfind('"]')
        if start > 0 and end > 0:
            substring = s[start+2:end]
            if substring in bone_names:
                return True
    return False

def get_if_action_can_associate_armature(action: bpy.types.Action, armature: bpy.types.Armature) -> bool:
    # for group in action.groups:
    #    for fcurve in group.channels:
    for fcurve in action.fcurves:
        s = fcurve.data_path
        start = s.find('["')
        end = s.rfind('"]')
        if start > 0 and end > 0:
            substring = s[start+2:end]
            if substring in armature.bones:
                return True
    return False


def get_surface_area(obj: bpy.types.Object) -> float:
    if isinstance(obj.data, bpy.types.Mesh):
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        area = sum(f.calc_area() for f in bm.faces)
        bm.free()
        return area
    return -1.0


def set_windows_clipboard(text: str) -> None:
    if bpy.context.window_manager:
        bpy.context.window_manager.clipboard = text
    # bpy.context.window_manager.clipboard.encode('utf8')
