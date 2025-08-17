# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


from ...bfu_check_types import bfu_checker
from .... import bfu_utils
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport

class BFU_Checker_ArmatureMultipleRoots(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature Multiple Roots"


    # Check if the skeleton has multiple root bones
    def run_asset_check(self, asset: AssetToExport):
        if not asset.asset_type.is_skeletal():
            return

        for obj in self.get_armatures_to_check(asset):
            root_bones = bfu_utils.get_armature_root_bones(obj)

            root_bones_str = ""
            for bone in root_bones:
                if bone.use_deform:
                    root_bones_str += bone.name + "(def), "
                else:
                    root_bones_str += bone.name + "(def child(s)), "

            if len(root_bones) > 1:
                my_po_error = self.add_potential_error()
                my_po_error.name = obj.name
                my_po_error.type = 1
                my_po_error.text = (
                    f'Object "{obj.name}" has multiple root bones. Unreal only supports a single root bone.'
                )
                my_po_error.text += '\n' + f' {len(root_bones)} root bone(s) found: {root_bones_str}'
                my_po_error.text += '\n' + 'A custom root bone will be added at export.'
                my_po_error.object = obj
