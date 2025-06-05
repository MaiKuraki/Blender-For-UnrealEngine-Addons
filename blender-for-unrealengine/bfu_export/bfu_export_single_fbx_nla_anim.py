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
from . import bfu_fbx_export
from . import bfu_export_utils
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_naming
from .. import bfu_export_logs
from .. import bfu_skeletal_mesh
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport
from .. import bfu_cached_assets

def process_nla_anim_export_from_asset(
    op: bpy.types.Operator,
    asset: AssetToExport
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:

    armature = asset.obj
    my_asset_log = process_nla_anim_export(op, armature)
    my_asset_log.unreal_target_import_path = asset.import_dirpath
    return my_asset_log


def process_nla_anim_export(
    op: bpy.types.Operator,
    armature: bpy.types.Object
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:

    init_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Init export", 2)
    init_export_time_log.should_print_log = True
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()


    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(armature, "SkeletalAnimation")
    asset_type = asset_class.get_asset_type(armature)
    dirpath = asset_class.get_package_export_directory_path(armature, "", True)

    scene.frame_end += 1  # Why ?

    my_asset_log = bfu_export_logs.bfu_asset_export_logs_utils.create_new_asset_log()
    my_asset_log.object = armature
    my_asset_log.skeleton_name = armature.name
    my_asset_log.asset_name = bfu_naming.get_nonlinear_animation_file_name(armature)
    my_asset_log.asset_global_scale = armature.bfu_export_global_scale
    my_asset_log.asset_type = asset_type.get_type_as_string()
    frame_range = bfu_utils.get_desired_nla_start_end_range(armature)
    my_asset_log.animation_start_frame = frame_range[0]
    my_asset_log.animation_end_frame = frame_range[1]

    file = my_asset_log.add_new_file()
    file.file_name = bfu_naming.get_nonlinear_animation_file_name(armature, "")
    file.file_extension = "fbx"
    file.file_path = dirpath
    file.file_type = "FBX"

    fullpath = bfu_export_utils.check_and_make_export_path(dirpath, file.GetFileWithExtension())
    init_export_time_log.end_time_log()
    if fullpath:
        my_asset_log.StartAssetExport()
        export_single_fbx_nla_anim(op, fullpath, armature)
        my_asset_log.EndAssetExport(True)
    return my_asset_log


def export_single_fbx_nla_anim(
    op: bpy.types.Operator,
    fullpath: str,
    armature: bpy.types.Object
) -> None:

    '''
    #####################################################
            #NLA ANIMATION
    #####################################################
    '''
    # Export a single NLA Animation

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    export_as_proxy = bfu_utils.GetExportAsProxy(armature)
    export_proxy_child = bfu_utils.GetExportProxyChild(armature)

    bbpl.utils.safe_mode_set('OBJECT')

    if armature.bfu_export_animation_without_mesh:
        bfu_skeletal_mesh.bfu_skeletal_mesh_utils.SelectArmatureParentAndDesiredChilds(armature, False, False)
    else:
        bfu_skeletal_mesh.bfu_skeletal_mesh_utils.SelectArmatureParentAndDesiredChilds(armature, True, False)

    bfu_skeletal_mesh.bfu_skeletal_mesh_utils.deselect_socket(armature) 

    asset_name = bfu_export_utils.PrepareExportName(armature, True)
    if export_as_proxy is False:
        duplicate_data = bfu_export_utils.duplicate_select_for_export()
        bfu_export_utils.set_duplicate_name_for_export(duplicate_data)

    if export_as_proxy is False:
        bfu_export_utils.ConvertSelectedToMesh()
        bfu_export_utils.MakeSelectVisualReal()

    saved_base_transforms = bfu_export_utils.SaveTransformObjects(armature)
    active = bpy.context.view_layer.objects.active
    asset_name.target_object = active

    skeleton_export_procedure = active.bfu_skeleton_export_procedure

    animation_data = bbpl.anim_utils.AnimationManagment()
    animation_data.save_animation_data(armature)
    animation_data.set_animation_data(active, True)

    if export_as_proxy:
        bfu_export_utils.ApplyProxyData(active)
        bfu_utils.RemoveSocketFromSelectForProxyArmature()

    if addon_prefs.bakeArmatureAction:
        bfu_export_utils.BakeArmatureAnimation(active, scene.frame_start, scene.frame_end)

    bfu_utils.apply_export_transform(active, "NLA")  # Apply export transform before rescale

    # This will rescale the rig and unit scale to get a root bone egal to 1
    ShouldRescaleRig = bfu_export_utils.GetShouldRescaleRig(active)
    if ShouldRescaleRig:

        rrf = bfu_export_utils.GetRescaleRigFactor()  # rigRescaleFactor
        my_scene_unit_settings = bfu_utils.SceneUnitSettings(bpy.context.scene)
        my_scene_unit_settings.SetUnitForUnrealEngineExport()
        my_skeletal_export_scale = bfu_utils.SkeletalExportScale(active)
        my_skeletal_export_scale.ApplySkeletalExportScale(rrf, target_animation_data=animation_data, is_a_proxy=export_as_proxy)
        my_action_curve_scale = bfu_utils.ActionCurveScale(rrf*active.scale.z)
        my_action_curve_scale.ResacleForUnrealEngine()
        my_shape_keys_curve_scale = bfu_utils.ShapeKeysCurveScale(rrf, is_a_proxy=export_as_proxy)
        my_shape_keys_curve_scale.ResacleForUnrealEngine()
        my_modifiers_data_scale = bfu_utils.ModifiersDataScale(rrf, is_a_proxy=export_as_proxy)
        my_modifiers_data_scale.ResacleForUnrealEngine()

        bfu_utils.RescaleSelectCurveHook(1/rrf)
        bbpl.anim_utils.reset_armature_pose(active)
        my_rig_consraints_scale = bfu_utils.RigConsraintScale(active, rrf)
        my_rig_consraints_scale.RescaleRigConsraintForUnrealEngine()
        bbpl.anim_utils.copy_drivers(armature, active)

    frame_range = bfu_utils.get_desired_nla_start_end_range(active)
    scene.frame_start = frame_range[0]
    scene.frame_end = frame_range[1] + 1

    asset_name.set_export_name()

    if (skeleton_export_procedure == "ue-standard"):
        bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            operator=op,
            context=bpy.context,
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            animation_only=active.bfu_export_animation_without_mesh,
            global_matrix=bfu_export_utils.get_skeleton_axis_conversion(active),
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'ARMATURE', 'EMPTY', 'MESH'},
            use_custom_props=armature.bfu_fbx_export_with_custom_props,
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=bfu_utils.GetAnimSample(active),
            bake_anim_simplify_factor=active.bfu_simplify_anim_for_export,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=armature.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export_utils.get_final_fbx_export_primary_bone_axis(armature),
            secondary_bone_axis=bfu_export_utils.get_final_fbx_export_secondary_bone_axis(armature),
            mirror_symmetry_right_side_bones=active.bfu_mirror_symmetry_right_side_bones,
            use_ue_mannequin_bone_alignment=active.bfu_use_ue_mannequin_bone_alignment,
            disable_free_scale_animation=active.bfu_disable_free_scale_animation,
            use_space_transform=bfu_export_utils.get_skeleton_fbx_export_use_space_transform(armature),
            axis_forward=bfu_export_utils.get_skeleton_export_axis_forward(armature),
            axis_up=bfu_export_utils.get_skeleton_export_axis_up(armature),
            bake_space_transform=False
            )
    elif (skeleton_export_procedure == "blender-standard"):
        bfu_fbx_export.export_scene_fbx(
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'ARMATURE', 'EMPTY', 'MESH'},
            use_custom_props=armature.bfu_fbx_export_with_custom_props,
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=bfu_utils.GetAnimSample(active),
            bake_anim_simplify_factor=active.bfu_simplify_anim_for_export,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=armature.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export_utils.get_final_fbx_export_primary_bone_axis(armature),
            secondary_bone_axis=bfu_export_utils.get_final_fbx_export_secondary_bone_axis(armature),
            use_space_transform=bfu_export_utils.get_skeleton_fbx_export_use_space_transform(armature),
            axis_forward=bfu_export_utils.get_skeleton_export_axis_forward(armature),
            axis_up=bfu_export_utils.get_skeleton_export_axis_up(armature),
            bake_space_transform=False
            )

    bbpl.anim_utils.reset_armature_pose(active)
    # scene.frame_start -= active.bfu_anim_action_start_frame_offset
    # scene.frame_end -= active.bfu_anim_action_end_frame_offset

    asset_name.ResetNames()

    bbpl.anim_utils.reset_armature_pose(armature)

    # This will rescale the rig and unit scale to get a root bone egal to 1
    if ShouldRescaleRig:
        my_rig_consraints_scale.ResetScaleAfterExport()
        my_skeletal_export_scale.ResetSkeletalExportScale()
        my_scene_unit_settings.ResetUnit()
        my_action_curve_scale.ResetScaleAfterExport()
        my_shape_keys_curve_scale.ResetScaleAfterExport()
        my_modifiers_data_scale.ResetScaleAfterExport()

    # Reset Transform
    saved_base_transforms.reset_object_transforms()

    if export_as_proxy is False:
        bfu_utils.clean_delete_objects(bpy.context.selected_objects)
        for data in duplicate_data.data_to_remove:
            data.RemoveData()

        bfu_export_utils.ResetDuplicateNameAfterExport(duplicate_data)

    for armature in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(armature)
