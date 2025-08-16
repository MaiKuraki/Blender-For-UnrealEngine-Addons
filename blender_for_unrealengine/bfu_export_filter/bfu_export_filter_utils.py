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
from . import bfu_export_filter_props

def get_use_static_export() -> bool: 
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_static_export(scene) # type: ignore
    return False

def get_use_static_collection_export() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_static_collection_export(scene) # type: ignore
    return False

def get_use_skeletal_export() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_skeletal_export(scene) # type: ignore
    return False

def get_use_animation_export() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_animation_export(scene) # type: ignore
    return False

def get_use_alembic_export() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_alembic_export(scene) # type: ignore
    return False

def get_use_groom_simulation_export() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_groom_simulation_export(scene) # type: ignore
    return False

def get_use_camera_export() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_camera_export(scene) # type: ignore
    return False

def get_use_spline_export() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_spline_export(scene) # type: ignore
    return False

def get_use_text_export_log() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_text_export_log(scene) # type: ignore
    return False

def get_use_text_import_asset_script() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_text_import_asset_script(scene) # type: ignore
    return False

def get_use_text_import_sequence_script() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_text_import_sequence_script(scene) # type: ignore
    return False

def get_use_text_additional_data() -> bool:
    scene = bpy.context.scene
    if  scene:
        return bfu_export_filter_props.scene_use_text_additional_data(scene) # type: ignore
    return False
