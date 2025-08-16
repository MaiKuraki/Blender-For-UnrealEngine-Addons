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

from typing import List, Dict
from .bfu_asset_manager_type import BFU_BaseAssetClass

registred_asset_class: List[BFU_BaseAssetClass] = []
registred_asset_class_by_type: Dict[str, List[BFU_BaseAssetClass]] = {}

def register_asset_class(asset: BFU_BaseAssetClass, custom_type: str = ""):
    registred_asset_class.append(asset)
    if custom_type:
        if custom_type not in registred_asset_class_by_type:
            registred_asset_class_by_type[custom_type] = []
        registred_asset_class_by_type[custom_type].append(asset)

def get_registred_asset_class() -> List[BFU_BaseAssetClass]:
    return registred_asset_class

def get_registred_asset_class_by_type(asset_type: str) -> List[BFU_BaseAssetClass]:
    return registred_asset_class_by_type.get(asset_type, [])
