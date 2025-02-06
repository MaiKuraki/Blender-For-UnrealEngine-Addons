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

try:
    import unreal
except ImportError:
    import unreal_engine as unreal

support_interchange = import_module_unreal_utils.get_support_interchange()

def get_vertex_override_color(asset_additional_data: dict) -> Optional[unreal.LinearColor]:
    """Retrieves the vertex override color from the asset data, if available."""
    if asset_additional_data is None:
        return None

    if "vertex_override_color" in asset_additional_data:
        return unreal.LinearColor(
            asset_additional_data["vertex_override_color"][0],
            asset_additional_data["vertex_override_color"][1],
            asset_additional_data["vertex_override_color"][2]
        )

    return None

if support_interchange:
    def get_interchange_vertex_color_import_option(asset_additional_data: dict) -> Optional[unreal.InterchangeVertexColorImportOption]:
        """Retrieves the vertex color import option based on the asset data and pipeline."""
        if asset_additional_data is None:
            return None

        key = "vertex_color_import_option"
        option_value = asset_additional_data.get(key)

        # For unreal.InterchangeGenericCommonMeshesProperties
        if option_value == "IGNORE":
            return unreal.InterchangeVertexColorImportOption.IVCIO_IGNORE
        elif option_value == "OVERRIDE":
            return unreal.InterchangeVertexColorImportOption.IVCIO_OVERRIDE
        elif option_value == "REPLACE":
            return unreal.InterchangeVertexColorImportOption.IVCIO_REPLACE
        return unreal.InterchangeVertexColorImportOption.IVCIO_REPLACE  # Default


def get_vertex_color_import_option(asset_additional_data: dict) -> Optional[unreal.VertexColorImportOption]:
    """Retrieves the vertex color import option based on the asset data and pipeline."""
    if asset_additional_data is None:
        return None

    key = "vertex_color_import_option"
    option_value = asset_additional_data.get(key)

    # For unreal.FbxStaticMeshImportData
    if option_value == "IGNORE":
        return unreal.VertexColorImportOption.IGNORE
    elif option_value == "OVERRIDE":
        return unreal.VertexColorImportOption.OVERRIDE
    elif option_value == "REPLACE":
        return unreal.VertexColorImportOption.REPLACE
    return unreal.VertexColorImportOption.REPLACE  # Default
    


def apply_import_settings(itask: import_module_tasks_class.ImportTaks, asset_data: dict, asset_additional_data: dict) -> None:
    """Applies vertex color settings during the import process."""

    asset_type = asset_additional_data.get("asset_type")
    if asset_type not in ["StaticMesh", "SkeletalMesh"]:
        # Only apply settings for StaticMesh and SkeletalMesh
        return

    vertex_override_color = get_vertex_override_color(asset_additional_data)
    if itask.use_interchange:
        vertex_color_import_option = get_interchange_vertex_color_import_option(asset_additional_data)
    else:
        vertex_color_import_option = get_vertex_color_import_option(asset_additional_data)

    if itask.use_interchange:
        itask.get_igap_common_mesh().set_editor_property('vertex_color_import_option', vertex_color_import_option)
        if vertex_override_color:
            itask.get_igap_common_mesh().set_editor_property('vertex_override_color', vertex_override_color.to_rgbe())
    else:
        if asset_type == "StaticMesh":
            itask.get_static_mesh_import_data().set_editor_property('vertex_color_import_option', vertex_color_import_option)
            if vertex_override_color:
                itask.get_static_mesh_import_data().set_editor_property('vertex_override_color', vertex_override_color.to_rgbe())

        elif asset_type == "SkeletalMesh":
            itask.get_skeletal_mesh_import_data().set_editor_property('vertex_color_import_option', vertex_color_import_option)
            if vertex_override_color:
                itask.get_skeletal_mesh_import_data().set_editor_property('vertex_override_color', vertex_override_color.to_rgbe())


def apply_asset_settings(itask: import_module_tasks_class.ImportTaks, asset_additional_data: dict) -> None:
    """Applies vertex color settings to an already imported asset."""

    # Check   
    static_mesh = itask.get_imported_static_mesh()
    skeletal_mesh = itask.get_imported_skeletal_mesh()

    # Loop for static and skeletal meshs
    for asset in [static_mesh, skeletal_mesh]:
        if asset:
            apply_one_asset_settings(itask, asset, asset_additional_data)


def apply_one_asset_settings(itask: import_module_tasks_class.ImportTaks, asset: unreal.Object, asset_additional_data: dict) -> None:
    """Applies vertex color settings to an already imported asset."""

    # Check   
    if asset is None:
        return

    vertex_override_color = get_vertex_override_color(asset_additional_data)
    if itask.use_interchange:
        vertex_color_import_option = get_interchange_vertex_color_import_option(asset_additional_data)
    else:
        vertex_color_import_option = get_vertex_color_import_option(asset_additional_data)

    if itask.use_interchange:
        common_meshes_properties = asset.get_editor_property('asset_import_data').get_pipelines()[0].get_editor_property('common_meshes_properties')
        if vertex_override_color:
            common_meshes_properties.set_editor_property('vertex_override_color', vertex_override_color.to_rgbe())
        if vertex_color_import_option:
            common_meshes_properties.set_editor_property('vertex_color_import_option', vertex_color_import_option)
    else:
        asset_import_data = asset.get_editor_property('asset_import_data')
        if vertex_override_color:
            asset_import_data.set_editor_property('vertex_override_color', vertex_override_color.to_rgbe())
        if vertex_color_import_option:
            asset_import_data.set_editor_property('vertex_color_import_option', vertex_color_import_option)