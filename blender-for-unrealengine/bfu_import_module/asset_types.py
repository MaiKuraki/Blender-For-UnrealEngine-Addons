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

# Export asset types from Blender
from enum import Enum

class ExportAssetType(Enum):
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
        if self == ExportAssetType.UNKNOWN:
            return "Unknown Asset Type"
        elif self == ExportAssetType.SKELETAL_MESH:
            return "Skeletal Mesh"
        elif self == ExportAssetType.STATIC_MESH:
            return "Static Mesh"
        elif self == ExportAssetType.COLLECTION_AS_STATIC_MESH:
            return "Collection Static Mesh"
        elif self == ExportAssetType.CAMERA:
            return "Camera"
        elif self == ExportAssetType.GROOM_SIMULATION:
            return "Groom Simulation"
        elif self == ExportAssetType.SPLINE:
            return "Spline"
        elif self == ExportAssetType.ANIM_ACTION:
            return "Action Animation"
        elif self == ExportAssetType.ANIM_POSE:
            return "Pose Animation"
        elif self == ExportAssetType.ANIM_NLA:
            return "Non Linear Animation"
        elif self == ExportAssetType.ANIM_ALEMBIC:
            return "Alembic Animation"
        else:
            return "Unknown"    
        
    def get_type_as_string(self):
        if self == ExportAssetType.UNKNOWN:
            return "Unknown"
        elif self == ExportAssetType.SKELETAL_MESH:
            return "SkeletalMesh"
        elif self == ExportAssetType.STATIC_MESH:
            return "StaticMesh"
        elif self == ExportAssetType.COLLECTION_AS_STATIC_MESH:
            return "CollectionStaticMesh"
        elif self == ExportAssetType.CAMERA:
            return "Camera"
        elif self == ExportAssetType.GROOM_SIMULATION:
            return "GroomSimulation"
        elif self == ExportAssetType.SPLINE:
            return "Spline"
        elif self == ExportAssetType.ANIM_ACTION:
            return "Action"
        elif self == ExportAssetType.ANIM_POSE:
            return "Pose"
        elif self == ExportAssetType.ANIM_NLA:
            return "NonLinearAnimation"
        elif self == ExportAssetType.ANIM_ALEMBIC:
            return "AlembicAnimation"
        else:
            return "Unknown"
        
    def get_asset_type_from_string(asset_type_str: str) -> 'ExportAssetType':
        for asset_type in ExportAssetType:
            if asset_type.value == asset_type_str:
                return asset_type
        return ExportAssetType.UNKNOWN
    
    def is_skeletal(self) -> bool:
        return self in [
            ExportAssetType.SKELETAL_MESH, 
            ExportAssetType.ANIM_ACTION, 
            ExportAssetType.ANIM_POSE, 
            ExportAssetType.ANIM_NLA
        ]
    
    def is_skeletal_animation(self) -> bool:
        return self in [
            ExportAssetType.ANIM_ACTION, 
            ExportAssetType.ANIM_POSE, 
            ExportAssetType.ANIM_NLA
        ]