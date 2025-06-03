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
import fnmatch
from . import bfu_skeletal_mesh_config
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_unreal_utils
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType

def SelectArmatureParentAndDesiredChilds(active: bpy.types.Object, inclide_meshs=True, inclide_sockets=True):
    # Selects only auto desired child objects that must be exported with armature object
    if active.type != "ARMATURE":
        print(f"The object {active.name} is not an armature!")
        return

    new_select_list = []
    bpy.ops.object.select_all(action='DESELECT')
    for select_obj in bfu_utils.GetExportDesiredChilds(active):
        if inclide_meshs == True:
            new_select_list.append(select_obj)
        elif select_obj.type != "MESH":
            new_select_list.append(select_obj)

        # @TODO -> inclide_sockets

    # Select active at end to move a list end
    new_select_list.append(active)

    # Select proxy at end to move a list end
    if bfu_utils.GetExportAsProxy(active):
        proxy_child = bfu_utils.GetExportProxyChild(active)
        if proxy_child is not None:
            new_select_list.append(active)

    return bbpl.utils.select_specific_object_list(active, new_select_list)


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