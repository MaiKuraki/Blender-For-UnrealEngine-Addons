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
import bpy
from typing import List, Tuple, Set, Dict
from .. import bfu_debug_settings
from .. import bfu_basics
from . import bfu_anim_action_props
from .bfu_anim_action_props import BFU_AnimActionExportEnum


def precompute_action_bones() -> Dict[bpy.types.Action, Set[str]]:
    """Retourne un dict {Action: set(noms de bones dans l'action)}"""
    action_bones_map: Dict[bpy.types.Action, Set[str]] = {}
    for action in bpy.data.actions:
        bones_in_action: Set[str] = set()
        for fcurve in action.fcurves:
            path = fcurve.data_path
            if path.startswith('pose.bones["'):
                bone_name = path.split('"')[1]
                bones_in_action.add(bone_name)
        action_bones_map[action] = bones_in_action
    return action_bones_map

def find_compatible_actions(armature: bpy.types.Armature, action_bones_map: Dict[bpy.types.Action, Set[str]]) -> List[bpy.types.Action]:
    """Retourne la liste des actions compatibles avec l'armature"""        

    arm_bones: Set[str] = {b.name for b in armature.bones}
    compatible = [
        action
        for action, bones in action_bones_map.items()
        if bones & arm_bones  # au moins un bone en commun
    ]
    return compatible

def optimizated_asset_search(objects: List[bpy.types.Object]) -> List[Tuple[bpy.types.Object, bpy.types.Action]]:
    events = bfu_debug_settings.root_events
    armature_actions_map: List[Tuple[bpy.types.Object, bpy.types.Action]] = []

    for obj in objects:
        if isinstance(obj.data, bpy.types.Armature):
            action_export_enum = bfu_anim_action_props.get_object_anim_action_export_enum(obj)

            # Export Auto
            if action_export_enum == BFU_AnimActionExportEnum.EXPORT_AUTO:
                events.add_sub_event(f'Export Auto "{obj.name}"')
                obj_bone_names: Set[str] = {b.name for b in obj.data.bones}
                events.stop_last_and_start_new_event("loop action")
                for action in bpy.data.actions:
                    if not action.library:
                        if bfu_basics.get_if_action_can_associate_str_set(action, obj_bone_names):
                            armature_actions_map.append((obj, action))
                events.stop_last_event()

            # Export Specific List
            elif action_export_enum == BFU_AnimActionExportEnum.EXPORT_SPECIFIC_LIST:
                events.add_sub_event(f'Export Specific List "{obj.name}"')
                for target_action in bfu_anim_action_props.get_object_action_asset_list(obj):
                    if target_action.use:
                        # No need to check if not action.library: because alredsy checked in get_object_action_asset_list
                        if target_action.name in bpy.data.actions:
                            armature_actions_map.append((obj, bpy.data.actions[target_action.name]))
                events.stop_last_event()

            # Export Specific Prefix
            elif action_export_enum == BFU_AnimActionExportEnum.EXPORT_SPECIFIC_PREFIX:
                events.add_sub_event(f'Export Specific Prefix "{obj.name}"')
                for action in bpy.data.actions:
                    if get_action_use_prefix(obj, action):
                        armature_actions_map.append((obj, action))
                events.stop_last_event()

            # Export Current
            elif action_export_enum == BFU_AnimActionExportEnum.EXPORT_CURRENT:
                events.add_sub_event(f'Export Current "{obj.name}"')
                if obj.animation_data and obj.animation_data.action:
                        armature_actions_map.append((obj, obj.animation_data.action))
                events.stop_last_event()

            # Custom use
            else:
                print(f"Unknown action export enum: {action_export_enum} for object {obj.name}!")
  
    return armature_actions_map


def get_action_is_in_action_asset_list(obj: bpy.types.Object, action: bpy.types.Action) -> bool:
    events = bfu_debug_settings.root_events
    events.add_sub_event("Get bfu list")
    action_asset_list = bfu_anim_action_props.get_object_action_asset_list(obj)  # CollectionProperty<BFU_OT_ObjExportAction>
    events.stop_last_and_start_new_event("Check Action In Asset List")
    for target_action in action_asset_list:
        if target_action.use:
            if target_action.name == action.name:
                events.stop_last_event()
                return True
    events.stop_last_event()
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