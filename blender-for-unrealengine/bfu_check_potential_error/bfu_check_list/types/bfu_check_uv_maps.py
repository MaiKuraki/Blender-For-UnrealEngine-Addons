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
from .... import bfu_utils
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport

class BFU_Checker_UVMaps(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "UV Maps"

    # Check that the objects have at least one valid UV map
    def run_asset_check(self, asset: AssetToExport):
        for obj in self.get_meshes_to_check(asset):
            if obj.data:
                if not bfu_utils.check_is_collision(obj):
                    if len(obj.data.uv_layers) < 1:  # type: ignore
                        my_po_error = self.add_potential_error()
                        my_po_error.name = obj.name
                        my_po_error.type = 1
                        my_po_error.text = f'Object "{obj.name}" does not have any UV Layer.'
                        my_po_error.object = obj
                        my_po_error.correct_ref = "CreateUV"
                        my_po_error.correct_label = 'Create Smart UV Project'
