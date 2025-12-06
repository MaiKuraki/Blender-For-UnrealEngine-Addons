# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import fnmatch
import bpy
from bpy_extras import anim_utils
from typing import List, Tuple, Set, Dict, Optional
from .. import bfu_debug_settings
from .. import bfu_export_filter
from .. import bfu_anim_nla
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

def support_action_export(scene: bpy.types.Scene) -> bool:
    return bfu_export_filter.bfu_export_filter_props.scene_use_animation_export(scene)

def object_support_action_export(obj: bpy.types.Object) -> bool:
    if obj.bfu_export_as_lod_mesh:  # type: ignore[attr-defined]
        return False
    if bfu_anim_nla.bfu_anim_nla_props.get_object_anim_nla_use(obj):
        return False
    if obj.bfu_export_skeletal_mesh_as_static_mesh:  # type: ignore[attr-defined]
        return False
    return True

def get_can_associate_fcurve_list_with_armature(obj: bpy.types.Object, fcurves: List[bpy.types.FCurve]) -> bool:
    # Check if an list of fcurves can be associated with an armature object

    if not isinstance(obj.data, bpy.types.Armature):
        return False

    for fcurve in fcurves:
        s = fcurve.data_path
        start = s.find('["')
        end = s.rfind('"]')
        if start > 0 and end > 0:
            substring = s[start+2:end]
            if substring in obj.data.bones:
                return True
    return False

def optimizated_asset_search(scene: bpy.types.Scene, objects: List[bpy.types.Object]) -> List[Tuple[bpy.types.Object, bpy.types.Action]]:
    if not support_action_export(scene):
        return []

    events = bfu_debug_settings.root_events
    armature_actions_map: List[Tuple[bpy.types.Object, bpy.types.Action]] = []

    for obj in objects:
        if not object_support_action_export(obj):
            continue
        if isinstance(obj.data, bpy.types.Armature):
            action_export_enum = bfu_anim_action_props.get_object_anim_action_export_enum(obj)

            # Export Auto
            if action_export_enum.value == BFU_AnimActionExportEnum.EXPORT_AUTO.value:
                events.add_sub_event(f'Export Auto "{obj.name}" Prepare')

                if bpy.app.version >= (4, 4, 0):
                    # Found compatible actions using action slot and amature bones
                    if obj.animation_data:
                        last_slot_identifier: str = obj.animation_data.last_slot_identifier
                        events.stop_last_and_start_new_event(f'Export Auto "{obj.name}" Loop actions')
                        for action in bpy.data.actions:
                            if not action.library:
                                if last_slot_identifier in action.slots:
                                    slot: bpy.types.ActionSlot = action.slots[last_slot_identifier]
                                    action_channel_bag: Optional[bpy.types.ActionChannelbag] = anim_utils.action_get_channelbag_for_slot(action, slot)  # type: ignore
                                    if action_channel_bag:
                                        if get_can_associate_fcurve_list_with_armature(obj, action_channel_bag.fcurves):
                                            armature_actions_map.append((obj, action))

                else:
                    # Found compatible actions using armature bones
                    events.stop_last_and_start_new_event(f'Export Auto "{obj.name}" Loop actions')
                    for action in bpy.data.actions:
                        if not action.library:
                            if get_can_associate_fcurve_list_with_armature(obj, action.fcurves): #type: ignore
                                armature_actions_map.append((obj, action))
                
                events.stop_last_event()

                

            # Export Specific List
            elif action_export_enum.value == BFU_AnimActionExportEnum.EXPORT_SPECIFIC_LIST.value:
                events.add_sub_event(f'Export Specific List "{obj.name}"')
                for target_action in bfu_anim_action_props.object_action_asset_list(obj):
                    if target_action.use:
                        # No need to check if not action.library: because alredsy checked in get_object_action_asset_list
                        if target_action.name in bpy.data.actions:
                            armature_actions_map.append((obj, bpy.data.actions[target_action.name]))
                events.stop_last_event()

            # Export Specific Prefix
            elif action_export_enum.value == BFU_AnimActionExportEnum.EXPORT_SPECIFIC_PREFIX.value:
                events.add_sub_event(f'Export Specific Prefix "{obj.name}"')
                for action in bpy.data.actions:
                    if get_action_use_prefix(obj, action):
                        armature_actions_map.append((obj, action))
                events.stop_last_event()

            # Export Current
            elif action_export_enum.value == BFU_AnimActionExportEnum.EXPORT_CURRENT.value:
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
    action_asset_list = bfu_anim_action_props.object_action_asset_list(obj)  # CollectionProperty<BFU_OT_ObjExportAction>
    events.stop_last_and_start_new_event("Check Action In Asset List")
    for target_action in action_asset_list:
        if target_action.use:
            if target_action.name == action.name:
                events.stop_last_event()
                return True
    events.stop_last_event()
    return False

def get_action_use_prefix(obj: bpy.types.Object, action: bpy.types.Action) -> bool:
    if fnmatch.fnmatchcase(action.name, bfu_anim_action_props.object_prefix_name_to_export(obj) + "*"):
        return True
    return False

def get_action_is_current(obj: bpy.types.Object, action: bpy.types.Action) -> bool:
    if obj.animation_data and obj.animation_data.action:
        if obj.animation_data.action == action:
            return True
    return False
