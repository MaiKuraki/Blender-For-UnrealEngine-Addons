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
from pathlib import Path
from typing import List, Any, Dict, Optional, TYPE_CHECKING
from . import bfu_export_static_mesh_package
from . import bfu_export_procedure
from .. import bfu_basics
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType, AssetToExport, AssetDataSearchMode
from .. import bbpl
from .. import bfu_socket
from .. import bfu_light_map
from .. import bfu_nanite
from .. import bfu_vertex_color
from .. import bfu_material
from .. import bfu_lod
from .. import bfu_base_object
from .. import bfu_export_nomenclature
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum
from .. import bfu_addon_pref





class BFU_StaticMesh(bfu_assets_manager.bfu_asset_manager_type.BFU_BaseAssetClass):
    def __init__(self):
        super().__init__()
        self.use_lods = True
        self.use_materials = True

    def test_abstract_method(self) -> str:
        return "This is a test method for BFU_StaticMesh class."

# ###################################################################
# # Asset Root Class
# ###################################################################

    def support_asset_type(self, data: Any, details: Any = None) -> bool:
        if not isinstance(data, bpy.types.Object):
            return False
        if details is not None:
            return False
        if data.bfu_export_skeletal_mesh_as_static_mesh:  # type: ignore
            return True
        elif data.bfu_export_as_groom_simulation:  # type: ignore
            return False
        elif data.bfu_export_as_alembic_animation:  # type: ignore
            return False
        elif data.type in ["ARMATURE", "CAMERA"]:  # type: ignore
            return False
        return True

    def get_asset_type(self, data: bpy.types.Object, details: Any = None) -> AssetType:
        return AssetType.STATIC_MESH

    def can_export_asset_type(self) -> bool:
        # Can export the asset for this asset type.
        if bpy.context is None:
            return False

        return bpy.context.scene.bfu_use_static_export  # type: ignore

    def get_asset_import_directory_path(self, data: bpy.types.Object, details: Any = None, extra_path: Optional[Path] = None) -> Path:
        dirpath = bfu_export_nomenclature.bfu_export_nomenclature_utils.get_obj_import_location(data)
        return dirpath if extra_path is None else dirpath / extra_path # Add extra path if provided


# ###################################################################
# # Asset Package Management
# ###################################################################

    def get_package_file_type(self, data: bpy.types.Object, details: Any = None) -> BFU_FileTypeEnum:
        return bfu_export_procedure.get_obj_export_file_type(data)

    def get_package_file_name(self, data: bpy.types.Object, details: Any = None, desired_name: str = "", without_extension: bool = False) -> str:
        # Generate assset file name for skeletal mesh
        
        if TYPE_CHECKING:
            class FakeObject(bpy.types.Object): 
                bfu_use_custom_export_name: str = ""
                bfu_custom_export_name: str = ""
            data = FakeObject()

        # Use custom export name if set
        if data.bfu_use_custom_export_name and data.bfu_custom_export_name:
            if without_extension:
                return bfu_basics.valid_file_name(data.bfu_custom_export_name)
            else:
                return bfu_basics.valid_file_name(data.bfu_custom_export_name + self.get_package_file_type(data).get_file_extension())

        if bpy.context is None:
            return "<Unknown>"
        scene = bpy.context.scene

        if TYPE_CHECKING:
            class FakeScene(bpy.types.Scene):
                bfu_static_mesh_prefix_export_name: str = ""
            scene = FakeScene()

        prefix = scene.bfu_static_mesh_prefix_export_name
        base_name = prefix + (desired_name if desired_name else data.name)

        if without_extension:
            return bfu_basics.valid_file_name(base_name)
        else:
            return bfu_basics.valid_file_name(base_name + self.get_package_file_type(data).get_file_extension())


    def get_package_export_directory_path(self, data: bpy.types.Object, details: Any = None, extra_path: Optional[Path] = None, absolute: bool = True) -> Path:

        if bpy.context is None:
            return Path("<Unknown>")
        scene = bpy.context.scene
        if TYPE_CHECKING:
            class FakeScene(bpy.types.Scene):
                bfu_export_static_file_path: str = ""
            scene = FakeScene()

        if absolute:
            dirpath = Path(bpy.path.abspath(scene.bfu_export_static_file_path))  # type: ignore
        else:
            dirpath = scene.bfu_export_static_file_path
        dirpath /= Path(bfu_export_nomenclature.bfu_export_nomenclature_utils.get_obj_export_folder(data))
        return dirpath if extra_path is None else dirpath / extra_path # Add extra path if provided


# ###################################################################
# # UI
# ###################################################################

    def draw_ui_export_procedure(self, layout: bpy.types.UILayout, context: bpy.types.Context, data: bpy.types.Object) -> bpy.types.UILayout:
        return bfu_export_procedure.draw_object_export_procedure(layout, data)

# ####################################################################
# # Asset Construction
# ####################################################################

    def get_asset_export_content(self, data: bpy.types.Object) -> List[bpy.types.Object]:
        desired_obj_list: List[bpy.types.Object] = []
        desired_obj_list.append(data)
        for child in bbpl.basics.get_recursive_obj_childs(data):
            if bfu_base_object.bfu_export_type.is_auto_or_export_recursive(child):
                if bpy.context:
                    if child.name in bpy.context.window.view_layer.objects:
                        desired_obj_list.append(child)

        return desired_obj_list

    def get_asset_export_data(self, data: bpy.types.Object, details: Any, search_mode: AssetDataSearchMode)-> List[AssetToExport]:
        

        if bpy.context is None:
            return []
        scene = bpy.context.scene
        addon_prefs = bfu_addon_pref.get_addon_prefs()

        if TYPE_CHECKING:
            class FakeScene(bpy.types.Scene):
                bfu_use_static_export: bool = False
                bfu_use_text_additional_data: bool = False
            scene = FakeScene()

            class FakeObject(bpy.types.Object):
                bfu_export_as_lod_mesh: bool = False
            data = FakeObject()

        asset_list: List[AssetToExport] = []
        if scene.bfu_use_static_export:
            if data.bfu_export_as_lod_mesh == False:
                asset = AssetToExport(data.name, AssetType.STATIC_MESH)
                asset_list.append(asset)

                import_dirpath = self.get_asset_import_directory_path(data)
                asset.set_import_name(self.get_package_file_name(data, without_extension=True))
                asset.set_import_dirpath(import_dirpath)

                if search_mode.search_packages():
                    pak = asset.add_asset_package(data.name, ["Lod0"])

                    # Set the export dirpath
                    dirpath = self.get_package_export_directory_path(data, absolute=True)
                    file_name = self.get_package_file_name(data)
                    file_type = self.get_package_file_type(data)
                    pak.set_file(dirpath, file_name, file_type)

                    if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
                        file_name_without_extension = self.get_package_file_name(data, without_extension=True)
                        additional_data = asset.set_asset_additional_data(self.get_asset_additional_data(data))
                        additional_data.set_file(dirpath, f"{file_name_without_extension}_additional_data.json")

                    if search_mode.search_package_content():
                        pak.add_objects(self.get_asset_export_content(data))

                        pak.export_function = bfu_export_static_mesh_package.process_static_mesh_export_from_package

                for i in range(1, 6):
                    target = getattr(data, f"bfu_lod_target{i}", None)
                    if target and target.name in bpy.data.objects:

                        if search_mode.search_packages():
                            target_pak = asset.add_asset_package(target.name, [f"Lod{i}"])

                            if search_mode.search_package_content():
                                target_pak.add_objects(self.get_asset_export_content(target))

                                # Set the export dirpath
                                dirpath = self.get_package_export_directory_path(target, absolute=True)
                                file_name = self.get_package_file_name(target)
                                file_type = self.get_package_file_type(target)
                                target_pak.set_file(dirpath, file_name, file_type)

                                target_pak.export_function = bfu_export_static_mesh_package.process_static_mesh_export_from_package
                            
        return asset_list

    def get_asset_additional_data(self, data: bpy.types.Object) -> Dict[str, Any]:
        additional_data: Dict[str, Any] = {}
        # Sockets
        if data:
            additional_data['Sockets'] = bfu_socket.bfu_socket_utils.get_skeletal_mesh_sockets(data)

        additional_data.update(bfu_lod.bfu_lod_utils.get_lod_additional_data(data, AssetType.STATIC_MESH))
        additional_data.update(bfu_vertex_color.bfu_vertex_color_utils.get_vertex_color_additional_data(data, AssetType.STATIC_MESH))
        additional_data.update(bfu_material.bfu_material_utils.get_material_asset_additional_data(data, AssetType.STATIC_MESH))
        additional_data.update(bfu_light_map.bfu_light_map_utils.get_light_map_additional_data(data, AssetType.STATIC_MESH))
        additional_data.update(bfu_nanite.bfu_nanite_utils.get_nanite_asset_additional_data(data, AssetType.STATIC_MESH))
        return additional_data

# --------------------------------------------
# Register and Unregister functions
# --------------------------------------------

def register():
    my_asset_class = BFU_StaticMesh()
    bfu_assets_manager.bfu_asset_manager_registred_assets.register_asset_class(my_asset_class)

def unregister():
    pass
