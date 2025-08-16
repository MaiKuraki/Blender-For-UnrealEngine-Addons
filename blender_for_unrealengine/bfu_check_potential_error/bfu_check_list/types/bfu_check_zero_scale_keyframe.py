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

class BFU_Checker_ZeroScaleKeyframe(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Zero Scale Keyframe"

    # Check that animations do not use an invalid scale value
    def run_asset_check(self, asset: AssetToExport):
        if asset.asset_type not in [AssetType.ANIM_ACTION, AssetType.ANIM_POSE, AssetType.ANIM_NLA]:
            # This check is only relevant for skeletal assets with animations
            return

        for packages in asset.asset_packages:
            action = packages.action
            action_name = action.name  # type: ignore
            for obj in self.get_armatures_to_check(asset):
                for fcurve in action.fcurves:  # type: ignore
                    # Detect scale curves
                    if fcurve.data_path.split(".")[-1] == "scale":
                        for key in fcurve.keyframe_points:
                            x_curve, y_curve = key.co
                            if y_curve == 0:
                                bone_name = fcurve.data_path.split('"')[1]
                                my_po_error = self.add_potential_error()
                                my_po_error.type = 2
                                my_po_error.text = (
                                    f'In action "{action_name}" used with object "{obj.name}" at frame {x_curve}, '
                                    f'the bone named "{bone_name}" has a zero value in the scale '
                                    'transform. This is invalid in Unreal.'
                                )
