# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
from typing import TYPE_CHECKING
from pathlib import Path
from .. import bfu_basics

def get_import_location()-> Path:
    """Get the path to import assets into Unreal Engine."""
    
    scene = bpy.context.scene
    if TYPE_CHECKING:
        class FakeScene(bpy.types.Scene):
            bfu_unreal_import_module: str = ""
            bfu_unreal_import_location: str = ""
        scene = FakeScene()

    unreal_import_module = bfu_basics.valid_folder_name(scene.bfu_unreal_import_module)
    unreal_import_location = bfu_basics.valid_folder_name(scene.bfu_unreal_import_location)
    return Path(unreal_import_module) / unreal_import_location

def get_obj_import_location(obj: bpy.types.Object) -> Path:
    """Get the path to import an object into Unreal Engine."""
    
    if TYPE_CHECKING:
        class FakeObject(bpy.types.Object): 
            bfu_export_folder_name: str = ""
        obj = FakeObject()

    return get_import_location() / bfu_basics.valid_folder_name(obj.bfu_export_folder_name)

def get_obj_export_folder(obj: bpy.types.Object) -> str:
    """Get the export folder name for an object."""
    
    if TYPE_CHECKING:
        class FakeObject(bpy.types.Object): 
            bfu_export_folder_name: str = ""
        obj = FakeObject()

    return bfu_basics.valid_folder_name(obj.bfu_export_folder_name)

def get_col_import_location(col: bpy.types.Collection) -> Path:
    """Get the path to import a collection into Unreal Engine."""

    if TYPE_CHECKING:
        class FakeCollection(bpy.types.Collection): 
            bfu_export_folder_name: str = ""
        col = FakeCollection()

    return get_import_location() / bfu_basics.valid_folder_name(col.bfu_export_folder_name)

def get_col_export_folder(col: bpy.types.Collection) -> str:
    """Get the export folder name for a collection."""
    
    if TYPE_CHECKING:
        class FakeCollection(bpy.types.Collection): 
            bfu_export_folder_name: str = ""
        col = FakeCollection()

    return bfu_basics.valid_folder_name(col.bfu_export_folder_name)