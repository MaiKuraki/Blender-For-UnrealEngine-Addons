# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import os
import bpy
from . import bfu_utils

def get_predicted_skeleton_name(obj: bpy.types.Object) -> str:
    # Get the predicted skeleton name in Unreal Engine
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")

    return scene.bfu_skeleton_prefix_export_name + bfu_utils.clean_filename_for_unreal(obj.name) + "_Skeleton"

def get_predicted_skeleton_path(obj: bpy.types.Object) -> str:
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")

    ref_path = os.path.join("/" + scene.bfu_unreal_import_module + "/", scene.bfu_unreal_import_location, obj.bfu_export_folder_name)
    ref_path = ref_path.replace('\\', '/')
    return ref_path

def get_predicted_skeleton_ref(obj: bpy.types.Object) -> str:
    name = get_predicted_skeleton_name(obj)
    path = get_predicted_skeleton_path(obj)
    ref_path = os.path.join(path, f"{name}.{name}")
    ref_path = ref_path.replace('\\', '/')
    return f"/Script/Engine.Skeleton'{ref_path}'"

def get_predicted_skeletal_mesh_name(obj: bpy.types.Object) -> str:
    # Get the predicted SkeletalMesh name in Unreal Engine
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")
    
    return scene.bfu_skeletal_mesh_prefix_export_name + bfu_utils.clean_filename_for_unreal(obj.name)

def get_predicted_skeletal_mesh_path(obj: bpy.types.Object) -> str:
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")

    ref_path = os.path.join("/" + scene.bfu_unreal_import_module + "/", scene.bfu_unreal_import_location, obj.bfu_export_folder_name)
    ref_path = ref_path.replace('\\', '/')
    return ref_path

def get_predicted_skeletal_mesh_ref(obj: bpy.types.Object) -> str:
    name = get_predicted_skeletal_mesh_name(obj)
    path = get_predicted_skeletal_mesh_path(obj)
    ref_path = os.path.join(path, f"{name}.{name}")
    ref_path = ref_path.replace('\\', '/')
    return f"/Script/Engine.SkeletalMesh'{ref_path}'"

def generate_name_for_unreal_engine(desired_name: str, current_name: str = "") -> str:
    # Generate a new name with suffix number

    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")

    clean_desired_name = desired_name

    def is_valid_name(tested_name: str) -> bool:
        tested_name_without_start = tested_name[len(clean_desired_name):]
        parts = tested_name_without_start.split("_")

        # Ensure the name has a suffix and the suffix is numeric
        if len(parts) == 1 or not parts[-1].isnumeric():
            return False
        
        # Special case for checking against the current name
        if current_name and tested_name == current_name:
            return True

        # Ensure no existing object uses this name
        for obj in scene.objects:
            if tested_name == obj.name:
                return False

        return True

    # Check if the desired name itself is valid and unique
    if is_valid_name(clean_desired_name):
        return clean_desired_name

    # Attempt to append a numeric suffix to make the name unique
    for num in range(10000):
        new_name = f"{clean_desired_name}_{num:02d}"  # Pads number with leading zeros
        if is_valid_name(new_name):
            return new_name

    raise ValueError("ERROR: No valid name found within the given constraints.")
