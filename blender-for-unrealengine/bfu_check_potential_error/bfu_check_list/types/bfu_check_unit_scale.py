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
from .... import bfu_utils
from ....bfu_simple_file_type_enum import BFU_FileTypeEnum
from .... import bfu_addon_prefs
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport
from ...bfu_check_types import bfu_checker


class BFU_Checker_UnitScale(bfu_checker):
    
    def __init__(self):
        super().__init__()
        self.check_name = "Unit Scale"

    def run_asset_check(self, asset: AssetToExport):
        addon_prefs = bfu_addon_prefs.get_addon_prefs()

        if bpy.context is None:
            return
        
        main_object = asset.get_primary_asset_package()

        if main_object:
            file_type = asset.original_asset_class.get_package_file_type(main_object)

            if file_type in [BFU_FileTypeEnum.FBX, BFU_FileTypeEnum.ALEMBIC]:

                # Check if the unit scale is equal to 0.01 for FBX and Alembic export.
                if addon_prefs.notifyUnitScalePotentialError:
                    if not bfu_utils.get_scene_unit_scale_is_close(0.01):
                        str_unit_scale = str(bfu_utils.get_scene_unit_scale())
                        my_po_error = self.add_potential_error()
                        my_po_error.name = bpy.context.scene.name
                        my_po_error.type = 1
                        my_po_error.text = (f"Asset '{asset.name}'(FBX) in scene '{bpy.context.scene.name}' has a Unit Scale equal to {str_unit_scale}.")
                        my_po_error.text += ('\nFor Unreal, with FBX and Alembic export a unit scale equal to 0.01 is recommended.')
                        my_po_error.text += ('\n(You can disable this potential error in the addon preferences.)')
                        my_po_error.object = main_object
                        my_po_error.correct_ref = "SetUnrealUnit"
                        my_po_error.correct_label = 'Set Unreal Unit'
            
            elif file_type in [BFU_FileTypeEnum.GLTF]:
                
                # Check if the unit scale is equal to 1.0 for GLTF export.
                if addon_prefs.notifyUnitScalePotentialError:
                    if not bfu_utils.get_scene_unit_scale_is_close(0.01):
                        str_unit_scale = str(bfu_utils.get_scene_unit_scale())
                        my_po_error = self.add_potential_error()
                        my_po_error.name = bpy.context.scene.name
                        my_po_error.type = 1
                        my_po_error.text = (f"Asset '{asset.name}'(GLTF) in scene '{bpy.context.scene.name}' has a Unit Scale equal to {str_unit_scale}.")
                        my_po_error.text += ('\nFor Unreal, with GLTF export a unit scale equal to 1.0 is recommended.')
                        my_po_error.text += ('\n(You can disable this potential error in the addon preferences.)')
                        my_po_error.object = main_object
                        my_po_error.correct_ref = "SetUnrealUnit"
                        my_po_error.correct_label = 'Set Unreal Unit'