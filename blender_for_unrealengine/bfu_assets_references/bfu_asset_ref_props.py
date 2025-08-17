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
        'obj.bfu_engine_ref_skeleton_search_mode',
        'obj.bfu_engine_ref_skeleton_custom_path',
        'obj.bfu_engine_ref_skeleton_custom_name',
        'obj.bfu_engine_ref_skeleton_custom_ref',

        'obj.bfu_engine_ref_skeletal_mesh_search_mode',
        'obj.bfu_engine_ref_skeletal_mesh_custom_path',
        'obj.bfu_engine_ref_skeletal_mesh_custom_name',
        'obj.bfu_engine_ref_skeletal_mesh_custom_ref'
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

    bpy.types.Scene.bfu_engine_ref_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Engine Refs")


    bpy.types.Object.bfu_engine_ref_skeleton_search_mode = bpy.props.EnumProperty(
        name="Skeleton Ref",
        description='Specify the skeleton location in Unreal',
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ("auto",
                "Auto",
                "...",
                1),
            ("custom_name",
                "Custom name",
                "Default location with custom name",
                2),
            ("custom_path_name",
                "Custom path and name",
                "Set the custom light map resolution",
                3),
            ("custom_reference",
                "custom reference",
                "Reference from Unreal.",
                4)
            ]
        )

    bpy.types.Object.bfu_engine_ref_skeleton_custom_path = bpy.props.StringProperty(
        name="",
        description="The path of the Skeleton in Unreal. Skeleton not the skeletal mesh.",
        override={'LIBRARY_OVERRIDABLE'},
        default="ImportedBlenderAssets"
        )

    bpy.types.Object.bfu_engine_ref_skeleton_custom_name = bpy.props.StringProperty(
        name="",
        description="The name of the Skeleton in Unreal. Skeleton not the skeletal mesh.",
        override={'LIBRARY_OVERRIDABLE'},
        default="SK_MySketon_Skeleton"
        )

    bpy.types.Object.bfu_engine_ref_skeleton_custom_ref = bpy.props.StringProperty(
        name="",
        description=(
            "The full reference of the Skeleton in Unreal. " +
            "(Use right clic on asset and copy reference.)"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default="SkeletalMesh'/Game/ImportedBlenderAssets/SK_MySketon_Skeleton.SK_MySketon_Skeleton'"
        )


    bpy.types.Object.bfu_engine_ref_skeletal_mesh_search_mode = bpy.props.EnumProperty(
        name="Skeletal Mesh Ref",
        description='Specify the Skeletal Mesh location in Unreal',
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ("auto",
                "Auto",
                "...",
                1),
            ("custom_name",
                "Custom name",
                "Default location with custom name",
                2),
            ("custom_path_name",
                "Custom path and name",
                "Set the custom light map resolution",
                3),
            ("custom_reference",
                "custom reference",
                "Reference from Unreal.",
                4)
            ]
        )

    bpy.types.Object.bfu_engine_ref_skeletal_mesh_custom_path = bpy.props.StringProperty(
        name="",
        description="The path of the Skeletal Mesh in Unreal. Skeletal Mesh not the skeletal mesh.",
        override={'LIBRARY_OVERRIDABLE'},
        default="ImportedBlenderAssets"
        )

    bpy.types.Object.bfu_engine_ref_skeletal_mesh_custom_name = bpy.props.StringProperty(
        name="",
        description="The name of the Skeletal Mesh in Unreal. Skeletal Mesh not the skeletal mesh.",
        override={'LIBRARY_OVERRIDABLE'},
        default="SKM_MySkeletalMesh"
        )

    bpy.types.Object.bfu_engine_ref_skeletal_mesh_custom_ref = bpy.props.StringProperty(
        name="",
        description=(
            "The full reference of the Skeletal Mesh in Unreal. " +
            "(Use right clic on asset and copy reference.)"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default="SkeletalMesh'/Game/ImportedBlenderAssets/SKM_MySkeletalMesh.SKM_MySkeletalMesh'"
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_engine_ref_skeleton_custom_ref
    del bpy.types.Object.bfu_engine_ref_skeleton_custom_name
    del bpy.types.Object.bfu_engine_ref_skeleton_custom_path
    del bpy.types.Object.bfu_engine_ref_skeleton_search_mode

    del bpy.types.Object.bfu_engine_ref_skeletal_mesh_custom_ref
    del bpy.types.Object.bfu_engine_ref_skeletal_mesh_custom_name
    del bpy.types.Object.bfu_engine_ref_skeletal_mesh_custom_path
    del bpy.types.Object.bfu_engine_ref_skeletal_mesh_search_mode

    del bpy.types.Scene.bfu_engine_ref_properties_expanded