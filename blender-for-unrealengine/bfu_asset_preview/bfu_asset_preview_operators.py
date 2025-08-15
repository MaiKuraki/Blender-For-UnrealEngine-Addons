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
from typing import TYPE_CHECKING, Set
from .. import bfu_cached_assets
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToSearch, AssetDataSearchMode
from . import bfu_asset_preview_ui

class BFU_OT_ShowAssetToExport(bpy.types.Operator):
    bl_label = "Show asset(s)"
    bl_idname = "object.showasset"
    bl_description = "Click to show assets that are to be exported."
    asset_to_search_str: bpy.props.StringProperty(
        name="Asset Type",
        description="Type of assets to show",
        default="all_assets"
    )
    if TYPE_CHECKING:
        asset_to_search_str: str


    def execute(self, context: bpy.types.Context):

        bpy.ops.object.openshowassettoexport("INVOKE_DEFAULT", asset_to_search_str=self.asset_to_search_str)
        return {'FINISHED'}


class BFU_OT_OpenShowAssetToExport(bpy.types.Operator):
    bl_label = "Open assets to export"
    bl_idname = "object.openshowassettoexport"
    bl_description = "Open the list of assets to export."
    asset_to_search_str: bpy.props.StringProperty(
        name="Asset Type",
        description="Type of assets to show",
        default="all_assets"
    )
    if TYPE_CHECKING:
        asset_to_search_str: str

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> Set[str]:
        if context is None:
            return {'CANCELLED'}
        
        wm = context.window_manager
        return wm.invoke_popup(self, width=1200)  # type: ignore

    def execute(self, context: bpy.types.Context):
        if context is None:
            return {'CANCELLED'}
        return {'FINISHED'}

    def draw(self, context: bpy.types.Context):
        if context is None:
            return
        layout = self.layout
        if layout:
            final_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.get_final_asset_cache()
            asset_to_search = AssetToSearch(self.asset_to_search_str)
            final_asset_list_to_export = final_asset_cache.get_final_asset_list(asset_to_search, AssetDataSearchMode.FULL)
            bfu_asset_preview_ui.draw_assets_list(layout, context, asset_to_search, final_asset_list_to_export)


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_ShowAssetToExport,
    BFU_OT_OpenShowAssetToExport,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

