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


from typing import List
import bpy
import math
from .. import bfu_basics
from .. import bbpl
from .. import languages
from . import bfu_camera_utils
from . import bfu_camera_write_paste_commands


def get_preset_values() -> List[str]:
    preset_values = [
        'obj.bfu_export_fbx_camera',
        'obj.bfu_fix_axis_flippings',
        'obj.bfu_desired_camera_type',
        'obj.bfu_custom_camera_actor',
        'obj.bfu_custom_camera_default_actor',
        'obj.bfu_custom_camera_component'
        ]
    return preset_values


# Object button
class BFU_OT_CopyActiveCameraOperator(bpy.types.Operator):
    bl_label = "Copy active camera for Unreal"
    bl_idname = "object.bfu_copy_active_camera_data"
    bl_description = "Copy active camera data. (Use CTRL+V in Unreal viewport)"

    def execute(self, context: bpy.types.Context):  # type: ignore
        obj = context.object
        result = bfu_camera_write_paste_commands.get_import_camera_script_command([obj])  # type: ignore
        if result[0]:
            bfu_basics.set_windows_clipboard(result[1])
            self.report({'INFO'}, result[2])
        else:
            self.report({'WARNING'}, result[2])
        return {'FINISHED'}

# Scene button
class BFU_OT_CopySelectedCamerasOperator(bpy.types.Operator):
    bl_label = "Copy selected camera(s) for Unreal"
    bl_idname = "object.copy_selected_cameras_data"
    bl_description = "Copy selected camera(s) data. (Use CTRL+V in Unreal viewport)"

    def execute(self, context: bpy.types.Context):  # type: ignore
        objs = context.selected_objects
        result = bfu_camera_write_paste_commands.get_import_camera_script_command(objs)
        if result[0]:
            bfu_basics.set_windows_clipboard(result[1])
            self.report({'INFO'}, result[2])
        else:
            self.report({'WARNING'}, result[2])
        return {'FINISHED'}



# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_CopyActiveCameraOperator,
    BFU_OT_CopySelectedCamerasOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.bfu_camera_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Camera Properties")  # type: ignore
    bpy.types.Scene.bfu_camera_tools_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Camera")  # type: ignore

    bpy.types.Object.bfu_export_fbx_camera = bpy.props.BoolProperty(  # type: ignore
        name=(languages.ti('export_camera_as_fbx_name')),
        description=(languages.tt('export_camera_as_fbx_desc')),
        override={'LIBRARY_OVERRIDABLE'},
        default=False,
        )
    bpy.types.Object.bfu_fix_axis_flippings = bpy.props.BoolProperty(  # type: ignore
        name="Fix Camera Axis",
        description=('Enable this option to fix axis flipping caused by rotation wrapping. '
                    'Disable only if you use extreme camera animations in a single frame.'),
        override={'LIBRARY_OVERRIDABLE'},
        default=True,
        )
    bpy.types.Object.bfu_fix_axis_flippings_warp_target = bpy.props.FloatVectorProperty(  # type: ignore
        name="Fix Camera Axis Warp Target",
        description=('Target rotation values (in degrees) used to fix camera axis wrapping issues.'),
        override={'LIBRARY_OVERRIDABLE'},
        default=(math.radians(360.0), math.radians(360.0), math.radians(360.0)),  # Convert to radians
        subtype='EULER'
        )
    bpy.types.Object.bfu_desired_camera_type = bpy.props.EnumProperty(  # type: ignore
        name="Camera Type",
        description="Choose the type of camera",
        items=bfu_camera_utils.get_enum_cameras_list(),
        default=bfu_camera_utils.get_enum_cameras_default()
    )
    bpy.types.Object.bfu_custom_camera_actor = bpy.props.StringProperty(  # type: ignore
        name="Custom Camera Actor",
        description=('Ref adress for an custom camera actor'),
        override={'LIBRARY_OVERRIDABLE'},
        default="/Script/MyModule.MyCameraActor",
        )
    bpy.types.Object.bfu_custom_camera_default_actor = bpy.props.StringProperty(  # type: ignore
        name="Custom Camera Actor(default)",
        description=('Ref adress for an custom camera actor (default)'),
        override={'LIBRARY_OVERRIDABLE'},
        default="/Script/MyModule.Default__MyCameraActor",
        )
    bpy.types.Object.bfu_custom_camera_component = bpy.props.StringProperty(  # type: ignore
        name="Custom Camera Component",
        description=('Ref adress for an custom camera component'),
        override={'LIBRARY_OVERRIDABLE'},
        default="/Script/MyModule.MyCameraComponent",
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_custom_camera_component  # type: ignore
    del bpy.types.Object.bfu_custom_camera_default_actor  # type: ignore
    del bpy.types.Object.bfu_custom_camera_actor  # type: ignore
    del bpy.types.Object.bfu_desired_camera_type  # type: ignore
    del bpy.types.Object.bfu_fix_axis_flippings  # type: ignore
    del bpy.types.Object.bfu_export_fbx_camera  # type: ignore
    del bpy.types.Scene.bfu_camera_tools_expanded  # type: ignore
    del bpy.types.Scene.bfu_camera_properties_expanded  # type: ignore



