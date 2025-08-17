# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl
from .. import bfu_skeletal_mesh
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
    is_skeletal_mesh = bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "ANIM"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_animation_nla_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():
            # NLA
            if is_skeletal_mesh:
                NLAAnim = panel.row()
                NLAAnim.prop(obj, 'bfu_anim_nla_use')
                NLAAnimChild = NLAAnim.column()
                NLAAnimChild.enabled = obj.bfu_anim_nla_use
                NLAAnimChild.prop(obj, 'bfu_anim_nla_export_name')

            # NLA Time
            if obj.type != "CAMERA":
                NLATimeProperty = panel.column()
                NLATimeProperty.enabled = obj.bfu_anim_nla_use
                NLATimeProperty.prop(obj, 'bfu_anim_nla_start_end_time_enum')
                if obj.bfu_anim_nla_start_end_time_enum == "with_customframes":
                    OfsetTime = NLATimeProperty.row()
                    OfsetTime.prop(obj, 'bfu_anim_nla_custom_start_frame')
                    OfsetTime.prop(obj, 'bfu_anim_nla_custom_end_frame')
                if obj.bfu_anim_nla_start_end_time_enum != "with_customframes":
                    OfsetTime = NLATimeProperty.row()
                    OfsetTime.prop(obj, 'bfu_anim_nla_start_frame_offset')
                    OfsetTime.prop(obj, 'bfu_anim_nla_end_frame_offset')