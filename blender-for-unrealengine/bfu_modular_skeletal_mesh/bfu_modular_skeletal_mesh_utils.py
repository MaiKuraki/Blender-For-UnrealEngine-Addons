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
from . import bfu_modular_skeletal_mesh_type
from .. import bfu_assets_manager
from ..bfu_cached_assets import bfu_cached_assets_types

def get_modular_skeletal_specified_parts_meshs_template(obj) -> bfu_modular_skeletal_mesh_type.BFU_UI_ModularSkeletalSpecifiedPartsMeshs:
    return obj.bfu_modular_skeletal_specified_parts_meshs_template
