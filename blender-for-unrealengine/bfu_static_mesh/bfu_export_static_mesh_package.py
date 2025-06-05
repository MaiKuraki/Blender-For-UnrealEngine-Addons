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
from pathlib import Path
from typing import TYPE_CHECKING
from .. import bfu_export
from .. import bbpl
from .. import bfu_utils
from .. import bfu_vertex_color
from .. import bfu_export_logs
from ..bfu_assets_manager.bfu_asset_manager_type import AssetPackage


def process_static_mesh_export_from_package(
    op: bpy.types.Operator,
    package: AssetPackage
) -> bool:

    if package.file:
        return export_as_static_mesh(
            op,
            fullpath=package.file.get_full_path(),
            objs=package.objects
        )
    else:
        return False

def export_as_static_mesh(
    op: bpy.types.Operator,
    fullpath: Path,
    objs: List[bpy.types.Object]
) -> bool:
    
    '''
    #####################################################
            #STATIC MESH
    #####################################################
    '''
    
    if bpy.context is None:
        return False
    

    # Export a single Mesh
    active = objs[0]
    prepare_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Prepare export", 2)
    scene = bpy.context.scene

    if TYPE_CHECKING:
        class FakeObject(bpy.types.Object):
            bfu_static_export_procedure: str
            bfu_convert_geometry_node_attribute_to_uv: bool
            bfu_convert_geometry_node_attribute_to_uv_name: str
            bfu_fbx_export_with_custom_props: bool
            bfu_export_deform_only: bool
            bfu_export_with_meta_data: bool
            bfu_mirror_symmetry_right_side_bones: bool
            bfu_use_ue_mannequin_bone_alignment: bool
            bfu_disable_free_scale_animation: bool
            bfu_fbx_export_with_custom_props: bool
        active = FakeObject()  # type: ignore

    bbpl.utils.safe_mode_set('OBJECT')
    bbpl.utils.select_specific_object_list(objs[0], objs)
    asset_name = bfu_export.bfu_export_utils.PrepareExportName(objs[0], False)
    duplicate_data = bfu_export.bfu_export_utils.duplicate_select_for_export(bpy.context)
    bfu_export.bfu_export_utils.set_duplicate_name_for_export(duplicate_data)

    bfu_export.bfu_export_utils.ConvertSelectedToMesh()
    bfu_export.bfu_export_utils.MakeSelectVisualReal()

    bfu_utils.ApplyNeededModifierToSelect() 
    for selected_obj in bpy.context.selected_objects:
        if selected_obj.bfu_convert_geometry_node_attribute_to_uv:  # type: ignore
            attrib_name: str = selected_obj.bfu_convert_geometry_node_attribute_to_uv_name  # type: ignore
            bfu_export.bfu_export_utils.ConvertGeometryNodeAttributeToUV(selected_obj, attrib_name)  # type: ignore
        bfu_vertex_color.bfu_vertex_color_utils.SetVertexColorForUnrealExport(selected_obj)
        bfu_export.bfu_export_utils.CorrectExtremUVAtExport(selected_obj)
        bfu_export.bfu_export_utils.SetSocketsExportTransform(selected_obj)
        bfu_export.bfu_export_utils.SetSocketsExportName(selected_obj)

    asset_name.target_object = active
    bfu_utils.ApplyExportTransform(active, "Object")
    asset_name.set_export_name()
    static_export_procedure = active.bfu_static_export_procedure

    save_use_simplify = bbpl.utils.SaveUserRenderSimplify()
    scene.render.use_simplify = False
    prepare_export_time_log.end_time_log()

    process_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Process export", 2)
    if (static_export_procedure == "custom_fbx_export"):
        bfu_export.bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            operator=op,
            context=bpy.context,
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            global_matrix=bfu_export.bfu_export_utils.get_static_axis_conversion(active),
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(active),
            use_custom_props=active.bfu_fbx_export_with_custom_props,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=False,
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
            use_space_transform=bfu_export.bfu_export_utils.get_static_fbx_export_use_space_transform(active),
            axis_forward=bfu_export.bfu_export_utils.get_static_fbx_export_axis_forward(active),
            axis_up=bfu_export.bfu_export_utils.get_static_fbx_export_axis_up(active),
            bake_space_transform=False
            
            )
    elif (static_export_procedure == "standard_fbx"):
        bfu_export.bfu_fbx_export.export_scene_fbx(
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            apply_unit_scale=True,
            global_scale=bfu_utils.GetObjExportScale(active),
            apply_scale_options='FBX_SCALE_NONE',
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(active),
            use_custom_props=active.bfu_fbx_export_with_custom_props,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=False,
            path_mode='AUTO',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=active.bfu_export_with_meta_data,
            use_space_transform=bfu_export.bfu_export_utils.get_static_fbx_export_use_space_transform(active),
            axis_forward=bfu_export.bfu_export_utils.get_static_fbx_export_axis_forward(active),
            axis_up=bfu_export.bfu_export_utils.get_static_fbx_export_axis_up(active),
            bake_space_transform=False
            )
    elif (static_export_procedure == "standard_gltf"):
        bfu_export.bfu_gltf_export.export_scene_gltf(
            filepath=str(fullpath),
            check_existing=False,
            use_selection=True,
            use_armature_deform_only=active.bfu_export_deform_only
            )
    else:
        print(f"Error: The export procedure '{static_export_procedure}' was not found!")
    process_export_time_log.end_time_log()

    post_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Clean after export", 2)
    save_use_simplify.LoadUserRenderSimplify()
    asset_name.ResetNames()

    bfu_vertex_color.bfu_vertex_color_utils.clear_vertex_color_for_unreal_export(active)
    bfu_export.bfu_export_utils.reset_sockets_export_name(active)
    bfu_export.bfu_export_utils.reset_sockets_transform(active)
    bfu_utils.clean_delete_objects(bpy.context.selected_objects)
    for data in duplicate_data.data_to_remove:
        data.RemoveData()

    bfu_export.bfu_export_utils.reset_duplicate_name_after_export(duplicate_data)

    for obj in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(obj)
    post_export_time_log.end_time_log()
    return True