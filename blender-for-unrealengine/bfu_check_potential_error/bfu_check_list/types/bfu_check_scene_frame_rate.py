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

class BFU_Checker_SceneFrameRate(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Scene Frame Rate"

    def run_scene_check(self, scene: bpy.types.Scene):
        # Check Scene Frame Rate.
        denominator = scene.render.fps_base
        numerator = scene.render.fps

        # Ensure denominator and numerator are at least 1 and int 32
        new_denominator = max(round(denominator), 1)
        new_numerator = max(round(numerator), 1)

        if denominator != new_denominator or numerator != new_numerator:
            message = (
                'Frame rate denominator and numerator must be an int32 over zero.\n'
                'Float denominator and numerator is not supported in Unreal Engine Sequencer.\n'
                f'- Denominator: {denominator} -> {new_denominator}\n'
                f'- Numerator: {numerator} -> {new_numerator}'
            )

            my_po_error = self.add_potential_error()
            my_po_error.name = scene.name
            my_po_error.type = 2
            my_po_error.text = message
            my_po_error.docs_octicon = 'scene-frame-rate'
