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
from . import bfu_modular_skeletal_mesh_type
from .. import bfu_assets_manager
from ..bfu_cached_assets import bfu_cached_assets_types

def get_assets_to_export_for_modular_skeletal_mesh(obj):
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_asset_class(obj)
    asset_list = []
    template = obj.bfu_modular_skeletal_specified_parts_meshs_template
    template: bfu_modular_skeletal_mesh_type.BFU_UI_ModularSkeletalSpecifiedPartsTargetList
    for part in template.get_template_collection():
        part: bfu_modular_skeletal_mesh_type.BFU_UI_ModularSkeletalSpecifiedPartsMeshItem
        
        if part.enabled:
            asset = bfu_cached_assets_types.AssetToExport(obj, None, "SkeletalMesh")
            asset.name = part.name
            for skeletal_part in part.skeletal_parts.get_template_collection():
                skeletal_part: bfu_modular_skeletal_mesh_type.BFU_UI_ModularSkeletalSpecifiedPartsTargetItem
                if skeletal_part.enabled:
                    if skeletal_part.target_type == 'OBJECT':  # Utilisez l'attribut target_type
                        if skeletal_part.obj:
                            if skeletal_part.obj.bfu_export_type != "dont_export":
                                asset.add_obj(skeletal_part.obj)
                    elif skeletal_part.target_type == 'COLLECTION':
                        if skeletal_part.collection:
                            for collection_obj in skeletal_part.collection.objects:
                                if collection_obj.bfu_export_type != "dont_export":
                                    asset.add_obj(collection_obj)
            
            dirpath = asset_class.get_obj_export_directory_path(obj, part.sub_folder, True)
            asset.set_dirpath(dirpath)

            asset_list.append(asset)
    return asset_list