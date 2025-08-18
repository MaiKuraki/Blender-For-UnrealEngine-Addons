# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from typing import List, Tuple
from .. import bfu_export_filter
from .. import bfu_anim_action
from ..bfu_anim_action.bfu_anim_action_props import BFU_AnimActionExportEnum

class CachedActionObjectInfo():
    def __init__(self) -> None:
        self.use_animation_export: bool = False

    def set_scene(self, scene: bpy.types.Scene) -> None:
        self.use_animation_export = bfu_export_filter.bfu_export_filter_props.scene_use_animation_export(scene)

    def is_identical(self, scene: bpy.types.Scene) -> bool:
        if self.use_animation_export != bfu_export_filter.bfu_export_filter_props.scene_use_animation_export(scene):
            return False
        return True

class CachedActionArmatureInfo():
    def __init__(self) -> None:
        self.obj_name: str = ""
        self.armature_bone_count: int = 0
        self.export_as_lod_mesh: bool = False
        self.anim_nla_use: bool = False
        self.export_skeletal_mesh_as_static_mesh: bool = False
        self.action_export_enum: BFU_AnimActionExportEnum = BFU_AnimActionExportEnum.EXPORT_AUTO

    def set_object(self, obj: bpy.types.Object) -> None:
        self.obj_name = obj.name
        if isinstance(obj.data, bpy.types.Armature):
            self.armature_bone_count = len(obj.data.bones)
        else:
            self.armature_bone_count = 0
        self.export_as_lod_mesh = obj.bfu_export_as_lod_mesh  # type: ignore[attr-defined]
        self.anim_nla_use = obj.bfu_anim_nla_use  # type: ignore[attr-defined]
        self.export_skeletal_mesh_as_static_mesh = obj.bfu_export_skeletal_mesh_as_static_mesh  # type: ignore[attr-defined]
        self.action_export_enum = bfu_anim_action.bfu_anim_action_props.get_object_anim_action_export_enum(obj)

    def is_identical(self, obj: bpy.types.Object) -> bool:
        if self.obj_name != obj.name:
            return False
        if self.armature_bone_count != (len(obj.data.bones) if isinstance(obj.data, bpy.types.Armature) else 0):
            return False
        if self.export_as_lod_mesh != obj.bfu_export_as_lod_mesh:  # type: ignore[attr-defined]
            return False
        if self.anim_nla_use != obj.bfu_anim_nla_use:  # type: ignore[attr-defined]
            return False
        if self.export_skeletal_mesh_as_static_mesh != obj.bfu_export_skeletal_mesh_as_static_mesh:  # type: ignore[attr-defined]
            return False
        if self.action_export_enum.value != bfu_anim_action.bfu_anim_action_props.get_object_anim_action_export_enum(obj).value:
            return False
        return True

class CachedActionManager():
    def __init__(self):
        self.cached_scene_details: CachedActionObjectInfo = CachedActionObjectInfo()
        self.cached_object_count: int = 0
        self.cached_object_details: List[CachedActionArmatureInfo] = []
        self.cached_total_action_count: int = 0
        
        self.armature_actions_map: List[Tuple[bpy.types.Object, bpy.types.Action]] = []

    def get_need_update_cache(self, scene: bpy.types.Scene, objects: List[bpy.types.Object]) -> bool:
        if self.cached_object_count != len(objects):
            print(f"CachedActionManager: Need update cache, because object count changed: {self.cached_object_count} != {len(objects)}")
            return True
        if self.cached_total_action_count != len(bpy.data.actions):
            print(f"CachedActionManager: Need update cache, because action count changed: {self.cached_total_action_count} != {len(bpy.data.actions)}")
            return True
        
        if not self.cached_scene_details.is_identical(scene):
            print(f"CachedActionManager: Need update cache, because scene details changed")
            return True

        obj_names = [o.name for o in objects]
        for items in self.armature_actions_map:
            if items[0].name not in obj_names:
                print(f"CachedActionManager: Need update cache, because cached armature '{items[0].name}' is not in tested objects")
                return True

        for x, obj in enumerate(objects):
            if not self.cached_object_details[x].is_identical(obj):
                print(f"CachedActionManager: Need update cache, because object details changed for '{obj.name}'")
                return True

        return False

    def set_cache(self, scene: bpy.types.Scene, objects: List[bpy.types.Object], new_armature_actions_map: List[Tuple[bpy.types.Object, bpy.types.Action]]) -> None:
        self.cached_scene_details.set_scene(scene)

        self.cached_object_count = len(objects)
        self.cached_total_action_count = len(bpy.data.actions)

        # Save object data to check cache
        self.cached_object_details.clear()
        for obj in objects:
            armature_info = CachedActionArmatureInfo()
            armature_info.set_object(obj)
            self.cached_object_details.append(armature_info)

        # Save Cached Armature Actions Map
        self.armature_actions_map = new_armature_actions_map

    def get_cache(self) -> List[Tuple[bpy.types.Object, bpy.types.Action]]:
        return self.armature_actions_map

cached_action_manager = CachedActionManager()