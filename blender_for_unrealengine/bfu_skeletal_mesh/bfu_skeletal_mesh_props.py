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
        'obj.bfu_export_deform_only',
        'obj.bfu_export_skeletal_mesh_as_static_mesh',
        'obj.bfu_create_sub_folder_with_skeletal_mesh_name',
        'obj.bfu_mirror_symmetry_right_side_bones',
        'obj.bfu_use_ue_mannequin_bone_alignment',
    ]
    return preset_values

def get_object_export_deform_only(obj: bpy.types.Object) -> bool:
    if obj:
        return obj.bfu_export_deform_only # type: ignore
    return False


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_skeleton_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Skeleton")

    bpy.types.Object.bfu_export_deform_only = bpy.props.BoolProperty(
        name="Export only deform bones",
        description=(
            "Only write deforming bones" +
            " (and non-deforming ones when they have deforming children)"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )

    bpy.types.Object.bfu_export_skeletal_mesh_as_static_mesh = bpy.props.BoolProperty(
        name="Export as Static Mesh",
        description="If true this mesh will be exported as a Static Mesh",
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )
    
    bpy.types.Object.bfu_create_sub_folder_with_skeletal_mesh_name = bpy.props.BoolProperty(
        name="Create SK Sub Folder",
        description="Create a subfolder with the armature name to avoid asset conflicts during the export. (Recommended)",
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )

    bpy.types.Object.bfu_mirror_symmetry_right_side_bones = bpy.props.BoolProperty(
        name="Revert direction of symmetry right side bones",
        description=(
            "If checked, The right-side bones will be mirrored for mirroring physic object in UE PhysicAsset Editor."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )

    bpy.types.Object.bfu_use_ue_mannequin_bone_alignment = bpy.props.BoolProperty(
        name="Apply bone alignments similar to UE Mannequin.",
        description=(
            "If checked, similar to the UE Mannequin, the leg bones will be oriented upwards, and the pelvis and feet bone will be aligned facing upwards during export."
        ),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_use_ue_mannequin_bone_alignment
    del bpy.types.Object.bfu_mirror_symmetry_right_side_bones
    
    del bpy.types.Object.bfu_create_sub_folder_with_skeletal_mesh_name
    del bpy.types.Object.bfu_export_skeletal_mesh_as_static_mesh

    del bpy.types.Object.bfu_export_deform_only

    del bpy.types.Scene.bfu_skeleton_properties_expanded