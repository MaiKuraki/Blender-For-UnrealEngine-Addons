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

import os
import bpy
import datetime
from shutil import copyfile

from . import bfu_export_text_files_asset_data
from . import bfu_export_text_files_sequencer_data
from . import bfu_export_text_files_utils

from .. import bpl
from .. import bbpl
from .. import languages
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_export_logs


def write_all_data_files():
    time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("Write text files")
    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    root_dirpath = bpy.path.abspath(scene.bfu_export_other_file_path)

    success_export_log = False
    success_asset_data = False
    success_sequencer_data = False
    success_import_script = False
    success_sequencer_script = False

    # Export log
    if scene.bfu_use_text_export_log:
        Text = languages.ti("write_text_additional_track_start") + "\n"
        Text += "" + "\n"
        Text += bfu_export_logs.bfu_asset_export_logs_utils.get_export_asset_logs_details()
        if Text is not None:
            Filename = bfu_basics.ValidFilename(scene.bfu_file_export_log_name)
            export_log_result = bfu_export_text_files_utils.export_single_text_file(Text, root_dirpath, Filename)
            if export_log_result:
                success_export_log = True

    # Import script
    if bpy.app.version >= (4, 2, 0):
        bfu_path = os.path.join(bbpl.blender_extension.extension_utils.get_package_path(), "bfu_import_module")
    else:
        bfu_path = os.path.join(bbpl.blender_addon.addon_utils.get_addon_path("Unreal Engine Assets Exporter"), "bfu_import_module")

    if scene.bfu_use_text_import_asset_script:
        json_data = bfu_export_text_files_asset_data.write_main_assets_data()
        export_asset_data_result = bfu_export_text_files_utils.export_single_json_file(json_data, root_dirpath, "ImportAssetData.json")
        if export_asset_data_result:
            success_asset_data = True

        source = os.path.join(bfu_path, "asset_import_script.py")
        filename = bfu_basics.ValidFilename(scene.bfu_file_import_asset_script_name)
        destination = os.path.join(root_dirpath, filename)
        if bfu_export_text_files_utils.is_read_only(destination):
            print(f"Cannot replace '{destination}': File is read-only.")
            success_import_script = False
        else:
            copyfile(source, destination)
            success_import_script = True

    if scene.bfu_use_text_import_sequence_script:
        json_data = bfu_export_text_files_sequencer_data.write_sequencer_tracks_data()
        export_sequencer_data_result = bfu_export_text_files_utils.export_single_json_file(json_data, root_dirpath, "ImportSequencerData.json")
        if export_sequencer_data_result:
            success_sequencer_data = True

        source = os.path.join(bfu_path, "sequencer_import_script.py")
        filename = bfu_basics.ValidFilename(scene.bfu_file_import_sequencer_script_name)
        destination = os.path.join(root_dirpath, filename)
        if bfu_export_text_files_utils.is_read_only(destination):
            print(f"Cannot replace '{destination}': File is read-only.")
            success_sequencer_script = False
        else:
            copyfile(source, destination)
            success_sequencer_script = True
    time_log.end_time_log()

