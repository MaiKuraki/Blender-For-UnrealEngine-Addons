# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

import bpy
from ...bfu_check_types import bfu_checker

class BFU_Checker_MarkerOverlay(bfu_checker):

    def __init__(self):
        super().__init__()
        self.check_name = "Marker Overlay"

    # Check that there is no overlap with the markers in the scene timeline
    def run_scene_check(self, scene: bpy.types.Scene):
        used_frames: List[int] = []
        for marker in scene.timeline_markers:
            if marker.frame in used_frames:
                my_po_error = self.add_potential_error()
                my_po_error.type = 2
                my_po_error.text = (
                    f'In the scene timeline, the frame "{marker.frame}" contains overlapping markers.'
                    '\nTo avoid camera conflicts in the generation of the sequencer, '
                    'you must use a maximum of one marker per frame.'
                )
            else:
                used_frames.append(marker.frame)
