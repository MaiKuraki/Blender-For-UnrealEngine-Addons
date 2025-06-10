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

class BFU_SkeletonExportProcedure(str, Enum):
    CUSTOM_FBX_EXPORT = "custom_fbx_export"
    STANDARD_FBX = "standard_fbx"
    STANDARD_GLTF = "standard_gltf"

    @staticmethod
    def default() -> "BFU_SkeletonExportProcedure":
        return BFU_SkeletonExportProcedure.STANDARD_FBX

def get_skeleton_export_procedure_enum_property_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value,
            "UE Standard (FBX)",
            "Modified fbx I/O for Unreal Engine",
            "OUTLINER_OB_GROUP_INSTANCE",
            1),
        (BFU_SkeletonExportProcedure.STANDARD_FBX.value,
            "Blender Standard (FBX)",
            "Standard fbx I/O.",
            "OUTLINER_OB_GROUP_INSTANCE",
            2),
        (BFU_SkeletonExportProcedure.STANDARD_GLTF.value,
            "Blender Standard (glTF 2.0)",
            "Standard glTF 2.0.",
            "OUTLINER_OB_GROUP_INSTANCE",
            3),
    ]

def get_default_skeleton_export_procedure() -> str:
    return BFU_SkeletonExportProcedure.default().value

def get_object_export_procedure(obj: bpy.types.Object) -> BFU_SkeletonExportProcedure:
    for procedure in BFU_SkeletonExportProcedure:
        if obj.bfu_skeleton_export_procedure == procedure.value:  # type: ignore
            return procedure

    print(f"Warning: Object {obj.name} has unknown export procedure '{obj.bfu_skeleton_export_procedure}'. Falling back to default export procedure...")  # type: ignore
    return BFU_SkeletonExportProcedure.default()

def get_obj_export_file_type(obj: bpy.types.Object) -> BFU_FileTypeEnum:
    return get_export_file_type(get_object_export_procedure(obj))

def get_export_file_type(procedure: BFU_SkeletonExportProcedure) -> BFU_FileTypeEnum:
    if procedure.value == BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value:
        return BFU_FileTypeEnum.FBX
    elif procedure.value == BFU_SkeletonExportProcedure.STANDARD_FBX.value:
        return BFU_FileTypeEnum.FBX
    elif procedure.value == BFU_SkeletonExportProcedure.STANDARD_GLTF.value:
        return BFU_FileTypeEnum.GLTF

def is_fbx_file_export(obj: bpy.types.Object) -> bool:
    return get_obj_export_file_type(obj) == BFU_FileTypeEnum.FBX

def get_obj_skeleton_fbx_procedure_preset(obj: bpy.types.Object) -> Dict[str, str | bool]:
    return get_skeleton_procedure_preset(get_object_export_procedure(obj))

def get_skeleton_procedure_preset(procedure: BFU_SkeletonExportProcedure) -> Dict[str, str | bool]:
    preset: Dict[str, str | bool] = {}
    if procedure.value == BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value:
        preset["use_space_transform"] = True
        preset["axis_forward"] = '-Z'
        preset["axis_up"] = 'Y'
        preset["primary_bone_axis"] = 'X'
        preset["secondary_bone_axis"] = '-Z'
    elif procedure.value == BFU_SkeletonExportProcedure.STANDARD_FBX.value:
        preset["use_space_transform"] = True
        preset["axis_forward"] = '-Z'
        preset["axis_up"] = 'Y'
        preset["primary_bone_axis"] = 'Y'
        preset["secondary_bone_axis"] = 'X'
    return preset

def draw_object_export_procedure(layout: bpy.types.UILayout, obj: bpy.types.Object) -> bpy.types.UILayout:
    layout.prop(obj, 'bfu_skeleton_export_procedure')  # type: ignore
    return layout


classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore

    bpy.types.Object.bfu_skeleton_export_procedure = bpy.props.EnumProperty(  # type: ignore
        name="Export Procedure",
        description=(
            "This will define how a skeleton should be exported."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        items=get_skeleton_export_procedure_enum_property_list(),
        default=get_default_skeleton_export_procedure()
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    del bpy.types.Object.bfu_skeleton_export_procedure  # type: ignore