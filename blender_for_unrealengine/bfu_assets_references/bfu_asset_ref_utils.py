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
