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
from .. import bfu_export_control


def get_recursive_obj_childs(obj: bpy.types.Object) -> List[bpy.types.Object]:
    # Get all recursive childs of a object
    # include_self is True obj is index 0
    context = bpy.context
    if context is None:
        return []
    scene_objects = context.scene.objects

    save_objects: List[bpy.types.Object] = []

    # Get all direct childs of a object
    def get_obj_childs(obj: bpy.types.Object) -> List[bpy.types.Object]:
        # Get all direct childs of a object
        
        childs_obj: List[bpy.types.Object] = []
        for child_obj in scene_objects:
            if child_obj.name in context.window.view_layer.objects:
                # Export only objects that are not library linked.
                # Still work on overridden objects.
                if bfu_export_control.bfu_export_control_utils.is_auto_or_export_recursive(child_obj):
                    if child_obj.library is None:  # type: ignore
                        if child_obj.parent is not None:
                            if child_obj.parent.name == obj.name:
                                childs_obj.append(child_obj)

        return childs_obj

    for newobj in get_obj_childs(obj):
        for childs in get_recursive_obj_childs(newobj):
            save_objects.append(childs)
        save_objects.append(newobj)
    return save_objects

def get_exportable_objects(obj: bpy.types.Object) -> List[bpy.types.Object]:
    # Found all exportable children of the object
    # Include the object itself

    desired_obj_list: List[bpy.types.Object] = [obj]
    desired_obj_list.extend(get_recursive_obj_childs(obj))
    return desired_obj_list