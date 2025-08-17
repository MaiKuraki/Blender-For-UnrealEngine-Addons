# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bfu_ui
from .. import bfu_export_control
from . import bfu_static_mesh_utils

def draw_ui_object(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):

    if obj is None:
        return
    
    scene = bpy.context.scene 
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        if scene.bfu_object_properties_expanded.is_expend():
            if bfu_static_mesh_utils.is_static_mesh(obj):
                if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):

                    StaticMeshUI = layout.column()
                    export_procedure_prop = StaticMeshUI.column()
                    export_procedure_prop.prop(obj, 'bfu_static_export_procedure')


    if scene.bfu_object_advanced_properties_expanded.is_expend():
        if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):
            pass
            

def draw_ui_scene(layout: bpy.types.UILayout):
    pass