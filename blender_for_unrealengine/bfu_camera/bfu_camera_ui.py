# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------



import bpy
import math
from .. import bfu_basics
from .. import bfu_ui
from .. import bbpl
from .. import languages
from .. import bfu_export_control
from . import bfu_camera_utils
from . import bfu_camera_write_paste_commands

def draw_ui_object_camera(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
  

    if obj is None:
        return
    
    if obj.type != "CAMERA":
        return

    scene = bpy.context.scene 
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_camera_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expanded():
            camera_ui = panel.column()
            if obj.type == "CAMERA":
                camera_ui_pop = camera_ui.column()

                export_procedure_prop = camera_ui_pop.column()
                export_procedure_prop.prop(obj, 'bfu_camera_export_procedure')

                camera_ui_pop.prop(obj, 'bfu_desired_camera_type')
                if obj.bfu_desired_camera_type == "CUSTOM":
                    camera_ui_pop.prop(obj, 'bfu_custom_camera_actor')
                    camera_ui_pop.prop(obj, 'bfu_custom_camera_default_actor')
                    camera_ui_pop.prop(obj, 'bfu_custom_camera_component')
                camera_ui_fix_axis = camera_ui_pop.box()
                camera_ui_fix_axis_prop = camera_ui_fix_axis.row()
                camera_ui_fix_axis_prop.prop(obj, 'bfu_fix_axis_flippings')
                bbpl.blender_layout.layout_doc_button.add_doc_page_operator(camera_ui_fix_axis_prop, text="", url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Camera-Axis")
                if obj.bfu_fix_axis_flippings:
                    camera_ui_fix_axis.prop(obj, 'bfu_fix_axis_flippings_warp_target', text="")

                    invalid = False
                    warp_target_degrees = [math.degrees(v) for v in obj.bfu_fix_axis_flippings_warp_target]
                    tolerance = 1e-4

                    for axis_value in obj.bfu_fix_axis_flippings_warp_target:
                        if axis_value == 0.0:
                            invalid = True
                            camera_ui_fix_axis.label(
                                text="Error: Axis value cannot be 0!",
                                icon='ERROR'
                            )
                            break  # Stop check

                    if not invalid:
                        for axis_value in warp_target_degrees:
                            if abs(axis_value % 90) > tolerance:
                                camera_ui_fix_axis.label(
                                    text=(
                                        f"Warning: {axis_value:.1f}° is not a multiple of 90°. "
                                        "It is recommended to use 360° or multiples of 90°."
                                    ),
                                    icon='INFO'
                                )

                camera_ui_pop.enabled = bfu_export_control.bfu_export_control_utils.is_export_recursive(obj)
                camera_ui.operator("object.bfu_copy_active_camera_data", icon="COPYDOWN")


def draw_tools_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene

    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_camera_tools_expanded")
    if accordion:
        _, panel = accordion.draw(layout)
        if panel:
            camera_ui = panel.column()
            camera_ui.operator("object.copy_selected_cameras_data", icon="COPYDOWN")
        
