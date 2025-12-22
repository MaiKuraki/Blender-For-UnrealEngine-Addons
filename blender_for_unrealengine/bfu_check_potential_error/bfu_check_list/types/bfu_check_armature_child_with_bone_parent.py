# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

from ...bfu_check_types import bfu_checker
from .... import bfu_utils
from ....bfu_assets_manager.bfu_asset_manager_type import AssetToExport

class BFU_Checker_ArmatureChildWithBoneParent(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Armature Child With Bone Parent"

    # Check if a mesh child is parented to a bone, which will cause import issues
    def run_asset_check(self, asset: AssetToExport):
        if not asset.asset_type.is_skeletal():
            return
        for obj in self.get_armatures_to_check(asset):
            childs = bfu_utils.get_export_desired_childs(obj)
            for child in childs:
                if child.type == "MESH" and child.parent_type == 'BONE':  # type: ignore
                    my_po_error = self.add_potential_error()
                    my_po_error.name = child.name
                    my_po_error.type = 2
                    my_po_error.text = (
                        f'Object "{child.name}" uses Parent Bone to parent. '
                        '\nIf you use Parent Bone to parent your mesh to your armature, the import will fail.'
                    )
                    my_po_error.object = child
                    my_po_error.docs_octicon = 'armature-child-with-bone-parent'
