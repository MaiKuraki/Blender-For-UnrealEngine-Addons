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
import math
from typing import List, TYPE_CHECKING

from . import bfu_check_props
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_cached_assets

from .. import bfu_collision
from .. import bfu_socket
from .. import bfu_skeletal_mesh
from .. import bfu_export_logs

def get_potential_errors() -> List[bfu_check_props.BFU_OT_UnrealPotentialError]:
    scene = bpy.context.scene
    return scene.bfu_export_potential_errors

def get_potential_error_by_index(index) -> bfu_check_props.BFU_OT_UnrealPotentialError:
    scene = bpy.context.scene
    return scene.bfu_export_potential_errors[index]

def remove_potential_by_index(index):
    scene = bpy.context.scene
    scene.bfu_export_potential_errors.remove(index)

def clear_potential_errors():
    scene = bpy.context.scene
    scene.bfu_export_potential_errors.clear()

def process_general_fix():
    time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("Clean before export")
    fixed_collisions = bfu_collision.bfu_collision_utils.fix_export_type_on_collision()
    fixed_collision_names = bfu_collision.bfu_collision_utils.fix_name_on_collision()
    fixed_sockets = bfu_socket.bfu_socket_utils.fix_export_type_on_socket()
    fixed_socket_names = bfu_socket.bfu_socket_utils.fix_name_on_socket()

    fix_info = {
        "Fixed Collision(s)": fixed_collisions,
        "Fixed Collision Names(s)": fixed_collision_names,
        "Fixed Socket(s)": fixed_sockets,
        "Fixed Socket Names(s)": fixed_socket_names,
    }

    time_log.end_time_log()
    return fix_info

def get_vertices_with_zero_weight(Armature, Mesh):
    vertices = []
    
    # Créez un ensemble des noms des os de l'armature pour une recherche plus rapide
    armature_bone_names = set(bone.name for bone in Armature.data.bones)
    
    
    for vertex in Mesh.data.vertices: #MeshVertex(bpy_struct)
        cumulateWeight = 0
        
        if vertex.groups:
            for group_elem in vertex.groups: #VertexGroupElement(bpy_struct)
                if group_elem.weight > 0:
                    group_index = group_elem.group
                    group_len = len(Mesh.vertex_groups)
                    if group_index <= group_len:
                        group = Mesh.vertex_groups[group_elem.group]
                        
                        # Utilisez l'ensemble des noms d'os pour vérifier l'appartenance à l'armature
                        if group.name in armature_bone_names:
                            cumulateWeight += group_elem.weight
        
        if cumulateWeight == 0:
            vertices.append(vertex)
    
    return vertices

def select_potential_issue_object(issue_index):
    # Select potential error

    bbpl.utils.safe_mode_set('OBJECT', bpy.context.active_object)
    scene = bpy.context.scene
    my_po_error = get_potential_error_by_index(issue_index)

    obj = my_po_error.object

    bpy.ops.object.select_all(action='DESELECT')
    obj.hide_viewport = False
    obj.hide_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # show collection for select object
    for collection in bpy.data.collections:
        for ColObj in collection.objects:
            if ColObj == obj:
                bfu_basics.SetCollectionUse(collection)
    bpy.ops.view3d.view_selected()
    return obj

def select_potential_issue_vertices(issue_index):
    # Select potential error
    select_potential_issue_object(issue_index)
    bbpl.utils.safe_mode_set('EDIT')

    scene = bpy.context.scene
    my_po_error = get_potential_error_by_index(issue_index)
    obj = my_po_error.object
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')

    bbpl.utils.safe_mode_set('OBJECT')
    if my_po_error.selectOption == "VertexWithZeroWeight":
        for vertex in get_vertices_with_zero_weight(obj.parent, obj):
            vertex.select = True
    bbpl.utils.safe_mode_set('EDIT')
    bpy.ops.view3d.view_selected()
    return obj

def select_potential_issue_pose_bone(issue_index):
    # Select potential error
    select_potential_issue_object(issue_index)
    bbpl.utils.safe_mode_set('POSE')

    scene = bpy.context.scene
    my_po_error = get_potential_error_by_index(issue_index)
    obj = my_po_error.object
    bone = obj.data.bones[my_po_error.itemName]

    # Make bone visible if hide in a layer
    for x, layer in enumerate(bone.layers):
        if not obj.data.layers[x] and layer:
            obj.data.layers[x] = True

    bpy.ops.pose.select_all(action='DESELECT')
    obj.data.bones.active = bone
    bone.select = True

    bpy.ops.view3d.view_selected()
    return obj

def try_to_correct_potential_issues(issue_index):
    # Try to correct potential error

    scene = bpy.context.scene
    my_po_error = get_potential_error_by_index(issue_index)
    global successCorrect
    successCorrect = False

    local_view_areas = bbpl.scene_utils.move_to_global_view()

    MyCurrentDataSave = bbpl.save_data.scene_save.UserSceneSave()
    MyCurrentDataSave.save_current_scene()

    bbpl.utils.safe_mode_set('OBJECT', MyCurrentDataSave.user_select_class.user_active)

    print("Start correct")

    def SelectObj(obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    # Correction list

    if my_po_error.correctRef == "SetUnrealUnit":
        bpy.context.scene.unit_settings.scale_length = 0.01
        successCorrect = True

    if my_po_error.correctRef == "ConvertToMesh":
        obj = my_po_error.object
        SelectObj(obj)
        bpy.ops.object.convert(target='MESH')
        successCorrect = True

    if my_po_error.correctRef == "SetKeyRangeMin":
        obj = my_po_error.object
        key = obj.data.shape_keys.key_blocks[my_po_error.itemName]
        key.slider_min = -5
        successCorrect = True

    if my_po_error.correctRef == "SetKeyRangeMax":
        obj = my_po_error.object
        key = obj.data.shape_keys.key_blocks[my_po_error.itemName]
        key.slider_max = 5
        successCorrect = True

    if my_po_error.correctRef == "CreateUV":
        obj = my_po_error.object
        SelectObj(obj)
        if bbpl.utils.safe_mode_set("EDIT", obj):
            bpy.ops.uv.smart_project()
            successCorrect = True
        else:
            successCorrect = False

    if my_po_error.correctRef == "RemoveModfier":
        obj = my_po_error.object
        mod = obj.modifiers[my_po_error.itemName]
        obj.modifiers.remove(mod)
        successCorrect = True

    if my_po_error.correctRef == "PreserveVolume":
        obj = my_po_error.object
        mod = obj.modifiers[my_po_error.itemName]
        mod.use_deform_preserve_volume = False
        successCorrect = True

    if my_po_error.correctRef == "BoneSegments":
        obj = my_po_error.object
        bone = obj.data.bones[my_po_error.itemName]
        bone.bbone_segments = 1
        successCorrect = True

    if my_po_error.correctRef == "InheritScale":
        obj = my_po_error.object
        bone = obj.data.bones[my_po_error.itemName]
        bone.use_inherit_scale = True
        successCorrect = True

    # ----------------------------------------Reset data
    MyCurrentDataSave.reset_select(use_names = True)
    MyCurrentDataSave.reset_scene_at_save()
    bbpl.scene_utils.move_to_local_view(local_view_areas)

    # ----------------------------------------

    if successCorrect:
        print("end correct, Error: " + my_po_error.correctRef)
        remove_potential_by_index(issue_index)
        return "Corrected"
    print("end correct, Error not found")
    return "Correct fail"





