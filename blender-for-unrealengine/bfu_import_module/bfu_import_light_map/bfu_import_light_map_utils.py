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

from typing import Optional
from .. import import_module_unreal_utils
from .. import import_module_tasks_class
from .. import import_module_utils
from ..asset_types import ExportAssetType

try:
    import unreal
except ImportError:
    import unreal_engine as unreal

support_interchange = import_module_unreal_utils.get_support_interchange()


def apply_import_settings(itask: import_module_tasks_class.ImportTaks, asset_data: dict, asset_additional_data: dict) -> None:
    import_module_utils.print_debug_step("Set Light Map import settings.")

    asset_type = ExportAssetType.get_asset_type_from_string(asset_data.get("asset_type"))
    if asset_type not in [ExportAssetType.STATIC_MESH]:
        # Only apply settings for StaticMesh and SkeletalMesh
        return

    if itask.use_interchange:
        if asset_type == ExportAssetType.STATIC_MESH:
            if "generate_lightmap_u_vs" in asset_additional_data:
                itask.get_igap_mesh().set_editor_property('generate_lightmap_u_vs', asset_additional_data["generate_lightmap_u_vs"])
    else:
        if asset_type == ExportAssetType.STATIC_MESH:
            if "generate_lightmap_u_vs" in asset_additional_data:
                itask.get_static_mesh_import_data().set_editor_property('generate_lightmap_u_vs', asset_additional_data["generate_lightmap_u_vs"])


def apply_asset_settings(itask: import_module_tasks_class.ImportTaks, asset_additional_data: dict) -> None:
    import_module_utils.print_debug_step("Set Light Map post import settings.")

    # Check   
    static_mesh = itask.get_imported_static_mesh()
    if static_mesh is None:
        return
    
    if "use_custom_light_map_resolution" in asset_additional_data:
        if asset_additional_data["use_custom_light_map_resolution"]:
            if "light_map_resolution" in asset_additional_data:
                static_mesh.set_editor_property('light_map_resolution', asset_additional_data["light_map_resolution"])
                build_settings = unreal.EditorStaticMeshLibrary.get_lod_build_settings(static_mesh, 0)
                build_settings.min_lightmap_resolution = asset_additional_data["light_map_resolution"]
                unreal.EditorStaticMeshLibrary.set_lod_build_settings(static_mesh, 0, build_settings)

    if itask.use_interchange:
        if "generate_lightmap_u_vs" in asset_additional_data:
            mesh_pipeline = static_mesh.get_editor_property('asset_import_data').get_pipelines()[0].get_editor_property('mesh_pipeline')
            mesh_pipeline.set_editor_property('generate_lightmap_u_vs', asset_additional_data["generate_lightmap_u_vs"])  # Import data
            unreal.EditorStaticMeshLibrary.set_generate_lightmap_uv(static_mesh, asset_additional_data["generate_lightmap_u_vs"])  # Build settings at lod

    else:
        asset_import_data = static_mesh.get_editor_property('asset_import_data')
        if "generate_lightmap_u_vs" in asset_additional_data:
            asset_import_data.set_editor_property('generate_lightmap_u_vs', asset_additional_data["generate_lightmap_u_vs"])  # Import data
            unreal.EditorStaticMeshLibrary.set_generate_lightmap_uv(static_mesh, asset_additional_data["generate_lightmap_u_vs"])  # Build settings at lod
