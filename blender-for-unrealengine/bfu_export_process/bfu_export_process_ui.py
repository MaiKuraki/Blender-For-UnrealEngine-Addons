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
from .. import bfu_asset_preview
from .. import bfu_addon_prefs


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_export_process_properties_expanded")
    header, panel = accordion.draw(layout)
    if accordion.is_expend():

        # Feedback info :
        bfu_asset_preview.bfu_asset_preview_ui.draw_asset_preview_bar(panel, context)

        # Export button :
        checkButton = panel.row(align=True)
        checkButton.operator("object.checkpotentialerror", icon='FILE_TICK')
        checkButton.operator("object.openpotentialerror", icon='LOOP_BACK', text="")

        exportButton = panel.row()
        exportButton.scale_y = 2.0
        exportButton.operator("object.exportforunreal", icon='EXPORT')

    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_script_tool_expanded")
    header, panel = accordion.draw(layout)
    if accordion.is_expend():
        if addon_prefs.useGeneratedScripts:
            copyButton = panel.row()
            copyButton.operator("object.copy_importassetscript_command")
            copyButton.operator("object.copy_importsequencerscript_command")
            panel.label(text="Click on one of the buttons to copy the import command.", icon='INFO')
            panel.label(text="Then paste it into the cmd console of unreal.")
            panel.label(text="You need activate python plugins in Unreal Engine.")

        else:
            panel.label(text='(Generated scripts are deactivated.)')