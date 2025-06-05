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
from typing import List, Tuple
from enum import Enum


class BFU_ExportTypeEnum(Enum):
    AUTO = "auto"
    EXPORT_RECURSIVE = "export_recursive"
    DONT_EXPORT = "dont_export"

    @staticmethod
    def default() -> "BFU_ExportTypeEnum":
        return BFU_ExportTypeEnum.AUTO

def get_blender_default() -> str:
    return BFU_ExportTypeEnum.default().value

def get_blender_enum_property_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_ExportTypeEnum.AUTO.value,
            "Auto",
            "Export with the parent if the parents is \"Export recursive\"",
            "BOIDS",
            1),
        (BFU_ExportTypeEnum.EXPORT_RECURSIVE.value,
            "Export recursive",
            "Export self object and all children",
            "KEYINGSET",
            2),
        (BFU_ExportTypeEnum.DONT_EXPORT.value,
            "Not exported",
            "Will never export",
            "CANCEL",
            3),
        ]

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

def get_all_export_recursive_objects() -> list[bpy.types.Object]:
    found_objects: list[bpy.types.Object] = []
    if bpy.context:
        for obj in bpy.context.scene.objects:
            if is_export_recursive(obj):
                found_objects.append(obj)
    return found_objects

def get_all_export_recursive_armatures() -> list[bpy.types.Object]:
    found_objects: list[bpy.types.Object] = []
    if bpy.context:
        for obj in bpy.context.scene.objects:
            if obj.type == "ARMATURE" and is_export_recursive(obj):  # type: ignore
                found_objects.append(obj)
    return found_objects

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore

    bpy.types.Object.bfu_export_type = bpy.props.EnumProperty(  # type: ignore
        name="Export type",
        description="Export procedure",
        override={'LIBRARY_OVERRIDABLE'},
        items=get_blender_enum_property_list(),
        default=get_blender_default(),
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    del bpy.types.Object.bfu_export_type # type: ignore