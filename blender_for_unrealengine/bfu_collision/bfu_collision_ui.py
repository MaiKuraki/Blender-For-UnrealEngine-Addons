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
            # Draw user tips and check can use buttons
            ready_for_convert_collider = False
            if not bbpl.utils.active_mode_is("OBJECT"):
                panel.label(text="Switch to Object Mode.", icon='INFO')
            else:
                if bbpl.utils.found_type_in_selection("MESH", False):
                    if bbpl.utils.active_type_is_not("ARMATURE") and len(bpy.context.selected_objects) > 1:
                        panel.label(text="Click on button for convert to collider.", icon='INFO')
                        ready_for_convert_collider = True
                    else:
                        panel.label(text="Select with [SHIFT] the collider owner.", icon='INFO')
                else:
                    panel.label(text="Please select your collider Object(s). Active should be the owner.", icon='INFO')
                
            # Draw buttons
            convertButtons = panel.row().split(factor=0.80)
            convertStaticCollisionButtons = convertButtons.column()
            convertStaticCollisionButtons.enabled = ready_for_convert_collider
            convertStaticCollisionButtons.operator("object.converttoboxcollision", icon='MESH_CUBE')
            convertStaticCollisionButtons.operator("object.converttoconvexcollision", icon='MESH_ICOSPHERE')
            convertStaticCollisionButtons.operator("object.converttocapsulecollision", icon='MESH_CAPSULE')
            convertStaticCollisionButtons.operator("object.converttospherecollision", icon='MESH_UVSPHERE')
            panel.operator("object.toggle_collision_visibility", text="Toggle Collision Visibility", icon='HIDE_OFF')