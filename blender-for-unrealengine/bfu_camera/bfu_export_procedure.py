import bpy
from enum import Enum
from typing import List, Tuple, Dict
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum

class BFU_CameraExportProcedure(str, Enum):
    UE_STANDARD = "ue-standard"
    BLENDER_STANDARD = "blender-standard"

    @staticmethod
    def default() -> "BFU_CameraExportProcedure":
        return BFU_CameraExportProcedure.BLENDER_STANDARD

def get_camera_export_procedure_enum_property_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_CameraExportProcedure.UE_STANDARD.value,
            "UE Standard",
            "Modified fbx I/O for Unreal Engine",
            "ARMATURE_DATA",
            1),
        (BFU_CameraExportProcedure.BLENDER_STANDARD.value,
            "Blender Standard",
            "Standard fbx I/O.",
            "ARMATURE_DATA",
            2),
        ]

def get_default_camera_export_procedure() -> str:
    return BFU_CameraExportProcedure.default().value

def get_obj_export_file_type(obj: bpy.types.Object) -> BFU_FileTypeEnum:
    return get_export_file_type(get_object_export_procedure(obj))

def get_export_file_type(procedure: BFU_CameraExportProcedure) -> BFU_FileTypeEnum:
    return BFU_FileTypeEnum.FBX

def get_object_export_procedure(obj: bpy.types.Object) -> BFU_CameraExportProcedure:
    for export_type in BFU_CameraExportProcedure:
        if getattr(obj, "bfu_camera_export_procedure", None) == export_type.value:
            return export_type
    return BFU_CameraExportProcedure.default()

def get_camera_procedure_preset(procedure: BFU_CameraExportProcedure) -> Dict[str, str | bool]:
    preset: Dict[str, str | bool] = {}
    return preset

def draw_object_export_procedure(layout: bpy.types.UILayout, obj: bpy.types.Object) -> bpy.types.UILayout:
    layout.prop(obj, 'bfu_camera_export_procedure')  # type: ignore
    return layout

classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore

    bpy.types.Object.bfu_camera_export_procedure = bpy.props.EnumProperty(  # type: ignore
        name="Export Procedure",
        description=(
            "This will define how a camera should be exported."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        items=get_camera_export_procedure_enum_property_list(),
        default=get_default_camera_export_procedure()
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    del bpy.types.Object.bfu_camera_export_procedure  # type: ignore