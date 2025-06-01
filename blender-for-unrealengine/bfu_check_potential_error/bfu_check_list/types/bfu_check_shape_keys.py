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

class BFU_Checker_ShapeKeys(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Shape Keys"

        # Destructive modifiers that can break shape keys at export
        self.destructive_modifiers = {
            "BOOLEAN",       # ...
            "BUILD",         # ...
            "DECIMATE",      # ...
            "EDGE_SPLIT",    # ...
            "MASK",          # ...
            "MIRROR",        # ...
            "REMESH",        # ...
            "SCREW",         # ...
            "SKIN",          # ...
            "SOLIDIFY",      # ...
            "SUBSURF",       # ...
            "TRIANGULATE",   # ...
            "WELD",          # ...
            "WIREFRAME",     # ...
        }


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

    # Check shape keys validity and safety for Unreal export
    def run_check(self):
        mesh_type_to_check = self.get_mesh_to_check()
        for obj in mesh_type_to_check:
            shape_keys = obj.data.shape_keys
            if shape_keys is not None and len(shape_keys.key_blocks) > 0:
                # Check that no modifiers is destructive for the key shapes
                for modif in obj.modifiers:
                    if modif.type in self.destructive_modifiers:
                        my_po_error = self.add_potential_error()
                        my_po_error.name = obj.name
                        my_po_error.type = 2
                        my_po_error.object = obj
                        my_po_error.itemName = modif.name
                        my_po_error.text = (
                            f'In object "{obj.name}", the modifier "{modif.type}" '
                            f'named "{modif.name}" can destroy shape keys. '
                            'Please use only the Armature modifier with shape keys.'
                        )
                        my_po_error.correctRef = "RemoveModifier"
                        my_po_error.correctlabel = 'Remove modifier'

                # Check shape key ranges for Unreal Engine compatibility
                unreal_engine_shape_key_max = 5
                unreal_engine_shape_key_min = -5
                for key in shape_keys.key_blocks:
                    # Min check
                    if key.slider_min < unreal_engine_shape_key_min:
                        my_po_error = self.add_potential_error()
                        my_po_error.name = obj.name
                        my_po_error.type = 1
                        my_po_error.object = obj
                        my_po_error.itemName = key.name
                        my_po_error.text = (
                            f'In object "{obj.name}", the shape key "{key.name}" '
                            f'is out of bounds for Unreal. The minimum range must not be less than {unreal_engine_shape_key_min}.'
                        )
                        my_po_error.correctRef = "SetKeyRangeMin"
                        my_po_error.correctlabel = f'Set min range to {unreal_engine_shape_key_min}'

                    # Max check
                    if key.slider_max > unreal_engine_shape_key_max:
                        my_po_error = self.add_potential_error()
                        my_po_error.name = obj.name
                        my_po_error.type = 1
                        my_po_error.object = obj
                        my_po_error.itemName = key.name
                        my_po_error.text = (
                            f'In object "{obj.name}", the shape key "{key.name}" '
                            f'is out of bounds for Unreal. The maximum range must not exceed {unreal_engine_shape_key_max}.'
                        )
                        my_po_error.correctRef = "SetKeyRangeMax"
                        my_po_error.correctlabel = f'Set max range to {unreal_engine_shape_key_max}'
