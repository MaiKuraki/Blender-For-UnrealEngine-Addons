# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================


import bpy
from .. import bbpl




def get_preset_values():
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