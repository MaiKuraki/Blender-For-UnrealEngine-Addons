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
from . import bfu_light_map_utils
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl
from .. import bfu_static_mesh
from .. import bfu_base_object


def draw_obj_ui(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):

    scene = bpy.context.scene 
    addon_prefs = bfu_basics.GetAddonPrefs()

    # Hide filters
    if obj is None:
        return
    is_static_mesh = bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj)
    if addon_prefs.useGeneratedScripts is False:
        return
    if not bfu_utils.draw_proxy_propertys(obj):
        return
    if bfu_base_object.bfu_export_type.is_not_export_recursive(obj):
        return
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "MISC"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_object_light_map_properties_expanded")
        header, panel = accordion.draw(layout)
        if accordion.is_expend():
            if is_static_mesh:
                StaticMeshLightMapRes = panel.box()
                StaticMeshLightMapRes.prop(obj, 'bfu_static_mesh_light_map_mode')
                if obj.bfu_static_mesh_light_map_mode == "CustomMap":
                    CustomLightMap = StaticMeshLightMapRes.column()
                    CustomLightMap.prop(obj, 'bfu_static_mesh_custom_light_map_res')
                if obj.bfu_static_mesh_light_map_mode == "SurfaceArea":
                    SurfaceAreaLightMap = StaticMeshLightMapRes.column()
                    SurfaceAreaLightMapButton = SurfaceAreaLightMap.row()
                    SurfaceAreaLightMapButton.operator("object.comput_lightmap", icon='TEXTURE')
                    SurfaceAreaLightMapButton.operator("object.comput_all_lightmap", icon='TEXTURE')
                    SurfaceAreaLightMap.prop(obj, 'bfu_use_static_mesh_light_map_world_scale')
                    SurfaceAreaLightMap.prop(obj, 'bfu_static_mesh_light_map_surface_scale')
                    SurfaceAreaLightMap.prop(obj, 'bfu_static_mesh_light_map_round_power_of_two')
                if obj.bfu_static_mesh_light_map_mode != "Default":
                    CompuntedLightMap = str(bfu_light_map_utils.GetCompuntedLightMap(obj))
                    StaticMeshLightMapRes.label(text='Compunted light map: ' + CompuntedLightMap)
                bfu_generate_light_map_uvs = panel.row()
                bfu_generate_light_map_uvs.prop(obj, 'bfu_generate_light_map_uvs')

def draw_tools_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_tools_light_map_properties_expanded")
    header, panel = accordion.draw(layout)
    if accordion.is_expend():
        checkButton = panel.column()
        checkButton.operator("object.comput_all_lightmap", icon='TEXTURE')