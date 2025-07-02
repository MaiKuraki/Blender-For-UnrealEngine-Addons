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
import math
import os
import mathutils
from bpy_extras.io_utils import axis_conversion
from pathlib import Path
from typing import Optional, Dict, Any, List
from .. import bpl
from .. import bfu_export_text_files
from .. import bfu_basics
from .. import bfu_utils
from .. import bbpl
from .. import bfu_static_mesh
from .. import bfu_skeletal_mesh
from .. import bfu_socket
from .. import bfu_export_logs
from .. import bfu_addon_prefs
from .. import bfu_skeletal_mesh

# @TODO: Move this to a config file.
dup_temp_name = "BFU_Temp"  # Duplicate object temporary name
Export_temp_preFix = "_ESO_Temp"  # _ExportSubObject_TempName

class SavedSceneSimplfy():
    def __init__(self):
        if bpy.context is None:
            return
        scene = bpy.context.scene

        # General
        self.use_simplify: bool = bpy.context.scene.render.use_simplify

        # Viewport
        self.simplify_subdivision: int = scene.render.simplify_subdivision
        self.simplify_child_particles: int = scene.render.simplify_child_particles
        self.simplify_volumes: int = scene.render.simplify_volumes
        self.use_simplify_normals: bool = scene.render.use_simplify_normals

        # Render
        self.simplify_subdivision_render: int = scene.render.simplify_subdivision_render
        self.simplify_child_particles_render: int = scene.render.simplify_child_particles_render

    def simplify_scene(self):
        if bpy.context is None:
            return
        scene = bpy.context.scene

        simplify_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Simplify scene")
        # General
        scene.render.use_simplify = True

        # Viewport
        scene.render.simplify_subdivision = 0
        scene.render.simplify_child_particles = 0
        scene.render.simplify_volumes = 0
        scene.render.use_simplify_normals = False

        # Render
        scene.render.simplify_subdivision_render = 0
        scene.render.simplify_child_particles_render = 0
        simplify_time_log.end_time_log()

    def unsimplify_scene(self):
        # Reset scene for without data loose.
        if bpy.context is None:
            return
        scene = bpy.context.scene

        unsimplify_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Unsimplify scene")
        # General
        scene.render.use_simplify = False
        unsimplify_time_log.end_time_log()


    def reset_scene(self):
        # Reset scene to saved scene.
        if bpy.context is None:
            return
        scene = bpy.context.scene

        # General
        scene.render.use_simplify = self.use_simplify

        # Viewport
        scene.render.simplify_subdivision = self.simplify_subdivision
        scene.render.simplify_child_particles = self.simplify_child_particles
        scene.render.simplify_volumes = self.simplify_volumes
        scene.render.use_simplify_normals = self.use_simplify_normals

        # Render
        scene.render.simplify_subdivision_render = self.simplify_subdivision_render
        scene.render.simplify_child_particles_render = self.simplify_child_particles_render


def check_and_make_export_path(dirpath: Path):
    """
    Check if the directory exists, and create it if it doesn't.
    If the path ends with a file extension, it will create the directory of that file.
    """
    absdirpath = dirpath.resolve()

    # Si le chemin finit par une extension, on suppose que c'est un fichier
    if absdirpath.suffix:
        absdirpath = absdirpath.parent

    if not absdirpath.exists():
        try:
            os.makedirs(absdirpath)
        except Exception as e:
            error_text: str = f"An error occurred during makedirs: {str(e)}"
            print(bpl.color_set.red(error_text))
            return False

    return True


def ApplyProxyData(obj):

    scene = bpy.context.scene
    # Apply proxy data if needed.
    if bfu_utils.GetExportProxyChild(obj) is not None:

        def ReasignProxySkeleton(newArmature, oldArmature):
            for select in bpy.context.selected_objects:
                if select.type == "CURVE":
                    for mod in select.modifiers:
                        if mod.type == "HOOK":
                            if mod.object == oldArmature:
                                matrix_inverse = mod.matrix_inverse.copy()
                                mod.object = newArmature
                                mod.matrix_inverse = matrix_inverse

                else:
                    for mod in select.modifiers:
                        if mod.type == 'ARMATURE':
                            if mod.object == oldArmature:
                                mod.object = newArmature

            for bone in newArmature.pose.bones:
                for cons in bone.constraints:
                    if hasattr(cons, 'target'):
                        if cons.target == oldArmature:
                            cons.target = newArmature
                        else:
                            ChildProxyName = (
                                cons.target.name +
                                "_UEProxyChild"
                            )
                            if ChildProxyName in scene.objects:
                                cons.target = scene.objects[ChildProxyName]

        # Get old armature in selected objects
        OldProxyChildArmature = None
        for selectedObj in bpy.context.selected_objects:
            if selectedObj != obj:
                if selectedObj.type == "ARMATURE":
                    OldProxyChildArmature = selectedObj

        # Reasing parent + add to remove
        if OldProxyChildArmature is not None:
            ToRemove = []
            ToRemove.append(OldProxyChildArmature)
            for selectedObj in bpy.context.selected_objects:
                if selectedObj != obj:
                    if selectedObj.parent == OldProxyChildArmature:
                        # Reasing parent and keep position
                        SavedPos = selectedObj.matrix_world.copy()
                        selectedObj.name += "_UEProxyChild"
                        selectedObj.parent = obj
                        selectedObj.matrix_world = SavedPos
                    else:
                        ToRemove.append(selectedObj)
            ReasignProxySkeleton(obj, OldProxyChildArmature)
            SavedSelect = bbpl.save_data.select_save.UserSelectSave()
            SavedSelect.save_current_select()

            RemovedObjects = bfu_utils.clean_delete_objects(ToRemove)
            SavedSelect.remove_from_list_by_name(RemovedObjects)
            SavedSelect.reset_select()


def bake_armature_animation(armature: bpy.types.Object, frame_start: int, frame_end: int):
    # Change to pose mode
    SavedSelect = bbpl.save_data.select_save.UserSelectSave()
    SavedSelect.save_current_select()
    bpy.ops.object.select_all(action='DESELECT')  # type: ignore
    bbpl.utils.select_specific_object(armature)
    bpy.ops.nla.bake(  # type: ignore
        frame_start=frame_start-10,
        frame_end=frame_end+10,
        only_selected=False,
        visual_keying=True,
        clear_constraints=True,
        use_current_action=False,
        bake_types={'POSE'}
        )
    bpy.ops.object.select_all(action='DESELECT')  # type: ignore
    SavedSelect.reset_select()

class DelegateOldData():
    # contain a data to remove and function for remove

    def __init__(self, data_name: str, data_type: str):
        self.data_name = data_name
        self.data_type = data_type

    def remove_data(self):
        bfu_utils.remove_useless_specific_data(self.data_name, self.data_type)

class DuplicateData():
    def __init__(self):
        self.data_to_remove: list[DelegateOldData] = []
        self.origin_select: Optional[bbpl.save_data.select_save.UserSelectSave] = None
        self.duplicate_select: Optional[bbpl.save_data.select_save.UserSelectSave] = None

    def duplicate_select_for_export(self, context: bpy.types.Context, reset_simplify_after_duplicate: bool = True):
        duplicate_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Duplicate asset selection")

        # Enable simplify for faster duplicate (Don't )
        saved_simplify: SavedSceneSimplfy = SavedSceneSimplfy()
        saved_simplify.simplify_scene()

        log_4 = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Prepare duplicate")
        scene = context.scene

        self.set_origin_select()
        if self.origin_select:
            for user_selected in self.origin_select.user_selecteds:
                if user_selected:
                    bfu_utils.save_obj_current_name(user_selected)
                    if user_selected.type == "ARMATURE":  # type: ignore
                        bfu_utils.set_obj_proxy_data(user_selected)

        data_to_remove: list[DelegateOldData] = []

        # Save action befor export
        action_names: list[str] = []
        for action in bpy.data.actions:
            action_names.append(action.name)

        log_4.end_time_log()

        log_4 = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Duplicate")
        # Note: Need look for a optimized duplicate, This is too long
        bpy.ops.object.duplicate()  # type: ignore
        log_4.end_time_log()

        log_4 = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Prepare clean")
        # Save the name for found after "Make Instances Real"
        current_select_names: list[str] = []
        for current_select_name in context.selected_objects:
            current_select_names.append(current_select_name.name)

        for obj_select in current_select_names:
            if obj_select not in context.selected_objects:  # type: ignore
                scene.objects[obj_select].select_set(True)  # type: ignore

        # Make sigle user and clean useless data.
        for objScene in context.selected_objects:
            if objScene.data is not None:
                oldData = objScene.data.name
                objScene.data = objScene.data.copy()
                data_to_remove.append(DelegateOldData(oldData, objScene.type))  # type: ignore
        log_4.end_time_log()

        log_4 = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Clean")
        # Clean create actions by duplication
        for action in bpy.data.actions:
            if action.name not in action_names:
                bpy.data.actions.remove(action)  # type: ignore

        if reset_simplify_after_duplicate:
            saved_simplify.reset_scene()
        log_4.end_time_log()

        log_4 = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Update select")
        self.set_duplicate_select()
        log_4.end_time_log()

        duplicate_time_log.end_time_log()

    def set_origin_select(self):
        select = bbpl.save_data.select_save.UserSelectSave()
        select.save_current_select()
        self.origin_select = select

    def set_duplicate_select(self):
        select = bbpl.save_data.select_save.UserSelectSave()
        select.save_current_select()
        self.duplicate_select = select

    def set_duplicate_name_for_export(self, origin_prefix: str = "or_"):
        # Add prefix to the original objects.
        if self.origin_select:
            for user_selected in self.origin_select.user_selecteds:
                user_selected.name = origin_prefix + user_selected.name
        
        # Rename the duplicated copies with the original names.
        if self.duplicate_select:
            for user_selected in self.duplicate_select.user_selecteds:
                user_selected.name = bfu_utils.get_obj_origin_name(user_selected)


    def reset_duplicate_name_after_export(self):
        # Restore the original names of the objects after export.
        # Considering that the duplicated objects have been renamed.
        if self.origin_select:
            for user_selected in self.origin_select.user_selecteds:
                user_selected.name = bfu_utils.get_obj_origin_name(user_selected)
                bfu_utils.clear_obj_origin_name_var(user_selected)


def duplicate_select_for_export(context: bpy.types.Context, reset_simplify_after_duplicate: bool = True) -> DuplicateData:
    duplicate_data = DuplicateData()
    duplicate_data.duplicate_select_for_export(context, reset_simplify_after_duplicate)
    return duplicate_data


def apply_select_needed_modifiers_for_export():
    if bpy.context is None:
        return

    apply_modifiers_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Apply modifiers")
    apply_modifiers_prepare_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Prepare for apply modifiers")
    saved_select = bbpl.save_data.select_save.UserSelectSave()
    saved_select.save_current_select()

    # Disable simplify for avoid, skipping apply.
    bpy.context.scene.render.use_simplify = False
    apply_modifiers_prepare_time_log.end_time_log()

    # Get selected objects with modifiers.
    for obj in bpy.context.selected_objects:
        apply_object_modifiers(obj, ['ARMATURE'])

    saved_select.reset_select()
    apply_modifiers_time_log.end_time_log()

def apply_object_modifiers(obj: bpy.types.Object, blacklist_type = []):

    if(obj.type == "MESH" and obj.data.shape_keys is not None):
        # Can't apply modifiers with shape key
        return

    apply_modifiers_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Apply modifiers for: {obj.name}")
    apply_modifiers_prepare_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Search modifiers to apply")
    # Get Modifier to Apply
    mod_to_apply: list[bpy.types.Modifier] = []
    for mod in obj.modifiers:
        if mod.type not in blacklist_type:
            if mod.show_viewport == True:
                mod_to_apply.append(mod)
    apply_modifiers_prepare_time_log.end_time_log()

    if len(mod_to_apply) > 0:
        time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Select object for apply modifiers")
        bbpl.utils.select_specific_object(obj)
        time_log.end_time_log()
        
        time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Make single user")
        if obj.data.users > 1:
            # Make single user.
            obj.data = obj.data.copy()
        time_log.end_time_log()

        for mod in mod_to_apply:
            if bpy.ops.object.modifier_apply.poll():
                apply_modifier_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Apply modifier: {mod.name} ({mod.type})")
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                except RuntimeError as ex:
                    # print the error incase its important... but continue
                    print(ex)
                apply_modifier_time_log.end_time_log()
    apply_modifiers_time_log.end_time_log()


def convert_selected_to_mesh():
    # Have to convert text and curve objects to mesh before MakeSelectVisualReal to avoid duplicate issue.
    type_to_convert = ["CURVE", "SURFACE", "META", "FONT"]

    scene = bpy.context.scene

    # Save current scene object list
    previous_objects = []
    for obj in scene.objects:
        previous_objects.append(obj)

    # Save Select
    select = bbpl.save_data.select_save.UserSelectSave()
    select.save_current_select()
    
    # Select all object
    bpy.ops.object.select_all(action='DESELECT')

    # Select object to convert
    for selected_obj in select.user_selecteds:
        if selected_obj.type in type_to_convert:
            selected_obj.select_set(True)

    # Convert selct to mesh
    if bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0] #Convert fail if active is none.
        bpy.ops.object.convert(target='MESH')

    # Reset select
    select.reset_select(use_names = True)
    
    # Select the new objects
    for obj in scene.objects:
        if obj not in previous_objects:
            obj.select_set(True)


def make_select_visual_real():
    scene = bpy.context.scene
    select = bbpl.save_data.select_save.UserSelectSave()
    select.save_current_select()

    # Save object list
    previous_objects = []
    for obj in scene.objects:
        previous_objects.append(obj)

    # Visual Transform Apply
    bpy.ops.object.visual_transform_apply()

    # Make Instances Real 
    # Note:Text and curve need to be converted to mesh before Make Instances Real to avoid duplicate issue.
    bpy.ops.object.duplicates_make_real(
        use_base_parent=False,
        use_hierarchy=True
        )

    select.reset_select(use_names = True)
    
    # Select the new objects
    for obj in scene.objects:
        if obj not in previous_objects:
            obj.select_set(True)

# Sockets
def SetSocketsExportName(obj: bpy.types.Object):
    '''
    Try to apply the custom SocketName
    '''

    scene = bpy.context.scene
    for socket in bfu_socket.bfu_socket_utils.get_socket_desired_children(obj):
        if socket.bfu_use_socket_custom_Name:
            if socket.bfu_socket_custom_Name not in scene.objects:

                # Save the previous name
                socket["BFU_PreviousSocketName"] = socket.name
                socket.name = "SOCKET_"+socket.bfu_socket_custom_Name
            else:
                print(
                    'Can\'t rename socket "' +
                    socket.name +
                    '" to "'+socket.bfu_socket_custom_Name +
                    '".'
                    )


def SetSocketsExportTransform(obj: bpy.types.Object):
    # Set socket Transform for Unreal

    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    for socket in bfu_socket.bfu_socket_utils.get_socket_desired_children(obj):
        socket["BFU_PreviousSocketScale"] = socket.scale
        socket["BFU_PreviousSocketLocation"] = socket.location
        socket["BFU_PreviousSocketRotationEuler"] = socket.rotation_euler
        if get_should_rescale_sockets():
            socket.delta_scale *= GetRescaleSocketFactor()

        if addon_prefs.staticSocketsAdd90X:
            savedScale = socket.scale.copy()
            savedLocation = socket.location.copy()
            AddMat = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')
            socket.matrix_world = socket.matrix_world @ AddMat
            socket.scale.x = savedScale.x
            socket.scale.z = savedScale.y
            socket.scale.y = savedScale.z
            socket.location = savedLocation


def reset_sockets_export_name(obj: bpy.types.Object):
    # Reset socket Name

    for socket in bfu_socket.bfu_socket_utils.get_socket_desired_children(obj):
        if "BFU_PreviousSocketName" in socket:
            socket.name = socket["BFU_PreviousSocketName"]
            del socket["BFU_PreviousSocketName"]


def reset_sockets_transform(obj: bpy.types.Object):
    # Reset socket Transform

    for socket in bfu_socket.bfu_socket_utils.get_socket_desired_children(obj):
        if "BFU_PreviousSocketScale" in socket:
            socket.scale = socket["BFU_PreviousSocketScale"]
            del socket["BFU_PreviousSocketScale"]
        if "BFU_PreviousSocketLocation" in socket:
            socket.location = socket["BFU_PreviousSocketLocation"]
            del socket["BFU_PreviousSocketLocation"]
        if "BFU_PreviousSocketRotationEuler" in socket:
            socket.rotation_euler = socket["BFU_PreviousSocketRotationEuler"]
            del socket["BFU_PreviousSocketRotationEuler"]


# Main asset

class SavedObjectNames():
    def __init__(self):
        self.saved_names: Dict[bpy.types.Object, str] = {}

    def save_new_name(self, obj: bpy.types.Object):
        # Add object to save without clearing the previous saved names.
        self.saved_names[obj] = obj.name

    def save_new_names(self, objs: List[bpy.types.Object]):
        # Add objects to save without clearing the previous saved names.
        for obj in objs:
            self.saved_names[obj] = obj.name

    def restore_names(self):
        for obj, name in self.saved_names.items():
            obj.name = name
        self.saved_names.clear()

def set_object_export_name(obj: bpy.types.Object, is_skeletal: bool):
    # Set is_skeleton = True only for skeletal assets.
    # Static meshes with armature should use is_skeleton = False
    return set_duplicated_object_export_name(obj, obj, is_skeletal)

def set_duplicated_object_export_name(duplicated_obj: bpy.types.Object, original_obj: bpy.types.Object, is_skeletal: bool):
    # Set is_skeleton = True only for skeletal assets.
    # Static meshes with armature should use is_skeleton = False
    if bpy.context is None:
        return
    scene = bpy.context.scene

    # get the desired export name.
    if is_skeletal:
        desired_export_name: str = bfu_utils.get_desired_export_armature_name(original_obj)
    else:
        # Consider duplicated object as already renamed in set_duplicate_name_for_export() so keep the name.
        desired_export_name: str = duplicated_obj.name # Could be used in future?

    # Check if needs change before applying it.
    if duplicated_obj.name != desired_export_name:
        # Avoid same name for two assets.
        # Set a temporary name for conflict assets. 
        # Use SavedObjectNames() to save the original name and restore it after export.
        if desired_export_name in scene.objects:
            conflict_asset = scene.objects[desired_export_name]
            conflict_asset.name = dup_temp_name
        duplicated_obj.name = desired_export_name


# UVs
def ConvertGeometryNodeAttributeToUV(obj: bpy.types.Object, attrib_name: str):
    # I need apply the geometry modifier for get the data.
    # So this work only when I do export of the duplicate object.
    
    if hasattr(obj.data, "attributes"):  # Cuves has not attributes.
        if attrib_name in obj.data.attributes:

            # TO DO: Bad why to do this. Need found a way to convert without using ops.
            obj.data.attributes.active = obj.data.attributes[attrib_name]

            # Because a bug Blender set the wrong attribute as active in 3.5.
            if obj.data.attributes.active != obj.data.attributes[attrib_name]:
                for x, attribute in enumerate(obj.data.attributes):
                    if attribute.name == attrib_name:
                        obj.data.attributes.active_index = x

            SavedSelect = bbpl.save_data.select_save.UserSelectSave()
            SavedSelect.save_current_select()
            bbpl.utils.select_specific_object(obj)
            if bpy.app.version >= (3, 5, 0):
                if obj.data.attributes.active:
                    bpy.ops.geometry.attribute_convert(mode='GENERIC', domain='CORNER', data_type='FLOAT2')
            else:
                if obj.data.attributes.active:
                    bpy.ops.geometry.attribute_convert(mode='UV_MAP', domain='CORNER', data_type='FLOAT2')
            SavedSelect.reset_select()

            # Because it not possible to move UV index I need recreate all UV for place new UV Map at start...
            if len(obj.data.uv_layers) < 8:  # Blender Cannot add more than 8 UV maps.

                uv_names = []  # Cache uv names
                for old_uv in obj.data.uv_layers:
                    uv_names.append(old_uv.name)

                for name in uv_names:
                    old_uv = obj.data.uv_layers[name]
                    if name != attrib_name:
                        # Vars
                        new_uv_name = old_uv.name
                        old_uv_name = old_uv.name + "_OLDUVEXPORT"
                        # Rename and recreate new UV
                        old_uv.name += "_OLDUVEXPORT"
                        obj.data.uv_layers.active = old_uv
                        new_uv = obj.data.uv_layers.new(name=new_uv_name, do_init=True)
                        obj.data.uv_layers.active = new_uv
                        # Remove old one
                        obj.data.uv_layers.remove(obj.data.uv_layers[old_uv_name])

            return

            attrib = obj.data.attributes[attrib_name]

            new_uv = obj.data.uv_layers.new(name=attrib_name)
            uv_coords = []

            attrib.data  # TO DO: I don't understand why attrib.data is egal at zero just after a duplicate.
            print('XXXXXXXXXXXX')
            print(type(attrib.data))
            print('XXXXXXXXXXXX')
            print(dir(attrib.data))
            print('XXXXXXXXXXXX')
            print(attrib.data.values())
            print('XXXXXXXXXXXX')
            attrib_data = []
            attrib.data.foreach_get('vector', attrib_data)
            print(attrib_data)

            for fv_attrib in attrib.data:  # FloatVectorAttributeValue
                uv_coords.append(fv_attrib.vector)
            uv_coords.append(attrib.data[0])

            for loop in obj.data.loops:
                new_uv.data[loop.index].uv[0] = uv_coords[loop.index][0]
                new_uv.data[loop.index].uv[1] = uv_coords[loop.index][1]

            obj.data.attributes.remove(attrib_name)


def CorrectExtremUVAtExport(obj: bpy.types.Object):
    if obj.bfu_use_correct_extrem_uv_scale:
        SavedSelect = bbpl.save_data.select_save.UserSelectSave()
        SavedSelect.save_current_select()
        bbpl.utils.select_specific_object(obj)
        if bfu_utils.GoToMeshEditMode():
            bfu_utils.CorrectExtremeUV(obj.bfu_correct_extrem_uv_scale_step_scale, obj.bfu_correct_extrem_uv_scale_use_absolute)
            bbpl.utils.safe_mode_set('OBJECT')
            SavedSelect.reset_select()
            return True
    return False

# Armature


def ConvertArmatureConstraintToModifiers(armature: bpy.types.Object):
    for obj in bfu_utils.GetExportDesiredChilds(armature):
        previous_enabled_armature_constraints = []

        for const in obj.constraints:
            if const.type == "ARMATURE":
                if const.enabled is True:
                    previous_enabled_armature_constraints.append(const.name)

                    # Disable constraint
                    const.enabled = False

                    # Remove All Vertex Group
                    # TO DO:

                    # Add Vertex Group
                    for target in const.targets:
                        bone_name = target.subtarget
                        group = obj.vertex_groups.new(name=bone_name)

                        vertex_indices = range(0, len(obj.data.vertices))
                        group.add(vertex_indices, 1.0, 'REPLACE')

                    # Add armature modifier
                    mod = obj.modifiers.new("BFU_Const_"+const.name, "ARMATURE")
                    mod.object = armature

        # Save data for reset after export
        obj["BFU_PreviousEnabledArmatureConstraints"] = previous_enabled_armature_constraints


def ResetArmatureConstraintToModifiers(armature: bpy.types.Object):
    for obj in bfu_utils.GetExportDesiredChilds(armature):
        if "BFU_PreviousEnabledArmatureConstraints" in obj:
            for const_names in obj["BFU_PreviousEnabledArmatureConstraints"]:
                const = obj.constraints[const_names]

                # Remove created armature for export
                mod = obj.modifiers["BFU_Const_"+const_names]
                obj.modifiers.remove(mod)

                # Remove created Vertex Group
                for target in const.targets:
                    bone_name = target.subtarget
                    old_vertex_group = obj.vertex_groups[bone_name]
                    obj.vertex_groups.remove(old_vertex_group)

                # Reset all Vertex Groups
                    # TO DO:

                # Enable back constraint
                const.enabled = True




def get_should_rescale_skeleton_for_fbx_export(obj: bpy.types.Object) -> bool:
    # This will return if the rig should be rescale.
    # This is only with FBX export. 
    # GlTF export support native blender scale to Unreal Engine. <3<3<3

    if not bfu_skeletal_mesh.bfu_export_procedure.is_fbx_file_export(obj):
        return False  # Rescale only if FBX export.

    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    if addon_prefs.rescaleFullRigAtExport == "auto":

        if bfu_utils.get_scene_unit_scale_is_close(0.01):
            return False  # False because that useless to rescale at 1 :v
        else:
            return True
    if addon_prefs.rescaleFullRigAtExport == "custom_rescale":
        return True
    if addon_prefs.rescaleFullRigAtExport == "dont_rescale":
        return False
    return False


def get_rescale_rig_factor() -> float:
    # This will return the rescale factor.

    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    if addon_prefs.rescaleFullRigAtExport == "auto":
        return 100 * bfu_utils.get_scene_unit_scale()
    else:
        return addon_prefs.newRigScale  # rigRescaleFactor


def get_should_rescale_sockets():
    # This will return if the socket should be rescale.

    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    if addon_prefs.rescaleSocketsAtExport == "auto":
        if bpy.context.scene.unit_settings.scale_length == 0.01:
            return False  # False because that useless to rescale at 1 :v
        else:
            return True
    if addon_prefs.rescaleSocketsAtExport == "custom_rescale":
        return True
    if addon_prefs.rescaleSocketsAtExport == "dont_rescale":
        return False
    return False


def GetRescaleSocketFactor():
    # This will return the rescale factor.

    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    if addon_prefs.rescaleSocketsAtExport == "auto":
        return 1/(100*bfu_utils.get_scene_unit_scale())
    else:
        return addon_prefs.staticSocketsImportedSize

def export_additional_data(fullpath: Path, data: Dict[str, str]) -> None:
    # Export additional parameter from static and skeletal mesh track for
    # SocketsList

    result = check_and_make_export_path(fullpath)
    if result:
        additional_data: Dict[str, Any] = bfu_export_text_files.bfu_export_text_files_asset_additional_data.write_additional_data(data)
        bfu_export_text_files.bfu_export_text_files_utils.export_single_json_file(additional_data, fullpath)

def get_final_fbx_export_primary_bone_axis(obj: bpy.types.Object) -> str:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_primary_bone_axis
    else:
        return bfu_skeletal_mesh.bfu_export_procedure.get_obj_skeleton_fbx_procedure_preset(obj)["primary_bone_axis"]

def get_final_fbx_export_secondary_bone_axis(obj: bpy.types.Object) -> str:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_secondary_bone_axis
    else:
        return bfu_skeletal_mesh.bfu_export_procedure.get_obj_skeleton_fbx_procedure_preset(obj)["secondary_bone_axis"]

def get_skeleton_fbx_export_use_space_transform(obj: bpy.types.Object) -> bool:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_use_space_transform
    else:
        return bfu_skeletal_mesh.bfu_export_procedure.get_obj_skeleton_fbx_procedure_preset(obj)["use_space_transform"]

def get_skeleton_export_axis_forward(obj: bpy.types.Object) -> str:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_axis_forward
    else:
        return bfu_skeletal_mesh.bfu_export_procedure.get_obj_skeleton_fbx_procedure_preset(obj)["axis_forward"]

def get_skeleton_export_axis_up(obj: bpy.types.Object) -> str:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_axis_up
    else:
        return bfu_skeletal_mesh.bfu_export_procedure.get_obj_skeleton_fbx_procedure_preset(obj)["axis_up"]

def get_static_fbx_export_use_space_transform(obj: bpy.types.Object) -> bool:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_use_space_transform
    else:
        return bfu_static_mesh.bfu_export_procedure.get_obj_static_fbx_procedure_preset(obj)["use_space_transform"]

def get_static_fbx_export_axis_forward(obj: bpy.types.Object) -> str:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_axis_forward
    else:
        return bfu_static_mesh.bfu_export_procedure.get_obj_static_fbx_procedure_preset(obj)["axis_forward"]

def get_static_fbx_export_axis_up(obj: bpy.types.Object) -> str:
    if obj.bfu_override_procedure_preset:
        return obj.bfu_fbx_export_axis_up
    else:
        return bfu_static_mesh.bfu_export_procedure.get_obj_static_fbx_procedure_preset(obj)["axis_up"]
    
class SaveTransformObjects():
    def __init__(self, obj: bpy.types.Object):

        self.saved_transform_objects = []
        obj_recursive_childs = bbpl.basics.get_recursive_obj_childs(obj, True)
        for obj in obj_recursive_childs:
            self.saved_transform_objects.append(bbpl.utils.SaveTransformObject(obj))

    def reset_object_transforms(self):
        for saved_transform_object in self.saved_transform_objects:
            saved_transform_object: bbpl.utils.SaveTransformObject
            if saved_transform_object.init_object:
                saved_transform_object.reset_object_transform()

def get_skeleton_axis_conversion(obj: bpy.types.Object) -> mathutils.Matrix:
    axis_forward = get_skeleton_export_axis_forward(obj)
    axis_up = get_skeleton_export_axis_up(obj)

    try:
        return axis_conversion(to_forward=axis_forward, to_up=axis_up).to_4x4()
    except Exception as e:
        print(f"For asset \"{obj.name}\" : {e}")
        return axis_conversion("-Z", "Y").to_4x4()

def get_static_axis_conversion(obj: bpy.types.Object) -> mathutils.Matrix:
    axis_forward = get_static_fbx_export_axis_forward(obj)
    axis_up = get_static_fbx_export_axis_up(obj)

    try:
        return axis_conversion(to_forward=axis_forward, to_up=axis_up).to_4x4()
    except Exception as e:
        print(f"For asset \"{obj.name}\" : {e}")
        return axis_conversion("-Z", "Y").to_4x4()