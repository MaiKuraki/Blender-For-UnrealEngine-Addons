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
        'obj.bfu_export_as_alembic_animation',
        'obj.bfu_create_sub_folder_with_alembic_name'
        ]
    return preset_values

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.bfu_export_as_alembic_animation = bpy.props.BoolProperty(
        name="Export as Alembic animation",
        description=("If true this mesh will be exported as a Alembic animation"),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )
    
    bpy.types.Object.bfu_create_sub_folder_with_alembic_name = bpy.props.BoolProperty(
        name="Create Alembic Sub Folder",
        description="Create a subfolder with the Alembic object name to avoid asset conflicts during the export. (Recommended)",
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )

    bpy.types.Scene.bfu_alembic_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Alembic")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_alembic_properties_expanded
    
    del bpy.types.Object.bfu_create_sub_folder_with_alembic_name
    del bpy.types.Object.bfu_export_as_alembic_animation