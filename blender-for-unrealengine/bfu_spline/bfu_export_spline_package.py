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
from pathlib import Path
from typing import TYPE_CHECKING
from .. import bbpl
from .. import bfu_utils
from ..bfu_assets_manager.bfu_asset_manager_type import AssetPackage
from ..bfu_export_logs.bfu_process_time_logs_types import SafeTimeGroup
from .. import bfu_export
from ..bfu_export.bfu_export_utils import SavedSceneSimplfy
from .. import bfu_skeletal_mesh
from ..bfu_skeletal_mesh.bfu_export_procedure import BFU_SkeletonExportProcedure


def process_spline_export_from_package(
    op: bpy.types.Operator,
    package: AssetPackage,
) -> bool:

    if package.file and package.objects:
        return export_single_fbx_spline(
            op=op,
            fullpath=package.file.get_full_path(),
            obj=package.objects[0]
        )
    else:
        return False


def export_single_fbx_spline(
    op: bpy.types.Operator,
    fullpath: Path,
    obj: bpy.types.Object
) -> bool:

    '''
    #####################################################
            #CAMERA
    #####################################################
    '''

    if bpy.context is None:
        return False

    # Export single spline
    my_timer_group = SafeTimeGroup()
    my_timer_group.start_timer(f"Prepare export")
    scene = bpy.context.scene

    # [SAVE ASSET DATA]
    # Save asset data before export like transforms, animation data, etc.
    # So can be restored after export.
    saved_simplify: SavedSceneSimplfy = SavedSceneSimplfy()
    saved_selection_names = bfu_export.bfu_export_utils.SavedObjectNames()
    saved_selection_names.save_new_name(obj)
    saved_base_transforms = bfu_export.bfu_export_utils.SaveTransformObjects(obj)


    # [SELECT ONLY] 
    # Select objects for export
    bbpl.utils.safe_mode_set('OBJECT')
    bbpl.utils.select_specific_object(obj)

    # Selected active that should be used for export.
    if bpy.context.active_object is None:
        raise ValueError("No active object found after duplicate!")
    active: bpy.types.Object = bpy.context.active_object
    bfu_export.bfu_export_utils.set_object_export_name(obj=active, is_skeletal=False)

    if TYPE_CHECKING:
        class FakeObject(bpy.types.Object):
            bfu_spline_export_procedure: str
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
        active = FakeObject()  # type: ignore

    bfu_utils.apply_export_transform(active, "Object")

    # [PREPARE SCENE FOR EXPORT]
    # Prepare scene for export (frame range, simplefying, etc.)
    saved_simplify.unsymplify_scene()

    my_timer_group.end_last_timer()

    # Process export
    my_timer_group.start_timer(f"Process export")
    spline_export_procedure: BFU_SkeletonExportProcedure = bfu_skeletal_mesh.bfu_export_procedure.get_object_export_procedure(active)
    if (spline_export_procedure.value == BFU_SkeletonExportProcedure.CUSTOM_FBX_EXPORT.value):
        bfu_export.bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            op,
            bpy.context,
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            global_matrix=bfu_export.bfu_export_utils.get_static_axis_conversion(active),
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'CAMERA'},
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
            mirror_symmetry_right_side_bones=active.bfu_mirror_symmetry_right_side_bones,
            use_ue_mannequin_bone_alignment=active.bfu_use_ue_mannequin_bone_alignment,
            disable_free_scale_animation=active.bfu_disable_free_scale_animation,
            use_space_transform=bfu_export.bfu_export_utils.get_static_fbx_export_use_space_transform(active),
            axis_forward=bfu_export.bfu_export_utils.get_static_fbx_export_axis_forward(active),
            axis_up=bfu_export.bfu_export_utils.get_static_fbx_export_axis_up(active),
            bake_space_transform=False
            )
    elif (spline_export_procedure.value == BFU_SkeletonExportProcedure.STANDARD_FBX.value):
        bfu_export.bfu_fbx_export.export_scene_fbx(
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'CAMERA'},
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
            use_space_transform=bfu_export.bfu_export_utils.get_static_fbx_export_use_space_transform(active),
            axis_forward=bfu_export.bfu_export_utils.get_static_fbx_export_axis_forward(active),
            axis_up=bfu_export.bfu_export_utils.get_static_fbx_export_axis_up(active),
            bake_space_transform=False
            )
    elif (spline_export_procedure.value == BFU_SkeletonExportProcedure.STANDARD_GLTF.value):
        # @TODO: Implement GLTF export for spline
        bfu_export.bfu_gltf_export.export_scene_gltf()
    else:
        print(f"Error: The export procedure '{spline_export_procedure}' was not found!")
    my_timer_group.end_last_timer()

    # [RESTORE ASSET DATA]
    # Restore asset data after export like transforms, animation data, etc.
    my_timer_group.start_timer(f"Clean after export")
    saved_base_transforms.reset_object_transforms()
    saved_selection_names.restore_names()
    saved_simplify.reset_scene()

    for obj in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(obj)
    my_timer_group.end_last_timer()
    return True