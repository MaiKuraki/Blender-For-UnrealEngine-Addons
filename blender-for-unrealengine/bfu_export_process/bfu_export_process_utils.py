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
from .. import bpl
from .. import bbpl
from .. import bfu_export_logs


def print_exported_asset_detail():
    bpl.advprint.print_simple_title("Exported asset(s)")
    print("")
    lines = bfu_export_logs.bfu_asset_export_logs_utils.get_export_asset_logs_details().splitlines()
    for line in lines:
        print(line)
    print("")
    bpl.advprint.print_simple_title("Export time details")
    print("")
    lines = bfu_export_logs.bfu_process_time_logs_utils.get_process_time_logs_details().splitlines()
    for line in lines:
        print(line)
    print("")
    bpl.advprint.print_separator()