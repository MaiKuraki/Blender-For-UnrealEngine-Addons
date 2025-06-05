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
from enum import Enum
import pathlib
from typing import List, Optional, Tuple, Callable, Any, Dict
from abc import ABC, abstractmethod
from pathlib import Path
from ..bfu_simple_file_type_enum import BFU_FileTypeEnum

class AssetDataSearchMode(Enum):
    FULL = "Full" # Search for all assets data.
    PREVIEW = "Preview" # Search assets data for user interface preview.
    ASSET_NUMBER = "AssetNumber" # Search for asset number.
    
    def search_packages(self):
        if self.value == AssetDataSearchMode.FULL.value:
            return True
        elif self.value == AssetDataSearchMode.PREVIEW.value:
            return True
        elif self.value == AssetDataSearchMode.ASSET_NUMBER.value:
            return False
        else:
            return False
        
    def search_package_content(self):
        if self.value == AssetDataSearchMode.FULL.value:
            return True
        elif self.value == AssetDataSearchMode.PREVIEW.value:
            return False
        elif self.value == AssetDataSearchMode.ASSET_NUMBER.value:
            return False
        else:
            return False

class AssetType(Enum):
    UNKNOWN = "Unknown" # Unknown asset type.
    SKELETAL_MESH = "SkeletalMesh"
    STATIC_MESH = "StaticMesh"
    COLLECTION_AS_STATIC_MESH = "Collection StaticMesh"
    CAMERA = "Camera"
    GROOM_SIMULATION = "GroomSimulation" # Groom simulation.
    SPLINE = "Spline" # Curve and spline objects.
    ANIM_ACTION = "Action" 
    ANIM_POSE = "Pose" # Action but only one frame.
    ANIM_NLA = "NonLinearAnimation" # Non linear animations.
    ANIM_ALEMBIC = "AlembicAnimation" # Alembic animations.

    def get_friendly_name(self):
        if self.value == AssetType.UNKNOWN.value:
            return "Unknown Asset Type"
        elif self.value == AssetType.SKELETAL_MESH.value:
            return "Skeletal Mesh"
        elif self.value == AssetType.STATIC_MESH.value:
            return "Static Mesh"
        elif self.value == AssetType.COLLECTION_AS_STATIC_MESH.value:
            return "Collection Static Mesh"
        elif self.value == AssetType.CAMERA.value:
            return "Camera"
        elif self.value == AssetType.GROOM_SIMULATION.value:
            return "Groom Simulation"
        elif self.value == AssetType.SPLINE.value:
            return "Spline"
        elif self.value == AssetType.ANIM_ACTION.value:
            return "Action Animation"
        elif self.value == AssetType.ANIM_POSE.value:
            return "Pose Animation"
        elif self.value == AssetType.ANIM_NLA.value:
            return "Non Linear Animation"
        elif self.value == AssetType.ANIM_ALEMBIC.value:
            return "Alembic Animation"
        else:
            return "Unknown"    
        
    def get_type_as_string(self):
        if self.value == AssetType.UNKNOWN.value:
            return "Unknown"
        elif self.value == AssetType.SKELETAL_MESH.value:
            return "SkeletalMesh"
        elif self.value == AssetType.STATIC_MESH.value:
            return "StaticMesh"
        elif self.value == AssetType.COLLECTION_AS_STATIC_MESH.value:
            return "CollectionStaticMesh"
        elif self.value == AssetType.CAMERA.value:
            return "Camera"
        elif self.value == AssetType.GROOM_SIMULATION.value:
            return "GroomSimulation"
        elif self.value == AssetType.SPLINE.value:
            return "Spline"
        elif self.value == AssetType.ANIM_ACTION.value:
            return "Action"
        elif self.value == AssetType.ANIM_POSE.value:
            return "Pose"
        elif self.value == AssetType.ANIM_NLA.value:
            return "NonLinearAnimation"
        elif self.value == AssetType.ANIM_ALEMBIC.value:
            return "AlembicAnimation"
        else:
            return "Unknown"

    

    def can_use_frame_range(self) -> bool:
        return self in [
            AssetType.ANIM_ACTION,
            AssetType.ANIM_POSE,
            AssetType.ANIM_NLA,
            AssetType.ANIM_ALEMBIC,
            AssetType.CAMERA
        ]
    
    def can_contain_objects(self) -> bool:
        return self in [
            AssetType.SKELETAL_MESH,
            AssetType.STATIC_MESH,
            AssetType.COLLECTION_AS_STATIC_MESH,
        ]

    def is_skeletal(self) -> bool:
        return self in [
            AssetType.SKELETAL_MESH, 
            AssetType.ANIM_ACTION, 
            AssetType.ANIM_POSE, 
            AssetType.ANIM_NLA
        ]
    
    def is_skeletal_animation(self) -> bool:
        return self in [
            AssetType.ANIM_ACTION, 
            AssetType.ANIM_POSE, 
            AssetType.ANIM_NLA
        ]

class PackageFile:
    def __init__(self, dirpath: Path, filename: str, file_type: BFU_FileTypeEnum = BFU_FileTypeEnum.UNKNOWN):
        self.dirpath: Path = dirpath
        self.filename: str = filename
        self.file_type: BFU_FileTypeEnum = file_type  # Type of the file, e.g., FBX, GLTF, etc.
        self.file_content_type: str = "" # Content type, LOD, MATERIAL, etc.

    def get_full_path(self) -> Path:
        # Return the full path of the package file
        return pathlib.Path(self.dirpath) / self.filename

class AssetPackage:
    def __init__(self, name: str, details: Optional[List[str]] = None):
        self.name: str = name
        self.details: Optional[List[str]] = details
        self.file: Optional[PackageFile] = None
        self.objects: List[bpy.types.Object] = []
        self.collection: Optional[bpy.types.Collection] = None
        self.action: Optional[bpy.types.Action] = None  # Action for animations
        self.export_function: Optional[Callable[..., Any]] = None
        self.frame_range: Optional[Tuple[float, float]] = None  # Frame range for animations, e.g., (start, end)

    def set_file(self, dirpath: Path, filename: str, file_type: BFU_FileTypeEnum) -> PackageFile:
        # Set the package file with the given directory path and filename
        self.file = PackageFile(dirpath, filename, file_type)
        return self.file
    
    def add_object(self, obj: bpy.types.Object) -> None:
        # Add an object to the package
        self.objects.append(obj)

    def add_objects(self, objects: List[bpy.types.Object]) -> None:
        # Add multiple objects to the package
        self.objects.extend(objects)

    def set_collection(self, collection: bpy.types.Collection) -> None:
        # Set the collection for the package
        self.collection = collection

    def set_action(self, action: bpy.types.Action) -> None:
        # Set the action for the package
        self.action = action

    def set_frame_range(self, start: float, end: float) -> None:
        # Set the frame range for animations
        self.frame_range = (start, end)

class AdditionalAssetData:
    def __init__(self, data: Dict[str, Any]):
        self.data: Dict[str, Any] = data
        self.file: Optional[PackageFile] = None

    def set_file(self, dirpath: Path, filename: str) -> PackageFile:
        # Set the additional data file with the given directory path and filename
        self.file = PackageFile(dirpath, filename)
        self.file.file_type = BFU_FileTypeEnum.JSON
        self.file.file_content_type = "ADDITIONAL_DATA"
        return self.file

class AssetToExport:
    def __init__(
        self,
        asset_class: "BFU_BaseAssetClass",
        asset_name: str,
        asset_type: AssetType
    ):
        # Base info
        self.name: str = asset_name
        self.asset_type: AssetType = asset_type
        self.import_name: str = ""
        self.import_dirpath: Path = Path()
        self.original_asset_class: BFU_BaseAssetClass = asset_class

        # Asset Pakages
        self.asset_packages: List[AssetPackage] = []

        # Asset Additional Data:
        self.additional_data: Optional[AdditionalAssetData] = None

    def add_asset_package(self, package_name: str, details: Optional[List[str]] = None) -> AssetPackage:
        # Create a new asset package and add it to the list
        new_package = AssetPackage(package_name, details)
        self.asset_packages.append(new_package)
        return new_package

    def set_asset_additional_data(self, data: Dict[str, Any]) -> AdditionalAssetData:
        # Set the additional data for the asset
        self.additional_data = AdditionalAssetData(data)
        return self.additional_data
    
    def get_primary_asset_package(self) -> Optional[bpy.types.Object]:
        # Get the primary asset package, which is the first one in the list
        if self.asset_packages:
            if len(self.asset_packages) > 0:
                if len(self.asset_packages[0].objects) > 0:
                    return self.asset_packages[0].objects[0]
        return None

    def set_import_name(self, new_import_name: str) -> None:
        self.import_name = new_import_name

    def set_import_dirpath(self, new_import_dirpath: Path) -> None:
        self.import_dirpath = new_import_dirpath

    
class BFU_BaseAssetClass(ABC):
    def __init__(self):
        self.use_lods = False
        self.use_materials = False
        self.use_sockets = False

    
# ###################################################################
# # Asset Root Class
# ###################################################################

    #@abstractmethod
    def support_asset_type(self, data: Any, details: Any = None) -> bool:
        # Used to detect if the data is supported by this asset type.
        return False

    #@abstractmethod
    def get_asset_type(self, data: Any, details: Any = None) -> AssetType:
        return AssetType.UNKNOWN

    #@abstractmethod
    def can_export_asset_type(self) -> bool:
        # Can export the asset for this asset type.
        # Used with scene filters. Export Static Meshes ? Export Skeletal Meshes ? etc.
        return False

    def can_export_asset(self, data: Any) -> bool:
        # Can export this specific asset (data)
        # By default True if the asset type can be exported.
        if not self.can_export_asset_type(): # First type the type before checking the data.
            return False

        return True

    #@abstractmethod
    def get_asset_import_directory_path(self, data: Any, details: Any = None, extra_path: Optional[Path] = None) -> Path:
        return Path()

# ###################################################################
# # Asset Package Management
# ###################################################################

    #@abstractmethod
    def get_package_file_type(self, data: Any, details: Any = None) -> BFU_FileTypeEnum:
        return BFU_FileTypeEnum.UNKNOWN

    #@abstractmethod
    def get_package_file_name(self, data: Any, details: Any = None, desired_name: str = "") -> str:
        return "<Unknown>"

    #@abstractmethod
    def get_package_export_directory_path(self, data: Any, details: Any = None, extra_path: Optional[Path] = None, absolute: bool = True) -> Path:
        return Path()

# ###################################################################
# # UI
# ###################################################################

    def draw_ui_export_procedure(self, layout: bpy.types.UILayout, context: bpy.types.Context, data: Any) -> bpy.types.UILayout:
        # If object supports export procedure, draw the UI for it
        return layout
    
# ####################################################################
# # Asset Construction
# ####################################################################

    def get_asset_export_content(self, data: Any) -> List[Any]:
        return []

    def get_asset_export_data(self, data: Any, details: Any, search_mode: AssetDataSearchMode) -> List[AssetToExport]:
        return []
    
    def get_asset_additional_data(self, data: Any) -> Dict[str, Any]:
        return {}