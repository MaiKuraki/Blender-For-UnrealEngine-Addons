# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================


import bpy
from typing import List, Optional, Tuple
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport, AssetToSearch, AssetDataSearchMode, AssetType
from .. import bfu_assets_manager
from .. import bfu_export_control
from .. import bfu_debug_settings
from .. import bfu_anim_action
from .. import bfu_base_collection
from . import bfu_cached_assets_types


class BFU_FinalExportAssetCache(bpy.types.PropertyGroup):

    def get_final_asset_list(self, asset_to_search: AssetToSearch = AssetToSearch.ALL_ASSETS, search_mode: AssetDataSearchMode = AssetDataSearchMode.ASSET_NUMBER, force_cache_update: bool = False) -> List[AssetToExport]:
        # Returns all assets that will be exported
        # WARNING: the assets not to be ordered. First asset are exported first.

        events = bfu_debug_settings.root_events
        events.add_sub_event("Get Final Asset List")
        events.add_sub_event("Prepare")

        def get_have_parent_to_export(obj: bpy.types.Object) -> Optional[bpy.types.Object]:
            if obj.parent is not None:
                if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj.parent):
                    return obj.parent
                else:
                    return get_have_parent_to_export(obj.parent)
            else:
                return None

        scene = bpy.context.scene
        export_filter = scene.bfu_export_selection_filter  # type: ignore[attr-defined]

        target_asset_to_export: List[AssetToExport] = []

        events.stop_last_and_start_new_event("Search Assets")
        if asset_to_search.value == AssetToSearch.ALL_ASSETS.value:

            events.add_sub_event("-> S1")
            # Search for objects
            obj_list: List[bpy.types.Object] = []
            if export_filter == "default":
                obj_list = bfu_export_control.bfu_export_control_utils.get_all_export_recursive_objects()

            elif export_filter in ["only_object", "only_object_and_active"]:
                recursive_list = bfu_export_control.bfu_export_control_utils.get_all_export_recursive_objects()

                for obj in bpy.context.selected_objects:
                    if obj in recursive_list:
                        if obj not in obj_list:
                            obj_list.append(obj)
                    parent_target = get_have_parent_to_export(obj)
                    if parent_target is not None:
                        if parent_target not in obj_list:
                            obj_list.append(parent_target)

            events.stop_last_and_start_new_event("-> S2")
            # Search for objects assets
            for obj in obj_list:
                asset_class_list = bfu_assets_manager.bfu_asset_manager_utils.get_all_supported_asset_class(obj)
                for asset_class in asset_class_list:
                    target_asset_to_export.extend(asset_class.get_asset_export_data(obj, None, search_mode=search_mode))

            events.stop_last_event()


        events.stop_last_and_start_new_event("Search Collections")
        if asset_to_search.value in [AssetToSearch.ALL_ASSETS.value, AssetToSearch.COLLECTION_ONLY.value]:
        
            if scene and export_filter == "default":
                collection_list: List[bpy.types.Collection] = []
                events.add_sub_event("-> S1")
            
                # Search for collections
                collection_list = bfu_base_collection.bfu_base_col_utils.optimized_collection_search(scene)

                events.stop_last_and_start_new_event("-> S2")
                # Search for collections assets
                for collection in collection_list:
                    asset_class_list = bfu_assets_manager.bfu_asset_manager_utils.get_all_supported_asset_class(collection)
                    if asset_class_list:
                        for asset_class in asset_class_list:
                            target_asset_to_export.extend(asset_class.get_asset_export_data(collection, None, search_mode=search_mode))

                events.stop_last_event()


        events.stop_last_and_start_new_event("Search Armatures")
        if asset_to_search.value in [AssetToSearch.ALL_ASSETS.value, AssetToSearch.ANIMATION_ONLY.value]:
            events.add_sub_event("-> S1")
            
            # Search for armatures and their actions
            armature_list: List[bpy.types.Object] = []
            if export_filter == "default":
                armature_list = bfu_export_control.bfu_export_control_utils.get_all_export_recursive_armatures()
            elif export_filter in ["only_object", "only_object_and_active"]:
                armature_recursive_list = bfu_export_control.bfu_export_control_utils.get_all_export_recursive_armatures()

                for obj in bpy.context.selected_objects:
                    if obj in armature_recursive_list:
                        if obj not in armature_list:
                            armature_list.append(obj)
                    armature_parent_target = get_have_parent_to_export(obj)
                    if armature_parent_target is not None:
                        if armature_parent_target not in armature_list:
                            armature_list.append(armature_parent_target)

            events.stop_last_and_start_new_event("-> S2")

            armature_actions_map: List[Tuple[bpy.types.Object, bpy.types.Action]] = []
            if export_filter == "only_object_and_active":
                events.add_sub_event("Active Search")
                for armature in armature_list:
                    if armature.animation_data and armature.animation_data.action:
                        armature_actions_map.append((armature, armature.animation_data.action))
                events.stop_last_event()
            else:
                if scene:
                    cached_action_manager = bfu_cached_assets_types.cached_action_manager
                    if force_cache_update or cached_action_manager.get_need_update_cache(scene, armature_list):
                        armature_actions_map = bfu_anim_action.bfu_anim_action_utils.optimizated_asset_search(scene, armature_list)
                        cached_action_manager.set_cache(armature_list, armature_actions_map)
                    else:
                        armature_actions_map = cached_action_manager.get_cache()

            events.stop_last_and_start_new_event("-> S3")

            # Search for actions assets
            for armature, action in armature_actions_map:
                asset_class_list = bfu_assets_manager.bfu_asset_manager_utils.get_all_supported_asset_class(armature, action)
                for asset_class in asset_class_list:
                    target_asset_to_export.extend(asset_class.get_asset_export_data(armature, action, search_mode=search_mode))

            events.stop_last_event()

        events.stop_last_and_start_new_event("Search Other Assets")

        # Reorder the asset list
        asset_type_order = [
            AssetType.COLLECTION_AS_STATIC_MESH,
            AssetType.CAMERA,
            AssetType.SPLINE,
            AssetType.STATIC_MESH,
            AssetType.SKELETAL_MESH,
            AssetType.ANIM_ALEMBIC,
            AssetType.GROOM_SIMULATION,
            AssetType.ANIM_POSE,
            AssetType.ANIM_ACTION,
            AssetType.ANIM_NLA,
        ]

        type_priority = {asset_type: index for index, asset_type in enumerate(asset_type_order)}

        def sort_key(asset: AssetToExport):
            return type_priority.get(asset.asset_type, len(asset_type_order))
        
        target_asset_to_export.sort(key=sort_key)
        events.stop_last_event()
        events.stop_last_event()
        return target_asset_to_export


def get_final_asset_cache() -> BFU_FinalExportAssetCache: # type: ignore
    scene = bpy.context.scene
    if scene:
        return scene.final_asset_cache # type: ignore

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_FinalExportAssetCache,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.final_asset_cache = bpy.props.PointerProperty( # type: ignore
        type=BFU_FinalExportAssetCache,
        options={'LIBRARY_EDITABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        )



def unregister():

    del bpy.types.Scene.final_asset_cache # type: ignore

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    