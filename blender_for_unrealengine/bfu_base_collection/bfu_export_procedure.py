# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
from enum import Enum
from typing import List, Tuple, Dict, Union
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum

class BFU_CollectionExportProcedure(str, Enum):
    CUSTOM_FBX_EXPORT = "custom_fbx_export"
    STANDARD_FBX = "standard_fbx"
    STANDARD_GLTF = "standard_gltf"

    @staticmethod
    def default() -> "BFU_CollectionExportProcedure":
        return BFU_CollectionExportProcedure.STANDARD_FBX

def get_collection_export_procedure_enum_property_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_CollectionExportProcedure.CUSTOM_FBX_EXPORT.value,
            "UE Standard",
            "Modified fbx I/O for Unreal Engine",
            "OUTLINER_OB_GROUP_INSTANCE",
            1),
        (BFU_CollectionExportProcedure.STANDARD_FBX.value,
            "Blender Standard",
            "Standard fbx I/O.",
            "OUTLINER_OB_GROUP_INSTANCE",
            2),
        ]

def get_default_collection_export_procedure() -> str:
    return BFU_CollectionExportProcedure.default().value

def get_col_export_type(col: bpy.types.Collection) -> BFU_FileTypeEnum:
    return get_export_file_type(get_col_export_procedure(col))

def get_export_file_type(procedure: BFU_CollectionExportProcedure) -> BFU_FileTypeEnum:
    return BFU_FileTypeEnum.FBX

def get_col_export_procedure(col: bpy.types.Collection) -> BFU_CollectionExportProcedure:
    for procedure in BFU_CollectionExportProcedure:
        if getattr(col, "bfu_collection_export_procedure", None) == procedure.value:
            return procedure

    print(f"Warning: Object {col.name} has unknown export procedure '{col.bfu_collection_export_procedure}'. Falling back to default export procedure...")  # type: ignore
    return BFU_CollectionExportProcedure.default()

def get_col_procedure_preset(procedure: BFU_CollectionExportProcedure) -> Dict[str, Union[str, bool]]:
    preset: Dict[str, Union[str, bool]] = {}
    return preset

def draw_col_export_procedure(layout: bpy.types.UILayout, col: bpy.types.Collection) -> bpy.types.UILayout:
    layout.prop(col, 'bfu_collection_export_procedure')  # type: ignore
    return layout

def get_preset_values() -> List[str]:
    preset_values = [
        'col.bfu_collection_export_procedure',
        ]
    return preset_values

classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore

    bpy.types.Collection.bfu_collection_export_procedure = bpy.props.EnumProperty(  # type: ignore
        name="Export Procedure",
        description=(
            "This will define how a collection should be exported."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        items=get_collection_export_procedure_enum_property_list(),
        default=get_default_collection_export_procedure()
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    del bpy.types.Collection.bfu_collection_export_procedure  # type: ignore