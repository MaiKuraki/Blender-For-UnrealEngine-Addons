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
from ...bfu_check_types import bfu_checker
from .... import bfu_basics
from .... import bfu_utils
from .... import bbpl
from .... import bfu_addon_pref

class BFU_Checker_UnitScale(bfu_checker):
    
    def __init__(self):
        super().__init__()
        self.check_name = "Unit Scale"

    def run_check(self):
        addon_prefs = bfu_basics.GetAddonPrefs()

        # Check if the unit scale is equal to 0.01.
        if addon_prefs.notifyUnitScalePotentialError:
            if not bfu_utils.get_scene_unit_scale_is_close(0.01):
                str_unit_scale = str(bfu_utils.get_scene_unit_scale())
                my_po_error = self.add_potential_error()
                my_po_error.name = bpy.context.scene.name
                my_po_error.type = 1
                my_po_error.text = (f'Scene "{bpy.context.scene.name}" has a Unit Scale equal to {str_unit_scale}.')
                my_po_error.text += ('\nFor Unreal, a unit scale equal to 0.01 is recommended.')
                my_po_error.text += ('\n(You can disable this potential error in the addon preferences.)')
                my_po_error.object = None
                my_po_error.correctRef = "SetUnrealUnit"
                my_po_error.correctlabel = 'Set Unreal Unit'
        