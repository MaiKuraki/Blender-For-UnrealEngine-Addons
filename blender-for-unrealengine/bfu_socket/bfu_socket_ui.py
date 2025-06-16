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
from .. import bfu_addon_prefs
from .. import bbpl


def draw_tools_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    
    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_tools_socket_properties_expanded")
    header, panel = accordion.draw(layout)
    if accordion.is_expend():
        addon_prefs = bfu_addon_prefs.get_addon_prefs()

        # Draw user tips and check can use buttons
        ready_for_convert_socket = False
        if not bbpl.utils.active_mode_is("OBJECT"):
            panel.label(text="Switch to Object Mode.", icon='INFO')
        else:

            if bbpl.utils.found_type_in_selection("EMPTY", False):
                if bbpl.utils.active_type_is_not("ARMATURE") and len(bpy.context.selected_objects) > 1:
                    panel.label(text="Click on button for convert to Socket.", icon='INFO')
                    ready_for_convert_socket = True
                else:
                    panel.label(text="Select with [SHIFT] the socket owner.", icon='INFO')
            else:
                panel.label(text="Please select your socket Empty(s). Active should be the owner.", icon='INFO')

        # Draw buttons
        convertButtons = panel.row().split(factor=0.80)
        convertStaticSocketButtons = convertButtons.column()
        convertStaticSocketButtons.enabled = ready_for_convert_socket
        convertStaticSocketButtons.operator("object.converttostaticsocket", icon='OUTLINER_DATA_EMPTY')


        if addon_prefs.useGeneratedScripts:

            # Draw user tips and check can use buttons (skeletal_socket)
            ready_for_convert_skeletal_socket = False
            if not bbpl.utils.active_mode_is("OBJECT"):
                if not bbpl.utils.active_type_is("ARMATURE"):
                    if not bbpl.utils.found_type_in_selection("EMPTY"):
                        panel.label(text="Switch to Object Mode.", icon='INFO')
            else:
                if bbpl.utils.found_type_in_selection("EMPTY"):
                    if bbpl.utils.active_type_is("ARMATURE") and len(bpy.context.selected_objects) > 1:
                        panel.label(text="Switch to Pose Mode.", icon='INFO')
                    else:
                        panel.label(text="Select with [SHIFT] the socket owner. (Armature)", icon='INFO')
                else:
                    panel.label(text="Select your socket Empty(s).", icon='INFO')

            if bbpl.utils.active_mode_is("POSE") and bbpl.utils.active_type_is("ARMATURE") and bbpl.utils.found_type_in_selection("EMPTY"):
                if len(bpy.context.selected_pose_bones) > 0:
                    panel.label(text="Click on button for convert to Socket.", icon='INFO')
                    ready_for_convert_skeletal_socket = True
                else:
                    panel.label(text="Select the owner bone.", icon='INFO')

            # Draw buttons (skeletal_socket)
            convertButtons = panel.row().split(factor=0.80)
            convertSkeletalSocketButtons = convertButtons.column()
            convertSkeletalSocketButtons.enabled = ready_for_convert_skeletal_socket
            convertSkeletalSocketButtons.operator("object.converttoskeletalsocket",icon='OUTLINER_DATA_EMPTY')
            
        obj = bpy.context.object
        if obj is not None:
            if obj.type == "EMPTY":
                socketName = panel.column()
                socketName.prop(obj, "bfu_use_socket_custom_Name")
                socketNameText = socketName.column()
                socketNameText.enabled = obj.bfu_use_socket_custom_Name
                socketNameText.prop(obj, "bfu_socket_custom_Name")

        copy_skeletalsocket_buttons = panel.column()
        copy_skeletalsocket_buttons.enabled = False
        copy_skeletalsocket_buttons.operator(
            "object.copy_skeletalsocket_command",
            icon='COPYDOWN')
        if obj is not None:
            if obj.type == "ARMATURE":
                copy_skeletalsocket_buttons.enabled = True
            
        