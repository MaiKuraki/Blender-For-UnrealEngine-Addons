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
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport, AssetType

class BFU_Checker_BadStaticMeshExportedLikeSkeletalMesh(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "StaticMesh Exported Like SkeletalMesh"

    # Check if a mesh with an Armature modifier is incorrectly exported as Static Mesh
    def run_asset_check(self, asset: AssetToExport):
        if asset.asset_type != AssetType.STATIC_MESH:
            return
        
        for obj in self.get_objects_to_check(asset):
            for mod in obj.modifiers:
                if mod.type == "ARMATURE":  # type: ignore
                    my_po_error = self.add_potential_error()
                    my_po_error.name = obj.name
                    my_po_error.type = 1
                    my_po_error.text = (
                        f'In object "{obj.name}", the modifier "{mod.type}" '
                        f'named "{mod.name}" will not be applied when exported '
                        'with StaticMesh assets.\nNote: with armature, if you want to export '
                        'objects as skeletal mesh, you need to set only the armature as '
                        'export_recursive, not the child objects.'
                    )
                    my_po_error.object = obj
