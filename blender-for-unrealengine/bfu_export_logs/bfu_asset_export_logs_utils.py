import bpy
from typing import List
from .. import bfu_utils
from .. import bpl

from . import bfu_asset_export_logs

def get_exported_assets_logs() -> List[bfu_asset_export_logs.BFU_OT_UnrealExportedAssetLog]:
    scene = bpy.context.scene
    return scene.bfu_unreal_exported_assets_logs

def create_new_asset_log()-> bfu_asset_export_logs.BFU_OT_UnrealExportedAssetLog:
    scene = bpy.context.scene
    return scene.bfu_unreal_exported_assets_logs.add()

def clear_asset_logs():
    scene = bpy.context.scene
    scene.bfu_unreal_exported_assets_logs.clear()

def get_exported_asset_number():
    # TODO Need add a check to know how many asset is realy exported
    scene = bpy.context.scene
    return len(scene.bfu_unreal_exported_assets_logs)

def get_export_asset_logs_details():
    """
    Generate a detailed export log for assets exported in the scene.
    The log includes counts and details for each asset type.

    Returns:
        str: The formatted export log.
    """

    # Initialize variables
    scene = bpy.context.scene
    asset_counts = {
        "StaticMesh": 0,
        "SkeletalMesh": 0,
        "Alembic": 0,
        "Animation": 0,
        "Camera": 0,
        "Spline": 0
    }

    # Count assets by type
    for asset in get_exported_assets_logs():
        if asset.asset_type in asset_counts:
            asset_counts[asset.asset_type] += 1
        elif bfu_utils.GetIsAnimation(asset.asset_type):
            asset_counts["Animation"] += 1

    # Calculate totals
    total_assets = len(scene.bfu_unreal_exported_assets_logs)
    exported_assets = sum(asset_counts.values())
    other_assets = total_assets - exported_assets

    # Build asset type summary
    asset_summary = " | ".join(
        f"{count} {asset_type}(s)" for asset_type, count in asset_counts.items()
    )
    asset_summary += f" | {other_assets} Other(s)\n"

    # Build asset type summary with color formatting
    def colorize_count(count, text):
        if count == 0:
            return bpl.color_set.red(text)
        return bpl.color_set.green(text)

    asset_summary = " | ".join(
        colorize_count(count, f"{count} {asset_type}(s)") for asset_type, count in asset_counts.items()
    )
    asset_summary += f" | {colorize_count(other_assets, f'{other_assets} Other(s)')}\n"

    # Build export log
    export_log = asset_summary + "\n"

    for asset in get_exported_assets_logs():
        # Determine primary information for the asset
        if asset.asset_type in ["NlAnim", "Action", "Pose"]:
            primary_info = f"Animation ({asset.asset_type})"
        else:
            primary_info = f"{asset.asset_type} (LOD)" if asset.object and asset.object.bfu_export_as_lod_mesh else asset.asset_type

        # Format export time
        export_time = bpl.color_set.yellow(bpl.utils.get_formatted_time(asset.GetExportTime()))

        # Append asset details to the log
        export_log += f"Asset [{primary_info}] '{asset.asset_name}' EXPORTED IN {export_time}\r\n"

        # Append file details
        for file in asset.files:
            export_log += f"- {file.file_path}\\{file.file_name}\n"

    return export_log