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
from . import bfu_alembic_animation_utils
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl

from .. import bfu_static_mesh
from .. import bfu_skeletal_mesh



def draw_general_ui_object(layout: bpy.types.UILayout, obj: bpy.types.Object):
    if obj is None:
        return
    
    scene = bpy.context.scene 
    addon_prefs = bfu_basics.GetAddonPrefs()
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        if scene.bfu_object_properties_expanded.is_expend():
            if obj.bfu_export_type == "export_recursive":
                if bfu_alembic_animation_utils.is_alembic_animation(obj) or bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj) or bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj):
                    if bfu_utils.draw_proxy_propertys(obj):
                        AlembicProp = layout.column()
                        AlembicProp.prop(obj, 'bfu_export_as_alembic_animation')

def draw_ui_object(layout: bpy.types.UILayout, obj: bpy.types.Object):
    if obj is None:
        return
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):            
        scene = bpy.context.scene 
        if bfu_alembic_animation_utils.is_alembic_animation(obj):
            scene.bfu_alembic_properties_expanded.draw(layout)
            if scene.bfu_alembic_properties_expanded.is_expend():
                AlembicProp = layout.column()

                export_procedure_prop = AlembicProp.column()
                export_procedure_prop.prop(obj, 'bfu_alembic_export_procedure')

                AlembicProp.label(text="(Alembic animation are exported with scene position.)")
                AlembicProp.label(text="(Use import script for use the origin position.)")
                AlembicProp.prop(obj, 'bfu_create_sub_folder_with_alembic_name')


def draw_ui_scene(layout: bpy.types.UILayout):
    pass