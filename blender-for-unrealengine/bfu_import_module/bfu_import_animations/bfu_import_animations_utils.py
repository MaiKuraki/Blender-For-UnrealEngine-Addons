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

import unreal
from typing import Any, Dict
from .. import import_module_unreal_utils
from .. import import_module_tasks_class
from ..asset_types import ExportAssetType

def set_animation_sample_rate(itask: import_module_tasks_class.ImportTask, asset_additional_data: Dict[str, Any], asset_type: ExportAssetType, filetype: str) -> None:
    if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
        if asset_type.is_skeletal_animation():
            if asset_additional_data and "animation_frame_rate_denominator" in asset_additional_data and "animation_frame_rate_numerator" in asset_additional_data:
                if filetype == "GLTF":
                    # Interchange use sample rate to set the animation frame rate.
                    sequencer_frame_rate_denominator = asset_additional_data['animation_frame_rate_denominator']
                    sequencer_frame_rate_numerator = asset_additional_data['animation_frame_rate_numerator']
                    # For GLTF, the sample rate is the frame rate.
                    animation_sample_rate = sequencer_frame_rate_numerator / sequencer_frame_rate_denominator
                    print("Set GLTF animation sample rate to:", animation_sample_rate)
                    animation_pipeline = itask.get_igap_animation()
                    animation_pipeline.set_editor_property('custom_bone_animation_sample_rate', animation_sample_rate)
                    animation_pipeline.set_editor_property('snap_to_closest_frame_boundary', True)
                    return
                
            # For other file types, use automatic sample rate.
            animation_pipeline = itask.get_igap_animation()
            animation_pipeline.set_editor_property('custom_bone_animation_sample_rate', 0)
        
            
def apply_post_import_assets_changes(itask: import_module_tasks_class.ImportTask, asset_data: Dict[str, Any]) -> None:
    """Applies post-import changes based on whether Interchange or FBX is used."""
    if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
        apply_interchange_post_import(itask, asset_data)
    else:
        apply_fbxui_post_import(itask, asset_data)

def apply_interchange_post_import(itask: import_module_tasks_class.ImportTask, asset_data: Dict[str, Any]) -> None:


    # When Import FBX animation using the Interchange it create Anim_0_Root and Root_MorphAnim_0. 
    # I'm not sure if that a bug... So remove I Root_MorphAnim_0 or other animations and I rename Anim_0_Root.
    asset_paths_to_remove = []
    main_anim_path = None
    for imported_asset in itask.get_imported_assets():
        if type(imported_asset) is unreal.AnimSequence:
            anim_asset_path = imported_asset.get_path_name()
            path, name = anim_asset_path.rsplit('/', 1)
            if name == "Root_MorphAnim_0.Root_MorphAnim_0":
                asset_paths_to_remove.append(imported_asset.get_path_name())
            else:
                main_anim_path = imported_asset.get_path_name()

    # Remove wrong animation assets
    for asset_path in asset_paths_to_remove:
        unreal.EditorAssetLibrary.delete_asset(asset_path)
    
    # Rename correct animation asset
    if main_anim_path:

        anim_asset_path = imported_asset.get_path_name()
        path, name = anim_asset_path.rsplit('/', 1)
        new_anim_path = path + "/" + asset_data["asset_import_name"] + "." + asset_data["asset_import_name"]
        if main_anim_path != new_anim_path:
            unreal.EditorAssetLibrary.rename_asset(main_anim_path, new_anim_path)
    else:
        fail_reason = f"animAsset {asset_data['asset_name']} not found after import: {main_anim_path}"
        return fail_reason, None

def apply_fbxui_post_import(itask: import_module_tasks_class.ImportTask, asset_data):
    """Applies post-import changes for FBX pipeline."""
    # When Import FBX animation using FbxImportUI it create a skeletal mesh and the animation at this side. 
    # I'm not sure if that a bug too... So remove the extra mesh
    imported_anim_sequence = itask.get_imported_anim_sequence()
    if imported_anim_sequence is None:
        # If Imported Anim Sequence is None it maybe imported the asset as Skeletal Mesh.
        skeleta_mesh_assset = itask.get_imported_skeletal_mesh()
        if skeleta_mesh_assset:
            # If Imported as Skeletal Mesh Search the real Anim Sequence
            path = skeleta_mesh_assset.get_path_name()
            base_name = path.split('.')[0]
            anim_asset_name = f"{base_name}_anim.{base_name.split('/')[-1]}_anim"
            desired_anim_path = f"{base_name}.{base_name.split('/')[-1]}"
            animAsset = import_module_unreal_utils.load_asset(anim_asset_name)
            if animAsset is not None:
                # Remove the imported skeletal mesh and rename te anim sequence with his correct name.
                unreal.EditorAssetLibrary.delete_asset(path)
                unreal.EditorAssetLibrary.rename_asset(anim_asset_name, desired_anim_path)
            else:
                fail_reason = f"animAsset {asset_data['asset_name']} not found after import: {anim_asset_name}"
                return fail_reason, None