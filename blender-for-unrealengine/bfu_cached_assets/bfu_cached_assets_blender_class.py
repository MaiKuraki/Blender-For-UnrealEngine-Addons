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
import fnmatch
from typing import List, Optional, Tuple

from . import bfu_cached_assets_types
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport, AssetToSearch, AssetDataSearchMode, AssetType
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_assets_manager
from .. import bfu_export_control






MyCachedActions = bfu_cached_assets_types.CachedAction()


class BFU_CollectionExportAssetCache(bpy.types.PropertyGroup):

    def get_collection_asset_list(self):

        scene: bpy.types.Scene = self.id_data
        collection_export_asset_list: list[bpy.types.Collection] = []

        for col in scene.bfu_collection_asset_list:
            col: bpy.types.Collection
            if col.use:
                if col.name in bpy.data.collections:
                    collection = bpy.data.collections[col.name]
                    collection_export_asset_list.append(collection)
        return collection_export_asset_list


class BFU_AnimationExportAssetCache(bpy.types.PropertyGroup):

    def UpdateActionCache(self):
        # Force update cache export auto action list
        return self.get_cached_export_auto_action_list(True)

    def get_cached_export_auto_action_list(self, force_update_cache: bool = False)-> list[bpy.types.Action]:
        # This will cheak if the action contains
        # the same bones of the armature

        obj: bpy.types.Object = self.id_data
        actions: list[bpy.types.Action] = []

        # Use the cache
        if force_update_cache:
            MyCachedActions.is_cached = False

        if MyCachedActions.check_cache(obj):
            actions = MyCachedActions.get_stored_actions()

        else:
            MyCachedActions.clear()

            obj_bone_names: List[str] = [bone.name for bone in obj.data.bones]
            for action in bpy.data.actions:
                if action.library is None:
                    if bfu_basics.get_if_action_can_associate_bone(action, obj_bone_names):
                        actions.append(action)
            # Update the cache
            MyCachedActions.store_actions(obj, actions)
        return actions
   
    def get_animation_asset_list(self):
        # Returns only the actions that will be exported with the Armature

        obj: bpy.types.Object = self.id_data

        if obj.bfu_export_as_lod_mesh:
            return []

        target_action_to_export: list[bpy.types.Action] = []  # Action list
        if obj.bfu_anim_action_export_enum == "dont_export":
            return []

        if obj.bfu_anim_action_export_enum == "export_current":
            if obj.animation_data is not None:
                if obj.animation_data.action is not None:
                    return [obj.animation_data.action]

        elif obj.bfu_anim_action_export_enum == "export_specific_list":
            for action in bpy.data.actions:
                for targetAction in obj.bfu_action_asset_list:
                    if targetAction.use:
                        if targetAction.name == action.name:
                            target_action_to_export.append(action)

        elif obj.bfu_anim_action_export_enum == "export_specific_prefix":
            for action in bpy.data.actions:
                if fnmatch.fnmatchcase(action.name, obj.bfu_prefix_name_to_export+"*"):
                    target_action_to_export.append(action)

        elif obj.bfu_anim_action_export_enum == "export_auto":
            target_action_to_export = self.get_cached_export_auto_action_list(obj)

        return target_action_to_export
    


class BFU_FinalExportAssetCache(bpy.types.PropertyGroup):

    def get_final_asset_list(self, asset_to_search: AssetToSearch = AssetToSearch.ALL_ASSETS, search_mode: AssetDataSearchMode = AssetDataSearchMode.ASSET_NUMBER) -> List[AssetToExport]:
        # Returns all assets that will be exported
        # WARNING: the assets not to be ordered. First asset are exported first.

        if bpy.context is None:
            return []

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

        if asset_to_search.value == AssetToSearch.ALL_ASSETS.value:
            # Search for collections
            collection_list: List[bpy.types.Collection] = []
            if export_filter == "default":
                collection_asset_cache = get_collectiona_asset_cache()
                collection_export_asset_list = collection_asset_cache.get_collection_asset_list()
                for col_asset in collection_export_asset_list:
                    if col_asset.name in bpy.data.collections:
                        collection = bpy.data.collections[col_asset.name]
                        collection_list.append(collection)

            # Search for collections assets
            for collection in collection_list:
                asset_class_list = bfu_assets_manager.bfu_asset_manager_utils.get_all_supported_asset_class(collection)
                if asset_class_list:
                    for asset_class in asset_class_list:
                        target_asset_to_export.extend(asset_class.get_asset_export_data(collection, None, search_mode=search_mode))

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

            # Search for objects assets
            for obj in obj_list:
                asset_class_list = bfu_assets_manager.bfu_asset_manager_utils.get_all_supported_asset_class(obj)
                for asset_class in asset_class_list:
                    target_asset_to_export.extend(asset_class.get_asset_export_data(obj, None, search_mode=search_mode))

        if asset_to_search.value in [AssetToSearch.ALL_ASSETS.value, AssetToSearch.ANIMATION_ONLY.value]:
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

            armature_actions_map: List[Tuple[bpy.types.Object, bpy.types.Action]] = []
            if export_filter == "only_object_and_active":
                for armature in armature_list:
                    if armature.animation_data and armature.animation_data.action:
                        armature_actions_map.append((armature, armature.animation_data.action))
            else:
                for armature in armature_list:
                    if isinstance(armature.data, bpy.types.Armature):
                        obj_bone_names: List[str] = [bone.name for bone in armature.data.bones]
                        for action in bpy.data.actions:
                            if not action.library:
                                if bfu_basics.get_if_action_can_associate_bone(action, obj_bone_names):
                                    armature_actions_map.append((armature, action))


            # Search for actions assets
            for armature, action in armature_actions_map:
                asset_class_list = bfu_assets_manager.bfu_asset_manager_utils.get_all_supported_asset_class(armature, action)
                for asset_class in asset_class_list:
                    target_asset_to_export.extend(asset_class.get_asset_export_data(armature, action, search_mode=search_mode))

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
        return target_asset_to_export
  
        # NLA
        if scene.bfu_use_animation_export:
            if obj.bfu_anim_nla_use:
                TargetAssetToExport.append(AssetToExport(obj, obj.animation_data, AssetType.ANIM_NLA))

        animation_asset_cache = get_animation_asset_cache(obj)
        animation_to_export = animation_asset_cache.GetAnimationAssetList()
        for action in animation_to_export:
            if scene.bfu_export_selection_filter == "only_object_and_active":
                if obj.animation_data:
                    if obj.animation_data.action == action:
                        TargetAssetToExport.append(AssetToExport(obj, action, AssetType.ANIM_ACTION))
            else:
                if scene.bfu_use_animation_export:
                    
                    if bfu_utils.action_is_one_frame(action) == True:
                        # Action
                        TargetAssetToExport.append(AssetToExport(obj, action, AssetType.ANIM_ACTION))
                    else:
                        # Pose
                        TargetAssetToExport.append(AssetToExport(obj, action, AssetType.ANIM_POSE))
        # Others
        asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_asset_class(obj)
        if asset_class and asset_class.can_export_asset(obj):
            TargetAssetToExport.append(AssetToExport(obj, None, asset_class.get_asset_type(obj)))




def get_collectiona_asset_cache() -> BFU_CollectionExportAssetCache:
    scene = bpy.context.scene
    return scene.collection_asset_cache

def get_animation_asset_cache(obj: bpy.types.Object) -> BFU_AnimationExportAssetCache:
    return obj.animation_asset_cache

def get_final_asset_cache() -> BFU_FinalExportAssetCache:
    scene = bpy.context.scene
    return scene.final_asset_cache

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (

    BFU_CollectionExportAssetCache,
    BFU_AnimationExportAssetCache,
    BFU_FinalExportAssetCache,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)



    bpy.types.Scene.collection_asset_cache = bpy.props.PointerProperty(
        type=BFU_CollectionExportAssetCache,
        options={'LIBRARY_EDITABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        )

    bpy.types.Object.animation_asset_cache = bpy.props.PointerProperty(
        type=BFU_AnimationExportAssetCache,
        options={'LIBRARY_EDITABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        )
    
    bpy.types.Scene.final_asset_cache = bpy.props.PointerProperty(
        type=BFU_FinalExportAssetCache,
        options={'LIBRARY_EDITABLE'},
        override={'LIBRARY_OVERRIDABLE'},
        )



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)