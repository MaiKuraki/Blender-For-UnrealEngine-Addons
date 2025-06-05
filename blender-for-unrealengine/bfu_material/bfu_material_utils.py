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
from typing import Dict, Any, TYPE_CHECKING
from .. bfu_assets_manager.bfu_asset_manager_type import AssetType

def get_material_asset_data(obj: bpy.types.Object, asset_type: AssetType) -> Dict[str, Any]:
    asset_data: Dict[str, Any] = {}
    return asset_data

def get_material_asset_additional_data(obj: bpy.types.Object, asset_type: AssetType) -> Dict[str, Any]:
    asset_data: Dict[str, Any] = {}
    if obj:

        if TYPE_CHECKING:
            class FakeObject(bpy.types.Object):
                bfu_import_materials: bool = False
                bfu_import_textures: bool = False
                bfu_flip_normal_map_green_channel: bool = False
                bfu_reorder_material_to_fbx_order: bool = False
                bfu_material_search_location: str = ""
            obj = FakeObject()

        if asset_type in [AssetType.STATIC_MESH, AssetType.SKELETAL_MESH]:
            asset_data["import_materials"] = obj.bfu_import_materials
            asset_data["import_textures"] = obj.bfu_import_textures
            asset_data["flip_normal_map_green_channel"] = obj.bfu_flip_normal_map_green_channel
            asset_data["reorder_material_to_fbx_order"] = obj.bfu_reorder_material_to_fbx_order
            asset_data["material_search_location"] = obj.bfu_material_search_location
    return asset_data