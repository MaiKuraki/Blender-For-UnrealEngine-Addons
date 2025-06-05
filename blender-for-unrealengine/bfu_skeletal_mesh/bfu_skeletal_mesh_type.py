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
from typing import List, Any, Dict
from . import bfu_export_skeletal_mesh_package
from .. import bfu_assets_manager
from ..bfu_assets_manager.bfu_asset_manager_type import AssetType, AssetToExport, AssetDataSearchMode
from .. import bfu_utils
from .. import bfu_basics
from .. import bbpl
from .. import bfu_modular_skeletal_mesh
from . import bfu_export_procedure
from .. import bfu_socket
from .. import bfu_light_map
from .. import bfu_nanite
from .. import bfu_vertex_color
from .. import bfu_material
from .. import bfu_lod
from .. import bfu_base_object


class BFU_SkeletalMesh(bfu_assets_manager.bfu_asset_manager_type.BFU_BaseAssetClass):
    def __init__(self):
        super().__init__()
        self.use_materials = True

    def support_asset_type(self, obj: bpy.types.Object, details: Any = None) -> bool:
        if not isinstance(obj, bpy.types.Object):
            return False
        if obj.type == "ARMATURE" and not obj.bfu_export_skeletal_mesh_as_static_mesh:
            if details == None:
                return True
        return False

    def get_asset_type(self, obj: bpy.types.Object, details: Any = None) -> AssetType:
        return AssetType.SKELETAL_MESH

    def get_asset_export_name(self, obj: bpy.types.Object) -> str:
        if not isinstance(obj, bpy.types.Object):
            return False
        if bfu_utils.GetExportAsProxy(obj):
            proxy_child = bfu_utils.GetExportProxyChild(obj)
            if proxy_child is not None:
                return bfu_basics.ValidFilename(proxy_child.name)
        return bfu_basics.ValidFilename(obj.name)

    def get_asset_file_type(self, obj: bpy.types.Object, details: Any = None) -> str:
        return bfu_export_procedure.get_obj_export_file_type(obj)

    def get_asset_file_name(self, obj: bpy.types.Object, details: Any = None, desired_name: str = "", without_extension: bool = False) -> str:
        # Generate assset file name for skeletal mesh
        scene = bpy.context.scene
        if obj.bfu_use_custom_export_name:
            if obj.bfu_custom_export_name:
                return obj.bfu_custom_export_name
            
        if without_extension:
            fileType = ""
        else:
            asset_type = self.get_asset_file_type(obj)
            if asset_type == "FBX":
                fileType = ".fbx"
            elif asset_type == "GLTF":
                fileType = ".glb"


        if desired_name:
            return bfu_basics.ValidFilename(scene.bfu_skeletal_mesh_prefix_export_name+desired_name+fileType)
        return bfu_basics.ValidFilename(scene.bfu_skeletal_mesh_prefix_export_name+obj.name+fileType)

    def get_asset_export_directory_path(self, obj: bpy.types.Object, extra_path: str = "", absolute: bool = True) -> str:
        scene = bpy.context.scene

        # Get root path
        if absolute:
            root_path = Path(bpy.path.abspath(scene.bfu_export_skeletal_file_path))
        else:
            root_path = Path(scene.bfu_export_skeletal_file_path)
    
        # Add obj folder path
        folder_name = bfu_utils.get_export_folder_name(obj)
        dirpath = root_path / folder_name

        # Add skeletal sub folder path
        if obj.bfu_create_sub_folder_with_skeletal_mesh_name:
            dirpath = dirpath / self.get_asset_export_name(obj)

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)
    
    def get_asset_import_directory_path(self, obj, extra_path = ""):
        scene = bpy.context.scene

        # Get root path
        root_path = Path(scene.bfu_unreal_import_module)

        # Add skeletal subfolder path
        dirpath = root_path / scene.bfu_unreal_import_location / obj.bfu_export_folder_name

        # Add extra path if provided
        if extra_path:
            dirpath = dirpath / extra_path

        # Clean path and return as string
        return str(dirpath)
    
    def get_meshs_object_for_skeletal_mesh(self, obj):
        meshs = []
        if self.support_asset_type(obj):  # Skeleton /  Armature
            childs = bfu_utils.GetExportDesiredChilds(obj)
            for child in childs:
                if child.type == "MESH":
                    meshs.append(child)
        return meshs

    def can_export_asset_type(self):
        scene = bpy.context.scene
        return scene.bfu_use_skeletal_export

    def can_export_asset(self, obj):
        return self.can_export_asset_type()
    
    def get_asset_export_data(self, obj: bpy.types.Object, details: Any, search_mode: AssetDataSearchMode) -> List[AssetToExport]:
        asset_list = []
        scene = bpy.context.scene
        addon_prefs = bfu_basics.GetAddonPrefs()

        
        if scene.bfu_use_skeletal_export:
            # Export the armature and all mesh as a single skeletal mesh
            if obj.bfu_modular_skeletal_mesh_mode == "all_in_one":
                asset = AssetToExport(obj.name, AssetType.SKELETAL_MESH)
                asset_list.append(asset)

                import_dirpath = self.get_asset_import_directory_path(obj)
                asset.set_import_name(self.get_asset_file_name(obj, without_extension=True))
                asset.set_import_dirpath(import_dirpath)

                if search_mode.search_packages():
                    pak = asset.add_asset_package(obj.name, ["Lod0"])

                    # Set the export dirpath
                    dirpath = self.get_asset_export_directory_path(obj, "", True)
                    file_name = self.get_asset_file_name(obj)
                    file_type = self.get_asset_file_type(obj)
                    pak.set_file(dirpath, file_name, file_type)

                    if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
                        file_name_without_extension = self.get_asset_file_name(obj, without_extension=True)
                        additional_data = asset.set_asset_additional_data(self.get_asset_additional_data(obj))
                        additional_data.set_file(dirpath, f"{file_name_without_extension}_additional_data.json")

                    if search_mode.search_package_content():

                        pak.add_objects(self.get_asset_export_content(obj))

                        pak.export_function = bfu_export_skeletal_mesh_package.process_skeletal_mesh_export_from_package

            # Export each mesh as a separate skeletal mesh
            elif obj.bfu_modular_skeletal_mesh_mode == "every_meshs":
                for mesh in bbpl.basics.get_obj_childs(obj):
                    asset_name = obj.name + obj.bfu_modular_skeletal_mesh_every_meshs_separate + mesh.name
                    asset = AssetToExport(asset_name, AssetType.SKELETAL_MESH)
                    asset_list.append(asset)

                    import_dirpath = self.get_asset_import_directory_path(obj)
                    asset.set_import_name(self.get_asset_file_name(mesh, without_extension=True))
                    asset.set_import_dirpath(import_dirpath)

                    if search_mode.search_packages():
                        pak = asset.add_asset_package(mesh.name, ["Lod0"])

                        # Set the export dirpath
                        dirpath = self.get_asset_export_directory_path(mesh, "", True)
                        file_name = self.get_asset_file_name(mesh)
                        file_type = self.get_asset_file_type(mesh)
                        pak.set_file(dirpath, file_name, file_type)

                        if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
                            file_name_without_extension = self.get_asset_file_name(mesh, without_extension=True)
                            additional_data = asset.set_asset_additional_data(self.get_asset_additional_data(mesh))
                            additional_data.set_file(dirpath, f"{file_name_without_extension}_additional_data.json")

                        if search_mode.search_package_content():

                            pak.add_object(mesh)

                            pak.export_function = bfu_export_skeletal_mesh_package.process_skeletal_mesh_export_from_package

            # Export specified parts of the modular skeletal mesh
            elif obj.bfu_modular_skeletal_mesh_mode == "specified_parts":
                
                template = bfu_modular_skeletal_mesh.bfu_modular_skeletal_mesh_utils.get_modular_skeletal_specified_parts_meshs_template(obj)
                for part in template.get_template_collection():
                    if part.enabled:
                        asset = AssetToExport(part.name, AssetType.SKELETAL_MESH)
                        asset_list.append(asset)
                        
                        import_dirpath = self.get_asset_import_directory_path(obj, part.sub_folder)
                        asset.set_import_name(self.get_asset_file_name(obj, desired_name=part.name, without_extension=True))
                        asset.set_import_dirpath(import_dirpath)

                        if search_mode.search_packages():
                            pak = asset.add_asset_package(obj.name, ["Lod0"])

                            # Set the export dirpath
                            dirpath = self.get_asset_export_directory_path(obj, part.sub_folder, True)
                            file_name = self.get_asset_file_name(obj, part.name)
                            file_type = self.get_asset_file_type(obj)
                            pak.set_file(dirpath, file_name, file_type)

                            if (scene.bfu_use_text_additional_data and addon_prefs.useGeneratedScripts):
                                file_name_without_extension = self.get_asset_file_name(obj, desired_name=part.name, without_extension=True)
                                additional_data = asset.set_asset_additional_data(self.get_asset_additional_data(obj))
                                additional_data.set_file(dirpath, f"{file_name_without_extension}_additional_data.json")

                            if search_mode.search_package_content():

                                for skeletal_part in part.skeletal_parts.get_template_collection():
                                    if skeletal_part.enabled:
                                        if skeletal_part.target_type == 'OBJECT':  # Utilisez l'attribut target_type
                                            if skeletal_part.obj:
                                                if bfu_base_object.bfu_export_type.is_auto_or_export_recursive(skeletal_part.obj):
                                                    pak.add_object(skeletal_part.obj)
                                        elif skeletal_part.target_type == 'COLLECTION':
                                            if skeletal_part.collection:
                                                for collection_obj in skeletal_part.collection.objects:
                                                    if bfu_base_object.bfu_export_type.is_auto_or_export_recursive(collection_obj):
                                                        pak.add_object(collection_obj)
                        
                                pak.export_function = bfu_export_skeletal_mesh_package.process_skeletal_mesh_export_from_package

        return asset_list

    def get_asset_export_content(self, obj: bpy.types.Object) -> List[bpy.types.Object]:
        desired_obj_list = []
        desired_obj_list.append(obj)
        for child in bbpl.basics.get_recursive_obj_childs(obj):
            if bfu_base_object.bfu_export_type.is_auto_or_export_recursive(child):
                if child.name in bpy.context.window.view_layer.objects:
                    desired_obj_list.append(child)

        return desired_obj_list

    def get_asset_additional_data(self, obj: bpy.types.Object) -> Dict[str, Any]:
        data = {}
        # Sockets
        if obj:
            data['Sockets'] = bfu_socket.bfu_socket_utils.get_skeletal_mesh_sockets(obj)
        

        data.update(bfu_lod.bfu_lod_utils.get_lod_additional_data(obj, AssetType.STATIC_MESH))
        data.update(bfu_vertex_color.bfu_vertex_color_utils.get_vertex_color_additional_data(obj, AssetType.STATIC_MESH))
        data.update(bfu_material.bfu_material_utils.get_material_asset_additional_data(obj, AssetType.STATIC_MESH))
        data.update(bfu_light_map.bfu_light_map_utils.get_light_map_additional_data(obj, AssetType.STATIC_MESH))
        data.update(bfu_nanite.bfu_nanite_utils.get_nanite_asset_additional_data(obj, AssetType.STATIC_MESH))
        return data

####################################################################
# UI
####################################################################

    def draw_ui_export_procedure(self, layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object) -> bpy.types.UILayout:
        return bfu_export_procedure.draw_object_export_procedure(layout, obj)
    

# --------------------------------------------
# Register and Unregister functions
# --------------------------------------------


def register():
    bfu_assets_manager.bfu_asset_manager_registred_assets.register_asset_class(BFU_SkeletalMesh())

def unregister():
    pass