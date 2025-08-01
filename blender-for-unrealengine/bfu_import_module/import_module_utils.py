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

import sys
import json
from pathlib import Path
from typing import Dict, Any
from . import config


def json_load(json_file: object) -> Dict[str, Any]:
    # Changed in Python 3.9: The keyword argument encoding has been removed.
    if sys.version_info >= (3, 9):
        return json.load(json_file)  # type: ignore
    else:
        return json.load(json_file, encoding="utf8")


def json_load_file(json_file_path: Path) -> Dict[str, Any]:
    if sys.version_info[0] < 3:
        with open(json_file_path, "r") as json_file:
            return json_load(json_file)
    else:
        with open(json_file_path, "r", encoding="utf8") as json_file:
            return json_load(json_file)

def print_debug_step(*args: object):
    if config.print_debug_steps:
        print(*args)