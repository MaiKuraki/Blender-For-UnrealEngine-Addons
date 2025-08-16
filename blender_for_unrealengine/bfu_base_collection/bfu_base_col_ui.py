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


from . import bfu_export_procedure
from .. import bfu_ui
from .. import bfu_cached_assets
from .. import bfu_asset_preview
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToSearch
from .. import bbpl


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context):

    scene = bpy.context.scene 

    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("SCENE", "GENERAL"):

        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_collection_properties_expanded")
        if accordion:
            _, panel = accordion.draw(layout)
            if panel:
                collectionListProperty = panel.column()
                collectionListProperty.template_list(
                    # type and unique id
                    "BFU_UL_CollectionExportTarget", "",
                    # pointer to the CollectionProperty
                    scene, "bfu_collection_asset_list",
                    # pointer to the active identifier
                    scene, "bfu_active_collection_asset_list",
                    maxrows=5,
                    rows=5
                )
                collectionListProperty.operator(
                    "object.updatecollectionlist",
                    icon='RECOVER_LAST')

                if scene.bfu_active_collection_asset_list < len(scene.bfu_collection_asset_list):
                    col_name = scene.bfu_collection_asset_list[scene.bfu_active_collection_asset_list].name
                    if col_name in bpy.data.collections:
                        col = bpy.data.collections[col_name]
                        col_prop = panel
                        col_prop.prop(col, 'bfu_export_folder_name', icon='FILE_FOLDER')
                        bfu_export_procedure.draw_col_export_procedure(panel, col)

                panel.label(text='Note: The collection are exported like StaticMesh.')

        bfu_asset_preview.bfu_asset_preview_ui.draw_asset_preview_bar(layout, context, asset_to_search=AssetToSearch.COLLECTION_ONLY)