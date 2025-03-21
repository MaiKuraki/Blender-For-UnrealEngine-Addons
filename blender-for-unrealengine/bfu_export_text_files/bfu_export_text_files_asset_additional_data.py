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
from . import bfu_export_text_files_utils
from .. import bfu_export_logs
from .. import languages
from .. import bfu_basics
from .. import bfu_socket
from .. import bfu_light_map
from .. import bfu_nanite
from .. import bfu_vertex_color
from .. import bfu_material
from .. import bfu_lod

def write_single_asset_additional_data(unreal_exported_asset: bfu_export_logs.bfu_asset_export_logs.BFU_OT_UnrealExportedAssetLog):

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    obj = unreal_exported_asset.object

    asset_additional_data = {}

    bfu_export_text_files_utils.add_generated_json_header(asset_additional_data, languages.ti('write_text_additional_track_all'))
    bfu_export_text_files_utils.add_generated_json_meta_data(asset_additional_data)

    # Defaultsettings
    asset_additional_data['DefaultSettings'] = {}
    # config.set('Defaultsettings', 'SocketNumber', str(len(sockets)))

    # Sockets
    if obj:
        asset_additional_data['Sockets'] = bfu_socket.bfu_socket_utils.get_skeletal_mesh_sockets(obj)


    asset_additional_data.update(bfu_lod.bfu_lod_utils.get_lod_additional_data(unreal_exported_asset))
    asset_additional_data.update(bfu_vertex_color.bfu_vertex_color_utils.get_vertex_color_additional_data(unreal_exported_asset))
    asset_additional_data.update(bfu_material.bfu_material_utils.get_material_asset_additional_data(unreal_exported_asset))
    asset_additional_data.update(bfu_light_map.bfu_light_map_utils.get_light_map_asset_data(unreal_exported_asset))
    asset_additional_data.update(bfu_nanite.bfu_nanite_utils.get_nanite_asset_additional_data(unreal_exported_asset))

    bfu_export_text_files_utils.add_generated_json_footer(asset_additional_data)
    return asset_additional_data