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
from ... import bfu_check_utils
from .... import bfu_utils
from .... import bfu_cached_assets
from .... import bfu_skeletal_mesh


class BFU_Checker_VertexGroupWeight(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Vertex Group Weight"

    # Prepare the list of objects to check
    def get_objects_to_check(self) -> List[bpy.types.Object]:
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
        return obj_to_check

    def get_skeleton_meshs(self, obj):
        meshes = []
        if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj):
            childs = bfu_utils.GetExportDesiredChilds(obj)
            for child in childs:
                if child.type == "MESH":
                    meshes.append(child)
        return meshes
    
    def contains_armature_modifier(self, obj):
        for mod in obj.modifiers:
            if mod.type == "ARMATURE":
                return True
        return False

    # Check that all vertices have a weight
    def run_check(self):
        for obj in self.get_objects_to_check():
            meshes = self.get_skeleton_meshs(obj)
            for mesh in meshes:
                if mesh.type == "MESH" and self.contains_armature_modifier(mesh):
                    # Get vertices with zero weight
                    vertices_with_zero_weight = bfu_check_utils.get_vertices_with_zero_weight(obj, mesh)
                    if vertices_with_zero_weight:
                        my_po_error = self.add_potential_error()
                        my_po_error.name = mesh.name
                        my_po_error.type = 1
                        my_po_error.text = (
                            f'Object "{mesh.name}" contains {len(vertices_with_zero_weight)} '
                            'vertices with zero cumulative valid weight.'
                        )
                        my_po_error.text += (
                            '\nNote: Vertex groups must have a bone with the same name to be valid.'
                        )
                        my_po_error.object = mesh
                        my_po_error.selectVertexButton = True
                        my_po_error.selectOption = "VertexWithZeroWeight"
