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
from typing import List, Tuple, TYPE_CHECKING, Optional
from pathlib import Path
from .. import bbpl
from .. import bfu_utils
from ..bfu_export_logs.bfu_process_time_logs_types import SafeTimeGroup
from .. import bfu_skeletal_mesh
from ..bfu_skeletal_mesh.bfu_export_procedure import BFU_SkeletonExportProcedure
from .. import bfu_material
from .. import bfu_addon_prefs
from ..bfu_assets_manager.bfu_asset_manager_type import AssetPackage
from .. import bfu_export
from ..bfu_export.bfu_export_utils import SavedSceneSimplfy


def process_nla_animation_export_from_package(
    op: bpy.types.Operator,
    package: AssetPackage
) -> bool:

    if package.file:
        return process_nla_anim_export(
            op=op,
            fullpath=package.file.get_full_path(),
            armature=package.objects[0],
            mesh_parts=package.objects[1:],
            frame_range=package.frame_range
        )

    else:
        return False


def process_nla_anim_export(
    op: bpy.types.Operator,
    fullpath: Path,
    armature: bpy.types.Object,
    mesh_parts: List[bpy.types.Object],
    frame_range: Optional[Tuple[float, float]]
) -> bool:

    '''
    #####################################################
            #NLA ANIMATION
    #####################################################
    '''

    if bpy.context is None:
        return False

    if not isinstance(armature.data, bpy.types.Armature):
        raise TypeError(f"The armature object is not a valid Armature type! Inputs: armature: {armature.name}")  

    # Export a single NLA Animation
    my_timer_group = SafeTimeGroup()
    my_timer_group.start_timer(f"Prepare export")
    scene = bpy.context.scene
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # [SAVE ASSET DATA]
    # Save asset data before export like transforms, animation data, etc.
    # So can be restored after export.
    saved_simplify: SavedSceneSimplfy = SavedSceneSimplfy()
    saved_selection_names = bfu_export.bfu_export_utils.SavedObjectNames()
    saved_selection_names.save_new_name(armature)
    saved_selection_names.save_new_names(mesh_parts)
    saved_unit_scale = scene.unit_settings.scale_length
    animation_data = bbpl.anim_utils.AnimationManagment()
    animation_data.save_animation_data(armature)
    saved_frame_range: Tuple[int, int] = (scene.frame_start, scene.frame_end)


    # [SELECT AND DUPLICATE] 
    # Select and duplicate objects for export (Export the duplicated objects)
    bbpl.utils.safe_mode_set('OBJECT')
    bbpl.utils.select_specific_object_list(armature, mesh_parts)
    # Deselect sockets because Unreal Engine detect them as bones
    bfu_skeletal_mesh.bfu_skeletal_mesh_utils.deselect_socket(armature) 
    duplicate_data = bfu_export.bfu_export_utils.duplicate_select_for_export(bpy.context, False)
    duplicate_data.set_duplicate_name_for_export()

    # Duplicated active that should be used for export.
    if bpy.context.active_object is None:
        raise ValueError("No active object found after duplicate!")
    active: bpy.types.Object = bpy.context.active_object
    bfu_export.bfu_export_utils.set_duplicated_object_export_name(
        duplicated_obj=active, 
        original_obj=armature, 
        is_skeletal=True
    )

    if TYPE_CHECKING:
        class FakeObject(bpy.types.Object):
            bfu_skeleton_export_procedure: str
            bfu_convert_geometry_node_attribute_to_uv: bool
            bfu_convert_geometry_node_attribute_to_uv_name: str
            bfu_fbx_export_with_custom_props: bool
            bfu_export_deform_only: bool
            bfu_export_with_meta_data: bool
            bfu_mirror_symmetry_right_side_bones: bool
            bfu_use_ue_mannequin_bone_alignment: bool
            bfu_disable_free_scale_animation: bool
            bfu_fbx_export_with_custom_props: bool
            bfu_simplify_anim_for_export: float
            bfu_export_animation_without_mesh: bool
            bfu_export_animation_with_mesh: bool
        active = FakeObject()  # type: ignore

    # [MAKE REAL COPY] 
    # Make objects real to be able to edit before export.
    bfu_export.bfu_export_utils.convert_selected_to_mesh()
    bfu_export.bfu_export_utils.make_select_visual_real()

    # Apply full Non Linear Animation (NLA) data to the active armature.
    animation_data.set_animation_data(active, True)

    if addon_prefs.bakeArmatureAction:
        bfu_export.bfu_export_utils.bake_armature_animation(active, scene.frame_start, scene.frame_end)

    bfu_utils.apply_export_transform(active, "NLA")  # Apply export transform before rescale

    # This will rescale the rig and unit scale to get a root bone egal to 1
    should_rescale_rig = bfu_export.bfu_export_utils.get_should_rescale_skeleton_for_fbx_export(active)
    if should_rescale_rig:
        rrf = bfu_export.bfu_export_utils.get_rescale_rig_factor()  # rigRescaleFactor
        scene.unit_settings.scale_length = 0.01
        my_skeletal_export_scale = bfu_utils.SkeletalExportScale(active)
        my_skeletal_export_scale.apply_skeletal_export_scale(rrf, target_animation_data=animation_data)
        my_action_curve_scale = bfu_utils.ActionCurveScale(rrf*active.scale.z)
        my_action_curve_scale.RescaleForUnrealEngine()
        my_shape_keys_curve_scale = bfu_utils.ShapeKeysCurveScale(rrf)
        my_shape_keys_curve_scale.rescale_for_unreal_engine()
        my_modifiers_data_scale = bfu_utils.ModifiersDataScale(rrf)
        my_modifiers_data_scale.RescaleForUnrealEngine()

        bfu_utils.rescale_select_curve_hooks(1/rrf)
        bbpl.anim_utils.reset_armature_pose(active)
        my_rig_consraints_scale = bfu_utils.RigConsraintScale(active, rrf)
        my_rig_consraints_scale.rescale_rig_consraint_for_unreal_engine()
        bbpl.anim_utils.copy_drivers(armature, active)

    # [PREPARE SCENE FOR EXPORT]
    # Prepare scene for export (frame range, simplefying, etc.)
    if frame_range:
        scene.frame_start = int(frame_range[0])
        scene.frame_end = int(frame_range[1]) + 1
    saved_simplify.unsimplify_scene()

    my_timer_group.end_last_timer()

    # Process export
    my_timer_group.start_timer(f"Process export")
    skeleton_export_procedure: BFU_SkeletonExportProcedure = bfu_skeletal_mesh.bfu_export_procedure.get_object_export_procedure(active)
    if (skeleton_export_procedure.value == BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value):
        bfu_export.bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            operator=op,
            context=bpy.context,
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            animation_only=active.bfu_export_animation_without_mesh,
            global_matrix=bfu_export.bfu_export_utils.get_skeleton_axis_conversion(active),
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'ARMATURE', 'EMPTY', 'MESH'},
            use_custom_props=active.bfu_fbx_export_with_custom_props,
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=bfu_utils.get_anim_sample(active),
            bake_anim_simplify_factor=active.bfu_simplify_anim_for_export,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=active.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export.bfu_export_utils.get_final_fbx_export_primary_bone_axis(active),
            secondary_bone_axis=bfu_export.bfu_export_utils.get_final_fbx_export_secondary_bone_axis(active),
            mirror_symmetry_right_side_bones=active.bfu_mirror_symmetry_right_side_bones,
            use_ue_mannequin_bone_alignment=active.bfu_use_ue_mannequin_bone_alignment,
            disable_free_scale_animation=active.bfu_disable_free_scale_animation,
            use_space_transform=bfu_export.bfu_export_utils.get_skeleton_fbx_export_use_space_transform(active),
            axis_forward=bfu_export.bfu_export_utils.get_skeleton_export_axis_forward(active),
            axis_up=bfu_export.bfu_export_utils.get_skeleton_export_axis_up(active),
            bake_space_transform=False
            )
    elif (skeleton_export_procedure.value == BFU_SkeletonExportProcedure.STANDARD_FBX.value):
        bfu_export.bfu_fbx_export.export_scene_fbx(
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'ARMATURE', 'EMPTY', 'MESH'},
            use_custom_props=active.bfu_fbx_export_with_custom_props,
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=bfu_utils.get_anim_sample(active),
            bake_anim_simplify_factor=active.bfu_simplify_anim_for_export,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=active.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export.bfu_export_utils.get_final_fbx_export_primary_bone_axis(active),
            secondary_bone_axis=bfu_export.bfu_export_utils.get_final_fbx_export_secondary_bone_axis(active),
            use_space_transform=bfu_export.bfu_export_utils.get_skeleton_fbx_export_use_space_transform(active),
            axis_forward=bfu_export.bfu_export_utils.get_skeleton_export_axis_forward(active),
            axis_up=bfu_export.bfu_export_utils.get_skeleton_export_axis_up(active),
            bake_space_transform=False
            )
    elif (skeleton_export_procedure.value == BFU_SkeletonExportProcedure.STANDARD_GLTF.value):
        bpy.ops.export_scene.gltf(
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            export_def_bones=active.bfu_export_deform_only,
            export_materials=bfu_material.bfu_material_utils.get_gltf_export_materials(active, is_animation=True),
            export_image_format=bfu_material.bfu_material_utils.get_gltf_export_textures(active, is_animation=True),
            export_apply = True,
            )
    else:
        print(f"Error: The export procedure '{skeleton_export_procedure}' was not found!")
    my_timer_group.end_last_timer()

    # [RESTORE ASSET DATA]
    # Restore asset data after export like transforms, animation data, etc.
    my_timer_group.start_timer(f"Clean after export")
    scene.unit_settings.scale_length = saved_unit_scale
    saved_selection_names.restore_names()
    saved_simplify.reset_scene()
    animation_data.set_animation_data(armature, copy_nla=True)
    scene.frame_start = saved_frame_range[0]
    scene.frame_end = saved_frame_range[1]


    bbpl.anim_utils.reset_armature_pose(active)
    # scene.frame_start -= active.bfu_anim_action_start_frame_offset
    # scene.frame_end -= active.bfu_anim_action_end_frame_offset

   

    bbpl.anim_utils.reset_armature_pose(armature)

    # This will rescale the rig and unit scale to get a root bone egal to 1
    if should_rescale_rig:
        my_rig_consraints_scale.reset_scale_after_export()  # type: ignore
        my_skeletal_export_scale.ResetSkeletalExportScale()  # type: ignore
        my_action_curve_scale.ResetScaleAfterExport()  # type: ignore
        my_shape_keys_curve_scale.reset_scale_after_export()  # type: ignore
        my_modifiers_data_scale.ResetScaleAfterExport()  # type: ignore

    bfu_utils.clean_delete_objects(bpy.context.selected_objects)
    for data in duplicate_data.data_to_remove:
        data.remove_data()

    duplicate_data.reset_duplicate_name_after_export()

    for obj in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(obj)
    my_timer_group.end_last_timer()
    return True