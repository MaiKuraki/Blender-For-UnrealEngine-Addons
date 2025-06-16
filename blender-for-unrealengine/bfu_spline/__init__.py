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
import importlib

from . import bfu_export_procedure
from . import bfu_spline_props
from . import bfu_spline_ui
from . import bfu_spline_utils
from . import bfu_spline_unreal_utils
from . import bfu_spline_data
from . import bfu_spline_export_utils
from . import bfu_spline_write_text
from . import bfu_spline_write_paste_commands
from . import bfu_spline_type
from . import bfu_export_spline_package

if "bfu_export_procedure" in locals():
    importlib.reload(bfu_export_procedure)
if "bfu_spline_props" in locals():
    importlib.reload(bfu_spline_props)
if "bfu_spline_ui" in locals():
    importlib.reload(bfu_spline_ui)
if "bfu_spline_utils" in locals():
    importlib.reload(bfu_spline_utils)
if "bfu_spline_unreal_utils" in locals():
    importlib.reload(bfu_spline_unreal_utils)
if "bfu_spline_data" in locals():
    importlib.reload(bfu_spline_data)
if "bfu_spline_export_utils" in locals():
    importlib.reload(bfu_spline_export_utils)
if "bfu_spline_write_text" in locals():
    importlib.reload(bfu_spline_write_text)
if "bfu_spline_write_paste_commands" in locals():
    importlib.reload(bfu_spline_write_paste_commands)
if "bfu_spline_type" in locals():
    importlib.reload(bfu_spline_type)
if "bfu_export_spline_package" in locals():
    importlib.reload(bfu_export_spline_package)

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)  # type: ignore

    bfu_export_procedure.register()
    bfu_spline_props.register()
    bfu_spline_type.register()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)  # type: ignore

    bfu_spline_type.unregister()
    bfu_spline_props.unregister()
    bfu_export_procedure.unregister()