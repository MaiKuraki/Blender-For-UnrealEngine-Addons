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
from .. import bfu_basics

class AssetDataSearchMode(Enum):
    FULL = "Full" # Search for all assets data.
    PREVIEW = "Preview" # Search assets data for user interface preview.
    ASSET_NUMBER = "AssetNumber" # Search for asset number.
    
    def search_packages(self):
        if self == AssetDataSearchMode.FULL:
            return True
        elif self == AssetDataSearchMode.PREVIEW:
            return True
        elif self == AssetDataSearchMode.ASSET_NUMBER:
            return False
        else:
            return False
        
    def search_package_content(self):
        if self == AssetDataSearchMode.FULL:
            return True
        elif self == AssetDataSearchMode.PREVIEW:
            return False
        elif self == AssetDataSearchMode.ASSET_NUMBER:
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
        if self == AssetType.UNKNOWN:
            return "Unknown Asset Type"
        elif self == AssetType.SKELETAL_MESH:
            return "Skeletal Mesh"
        elif self == AssetType.STATIC_MESH:
            return "Static Mesh"
        elif self == AssetType.COLLECTION_AS_STATIC_MESH:
            return "Collection Static Mesh"
        elif self == AssetType.CAMERA:
            return "Camera"
        elif self == AssetType.GROOM_SIMULATION:
            return "Groom Simulation"
        elif self == AssetType.SPLINE:
            return "Spline"
        elif self == AssetType.ANIM_ACTION:
            return "Action Animation"
        elif self == AssetType.ANIM_POSE:
            return "Pose Animation"
        elif self == AssetType.ANIM_NLA:
            return "Non Linear Animation"
        elif self == AssetType.ANIM_ALEMBIC:
            return "Alembic Animation"
        else:
            return "Unknown"    
        
    def get_type_as_string(self):
        if self == AssetType.UNKNOWN:
            return "Unknown"
        elif self == AssetType.SKELETAL_MESH:
            return "SkeletalMesh"
        elif self == AssetType.STATIC_MESH:
            return "StaticMesh"
        elif self == AssetType.COLLECTION_AS_STATIC_MESH:
            return "CollectionStaticMesh"
        elif self == AssetType.CAMERA:
            return "Camera"
        elif self == AssetType.GROOM_SIMULATION:
            return "GroomSimulation"
        elif self == AssetType.SPLINE:
            return "Spline"
        elif self == AssetType.ANIM_ACTION:
            return "Action"
        elif self == AssetType.ANIM_POSE:
            return "Pose"
        elif self == AssetType.ANIM_NLA:
            return "NonLinearAnimation"
        elif self == AssetType.ANIM_ALEMBIC:
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


class PackageFile:
    def __init__(self, dirpath: str, filename: str, file_type: str = "Unknown"):
        self.dirpath: str = dirpath
        self.filename: str = filename
        self.file_type: str = file_type  # Type of the file, e.g., FBX, GLTF, etc.

    def get_full_path(self) -> str:
        # Return the full path of the package file
        return str(pathlib.Path(self.dirpath) / self.filename)

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

    def set_file(self, dirpath: str, filename: str, file_type: str) -> PackageFile:
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

    def set_file(self, dirpath: str, filename: str) -> PackageFile:
        # Set the additional data file with the given directory path and filename
        self.file = PackageFile(dirpath, filename)
        self.file.file_type = "AdditionalData"
        return self.file

class AssetToExport:
    def __init__(
        self,
        asset_name: str,
        asset_type: AssetType
    ):
        # Base info
        self.name: str = asset_name
        self.asset_type: AssetType = asset_type
        self.import_name: str = ""
        self.import_dirpath: str = ""
        

        # Asset Pakages
        self.asset_pakages: List[AssetPackage] = []

        # Asset Additional Data:
        self.additional_data: Optional[AdditionalAssetData] = None

    def add_asset_package(self, package_name: str, details: Optional[List[str]] = None) -> AssetPackage:
        # Create a new asset package and add it to the list
        new_package = AssetPackage(package_name, details)
        self.asset_pakages.append(new_package)
        return new_package

    def set_asset_additional_data(self, data: Dict[str, Any]) -> AdditionalAssetData:
        # Set the additional data for the asset
        self.additional_data = AdditionalAssetData(data)
        return self.additional_data
    
    def set_import_name(self, new_import_name: str) -> None:
        self.import_name = new_import_name

    def set_import_dirpath(self, new_import_dirpath: str) -> None:
        self.import_dirpath = new_import_dirpath
    
class BFU_BaseAssetClass:
    def __init__(self):
        self.use_lods = False
        self.use_materials = False
        self.use_sockets = False

    def support_asset_type(self, data: Any, details: Any = None) -> bool:
        return False

    def get_asset_type(self, data: Any) -> AssetType:
        return AssetType.UNKNOWN

    def get_asset_export_name(self, data: Any) -> str:
        return ""

    def get_asset_file_name(self, data: Any, details: Any = None, desired_name: str = "") -> str:
        return ""

    def get_asset_export_directory_path(self, data: Any, details: Any = None, extra_path: str = "", absolute: bool = True) -> str:
        return ""

    def get_asset_import_directory_path(self, data: Any, details: Any = None, extra_path: str = "") -> str:
        return ""

    def can_export_asset_type(self) -> bool:
        return False

    def can_export_asset(self, data: Any) -> bool:
        return False

    def get_asset_export_data(self, data: Any, details: Any, search_mode: AssetDataSearchMode) -> List[AssetToExport]:
        return []

    def get_asset_export_content(self, data: Any) -> List[bytes]:
        return []

    def get_asset_additional_data(self, data: Any) -> Dict[str, Any]:
        return {}
    
####################################################################
# UI
####################################################################

    def draw_ui_export_procedure(self, layout: bpy.types.UILayout, context: bpy.types.Context, data: Any) -> bpy.types.UILayout:
        # If object supports export procedure, draw the UI for it
        return layout