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

import unreal


def set_sequence_preview_skeletal_mesh(asset: unreal.AnimSequence, origin_skeletal_mesh):
    if origin_skeletal_mesh:
        if asset:
            # @TODO preview_pose_asset doesn’t retarget right now. Need wait update in Unreal Engine Python API.
            asset.get_editor_property('preview_pose_asset')
            pass
            