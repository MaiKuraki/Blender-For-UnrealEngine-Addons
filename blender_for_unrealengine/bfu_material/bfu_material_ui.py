# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bfu_addon_prefs
from .. import bfu_ui
from .. import bbpl
from .. import bfu_assets_manager
from .. import bfu_export_control



def draw_ui_object(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):

    if bpy.context is None:
        return
    
    scene = bpy.context.scene

    # Hide filters
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    if obj.bfu_export_as_lod_mesh:
        return

    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "MISC"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_object_material_properties_expanded")
        if accordion is None:
            return

        _, panel = accordion.draw(layout)
        if accordion.is_expend():
            asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
            if asset_class and asset_class.use_materials == True:

                bbpl.blender_layout.layout_doc_button.add_doc_page_operator(panel, text="About Materials", url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Material")

                # from blender
                from_blender_ui = panel.column()
                export_material_ui = from_blender_ui.column()
                export_material_ui.prop(obj, 'bfu_export_materials')

                export_export_texture_ui = export_material_ui.column()
                export_export_texture_ui.enabled = obj.bfu_export_materials
                export_export_texture_ui.prop(obj, 'bfu_export_textures')

                # To Unreal Engine
                to_unreal_ui = panel.column()
                bfu_material_search_location = to_unreal_ui.column()
                bfu_material_search_location.prop(obj, 'bfu_material_search_location')

                import_material_ui = bfu_material_search_location.column()
                import_material_ui.prop(obj, 'bfu_import_materials')

                import_texture_ui = import_material_ui.column()
                import_texture_ui.enabled = obj.bfu_import_materials
                import_texture_ui.prop(obj, 'bfu_import_textures')


                normal_texture_ui = import_texture_ui.column()
                normal_texture_ui.enabled = obj.bfu_import_textures and obj.bfu_import_materials
                normal_texture_ui.prop(obj, 'bfu_flip_normal_map_green_channel')

                material_utils_ui = bfu_material_search_location.column()
                material_utils_ui.prop(obj, 'bfu_reorder_material_to_fbx_order')
                            

def draw_ui_scene_collision(layout: bpy.types.UILayout):
    pass