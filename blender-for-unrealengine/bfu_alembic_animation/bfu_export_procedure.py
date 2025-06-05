import bpy
from enum import Enum
from typing import List, Tuple, Dict

class BFU_AlembicExportProcedure(str, Enum):
    BLENDER_STANDARD = "blender-standard"

    @staticmethod
    def default() -> "BFU_AlembicExportProcedure":
        return BFU_AlembicExportProcedure.BLENDER_STANDARD

def get_alembic_export_procedure_enum_property_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_AlembicExportProcedure.BLENDER_STANDARD.value,
            "Blender Standard",
            "Standard ALEMBIC.",
            "OUTLINER_OB_FONT",
            1),
        ]

def get_default_alembic_export_procedure() -> str:
    return BFU_AlembicExportProcedure.default().value

def get_object_export_procedure(obj: bpy.types.Object) -> BFU_AlembicExportProcedure:
    for export_type in BFU_AlembicExportProcedure:
        if getattr(obj, "bfu_alembic_export_procedure", None) == export_type.value:
            return export_type
    return BFU_AlembicExportProcedure.default()

def get_alembic_procedure_preset(procedure: BFU_AlembicExportProcedure) -> Dict[str, str | bool]:
    preset: Dict[str, str | bool] = {}
    return preset

def draw_object_export_procedure(layout: bpy.types.UILayout, obj: bpy.types.Object) -> bpy.types.UILayout:
    layout.prop(obj, 'bfu_alembic_export_procedure')  # type: ignore
    return layout

classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore
    
    bpy.types.Object.bfu_alembic_export_procedure = bpy.props.EnumProperty(  # type: ignore
        name="Export Procedure",
        description=(
            "This will define how an Alembic animation should be exported."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        items=get_alembic_export_procedure_enum_property_list(),
        default=get_default_alembic_export_procedure()
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    del bpy.types.Object.bfu_alembic_export_procedure  # type: ignore