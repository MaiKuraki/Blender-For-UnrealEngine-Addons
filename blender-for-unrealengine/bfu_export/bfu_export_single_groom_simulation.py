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




def ProcessGroomSimulationExport(obj):
    scene = bpy.context.scene
    
    asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_asset_class(obj)
    dirpath = asset_class.get_obj_export_directory_path(obj, True)
    file_name = asset_class.get_obj_file_name(obj, obj.name, "")
    asset_type = asset_class.get_asset_type_name(obj)

    print("->", dirpath, file_name)

    my_asset_log = bfu_export_logs.bfu_asset_export_logs_utils.create_new_asset_log()
    my_asset_log.object = obj
    my_asset_log.asset_name = obj.name
    my_asset_log.asset_global_scale = obj.bfu_export_global_scale
    my_asset_log.folder_name = obj.bfu_export_folder_name
    my_asset_log.asset_type = asset_type
    my_asset_log.animation_start_frame = scene.frame_start + obj.bfu_anim_action_start_frame_offset
    my_asset_log.animation_end_frame = scene.frame_end + obj.bfu_anim_action_end_frame_offset

    file = my_asset_log.add_new_file()
    file.file_name = file_name
    file.file_extension = "abc"
    file.file_path = dirpath
    file.file_type = "ABC"

    fullpath = bfu_export_utils.check_and_make_export_path(dirpath, file.GetFileWithExtension())
    if fullpath:
        my_asset_log.StartAssetExport()
        ExportSingleGroomSimulation(fullpath, obj)
        my_asset_log.EndAssetExport(True)
    return my_asset_log


def ExportSingleGroomSimulation(
        fullpath,
        obj
        ):

    '''
    #####################################################
            #GROOM SIMULATION
    #####################################################
    '''
    # Export a single groom simulation

    scene = bpy.context.scene
    bbpl.utils.safe_mode_set('OBJECT')

    bfu_utils.SelectParentAndDesiredChilds(obj)

    groom_simulation_export_procedure = obj.bfu_groom_export_procedure

    frame = bpy.context.scene.frame_current = 1
    
    # Export
    if (groom_simulation_export_procedure == "blender-standard"):
        bpy.ops.wm.alembic_export(
            filepath=fullpath,
            check_existing=False,
            selected=True,
            visible_objects_only=True,
            global_scale=1,
            start=frame,
            end=frame,
            uvs=False,
            normals=False,
            vcolors=True
            )



    for obj in scene.objects:
        bfu_utils.ClearAllBFUTempVars(obj)
