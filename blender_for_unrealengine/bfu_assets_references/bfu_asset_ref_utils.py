# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
import os
import fnmatch
from .. import bbpl
from .. import bfu_unreal_utils
from .. import bfu_utils



def get_skeleton_search_ref(obj: bpy.types.Object):
    scene = bpy.context.scene
   
    if(obj.bfu_engine_ref_skeleton_search_mode) == "auto":
        return bfu_unreal_utils.get_predicted_skeleton_ref(obj)

    elif(obj.bfu_engine_ref_skeleton_search_mode) == "custom_name":
        name = bfu_utils.clean_filename_for_unreal(obj.bfu_engine_ref_skeleton_custom_name)
        target_ref = os.path.join("/" + scene.bfu_unreal_import_module + "/", scene.bfu_unreal_import_location, obj.bfu_export_folder_name, name+"."+name)
        target_ref = target_ref.replace('\\', '/')
        return target_ref

    elif(obj.bfu_engine_ref_skeleton_search_mode) == "custom_path_name":
        name = bfu_utils.clean_filename_for_unreal(obj.bfu_engine_ref_skeleton_custom_name)
        target_ref = os.path.join("/" + scene.bfu_unreal_import_module + "/", obj.bfu_engine_ref_skeleton_custom_path, name+"."+name)
        target_ref = target_ref.replace('\\', '/')
        return target_ref

    elif(obj.bfu_engine_ref_skeleton_search_mode) == "custom_reference":
        target_ref = obj.bfu_engine_ref_skeleton_custom_ref.replace('\\', '/')
        return target_ref
    else:
        return None

def get_skeletal_mesh_search_ref(obj: bpy.types.Object):
    scene = bpy.context.scene
   
    if(obj.bfu_engine_ref_skeletal_mesh_search_mode) == "auto":
        return bfu_unreal_utils.get_predicted_skeletal_mesh_ref(obj)

    elif(obj.bfu_engine_ref_skeletal_mesh_search_mode) == "custom_name":
        name = bfu_utils.clean_filename_for_unreal(obj.bfu_engine_ref_skeletal_mesh_custom_name)
        target_ref = os.path.join("/" + scene.bfu_unreal_import_module + "/", scene.bfu_unreal_import_location, obj.bfu_export_folder_name, name+"."+name)
        target_ref = target_ref.replace('\\', '/')
        return target_ref

    elif(obj.bfu_engine_ref_skeletal_mesh_search_mode) == "custom_path_name":
        name = bfu_utils.clean_filename_for_unreal(obj.bfu_engine_ref_skeletal_mesh_custom_name)
        target_ref = os.path.join("/" + scene.bfu_unreal_import_module + "/", obj.bfu_engine_ref_skeletal_mesh_custom_path, name+"."+name)
        target_ref = target_ref.replace('\\', '/')
        return target_ref

    elif(obj.bfu_engine_ref_skeletal_mesh_search_mode) == "custom_reference":
        target_ref = obj.bfu_engine_ref_skeletal_mesh_custom_ref.replace('\\', '/')
        return target_ref
    else:
        return None
