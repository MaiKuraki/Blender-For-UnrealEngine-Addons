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
from . import bfu_collision_utils
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl

class BFU_OT_ConvertToCollisionButtonBox(bpy.types.Operator):
    bl_label = "Convert to box (UBX)"
    bl_idname = "object.converttoboxcollision"
    bl_description = (
        "Convert selected mesh(es) to Unreal" +
        " collision ready for export (Boxes type)")

    def execute(self, context):
        ConvertedObj = bfu_collision_utils.unreal_engine_sub_objs_set("Box")
        if len(ConvertedObj) > 0:
            self.report(
                {'INFO'},
                str(len(ConvertedObj)) +
                " object(s) of the selection have be" +
                " converted to UE4 Box collisions.")
        else:
            self.report(
                {'WARNING'},
                "Please select two objects." +
                " (Active object is the owner of the collision)")
        return {'FINISHED'}

class BFU_OT_ConvertToCollisionButtonCapsule(bpy.types.Operator):
    bl_label = "Convert to capsule (UCP)"
    bl_idname = "object.converttocapsulecollision"
    bl_description = (
        "Convert selected mesh(es) to Unreal collision" +
        " ready for export (Capsules type)")

    def execute(self, context):
        ConvertedObj = bfu_collision_utils.unreal_engine_sub_objs_set("Capsule")
        if len(ConvertedObj) > 0:
            self.report(
                {'INFO'},
                str(len(ConvertedObj)) +
                " object(s) of the selection have be converted" +
                " to UE4 Capsule collisions.")
        else:
            self.report(
                {'WARNING'},
                "Please select two objects." +
                " (Active object is the owner of the collision)")
        return {'FINISHED'}

class BFU_OT_ConvertToCollisionButtonSphere(bpy.types.Operator):
    bl_label = "Convert to sphere (USP)"
    bl_idname = "object.converttospherecollision"
    bl_description = (
        "Convert selected mesh(es)" +
        " to Unreal collision ready for export (Spheres type)")

    def execute(self, context):
        ConvertedObj = bfu_collision_utils.unreal_engine_sub_objs_set("Sphere")
        if len(ConvertedObj) > 0:
            self.report(
                {'INFO'},
                str(len(ConvertedObj)) +
                " object(s) of the selection have" +
                " be converted to UE4 Sphere collisions.")
        else:
            self.report(
                {'WARNING'},
                "Please select two objects." +
                " (Active object is the owner of the collision)")
        return {'FINISHED'}

class BFU_OT_ConvertToCollisionButtonConvex(bpy.types.Operator):
    bl_label = "Convert to convex shape (UCX)"
    bl_idname = "object.converttoconvexcollision"
    bl_description = (
        "Convert selected mesh(es) to Unreal" +
        " collision ready for export (Convex shapes type)")

    def execute(self, context):
        ConvertedObj = bfu_collision_utils.unreal_engine_sub_objs_set("Convex")
        if len(ConvertedObj) > 0:
            self.report(
                {'INFO'},
                str(len(ConvertedObj)) +
                " object(s) of the selection have be" +
                " converted to UE4 Convex Shape collisions.")
        else:
            self.report(
                {'WARNING'},
                "Please select two objects." +
                " (Active object is the owner of the collision)")
        return {'FINISHED'}
    
class BFU_OT_ToggleCollisionVisibility(bpy.types.Operator):
    bl_label = "Toggle Collision Visibility"
    bl_idname = "object.toggle_collision_visibility"
    bl_description = "Toggle the visibility of all collision objects in the scene"

    def execute(self, context):
        visibility_states = [obj.hide_viewport for obj in bpy.context.scene.objects if obj.name.startswith(("UCX_", "UBX_", "USP_", "UCP_"))]
        new_visibility = not all(visibility_states) if visibility_states else True

        for obj in bpy.context.scene.objects:
            if obj.name.startswith(("UCX_", "UBX_", "USP_", "UCP_")):
                obj.hide_viewport = new_visibility

        return {'FINISHED'}


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_ConvertToCollisionButtonBox,
    BFU_OT_ConvertToCollisionButtonCapsule,
    BFU_OT_ConvertToCollisionButtonSphere,
    BFU_OT_ConvertToCollisionButtonConvex,
    BFU_OT_ToggleCollisionVisibility,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
