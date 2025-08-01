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
import os
import importlib
import inspect
from typing import List, Any, Dict
from ..bfu_check_types import bfu_checker
from .. import bfu_check_utils
from ... import bpl
from ... import bfu_cached_assets
from ...bfu_cached_assets.bfu_cached_assets_blender_class import AssetToSearch, AssetDataSearchMode

# Dynamic import and reload for layers.
def get_modules_from_directory(directory: str):
    module_names: List[str] = []
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]  # Remove '.py'
                module_names.append(module_name)
    return module_names

# Path to the 'types' directory (adjust based on project structure)
types_dir = os.path.join(os.path.dirname(__file__), "types")

# Import and reload modules dynamically
module_names = get_modules_from_directory(types_dir)

modules: Dict[str, Any] = {}
all_classes: List[Any] = []
for module_name in module_names:
    module = importlib.import_module(f".types.{module_name}", package=__package__)
    importlib.reload(module)
    modules[module_name] = module

    # Get all classes in the current module and avoid duplicates
    all_classes.extend([
        obj for _, obj in inspect.getmembers(module) 
        if inspect.isclass(obj) and obj.__module__ == module.__name__ and obj not in all_classes
    ])

def run_all_check():
    # Clear existing potential errors before starting the checks
    bfu_check_utils.clear_potential_errors()

    # Collect all valid checker classes
    checker_classes = [
        cls for cls in all_classes
        if issubclass(cls, bfu_checker)
        and cls is not bfu_checker
        and (hasattr(cls, "run_asset_check") or hasattr(cls, "run_scene_check"))
    ]

    total = len(checker_classes)

    bpl.advprint.print_simple_title("Run check potential issues.")
    final_asset_cache = bfu_cached_assets.bfu_cached_assets_blender_class.get_final_asset_cache()
    final_asset_list_to_export = final_asset_cache.get_final_asset_list(AssetToSearch.ALL_ASSETS, AssetDataSearchMode.FULL)
    print(checker_classes)

    for index, my_check_cls in enumerate(checker_classes, start=1):
        counter = bpl.utils.CounterTimer()
        instance = my_check_cls()
        check_name = instance.check_name
        print(f"Check {index}/{total}: {check_name}...")

        # Count errors before and after to determine how many were added by this check
        before = len(bpy.context.scene.bfu_export_potential_errors)  # type: ignore

        # First run the scene check
        instance.run_scene_check(scene=bpy.context.scene)  # type: ignore

        # Then run the asset check for each asset in the final asset list
        for asset in final_asset_list_to_export:
            instance.run_asset_check(asset)


        after = len(bpy.context.scene.bfu_export_potential_errors)  # type: ignore
        new_issues = after - before

        # Display result with appropriate color
        if new_issues > 0:
            issue_result = bpl.color_set.red(f"{new_issues} issue(s)")
        else:
            issue_result = bpl.color_set.green("no issues")

        print(f"{check_name} finished in: {counter.get_str_time()} with {issue_result}\n")
