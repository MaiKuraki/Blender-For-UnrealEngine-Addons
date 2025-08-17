# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
import importlib

from . import bfu_light_map_props
from . import bfu_light_map_ui
from . import bfu_light_map_utils

if "bfu_light_map_props" in locals():
    importlib.reload(bfu_light_map_props)
if "bfu_light_map_ui" in locals():
    importlib.reload(bfu_light_map_ui)
if "bfu_light_map_utils" in locals():
    importlib.reload(bfu_light_map_utils)

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bfu_light_map_props.register()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bfu_light_map_props.unregister()