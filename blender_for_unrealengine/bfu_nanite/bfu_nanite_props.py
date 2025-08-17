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
            'obj.bfu_build_nanite_mode'
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

    # StaticMeshImportData
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxStaticMeshImportData/index.html
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxStaticMeshImportData/index.html


    bpy.types.Scene.bfu_object_nanite_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Nanite")
    bpy.types.Object.bfu_build_nanite_mode = bpy.props.EnumProperty(
        name="Light Map",
        description='If enabled, imported meshes will be rendered by Nanite at runtime.',
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ("auto",
                "Auto",
                "Use project settings.",
                1),
            ("build_nanite_true",
                "Build Nanite",
                "Build nanite at import.",
                2),
            ("build_nanite_false",
                "Don't Build Nanite",
                "Don't build and set object as non Nanite.",
                3)
            ]
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_build_nanite_mode
    del bpy.types.Scene.bfu_object_nanite_properties_expanded