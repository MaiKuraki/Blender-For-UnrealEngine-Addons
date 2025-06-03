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

class BFU_Checker_UVMaps(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "UV Maps"

    # Prepare the list of mesh objects without collision to check
    def get_mesh_without_collision(self) -> List[bpy.types.Object]:
        final_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.GetfinalAssetCache()
        final_asset_list_to_export = final_asset_cache.get_final_asset_list()

        obj_to_check = []
        for asset in final_asset_list_to_export:
            if asset.obj in bfu_utils.get_all_objects_by_export_type("export_recursive"):
                if asset.obj not in obj_to_check:
                    obj_to_check.append(asset.obj)
                for child in bfu_utils.GetExportDesiredChilds(asset.obj):
                    if child not in obj_to_check:
                        obj_to_check.append(child)

        mesh_type_to_check = [obj for obj in obj_to_check if obj.type == 'MESH']
        return [obj for obj in mesh_type_to_check if not bfu_utils.CheckIsCollision(obj)]

    # Check that the objects have at least one valid UV map
    def run_check(self):
        mesh_type_without_col = self.get_mesh_without_collision()
        for obj in mesh_type_without_col:
            if len(obj.data.uv_layers) < 1:
                my_po_error = self.add_potential_error()
                my_po_error.name = obj.name
                my_po_error.type = 1
                my_po_error.text = f'Object "{obj.name}" does not have any UV Layer.'
                my_po_error.object = obj
                my_po_error.correctRef = "CreateUV"
                my_po_error.correctlabel = 'Create Smart UV Project'
