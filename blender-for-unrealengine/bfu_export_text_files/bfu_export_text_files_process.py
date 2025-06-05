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
import pathlib
import bpy
import datetime
from shutil import copyfile
from typing import List

from pathlib import Path
from . import bfu_export_text_files_asset_data
from . import bfu_export_text_files_sequencer_data
from . import bfu_export_text_files_utils

from .. import bpl
from .. import bbpl
from .. import languages
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_export_logs


def write_all_data_files(exported_asset_log: List[bfu_export_logs.bfu_asset_export_logs.ExportedAssetLog]):
    if bpy.context is None:
        return

    time_log = bfu_export_logs.bfu_process_time_logs_utils.start_time_log("Write text files")
    scene = bpy.context.scene
    root_dirpath = Path(bpy.path.abspath(scene.bfu_export_other_file_path))


    # Export log
    if scene.bfu_use_text_export_log:
        Text = languages.ti("write_text_additional_track_start") + "\n"
        Text += "" + "\n"
        Text += bfu_export_logs.bfu_asset_export_logs_utils.get_export_asset_logs_details(exported_asset_log)
        if Text is not None:
            Filename = bfu_basics.valid_file_name(scene.bfu_file_export_log_name)
            log_fullpath = root_dirpath / Filename
            bfu_export_text_files_utils.export_single_text_file(Text, log_fullpath)


    # Import script
    if bpy.app.version >= (4, 2, 0):
        package_path = bbpl.blender_extension.extension_utils.get_package_path()
        if package_path:
            bfu_path = Path(package_path) / "bfu_import_module"
        else:
            bfu_path = Path("unknown")
    else:
        bfu_path = Path(bbpl.blender_addon.addon_utils.get_addon_path("Unreal Engine Assets Exporter")) / "bfu_import_module"

    # Asset data
    if scene.bfu_use_text_import_asset_script:
        json_data = bfu_export_text_files_asset_data.write_main_assets_data(exported_asset_log)
        asset_data_fullpath = root_dirpath / "ImportAssetData.json"
        bfu_export_text_files_utils.export_single_json_file(json_data, asset_data_fullpath)

        source = bfu_path / "asset_import_script.py"
        filename = bfu_basics.valid_file_name(scene.bfu_file_import_asset_script_name)
        destination = root_dirpath / filename
        if bfu_export_text_files_utils.is_read_only(destination):
            print(f"Cannot replace '{destination}': File is read-only.")
        else:
            copyfile(source, destination)

    # Sequencer data
    if scene.bfu_use_text_import_sequence_script:
        json_data = bfu_export_text_files_sequencer_data.write_sequencer_tracks_data(exported_asset_log)
        sequencer_data_fullpath = root_dirpath / "ImportSequencerData.json"
        bfu_export_text_files_utils.export_single_json_file(json_data, sequencer_data_fullpath)


        source = bfu_path / "sequencer_import_script.py"
        filename = bfu_basics.valid_file_name(scene.bfu_file_import_sequencer_script_name)
        destination = root_dirpath / filename
        if bfu_export_text_files_utils.is_read_only(destination):
            print(f"Cannot replace '{destination}': File is read-only.")
        else:
            copyfile(source, destination)
    time_log.end_time_log()

