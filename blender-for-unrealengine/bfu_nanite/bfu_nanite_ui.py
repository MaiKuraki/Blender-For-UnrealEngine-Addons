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
from . import bfu_nanite_utils
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl
from .. import bfu_static_mesh
from .. import bfu_skeletal_mesh

def draw_obj_ui(layout: bpy.types.UILayout, obj: bpy.types.Object):

    scene = bpy.context.scene 
    addon_prefs = bfu_basics.GetAddonPrefs()

    # Hide filters
    if obj is None:
        return
    if addon_prefs.useGeneratedScripts is False:
        return
    if not bfu_utils.draw_proxy_propertys(obj):
        return
    if obj.bfu_export_type != "export_recursive":
        return
    
    is_static_mesh = bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj)
    is_skeletal_mesh = bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj)
    if is_static_mesh == False and is_skeletal_mesh == False:
        return # Check only static and skeletal meshs for the moment.

    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "MISC"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_object_nanite_properties_expanded")
        header, panel = accordion.draw(layout)
        if accordion.is_expend():
            panel.prop(obj, 'bfu_build_nanite_mode')

