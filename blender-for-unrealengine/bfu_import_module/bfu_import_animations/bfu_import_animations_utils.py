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
from typing import Any, Dict, List
from .. import import_module_unreal_utils
from .. import import_module_tasks_class
from ..asset_types import ExportAssetType, AssetFileTypeEnum

def set_animation_sample_rate(itask: import_module_tasks_class.ImportTask, asset_additional_data: Dict[str, Any], asset_type: ExportAssetType, filetype: AssetFileTypeEnum) -> None:
    if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
        if asset_type.is_skeletal_animation():
            if asset_additional_data and "animation_frame_rate_denominator" in asset_additional_data and "animation_frame_rate_numerator" in asset_additional_data:
                if filetype.value == AssetFileTypeEnum.GLTF.value:
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
        
            
def apply_post_import_assets_changes(itask: import_module_tasks_class.ImportTask, asset_data: Dict[str, Any], filetype: AssetFileTypeEnum) -> None:
    """Applies post-import changes based on whether Interchange or FBX is used."""
    if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
        apply_interchange_post_import(itask, asset_data, filetype)
    else:
        apply_fbxui_post_import(itask, asset_data)

def cleanup_imported_assets(anim_sequences: List[unreal.AnimSequence], desired_asset_name: str, main_asset_name: str) -> None:
    '''
    anim_sequences: List of imported animation sequences to clean up.
    desired_asset_name: The desired name of the animation.
    main_asset_name: The name of the animation to use and rename.
    '''

    if len(anim_sequences) == 0:
        print(f"anim_sequences is empty.")

    elif len(anim_sequences) == 1:
        if anim_sequences[0].get_name() != desired_asset_name:
            import_module_unreal_utils.renamed_asset_name(anim_sequences[0], desired_asset_name)

    elif len(anim_sequences) > 1:
        # If more than one animation sequence is imported, rename the main one and delete the rest.
        desired_asset_found: bool = False
        main_asset_found: bool = False
        for anim_seq in anim_sequences:
            if anim_seq.get_name() == desired_asset_name:
                desired_asset_found = True
            elif anim_seq.get_name() == main_asset_name:
                main_asset_found = True


        if desired_asset_found:
            # Remove all imported assets except the desired one.
            for anim_seq in anim_sequences:
                if anim_seq.get_name() != desired_asset_name:
                    unreal.EditorAssetLibrary.delete_asset(anim_seq.get_path_name())

        elif main_asset_found:
            # If the desired asset is not found, rename the main asset to the desired name.
            for anim_seq in anim_sequences:
                if anim_seq.get_name() == main_asset_name:
                    import_module_unreal_utils.renamed_asset_name(anim_seq, desired_asset_name)
                else:
                    unreal.EditorAssetLibrary.delete_asset(anim_seq.get_path_name())
        else:
            # If neither the desired asset nor the main asset is found.
            # Rename the first imported animation sequence as the desired asset.
            for x, anim_seq in enumerate(anim_sequences):
                if x == 0:
                    import_module_unreal_utils.renamed_asset_name(anim_seq, desired_asset_name)
                else:
                    unreal.EditorAssetLibrary.delete_asset(anim_seq.get_path_name())

def apply_interchange_post_import(itask: import_module_tasks_class.ImportTask, asset_data: Dict[str, Any], filetype: AssetFileTypeEnum) -> None:

    if filetype.value == AssetFileTypeEnum.FBX.value:
        # When Import FBX animation using the Interchange it create "Anim_0_Root" and "Root_MorphAnim_0". 
        # I'm not sure if that a bug... So remove I "Root_MorphAnim_0" or other animations and I rename "Anim_0_Root".
        imported_assets = itask.get_imported_anim_sequences()
        cleanup_imported_assets(imported_assets, asset_data["asset_import_name"], "Anim_0_Root")
    
    elif filetype.value == AssetFileTypeEnum.GLTF.value:
        # For glTF I got exactly the same issue but with "Body" and "Scene". 
        # So remove I "Body" or other animations and I rename "Scene".
        # Scene it the name the the scene in Blender at the export.
        imported_assets = itask.get_imported_anim_sequences()
        cleanup_imported_assets(imported_assets, asset_data["asset_import_name"], "Scene")


def apply_fbxui_post_import(itask: import_module_tasks_class.ImportTask, asset_data: Dict[str, Any]) -> None:
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