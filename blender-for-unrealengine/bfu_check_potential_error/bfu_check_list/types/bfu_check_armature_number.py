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

class BFU_Checker_ArmatureNumber(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature Number"


    # Check if the number of ARMATURE modifiers or constraints is exactly 1
    def run_asset_check(self, asset: AssetToExport):
        if not asset.asset_type.is_skeletal():
            return

        for mesh in self.get_meshes_to_check(asset):
            # Count the number of ARMATURE modifiers and constraints
            armature_modifiers = sum(1 for mod in mesh.modifiers if mod.type == "ARMATURE")  # type: ignore
            armature_constraints = sum(1 for const in mesh.constraints if const.type == "ARMATURE")  # type: ignore

            # Check if the total number of ARMATURE modifiers and constraints is greater than 1
            if armature_modifiers + armature_constraints > 1:
                my_po_error = self.add_potential_error()
                my_po_error.name = mesh.name
                my_po_error.type = 2
                my_po_error.text = (
                    f'In object "{mesh.name}", {armature_modifiers} Armature modifier(s) and '
                    f'{armature_constraints} Armature constraint(s) were found. '
                    'Please use only one Armature modifier or one Armature constraint.'
                )
                my_po_error.object = mesh

            # Check if no ARMATURE modifiers or constraints are found
            if armature_modifiers + armature_constraints == 0:
                my_po_error = self.add_potential_error()
                my_po_error.name = mesh.name
                my_po_error.type = 2
                my_po_error.text = (
                    f'In object "{mesh.name}", no Armature modifiers or constraints were found. '
                    'Please use one Armature modifier or one Armature constraint.'
                )
                my_po_error.object = mesh
