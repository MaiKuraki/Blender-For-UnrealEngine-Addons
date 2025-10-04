# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl
from .. import bfu_static_mesh
from .. import bfu_skeletal_mesh
from .. import bfu_export_control
from .. import bfu_addon_prefs
from .. import bfu_lod



def draw_ui_object(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Hide filters
    is_static_mesh = bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj)
    is_skeletal_mesh = bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)
    if addon_prefs.useGeneratedScripts is False:
        return
    if not bfu_utils.draw_proxy_propertys(obj):
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    if is_static_mesh == False and is_skeletal_mesh == False:
        return

    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "MISC"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_object_collision_properties_expanded")
        if accordion:
            _, panel = accordion.draw(layout)
            if accordion.is_expend() and panel:
                # StaticMesh prop
                if is_static_mesh:
                    if not bfu_lod.bfu_lod_props.get_object_export_as_lod_mesh(obj):
                        auto_generate_collision = panel.row()
                        auto_generate_collision.prop(
                            obj,
                            'bfu_auto_generate_collision'
                            )
                        collision_trace_flag = panel.row()
                        collision_trace_flag.prop(
                            obj,
                            'bfu_collision_trace_flag'
                            )
                # SkeletalMesh prop
                if is_skeletal_mesh:
                    if not bfu_lod.bfu_lod_props.get_object_export_as_lod_mesh(obj):
                        create_physics_asset = panel.row()
                        create_physics_asset.prop(obj, "bfu_create_physics_asset")
                        enable_skeletal_mesh_per_poly_collision = panel.row()
                        enable_skeletal_mesh_per_poly_collision.prop(obj, 'bfu_enable_skeletal_mesh_per_poly_collision')


def draw_tools_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    
    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_tools_collision_properties_expanded")
    if accordion:
        _, panel = accordion.draw(layout)
        if accordion.is_expend() and panel:

            # Check draw collision settings
            setting_panel = panel.row()
            setting_panel.prop(scene, "bfu_keep_original_geometry", icon='MOD_PHYSICS')
            setting_panel.prop(scene, "bfu_use_world_space_for_collision", icon='WORLD')
            
            # Draw create new collider panel
            draw_how_create_collision_from_selection(panel, context)
            create_buttons_ui = panel.row().split(factor=0.80)
            create_static_collision_buttons = create_buttons_ui.column()
            create_static_collision_buttons.operator("object.createboxcollisionfromselection", icon='MESH_CUBE')
            create_static_collision_buttons.operator("object.createconvexcollisionfromselection", icon='MESH_ICOSPHERE')
            create_static_collision_buttons.operator("object.createcapsulecollisionfromselection", icon='MESH_CAPSULE')
            create_static_collision_buttons.operator("object.createspherecollisionfromselection", icon='MESH_UVSPHERE')

            # Draw convert to collider panel
            ready_for_convert_collider = draw_and_get_ready_for_convert_collider(panel, context)
            convert_buttons_ui = panel.row().split(factor=0.80)
            convert_static_collision_buttons = convert_buttons_ui.column()
            convert_static_collision_buttons.enabled = ready_for_convert_collider
            convert_static_collision_buttons.operator("object.converttoboxcollision", icon='MESH_CUBE')
            convert_static_collision_buttons.operator("object.converttoconvexcollision", icon='MESH_ICOSPHERE')
            convert_static_collision_buttons.operator("object.converttocapsulecollision", icon='MESH_CAPSULE')
            convert_static_collision_buttons.operator("object.converttospherecollision", icon='MESH_UVSPHERE')

            # Draw button toggle visibility panel
            sub_tool_panel = panel.column()
            sub_tool_panel.operator("object.toggle_collision_visibility", text="Toggle Collision Visibility", icon='HIDE_OFF')
            sub_tool_panel.operator("object.select_collision_from_current_selection", text="Select Collision from Current Selection", icon='RESTRICT_SELECT_OFF')


def draw_how_create_collision_from_selection(layout: bpy.types.UILayout, context: bpy.types.Context) -> None:
    if not bbpl.utils.active_mode_is("OBJECT"):
        layout.label(text="Switch to Object Mode.", icon='INFO')
    else:
        if bbpl.utils.found_type_in_selection("MESH", False):
            if bbpl.utils.active_type_is_not("ARMATURE"):
                layout.label(text="Click on button for create collision from selection.", icon='INFO')
        else:
            layout.label(text="Please select the mesh object(s) on which to create the collider.", icon='INFO')


def draw_and_get_ready_for_convert_collider(layout: bpy.types.UILayout, context: bpy.types.Context) -> bool:
    if not bbpl.utils.active_mode_is("OBJECT"):
        layout.label(text="Switch to Object Mode.", icon='INFO')
    else:
        if bbpl.utils.found_type_in_selection("MESH", False):
            if bbpl.utils.active_type_is_not("ARMATURE") and len(bpy.context.selected_objects) > 1:
                layout.label(text="Click on button for convert to collider.", icon='INFO')
                return True
            else:
                layout.label(text="Select with [SHIFT] the collider owner.", icon='INFO')
        else:
            layout.label(text="Please select your collider mesh object(s). Active should be the owner.", icon='INFO')
    return False