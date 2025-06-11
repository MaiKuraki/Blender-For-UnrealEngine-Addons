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
                bfu_material_search_location = panel.column()
                bbpl.blender_layout.layout_doc_button.add_doc_page_operator(bfu_material_search_location, text="About Materials", url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Material")
                bfu_material_search_location.prop(obj, 'bfu_material_search_location')

                material_ui = bfu_material_search_location.column()
                material_ui.prop(obj, 'bfu_export_materials')

                texture_ui = material_ui.column()
                texture_ui.enabled = obj.bfu_export_materials
                texture_ui.prop(obj, 'bfu_export_textures')

                normal_texture_ui = texture_ui.column()
                normal_texture_ui.enabled = obj.bfu_export_textures and obj.bfu_export_materials
                normal_texture_ui.prop(obj, 'bfu_flip_normal_map_green_channel')

                material_utils_ui = bfu_material_search_location.column()
                material_utils_ui.prop(obj, 'bfu_reorder_material_to_fbx_order')
                            

def draw_ui_scene_collision(layout: bpy.types.UILayout):
    pass