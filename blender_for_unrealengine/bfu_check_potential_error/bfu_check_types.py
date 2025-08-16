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
from . import bfu_check_props
from typing import List
from abc import ABC
from ..bfu_cached_assets.bfu_cached_assets_blender_class import AssetToExport

class bfu_checker(ABC):

    def __init__(self):
        self.check_name: str = "My Checker"
    
    # Helpers

    def add_potential_error(self) -> bfu_check_props.BFU_OT_UnrealPotentialError:
        scene = bpy.context.scene  # type: ignore
        return scene.bfu_export_potential_errors.add()  # type: ignore

    # Prepare list of skeletal objects to check
    def get_armatures_to_check(self, asset: AssetToExport) -> List[bpy.types.Object]:
        obj_to_check: List[bpy.types.Object] = []

        for package in asset.asset_packages:
            for obj in package.objects:
                if obj.type == 'ARMATURE':  # type: ignore
                    obj_to_check.append(obj)

        return obj_to_check

    def get_meshes_to_check(self, asset: AssetToExport) -> List[bpy.types.Object]:
        obj_to_check: List[bpy.types.Object] = []

        for package in asset.asset_packages:
            for obj in package.objects:
                if obj.type == 'MESH':  # type: ignore
                    obj_to_check.append(obj)

        return obj_to_check
    
    # Prepare list of objects to check
    def get_objects_to_check(self, asset: AssetToExport) -> List[bpy.types.Object]:
        obj_to_check: List[bpy.types.Object] = []

        for package in asset.asset_packages:
            for obj in package.objects:
                obj_to_check.append(obj)

        return obj_to_check

    # Prepare list of collections to check
    def get_collections_to_check(self, asset: AssetToExport) -> List[bpy.types.Collection]:
        collection_to_check: List[bpy.types.Collection] = []

        for package in asset.asset_packages:
            for col in package.collection:
                collection_to_check.append(col)

        return collection_to_check

    # Prepare list of actions to check
    def get_actions_to_check(self, asset: AssetToExport) -> List[bpy.types.Action]:
        action_to_check: List[bpy.types.Action] = []

        for package in asset.asset_packages:
            if package.action:
                action_to_check.append(package.action)

        return action_to_check

    # Check Methods

    def run_scene_check(self, scene: bpy.types.Scene):
        pass

    def run_asset_check(self, asset: AssetToExport):
        pass


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore