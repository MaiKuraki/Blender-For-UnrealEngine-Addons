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
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_camera
from .. import bfu_alembic_animation
from .. import bfu_groom
from .. import bfu_spline
from .. import bfu_skeletal_mesh
from .. import bfu_static_mesh
from .. import bfu_assets_manager
from .. import bfu_modular_skeletal_mesh


class AssetToExport:
    def __init__(self, obj: bpy.types.Object, action, asset_type):
        # Base info
        self.name = obj.name
        self.asset_type = asset_type
        self.dirpath = ""
        self.import_dirpath = ""

        # Mesh Info
        self.obj = obj
        self.obj_list = []

        # Action Info
        self.action = action

    def set_dirpath(self, new_dirpath):
        self.dirpath = new_dirpath

    def set_import_dirpath(self, new_import_dirpath):
        self.import_dirpath = new_import_dirpath

    def add_obj(self, new_obj):
        self.obj_list.append(new_obj)


class CachedAction():

    '''
    I can't use bpy.types.Scene or bpy.types.Object Property.
    "Writing to ID classes in this context is not allowed"
    So I use simple python var
    '''

    class ActionFromCache():
        # Info about actions from last cache.
        def __init__(self, action):
            self.total_action_fcurves_len = len(action.fcurves)

    def __init__(self):
        self.name = ""
        self.is_cached = False
        self.stored_actions = []
        self.total_actions = []
        self.total_rig_bone_len = 0

    def CheckCache(self, obj):
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

    def StoreActions(self, obj, actions):
        # Update new cache
        self.name = obj.name
        action_name_list = []
        for action in actions:
            action_name_list.append(action.name)
        self.stored_actions = action_name_list
        self.total_actions.clear()
        for action in bpy.data.actions:
            self.total_actions.append(self.ActionFromCache(action))
        self.total_rig_bone_len = len(obj.data.bones)
        self.is_cached = True
        # print("Stored action cache updated.")

    def GetStoredActions(self):
        actions = []
        for action_name in self.stored_actions:
            if action_name in bpy.data.actions:
                actions.append(bpy.data.actions[action_name])
        return actions

    def Clear(self):
        pass