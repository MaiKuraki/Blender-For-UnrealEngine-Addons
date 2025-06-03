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

class BFU_Checker_ZeroScaleKeyframe(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Zero Scale Keyframe"

    # Préparer les objets à tester
    def get_skeletal_objects(self) -> List[bpy.types.Object]:
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

        return [obj for obj in obj_to_check if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)]

    # Check that animations do not use an invalid scale value
    def run_check(self):
        for obj in self.get_skeletal_objects():
            animation_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.GetAnimationAssetCache(obj)
            animations_to_export = animation_asset_cache.GetAnimationAssetList()

            for action in animations_to_export:
                for fcurve in action.fcurves:
                    # Detect scale curves
                    if fcurve.data_path.split(".")[-1] == "scale":
                        for key in fcurve.keyframe_points:
                            x_curve, y_curve = key.co
                            if y_curve == 0:
                                bone_name = fcurve.data_path.split('"')[1]
                                my_po_error = self.add_potential_error()
                                my_po_error.type = 2
                                my_po_error.text = (
                                    f'In action "{action.name}" at frame {x_curve}, '
                                    f'the bone named "{bone_name}" has a zero value in the scale '
                                    'transform. This is invalid in Unreal.'
                                )
