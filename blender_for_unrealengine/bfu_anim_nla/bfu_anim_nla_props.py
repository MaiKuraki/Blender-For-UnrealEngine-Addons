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
        'obj.bfu_anim_nla_use',
        'obj.bfu_anim_nla_export_name',
        'obj.bfu_anim_nla_start_end_time_enum',
        'obj.bfu_anim_nla_start_frame_offset',
        'obj.bfu_anim_nla_end_frame_offset',
        'obj.bfu_anim_nla_custom_start_frame',
        'obj.bfu_anim_nla_custom_end_frame',
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

    bpy.types.Scene.bfu_animation_nla_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="NLA Properties")

    bpy.types.Object.bfu_anim_nla_use = bpy.props.BoolProperty(
        name="Export NLA (Nonlinear Animation)",
        description=(
            "If checked, exports the all animation of the scene with the NLA " +
            "(Don't work with Auto-Rig Pro for the moment.)"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )
    
    bpy.types.Object.bfu_anim_nla_export_name = bpy.props.StringProperty(
        name="NLA export name",
        description="Export NLA name (Don't work with Auto-Rig Pro for the moment.)",
        override={'LIBRARY_OVERRIDABLE'},
        maxlen=64,
        default="NLA_animation",
        subtype='FILE_NAME'
        )

    bpy.types.Object.bfu_anim_nla_start_end_time_enum = bpy.props.EnumProperty(
        name="NLA Start/End Time",
        description="Set when animation starts and end",
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ("with_sceneframes",
                "Scene time",
                "Time will be equal to the scene time",
                "SCENE_DATA",
                1),
            ("with_customframes",
                "Custom time",
                'The time of all the animations of this object' +
                ' is defined by you.' +
                ' Use "bfu_anim_action_custom_start_frame" and "bfu_anim_action_custom_end_frame"',
                "HAND",
                2),
            ]
        )
    
    bpy.types.Object.bfu_anim_nla_start_frame_offset = bpy.props.IntProperty(
        name="Offset at start frame",
        description="Offset for the start frame.",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
    )

    bpy.types.Object.bfu_anim_nla_end_frame_offset = bpy.props.IntProperty(
        name="Offset at end frame",
        description=(
            "Offset for the end frame. +1" +
            " is recommended for the sequences | 0 is recommended" +
            " for UnrealEngine cycles | -1 is recommended for Sketchfab cycles"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=0
    )

    bpy.types.Object.bfu_anim_nla_custom_start_frame = bpy.props.IntProperty(
        name="Custom start time",
        description="Set when animation start",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
        )

    bpy.types.Object.bfu_anim_nla_custom_end_frame = bpy.props.IntProperty(
        name="Custom end time",
        description="Set when animation end",
        override={'LIBRARY_OVERRIDABLE'},
        default=1
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_anim_nla_custom_end_frame
    del bpy.types.Object.bfu_anim_nla_custom_start_frame
    del bpy.types.Object.bfu_anim_nla_end_frame_offset
    del bpy.types.Object.bfu_anim_nla_start_frame_offset
    del bpy.types.Object.bfu_anim_nla_export_name
    del bpy.types.Object.bfu_anim_nla_use

    del bpy.types.Scene.bfu_animation_nla_properties_expanded