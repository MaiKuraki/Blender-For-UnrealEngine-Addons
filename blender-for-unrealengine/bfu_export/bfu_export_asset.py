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
from typing import List
from . import bfu_export_single_generic
from . import bfu_export_single_alembic_animation
from . import bfu_export_single_fbx_action
from . import bfu_export_single_camera
from . import bfu_export_single_spline
from . import bfu_export_single_fbx_nla_anim
from . import bfu_export_single_skeletal_mesh
from . import bfu_export_single_static_mesh
from . import bfu_export_single_static_mesh_collection
from . import bfu_export_single_groom_simulation
from .. import bfu_cached_assets
from .. import bbpl
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType, AssetToExport
from .. import bfu_basics
from .. import bfu_camera
from .. import bfu_spline
from .. import bfu_export_logs




def IsValidActionForExport(scene, obj, animType):
    if animType == "Action":
        if scene.bfu_use_anim_export:
            return True
        else:
            return False
    elif animType == "Pose":
        if scene.bfu_use_anim_export:
            return True
        else:
            return False
    elif animType == "NLA":
        if scene.bfu_use_anim_export:
            return True
        else:
            False
    else:
        print("Error in IsValidActionForExport() animType not found: ", animType)
    return False


def IsValidDataForExport(scene, obj):
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
    return asset_class.can_export_asset(obj)

def PrepareSceneForExport():
    scene = bpy.context.scene

    for obj in scene.objects:
        if obj.hide_select:
            obj.hide_select = False
        if obj.hide_viewport:
            obj.hide_viewport = False
        if obj.hide_get():
            obj.hide_set(False)

    for col in bpy.data.collections:
        if col.hide_select:
            col.hide_select = False
        if col.hide_viewport:
            col.hide_viewport = False

    for vlayer in bpy.context.scene.view_layers:
        layer_collections = bbpl.utils.get_layer_collections_recursive(vlayer.layer_collection)
        for layer_collection in layer_collections:
            if layer_collection.exclude:
                layer_collection.exclude = False
            if layer_collection.hide_viewport:
                layer_collection.hide_viewport = False

def process_export(op: bpy.types.Operator, final_asset_list_to_export: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    prepare_all_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("Prepare all export")

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()

    # Save scene data before export
    local_view_areas = bbpl.scene_utils.move_to_global_view()
    user_scene_save = bbpl.save_data.scene_save.UserSceneSave()
    user_scene_save.save_current_scene()
    
    PrepareSceneForExport()
    bbpl.utils.safe_mode_set('OBJECT', user_scene_save.user_select_class.user_active)

    if addon_prefs.revertExportPath:
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_static_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_skeletal_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_alembic_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_groom_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_camera_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_spline_file_path))
        bfu_basics.RemoveFolderTree(bpy.path.abspath(scene.bfu_export_other_file_path))


    prepare_all_export_time_log.end_time_log()
    exported_asset_log = export_all_from_asset_list(op, final_asset_list_to_export)

    post_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("Clean after all export")

    # Reset scene data after export
    user_scene_save.reset_select(use_names = True)
    user_scene_save.reset_scene_at_save(print_removed_items = True)

    # Clean actions
    for action in bpy.data.actions:
        if action.name not in user_scene_save.action_names:
            bpy.data.actions.remove(action)

    bbpl.scene_utils.move_to_local_view()
    post_export_time_log.end_time_log()
    return exported_asset_log


def export_all_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene

    export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("TOTAL EXPORT")
    exported_asset_log = []

    for asset in asset_list:
        export_asset_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as {asset.asset_type.get_friendly_name()}.", 1)
        # Save current start/end frame
        UserStartFrame = scene.frame_start
        UserEndFrame = scene.frame_end
        exported_asset_log.append(bfu_export_single_generic.process_generic_export_from_asset(op, asset))

        # Resets previous start/end frame
        scene.frame_start = UserStartFrame
        scene.frame_end = UserEndFrame
        export_asset_time_log.end_time_log()

    export_time_log.end_time_log()
    return exported_asset_log

# @TODO all following export function are deprecated, remove them in future releases


def export_collection_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene

    print("Start Export collection(s)")
    exported_asset_log = []
    for asset in asset_list:
        if asset.asset_type == AssetType.COLLECTION_AS_STATIC_MESH:
            export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as Collection Static Mesh.", 1)
            # Save current start/end frame
            UserStartFrame = scene.frame_start
            UserEndFrame = scene.frame_end

            exported_asset_log.extend(bfu_export_single_static_mesh_collection.process_static_mesh_collection_export_from_asset(op, asset))

            # Resets previous start/end frame
            scene.frame_start = UserStartFrame
            scene.frame_end = UserEndFrame
            export_time_log.end_time_log()
    return exported_asset_log
    
def export_camera_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    print("Start Export camera(s)")
    exported_asset_log = []

    camera_list = []

    use_camera_evaluate = (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts)
    if use_camera_evaluate:
        multi_camera_tracks = bfu_camera.bfu_camera_data.BFU_MultiCameraTracks()
        multi_camera_tracks.set_start_end_frames(scene.frame_start, scene.frame_end+1)
    
    # Preparre asset to export
    for asset in asset_list:
        if asset.asset_type == AssetType.CAMERA:
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":
                if bfu_camera.bfu_camera_utils.is_camera(obj) and IsValidDataForExport(scene, obj):                    
                    camera_list.append(obj)
                    multi_camera_tracks.add_camera_to_evaluate(obj)

    if use_camera_evaluate:
        multi_camera_tracks.evaluate_all_cameras()

    #Start export
    for obj in camera_list:
        # Save current start/end frame
        UserStartFrame = scene.frame_start
        UserEndFrame = scene.frame_end

        if use_camera_evaluate:
            camera_tracks = multi_camera_tracks.get_evaluate_camera_data(obj)
        else:
            camera_tracks = None
        bfu_export_single_camera.process_camera_export(op, obj, camera_tracks)

        # Resets previous start/end frame
        scene.frame_start = UserStartFrame
        scene.frame_end = UserEndFrame
    
    return exported_asset_log

def export_spline_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    print("Start Export spline(s)")
    exported_asset_log = []

    spline_list = []

    use_spline_evaluate = (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts)
    if use_spline_evaluate:
        multi_spline_tracks = bfu_spline.bfu_spline_data.BFU_MultiSplineTracks()
    
    # Preparre asset to export
    for asset in asset_list:
        if asset.asset_type == AssetType.SPLINE:
            obj = asset.obj
            if obj.bfu_export_type == "export_recursive":
                if bfu_spline.bfu_spline_utils.is_spline(obj) and IsValidDataForExport(scene, obj):                    
                    spline_list.append(obj)
                    multi_spline_tracks.add_spline_to_evaluate(obj)

    if use_spline_evaluate:
        multi_spline_tracks.evaluate_all_splines()

    #Start export
    for obj in spline_list:

        if use_spline_evaluate:
            spline_tracks = multi_spline_tracks.get_evaluate_spline_data(obj)
        else:
            spline_tracks = None
        bfu_export_single_spline.process_spline_export(op, obj, spline_tracks)
    return exported_asset_log

def export_skeletal_mesh_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene

    print("Start Export SkeletalMesh(s)")
    exported_asset_log = []
    for asset in asset_list:
        if asset.asset_type == AssetType.SKELETAL_MESH:
            export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as Static Mesh.", 1)
            # Save current start/end frame
            UserStartFrame = scene.frame_start
            UserEndFrame = scene.frame_end
            exported_asset_log.extend(bfu_export_single_skeletal_mesh.process_skeletal_mesh_export_from_asset(op, asset))

            # Resets previous start/end frame
            scene.frame_start = UserStartFrame
            scene.frame_end = UserEndFrame
            export_time_log.end_time_log()
    return exported_asset_log

def export_alembic_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene

    print("Start Export Alembic Animation(s)")
    exported_asset_log = []
    for asset in asset_list:
        if asset.asset_type == AssetType.ANIM_ALEMBIC:    
            export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as Alembic Animation.", 1)
            # Save current start/end frame
            UserStartFrame = scene.frame_start
            UserEndFrame = scene.frame_end
            exported_asset_log.extend(bfu_export_single_alembic_animation.process_alembic_animation_export_from_asset(op, asset))

            # Resets previous start/end frame
            scene.frame_start = UserStartFrame
            scene.frame_end = UserEndFrame
            export_time_log.end_time_log()
    return exported_asset_log

def export_groom_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene

    print("Start Export Groom Simulation(s)")
    exported_asset_log = []
    for asset in asset_list:
        if asset.asset_type == AssetType.GROOM_SIMULATION:
            export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as Groom Simulation.", 1)        
            # Save current start/end frame
            UserStartFrame = scene.frame_start
            UserEndFrame = scene.frame_end
            exported_asset_log.extend(bfu_export_single_groom_simulation.process_groom_simulation_export_from_asset(op, asset))

            # Resets previous start/end frame
            scene.frame_start = UserStartFrame
            scene.frame_end = UserEndFrame
            export_time_log.end_time_log()
    return exported_asset_log

def export_animation_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene

    print("Start Export Action(s)")
    exported_asset_log = []
    for asset in asset_list:
        if asset.asset_type in (AssetType.ANIM_ACTION, AssetType.ANIM_POSE):
            export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as Action and Pose Animation.", 1)
            # Save current start/end frame
            UserStartFrame = scene.frame_start
            UserEndFrame = scene.frame_end

            exported_asset_log.extend(bfu_export_single_fbx_action.process_fbx_action_export_from_asset(op, asset))

            # Resets previous start/end frame
            scene.frame_start = UserStartFrame
            scene.frame_end = UserEndFrame
            export_time_log.end_time_log()
    return exported_asset_log

def export_nonlinear_animation_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]:
    scene = bpy.context.scene

    print("Start Export NLA(s)")
    exported_asset_log = []
    for asset in asset_list:
        if asset.asset_type == AssetType.ANIM_NLA:
            export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as Non Linear Animation.", 1)
            # Save current start/end frame
            UserStartFrame = scene.frame_start
            UserEndFrame = scene.frame_end
            exported_asset_log.extend(bfu_export_single_fbx_nla_anim.process_nla_anim_export_from_asset(op, asset))

            # Resets previous start/end frame
            scene.frame_start = UserStartFrame
            scene.frame_end = UserEndFrame
            export_time_log.end_time_log()
    return exported_asset_log

