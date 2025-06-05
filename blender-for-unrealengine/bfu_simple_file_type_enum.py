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

from enum import Enum

class BFU_FileTypeEnum(Enum):
    # List of file types supported by the addon at export.
    FBX = "FBX"
    GLTF = "GLTF"
    ALEMBIC = "Alembic"
    JSON = "JSON"
    UNKNOWN = "Unknown"

    def get_file_extension(self) -> str:
        if self == BFU_FileTypeEnum.FBX:
            return ".fbx"
        elif self == BFU_FileTypeEnum.GLTF:
            return ".glb"
        elif self == BFU_FileTypeEnum.ALEMBIC:
            return ".abc"
        elif self == BFU_FileTypeEnum.JSON:
            return ".json"
        return ".unknown"