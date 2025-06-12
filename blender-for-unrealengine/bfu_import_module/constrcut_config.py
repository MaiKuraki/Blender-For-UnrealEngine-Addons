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

from typing import Tuple

interchange_minimal_support: Tuple[int, int, int] = (5, 1, 0) # Minimum UE version for Interchange support (5.1.0)
print("interchange_minimal_support ->", interchange_minimal_support)

# DEBUG
force_use_interchange = "Auto" # "Auto" by default. You can use "Auto", "Interchange" or "FBX" for debug.