# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
import fnmatch
from . import bfu_skeletal_mesh_config
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_unreal_utils
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType



def get_socket_in_desired_childs(obj: bpy.types.Object):
    socket_objs = []
    for obj in bfu_utils.GetExportDesiredChilds(obj):
        if fnmatch.fnmatchcase(obj.name, "SOCKET*"):
            socket_objs.append(obj)
    return socket_objs

def deselect_socket(obj: bpy.types.Object):
    # With skeletal mesh the Socket musts be not exported,
    # Because Unreal Engine will import it as bones.
    socket_objs = get_socket_in_desired_childs(obj)
    for obj in socket_objs:
        obj.select_set(False)


def is_skeletal_mesh(obj: bpy.types.Object):
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
    if asset_class:
        if asset_class.get_asset_type(obj) == AssetType.SKELETAL_MESH:
            return True
    return False

def is_not_skeletal_mesh(obj: bpy.types.Object):
    return not is_skeletal_mesh(obj)