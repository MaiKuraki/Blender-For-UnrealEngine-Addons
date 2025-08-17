# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


from typing import List
import bpy
from .. import bbpl


def get_preset_values() -> List[str]:
    preset_values = [
            'obj.bfu_export_type',
            'obj.bfu_export_folder_name',
            'obj.bfu_use_custom_export_name',
            'obj.bfu_custom_export_name',       
        ]
    return preset_values

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore

    bpy.types.Scene.bfu_object_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Object Properties")  # type: ignore[attr-defined]


    
    bpy.types.Object.bfu_export_folder_name = bpy.props.StringProperty(  # type: ignore[attr-defined]
        name="Sub folder name",
        description=(
            'The name of sub folder.' +
            ' You can now use ../ for up one directory.'
            ),
        override={'LIBRARY_OVERRIDABLE'},
        maxlen=64,
        default="",
        subtype='FILE_NAME'
        )
    
    bpy.types.Object.bfu_use_custom_export_name = bpy.props.BoolProperty(  # type: ignore[attr-defined]
        name="Export with custom name",
        description=("Specify a custom name for the exported file"),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )

    bpy.types.Object.bfu_custom_export_name = bpy.props.StringProperty(  # type: ignore[attr-defined]
        name="",
        description="The name of exported file",
        override={'LIBRARY_OVERRIDABLE'},
        default="MyObjectExportName.fbx"
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    del bpy.types.Object.bfu_custom_export_name  # type: ignore[attr-defined]
    del bpy.types.Object.bfu_use_custom_export_name  # type: ignore[attr-defined]
    del bpy.types.Object.bfu_export_folder_name  # type: ignore[attr-defined]
    del bpy.types.Scene.bfu_object_properties_expanded  # type: ignore[attr-defined]