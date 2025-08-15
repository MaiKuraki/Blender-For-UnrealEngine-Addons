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

from typing import List
import bpy
from .. import bfu_export_filter
from . import bfu_base_col_props

def support_collection_export(scene: bpy.types.Scene) -> bool:
    return bfu_export_filter.bfu_export_filter_props.scene_use_static_collection_export(scene)

def get_collection_asset_list(scene: bpy.types.Scene) -> List[bpy.types.Collection]:
    collection_export_asset_list: List[bpy.types.Collection] = []

    for target_col in bfu_base_col_props.scene_collection_asset_list(scene):
        if target_col.use:
            if target_col.name in bpy.data.collections:
                collection = bpy.data.collections[target_col.name]
                collection_export_asset_list.append(collection)
    return collection_export_asset_list

def optimized_collection_search(scene: bpy.types.Scene) -> List[bpy.types.Collection]:
    if not support_collection_export(scene):
        return []

    collection_list: List[bpy.types.Collection] = []

    collection_export_asset_list = get_collection_asset_list(scene)
    for col_asset in collection_export_asset_list:
        if col_asset.name in bpy.data.collections:
            collection = bpy.data.collections[col_asset.name]
            collection_list.append(collection)

    return collection_list