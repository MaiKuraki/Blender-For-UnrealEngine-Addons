import bpy
from . import bbpl

def get_addon_version() -> str:
    if bpy.app.version >= (4, 2, 0):
        return str(bbpl.blender_extension.extension_utils.get_package_version())
    else:
        return bbpl.blender_addon.addon_utils.get_addon_version_str("Unreal Engine Assets Exporter")

ADDON_VERSION_STR: str = get_addon_version()


