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

try:
    import unreal
except ImportError:
    import unreal_engine as unreal

support_interchange = import_module_unreal_utils.get_support_interchange()


def apply_import_settings(itask: import_module_tasks_class.ImportTaks, asset_data: dict, asset_additional_data: dict) -> None:
    import_module_utils.print_debug_step("Set Nanite import settings.")

    asset_type = asset_data.get("asset_type")
    if asset_type not in ["StaticMesh", "SkeletalMesh"]:
        # Only apply settings for StaticMesh and SkeletalMesh
        return
    
    if "build_nanite" in asset_additional_data:
        build_nanite = asset_additional_data["build_nanite"]

        if itask.use_interchange:
            if asset_type == "StaticMesh":
                if "build_nanite" in asset_additional_data:
                    itask.get_igap_mesh().set_editor_property('build_nanite', build_nanite)
            if asset_type == "SkeletalMesh":
                if "build_nanite" in asset_additional_data:
                    # Unreal Engine 5.5 support Nanite with Skeletal Mesh 
                    # but that was not yet added in Python API.
                    pass
                    #itask.get_igap_mesh().set_editor_property('build_nanite', build_nanite)
        else:
            if asset_type == "StaticMesh":
                if "build_nanite" in asset_additional_data:
                    itask.get_static_mesh_import_data().set_editor_property('build_nanite', build_nanite)
            if asset_type == "SkeletalMesh":
                if "build_nanite" in asset_additional_data:
                    # Unreal Engine 5.5 support Nanite with Skeletal Mesh 
                    # but that was not yet added in Python API.
                    pass
                    #itask.get_static_mesh_import_data().set_editor_property('build_nanite', build_nanite)


def apply_asset_settings(itask: import_module_tasks_class.ImportTaks, asset_additional_data: dict) -> None:
    import_module_utils.print_debug_step("Set Nanite post import settings.")

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
    
    # Apply asset Nanite
    if "build_nanite" in asset_additional_data:
        build_nanite = asset_additional_data["build_nanite"]

        if isinstance(asset, unreal.StaticMesh): 
            nanite_settings = asset.get_editor_property("nanite_settings")
            nanite_settings.enabled = build_nanite
        
            # Apply changes
            static_mesh_subsystem = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
            static_mesh_subsystem.set_nanite_settings(asset, nanite_settings, apply_changes=True)
            
        if isinstance(asset, unreal.SkeletalMesh): 
            # Unreal Engine 5.5 support Nanite with Skeletal Mesh 
            # but that was not yet added in Python API.
            pass
            '''
            nanite_settings = asset.get_editor_property("nanite_settings")
            nanite_settings.enabled = build_nanite
        
            # Apply changes
            skeletal_mesh_subsystem = unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem)
            skeletal_mesh_subsystem.set_nanite_settings(asset, nanite_settings, apply_changes=True)
            '''