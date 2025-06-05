# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

from ...bfu_check_types import bfu_checker
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport

class BFU_Checker_ArmatureScale(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature Scale"

    # Check if the armature uses the same value on all scale axes
    def run_asset_check(self, asset: AssetToExport):
        if not asset.asset_type.is_skeletal():
            return

        obj_to_check = self.get_armatures_to_check(asset)
        for obj in obj_to_check:
            if obj.scale.z != obj.scale.y or obj.scale.z != obj.scale.x:
                my_po_error = self.add_potential_error()
                my_po_error.name = obj.name
                my_po_error.type = 2
                my_po_error.text = (
                    f'In object "{obj.name}", the scale values are not consistent across all axes.'
                )
                my_po_error.text += (
                    f'\nScale x: {obj.scale.x}, y: {obj.scale.y}, z: {obj.scale.z}'
                )
                my_po_error.object = obj
