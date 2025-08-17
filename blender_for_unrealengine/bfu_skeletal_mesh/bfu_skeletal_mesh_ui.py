# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bfu_ui
from .. import bbpl
from .. import bfu_export_control
from .. import bfu_skeletal_mesh
from ..bfu_skeletal_mesh.bfu_export_procedure import BFU_SkeletonExportProcedure
from . import bfu_skeletal_mesh_utils


def draw_general_ui_object(layout: bpy.types.UILayout, obj: bpy.types.Object):
    if bpy.context is None:
        return

    if obj is None:
        return
    
    if obj.type != "ARMATURE":
        return
    
    scene = bpy.context.scene 
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_object_properties_expanded")
        if accordion.is_expend():
            if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):
                if not obj.bfu_export_as_alembic_animation:
                    skeletal_mesh_ui = layout.column()
                    # Show asset type
                    skeletal_mesh_ui.prop(obj, "bfu_export_skeletal_mesh_as_static_mesh")

def draw_ui_object(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
    if bpy.context is None:
        return
    
    if obj is None:
        return
    is_skeletal_mesh = bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)
    if obj.type != "ARMATURE":
        return
    if is_skeletal_mesh is False:
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    if obj.bfu_export_as_lod_mesh:
        return
    
    scene = bpy.context.scene 

    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_skeleton_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():

            # SkeletalMesh prop
            AssetType2 = panel.column()

            AssetType2.prop(obj, 'bfu_create_sub_folder_with_skeletal_mesh_name')
            AssetType2.prop(obj, 'bfu_export_deform_only')
            ue_standard_skeleton = panel.column()

            if bfu_skeletal_mesh.bfu_export_procedure.get_object_export_procedure(obj).value == BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value:
                ue_standard_skeleton_props = ue_standard_skeleton.column()
                ue_standard_skeleton_props.prop(obj, "bfu_mirror_symmetry_right_side_bones")
                mirror_symmetry_right_side_bones = ue_standard_skeleton_props.row()
                mirror_symmetry_right_side_bones.enabled = obj.bfu_mirror_symmetry_right_side_bones
                mirror_symmetry_right_side_bones.prop(obj, "bfu_use_ue_mannequin_bone_alignment")

def draw_ui_scene(layout: bpy.types.UILayout):
    pass