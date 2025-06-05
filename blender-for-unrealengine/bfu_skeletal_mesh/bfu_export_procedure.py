import bpy
from enum import Enum
from typing import List, Tuple, Dict
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum

class BFU_SkeletonExportProcedure(str, Enum):
    UE_STANDARD = "ue-standard"
    BLENDER_STANDARD = "blender-standard"

    @staticmethod
    def default() -> "BFU_SkeletonExportProcedure":
        return BFU_SkeletonExportProcedure.BLENDER_STANDARD

def get_skeleton_export_procedure_enum_property_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_SkeletonExportProcedure.UE_STANDARD.value,
            "UE Standard",
            "Modified fbx I/O for Unreal Engine",
            "ARMATURE_DATA",
            1),
        (BFU_SkeletonExportProcedure.BLENDER_STANDARD.value,
            "Blender Standard",
            "Standard fbx I/O.",
            "ARMATURE_DATA",
            2)
        ]

def get_default_skeleton_export_procedure() -> str:
    return BFU_SkeletonExportProcedure.default().value

def get_object_export_procedure(obj: bpy.types.Object) -> BFU_SkeletonExportProcedure:
    for export_type in BFU_SkeletonExportProcedure:
        if obj.bfu_skeleton_export_procedure == export_type.value:  # type: ignore
            return export_type
    return BFU_SkeletonExportProcedure.default()

def get_obj_export_file_type(obj: bpy.types.Object) -> BFU_FileTypeEnum:
    return get_export_file_type(get_object_export_procedure(obj))

def get_export_file_type(procedure: BFU_SkeletonExportProcedure) -> BFU_FileTypeEnum:
    return BFU_FileTypeEnum.FBX

def get_obj_skeleton_fbx_procedure_preset(obj: bpy.types.Object) -> Dict[str, str | bool]:
    return get_skeleton_procedure_preset(get_object_export_procedure(obj))

def get_skeleton_procedure_preset(procedure: BFU_SkeletonExportProcedure) -> Dict[str, str | bool]:
    preset: Dict[str, str | bool] = {}
    if procedure == BFU_SkeletonExportProcedure.UE_STANDARD:
        preset["use_space_transform"] = True
        preset["axis_forward"] = '-Z'
        preset["axis_up"] = 'Y'
        preset["primary_bone_axis"] = 'X'
        preset["secondary_bone_axis"] = '-Z'
    elif procedure == BFU_SkeletonExportProcedure.BLENDER_STANDARD:
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