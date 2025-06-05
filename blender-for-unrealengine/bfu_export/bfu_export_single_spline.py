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
from .. import bfu_spline
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_export_logs
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport
from .. import bfu_cached_assets

def process_spline_export_from_asset(
    op: bpy.types.Operator,
    asset: AssetToExport,
    pre_bake_spline: 'bfu_spline.bfu_spline_data.BFU_SplinesList' = None
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:

    obj = asset.obj
    my_asset_log = process_spline_export(op, obj, pre_bake_spline)
    my_asset_log.unreal_target_import_path = asset.import_dirpath
    return my_asset_log


def process_spline_export(
    op: bpy.types.Operator,
    obj: bpy.types.Object,
    pre_bake_spline: 'bfu_spline.bfu_spline_data.BFU_SplinesList' = None
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:

    init_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Init export", 2)
    init_export_time_log.should_print_log = True
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()

    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
    asset_type = asset_class.get_asset_type(obj)
    dirpath = asset_class.get_package_export_directory_path(obj, "", True)
    file_name = asset_class.get_package_file_name(obj, obj.name, "")
    file_name_at = asset_class.get_package_file_name(obj, obj.name+"_AdditionalTrack", "") 

    my_asset_log = bfu_export_logs.bfu_asset_export_logs_utils.create_new_asset_log()
    my_asset_log.object = obj
    my_asset_log.asset_name = obj.name
    my_asset_log.asset_global_scale = obj.bfu_export_global_scale
    my_asset_log.asset_type = asset_type.get_type_as_string()
    my_asset_log.animation_start_frame = scene.frame_start
    my_asset_log.animation_end_frame = scene.frame_end+1
    file = my_asset_log.add_new_file()

    fullpath = bfu_export_utils.check_and_make_export_path(dirpath, file.GetFileWithExtension())
    init_export_time_log.end_time_log()
    if fullpath:
        my_asset_log.StartAssetExport()

        if obj.bfu_export_fbx_spline:
            file.file_name = file_name
            file.file_extension = "fbx"
            file.file_path = dirpath
            file.file_type = "FBX"

            export_single_fbx_spline(op, dirpath, file.GetFileWithExtension(), obj)

        if scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts:
            file.file_name = file_name_at
            file.file_extension = "json"
            file.file_path = dirpath
            file.file_type = "AdditionalTrack"
            bfu_spline.bfu_spline_export_utils.ExportSingleAdditionalTrackSpline(dirpath, file.GetFileWithExtension(), obj, pre_bake_spline)

        my_asset_log.EndAssetExport(True)
    return my_asset_log


def export_single_fbx_spline(
    op: bpy.types.Operator,
    fullpath: str,
    obj: bpy.types.Object
) -> None:

    '''
    #####################################################
            #CAMERA
    #####################################################
    '''
    # Export single spline

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()

    filename = bfu_basics.valid_file_name(filename)
    if obj.type != 'CAMERA':
        return

    bbpl.utils.safe_mode_set('OBJECT')

    # Select and rescale spline for export
    bpy.ops.object.select_all(action='DESELECT')
    bbpl.utils.select_specific_object(obj)

    obj.delta_scale *= 0.01
    if obj.animation_data is not None:
        action = obj.animation_data.action
        frame_range = bfu_utils.get_desired_action_start_end_range(obj, action)
        scene.frame_start = frame_range[0]
        scene.frame_end = frame_range[1] + 1

    export_fbx_spline = obj.bfu_export_fbx_spline
    spline_export_procedure = obj.bfu_spline_export_procedure

    save_use_simplify = bbpl.utils.SaveUserRenderSimplify()
    scene.render.use_simplify = False

    if (spline_export_procedure == "ue-standard") and export_fbx_spline:
        bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            op,
            bpy.context,
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            global_matrix=bfu_export_utils.get_static_axis_conversion(obj),
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(obj),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'CAMERA'},
            use_custom_props=obj.bfu_fbx_export_with_custom_props,
            add_leaf_bones=False,
            use_armature_deform_only=obj.bfu_export_deform_only,
            bake_anim=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=bfu_utils.GetAnimSample(obj),
            bake_anim_simplify_factor=obj.bfu_simplify_anim_for_export,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=obj.bfu_export_with_meta_data,
            mirror_symmetry_right_side_bones=obj.bfu_mirror_symmetry_right_side_bones,
            use_ue_mannequin_bone_alignment=obj.bfu_use_ue_mannequin_bone_alignment,
            disable_free_scale_animation=obj.bfu_disable_free_scale_animation,
            use_space_transform=bfu_export_utils.get_static_fbx_export_use_space_transform(obj),
            axis_forward=bfu_export_utils.get_static_fbx_export_axis_forward(obj),
            axis_up=bfu_export_utils.get_static_fbx_export_axis_up(obj),
            bake_space_transform=False
            )
    elif (spline_export_procedure == "blender-standard") and export_fbx_spline:
        bfu_fbx_export.export_scene_fbx(
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(obj),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'CAMERA'},
            use_custom_props=obj.bfu_fbx_export_with_custom_props,
            add_leaf_bones=False,
            use_armature_deform_only=obj.bfu_export_deform_only,
            bake_anim=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=bfu_utils.GetAnimSample(obj),
            bake_anim_simplify_factor=obj.bfu_simplify_anim_for_export,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=obj.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export_utils.get_final_fbx_export_primary_bone_axis(obj),
            secondary_bone_axis=bfu_export_utils.get_final_fbx_export_secondary_bone_axis(obj),
            use_space_transform=bfu_export_utils.get_static_fbx_export_use_space_transform(obj),
            axis_forward=bfu_export_utils.get_static_fbx_export_axis_forward(obj),
            axis_up=bfu_export_utils.get_static_fbx_export_axis_up(obj),
            bake_space_transform=False
            )

    save_use_simplify.LoadUserRenderSimplify()

    # Reset spline scale
    obj.delta_scale *= 100

    for obj in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(obj)
