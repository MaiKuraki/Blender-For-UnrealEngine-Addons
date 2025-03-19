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
from .. import bfu_vertex_color
from .. import bfu_check_potential_error
from .. import bfu_export_logs


def ProcessCollectionExport(op, col: bpy.types.Collection):

    addon_prefs = bfu_basics.GetAddonPrefs()
    dirpath = bfu_utils.GetCollectionExportDir(bpy.data.collections[col.name])
    scene = bpy.context.scene

    my_asset_log = bfu_export_logs.bfu_asset_export_logs_utils.create_new_asset_log()
    my_asset_log.asset_name = col.name
    my_asset_log.asset_global_scale = 1.0 #col.bfu_export_global_scale
    my_asset_log.collection = col
    my_asset_log.asset_type = bfu_utils.GetCollectionType(col)
    my_asset_log.folder_name = col.bfu_export_folder_name

    file: bfu_export_logs.bfu_asset_export_logs.BFU_OT_FileExport = my_asset_log.files.add()
    file.file_name = bfu_naming.get_collection_file_name(col, col.name, "")
    file.file_extension = "fbx"
    file.file_path = dirpath
    file.file_type = "FBX"

    fullpath = bfu_export_utils.check_and_make_export_path(dirpath, file.GetFileWithExtension())
    if fullpath:
        my_asset_log.StartAssetExport()
        ExportSingleStaticMeshCollection(op, fullpath, col.name)

        if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
            
            file: bfu_export_logs.bfu_asset_export_logs.BFU_OT_FileExport = my_asset_log.files.add()
            file.file_name = bfu_naming.get_collection_file_name(col, col.name+"_AdditionalTrack", "")
            file.file_extension = "json"
            file.file_path = dirpath
            file.file_type = "AdditionalTrack"
            bfu_export_utils.ExportAdditionalParameter(dirpath, file.GetFileWithExtension(), my_asset_log)

        my_asset_log.EndAssetExport(True)
    return my_asset_log


def ExportSingleStaticMeshCollection(
        op,
        filepath,
        collection_name
        ):

    '''
    #####################################################
            #COLLECTION
    #####################################################
    '''
    # Export a single collection

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    col = bpy.data.collections[collection_name]

    bbpl.utils.safe_mode_set('OBJECT')

    bfu_utils.SelectCollectionObjects(col)
    duplicate_data = bfu_export_utils.DuplicateSelectForExport()
    bfu_export_utils.SetDuplicateNameForExport(duplicate_data)

    bfu_export_utils.ConvertSelectedToMesh()
    bfu_export_utils.MakeSelectVisualReal()

    bfu_utils.ApplyNeededModifierToSelect()
    for selected_obj in bpy.context.selected_objects:
        if selected_obj.bfu_convert_geometry_node_attribute_to_uv:
            attrib_name = selected_obj.bfu_convert_geometry_node_attribute_to_uv_name
            bfu_export_utils.ConvertGeometryNodeAttributeToUV(selected_obj, attrib_name)
        bfu_vertex_color.bfu_vertex_color_utils.SetVertexColorForUnrealExport(selected_obj)
        bfu_export_utils.CorrectExtremUVAtExport(selected_obj)
        bfu_export_utils.SetSocketsExportTransform(selected_obj)
        bfu_export_utils.SetSocketsExportName(selected_obj)

    static_export_procedure = col.bfu_collection_export_procedure

    save_use_simplify = bbpl.utils.SaveUserRenderSimplify()
    scene.render.use_simplify = False
    if (static_export_procedure == "ue-standard"):
        bfu_fbx_export.export_scene_fbx_with_custom_fbx_io(
            operator=op,
            context=bpy.context,
            filepath=filepath,
            check_existing=False,
            use_selection=True,
            global_scale=1,
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(obj),
            use_custom_props=obj.bfu_export_with_custom_props,
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
        
    elif (static_export_procedure == "blender-standard"):
        bfu_fbx_export.export_scene_fbx(
            filepath=filepath,
            check_existing=False,
            use_selection=True,
            global_scale=1,
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
            #colors_type=bfu_vertex_color.bfu_vertex_color_utils.get_export_colors_type(obj), @TODO
            #use_custom_props=obj.bfu_export_with_custom_props, @TODO
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
    
    save_use_simplify.LoadUserRenderSimplify()
    for obj in bpy.context.selected_objects:
        bfu_vertex_color.bfu_vertex_color_utils.ClearVertexColorForUnrealExport(obj)
        bfu_export_utils.ResetSocketsExportName(obj)
        bfu_export_utils.ResetSocketsTransform(obj)

    bfu_utils.CleanDeleteObjects(bpy.context.selected_objects)
    for data in duplicate_data.data_to_remove:
        data.RemoveData()

    bfu_export_utils.ResetDuplicateNameAfterExport(duplicate_data)

    for obj in scene.objects:
        bfu_utils.ClearAllBFUTempVars(obj)


def CleanSingleStaticMeshCollection(obj):
    # Remove the created collection
    bbpl.utils.select_specific_object(obj)
