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

import bpy
from ...bfu_check_types import bfu_checker
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport

class BFU_Checker_ArmatureNoDeformBone(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature No Deform Bone"

    # Check that the skeleton has at least one deform bone
    def run_asset_check(self, asset: AssetToExport):
        if not asset.asset_type.is_skeletal():
            return

        for obj in self.get_armatures_to_check(asset):
            if obj.bfu_export_deform_only:  # type: ignore
                if not isinstance(obj.data, bpy.types.Armature):
                    continue
                has_deform_bone = any(bone.use_deform for bone in obj.data.bones)
                if not has_deform_bone:
                    my_po_error = self.add_potential_error()
                    my_po_error.name = obj.name
                    my_po_error.type = 2
                    my_po_error.text = (
                        f'Object "{obj.name}" does not have any deform bones. '
                        'Unreal will import it as a StaticMesh.'
                    )
                    my_po_error.object = obj
