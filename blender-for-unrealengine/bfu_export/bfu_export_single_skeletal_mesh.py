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
from typing import List
from . import bfu_fbx_export
from . import bfu_export_utils
from .. import bbpl
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_export_logs
from .. import bfu_skeletal_mesh
from .. import bfu_vertex_color
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport
from .. import bfu_cached_assets
from .. import bfu_export_procedure


def process_skeletal_mesh_export_from_asset(
    op: bpy.types.Operator, 
    asset: AssetToExport
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:
    
    armature = asset.obj
    mesh_parts = asset.obj_list
    desired_name = asset.name
    desired_dirpath = asset.dirpath

    my_asset_log = process_skeletal_mesh_export(op, armature, mesh_parts, desired_name, desired_dirpath)
    my_asset_log.unreal_target_import_path = asset.import_dirpath
    return my_asset_log

def process_skeletal_mesh_export(
    op: bpy.types.Operator,
    armature: bpy.types.Object,
    mesh_parts: List[bpy.types.Object],
    desired_name: str = "",
    desired_dirpath: str = ""
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:

    init_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Init export", 2)
    init_export_time_log.should_print_log = True
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()

    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(armature)
    asset_type = asset_class.get_asset_type(armature)
    dirpath = desired_dirpath if desired_dirpath else asset_class.get_asset_export_directory_path(armature, "", True)
    final_name = desired_name if desired_name else armature.name

    file_name = asset_class.get_asset_file_name(armature, final_name, "")
    file_name_at = asset_class.get_asset_file_name(armature, final_name+"_AdditionalTrack", "") 

    my_asset_log = bfu_export_logs.bfu_asset_export_logs_utils.create_new_asset_log()
    my_asset_log.object = armature
    my_asset_log.skeleton_name = armature.name
    my_asset_log.asset_name = armature.name
    my_asset_log.asset_global_scale = armature.bfu_export_global_scale
    my_asset_log.asset_type = asset_type.get_type_as_string()

    export_type = bfu_export_procedure.bfu_skeleton_export_procedure.get_obj_export_type(armature)
    if export_type == "FBX":
        file = my_asset_log.add_new_file()
        file.file_name = file_name
        file.file_extension = "fbx"
        file.file_path = dirpath
        file.file_type = "FBX"
    elif export_type == "GLTF":
        file = my_asset_log.add_new_file()
        file.file_name = file_name
        file.file_extension = "glb"
        file.file_path = dirpath
        file.file_type = "GLTF"

    fullpath = bfu_export_utils.check_and_make_export_path(dirpath, file.GetFileWithExtension())
    init_export_time_log.end_time_log()
    if fullpath:
        my_asset_log.StartAssetExport()
        export_single_skeletal_mesh(op, fullpath, armature, mesh_parts)

        if not armature.bfu_export_as_lod_mesh:
            if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
            
                file = my_asset_log.add_new_file()
                file.file_name = file_name_at
                file.file_extension = "json"
                file.file_path = dirpath
                file.file_type = "AdditionalTrack"
                bfu_export_utils.export_additional_data_from_logs(dirpath, file.GetFileWithExtension(), my_asset_log)

        my_asset_log.EndAssetExport(True)
    return my_asset_log


def export_single_skeletal_mesh(
    op: bpy.types.Operator,
    fullpath: str,
    armature: bpy.types.Object,
    mesh_parts: List[bpy.types.Object]
) -> None:

    '''
    #####################################################
            #SKELETAL MESH
    #####################################################
    '''
    # Export a single Mesh

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    export_as_proxy = bfu_utils.GetExportAsProxy(armature)
    export_proxy_child = bfu_utils.GetExportProxyChild(armature)

    bbpl.utils.safe_mode_set('OBJECT')

    bfu_utils.SelectParentAndSpecificChilds(armature, mesh_parts)
    bfu_skeletal_mesh.bfu_skeletal_mesh_utils.deselect_socket(armature) 

    asset_name = bfu_export_utils.PrepareExportName(armature, True)
    duplicate_data = bfu_export_utils.DuplicateSelectForExport()
    bfu_export_utils.SetDuplicateNameForExport(duplicate_data)

    bfu_export_utils.ConvertSelectedToMesh()
    bfu_export_utils.MakeSelectVisualReal()

    bfu_utils.ApplyNeededModifierToSelect()
    for selected_obj in bpy.context.selected_objects:
        if armature.bfu_convert_geometry_node_attribute_to_uv:
            attrib_name = armature.bfu_convert_geometry_node_attribute_to_uv_name
            bfu_export_utils.ConvertGeometryNodeAttributeToUV(selected_obj, attrib_name)
        bfu_vertex_color.bfu_vertex_color_utils.SetVertexColorForUnrealExport(selected_obj)
        bfu_export_utils.CorrectExtremUVAtExport(selected_obj)
        bfu_export_utils.SetSocketsExportTransform(selected_obj)
        bfu_export_utils.SetSocketsExportName(selected_obj)

    saved_base_transforms = bfu_export_utils.SaveTransformObjects(armature)
    active = bpy.context.view_layer.objects.active
    asset_name.target_object = active

    skeleton_export_procedure = active.bfu_skeleton_export_procedure

    if export_as_proxy:
        bfu_export_utils.ApplyProxyData(active)

    bfu_utils.ApplyExportTransform(active, "Object")  # Apply export transform before rescale

    # This will rescale the rig and unit scale to get a root bone egal to 1
    ShouldRescaleRig = bfu_export_utils.GetShouldRescaleRig(active)

    if ShouldRescaleRig:

        rrf = bfu_export_utils.GetRescaleRigFactor()  # rigRescaleFactor
        my_scene_unit_settings = bfu_utils.SceneUnitSettings(bpy.context.scene)
        my_scene_unit_settings.SetUnitForUnrealEngineExport()
        my_skeletal_export_scale = bfu_utils.SkeletalExportScale(active)
        my_skeletal_export_scale.ApplySkeletalExportScale(rrf, is_a_proxy=export_as_proxy)
        my_modifiers_data_scale = bfu_utils.ModifiersDataScale(rrf, is_a_proxy=export_as_proxy)
        my_modifiers_data_scale.ResacleForUnrealEngine()

    # Set rename temporarily the Armature as "Armature"
    bfu_utils.disable_all_bones_consraints(active)
    bpy.context.object.data.pose_position = 'REST'

    bfu_export_utils.ConvertArmatureConstraintToModifiers(active)

    asset_name.SetExportName()

    save_use_simplify = bbpl.utils.SaveUserRenderSimplify()
    scene.render.use_simplify = False

    if (skeleton_export_procedure == "ue-standard"):
        bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            operator=op,
            context=bpy.context,
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            use_active_collection=False,
            global_matrix=bfu_export_utils.get_skeleton_axis_conversion(active),
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={
                'ARMATURE',
                'EMPTY',
                'CAMERA',
                'LIGHT',
                'MESH',
                'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(active),
            use_custom_props=active.bfu_fbx_export_with_custom_props,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            armature_nodetype='NULL',
            bake_anim=False,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=active.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export_utils.get_final_fbx_export_primary_bone_axis(active),
            secondary_bone_axis=bfu_export_utils.get_final_fbx_export_secondary_bone_axis(active),
            mirror_symmetry_right_side_bones=active.bfu_mirror_symmetry_right_side_bones,
            use_ue_mannequin_bone_alignment=active.bfu_use_ue_mannequin_bone_alignment,
            disable_free_scale_animation=active.bfu_disable_free_scale_animation,
            use_space_transform=bfu_export_utils.get_skeleton_fbx_export_use_space_transform(active),
            axis_forward=bfu_export_utils.get_skeleton_export_axis_forward(active),
            axis_up=bfu_export_utils.get_skeleton_export_axis_up(active),
            bake_space_transform=False
            )
    elif (skeleton_export_procedure == "blender-standard"):
        bfu_fbx_export.export_scene_fbx(
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            use_active_collection=False,
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={
                'ARMATURE',
                'EMPTY',
                'CAMERA',
                'LIGHT',
                'MESH',
                'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(active),
            use_custom_props=active.bfu_fbx_export_with_custom_props,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            armature_nodetype='NULL',
            bake_anim=False,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=active.bfu_export_with_meta_data,
            primary_bone_axis=bfu_export_utils.get_final_fbx_export_primary_bone_axis(active),
            secondary_bone_axis=bfu_export_utils.get_final_fbx_export_secondary_bone_axis(active),
            use_space_transform=bfu_export_utils.get_skeleton_fbx_export_use_space_transform(active),
            axis_forward=bfu_export_utils.get_skeleton_export_axis_forward(active),
            axis_up=bfu_export_utils.get_skeleton_export_axis_up(active),
            bake_space_transform=False
            )

    # This will rescale the rig and unit scale to get a root bone egal to 1
    if ShouldRescaleRig:
        # Reset Curve an unit
        my_scene_unit_settings.ResetUnit()
        my_modifiers_data_scale.ResetScaleAfterExport()

    # Reset Transform
    saved_base_transforms.reset_object_transforms()

    save_use_simplify.LoadUserRenderSimplify()
    asset_name.ResetNames()
    bfu_vertex_color.bfu_vertex_color_utils.ClearVertexColorForUnrealExport(active)
    bfu_export_utils.ResetArmatureConstraintToModifiers(active)
    bfu_export_utils.ResetSocketsExportName(active)
    bfu_export_utils.ResetSocketsTransform(active)
    bfu_utils.CleanDeleteObjects(bpy.context.selected_objects)
    for data in duplicate_data.data_to_remove:
        data.RemoveData()

    bfu_export_utils.ResetDuplicateNameAfterExport(duplicate_data)

    for armature in scene.objects:
        bfu_utils.ClearAllBFUTempVars(armature)
