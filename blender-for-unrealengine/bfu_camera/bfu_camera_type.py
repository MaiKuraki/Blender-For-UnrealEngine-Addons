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
from pathlib import Path
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType


class BFU_Camera(bfu_assets_manager.bfu_asset_manager_type.BFU_BaseAssetClass):
    def __init__(self):
        super().__init__()
        pass

    def support_asset_type(self, obj: bpy.types.Object, details: any = None) -> bool:
        if not isinstance(obj, bpy.types.Object):
            return False
        if obj.type == "CAMERA":
            return True
        return False

    def get_asset_type(self, obj: bpy.types.Object, details: any = None) -> AssetType:
        return AssetType.CAMERA
    
    def get_asset_file_name(self, obj: bpy.types.Object, details: any = None, desired_name: str = "", without_extension: bool = False) -> str:
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


        if desired_name:
            return bfu_basics.ValidFilename(scene.bfu_camera_prefix_export_name+desired_name+fileType)
        return bfu_basics.ValidFilename(scene.bfu_camera_prefix_export_name+obj.name+fileType)

    def get_asset_export_directory_path(self, obj: bpy.types.Object, extra_path: str = "", absolute: bool = True) -> str:
        scene = bpy.context.scene

        # Get root path
        if absolute:
            root_path = Path(bpy.path.abspath(scene.bfu_export_camera_file_path))
        else:
            root_path = Path(scene.bfu_export_camera_file_path)

        # Add obj folder path
        folder_name = bfu_utils.get_export_folder_name(obj)
        dirpath = root_path / folder_name

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)
    
    def get_asset_import_directory_path(self, obj, extra_path = ""):
        scene = bpy.context.scene

        # Get root path
        root_path = Path(scene.bfu_unreal_import_module)

        # Add skeletal subfolder path
        dirpath = root_path / scene.bfu_unreal_import_location / obj.bfu_export_folder_name

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)
    
    def can_export_asset_type(self):
        scene = bpy.context.scene
        return scene.bfu_use_camera_export

    def can_export_asset(self, obj):
        return self.can_export_asset_type()


####################################################################
# UI
####################################################################

    def draw_ui_export_procedure(self, layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object) -> bpy.types.UILayout:
        return bfu_export_procedure.draw_object_export_procedure(layout, obj)
    

# --------------------------------------------
# Register and Unregister functions
# --------------------------------------------

def register():
    bfu_assets_manager.bfu_asset_manager_registred_assets.register_asset_class(BFU_Camera())

def unregister():
    pass
