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
import json

from .. import bpl
from .. import bbpl
from .. import languages
from .. import bfu_basics


def add_generated_json_header(json_data, text: str):

    json_data['comment'] = {
        '1/3': languages.ti('write_text_additional_track_start'),
        '2/3': text,
        '3/3': languages.ti('write_text_additional_track_end'),
    }

def add_generated_json_footer(json_data):
    # Empty for the momment.
    pass

def add_generated_json_meta_data(json_data):
    
    current_datetime = datetime.datetime.now()
    current_datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = int(current_datetime.timestamp())

    blender_file_path = bpy.data.filepath

    if bpy.app.version >= (4, 2, 0):
        version_str = 'Version '+ str(bbpl.blender_extension.extension_utils.get_package_version())
        addon_path = bbpl.blender_extension.extension_utils.get_package_path()
    else:
        version_str = 'Version '+ bbpl.blender_addon.addon_utils.get_addon_version_str("Unreal Engine Assets Exporter")
        addon_path = bbpl.blender_addon.addon_utils.get_addon_path("Unreal Engine Assets Exporter")
    import_modiule_path = os.path.join(addon_path, "bfu_import_module")


    json_data['info'] = {
        'date_time_str': current_datetime_str,
        "timestamp": timestamp,
        "blender_file": blender_file_path,
        'addon_version': version_str,
        'addon_path': addon_path,
        'import_modiule_path': import_modiule_path,
    }

def is_read_only(filepath):
    return os.path.exists(filepath) and not os.access(filepath, os.W_OK)

def export_single_text_file(text, dirpath, filename):
    # Export single text
    counter = bpl.utils.CounterTimer()

    absdirpath = bpy.path.abspath(dirpath)
    bfu_basics.verifi_dirs(absdirpath)
    fullpath = os.path.join(absdirpath, filename)

    if is_read_only(fullpath):
        print(f"Cannot write to '{fullpath}': File is read-only.")
        return None

    with open(fullpath, "w") as file:
        file.write(text)

    exportTime = counter.get_time()
    # This return [AssetName , AssetType , ExportPath, ExportTime]
    return([filename, "TextFile", absdirpath, exportTime])

def export_single_json_file(json_data, dirpath, filename):
    # Export single Json

    counter = bpl.utils.CounterTimer()

    absdirpath = bpy.path.abspath(dirpath)
    bfu_basics.verifi_dirs(absdirpath)
    fullpath = os.path.join(absdirpath, filename)

    if is_read_only(fullpath):
        print(f"Cannot write to '{fullpath}': File is read-only.")
        return None

    with open(fullpath, 'w') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, sort_keys=False, indent=4)

    exportTime = counter.get_time()
    # This return [AssetName , AssetType , ExportPath, ExportTime]
    return([filename, "TextFile", absdirpath, exportTime])
