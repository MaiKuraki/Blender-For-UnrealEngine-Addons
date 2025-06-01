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
from typing import List
from ...bfu_check_types import bfu_checker
from .... import bfu_utils
from .... import bfu_cached_assets

class BFU_Checker_BadStaticMeshExportedLikeSkeletalMesh(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "StaticMesh Exported Like SkeletalMesh"

    # Prepare the list of mesh objects to check
    def get_mesh_to_check(self) -> List[bpy.types.Object]:
        final_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.GetfinalAssetCache()
        final_asset_list_to_export = final_asset_cache.GetFinalAssetList()

        obj_to_check = []
        for asset in final_asset_list_to_export:
            if asset.obj in bfu_utils.GetAllobjectsByExportType("export_recursive"):
                if asset.obj not in obj_to_check:
                    obj_to_check.append(asset.obj)
                for child in bfu_utils.GetExportDesiredChilds(asset.obj):
                    if child not in obj_to_check:
                        obj_to_check.append(child)

        return [obj for obj in obj_to_check if obj.type == 'MESH']

    # Check if a mesh with an Armature modifier is incorrectly exported as Static Mesh
    def run_check(self):
        mesh_type_to_check = self.get_mesh_to_check()
        for obj in mesh_type_to_check:
            for modif in obj.modifiers:
                if modif.type == "ARMATURE" and obj.bfu_export_type == "export_recursive":
                    my_po_error = self.add_potential_error()
                    my_po_error.name = obj.name
                    my_po_error.type = 1
                    my_po_error.text = (
                        f'In object "{obj.name}", the modifier "{modif.type}" '
                        f'named "{modif.name}" will not be applied when exported '
                        'with StaticMesh assets.\nNote: with armature, if you want to export '
                        'objects as skeletal mesh, you need to set only the armature as '
                        'export_recursive, not the child objects.'
                    )
                    my_po_error.object = obj
