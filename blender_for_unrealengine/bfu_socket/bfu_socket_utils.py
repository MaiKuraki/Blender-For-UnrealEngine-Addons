# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
import fnmatch
import math
import mathutils
from typing import List, Any, Dict
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_unreal_utils
from .. import bfu_export_control
from .. import bfu_addon_prefs
from .. import bfu_skeletal_mesh
from ..bfu_skeletal_mesh.bfu_export_procedure import BFU_SkeletonExportProcedure




def IsASocket(obj):
    '''
    Retrun True is object is an Socket.
    https://docs.unrealengine.com/en-US/WorkingWithContent/Importing/FBX/StaticMeshes/#sockets
    '''
    if obj.type == "EMPTY":
        cap_name = obj.name.upper()
        if cap_name.startswith("SOCKET_"):
            return True

    return False

def get_socket_desired_children(target_obj: bpy.types.Object) -> List[bpy.types.Object]:
    sockets: List[bpy.types.Object] = []
    for obj in bfu_utils.GetExportDesiredChilds(target_obj):
        if IsASocket(obj):
            sockets.append(obj)

    return sockets

def GetSocketsExportName(socket: bpy.types.Object) -> str:
    '''
    Get the current socket custom name
    '''
    if socket.bfu_use_socket_custom_Name:
        return socket.bfu_socket_custom_Name
    return socket.name[7:]

def get_skeletal_mesh_sockets(obj: bpy.types.Object) -> List[bpy.types.Object]:

    if obj.type != "ARMATURE":  # type: ignore
        return []

    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    data: Dict[str, Any] = {}
    sockets: List[bpy.types.Object] = []

    for socket in get_socket_desired_children(obj):
        sockets.append(socket)

    data['Sockets'] = []
    # config.set('Sockets', '; SocketName, BoneName, Location, Rotation, Scale')

    for socket in sockets:
        if IsASocket(socket):
            SocketName = GetSocketsExportName(socket)

        if socket.parent is None:
            print("Socket ", socket.name, " parent is None!")
            break
        if socket.parent.type != "ARMATURE":  # type: ignore
            print("Socket parent", socket.parent.name, " parent is not and Armature!")
            break

        if socket.parent.bfu_export_deform_only:
            b = bfu_basics.get_first_deform_bone_parent(socket.parent.data.bones[socket.parent_bone])
        else:
            b = socket.parent.data.bones[socket.parent_bone]

        bbpl.anim_utils.reset_armature_pose(socket.parent)
        # GetRelativePosition
        bml: mathutils.Matrix = b.matrix_local  # Bone
        am: mathutils.Matrix = socket.parent.matrix_world  # Armature
        em: mathutils.Matrix = socket.matrix_world  # Socket
        RelativeMatrix = (bml.inverted() @ am.inverted() @ em)
        
        if bfu_skeletal_mesh.bfu_export_procedure.get_object_export_procedure(obj).value == BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value:
            RelativeMatrix = mathutils.Matrix.Rotation(math.radians(90), 4, 'Y') @ RelativeMatrix
            RelativeMatrix = mathutils.Matrix.Rotation(math.radians(-90), 4, 'Z') @ RelativeMatrix
        t = RelativeMatrix.to_translation()
        r = RelativeMatrix.to_euler()
        s = socket.scale*addon_prefs.skeletalSocketsImportedSize

        # Convet to array for Json and convert value for Unreal
        if bfu_skeletal_mesh.bfu_export_procedure.get_object_export_procedure(obj).value == BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value:
            array_location = [t[0], t[1]*-1, t[2]]
            array_rotation = [math.degrees(r[0]), math.degrees(r[1])*-1, math.degrees(r[2])*-1]
            array_scale = [s[0], s[1], s[2]]

        else:
            array_location = [t[0], t[1]*-1, t[2]]
            array_rotation = [math.degrees(r[0]), math.degrees(r[1])*-1, math.degrees(r[2])*-1]
            array_scale = [s[0], s[1], s[2]]

        MySocket = {}
        MySocket["SocketName"] = SocketName
        MySocket["BoneName"] = b.name.replace('.', '_')
        MySocket["Location"] = array_location
        MySocket["Rotation"] = array_rotation
        MySocket["Scale"] = array_scale
        data['Sockets'].append(MySocket)

    return data['Sockets']

def get_all_socket_objs(objs_list=None):
    # Get any socket objects from bpy.context.scene.objects or list if valid.

    if objs_list is not None:
        objs = objs_list
    else:
        objs = bpy.context.scene.objects

    socket_objs = [obj for obj in objs if (
        fnmatch.fnmatchcase(obj.name, "SOCKET*")
        )]
    return socket_objs

def fix_export_type_on_socket(list=None):
    # Corrects bad properties

    if list is not None:
        objs = list
    else:
        objs = get_all_socket_objs()

    fixed_sockets = 0
    for obj in objs:
        if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):
            bfu_export_control.bfu_export_control_utils.set_auto(obj)
            fixed_sockets += 1
    return fixed_sockets

def fix_name_on_socket(list=None):
    # Updates hierarchy names
    if list is not None:
        objs = list
    else:
        objs = get_all_socket_objs()

    fixed_socket_names = 0
    for obj in objs:
        if fnmatch.fnmatchcase(obj.name, "SOCKET*"):
            if obj.type == 'MESH':
                update_length = update_socket_names("ST_Socket", [obj])
                fixed_socket_names += update_length
        if fnmatch.fnmatchcase(obj.name, "SOCKET*"):
            if obj.type == 'ARMATURE':
                update_length = update_socket_names("SKM_Socket", [obj])
                fixed_socket_names += update_length
    return fixed_socket_names
    
def update_socket_names(SubType, objList):
    # Update socket names for Unreal Engine.

    update_length = 0
    for obj in objList:
        ownerObj = obj.parent

        if ownerObj is not None:
            if obj != ownerObj:

                # StaticMesh Socket
                if obj.type == 'EMPTY' and SubType == "ST_Socket":
                    if ownerObj.type == 'MESH':
                        if not IsASocket(obj):
                            new_name = bfu_unreal_utils.generate_name_for_unreal_engine("SOCKET_"+obj.name, obj.name)
                            if new_name != obj.name:
                                obj.name = new_name 
                                update_length += 1

                # SkeletalMesh Socket
                if obj.type == 'EMPTY' and SubType == "SKM_Socket":
                    if ownerObj.type == 'ARMATURE':
                        if not IsASocket(obj):
                            new_name = bfu_unreal_utils.generate_name_for_unreal_engine("SOCKET_"+obj.name, obj.name)
                            if new_name != obj.name:
                                obj.name = new_name 
                                update_length += 1
    return update_length

def Ue4SubObj_set(SubType):
    # Convect obj to Unreal Engine Socket

    def DeselectAllWithoutActive():
        for obj in bpy.context.selected_objects:
            if obj != bpy.context.active_object:
                obj.select_set(False)

    ownerObj = bpy.context.active_object
    objList = bpy.context.selected_objects
    if ownerObj is None:
        return []

    ConvertedObjs = []

    for obj in objList:
        DeselectAllWithoutActive()
        obj.select_set(True)
        if obj != ownerObj:

            # StaticMesh Socket
            if obj.type == 'EMPTY' and SubType == "ST_Socket":
                if ownerObj.type == 'MESH':
                    if IsASocket(obj):
                        obj.name = bfu_unreal_utils.generate_name_for_unreal_engine(obj.name, obj.name)
                    else:
                        obj.name = bfu_unreal_utils.generate_name_for_unreal_engine("SOCKET_"+obj.name, obj.name)
                    bpy.ops.object.parent_set(type='OBJECT',keep_transform=True)
                    ConvertedObjs.append(obj)

            # SkeletalMesh Socket
            if obj.type == 'EMPTY' and SubType == "SKM_Socket":
                if ownerObj.type == 'ARMATURE':

                    if IsASocket(obj):
                        obj.name = bfu_unreal_utils.generate_name_for_unreal_engine(obj.name, obj.name)
                    else:
                        obj.name = bfu_unreal_utils.generate_name_for_unreal_engine("SOCKET_"+obj.name, obj.name)
                    bpy.ops.object.parent_set(type='BONE',keep_transform=True)
                    ConvertedObjs.append(obj)

    DeselectAllWithoutActive()
    for obj in objList:
        obj.select_set(True)  # Resets previous selected object
    return ConvertedObjs


def GetImportSkeletalMeshSocketScriptCommand(obj):

    if obj:
        if obj.type == "ARMATURE":
            sockets = get_skeletal_mesh_sockets(obj)
            t = "SocketCopyPasteBuffer" + "\n"
            t += "NumSockets=" + str(len(sockets)) + "\n"
            t += "IsOnSkeleton=1" + "\n"
            for socket in sockets:
                t += "Begin Object Class=/Script/Engine.SkeletalMeshSocket" + "\n"
                t += "\t" + 'SocketName="' + socket["SocketName"] + '"' + "\n"
                t += "\t" + 'BoneName="' + socket["BoneName"] + '"' + "\n"
                loc = socket["Location"]
                r = socket["Rotation"]
                s = socket["Scale"]
                t += "\t" + 'RelativeLocation=' + "(X="+str(loc[0])+",Y="+str(loc[1])+",Z="+str(loc[2])+")" + "\n"
                t += "\t" + 'RelativeRotation=' + "(Pitch="+str(r[1])+",Yaw="+str(r[2])+",Roll="+str(r[0])+")" + "\n"
                t += "\t" + 'RelativeScale=' + "(X="+str(s[0])+",Y="+str(s[1])+",Z="+str(s[2])+")" + "\n"
                t += "End Object" + "\n"
            return t
    return "Please select an armature."