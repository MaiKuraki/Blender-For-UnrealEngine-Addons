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
from . import bfu_base_col_props
from . import bfu_base_col_ui
from . import bfu_base_col_utils
from . import bfu_base_cole_type
from . import bfu_export_collection_as_static_mesh_package

if "bfu_export_procedure" in locals():
    importlib.reload(bfu_export_procedure)
if "bfu_base_col_props" in locals():
    importlib.reload(bfu_base_col_props)
if "bfu_base_col_ui" in locals():
    importlib.reload(bfu_base_col_ui)
if "bfu_base_col_utils" in locals():
    importlib.reload(bfu_base_col_utils)
if "bfu_base_cole_type" in locals():
    importlib.reload(bfu_base_cole_type)
if "bfu_export_collection_as_static_mesh_package" in locals():
    importlib.reload(bfu_export_collection_as_static_mesh_package)

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bfu_export_procedure.register()
    bfu_base_col_props.register()
    bfu_base_cole_type.register()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bfu_base_cole_type.unregister()
    bfu_base_col_props.unregister()
    bfu_export_procedure.unregister()