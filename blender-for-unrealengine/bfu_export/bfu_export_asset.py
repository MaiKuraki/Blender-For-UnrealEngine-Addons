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
from .. import bbpl
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport
from .. import bfu_basics
from .. import bfu_export_logs
from .. import bfu_addon_prefs
from . import bfu_export_single_generic


def IsValidActionForExport(scene, obj, animType):
    if animType == "Action":
        if scene.bfu_use_animation_export:
            return True
        else:
            return False
    elif animType == "Pose":
        if scene.bfu_use_animation_export:
            return True
        else:
            return False
    elif animType == "NLA":
        if scene.bfu_use_animation_export:
            return True
        else:
            False
    else:
        print("Error in IsValidActionForExport() animType not found: ", animType)
    return False


def IsValidDataForExport(scene, obj):
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
    return asset_class.can_export_asset(obj)

def prepare_scene_for_export():
    if bpy.context is None:
        return
    
    scene = bpy.context.scene

    #Unhide all objects, but hide on viewport and make them selectable
    for obj in scene.objects:
        if obj.hide_select:
            obj.hide_select = False
        if obj.hide_viewport is False:
            obj.hide_viewport = True
        if obj.hide_get():
            obj.hide_set(False)

    # Hhide all collections on viewport and make them selectable
    for col in bpy.data.collections:
        if col.hide_select:
            col.hide_select = False
        if col.hide_viewport:
            col.hide_viewport = False

    # Unexclude all layer collections and hide them on viewport
    for vlayer in bpy.context.scene.view_layers:
        layer_collections = bbpl.utils.get_layer_collections_recursive(vlayer.layer_collection)
        for layer_collection in layer_collections:
            if layer_collection.exclude:
                layer_collection.exclude = False
            if layer_collection.hide_viewport:
                layer_collection.hide_viewport = False

def process_export(op: bpy.types.Operator, final_asset_list_to_export: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs_types.ExportedAssetLog]:
    prepare_all_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("Prepare all export")

    scene = bpy.context.scene
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Save scene data before export
    local_view_areas = bbpl.scene_utils.move_to_global_view()
    user_scene_save = bbpl.save_data.scene_save.UserSceneSave()
    user_scene_save.save_current_scene()
    
    prepare_scene_for_export()
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


def export_all_from_asset_list(op, asset_list: List[AssetToExport]) -> List[bfu_export_logs.bfu_asset_export_logs_types.ExportedAssetLog]:
    scene = bpy.context.scene

    export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("TOTAL EXPORT")
    exported_asset_log = []

    for asset in asset_list:
        export_asset_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Export '{asset.name}' as {asset.asset_type.get_friendly_name()}.")
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