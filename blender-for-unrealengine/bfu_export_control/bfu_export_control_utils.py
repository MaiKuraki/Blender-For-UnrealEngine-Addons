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
from typing import List
from .bfu_export_control_type import BFU_ExportTypeEnum



def get_object_export_type(obj: bpy.types.Object) -> BFU_ExportTypeEnum:
    for export_type in BFU_ExportTypeEnum:
        if obj.bfu_export_type == export_type.value:  # type: ignore
            return export_type
    return BFU_ExportTypeEnum.default()

# Check functions

def is_auto(obj: bpy.types.Object) -> bool:
    """
    Check if the object is set to auto export.
    """
    return get_object_export_type(obj) == BFU_ExportTypeEnum.AUTO

def is_export_recursive(obj: bpy.types.Object) -> bool:
    """
    Check if the object is set to export recursively.
    """
    return get_object_export_type(obj) == BFU_ExportTypeEnum.EXPORT_RECURSIVE

def is_not_export_recursive(obj: bpy.types.Object) -> bool:
    """
    Check if the object is not set to export recursively.
    """
    return get_object_export_type(obj) != BFU_ExportTypeEnum.EXPORT_RECURSIVE

def is_auto_or_export_recursive(obj: bpy.types.Object) -> bool:
    """
    Check if the object is set to auto or export recursively.
    """
    return get_object_export_type(obj) in (BFU_ExportTypeEnum.AUTO, BFU_ExportTypeEnum.EXPORT_RECURSIVE)

# Set functions

def set_auto(obj: bpy.types.Object) -> None:
    """
    Set the object to auto export.
    """
    obj.bfu_export_type = BFU_ExportTypeEnum.AUTO.value  # type: ignore

# Objects getters

def get_all_export_recursive_objects() -> List[bpy.types.Object]:
    found_objects: List[bpy.types.Object] = []
    if bpy.context:
        for obj in bpy.context.scene.objects:
            if is_export_recursive(obj):
                found_objects.append(obj)
    return found_objects

def get_all_export_recursive_armatures() ->  List[bpy.types.Object]:
    found_objects: List[bpy.types.Object] = []
    if bpy.context:
        for obj in bpy.context.scene.objects:
            if obj.type == "ARMATURE" and is_export_recursive(obj):  # type: ignore
                found_objects.append(obj)
    return found_objects

