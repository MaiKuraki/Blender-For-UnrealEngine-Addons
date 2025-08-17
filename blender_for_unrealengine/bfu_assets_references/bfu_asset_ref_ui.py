# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bfu_skeletal_mesh
from .. import bfu_export_control
from .. import bfu_addon_prefs


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
    
    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Hide filters
    if obj is None:
        return
    if not bfu_utils.draw_proxy_propertys(obj):
        return
    if addon_prefs.useGeneratedScripts is False:
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    is_skeletal_mesh = bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)
    if is_skeletal_mesh is False:
        return
    
    # Draw UI
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):   
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_engine_ref_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():
            # SkeletalMesh prop
            if is_skeletal_mesh:
                if not obj.bfu_export_as_lod_mesh:
                    unreal_engine_refs = panel.column()
                    draw_skeleton_prop(unreal_engine_refs, obj)
                    draw_skeletal_mesh_prop(unreal_engine_refs, obj)


def draw_skeleton_prop(layout: bpy.types.UILayout, obj: bpy.types.Object):
    layout.prop(obj, "bfu_engine_ref_skeleton_search_mode")
    if obj.bfu_engine_ref_skeleton_search_mode == "auto":
        pass
    if obj.bfu_engine_ref_skeleton_search_mode == "custom_name":
        layout.prop(obj, "bfu_engine_ref_skeleton_custom_name")
    if obj.bfu_engine_ref_skeleton_search_mode == "custom_path_name":
        layout.prop(obj, "bfu_engine_ref_skeleton_custom_path")
        layout.prop(obj, "bfu_engine_ref_skeleton_custom_name")
    if obj.bfu_engine_ref_skeleton_search_mode == "custom_reference":
        layout.prop(obj, "bfu_engine_ref_skeleton_custom_ref")

def draw_skeletal_mesh_prop(layout: bpy.types.UILayout, obj: bpy.types.Object):
    layout.prop(obj, "bfu_engine_ref_skeletal_mesh_search_mode")
    if obj.bfu_engine_ref_skeletal_mesh_search_mode == "auto":
        pass
    if obj.bfu_engine_ref_skeletal_mesh_search_mode == "custom_name":
        layout.prop(obj, "bfu_engine_ref_skeletal_mesh_custom_name")
    if obj.bfu_engine_ref_skeletal_mesh_search_mode == "custom_path_name":
        layout.prop(obj, "bfu_engine_ref_skeletal_mesh_custom_path")
        layout.prop(obj, "bfu_engine_ref_skeletal_mesh_custom_name")
    if obj.bfu_engine_ref_skeletal_mesh_search_mode == "custom_reference":
        layout.prop(obj, "bfu_engine_ref_skeletal_mesh_custom_ref")