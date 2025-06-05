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
from typing import Set
from .. import bbpl
from . import bfu_check_list
from . import bfu_check_utils

class BFU_OT_CheckPotentialErrorPopup(bpy.types.Operator):
    bl_label = "Check Potential Issues"
    bl_idname = "object.checkpotentialerror"
    bl_description = "Check potential issues on assets to export."
    text = "none"

    def execute(self, context: bpy.types.Context | None):
        fix_info = bfu_check_utils.process_general_fix()
        invoke_info = ""
        for x, fix_info_key in enumerate(fix_info):
            fix_info_data = fix_info[fix_info_key]
            invoke_info += fix_info_key + ": " + str(fix_info_data) 
            if x < len(fix_info)-1:
                invoke_info += "\n"

        bfu_check_list.run_all_check()
        bpy.ops.object.openpotentialerror("INVOKE_DEFAULT", invoke_info=invoke_info)  # type: ignore
        return {'FINISHED'}

class BFU_OT_OpenPotentialErrorPopup(bpy.types.Operator):
    bl_label = "Open potential errors"
    bl_idname = "object.openpotentialerror"
    bl_description = "Open potential errors"
    invoke_info: bpy.props.StringProperty(default="...")  # type: ignore

    class BFU_OT_FixitTarget(bpy.types.Operator):
        bl_label = "Fix it !"
        bl_idname = "object.fixit_objet"
        bl_description = "Correct target error"
        error_index: bpy.props.IntProperty(default=-1)  # type: ignore

        def execute(self, context: bpy.types.Context | None):
            result = bfu_check_utils.try_to_correct_potential_issues(self.error_index)  # type: ignore
            self.report({'INFO'}, result)
            return {'FINISHED'}

    class BFU_OT_SelectObjectButton(bpy.types.Operator):
        bl_label = "Select(Object)"
        bl_idname = "object.select_error_objet"
        bl_description = "Select target Object."
        error_index: bpy.props.IntProperty(default=-1)  # type: ignore

        def execute(self, context: bpy.types.Context | None):
            bfu_check_utils.select_potential_issue_object(self.error_index)  # type: ignore
            return {'FINISHED'}

    class BFU_OT_SelectVertexButton(bpy.types.Operator):
        bl_label = "Select(Vertex)"
        bl_idname = "object.select_error_vertex"
        bl_description = "Select target Vertex."
        error_index: bpy.props.IntProperty(default=-1)  # type: ignore

        def execute(self, context: bpy.types.Context | None):
            bfu_check_utils.select_potential_issue_vertices(self.error_index)  # type: ignore
            return {'FINISHED'}

    class BFU_OT_SelectPoseBoneButton(bpy.types.Operator):
        bl_label = "Select(PoseBone)"
        bl_idname = "object.select_error_posebone"
        bl_description = "Select target Pose Bone."
        error_index: bpy.props.IntProperty(default=-1)  # type: ignore

        def execute(self, context: bpy.types.Context | None):
            bfu_check_utils.select_potential_issue_pose_bone(self.error_index)  # type: ignore
            return {'FINISHED'}


    def execute(self, context: bpy.types.Context | None):
        return {'FINISHED'}

    def invoke(self, context: bpy.types.Context | None, event: bpy.types.Event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=1020)

    def check(self, context: bpy.types.Context | None):
        return True

    def draw(self, context: bpy.types.Context | None):

        layout = self.layout

        potential_errors = bfu_check_utils.get_potential_errors()
        if len(potential_errors) > 0:
            popup_title = (
                str(len(potential_errors)) +
                " potential error(s) found!")
        else:
            popup_title = "No potential error to correct!"


        layout.label(text=popup_title)
        invoke_info_lines: list[str] = self.invoke_info.split("\n")
        for invoke_info_line in invoke_info_lines:
            layout.label(text="- "+invoke_info_line)
        
        layout.separator()
        row = layout.row()
        col = row.column()
        for x, error in enumerate(potential_errors):
            myLine = col.box().split(factor=0.85)
            # ----
            if error.type == 0:
                msg_type: str = 'INFO'
                msg_icon: str = 'INFO'
            elif error.type == 1:
                msg_type: str = 'WARNING'
                msg_icon: str = 'ERROR'
            elif error.type == 2:
                msg_type: str = 'ERROR'
                msg_icon: str = 'CANCEL'
            else:
                msg_type: str = 'UNKNOWN'
                msg_icon: str = 'QUESTION'
            # ----

            # Text
            TextLine = myLine.column()
            error_full_msg: str = msg_type + ": " + error.text
            splited_texts: list[str] = error_full_msg.split("\n")

            for text, Line in enumerate(splited_texts):
                if (text < 1):

                    if (error.docs_octicon != "None"):  # Doc button

                        url = "https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/How-avoid-potential-errors" + "#" + error.docs_octicon
                        bbpl.blender_layout.layout_doc_button.add_left_doc_page_operator(TextLine, text="More Info", url=url)

                    first_text_line = TextLine.row()
                    first_text_line.label(text=Line, icon=msg_icon)
                else:
                    TextLine.label(text=Line)

            # Select and fix button
            ButtonLine = myLine.column()
            if (error.correct_ref != "None"):
                props = ButtonLine.operator("object.fixit_objet",text=error.correct_label)
                props.error_index = x
            if (error.object is not None):
                if (error.select_object_button):
                    props = ButtonLine.operator("object.select_error_objet")
                    props.error_index = x
                if (error.select_vertex_button):
                    props = ButtonLine.operator("object.select_error_vertex")
                    props.error_index = x
                if (error.select_pose_bone_button):
                    props = ButtonLine.operator("object.select_error_posebone")
                    props.error_index = x



# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_CheckPotentialErrorPopup,
    BFU_OT_OpenPotentialErrorPopup,
    BFU_OT_OpenPotentialErrorPopup.BFU_OT_FixitTarget,
    BFU_OT_OpenPotentialErrorPopup.BFU_OT_SelectObjectButton,
    BFU_OT_OpenPotentialErrorPopup.BFU_OT_SelectVertexButton,
    BFU_OT_OpenPotentialErrorPopup.BFU_OT_SelectPoseBoneButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

