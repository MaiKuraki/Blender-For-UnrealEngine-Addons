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
import fnmatch
from typing import List
from pathlib import Path
from . import bfu_export_action_animation_package
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType, AssetToExport, AssetDataSearchMode
from .. import bfu_utils
from .. import bfu_basics
from .. import bfu_export_procedure
from .. import bbpl



class BFU_SkeletalAnimation(bfu_assets_manager.bfu_asset_manager_type.BFU_BaseAssetClass):
    def __init__(self):
        super().__init__()
        self.use_materials = True

    def support_asset_type(self, obj: bpy.types.Object, action: bpy.types.Action) -> bool:
        if not isinstance(obj, bpy.types.Object):
            return False
        if not isinstance(action, bpy.types.Action):
            return False

        if obj.type == "ARMATURE" and not obj.bfu_export_skeletal_mesh_as_static_mesh:
            return True
        return False

    def get_asset_type(self, obj: bpy.types.Object, action: bpy.types.Action) -> AssetType:
        if bfu_utils.action_is_one_frame(action):
            return AssetType.ANIM_POSE
        else:
            return AssetType.ANIM_ACTION

    def get_asset_file_type(self, obj):
        return bfu_export_procedure.bfu_skeleton_export_procedure.get_obj_export_type(obj)

    def get_asset_export_name(self, obj):
        if bfu_utils.GetExportAsProxy(obj):
            proxy_child = bfu_utils.GetExportProxyChild(obj)
            if proxy_child is not None:
                return bfu_basics.ValidFilename(proxy_child.name)
        return super().get_asset_export_name(obj)

    def get_asset_file_name(self, obj: bpy.types.Object, action: bpy.types.Action = None, desired_name: str = "", without_extension: bool = False) -> str:
        # Generate assset file name for skeletal mesh
        scene = bpy.context.scene
        if obj.bfu_use_custom_export_name:
            if obj.bfu_custom_export_name:
                return obj.bfu_custom_export_name
            
        if without_extension:
            fileType = ""
        else:
            asset_type = self.get_asset_file_type(obj)
            if asset_type == "FBX":
                fileType = ".fbx"
            elif asset_type == "GLTF":
                fileType = ".glb"

        if self.get_asset_type(obj, action) == AssetType.ANIM_POSE:
            if desired_name:
                return bfu_basics.ValidFilename(scene.bfu_pose_prefix_export_name+desired_name+fileType)
            return bfu_basics.ValidFilename(scene.bfu_pose_prefix_export_name+action.name+fileType)
        else:
            if desired_name:
                return bfu_basics.ValidFilename(scene.bfu_anim_prefix_export_name+desired_name+fileType)
            return bfu_basics.ValidFilename(scene.bfu_anim_prefix_export_name+action.name+fileType)

    def get_asset_export_directory_path(self, obj: bpy.types.Object, extra_path: str = "", absolute: bool = True) -> str:
        scene = bpy.context.scene

        # Get root path
        if absolute:
            root_path = Path(bpy.path.abspath(scene.bfu_export_skeletal_file_path))
        else:
            root_path = Path(scene.bfu_export_skeletal_file_path)

        # Add obj folder path
        folder_name = bfu_utils.get_export_folder_name(obj)
        dirpath = root_path / folder_name

        # Add skeletal subfolder and animation subfolder
        if obj.bfu_create_sub_folder_with_skeletal_mesh_name:
            dirpath = dirpath / self.get_asset_export_name(obj) / scene.bfu_anim_subfolder_name
        else:
            dirpath = dirpath / scene.bfu_anim_subfolder_name

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)
    
    def get_asset_import_directory_path(self, obj, extra_path = ""):
        scene = bpy.context.scene

        # Get root path
        root_path = Path(scene.bfu_unreal_import_module)

        # Add skeletal subfolder and animation subfolder
        dirpath = root_path / scene.bfu_unreal_import_location / obj.bfu_export_folder_name / scene.bfu_anim_subfolder_name

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)
    
    def get_meshs_object_for_skeletal_mesh(self, obj):
        meshs = []
        if self.support_asset_type(obj):  # Skeleton /  Armature
            childs = bfu_utils.GetExportDesiredChilds(obj)
            for child in childs:
                if child.type == "MESH":
                    meshs.append(child)
        return meshs

    def can_export_asset_type(self):
        scene = bpy.context.scene
        return scene.bfu_use_skeletal_export

    def can_export_asset(self, obj):
        return self.can_export_asset_type()

    def get_asset_export_data(self, obj: bpy.types.Object, action: bpy.types.Action, search_mode: AssetDataSearchMode) -> List[AssetToExport]:
        asset_list = []
        scene = bpy.context.scene
        addon_prefs = bfu_basics.GetAddonPrefs()
        if scene.bfu_use_anim_export:

            asset_name = f"{obj.name}_{action.name}"
            if bfu_utils.action_is_one_frame(action):
                # Action
                asset = AssetToExport(asset_name, AssetType.ANIM_POSE)
                asset_list.append(asset)
            else:
                # Pose
                asset = AssetToExport(asset_name, AssetType.ANIM_ACTION)
                asset_list.append(asset)

            import_dirpath = self.get_asset_import_directory_path(obj)
            asset.set_import_name(self.get_asset_file_name(obj, action, without_extension=True))
            asset.set_import_dirpath(import_dirpath)

            if search_mode.search_packages():

                pak = asset.add_asset_package(action.name, ["Action"])

                # Set the export dirpath
                dirpath = self.get_asset_export_directory_path(obj, "", True)
                file_name = self.get_asset_file_name(obj, action)
                file_type = self.get_asset_file_type(obj)
                pak.set_file(dirpath, file_name, file_type)

                if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
                    file_name_without_extension = self.get_asset_file_name(obj, action, without_extension=True)
                    additional_data = asset.set_asset_additional_data(self.get_asset_additional_data(obj))
                    additional_data.set_file(dirpath, f"{file_name_without_extension}_additional_data.json")

                if search_mode.search_package_content():
                    pak.add_objects(self.get_asset_export_content(obj))
                    pak.set_action(action)
                    frame_range = bfu_utils.get_desired_action_start_end_range(obj, action)
                    pak.set_frame_range(frame_range[0], frame_range[1])
                    pak.export_function = bfu_export_action_animation_package.process_action_animation_export_from_package
                            
        return asset_list
    
    def get_asset_export_content(self, obj: bpy.types.Object) -> List[bpy.types.Object]:

        if obj.bfu_export_animation_without_mesh:
            # If the animation is exported without mesh, we only need the armature object
            return [obj]
        else:
            desired_obj_list = []
            desired_obj_list.append(obj)
            for child in bbpl.basics.get_recursive_obj_childs(obj):
                if child.bfu_export_type != "dont_export":
                    if child.name in bpy.context.window.view_layer.objects:
                        desired_obj_list.append(child)

        return desired_obj_list

def register():
    bfu_assets_manager.bfu_asset_manager_registred_assets.register_asset_class(BFU_SkeletalAnimation())

def unregister():
    pass