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


from typing import TYPE_CHECKING, List
import bpy


def get_preset_values() -> List[str]:
    preset_values = [
        ]
    return preset_values

class BFU_OT_UnrealPotentialError(bpy.types.PropertyGroup):
    type: bpy.props.IntProperty(default=0)  # 0:Info, 1:Warning, 2:Error  # type: ignore
    object: bpy.props.PointerProperty(type=bpy.types.Object)  # type: ignore
    ###
    select_object_button: bpy.props.BoolProperty(default=True)  # type: ignore
    select_vertex_button: bpy.props.BoolProperty(default=False)  # type: ignore
    select_pose_bone_button: bpy.props.BoolProperty(default=False)  # type: ignore
    ###
    select_option: bpy.props.StringProperty(default="None")  # 0:VertexWithZeroWeight  # type: ignore
    item_name: bpy.props.StringProperty(default="None")  # type: ignore
    text: bpy.props.StringProperty(default="Unknown")  # type: ignore
    correct_ref: bpy.props.StringProperty(default="None")  # type: ignore
    correct_label: bpy.props.StringProperty(default="Fix it !")  # type: ignore
    correct_desc: bpy.props.StringProperty(default="Correct target error")  # type: ignore
    docs_octicon: bpy.props.StringProperty(default="None")  # type: ignore

    if TYPE_CHECKING:
        type: int
        object: bpy.types.Object

        select_object_button: bool
        select_vertex_button: bool
        select_pose_bone_button: bool

        select_option: str
        item_name: str
        text: str
        correct_ref: str
        correct_label: str
        correct_desc: str
        docs_octicon: str


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_UnrealPotentialError,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_export_potential_errors = bpy.props.CollectionProperty(type=BFU_OT_UnrealPotentialError)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_export_potential_errors
