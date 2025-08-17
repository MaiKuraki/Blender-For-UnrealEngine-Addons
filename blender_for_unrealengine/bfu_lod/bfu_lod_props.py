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
            'obj.bfu_export_as_lod_mesh',
            'obj.bfu_use_static_mesh_lod_group',
            'obj.bfu_static_mesh_lod_group',
            'obj.bfu_lod_target1',
            'obj.bfu_lod_target2',
            'obj.bfu_lod_target3',
            'obj.bfu_lod_target4',
            'obj.bfu_lod_target5',
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

    bpy.types.Scene.bfu_lod_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Lod")

    bpy.types.Object.bfu_export_as_lod_mesh = bpy.props.BoolProperty(
        name="Export as lod?",
        description=(
            "If true this mesh will be exported" +
            " as a level of detail for another mesh"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )

    # Lod Group
    bpy.types.Object.bfu_use_static_mesh_lod_group = bpy.props.BoolProperty(
        name="",
        description='',
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )

    bpy.types.Object.bfu_static_mesh_lod_group = bpy.props.StringProperty(
        name="LOD Group",
        description=(
            "The LODGroup to associate with this mesh when it is imported." +
            " Default: LevelArchitecture, SmallProp, " +
            "LargeProp, Deco, Vista, Foliage, HighDetail"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        maxlen=32,
        default="SmallProp"
        )

    # Lod list
    bpy.types.Object.bfu_lod_target1 = bpy.props.PointerProperty(
        name="LOD1",
        description="Target objet for level of detail 01",
        override={'LIBRARY_OVERRIDABLE'},
        type=bpy.types.Object
        )

    bpy.types.Object.bfu_lod_target2 = bpy.props.PointerProperty(
        name="LOD2",
        description="Target objet for level of detail 02",
        override={'LIBRARY_OVERRIDABLE'},
        type=bpy.types.Object
        )

    bpy.types.Object.bfu_lod_target3 = bpy.props.PointerProperty(
        name="LOD3",
        description="Target objet for level of detail 03",
        override={'LIBRARY_OVERRIDABLE'},
        type=bpy.types.Object
        )

    bpy.types.Object.bfu_lod_target4 = bpy.props.PointerProperty(
        name="LOD4",
        description="Target objet for level of detail 04",
        override={'LIBRARY_OVERRIDABLE'},
        type=bpy.types.Object
        )

    bpy.types.Object.bfu_lod_target5 = bpy.props.PointerProperty(
        name="LOD5",
        description="Target objet for level of detail 05",
        override={'LIBRARY_OVERRIDABLE'},
        type=bpy.types.Object
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_lod_target5
    del bpy.types.Object.bfu_lod_target4
    del bpy.types.Object.bfu_lod_target3
    del bpy.types.Object.bfu_lod_target2
    del bpy.types.Object.bfu_lod_target1

    del bpy.types.Object.bfu_static_mesh_lod_group
    del bpy.types.Object.bfu_use_static_mesh_lod_group

    del bpy.types.Object.bfu_export_as_lod_mesh
    del bpy.types.Scene.bfu_lod_properties_expanded