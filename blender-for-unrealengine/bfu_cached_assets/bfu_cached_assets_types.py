# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================


import bpy
import fnmatch
import pathlib
from typing import List




class CachedAction():
    '''
    I can't use bpy.types.Scene or bpy.types.Object Property.
    "Writing to ID classes in this context is not allowed"
    So I use simple python var
    '''

    class ActionFromCache:
        # Info about actions from last cache.
        def __init__(self, action: bpy.types.Action):
            self.total_action_fcurves_len: int = len(action.fcurves)

    def __init__(self):
        self.name: str = ""
        self.is_cached: bool = False
        self.stored_actions: List[str] = []
        self.total_actions: List[CachedAction.ActionFromCache] = []
        self.total_rig_bone_len: int = 0

    def check_cache(self, obj: bpy.types.Object) -> bool:
        # Check if the cache need update
        if self.name != obj.name:
            self.is_cached = False
        if len(bpy.data.actions) != len(self.total_actions):
            self.is_cached = False
        if len(obj.data.bones) != self.total_rig_bone_len:
            self.is_cached = False
        for action_name in self.stored_actions:
            if action_name not in bpy.data.actions:
                self.is_cached = False

        return self.is_cached

    def store_actions(self, obj: bpy.types.Object, actions: List[bpy.types.Action]) -> None:
        # Update new cache
        self.name = obj.name
        action_name_list: List[str] = []
        for action in actions:
            action_name_list.append(action.name)
        self.stored_actions = action_name_list
        self.total_actions.clear()
        for action in bpy.data.actions:
            self.total_actions.append(self.ActionFromCache(action))
        self.total_rig_bone_len = len(obj.data.bones)
        self.is_cached = True
        # print("Stored action cache updated.")

    def get_stored_actions(self) -> List[bpy.types.Action]:
        actions: List[bpy.types.Action] = []
        for action_name in self.stored_actions:
            if action_name in bpy.data.actions:
                actions.append(bpy.data.actions[action_name])
        return actions

    def clear(self) -> None:
        pass