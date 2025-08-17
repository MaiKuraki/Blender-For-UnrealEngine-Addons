# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


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
