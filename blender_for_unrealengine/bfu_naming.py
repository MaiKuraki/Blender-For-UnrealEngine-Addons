# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================


import bpy
from typing import TYPE_CHECKING
from . import bfu_basics


def get_collection_file_name(collection: bpy.types.Collection, desired_name: str = "", fileType: str = ".fbx") -> str:
    # Generate assset file name for skeletal mesh
    
    if bpy.context is None:
        return ""

    scene = bpy.context.scene
    if TYPE_CHECKING:
        class FakeScene(bpy.types.Scene):
            bfu_static_mesh_prefix_export_name: str = ""
            bfu_static_mesh_prefix_export_name: str = ""
        scene = FakeScene()

    if desired_name:
        return bfu_basics.valid_file_name(scene.bfu_static_mesh_prefix_export_name + desired_name + fileType)
    return bfu_basics.valid_file_name(scene.bfu_static_mesh_prefix_export_name + collection.name + fileType)


def get_nonlinear_animation_file_name(obj: bpy.types.Object, fileType: str = ".fbx") -> str:
    # Generate action file name
    
    if bpy.context is None:
        return ""

    scene = bpy.context.scene

    if TYPE_CHECKING:
        class FakeScene(bpy.types.Scene):
            bfu_anim_prefix_export_name: str = ""
        scene = FakeScene()

    if TYPE_CHECKING:
        class FakeObject(bpy.types.Object):
            bfu_anim_naming_type: str = ""
            bfu_anim_naming_custom: str = ""
            bfu_anim_nla_export_name: str = ""
        obj = FakeObject()

    if obj.bfu_anim_naming_type == "include_armature_name":
        armature_name: str = obj.name+"_"
    elif obj.bfu_anim_naming_type == "action_name":
        armature_name: str = ""
    elif obj.bfu_anim_naming_type == "include_custom_name":
        armature_name: str = obj.bfu_anim_naming_custom+"_"
    else:
        armature_name: str = ""

    return bfu_basics.valid_file_name(scene.bfu_anim_prefix_export_name+armature_name+obj.bfu_anim_nla_export_name+fileType)
