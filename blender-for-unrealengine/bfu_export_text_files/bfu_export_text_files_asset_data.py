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
from typing import List, Dict, Any, Union, Optional
from . import bfu_export_text_files_utils
from .. import bfu_export_logs
from .. import languages
from .. import bfu_utils
from .. import bfu_material
from .. import bfu_nanite
from .. import bfu_light_map
from .. import bfu_assets_references
from .. import bfu_vertex_color
from .. import bfu_lod
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType
from .. import bfu_export_nomenclature

def write_main_assets_data(exported_asset_log: List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]) -> Dict[str, Any]:
    # Generate a script for import assets in Unreal Engine.

    data: Dict[str, Any] = {}

    bfu_export_text_files_utils.add_generated_json_header(data, languages.ti('write_text_additional_track_all'))
    bfu_export_text_files_utils.add_generated_json_meta_data(data)

    data['unreal_import_location'] = str(bfu_export_nomenclature.bfu_export_nomenclature_utils.get_import_location())

    # Import assets
    assets: List[Dict[str, Any]] = []
    for unreal_exported_asset in exported_asset_log:
        assets.append(write_single_asset_data(unreal_exported_asset))
    data['assets'] = assets

    bfu_export_text_files_utils.add_generated_json_footer(data)
    return data

def write_single_asset_data(unreal_exported_asset: bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog) -> Dict[str, Union[str, bool, float, List[Any]]]:
    asset_data: Dict[str, Any] = {}
    asset_data["scene_unit_scale"] = bfu_utils.get_scene_unit_scale()

    asset_data["asset_name"] = unreal_exported_asset.exported_asset.name
    asset_data["asset_type"] = unreal_exported_asset.exported_asset.asset_type.get_type_as_string()
    asset_data["asset_import_name"] = unreal_exported_asset.exported_asset.import_name
    asset_data["asset_import_path"] = str(unreal_exported_asset.exported_asset.import_dirpath) 

    asset_type = unreal_exported_asset.exported_asset.asset_type
    files: List[Dict[str, Any]] = []
    for pakages in unreal_exported_asset.exported_asset.asset_pakages:
        file = pakages.file
        if file:
            file_data: Dict[str, Any] = {}
            file_data["type"] = file.file_type.value
            file_data["content_type"] = file.file_content_type
            file_data["file_path"] = str(file.get_full_path())
            files.append(file_data)
    if unreal_exported_asset.exported_asset.additional_data:
        additional_data = unreal_exported_asset.exported_asset.additional_data
        file = additional_data.file
        if file:
            file_data: Dict[str, Any] = {}
            file_data["type"] = file.file_type.value
            file_data["content_type"] = file.file_content_type
            file_data["file_path"] = str(file.get_full_path())
            files.append(file_data)
    asset_data["files"] = files

    if asset_type in [AssetType.SKELETAL_MESH, AssetType.ANIM_ACTION, AssetType.ANIM_POSE, AssetType.ANIM_NLA]:
        main_armature = unreal_exported_asset.exported_asset.asset_pakages[0].objects[0]
        # Skeleton
        asset_data["target_skeleton_search_ref"] = bfu_assets_references.bfu_asset_ref_utils.get_skeleton_search_ref(main_armature)
        # Skeletal Mesh
        asset_data["target_skeletal_mesh_search_ref"] = bfu_assets_references.bfu_asset_ref_utils.get_skeletal_mesh_search_ref(main_armature)

        # Better to seperate to let control to uses but my default it use the Skeleton Search Ref.
        asset_data["target_skeleton_import_ref"] = bfu_assets_references.bfu_asset_ref_utils.get_skeleton_search_ref(main_armature)

        

    if asset_type in [AssetType.ANIM_ACTION, AssetType.ANIM_POSE, AssetType.ANIM_NLA]:
        frame_range = unreal_exported_asset.exported_asset.asset_pakages[0].frame_range
        if frame_range:
            asset_data["animation_start_frame"] = frame_range[0]
            asset_data["animation_end_frame"] = frame_range[1]

    main_obj_data: Optional[bpy.types.Object] = None
    
    if asset_type in [AssetType.COLLECTION_AS_STATIC_MESH]:
        pass
        #main_collection = unreal_exported_asset.exported_asset.asset_pakages[0].collection
        #main_obj_data = main_collection
    else:
        main_object = unreal_exported_asset.exported_asset.asset_pakages[0].objects[0]
        if main_object:
            if asset_type in [AssetType.STATIC_MESH]:
                asset_data["auto_generate_collision"] = main_object.bfu_auto_generate_collision
                asset_data["collision_trace_flag"] = main_object.bfu_collision_trace_flag

            if asset_type in [AssetType.SKELETAL_MESH]:
                asset_data["create_physics_asset"] = main_object.bfu_create_physics_asset
                asset_data["enable_skeletal_mesh_per_poly_collision"] = main_object.bfu_enable_skeletal_mesh_per_poly_collision

            if asset_type in [AssetType.ANIM_ACTION, AssetType.ANIM_POSE, AssetType.ANIM_NLA]:
                asset_data["do_not_import_curve_with_zero"] = main_object.bfu_do_not_import_curve_with_zero
        main_obj_data = main_object

    if main_obj_data is not None:
        asset_data.update(bfu_lod.bfu_lod_utils.get_lod_asset_data(main_obj_data, asset_type))
        asset_data.update(bfu_vertex_color.bfu_vertex_color_utils.get_vertex_color_asset_data(main_obj_data, asset_type))
        asset_data.update(bfu_material.bfu_material_utils.get_material_asset_data(main_obj_data, asset_type))
        asset_data.update(bfu_light_map.bfu_light_map_utils.get_light_map_asset_data(main_obj_data, asset_type))
        asset_data.update(bfu_nanite.bfu_nanite_utils.get_nanite_asset_data(main_obj_data, asset_type))

    return asset_data