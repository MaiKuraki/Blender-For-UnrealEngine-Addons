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
from . import bfu_export_utils
from .. import bbpl
from .. import bfu_utils
from .. import bfu_naming
from .. import bfu_export_logs
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport
from .. import bfu_cached_assets

def process_alembic_animation_export_from_asset(
    op: bpy.types.Operator,
    asset: AssetToExport
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:

    obj = asset.obj
    my_asset_log = process_alembic_animation_export(op, obj)
    my_asset_log.unreal_target_import_path = asset.import_dirpath
    return my_asset_log


def process_alembic_animation_export(
    op: bpy.types.Operator,
    obj: bpy.types.Object
) -> bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog:
    
    init_export_time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log(f"Init export", 2)
    init_export_time_log.should_print_log = True
    scene = bpy.context.scene
    
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
    asset_type = asset_class.get_asset_type(obj)
    dirpath = asset_class.get_package_export_directory_path(obj, "", True)
    file_name = asset_class.get_package_file_name(obj, obj.name, "")

    my_asset_log = bfu_export_logs.bfu_asset_export_logs_utils.create_new_asset_log()
    my_asset_log.object = obj
    my_asset_log.asset_name = obj.name
    my_asset_log.asset_global_scale = obj.bfu_export_global_scale
    my_asset_log.asset_type = asset_type.get_type_as_string()
    my_asset_log.animation_start_frame = scene.frame_start + obj.bfu_anim_action_start_frame_offset
    my_asset_log.animation_end_frame = scene.frame_end + obj.bfu_anim_action_end_frame_offset

    file = my_asset_log.add_new_file()
    file.file_name = file_name
    file.file_extension = "abc"
    file.file_path = dirpath
    file.file_type = "ABC"

    fullpath = bfu_export_utils.check_and_make_export_path(dirpath, file.GetFileWithExtension())
    init_export_time_log.end_time_log()
    if fullpath:
        my_asset_log.StartAssetExport()
        export_single_alembic_animation(fullpath, obj)
        my_asset_log.EndAssetExport(True)
    return my_asset_log


def export_single_alembic_animation(
    fullpath: str,
    obj: bpy.types.Object
) -> None:

    '''
    #####################################################
            #ALEMBIC ANIMATION
    #####################################################
    '''
    # Export a single alembic animation

    scene = bpy.context.scene
    bbpl.utils.safe_mode_set('OBJECT')

    bfu_utils.SelectParentAndDesiredChilds(obj)

    scene.frame_start += obj.bfu_anim_action_start_frame_offset
    scene.frame_end += obj.bfu_anim_action_end_frame_offset

    alembic_animation_export_procedure = obj.bfu_alembic_export_procedure

    # Export
    if (alembic_animation_export_procedure == "blender-standard"):
        bpy.ops.wm.alembic_export(
            filepath=fullpath,
            check_existing=False,
            selected=True,
            triangulate=True,
            global_scale=1,
            )

    scene.frame_start -= obj.bfu_anim_action_start_frame_offset
    scene.frame_end -= obj.bfu_anim_action_end_frame_offset

    for obj in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(obj)
