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
from typing import List
from .bfu_modular_skeletal_mesh_type import BFU_UI_ModularSkeletalSpecifiedPartsMeshs, BFU_UI_ModularSkeletalSpecifiedPartsMeshItem
from .. import bfu_export_control

def get_modular_skeletal_specified_parts_meshs_template(obj: bpy.types.Object) -> BFU_UI_ModularSkeletalSpecifiedPartsMeshs:
    return obj.bfu_modular_skeletal_specified_parts_meshs_template  # type: ignore[attr-defined]

def get_modular_objects_from_part(part: BFU_UI_ModularSkeletalSpecifiedPartsMeshItem) -> List[bpy.types.Object]:
    objects: List[bpy.types.Object] = []
    for skeletal_part in part.skeletal_parts.get_template_collection():
        if skeletal_part.enabled:
            if skeletal_part.target_type == 'OBJECT':  # Utilisez l'attribut target_type
                if skeletal_part.obj:
                    if bfu_export_control.bfu_export_control_utils.is_auto_or_export_recursive(skeletal_part.obj):
                        objects.append(skeletal_part.obj)
            elif skeletal_part.target_type == 'COLLECTION':
                if skeletal_part.collection:
                    for collection_obj in skeletal_part.collection.objects:
                        if bfu_export_control.bfu_export_control_utils.is_auto_or_export_recursive(collection_obj):
                            objects.append(collection_obj)
    return objects

def modular_mode_is_all_in_one(obj: bpy.types.Object) -> bool:
    return obj.bfu_modular_skeletal_mesh_mode == 'all_in_one'  # type: ignore[attr-defined]

def modular_mode_is_every_meshs(obj: bpy.types.Object) -> bool:
    return obj.bfu_modular_skeletal_mesh_mode == 'every_meshs'  # type: ignore[attr-defined]

def modular_mode_is_specified_parts(obj: bpy.types.Object) -> bool:
    return obj.bfu_modular_skeletal_mesh_mode == 'specified_parts'  # type: ignore[attr-defined]