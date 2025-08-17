# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType

def get_enum_cameras_list():
    camera_types = [
        ("REGULAR", "Regular", "Regular camera, for standard gameplay views."),
        ("CINEMATIC", "Cinematic", "The Cine Camera Actor is a specialized Camera Actor with additional settings that replicate real-world film camera behavior. You can use the Filmback, Lens, and Focus settings to create realistic scenes, while adhering to industry standards."),
        ("ARCHVIS", "ArchVis", "Support for ArchVis Tools Cameras."),
        ("CUSTOM", "Custom", "If you use an custom camera actor."),
    ]
    return camera_types



def get_enum_cameras_default():
    return "CINEMATIC"

def is_camera(obj: bpy.types.Object) -> bool:
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
    if asset_class:
        if asset_class.get_asset_type(obj) == AssetType.CAMERA:
            return True
    return False