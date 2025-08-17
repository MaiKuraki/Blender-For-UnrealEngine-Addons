# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


from typing import List
import bpy
from .. import bbpl

def get_preset_values() -> List[str]:
    preset_values = [
            'obj.bfu_create_physics_asset',
            'obj.bfu_auto_generate_collision',
            'obj.bfu_collision_trace_flag',
            'obj.bfu_enable_skeletal_mesh_per_poly_collision',
        ]
    return preset_values

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_object_collision_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Collision")
    bpy.types.Scene.bfu_tools_collision_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Collision")

    # ImportUI
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxImportUI/index.html

    bpy.types.Object.bfu_create_physics_asset = bpy.props.BoolProperty(
        name="Create PhysicsAsset",
        description="If checked, create a PhysicsAsset when is imported",
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )


    bpy.types.Object.bfu_auto_generate_collision = bpy.props.BoolProperty(
        name="Auto Generate Collision",
        description=(
            "If checked, collision will automatically be generated" +
            " (ignored if custom collision is imported or used)."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=True,
        )


    bpy.types.Object.bfu_collision_trace_flag = bpy.props.EnumProperty(
        name="Collision Complexity",
        description="Collision Trace Flag",
        override={'LIBRARY_OVERRIDABLE'},
        # Vania python
        # https://docs.unrealengine.com/en-US/PythonAPI/class/CollisionTraceFlag.html
        # C++ API
        # https://api.unrealengine.com/INT/API/Runtime/Engine/PhysicsEngine/ECollisionTraceFlag/index.html
        items=[
            ("CTF_UseDefault",
                "Project Default",
                "Create only complex shapes (per poly)." +
                " Use complex shapes for all scene queries" +
                " and collision tests." +
                " Can be used in simulation for" +
                " static shapes only" +
                " (i.e can be collided against but not moved" +
                " through forces or velocity.",
                1),
            ("CTF_UseSimpleAndComplex",
                "Use Simple And Complex",
                "Use project physics settings (DefaultShapeComplexity)",
                2),
            ("CTF_UseSimpleAsComplex",
                "Use Simple as Complex",
                "Create both simple and complex shapes." +
                " Simple shapes are used for regular scene queries" +
                " and collision tests. Complex shape (per poly)" +
                " is used for complex scene queries.",
                3),
            ("CTF_UseComplexAsSimple",
                "Use Complex as Simple",
                "Create only simple shapes." +
                " Use simple shapes for all scene" +
                " queries and collision tests.",
                4)
            ]
        )

    bpy.types.Object.bfu_enable_skeletal_mesh_per_poly_collision = bpy.props.BoolProperty(
        name="Enable Per-Poly Collision",
        description="Enable per-polygon collision for Skeletal Mesh",
        default=False
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_enable_skeletal_mesh_per_poly_collision

    del bpy.types.Object.bfu_collision_trace_flag
    del bpy.types.Object.bfu_auto_generate_collision
    del bpy.types.Object.bfu_create_physics_asset

    del bpy.types.Scene.bfu_tools_collision_properties_expanded
    del bpy.types.Scene.bfu_object_collision_properties_expanded