import bpy
from typing import Dict, Optional, Tuple

import importlib
from . import config
from . import utils

if "config" in locals():
    importlib.reload(config)
if "utils" in locals():
    importlib.reload(utils)


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    translations_dict: Optional[Dict[str, Dict[Tuple[Optional[str], str], str]]] = utils.construct_translations_dict()
    bpy.app.translations.register(__name__, translations_dict)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)