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
from .. import bfu_export_logs
from ..bfu_export_logs.bfu_process_time_logs_types import SafeTimeGroup
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport, AssetPackage
from .. import bbpl

def prepare_scene_for_package_export(package: AssetPackage):
    if bpy.context is None:
        return
    
    scene = bpy.context.scene

    for obj in scene.objects:
        if obj in package.objects:
            if obj.hide_viewport is True:
                obj.hide_viewport = False
        else:
            if obj.hide_viewport is False:
                obj.hide_viewport = True


def process_generic_export_from_asset(
    op: bpy.types.Operator,
    asset: AssetToExport
) -> bfu_export_logs.bfu_asset_export_logs_types.ExportedAssetLog:


    new_log = bfu_export_logs.bfu_asset_export_logs_types.ExportedAssetLog(asset)
    new_log.start_asset_export()
    for package in asset.asset_packages:
        new_log.start_package_export(package)

        my_timer_group = SafeTimeGroup()
        my_timer_group.start_timer(f"Preparing scene for package export: {package.name}")
        prepare_scene_for_package_export(package)
        my_timer_group.end_last_timer()

        # Check folder before export
        if package.file:
            bfu_export_utils.check_and_make_export_path(package.file.get_full_path())

        if package.export_function:
            my_timer_group.start_timer(f"Exporting package: {package.name}")
            result = package.export_function(op, package)
            my_timer_group.end_last_timer()

            if result:
                new_log.end_package_export(package, True)
            else:
                new_log.end_package_export(package, False)
        else:
            new_log.end_package_export(package, False)

    if asset.additional_data and asset.additional_data.file:
        bfu_export_utils.export_additional_data(asset.additional_data.file.get_full_path(), asset.additional_data.data)

    new_log.end_asset_export(True)
    return new_log

