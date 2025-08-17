# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
from typing import Dict, Any, TYPE_CHECKING
from .. bfu_assets_manager.bfu_asset_manager_type import AssetType

def get_nanite_asset_data(obj: bpy.types.Object, asset_type: AssetType) -> Dict[str, Any]:
    asset_data: Dict[str, Any] = {}
    return asset_data

def get_nanite_asset_additional_data(obj: bpy.types.Object, asset_type: AssetType) -> Dict[str, Any]:
    asset_data: Dict[str, Any] = {}
    if obj:

        if TYPE_CHECKING:
            class FakeObject(bpy.types.Object):
                bfu_build_nanite_mode: str = "build_nanite_auto"
            obj = FakeObject()

        if asset_type in [AssetType.STATIC_MESH, AssetType.SKELETAL_MESH]:
            if obj.bfu_build_nanite_mode == "build_nanite_true":
                asset_data["build_nanite"] = True
            elif obj.bfu_build_nanite_mode == "build_nanite_false":
                asset_data["build_nanite"] = False
            # Keep empty for auto
    return asset_data