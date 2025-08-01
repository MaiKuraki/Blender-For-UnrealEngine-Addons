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
from .bfu_export_control_type import BFU_ExportTypeEnum


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