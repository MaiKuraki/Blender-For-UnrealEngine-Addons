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
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl
from .. import bfu_skeletal_mesh
from .. import bfu_alembic_animation
from .. import bfu_cached_assets
from .. import bfu_export_control
from .. import bfu_addon_prefs


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):
    
    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Hide filters
    if obj is None:
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "ANIM"):
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_animation_advanced_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():
            # Animation fbx properties
            if bfu_alembic_animation.bfu_alembic_animation_utils.is_not_alembic_animation(obj):
                propsFbx = panel.row()
                propsFbx.prop(obj, 'bfu_sample_anim_for_export')
                propsFbx.prop(obj, 'bfu_simplify_anim_for_export')

            props_scale_animation = panel.column()
            props_scale_animation.prop(obj, "bfu_disable_free_scale_animation")

            props_animation_mesh = panel.column()
            props_animation_mesh.prop(obj, "bfu_export_animation_without_mesh")

            props_animation_materials = panel.column()
            props_animation_materials.prop(obj, "bfu_export_animation_without_materials")
            props_animation_materials.enabled = not obj.bfu_export_animation_without_mesh

            props_animation_textures = panel.column()
            props_animation_textures.prop(obj, "bfu_export_animation_without_textures")
            props_animation_textures.enabled = not obj.bfu_export_animation_without_materials and not obj.bfu_export_animation_without_mesh

def draw_animation_tab_footer_ui(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):

    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Hide filters
    if obj is None:
        return
    if not bfu_utils.draw_proxy_propertys(obj):
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    if bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_not_skeletal_mesh(obj):
        return
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "ANIM"):
        # Armature export action list feedback
        layout.label(
            text='Note: The Action with only one' +
            ' frame are exported like Pose.')
        ArmaturePropertyInfo = (
            layout.row().box().split(factor=0.75)
            )
        animation_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.get_animation_asset_cache(obj)
        animation_to_export = animation_asset_cache.get_animation_asset_list()
        ActionNum = len(animation_to_export)
        if obj.bfu_anim_nla_use:
            ActionNum += 1
        actionFeedback = (
            str(ActionNum) +
            " Animation(s) will be exported with this object.")
        ArmaturePropertyInfo.label(
            text=actionFeedback,
            icon='INFO')
        ArmaturePropertyInfo.operator("object.showobjaction")
