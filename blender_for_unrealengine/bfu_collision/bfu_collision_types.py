# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


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
