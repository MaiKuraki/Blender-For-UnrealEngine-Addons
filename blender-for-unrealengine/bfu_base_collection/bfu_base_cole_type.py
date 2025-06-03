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
from typing import List
from . import bfu_export_collection_as_static_mesh_package
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType, AssetToExport, AssetDataSearchMode
from .. import bbpl
from .. import bfu_export_procedure
from .. import bfu_socket
from .. import bfu_light_map
from .. import bfu_nanite
from .. import bfu_vertex_color
from .. import bfu_material
from .. import bfu_lod




class BFU_StaticMesh_Collection(bfu_assets_manager.bfu_asset_manager_type.BFU_BaseAssetClass):
    def __init__(self):
        super().__init__()
        self.use_lods = True
        self.use_materials = True

    def support_asset_type(self, col: bpy.types.Collection, details: any = None) -> bool:
        if not isinstance(col, bpy.types.Collection):
            return False
        return True

    def get_asset_type(self, col: bpy.types.Collection, details: any = None) -> AssetType:
        return AssetType.COLLECTION_AS_STATIC_MESH

    def get_asset_file_type(self, col: bpy.types.Collection) -> str:
        return bfu_export_procedure.bfu_collection_export_procedure.get_col_export_type(col)

    def get_asset_file_name(self, col: bpy.types.Collection, details: any = None, desired_name: str = "", without_extension: bool = False) -> str:
        # Generate assset file name for skeletal mesh
        scene = bpy.context.scene

        if without_extension:
            fileType = ""
        else:
            asset_type = self.get_asset_file_type(col)
            if asset_type == "FBX":
                fileType = ".fbx"
            elif asset_type == "GLTF":
                fileType = ".glb"


        if desired_name:
            return bfu_basics.ValidFilename(scene.bfu_static_mesh_prefix_export_name+desired_name+fileType)
        return bfu_basics.ValidFilename(scene.bfu_static_mesh_prefix_export_name+col.name+fileType)

    def get_asset_export_directory_path(self, col: bpy.types.Collection, extra_path = "", absolute = True):
        scene = bpy.context.scene

        # Get root path
        if absolute:
            root_path = Path(bpy.path.abspath(scene.bfu_export_static_file_path))
        else:
            root_path = Path(scene.bfu_export_static_file_path)

        # Add obj folder path
        folder_name = bfu_utils.get_export_folder_name(col)
        dirpath = root_path / folder_name

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)

    def get_asset_import_directory_path(self, col: bpy.types.Collection, extra_path = ""):
        scene = bpy.context.scene

        # Get root path
        root_path = Path(scene.bfu_unreal_import_module)

        # Add skeletal subfolder path
        dirpath = root_path / scene.bfu_unreal_import_location / col.bfu_export_folder_name

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)
    
    def can_export_asset_type(self):
        scene = bpy.context.scene
        return scene.bfu_use_static_export

    def can_export_asset(self, obj):
        return self.can_export_asset_type()

    def get_asset_export_data(self, col: bpy.types.Collection, details: any, search_mode: AssetDataSearchMode) -> List[AssetToExport]:
        asset_list = []
        scene = bpy.context.scene
        addon_prefs = bfu_basics.GetAddonPrefs()
        if scene.bfu_use_static_collection_export:
            asset = AssetToExport(col, None, AssetType.COLLECTION_AS_STATIC_MESH)

            import_dirpath = self.get_asset_import_directory_path(col)
            asset.set_import_name(self.get_asset_file_name(col, without_extension=True))
            asset.set_import_dirpath(import_dirpath)
            asset_list.append(asset)

            if search_mode.search_packages():
                pak = asset.add_asset_package(col.name, ["Collection"])

                # Set the export dirpath
                dirpath = self.get_asset_export_directory_path(col, "", True)
                file_name = self.get_asset_file_name(col)
                file_type = self.get_asset_file_type(col)
                pak.set_file(dirpath, file_name, file_type)
                        

                if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
                    file_name_without_extension = self.get_asset_file_name(col, without_extension=True)
                    additional_data = asset.set_asset_additional_data(self.get_asset_additional_data(col))
                    additional_data.set_file(dirpath, f"{file_name_without_extension}_additional_data.json")

                if search_mode.search_package_content():
                    pak.set_collection(col)

                    pak.export_function = bfu_export_collection_as_static_mesh_package.process_collection_as_static_mesh_export_from_package

            

        return asset_list


    def get_asset_additional_data(self, col: bpy.types.Collection) -> dict:
        data = {}

        data.update(bfu_vertex_color.bfu_vertex_color_utils.get_vertex_color_additional_data(col, AssetType.COLLECTION_AS_STATIC_MESH))
        data.update(bfu_material.bfu_material_utils.get_material_asset_additional_data(col, AssetType.COLLECTION_AS_STATIC_MESH))
        data.update(bfu_light_map.bfu_light_map_utils.get_light_map_additional_data(col, AssetType.COLLECTION_AS_STATIC_MESH))
        data.update(bfu_nanite.bfu_nanite_utils.get_nanite_asset_additional_data(col, AssetType.COLLECTION_AS_STATIC_MESH))
        return data



def register():
    bfu_assets_manager.bfu_asset_manager_registred_assets.register_asset_class(BFU_StaticMesh_Collection())

def unregister():
    pass
