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
from typing import List, Any, Optional, Dict, TYPE_CHECKING
from pathlib import Path
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType, AssetToExport, AssetDataSearchMode, BFU_ObjectAssetClass
from .. import bfu_utils
from .. import bfu_basics
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum
from .. import bfu_export_nomenclature
from .. import bfu_base_object
from .. import bfu_anim_action
from .. import bfu_export_filter
from . import bfu_export_action_package
from . import bfu_export_procedure




class BFU_SkeletalAnimation(BFU_ObjectAssetClass):
    def __init__(self):
        super().__init__()
        self.use_materials = True


# ###################################################################
# # Asset Root Class
# ###################################################################

    def support_asset_type(self, data: Any, details: Any = None) -> bool:
        if not isinstance(data, bpy.types.Object):
            return False
        if not isinstance(details, bpy.types.Action):
            return False
        if not bfu_anim_action.bfu_anim_action_utils.object_support_action_export(data):
            return False
        if isinstance(data.data, bpy.types.Armature):  # type: ignore[attr-defined]
            return True # The rest is already checked before in bfu_anim_action.bfu_anim_action_utils.optimizated_asset_search()
        return False

    def get_asset_type(self, data: Any, details: Any = None) -> AssetType:
        if bfu_utils.action_is_one_frame(details):
            return AssetType.ANIM_POSE
        else:
            return AssetType.ANIM_ACTION

    def can_export_asset_type(self) -> bool:
        return bfu_export_filter.bfu_export_filter_utils.get_use_animation_export()

    def get_asset_import_directory_path(self, data: Any, details: Any = None, extra_path: Optional[Path] = None) -> Path:
        anim_subfolder_name: str = ""
        scene = bpy.context.scene
        if scene is not None:
            if TYPE_CHECKING:
                anim_subfolder_name = ""
            else:
                anim_subfolder_name = scene.bfu_anim_subfolder_name  # type: ignore[attr-defined]

        dirpath: Path = bfu_export_nomenclature.bfu_export_nomenclature_utils.get_obj_import_location(data)
        dirpath /= anim_subfolder_name
        return dirpath if extra_path is None else dirpath / extra_path  # Add extra path if provided

####################################################################
# Asset Package Management
####################################################################

    def get_package_file_prefix(self, data: Any, details: Any = None) -> str:
        if bpy.context:
            scene = bpy.context.scene
            if self.get_asset_type(data, details) == AssetType.ANIM_POSE:
                return scene.bfu_pose_prefix_export_name  # type: ignore[attr-defined]
            else:
                return scene.bfu_anim_prefix_export_name  # type: ignore[attr-defined]
        else:
            return ""
        
    def get_export_file_path(self, data: Any, details: Any = None) -> str:
        if bpy.context:
            scene = bpy.context.scene
            return scene.bfu_export_skeletal_file_path  # type: ignore[attr-defined]
        return ""

    def get_package_file_type(self, data: bpy.types.Object, details: Any = None) -> BFU_FileTypeEnum:
        return bfu_export_procedure.get_obj_export_file_type(data)

    def get_package_file_name(self, data: bpy.types.Object, details: Any = None, desired_name: str = "", without_extension: bool = False) -> str:
        return super().get_package_file_name(
            data,
            details,
            desired_name=details.name,
            without_extension=without_extension,
        )

    def get_asset_folder_path(self, data: bpy.types.Object, details: Any = None) -> Path:
        # Add skeletal sub folder path
        if bpy.context:
            scene = bpy.context.scene
            if data.bfu_create_sub_folder_with_skeletal_mesh_name:  # type: ignore[attr-defined]
                sub_folder = bfu_basics.valid_file_name(data.name)
                return Path(sub_folder) / scene.bfu_anim_subfolder_name  # type: ignore[attr-defined]
        return Path()
   
# ###################################################################
# # UI
# ###################################################################

    def draw_ui_export_procedure(self, layout: bpy.types.UILayout, context: bpy.types.Context, data: bpy.types.Object) -> bpy.types.UILayout:
        # Skeletal use the skeletal mesh export procedure.
        return layout

# ####################################################################
# # Asset Construction
# ####################################################################

    def get_asset_export_data(self, data: bpy.types.Object, details: bpy.types.Action, search_mode: AssetDataSearchMode) -> List[AssetToExport]:
        asset_list: List[AssetToExport] = []

        # One asset per action. Can be action or pose for one frame actions.
        # In the future I will add the support for multiple pose asset per action framess.
        asset_name = f"{data.name}_{details.name}"
        asset_type = AssetType.ANIM_POSE if bfu_utils.action_is_one_frame(details) else AssetType.ANIM_ACTION
        asset = AssetToExport(self, asset_name, asset_type)
        asset.set_import_name(self.get_package_file_name(data, details, without_extension=True))
        asset.set_import_dirpath(self.get_asset_import_directory_path(data))

        if search_mode.search_packages():

            pak = asset.add_asset_package(details.name, ["Action"])
            self.set_package_file(pak, data, details)

            if search_mode.search_package_content():
                if data.bfu_export_animation_without_mesh: # type: ignore[attr-defined]
                    pak.add_object(data)
                else:
                    pak.add_objects(bfu_base_object.bfu_base_obj_utils.get_exportable_objects(data))
                pak.set_action(details)
                frame_range = bfu_utils.get_desired_action_start_end_range(data, details)
                pak.set_frame_range(frame_range[0], frame_range[1])
                pak.export_function = bfu_export_action_package.process_action_animation_export_from_package
                            
        # Set the additional data in the asset, add asset to the list and return the list.
        self.set_additional_data_in_asset(asset, data, details, search_mode)
        asset_list.append(asset)
        return asset_list

    def get_asset_additional_data(self, data: bpy.types.Object, details: Any, search_mode: AssetDataSearchMode) -> Dict[str, Any]:
        additional_data: Dict[str, Any] = {}

        scene = bpy.context.scene
        if scene:
            # Used for set animation sample rate with glTF imports
            additional_data['animation_frame_rate_denominator'] = scene.render.fps_base
            additional_data['animation_frame_rate_numerator'] = scene.render.fps
        return additional_data

# --------------------------------------------
# Register and Unregister functions
# --------------------------------------------

def register():
    my_asset_class = BFU_SkeletalAnimation()
    bfu_assets_manager.bfu_asset_manager_registred_assets.register_asset_class(my_asset_class)

def unregister():
    pass