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
        'obj.bfu_move_to_center_for_export',
        'obj.bfu_rotate_to_zero_for_export',
        'obj.bfu_additional_location_for_export',
        'obj.bfu_additional_rotation_for_export',
        'obj.bfu_export_global_scale',
        'obj.bfu_override_procedure_preset',
        'obj.bfu_fbx_export_use_space_transform',
        'obj.bfu_fbx_export_axis_forward',
        'obj.bfu_fbx_export_axis_up',
        'obj.bfu_fbx_export_primary_bone_axis',
        'obj.bfu_fbx_export_secondary_bone_axis',
        'obj.bfu_export_with_meta_data',
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

    bpy.types.Scene.bfu_object_advanced_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Object Advanced Properties")

    bpy.types.Object.bfu_move_to_center_for_export = bpy.props.BoolProperty(
        name="Move to center",
        description=(
            "If true use object origin else use scene origin." +
            " | If true the mesh will be moved to the center" +
            " of the scene for export." +
            " (This is used so that the origin of the fbx file" +
            " is the same as the mesh in blender)"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )

    bpy.types.Object.bfu_rotate_to_zero_for_export = bpy.props.BoolProperty(
        name="Rotate to zero",
        description=(
            "If true use object rotation else use scene rotation." +
            " | If true the mesh will use zero rotation for export."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )

    bpy.types.Object.bfu_additional_location_for_export = bpy.props.FloatVectorProperty(
        name="Additional location",
        description=(
            "This will add a additional absolute location to the mesh"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        subtype="TRANSLATION",
        default=(0, 0, 0)
        )

    bpy.types.Object.bfu_additional_rotation_for_export = bpy.props.FloatVectorProperty(
        name="Additional rotation",
        description=(
            "This will add a additional absolute rotation to the mesh"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        subtype="EULER",
        default=(0, 0, 0)
        )

    bpy.types.Object.bfu_export_global_scale = bpy.props.FloatProperty(
        name="Global scale",
        description="Scale, change is not recommended with SkeletalMesh.",
        override={'LIBRARY_OVERRIDABLE'},
        default=1.0
        )
    
    bpy.types.Object.bfu_override_procedure_preset = bpy.props.BoolProperty(
        name="Override Export Preset",
        description="If true override the export precedure preset.",
        override={'LIBRARY_OVERRIDABLE'},
        default=False,
        )

    bpy.types.Object.bfu_fbx_export_use_space_transform = bpy.props.BoolProperty(
        name="Use Space Transform",
        default=True,
        )

    bpy.types.Object.bfu_fbx_export_axis_forward = bpy.props.EnumProperty(
        name="Axis Forward",
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ('X', "X Forward", ""),
            ('Y', "Y Forward", ""),
            ('Z', "Z Forward", ""),
            ('-X', "-X Forward", ""),
            ('-Y', "-Y Forward", ""),
            ('-Z', "-Z Forward", ""),
            ],
        default='-Z',
        )

    bpy.types.Object.bfu_fbx_export_axis_up = bpy.props.EnumProperty(
        name="Axis Up",
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ('X', "X Up", ""),
            ('Y', "Y Up", ""),
            ('Z', "Z Up", ""),
            ('-X', "-X Up", ""),
            ('-Y', "-Y Up", ""),
            ('-Z', "-Z Up", ""),
            ],
        default='Y',
        )

    bpy.types.Object.bfu_fbx_export_primary_bone_axis = bpy.props.EnumProperty(
        name="Primary Axis Bone",
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
            ('-X', "-X", ""),
            ('-Y', "-Y", ""),
            ('-Z', "-Z", ""),
            ],
        default='Y',
        )

    bpy.types.Object.bfu_fbx_export_secondary_bone_axis = bpy.props.EnumProperty(
        name="Secondary Axis Bone",
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
            ('-X', "-X", ""),
            ('-Y', "-Y", ""),
            ('-Z', "-Z", ""),
            ],
        default='X',
        )

    bpy.types.Object.bfu_export_with_meta_data = bpy.props.BoolProperty(
        name=bpy.app.translations.pgettext("Export meta data", "interface.export_with_meta_data_name"),
        description=bpy.app.translations.pgettext("Process export with meta data.", "tooltips.export_with_meta_data_desc"),
        override={'LIBRARY_OVERRIDABLE'},
        default=False,
        )
    





def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_export_with_meta_data

    del bpy.types.Object.bfu_fbx_export_secondary_bone_axis
    del bpy.types.Object.bfu_fbx_export_primary_bone_axis
    del bpy.types.Object.bfu_fbx_export_axis_up
    del bpy.types.Object.bfu_fbx_export_axis_forward
    del bpy.types.Object.bfu_fbx_export_use_space_transform
    del bpy.types.Object.bfu_override_procedure_preset

    del bpy.types.Object.bfu_export_global_scale
    del bpy.types.Object.bfu_additional_rotation_for_export
    del bpy.types.Object.bfu_additional_location_for_export
    del bpy.types.Object.bfu_rotate_to_zero_for_export
    del bpy.types.Object.bfu_move_to_center_for_export

    del bpy.types.Scene.bfu_object_advanced_properties_expanded