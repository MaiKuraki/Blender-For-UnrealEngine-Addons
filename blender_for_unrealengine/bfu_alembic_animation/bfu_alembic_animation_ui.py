# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from . import bfu_alembic_animation_utils
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl

from .. import bfu_static_mesh
from .. import bfu_skeletal_mesh
from .. import bfu_export_control
from .. import bfu_addon_prefs



def draw_general_ui_object(layout: bpy.types.UILayout, obj: bpy.types.Object):
    if obj is None:
        return
    
    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        if scene.bfu_object_properties_expanded.is_expend():
            if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):
                if bfu_alembic_animation_utils.is_alembic_animation(obj) or bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj) or bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj):
                    if bfu_utils.draw_proxy_propertys(obj):
                        AlembicProp = layout.column()
                        AlembicProp.prop(obj, 'bfu_export_as_alembic_animation')

def draw_ui_object(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
    if obj is None:
        return
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):            
        scene = bpy.context.scene 
        if bfu_alembic_animation_utils.is_alembic_animation(obj):
            accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_alembic_properties_expanded")
            _, panel = accordion.draw(layout)
            if accordion.is_expend():
                AlembicProp = panel.column()

                export_procedure_prop = AlembicProp.column()
                export_procedure_prop.prop(obj, 'bfu_alembic_export_procedure')

                AlembicProp.label(text="(Alembic animation are exported with scene position.)")
                AlembicProp.label(text="(Use import script for use the origin position.)")
                AlembicProp.prop(obj, 'bfu_create_sub_folder_with_alembic_name')


def draw_ui_scene(layout: bpy.types.UILayout):
    pass