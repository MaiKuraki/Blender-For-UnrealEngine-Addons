import bpy
from bfu_spline.bfu_spline_props import BFU_SplineDesiredComponent

def get_spline_unreal_component(spline: bpy.types.Object) -> str:
    # Engin ref:
    spline_type = spline.bfu_desired_spline_type  # type: ignore
    if spline_type == BFU_SplineDesiredComponent.SPLINE.value:
        return "/Script/Engine.SplineComponent"
    else:
        return spline.bfu_custom_spline_component  # type: ignore
    