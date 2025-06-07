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
from .. import bfu_cached_assets
from ..bfu_assets_manager.bfu_asset_manager_type import AssetToExport, AssetDataSearchMode, AssetType, AssetPackage
from .. import bpl

def get_asset_title_text(asset_count: int) -> str:
    if asset_count == 0:
        return "No exportable assets were found."
    elif asset_count == 1:
        return "1 asset will be exported."
    else:
        return f"{asset_count} assets will be exported."

def draw_asset_preview_bar(
    layout: bpy.types.UILayout, 
    context: bpy.types.Context,
) -> None:
    
    final_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.get_final_asset_cache()
    final_asset_list_to_export = final_asset_cache.get_final_asset_list(AssetDataSearchMode.ASSET_NUMBER)

    asset_count = len(final_asset_list_to_export)
    asset_info_ui = layout.row().box().split(factor=0.75)
    asset_info_text = get_asset_title_text(asset_count)
    asset_info_ui.label(text=asset_info_text)  # type: ignore
    asset_info_ui.operator("object.showasset", text="Show Assets")  # type: ignore


def draw_asset_content_line(
    layout: bpy.types.UILayout, 
    context: bpy.types.Context,
) -> bpy.types.UILayout:

    package_row = layout.row()
    package_row.alignment = "EXPAND"
    package_content_col = package_row.column()
    package_content_col.alignment = "EXPAND"
    package_content_col.scale_y = 0.8
    return package_content_col

def draw_asset_package(
    asset: AssetToExport,
    package: AssetPackage, 
    layout: bpy.types.UILayout, 
    context: bpy.types.Context
) -> None:
    
    scene = context.scene
    package_line = draw_asset_content_line(layout, context)

    # Package name and details
    package_content_details_row = package_line.row()
    package_content_details_row.alignment = "LEFT"

    # package Title
    package_title = f"{package.name}"
    package_content_details_row.label(text=package_title)  # type: ignore

    # Package details
    if package.details:
        package_details = f"({', '.join(package.details)})"
    else:
        package_details = ""
    package_content_details_row.label(text=f"{package_details}")  # type: ignore

    # Package resource count
    if asset.asset_type.can_contain_objects():
        package_resource = f"[{len(package.objects)} objects]"
        package_resource = ""
        if len(package.objects) > 0:
            package_resource = f"[{len(package.objects)} objects]"
        package_content_details_row.label(text=package_resource)  # type: ignore

    # Package animation details
    if asset.asset_type.can_use_frame_range():
        frame_range = package.frame_range
        if frame_range is not None:
            if asset.asset_type == AssetType.ANIM_POSE:
                pose_frame_text = f"Frame: {frame_range[0]}"
                package_content_details_row.label(text=pose_frame_text)  # type: ignore
            else:
                frame_range_text = f"Frames: {frame_range[0]}-{frame_range[1]}"
                frame_count = frame_range[1] - frame_range[0] + 1
                fps = scene.render.fps / scene.render.fps_base
                animation_duration = frame_count / fps
                animation_duration_text = bpl.utils.get_formatted_time_as_seconds(time_in_seconds=animation_duration, compact=True, min_decimals=2)
                package_content_details_row.label(text=f"{frame_range_text} ({frame_count}, {animation_duration_text}) FPS: {fps}")  # type: ignore
        else:
            package_content_details_row.label(text="No frame range set.")  # type: ignore

    # Package file path
    package_content_file_row = package_line.row()
    package_content_file_row.alignment = "EXPAND"
    if package.file is not None:
        str_path = str(package.file.get_full_path())
        package_content_file_row.label(icon='FILE', text=str_path)  # type: ignore
    else:
        package_content_file_row.label(icon='FILE', text="No file set for this package.")  # type: ignore

def draw_additional_data(
    asset: AssetToExport,
    layout: bpy.types.UILayout,
    context: bpy.types.Context
) -> None:

    if asset.additional_data is not None:
        additional_data_line = draw_asset_content_line(layout, context)
        additional_data_row = additional_data_line.row()
        additional_data_row.alignment = "EXPAND"
        if asset.additional_data.file is not None:
            str_path = str(asset.additional_data.file.get_full_path())
            additional_data_row.label(icon='FILE', text=str_path)  # type: ignore
        else:
            additional_data_row.label(icon='FILE', text="No file set for additional data.")  # type: ignore

def draw_asset(
    asset: AssetToExport, 
    layout: bpy.types.UILayout, 
    context: bpy.types.Context
) -> None:

    asset_box = layout.box()
    asset_box.alignment = 'LEFT'
    asset_row = asset_box.row()
    asset_row.alignment = 'EXPAND'
    asset_row.scale_y = 0.8

    # Asset name and type
    asset_info = asset_row.row()
    asset_info.alignment = 'LEFT'
    asset_name = f"- {asset.name} ({asset.asset_type.get_friendly_name()})"
    asset_info.label(text=asset_name)  # type: ignore

    # Asset Pakages
    asset_col = asset_row.column()
    asset_col.alignment = 'EXPAND'
    for package in asset.asset_packages:
        draw_asset_package(asset, package, asset_col, context)
    draw_additional_data(asset, asset_col, context)


def draw_assets_list(
    layout: bpy.types.UILayout, 
    context: bpy.types.Context, 
    final_asset_list_to_export: list[AssetToExport]
) -> None:

    # Popup title
    popup_title = get_asset_title_text(len(final_asset_list_to_export))
    layout.label(text=popup_title, icon='PACKAGE')  # type: ignore

    for asset in final_asset_list_to_export:
        draw_asset(asset, layout, context)


        '''
        if asset.obj is not None:

            
            if asset.action is not None:
                if (type(asset.action) is bpy.types.Action):
                    # Action name
                    action = asset.action.name
                elif (type(asset.action) is bpy.types.AnimData):
                    # Nonlinear name
                    action = asset.obj.bfu_anim_nla_export_name
                else:
                    action = "..."
                row.label(
                    text="- ["+asset.name+"] --> " +
                    action+" ("+asset.asset_type.get_friendly_name()+")")
            else:
                if asset.asset_type != "Collection StaticMesh":
                    row.label(
                        text="- "+asset.name +
                        " ("+asset.asset_type.get_friendly_name()+")")
                else:
                    row.label(
                        text="- "+asset.obj.name +
                        " ("+asset.asset_type.get_friendly_name()+")")
            
        else:
            row.label(text="- ("+asset.asset_type.get_friendly_name()+")")
        '''