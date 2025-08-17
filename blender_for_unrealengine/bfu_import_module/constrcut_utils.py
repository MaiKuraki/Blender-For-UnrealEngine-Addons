# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

from typing import Tuple
import unreal
from . import constrcut_config

def get_unreal_version() -> Tuple[int, int, int]:
    """Returns the Unreal Engine version as a tuple of (major, minor, patch)."""
    version_info = unreal.SystemLibrary.get_engine_version().split('-')[0]
    major, minor, patch = map(int, version_info.split('.'))
    return (major, minor, patch)

def include_interchange_functions() -> bool:
    # Interchange import is avaliable since 5.1,

    # If True: Set values inside unreal.InterchangeGenericAssetsPipeline (unreal.InterchangeGenericCommonMeshesProperties or ...)
    # If False: Set values inside unreal.FbxStaticMeshImportData or ...

    if constrcut_config.force_use_interchange == "Interchange":
        return True

    elif constrcut_config.force_use_interchange == "FBX":
        return False

    else:
        return get_unreal_version() >= constrcut_config.interchange_minimal_support