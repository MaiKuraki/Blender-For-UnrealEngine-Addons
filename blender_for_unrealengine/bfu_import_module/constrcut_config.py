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

from typing import Tuple

# Minimum UE version for Interchange support (5.1.0)
interchange_minimal_support: Tuple[int, int, int] = (5, 1, 0) 

# Interchange is expiremental since 5.1, but it is not fully supported until 5.5.
# Some modules like InterchangeMaterialSearchLocation was added later.
interchange_unreal_support: Tuple[int, int, int] = (5, 5, 0)

# NOTES
# - unreal.InterchangePipelineStackOverride was added in 5.2
# - unreal.InterchangeGenericMaterialPipeline.search_location was added in 5.4
# - When use unreal.load_asset() and asset.asset_import_data it will return a class of unreal.InterchangeAssetImportData in 5.5
#   And FbxSkeletalMeshImportData, FbxStaticMeshImportData in older versions.


# DEBUG
force_use_interchange = "Auto" # "Auto" by default. You can use "Auto", "Interchange" or "FBX" for debug.