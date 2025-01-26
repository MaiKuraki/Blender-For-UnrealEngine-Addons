import bpy
import importlib

from . import bfu_asset_export_logs
from . import bfu_asset_export_logs_utils

if "bfu_asset_export_logs" in locals():
    importlib.reload(bfu_asset_export_logs)
if "bfu_asset_export_logs_utils" in locals():
    importlib.reload(bfu_asset_export_logs_utils)


def clear_all_logs():
    bfu_asset_export_logs_utils.clear_asset_logs()

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bfu_asset_export_logs.register()

def unregister():
    bfu_asset_export_logs.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

