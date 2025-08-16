# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

import bpy
from typing import List
from ....bfu_simple_file_type_enum import BFU_FileTypeEnum
from ....bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport
from ...bfu_check_types import bfu_checker


class BFU_Checker_UnitScale(bfu_checker):
    
    def __init__(self):
        super().__init__()
        self.check_name = "Hierarchy modification risk"

    @staticmethod
    def get_non_deform_bones_with_deform_children(armature: bpy.types.Object) -> List[str]:
        found_bones: List[str] = []
        if isinstance(armature.data, bpy.types.Armature):
            for bone in armature.data.bones:
                if not bone.use_deform:
                    for child in bone.children:
                        if child.use_deform:
                            found_bones.append(bone.name)
        return found_bones

    @staticmethod
    def get_issue_message(asset: AssetToExport, scene: bpy.types.Scene, found_bones: List[str]) -> str:
        text = f"In asset '{asset.name}' (GLTF) in scene '{scene.name}' some bones will be skipped because they are not deformable.\n"
        text += "This happens even if they have deformable children with glTF exports. It may break the bone hierarchy and cause issues in Unreal.\n"
        text += "Bones affected: " + ', '.join(found_bones) + "\n"
        text += "Set these bones as deformable, or disable 'Deform Only'.\n"
        return text

    def run_asset_check(self, asset: AssetToExport):
        scene = bpy.context.scene
        if scene is None:
            return
        
        main_object = asset.get_primary_asset_package()

        if main_object:
            file_type = asset.original_asset_class.get_package_file_type(main_object)

            if file_type in [BFU_FileTypeEnum.GLTF]:
                if main_object.bfu_export_deform_only == True:
            
                # Check if the unit scale is equal to 1.0 for GLTF export.
                    found_bones = self.get_non_deform_bones_with_deform_children(main_object)
                    if len(found_bones) > 0:
                        my_po_error = self.add_potential_error()
                        my_po_error.name = scene.name
                        my_po_error.type = 1
                        my_po_error.text = self.get_issue_message(asset, scene, found_bones)
                        my_po_error.object = main_object