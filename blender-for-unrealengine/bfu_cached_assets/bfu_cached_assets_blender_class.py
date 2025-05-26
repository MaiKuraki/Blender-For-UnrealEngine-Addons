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
from typing import TYPE_CHECKING, List

from . import bfu_cached_assets_types
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_camera
from .. import bfu_alembic_animation
from .. import bfu_groom
from .. import bfu_spline
from .. import bfu_skeletal_mesh
from .. import bfu_static_mesh
from .. import bfu_assets_manager
from .. import bfu_modular_skeletal_mesh






MyCachedActions = bfu_cached_assets_types.CachedAction()


class BFU_CollectionExportAssetCache(bpy.types.PropertyGroup):

    def GetCollectionAssetList(self):

        scene = self.id_data
        collection_export_asset_list = []

        for col in scene.bfu_collection_asset_list:
            if col.use:
                if col.name in bpy.data.collections:
                    collection = bpy.data.collections[col.name]
                    collection_export_asset_list.append(collection)
        return collection_export_asset_list


class BFU_AnimationExportAssetCache(bpy.types.PropertyGroup):

    def UpdateActionCache(self):
        # Force update cache export auto action list
        return self.GetCachedExportAutoActionList(True)

    def GetCachedExportAutoActionList(self, force_update_cache=False):
        # This will cheak if the action contains
        # the same bones of the armature
        
        obj = self.id_data
        actions = []

        # Use the cache
        if force_update_cache:
            MyCachedActions.is_cached = False

        if MyCachedActions.CheckCache(obj):
            actions = MyCachedActions.GetStoredActions()

        else:
            MyCachedActions.Clear()

            objBoneNames = [bone.name for bone in obj.data.bones]
            for action in bpy.data.actions:
                if action.library is None:
                    if bfu_basics.GetIfActionIsAssociated(action, objBoneNames):
                        actions.append(action)
            # Update the cache
            MyCachedActions.StoreActions(obj, actions)
        return actions

    def GetAnimationAssetList(self):
        # Returns only the actions that will be exported with the Armature

        obj = self.id_data

        if obj.bfu_export_as_lod_mesh:
            return []

        TargetActionToExport = []  # Action list
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
                            TargetActionToExport.append(action)

        elif obj.bfu_anim_action_export_enum == "export_specific_prefix":
            for action in bpy.data.actions:
                if fnmatch.fnmatchcase(action.name, obj.bfu_prefix_name_to_export+"*"):
                    TargetActionToExport.append(action)

        elif obj.bfu_anim_action_export_enum == "export_auto":
            TargetActionToExport = self.GetCachedExportAutoActionList(obj)

        return TargetActionToExport


class BFU_FinalExportAssetCache(bpy.types.PropertyGroup):

    def GetFinalAssetList(self) -> List[bfu_cached_assets_types.AssetToExport]:
        # Returns all assets that will be exported

        def getHaveParentToExport(obj):
            if obj.parent is not None:
                if obj.parent.bfu_export_type == 'export_recursive':
                    return obj.parent
                else:
                    return getHaveParentToExport(obj.parent)
            else:
                return None

        scene = bpy.context.scene
        export_filter = scene.bfu_export_selection_filter

        TargetAssetToExport = []  # Obj, Action, type

        objList = []
        collectionList = []

        if export_filter == "default":
            objList = bfu_utils.GetAllobjectsByExportType("export_recursive")
            collection_asset_cache = GetCollectionAssetCache()
            collection_export_asset_list = collection_asset_cache.GetCollectionAssetList()
            for col_asset in collection_export_asset_list:
                if col_asset.name in bpy.data.collections:
                    collection = bpy.data.collections[col_asset.name]
                    collectionList.append(collection)
                

        elif export_filter == "only_object" or export_filter == "only_object_action":
            recuList = bfu_utils.GetAllobjectsByExportType("export_recursive")

            for obj in bpy.context.selected_objects:
                if obj in recuList:
                    if obj not in objList:
                        objList.append(obj)
                parentTarget = getHaveParentToExport(obj)
                if parentTarget is not None:
                    if parentTarget not in objList:
                        objList.append(parentTarget)

        for collection in collectionList:
            # Collection
            if scene.bfu_use_static_collection_export:
                TargetAssetToExport.append(bfu_cached_assets_types.AssetToExport(collection, None, "Collection StaticMesh"))

        for obj in objList:


            if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj):

                # Skeletal Mesh
                if scene.bfu_use_skeletal_export:
                    if obj.bfu_modular_skeletal_mesh_mode == "all_in_one":
                        asset = bfu_cached_assets_types.AssetToExport(obj, None, "SkeletalMesh")
                        asset.name = obj.name
                        asset.obj_list = bfu_utils.GetExportDesiredChilds(obj)
                        TargetAssetToExport.append(asset)
                    elif obj.bfu_modular_skeletal_mesh_mode == "every_meshs":
                        for mesh in bbpl.basics.get_obj_childs(obj):
                            asset = bfu_cached_assets_types.AssetToExport(obj, None, "SkeletalMesh")
                            asset.name = obj.name + obj.bfu_modular_skeletal_mesh_every_meshs_separate + mesh.name
                            asset.obj_list = [mesh]
                            TargetAssetToExport.append(asset)
                    elif obj.bfu_modular_skeletal_mesh_mode == "specified_parts":
                        TargetAssetToExport.extend(bfu_modular_skeletal_mesh.bfu_modular_skeletal_mesh_utils.get_assets_to_export_for_modular_skeletal_mesh(obj))



                # NLA
                if scene.bfu_use_anin_export:
                    if obj.bfu_anim_nla_use:
                        TargetAssetToExport.append(bfu_cached_assets_types.AssetToExport(obj, obj.animation_data, "NlAnim"))

                animation_asset_cache = GetAnimationAssetCache(obj)
                animation_to_export = animation_asset_cache.GetAnimationAssetList()
                for action in animation_to_export:
                    if scene.bfu_export_selection_filter == "only_object_action":
                        if obj.animation_data:
                            if obj.animation_data.action == action:
                                TargetAssetToExport.append(bfu_cached_assets_types.AssetToExport(obj, action, "Action"))
                    else:
                        # Action
                        if scene.bfu_use_anin_export:
                            if bfu_utils.GetActionType(action) == "Action":
                                TargetAssetToExport.append(bfu_cached_assets_types.AssetToExport(obj, action, "Action"))

                        # Pose
                        if scene.bfu_use_anin_export:
                            if bfu_utils.GetActionType(action) == "Pose":
                                TargetAssetToExport.append(bfu_cached_assets_types.AssetToExport(obj, action, "Pose"))
            # Others
            else:
                asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_asset_class(obj)
                if asset_class and asset_class.can_export_obj_asset(obj):
                    TargetAssetToExport.append(bfu_cached_assets_types.AssetToExport(obj, None, asset_class.get_asset_type_name(obj)))


        return TargetAssetToExport

def GetCollectionAssetCache() -> BFU_CollectionExportAssetCache:
    scene = bpy.context.scene
    return scene.collection_asset_cache

def GetAnimationAssetCache(obj) -> BFU_AnimationExportAssetCache:
    return obj.animation_asset_cache

def GetfinalAssetCache() -> BFU_FinalExportAssetCache:
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