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

class BFU_Checker_ArmatureValidChild(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature Valid Child"


    # Check that the skeleton has at least one valid mesh child to export
    def run_asset_check(self, asset: AssetToExport):
        if not asset.asset_type.is_skeletal():
            return

        if len(self.get_meshes_to_check(asset)) == 0:
            main_object = asset.asset_packages[0].objects[0]
            my_po_error = self.add_potential_error()
            my_po_error.name = asset.name
            my_po_error.type = 2
            my_po_error.text = (
                f'In asset named "{asset.name}", the Armature "{main_object.name}" does not have '
                'any valid children.'
            )
            my_po_error.object = main_object
