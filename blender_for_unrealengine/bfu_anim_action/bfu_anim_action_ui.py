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
from .. import bfu_alembic_animation
from .. import bfu_camera
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
    is_camera = bfu_camera.bfu_camera_utils.is_camera(obj)
    is_alembic_animation = bfu_alembic_animation.bfu_alembic_animation_utils.is_alembic_animation(obj)
    if True not in [is_skeletal_mesh, is_camera, is_alembic_animation]:
        return

    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "ANIM"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_animation_action_properties_expanded")
        if accordion:
            _, panel = accordion.draw(layout)
            if panel:
                if is_skeletal_mesh:
                    # Action list
                    ActionListProperty = panel.column()
                    ActionListProperty.prop(obj, 'bfu_anim_action_export_enum')
                    if obj.bfu_anim_action_export_enum == "export_specific_list":
                        ActionListProperty.template_list(
                            # type and unique id
                            "BFU_UL_ActionExportTarget", "",
                            # pointer to the CollectionProperty
                            obj, "bfu_action_asset_list",
                            # pointer to the active identifier
                            obj, "bfu_active_action_asset_list",
                            maxrows=5,
                            rows=5
                        )
                        UpdateObjActionList = ActionListProperty.row()
                        UpdateObjActionList.operator(
                            "object.updateobjactionlist",
                            icon='RECOVER_LAST')
                        SelectDeselectObjActionList = ActionListProperty.row()
                        SelectDeselectObjActionList.operator("object.selectallobjactionlist")
                        SelectDeselectObjActionList.operator("object.deselectallobjactionlist")
                    if obj.bfu_anim_action_export_enum == "export_specific_prefix":
                        ActionListProperty.prop(obj, 'bfu_prefix_name_to_export')

                # Action Time
                if obj.type != "CAMERA":
                    ActionTimeProperty = panel.column()
                    ActionTimeProperty.enabled = obj.bfu_anim_action_export_enum != "dont_export"
                    ActionTimeProperty.prop(obj, 'bfu_anim_action_start_end_time_enum')
                    if obj.bfu_anim_action_start_end_time_enum == "with_customframes":
                        OfsetTime = ActionTimeProperty.row()
                        OfsetTime.prop(obj, 'bfu_anim_action_custom_start_frame')
                        OfsetTime.prop(obj, 'bfu_anim_action_custom_end_frame')
                    if obj.bfu_anim_action_start_end_time_enum != "with_customframes":
                        OfsetTime = ActionTimeProperty.row()
                        OfsetTime.prop(obj, 'bfu_anim_action_start_frame_offset')
                        OfsetTime.prop(obj, 'bfu_anim_action_end_frame_offset')

                else:
                    panel.label(
                        text=(
                            "Note: animation start/end use scene frames" +
                            " with the camera for the sequencer.")
                        )

                # Nomenclature
                if is_skeletal_mesh:
                    export_anim_naming = panel.column()
                    export_anim_naming.enabled = obj.bfu_anim_action_export_enum != "dont_export"
                    export_anim_naming.prop(obj, 'bfu_anim_naming_type')
                    if obj.bfu_anim_naming_type == "include_custom_name":
                        export_anim_naming_text = export_anim_naming.column()
                        export_anim_naming_text.prop(obj, 'bfu_anim_naming_custom')