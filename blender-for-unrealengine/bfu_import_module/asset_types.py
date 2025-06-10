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
        if self.value == ExportAssetType.UNKNOWN.value:
            return "Unknown Asset Type"
        elif self.value == ExportAssetType.SKELETAL_MESH.value:
            return "Skeletal Mesh"
        elif self.value == ExportAssetType.STATIC_MESH.value:
            return "Static Mesh"
        elif self.value == ExportAssetType.COLLECTION_AS_STATIC_MESH.value:
            return "Collection Static Mesh"
        elif self.value == ExportAssetType.CAMERA.value:
            return "Camera"
        elif self.value == ExportAssetType.GROOM_SIMULATION.value:
            return "Groom Simulation"
        elif self.value == ExportAssetType.SPLINE.value:
            return "Spline"
        elif self.value == ExportAssetType.ANIM_ACTION.value:
            return "Action Animation"
        elif self.value == ExportAssetType.ANIM_POSE.value:
            return "Pose Animation"
        elif self.value == ExportAssetType.ANIM_NLA.value:
            return "Non Linear Animation"
        elif self.value == ExportAssetType.ANIM_ALEMBIC.value:
            return "Alembic Animation"
        else:
            return "Unknown"    
        
    def get_type_as_string(self):
        if self.value == ExportAssetType.UNKNOWN.value:
            return "Unknown"
        elif self.value == ExportAssetType.SKELETAL_MESH.value:
            return "SkeletalMesh"
        elif self.value == ExportAssetType.STATIC_MESH.value:
            return "StaticMesh"
        elif self.value == ExportAssetType.COLLECTION_AS_STATIC_MESH.value:
            return "CollectionStaticMesh"
        elif self.value == ExportAssetType.CAMERA.value:
            return "Camera"
        elif self.value == ExportAssetType.GROOM_SIMULATION.value:
            return "GroomSimulation"
        elif self.value == ExportAssetType.SPLINE.value:
            return "Spline"
        elif self.value == ExportAssetType.ANIM_ACTION.value:
            return "Action"
        elif self.value == ExportAssetType.ANIM_POSE.value:
            return "Pose"
        elif self.value == ExportAssetType.ANIM_NLA.value:
            return "NonLinearAnimation"
        elif self.value == ExportAssetType.ANIM_ALEMBIC.value:
            return "AlembicAnimation"
        else:
            return "Unknown"
    
    @staticmethod
    def get_asset_type_from_string(asset_type_str: str) -> 'ExportAssetType':
        for asset_type in ExportAssetType:
            if asset_type.value == asset_type_str:
                return asset_type
        return ExportAssetType.UNKNOWN
    
    def is_skeletal(self) -> bool:
        return self.value in [
            ExportAssetType.SKELETAL_MESH.value, 
            ExportAssetType.ANIM_ACTION.value, 
            ExportAssetType.ANIM_POSE.value, 
            ExportAssetType.ANIM_NLA.value
        ]
    
    def is_skeletal_animation(self) -> bool:
        return self.value in [
            ExportAssetType.ANIM_ACTION.value, 
            ExportAssetType.ANIM_POSE.value, 
            ExportAssetType.ANIM_NLA.value
        ]