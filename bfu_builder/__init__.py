import importlib

from . import bpl
from . import main
from . import config
from . import blender_exec
from . import blender_version_manager

if "bpl" in locals():
    importlib.reload(bpl)
if "main" in locals():
    importlib.reload(main)
if "config" in locals():
    importlib.reload(config)
if "blender_exec" in locals():
    importlib.reload(blender_exec)
if "blender_version_manager" in locals():
    importlib.reload(blender_version_manager)
