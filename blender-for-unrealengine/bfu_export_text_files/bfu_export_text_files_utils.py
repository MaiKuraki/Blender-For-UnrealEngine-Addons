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
from .. import bfu_utils
from .. import bfu_export_logs



def WriteImportPythonHeadComment(useSequencer=False):

    scene = bpy.context.scene

    # Comment
    ImportScript = (
        "#This script was generated with the addons Blender for UnrealEngine" +
        " : https://github.com/xavier150/Blender-For-UnrealEngine-Addons" +
        "\n"
        )
    if useSequencer:
        ImportScript += (
            "#It will import into Unreal Engine all the assets of type" +
            " StaticMesh, SkeletalMesh, Animation and Pose" +
            "\n")
    else:
        ImportScript += (
            "#This script will import in unreal" +
            " all camera in target sequencer" +
            "\n")

    ImportScript += (
        "#The script must be used in Unreal Engine Editor" +
        " with Python plugins : " +
        "https://docs.unrealengine.com/en-US/Engine/" +
        "Editor/ScriptingAndAutomation/Python" +
        "\n"
        )

    if useSequencer:
        ImportScript += "#Use this command : " + bfu_utils.GetImportSequencerScriptCommand() + "\n"
    else:
        ImportScript += "#Use this command : " + bfu_utils.GetImportAssetScriptCommand() + "\n"
    ImportScript += "\n"
    ImportScript += "\n"
    return ImportScript

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

def ExportSingleText(text, dirpath, filename):
    # Export single text

    counter = bpl.utils.CounterTimer()

    absdirpath = bpy.path.abspath(dirpath)
    bfu_basics.verifi_dirs(absdirpath)
    fullpath = os.path.join(absdirpath, filename)

    with open(fullpath, "w") as file:
        file.write(text)

    exportTime = counter.get_time()
    # This return [AssetName , AssetType , ExportPath, ExportTime]
    return([filename, "TextFile", absdirpath, exportTime])

def ExportSingleJson(json_data, dirpath, filename):
    # Export single Json

    counter = bpl.utils.CounterTimer()

    absdirpath = bpy.path.abspath(dirpath)
    bfu_basics.verifi_dirs(absdirpath)
    fullpath = os.path.join(absdirpath, filename)

    with open(fullpath, 'w') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, sort_keys=False, indent=4)

    exportTime = counter.get_time()
    # This return [AssetName , AssetType , ExportPath, ExportTime]
    return([filename, "TextFile", absdirpath, exportTime])
