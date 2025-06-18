# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================


from typing import Optional
import bpy
from .. import bfu_ui
from .. import bbpl
from .. import bfu_export_control
from ..bbpl.blender_layout import layout_doc_button
from . import bfu_spline_utils
from . import bfu_spline_data
from .bfu_spline_data import BFU_SimpleSpline

def draw_debug_panel(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):

    pre_bake_spline = bfu_spline_data.BFU_MultiSplineTracks()
    if isinstance(obj.data, bpy.types.Curve):
        pre_bake_spline.add_spline_to_evaluate(obj)
        pre_bake_spline.evaluate_all_splines(preview=True)

        debug_panel = layout.column(align=True)
        debug_panel.label(text="Spline Debug Panel", icon="INFO")
        debug_panel.label(text=f"Number of splines: {len(obj.data.splines)}")
        total_points = 0
        active_spline: Optional[bpy.types.Spline] = None
        active_spline_index = -1
        active_point = -1
        for x, spline in enumerate(obj.data.splines):
            if spline.type == 'NURBS':
                total_points += len(spline.points)
            elif spline.type == 'BEZIER':
                total_points += len(spline.bezier_points)
                for i, bp in enumerate(spline.bezier_points):
                    if bp.select_control_point:
                        active_spline = spline
                        active_spline_index = x
                        active_point = i
            elif spline.type == 'POLY':
                total_points += len(spline.points)


        debug_panel.label(text=f"Total points: {total_points}")
        debug_panel.label(text=f"--------------------")
        debug_panel.label(text=f"Current active spline: {active_spline_index}")
        debug_panel.label(text=f"Current active point: {active_point}")
        if active_spline is not None:
            debug_panel.label(text=f"--------------------")
            debug_panel.label(text=f"In Unreal Engine:")
            debug_panel.label(text=f"Input Key: {active_point}")
            simple_spline: BFU_SimpleSpline = pre_bake_spline.evaluate_splines[obj.name].simple_splines[active_spline_index]
            simple_point = simple_spline.spline_points[active_point]
            debug_panel.label(text=f"Location: {simple_point.get_ue_position()}")
            debug_panel.label(text=f"Rotation: {simple_point.get_human_readable_rotation(unreal_format=True)}")
            debug_panel.label(text=f"Scale: {simple_point.get_ue_scale()}")
    else:
        debug_panel = layout.column(align=True)
        debug_panel.label(text="No spline data available", icon="ERROR")
        return

def draw_general_ui_object(layout: bpy.types.UILayout, obj: bpy.types.Object):
    if bpy.context is None:
        return

    if obj is None:
        return
    
    if obj.type != "CURVE":
        return
    
    scene = bpy.context.scene 
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_object_properties_expanded")
        if accordion.is_expend():
            if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):
                if not obj.bfu_export_as_alembic_animation:
                    skeletal_mesh_ui = layout.column()
                    # Show asset type
                    skeletal_mesh_ui.prop(obj, "bfu_export_spline_as_static_mesh")

def draw_ui_object_spline(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
  
    if obj is None:
        return
    
    if obj.type != "CURVE":
        return

    show_spline_debug_panel = True

    scene = context.scene 
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_spline_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():
            spline_ui = panel.column()
            if obj.type == "CURVE":
                spline_ui_pop = spline_ui.column()
                spline_ui_as_static_mesh = spline_ui_pop.column()
                spline_ui_as_static_mesh.prop(obj, 'bfu_export_spline_as_static_mesh')
                spline_ui_as_static_mesh.enabled = bfu_export_control.bfu_export_control_utils.is_export_recursive(obj)
                
                # Show spline type
                spline_ui_spline_type = spline_ui_pop.column()
                spline_ui_spline_type.prop(obj, 'bfu_desired_spline_type')
                if obj.bfu_desired_spline_type == "CUSTOM":
                    spline_ui_spline_type.prop(obj, 'bfu_custom_spline_component')
                if bfu_spline_utils.contain_nurbs_spline(obj):
                    resample_resolution = spline_ui_spline_type.row()
                    resample_resolution.prop(obj, 'bfu_spline_resample_resolution')
                    layout_doc_button.add_doc_page_operator(
                        layout=resample_resolution, 
                        url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Curve-and-Spline#notes",
                        text=""
                    )
                spline_ui_spline_type.enabled = obj.bfu_export_spline_as_static_mesh is False
                
                # Spline scale
                spline_ui_spline_vector_scale = spline_ui_pop.row()
                spline_ui_spline_vector_scale.prop(scene, 'bfu_spline_vector_scale', text="Spline Vector Scale")

                # Spline buttons
                copy_spline_buttons = spline_ui.row(align=True)
                copy_spline_buttons.operator("object.bfu_copy_active_spline_data", icon="COPYDOWN")
                bbpl.blender_layout.layout_doc_button.functions.add_doc_page_operator(
                    layout=copy_spline_buttons,
                    url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Curve-and-Spline#import-with-copypaste",
                    text=""
                )

                # Current spline point debug panel
                if show_spline_debug_panel:
                    draw_debug_panel(spline_ui, context, obj)



def draw_tools_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene

    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_spline_tools_expanded")
    _, panel = accordion.draw(layout)
    if accordion.is_expend():
        spline_ui = panel.column()
        spline_ui.operator("object.copy_selected_splines_data", icon="COPYDOWN")
    
