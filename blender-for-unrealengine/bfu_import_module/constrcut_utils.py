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