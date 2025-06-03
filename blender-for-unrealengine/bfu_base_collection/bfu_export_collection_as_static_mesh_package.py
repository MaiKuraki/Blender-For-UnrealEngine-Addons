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
from typing import Optional
from .. import bfu_export
from .. import bbpl
from .. import bfu_utils
from .. import bfu_vertex_color
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport, AssetPackage
from .. import bfu_export_logs

def process_collection_as_static_mesh_export_from_package(
    op: bpy.types.Operator,
    package: AssetPackage
) -> bool:

    return export_collection_as_static_mesh(
        op,
        fullpath=package.file.get_full_path(),
        col=package.collection
    )


def export_collection_as_static_mesh(
    op: bpy.types.Operator,
    fullpath: str,
    col: bpy.types.Collection
) -> bool:

    '''
    #####################################################
            # COLLECTION AS STATIC MESH
    #####################################################
    '''
    # Export a single collection
    prepare_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Prepare export", 2)
    scene = bpy.context.scene
    bbpl.utils.safe_mode_set('OBJECT')

    bfu_utils.SelectCollectionObjects(col)
    duplicate_data = bfu_export.bfu_export_utils.DuplicateSelectForExport()
    bfu_export.bfu_export_utils.SetDuplicateNameForExport(duplicate_data)

    bfu_export.bfu_export_utils.ConvertSelectedToMesh()
    bfu_export.bfu_export_utils.MakeSelectVisualReal()

    bfu_utils.ApplyNeededModifierToSelect()
    for selected_obj in bpy.context.selected_objects:
        if selected_obj.bfu_convert_geometry_node_attribute_to_uv:
            attrib_name = selected_obj.bfu_convert_geometry_node_attribute_to_uv_name
            bfu_export.bfu_export_utils.ConvertGeometryNodeAttributeToUV(selected_obj, attrib_name)
        bfu_vertex_color.bfu_vertex_color_utils.SetVertexColorForUnrealExport(selected_obj)
        bfu_export.bfu_export_utils.CorrectExtremUVAtExport(selected_obj)
        bfu_export.bfu_export_utils.SetSocketsExportTransform(selected_obj)
        bfu_export.bfu_export_utils.SetSocketsExportName(selected_obj)

    static_collection_export_procedure = col.bfu_collection_export_procedure

    save_use_simplify = bbpl.utils.SaveUserRenderSimplify()
    scene.render.use_simplify = False
    prepare_export_time_log.end_time_log()

    process_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Process export", 2)
    if (static_collection_export_procedure == "ue-standard"):
        bfu_export.bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            operator=op,
            context=bpy.context,
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            global_scale=1,
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(obj),
            use_custom_props=obj.bfu_fbx_export_with_custom_props,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            # use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=False,
            use_metadata=obj.bfu_export_with_meta_data,
            # primary_bone_axis=bfu_export_utils.get_final_export_primary_bone_axis(obj),
            # secondary_bone_axis=bfu_export_utils.get_final_export_secondary_bone_axis(obj),
            # use_space_transform=bfu_export_utils.get_export_use_space_transform(obj),
            # axis_forward=bfu_export_utils.get_export_axis_forward(obj),
            # axis_up=bfu_export_utils.get_export_axis_up(obj),
            bake_space_transform=False
            )
        
    elif (static_collection_export_procedure == "blender-standard"):
        bfu_export.bfu_fbx_export.export_scene_fbx(
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            global_scale=1,
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            #colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(obj), @TODO
            #use_custom_props=obj.bfu_fbx_export_with_custom_props, @TODO
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            # use_armature_deform_only=active.bfu_export_deform_only,
            bake_anim=False,
            #use_metadata=obj.bfu_export_with_meta_data, @TODO
            # use_space_transform=bfu_export_utils.get_export_use_space_transform(obj),
            # axis_forward=bfu_export_utils.get_export_axis_forward(obj),
            # axis_up=bfu_export_utils.get_export_axis_up(obj),
            bake_space_transform=False
            )
    process_export_time_log.end_time_log()

    post_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Clean after export", 2)
    save_use_simplify.LoadUserRenderSimplify()
    for obj in bpy.context.selected_objects:
        bfu_vertex_color.bfu_vertex_color_utils.ClearVertexColorForUnrealExport(obj)
        bfu_export.bfu_export_utils.ResetSocketsExportName(obj)
        bfu_export.bfu_export_utils.ResetSocketsTransform(obj)

    bfu_utils.CleanDeleteObjects(bpy.context.selected_objects)
    for data in duplicate_data.data_to_remove:
        data.RemoveData()

    bfu_export.bfu_export_utils.ResetDuplicateNameAfterExport(duplicate_data)

    for obj in scene.objects:
        bfu_utils.ClearAllBFUTempVars(obj)
    post_export_time_log.end_time_log()
    return True