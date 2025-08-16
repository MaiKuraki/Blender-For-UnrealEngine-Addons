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

from pathlib import Path
from typing import List, Any, Optional, Dict
import bpy
from . import bfu_export_procedure
from . import bfu_export_spline_package
from .. import bfu_spline
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType, BFU_ObjectAssetClass, AssetDataSearchMode, AssetToExport
from .. import bfu_export_nomenclature
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum
from .. import bfu_export_filter


class BFU_Spline(BFU_ObjectAssetClass):
    def __init__(self):
        super().__init__()

# ###################################################################
# # Asset Root Class
# ###################################################################

    def support_asset_type(self, data: Any, details: Any = None) -> bool:
        if not isinstance(data, bpy.types.Object):
            return False
        if details is not None:
            return False
        if data.bfu_export_spline_as_static_mesh:  # type: ignore
            return False
        if data.type == "CURVE":  # type: ignore
            return True
        return False

    def get_asset_type(self, data: Any, details: Any = None) -> AssetType:
        return AssetType.SPLINE
    
    def can_export_asset_type(self) -> bool:
        return bfu_export_filter.bfu_export_filter_utils.get_use_spline_export()

    def get_asset_import_directory_path(self, data: Any, details: Any = None, extra_path: Optional[Path] = None) -> Path:
        dirpath = bfu_export_nomenclature.bfu_export_nomenclature_utils.get_obj_import_location(data)
        return dirpath if extra_path is None else dirpath / extra_path  # Add extra path if provided

####################################################################
# Asset Package Management
####################################################################

    def get_package_file_prefix(self, data: Any, details: Any = None) -> str:
        if bpy.context:
            return bpy.context.scene.bfu_spline_prefix_export_name  # type: ignore
        return ""

    def get_export_file_path(self, data: Any, details: Any = None) -> str:
        if bpy.context:
            scene = bpy.context.scene
            return scene.bfu_export_spline_file_path  # type: ignore[attr-defined]
        return ""

    def get_package_file_type(self, data: bpy.types.Object, details: Any = None) -> BFU_FileTypeEnum:
        return bfu_export_procedure.get_obj_export_file_type(data)

####################################################################
# UI
####################################################################

    def draw_ui_export_procedure(self, layout: bpy.types.UILayout, context: bpy.types.Context, data: bpy.types.Object) -> bpy.types.UILayout:
        return bfu_export_procedure.draw_object_export_procedure(layout, data)
    
# ####################################################################
# # Asset Construction
# ####################################################################

    def get_asset_export_data(self, data: bpy.types.Object, details: Any, search_mode: AssetDataSearchMode) -> List[AssetToExport]:
        asset_list: List[AssetToExport] = []

        # One asset per alembic animation pack
        asset = AssetToExport(self, data.name, AssetType.STATIC_MESH)
        asset.set_import_name(self.get_package_file_name(data, without_extension=True))
        asset.set_import_dirpath(self.get_asset_import_directory_path(data))
    
        if search_mode.search_packages():
            if not bfu_export_procedure.get_object_export_additional_data_only(data):
                pak = asset.add_asset_package(data.name, ["Spline"])
                self.set_package_file(pak, data, details)

                if search_mode.search_package_content():
                    pak.add_object(data)
                    pak.export_function = bfu_export_spline_package.process_spline_export_from_package

        # Set the additional data in the asset, add asset to the list and return the list.
        self.set_additional_data_in_asset(asset, data, details, search_mode)
        asset_list.append(asset)
        return asset_list

    def get_asset_additional_data(self, data: bpy.types.Object, details: Any, search_mode: AssetDataSearchMode) -> Dict[str, Any]:
        additional_data: Dict[str, Any] = {}
        if search_mode.value == AssetDataSearchMode.FULL.value:
            pre_bake_spline = bfu_spline.bfu_spline_data.BFU_SplinesList(data)
            if search_mode.search_package_content():
                pre_bake_spline.evaluate_spline_obj_data(data)
            additional_data.update(bfu_spline.bfu_spline_write_text.write_spline_points_data(data, pre_bake_spline=pre_bake_spline))
        return additional_data

# --------------------------------------------
# Register and Unregister functions
# --------------------------------------------

def register():
    my_asset_class = BFU_Spline()
    bfu_assets_manager.bfu_asset_manager_registred_assets.register_asset_class(my_asset_class, "Object")

def unregister():
    pass