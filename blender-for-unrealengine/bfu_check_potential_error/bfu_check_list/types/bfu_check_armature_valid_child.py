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
from .... import bfu_skeletal_mesh

class BFU_Checker_ArmatureValidChild(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature Valid Child"

    # Prepare the list of skeletal armatures to check
    def get_armatures_to_check(self) -> List[bpy.types.Object]:
        final_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.GetfinalAssetCache()
        final_asset_list_to_export = final_asset_cache.get_final_asset_list()

        obj_to_check = []
        for asset in final_asset_list_to_export:
            if asset.obj in bfu_base_object.bfu_export_type.get_all_export_recursive_objects():
                if asset.obj not in obj_to_check:
                    obj_to_check.append(asset.obj)
                for child in bfu_utils.GetExportDesiredChilds(asset.obj):
                    if child not in obj_to_check:
                        obj_to_check.append(child)

        return [obj for obj in obj_to_check if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)]

    # Check that the skeleton has at least one valid mesh child to export
    def run_check(self):
        for obj in self.get_armatures_to_check():
            export_as_proxy = bfu_utils.GetExportAsProxy(obj)
            childs = bfu_utils.GetExportDesiredChilds(obj)
            valid_child = sum(1 for child in childs if child.type == "MESH")

            if export_as_proxy and bfu_utils.GetExportProxyChild(obj) is not None:
                valid_child += 1

            if valid_child < 1:
                my_po_error = self.add_potential_error()
                my_po_error.name = obj.name
                my_po_error.type = 2
                my_po_error.text = (
                    f'Object "{obj.name}" is an Armature and does not have '
                    'any valid children.'
                )
                my_po_error.object = obj
