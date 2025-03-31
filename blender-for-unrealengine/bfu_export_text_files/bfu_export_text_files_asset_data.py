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

def write_main_assets_data():
    # Generate a script for import assets in Ue4
    scene = bpy.context.scene

    data = {}

    bfu_export_text_files_utils.add_generated_json_header(data, languages.ti('write_text_additional_track_all'))
    bfu_export_text_files_utils.add_generated_json_meta_data(data)

    data['bfu_unreal_import_location'] = '/' + scene.bfu_unreal_import_module + '/' + scene.bfu_unreal_import_location

    # Import assets
    data['assets'] = []
    for unreal_exported_asset in bfu_export_logs.bfu_asset_export_logs_utils.get_exported_assets_logs():
        data['assets'].append(write_single_asset_data(unreal_exported_asset))

    bfu_export_text_files_utils.add_generated_json_footer(data)
    return data

def write_single_asset_data(unreal_exported_asset: bfu_export_logs.bfu_asset_export_logs.BFU_OT_UnrealExportedAssetLog):
    scene = bpy.context.scene
    asset_data = {}
    asset_data["scene_unit_scale"] = bfu_utils.get_scene_unit_scale()

    asset_data["asset_name"] = unreal_exported_asset.asset_name
    asset_data["asset_global_scale"] = unreal_exported_asset.asset_global_scale
    if bfu_utils.GetIsAnimation(unreal_exported_asset.asset_type):
        asset_data["asset_type"] = "Animation"
    elif unreal_exported_asset.asset_type == "Collection StaticMesh":
        asset_data["asset_type"] = "StaticMesh"
    else:
        asset_data["asset_type"] = unreal_exported_asset.asset_type
    if unreal_exported_asset.asset_type in ["StaticMesh", "SkeletalMesh"]:
        if unreal_exported_asset.object.bfu_export_as_lod_mesh:
            asset_data["import_as_lod_mesh"] = True
        else:
            asset_data["import_as_lod_mesh"] = False

    if bfu_utils.GetIsAnimation(unreal_exported_asset.asset_type):
        relative_import_path = os.path.join(unreal_exported_asset.folder_name, scene.bfu_anim_subfolder_name)
    else:
        relative_import_path = unreal_exported_asset.folder_name

    full_import_path = "/" + scene.bfu_unreal_import_module + "/" + os.path.join(scene.bfu_unreal_import_location, relative_import_path)
    full_import_path = full_import_path.replace('\\', '/').rstrip('/')
    asset_data["full_import_path"] = full_import_path

    if unreal_exported_asset.GetFileByType("FBX"):
        asset_data["fbx_path"] = unreal_exported_asset.GetFileByType("FBX").GetAbsolutePath()
    else:
        asset_data["fbx_path"] = None

    if unreal_exported_asset.GetFileByType("ABC"):
        asset_data["abc_path"] = unreal_exported_asset.GetFileByType("ABC").GetAbsolutePath()
    else:
        asset_data["abc_path"] = None

    if unreal_exported_asset.GetFileByType("AdditionalTrack"):
        asset_data["additional_tracks_path"] = unreal_exported_asset.GetFileByType("AdditionalTrack").GetAbsolutePath()
    else:
        asset_data["additional_tracks_path"] = None

    if bfu_utils.GetIsAnimation(unreal_exported_asset.asset_type) or unreal_exported_asset.asset_type == "SkeletalMesh":
        
        # Skeleton
        asset_data["target_skeleton_search_ref"] = bfu_assets_references.bfu_asset_ref_utils.get_skeleton_search_ref(unreal_exported_asset.object)
        # Skeletal Mesh
        asset_data["target_skeletal_mesh_search_ref"] = bfu_assets_references.bfu_asset_ref_utils.get_skeletal_mesh_search_ref(unreal_exported_asset.object)

        # Better to seperate to let control to uses but my default it use the Skeleton Search Ref.
        asset_data["target_skeleton_import_ref"] = bfu_assets_references.bfu_asset_ref_utils.get_skeleton_search_ref(unreal_exported_asset.object)

        

    if bfu_utils.GetIsAnimation(unreal_exported_asset.asset_type):
        asset_data["animation_start_frame"] = unreal_exported_asset.animation_start_frame
        asset_data["animation_end_frame"] = unreal_exported_asset.animation_end_frame    

    if unreal_exported_asset.object:
        if unreal_exported_asset.asset_type in ["StaticMesh"]:
            asset_data["auto_generate_collision"] = unreal_exported_asset.object.bfu_auto_generate_collision
            asset_data["collision_trace_flag"] = unreal_exported_asset.object.bfu_collision_trace_flag

        if unreal_exported_asset.asset_type in ["SkeletalMesh"]:
            asset_data["create_physics_asset"] = unreal_exported_asset.object.bfu_create_physics_asset
            asset_data["enable_skeletal_mesh_per_poly_collision"] = unreal_exported_asset.object.bfu_enable_skeletal_mesh_per_poly_collision

        if bfu_utils.GetIsAnimation(unreal_exported_asset.asset_type):
            asset_data["do_not_import_curve_with_zero"] = unreal_exported_asset.object.bfu_do_not_import_curve_with_zero

    asset_data.update(bfu_lod.bfu_lod_utils.get_lod_asset_data(unreal_exported_asset))
    asset_data.update(bfu_vertex_color.bfu_vertex_color_utils.get_vertex_color_asset_data(unreal_exported_asset))
    asset_data.update(bfu_material.bfu_material_utils.get_material_asset_data(unreal_exported_asset))
    asset_data.update(bfu_light_map.bfu_light_map_utils.get_light_map_asset_data(unreal_exported_asset))
    asset_data.update(bfu_nanite.bfu_nanite_utils.get_nanite_asset_data(unreal_exported_asset))

    return asset_data