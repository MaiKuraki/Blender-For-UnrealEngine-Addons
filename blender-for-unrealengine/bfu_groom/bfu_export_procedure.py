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
from enum import Enum
from typing import List, Tuple, Dict
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum

class BFU_GroomExportProcedure(str, Enum):
    STANDARD_ALEMBIC = "standard_alembic"

    @staticmethod
    def default() -> "BFU_GroomExportProcedure":
        return BFU_GroomExportProcedure.STANDARD_ALEMBIC

def get_groom_export_procedure_enum_property_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_GroomExportProcedure.STANDARD_ALEMBIC.value,
            "Blender Standard",
            "Standard ALEMBIC.",
            "OUTLINER_OB_FONT",
            1),
        ]

def get_default_groom_export_procedure() -> str:
    return BFU_GroomExportProcedure.default().value

def get_obj_export_file_type(obj: bpy.types.Object) -> BFU_FileTypeEnum:
    return get_export_file_type(get_object_export_procedure(obj))

def get_export_file_type(procedure: BFU_GroomExportProcedure) -> BFU_FileTypeEnum:
    return BFU_FileTypeEnum.ALEMBIC

def get_object_export_procedure(obj: bpy.types.Object) -> BFU_GroomExportProcedure:
    for export_type in BFU_GroomExportProcedure:
        if getattr(obj, "bfu_groom_export_procedure", None) == export_type.value:
            return export_type
    return BFU_GroomExportProcedure.default()

def get_groom_procedure_preset(procedure: BFU_GroomExportProcedure) -> Dict[str, str | bool]:
    preset: Dict[str, str | bool] = {}
    return preset

def draw_object_export_procedure(layout: bpy.types.UILayout, obj: bpy.types.Object) -> bpy.types.UILayout:
    layout.prop(obj, 'bfu_groom_export_procedure')  # type: ignore
    return layout

classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore
    
    bpy.types.Object.bfu_groom_export_procedure = bpy.props.EnumProperty(  # type: ignore
        name="Export Procedure",
        description=(
            "This will define how a groom animation should be exported."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        items=get_groom_export_procedure_enum_property_list(),
        default=get_default_groom_export_procedure()
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    del bpy.types.Object.bfu_groom_export_procedure  # type: ignore