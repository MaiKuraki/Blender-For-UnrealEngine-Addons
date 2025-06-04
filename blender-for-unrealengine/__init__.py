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



'''
This addons allows to easily export several objects, animation, cameras, [...] at the same time for use in game engines
like Unreal Engine of Unity by removing the usual constraints while respecting engine naming conventions
and a clean tree structure.
It also contains a small toolkit for collisions and sockets.

Asset = Object to export in game engine.
Sub object are object in assets like collision or sockets.

Addon for Blender by Xavier Loux (BleuRaven)
xavierloux.com
xavierloux.loux@gmail.com
'''

try:
    import bpy
    import importlib
    from . import bpl
    from . import bbpl
    from . import bfu_assets_manager
    from . import bfu_asset_preview
    from . import bfu_propertys
    from . import bfu_base_object
    from . import bfu_adv_object
    from . import bfu_base_collection
    from . import bfu_static_mesh
    from . import bfu_skeletal_mesh
    from . import bfu_modular_skeletal_mesh
    from . import bfu_alembic_animation
    from . import bfu_anim_base
    from . import bfu_anim_action
    from . import bfu_anim_action_adv
    from . import bfu_anim_nla
    from . import bfu_anim_nla_adv
    from . import bfu_groom
    from . import bfu_camera
    from . import bfu_spline
    from . import bfu_collision
    from . import bfu_socket
    from . import bfu_material
    from . import bfu_vertex_color
    from . import bfu_lod
    from . import bfu_uv_map
    from . import bfu_light_map
    from . import bfu_nanite
    from . import bfu_assets_references
    from . import bfu_custom_property
    from . import bfu_addon_parts
    from . import bfu_export_nomenclature
    from . import bfu_export_filter
    from . import bfu_export_process
    from . import bfu_export_procedure
    from . import bfu_addon_pref
    from . import bfu_export_logs
    from . import bfu_ui
    from . import bfu_check_potential_error
    from . import bfu_export_text_files
    from . import bfu_basics
    from . import bfu_utils
    from . import bfu_unreal_utils
    from . import bfu_naming
    from . import fbxio
    from . import bfu_export
    from . import bfu_backward_compatibility
    from . import bfu_cached_assets

# Try/Execpt is useful for dev, need to make BBAM automatically add at build time in dev mode.
except Exception as e:
    import traceback
    print("Failed to import addon modules:")
    print("\033[91m" + "---------------------------------" + "\033[0m")
    traceback.print_exc()
    print("\033[91m" + "---------------------------------" + "\033[0m")


if "bpl" in locals():
    importlib.reload(bpl)
if "bbpl" in locals():
    importlib.reload(bbpl)
if "bfu_assets_manager" in locals():
    importlib.reload(bfu_assets_manager)
if "bfu_asset_preview" in locals():
    importlib.reload(bfu_asset_preview)
if "bfu_propertys" in locals():
    importlib.reload(bfu_propertys)
if "bfu_base_object" in locals():
    importlib.reload(bfu_base_object)
if "bfu_adv_object" in locals():
    importlib.reload(bfu_adv_object)
if "bfu_base_collection" in locals():
    importlib.reload(bfu_base_collection)
if "bfu_static_mesh" in locals():
    importlib.reload(bfu_static_mesh)
if "bfu_skeletal_mesh" in locals():
    importlib.reload(bfu_skeletal_mesh)
if "bfu_modular_skeletal_mesh" in locals():
    importlib.reload(bfu_modular_skeletal_mesh)
if "bfu_alembic_animation" in locals():
    importlib.reload(bfu_alembic_animation)
if "bfu_anim_base" in locals():
    importlib.reload(bfu_anim_base)
if "bfu_anim_action" in locals():
    importlib.reload(bfu_anim_action)
if "bfu_anim_action_adv" in locals():
    importlib.reload(bfu_anim_action_adv)
if "bfu_anim_nla" in locals():
    importlib.reload(bfu_anim_nla)
if "bfu_anim_nla_adv" in locals():
    importlib.reload(bfu_anim_nla_adv)
if "bfu_groom" in locals():
    importlib.reload(bfu_groom)
if "bfu_camera" in locals():
    importlib.reload(bfu_camera)
if "bfu_spline" in locals():
    importlib.reload(bfu_spline)
if "bfu_collision" in locals():
    importlib.reload(bfu_collision)
if "bfu_socket" in locals():
    importlib.reload(bfu_socket)
if "bfu_material" in locals():
    importlib.reload(bfu_material)
if "bfu_vertex_color" in locals():
    importlib.reload(bfu_vertex_color)
if "bfu_lod" in locals():
    importlib.reload(bfu_lod)
if "bfu_uv_map" in locals():
    importlib.reload(bfu_uv_map)
if "bfu_light_map" in locals():
    importlib.reload(bfu_light_map)
if "bfu_nanite" in locals():
    importlib.reload(bfu_nanite)
if "bfu_assets_references" in locals():
    importlib.reload(bfu_assets_references)
if "bfu_custom_property" in locals():
    importlib.reload(bfu_custom_property)
if "bfu_addon_parts" in locals():
    importlib.reload(bfu_addon_parts)
if "bfu_export_nomenclature" in locals():
    importlib.reload(bfu_export_nomenclature)
if "bfu_export_filter" in locals():
    importlib.reload(bfu_export_filter)
if "bfu_export_process" in locals():
    importlib.reload(bfu_export_process)
if "bfu_export_procedure" in locals():
    importlib.reload(bfu_export_procedure)
if "bfu_addon_pref" in locals():
    importlib.reload(bfu_addon_pref)
if "bfu_export_logs" in locals():
    importlib.reload(bfu_export_logs)
if "bfu_ui" in locals():
    importlib.reload(bfu_ui)
if "bfu_check_potential_error" in locals():
    importlib.reload(bfu_check_potential_error)
if "bfu_export_text_files" in locals():
    importlib.reload(bfu_export_text_files)
if "bfu_basics" in locals():
    importlib.reload(bfu_basics)
if "bfu_utils" in locals():
    importlib.reload(bfu_utils)
if "bfu_unreal_utils" in locals():
    importlib.reload(bfu_unreal_utils)
if "bfu_naming" in locals():
    importlib.reload(bfu_naming)
if "fbxio" in locals():
    importlib.reload(fbxio)
if "bfu_export" in locals():
    importlib.reload(bfu_export)
if "bfu_backward_compatibility" in locals():
    importlib.reload(bfu_backward_compatibility)
if "bfu_cached_assets" in locals():
    importlib.reload(bfu_cached_assets)

    
class BFUCachedAction(bpy.types.PropertyGroup):
    """
    Represents a cached action for Blender File Utils (BFU).
    """
    name: bpy.props.StringProperty()


classes = (
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bbpl.register()
    bfu_assets_manager.register()
    bfu_asset_preview.register()
    bfu_propertys.register()
    bfu_base_object.register()
    bfu_adv_object.register()
    bfu_base_collection.register()
    bfu_static_mesh.register()
    bfu_skeletal_mesh.register()
    bfu_modular_skeletal_mesh.register()
    bfu_alembic_animation.register()
    bfu_anim_base.register()
    bfu_anim_action.register()
    bfu_anim_action_adv.register()
    bfu_anim_nla.register()
    bfu_anim_nla_adv.register()
    bfu_groom.register()
    bfu_camera.register()
    bfu_spline.register()
    bfu_collision.register()
    bfu_socket.register()
    bfu_material.register()
    bfu_vertex_color.register()
    bfu_lod.register()
    bfu_uv_map.register()
    bfu_light_map.register()
    bfu_nanite.register()
    bfu_assets_references.register()
    bfu_custom_property.register()
    bfu_addon_parts.register()
    bfu_export_nomenclature.register()
    bfu_export_filter.register()
    bfu_export_process.register()
    bfu_export_procedure.register()
    bfu_addon_pref.register()
    bfu_export_logs.register()
    bfu_ui.register()
    bfu_check_potential_error.register()
    bfu_backward_compatibility.register()
    bfu_cached_assets.register()


def unregister():


    bfu_cached_assets.unregister()
    bfu_backward_compatibility.unregister()
    bfu_check_potential_error.unregister()
    bfu_ui.unregister()
    bfu_export_logs.unregister()
    bfu_addon_pref.unregister()
    bfu_export_procedure.unregister()
    bfu_export_process.unregister()
    bfu_export_filter.unregister()
    bfu_export_nomenclature.unregister()
    bfu_addon_parts.unregister()
    bfu_custom_property.unregister()
    bfu_assets_references.unregister()
    bfu_nanite.unregister()
    bfu_light_map.unregister()
    bfu_uv_map.unregister()
    bfu_lod.unregister()
    bfu_vertex_color.unregister()
    bfu_material.unregister()
    bfu_socket.unregister()
    bfu_collision.unregister()
    bfu_spline.unregister()
    bfu_camera.unregister()
    bfu_anim_nla_adv.unregister()
    bfu_anim_nla.unregister()
    bfu_anim_action_adv.unregister()
    bfu_anim_action.unregister()
    bfu_anim_base.unregister()
    bfu_alembic_animation.unregister()
    bfu_groom.unregister()
    bfu_modular_skeletal_mesh.unregister()
    bfu_skeletal_mesh.unregister()
    bfu_static_mesh.unregister()
    bfu_base_collection.unregister()
    bfu_adv_object.unregister()
    bfu_base_object.unregister()
    bfu_propertys.unregister()
    bfu_asset_preview.unregister()
    bfu_assets_manager.unregister()
    bbpl.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)