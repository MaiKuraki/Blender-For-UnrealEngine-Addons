# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bfu_basics
from .. import bfu_ui
from .. import bbpl
from .. import bfu_alembic_animation
from .. import bfu_export_control
from .. import bfu_addon_prefs

def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):

    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Hide filters
    if obj is None:
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    if bfu_alembic_animation.bfu_alembic_animation_utils.is_alembic_animation(obj):
        return
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "ANIM"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_animation_action_advanced_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():
            transformProp = panel.column()
            transformProp.enabled = obj.bfu_anim_action_export_enum != "dont_export"
            transformProp.prop(obj, "bfu_move_action_to_center_for_export")
            transformProp.prop(obj, "bfu_rotate_action_to_zero_for_export")