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



import bpy
from .. import bfu_ui
from .. import bbpl
from .. import bfu_export_control
from ..bbpl.blender_layout import layout_doc_button
from . import bfu_spline_utils


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


    scene = bpy.context.scene 
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
                
                spline_ui_spline_type = spline_ui_pop.column()
                spline_ui_spline_type.prop(obj, 'bfu_desired_spline_type')
                if obj.bfu_desired_spline_type == "CUSTOM":
                    spline_ui_spline_type.prop(obj, 'bfu_custom_spline_component')
                if bfu_spline_utils.contain_nurbs_spline(obj):
                    resample_resolution = spline_ui_spline_type.row()
                    resample_resolution.prop(obj, 'bfu_spline_resample_resolution')
                    layout_doc_button.add_doc_page_operator(resample_resolution, text="", url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Curve-and-Spline#notes")
                spline_ui_spline_type.enabled = obj.bfu_export_spline_as_static_mesh is False
                spline_ui.operator("object.bfu_copy_active_spline_data", icon="COPYDOWN")


def draw_tools_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene

    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_spline_tools_expanded")
    _, panel = accordion.draw(layout)
    if accordion.is_expend():
        spline_ui = panel.column()
        spline_ui.operator("object.copy_selected_splines_data", icon="COPYDOWN")
    
