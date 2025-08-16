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
from .. import bfu_basics
from .. import bbpl
from . import bfu_socket_utils

class BFU_OT_ConvertToStaticSocketButton(bpy.types.Operator):
    bl_label = "Convert to StaticMesh socket"
    bl_idname = "object.converttostaticsocket"
    bl_description = (
        "Convert selected Empty(s) to Unreal sockets" +
        " ready for export (StaticMesh)")

    def execute(self, context):
        ConvertedObj = bfu_socket_utils.Ue4SubObj_set("ST_Socket")
        if len(ConvertedObj) > 0:
            self.report({'INFO'}, str(len(ConvertedObj)) + " object(s) of the selection have be converted to UE Socket. (Static)")
        else:
            self.report({'WARNING'}, "Please select two objects. (Active mesh object is the owner of the socket)")
        return {'FINISHED'}

class BFU_OT_ConvertToSkeletalSocketButton(bpy.types.Operator):
    bl_label = "Convert to SkeletalMesh socket"
    bl_idname = "object.converttoskeletalsocket"
    bl_description = (
        "Convert selected Empty(s)" +
        " to Unreal sockets ready for export (SkeletalMesh)")

    def execute(self, context):
        ConvertedObj = bfu_socket_utils.Ue4SubObj_set("SKM_Socket")
        if len(ConvertedObj) > 0:
            self.report({'INFO'}, str(len(ConvertedObj)) + " object(s) of the selection have be converted to UE Socket. (Skeletal)")
        else:
            self.report({'WARNING'}, "Please select two objects. (Active armature object is the owner of the socket)")
        return {'FINISHED'}

class BFU_OT_CopySkeletalSocketButton(bpy.types.Operator):
    bl_label = "Copy Skeletal Mesh socket for Unreal"
    bl_idname = "object.copy_skeletalsocket_command"
    bl_description = "Copy Skeletal Socket Script command"

    def execute(self, context):
        obj = context.object
        if obj:
            if obj.type == "ARMATURE":
                bfu_basics.set_windows_clipboard(bfu_socket_utils.GetImportSkeletalMeshSocketScriptCommand(obj))
                self.report(
                    {'INFO'},
                    "Skeletal sockets copied. Paste in Unreal Engine Skeletal Mesh assets for import sockets. (Ctrl+V)")
        return {'FINISHED'}
        

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_ConvertToStaticSocketButton,
    BFU_OT_ConvertToSkeletalSocketButton,
    BFU_OT_CopySkeletalSocketButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_tools_socket_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Socket")

    bpy.types.Object.bfu_use_socket_custom_Name = bpy.props.BoolProperty(
        name="Socket custom name",
        description='Use a custom name in Unreal Engine for this socket?',
        default=False
        )

    bpy.types.Object.bfu_socket_custom_Name = bpy.props.StringProperty(
        name="",
        description='',
        default="MySocket"
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_socket_custom_Name
    del bpy.types.Object.bfu_use_socket_custom_Name

    del bpy.types.Scene.bfu_tools_socket_properties_expanded