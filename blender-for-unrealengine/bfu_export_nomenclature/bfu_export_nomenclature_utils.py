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
from typing import TYPE_CHECKING
from pathlib import Path
from .. import bfu_basics

def get_import_location()-> Path:
    """Get the path to import assets into Unreal Engine."""

    if bpy.context is None:
        return Path()
    
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