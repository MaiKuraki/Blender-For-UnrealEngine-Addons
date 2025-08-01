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

from typing import Dict, Any
from . import bfu_export_text_files_utils
from .. import languages

def write_additional_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Writes the additional data for a preset to a JSON file.
    :param data: The data to write.
    :return: The additional data as a dictionary.
    """
    asset_additional_data: Dict[str, Any] = {}

    bfu_export_text_files_utils.add_generated_json_header(asset_additional_data, languages.ti('write_text_additional_track_all'))
    bfu_export_text_files_utils.add_generated_json_meta_data(asset_additional_data)

    # Defaultsettings
    asset_additional_data['DefaultSettings'] = {}
    
    # Add the preset data
    asset_additional_data.update(data)

    bfu_export_text_files_utils.add_generated_json_footer(asset_additional_data)
    return asset_additional_data
