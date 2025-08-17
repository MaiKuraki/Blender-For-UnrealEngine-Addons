# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
import importlib

from . import bfu_export_process_props
from . import bfu_export_process_operators
from . import bfu_export_process_ui
from . import bfu_export_process_utils

if "bfu_export_process_props" in locals():
    importlib.reload(bfu_export_process_props)
if "bfu_export_process_operators" in locals():
    importlib.reload(bfu_export_process_operators)
if "bfu_export_process_ui" in locals():
    importlib.reload(bfu_export_process_ui)
if "bfu_export_process_utils" in locals():
    importlib.reload(bfu_export_process_utils)

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bfu_export_process_props.register()
    bfu_export_process_operators.register()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bfu_export_process_operators.unregister()
    bfu_export_process_props.unregister()