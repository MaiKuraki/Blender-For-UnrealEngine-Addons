# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

# NOTES
# - unreal.InterchangePipelineStackOverride was added in 5.2
# - unreal.InterchangeGenericMaterialPipeline.search_location was added in 5.4
# - When use unreal.load_asset() and asset.asset_import_data it will return a class of unreal.InterchangeAssetImportData in 5.5
#   And FbxSkeletalMeshImportData, FbxStaticMeshImportData in older versions.


# DEBUG
force_use_interchange = "Auto" # "Auto" by default. You can use "Auto", "Interchange" or "FBX" for debug.