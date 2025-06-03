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

import os
import bpy
import fnmatch
from .. import bbpl
from .. import bfu_export_logs
from .. import bfu_static_mesh
from .. import bfu_assets_manager
from .. bfu_assets_manager.bfu_asset_manager_type import AssetType


def get_lod_asset_data(obj: bpy.types.Object, asset_type: AssetType) -> dict:
    asset_data = {}

    if asset_type in [AssetType.STATIC_MESH, AssetType.SKELETAL_MESH]:
        if obj.bfu_export_as_lod_mesh:
            asset_data["import_as_lod_mesh"] = True
        else:
            asset_data["import_as_lod_mesh"] = False

    return asset_data

def get_lod_additional_data(obj: bpy.types.Object, asset_type: AssetType) -> dict:
    asset_data = {}

    # Add lod group name
    if obj:
        if asset_type in [AssetType.STATIC_MESH]:
            if (obj.bfu_use_static_mesh_lod_group):
                asset_data["static_mesh_lod_group"] = obj.bfu_static_mesh_lod_group
            else:
                asset_data["static_mesh_lod_group"] = None

    # Add lod slots
    if obj:
        asset_data['level_of_details'] = {}

        def GetLodPath(lod_obj):
            asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(lod_obj)
            if asset_class:
                directory_path = asset_class.get_asset_export_directory_path(lod_obj, "", True)
                file_name = asset_class.get_asset_file_name(lod_obj)
            return os.path.join(directory_path, file_name)

        if obj.bfu_lod_target1 is not None:
            asset_data['level_of_details']['lod_1'] = GetLodPath(obj.bfu_lod_target1)
        if obj.bfu_lod_target2 is not None:
            asset_data['level_of_details']['lod_2'] = GetLodPath(obj.bfu_lod_target2)
        if obj.bfu_lod_target3 is not None:
            asset_data['level_of_details']['lod_3'] = GetLodPath(obj.bfu_lod_target3)
        if obj.bfu_lod_target4 is not None:
            asset_data['level_of_details']['lod_4'] = GetLodPath(obj.bfu_lod_target4)
        if obj.bfu_lod_target5 is not None:
            asset_data['level_of_details']['lod_5'] = GetLodPath(obj.bfu_lod_target5)

    return asset_data