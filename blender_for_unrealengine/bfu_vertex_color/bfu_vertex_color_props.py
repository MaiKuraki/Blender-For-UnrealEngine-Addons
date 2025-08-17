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
            'obj.bfu_vertex_color_import_option',
            'obj.bfu_vertex_color_override_color',
            'obj.bfu_vertex_color_to_use',
            'obj.bfu_vertex_color_index_to_use'
        ]
    return preset_values



# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (

)


# colors_type was added in 3.4 default is SRGB

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.bfu_vertex_color_import_option = bpy.props.EnumProperty(
        name="Vertex Color Import Option",
        description="Specify how vertex colors should be imported",
        override={'LIBRARY_OVERRIDABLE'},
        # Vania python
        # https://docs.unrealengine.com/en-US/PythonAPI/class/VertexColorImportOption.html
        # C++ API
        # https://docs.unrealengine.com/en-US/API/Editor/UnrealEd/Factories/EVertexColorImportOption__Type/index.html
        items=[
            ("IGNORE", "Ignore",
                "Ignore vertex colors, and keep the existing mesh vertex colors.", 1),
            ("OVERRIDE", "Override",
                "Override all vertex colors with the specified color.", 2),
            ("REPLACE", "Replace",
                "Import the static mesh using the target vertex colors.", 0)
            ],
        default="REPLACE"
        )

    bpy.types.Object.bfu_vertex_color_override_color = bpy.props.FloatVectorProperty(
            name="Vertex Override Color",
            subtype='COLOR',
            description="Specify override color in the case that bfu_vertex_color_import_option is set to Override",
            override={'LIBRARY_OVERRIDABLE'},
            default=(1.0, 1.0, 1.0),
            min=0.0,
            max=1.0
            # Vania python
            # https://docs.unrealengine.com/en-US/PythonAPI/class/FbxSkeletalMeshImportData.html
        )

    bpy.types.Object.bfu_vertex_color_to_use = bpy.props.EnumProperty(
        name="Vertex Color to use",
        description="Specify which vertex colors should be imported",
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ("FirstIndex", "First Index",
                "Use the the first index in Object Data -> Vertex Color.", 0),
            ("LastIndex", "Last Index",
                "Use the the last index in Object Data -> Vertex Color.", 1),
            ("ActiveIndex", "Active Render",
                "Use the the active index in Object Data -> Vertex Color.", 2),
            ("CustomIndex", "CustomIndex",
                "Use a specific Vertex Color in Object Data -> Vertex Color.", 3)
            ],
        default="ActiveIndex"
        )

    bpy.types.Object.bfu_vertex_color_index_to_use = bpy.props.IntProperty(
        name="Vertex color index",
        description="Vertex Color index to use.",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
    )

    bpy.types.Object.bfu_vertex_color_type = bpy.props.EnumProperty(
        name="Vertex Color to use",
        description="Target color space",
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ("SRGB", "sRGB", "Export colors in sRGB color space.", 0),
            ("LINEAR", "Linear", "Export colors in linear color space.", 1)
            ],
        default="SRGB"
        )

    bpy.types.Scene.bfu_object_vertex_color_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Vertex color")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_object_vertex_color_properties_expanded
    del bpy.types.Object.bfu_vertex_color_type
    del bpy.types.Object.bfu_vertex_color_index_to_use
    del bpy.types.Object.bfu_vertex_color_to_use
    del bpy.types.Object.bfu_vertex_color_override_color
    del bpy.types.Object.bfu_vertex_color_import_option