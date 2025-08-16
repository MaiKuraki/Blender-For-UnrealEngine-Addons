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


from ...bfu_check_types import bfu_checker
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport

class BFU_Checker_ObjType(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Object Type"

        self.non_recommended_types = {"SURFACE", "META", "FONT"}

    def run_asset_check(self, asset: AssetToExport):
        for package in asset.asset_packages:
            for obj in package.objects:
                obj_type = obj.type  # type: ignore
                if obj_type in self.non_recommended_types:
                    my_po_error = self.add_potential_error()
                    my_po_error.name = obj.name
                    my_po_error.type = 1
                    my_po_error.text = (
                        f'Object "{obj.name}" is a {obj_type}. The object of the type '
                        'SURFACE, META, and FONT is not recommended.'
                    )
                    my_po_error.object = obj
                    my_po_error.correct_ref = "ConvertToMesh"
                    my_po_error.correct_label = 'Convert to mesh'
