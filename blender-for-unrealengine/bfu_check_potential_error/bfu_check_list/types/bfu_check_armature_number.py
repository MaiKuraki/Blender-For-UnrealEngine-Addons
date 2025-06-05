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
from .... import bfu_base_object

class BFU_Checker_ArmatureNumber(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature Number"

    # Prepare list of objects to check
    def get_objects_to_check(self) -> List[bpy.types.Object]:
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
        return obj_to_check

    def get_skeleton_meshs(self, obj):
        meshes = []
        if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj):
            childs = bfu_utils.GetExportDesiredChilds(obj)
            for child in childs:
                if child.type == "MESH":
                    meshes.append(child)
        return meshes

    # Check if the number of ARMATURE modifiers or constraints is exactly 1
    def run_check(self):
        obj_to_check = self.get_objects_to_check()
        for obj in obj_to_check:
            meshes = self.get_skeleton_meshs(obj)
            for mesh in meshes:
                # Count the number of ARMATURE modifiers and constraints
                armature_modifiers = sum(1 for mod in mesh.modifiers if mod.type == "ARMATURE")
                armature_constraints = sum(1 for const in mesh.constraints if const.type == "ARMATURE")

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
