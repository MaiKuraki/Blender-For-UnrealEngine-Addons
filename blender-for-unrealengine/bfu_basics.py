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
import bpy
import shutil
import bmesh

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


def ConvertToConvexHull(obj: bpy.types.Object, recalc_face_normals: bool = False) -> None:
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


def get_if_action_can_associate_bone(action: bpy.types.Action, bone_names: list[str]) -> bool:
    for group in action.groups:
        for fcurve in group.channels:
            s = fcurve.data_path
            start = s.find('["')
            end = s.rfind('"]')
            if start > 0 and end > 0:
                substring = s[start+2:end]
                if substring in bone_names:
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
