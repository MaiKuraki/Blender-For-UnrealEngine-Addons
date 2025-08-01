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

import fnmatch
from typing import List
import bpy
from . import bfu_anim_action_props
from .bfu_anim_action_props import BFU_OT_ObjExportAction

def get_action_is_in_action_asset_list(obj: bpy.types.Object, action: bpy.types.Action) -> bool:
    action_asset_list = bfu_anim_action_props.get_object_action_asset_list(obj)  # CollectionProperty
    action_asset_list: List[BFU_OT_ObjExportAction]
    for target_action in action_asset_list:
        if target_action.use:
            if target_action.name == action.name:
                return True
    return False

def get_action_use_prefix(obj: bpy.types.Object, action: bpy.types.Action) -> bool:
    if fnmatch.fnmatchcase(action.name, bfu_anim_action_props.get_object_prefix_name_to_export(obj) + "*"):
        return True
    return False

def get_action_is_current(obj: bpy.types.Object, action: bpy.types.Action) -> bool:
    if obj.animation_data and obj.animation_data.action:
        if obj.animation_data.action == action:
            return True
    return False