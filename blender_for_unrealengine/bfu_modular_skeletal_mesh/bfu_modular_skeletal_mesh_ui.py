# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bbpl
from .. import bfu_addon_prefs
from .. import bfu_ui
from .. import bfu_skeletal_mesh
from .. import bfu_modular_skeletal_mesh
from .. import bfu_export_control


def draw_general_ui_object(layout: bpy.types.UILayout, obj: bpy.types.Object):
    if obj is None:
        return
    
    if obj.type != "ARMATURE":
        return
    
    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        if scene.bfu_object_properties_expanded.is_expend():
            if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):
                if not obj.bfu_export_as_alembic_animation:
                    AssetType2 = layout.column()
                    # Show asset type
                    AssetType2.prop(obj, "bfu_export_skeletal_mesh_as_static_mesh")

def draw_ui_object(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
    
    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    if obj is None:
        return
    if obj.type != "ARMATURE":
        return
    is_skeletal_mesh = bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)
    if is_skeletal_mesh is False:
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return

    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_modular_skeletal_mesh_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():
            # SkeletalMesh prop
            if not obj.bfu_export_as_lod_mesh:
                modular_skeletal_mesh = panel.column()
                modular_skeletal_mesh.prop(obj, "bfu_modular_skeletal_mesh_mode")
                if obj.bfu_modular_skeletal_mesh_mode == "every_meshs":
                    modular_skeletal_mesh.prop(obj, "bfu_modular_skeletal_mesh_every_meshs_separate")
                if obj.bfu_modular_skeletal_mesh_mode == "specified_parts":
                    bfu_modular_skeletal_mesh.bfu_modular_skeletal_mesh_utils.get_modular_skeletal_specified_parts_meshs_template(obj).draw(modular_skeletal_mesh)

def draw_ui_scene(layout: bpy.types.UILayout):
    pass