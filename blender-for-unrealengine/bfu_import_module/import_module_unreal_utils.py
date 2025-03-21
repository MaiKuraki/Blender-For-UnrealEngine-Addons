# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

import string
from typing import List, Tuple
from . import import_module_unreal_utils

try:
    import unreal
except ImportError:
    import unreal_engine as unreal

import unreal
import re

def get_package_path_from_any_string(asset_string: str) -> str:
    """
    Convert any asset reference string (including full object references with /Script/...)
    into a clean package path suitable for EditorAssetLibrary functions.
    """
    
    # Match format like /Script/Engine.SkeletalMesh'/Game/Path/Asset.Asset'
    match = re.match(r"^/Script/.+?'(/Game/.+?)'\s*$", asset_string)
    if match:
        asset_path = match.group(1)
    else:
        asset_path = asset_string

    # Handle /Game/Path/Asset.Asset -> /Game/Path/Asset
    if asset_path.count(".") == 1:
        asset_path = asset_path.split(".")[0]

    return asset_path


def load_asset(name):
    # Convert ObjectPath to PackageName
    package_name = get_package_path_from_any_string(name)
    asset_exist = unreal.EditorAssetLibrary.does_asset_exist(package_name)
    if asset_exist:
        find_asset = unreal.find_asset(name, follow_redirectors=True)
        if find_asset is None:
            # Load asset if not find.
            # Sometimes assets exist but not found because unloaded.
            find_asset = unreal.load_asset(name, follow_redirectors=True)
        return find_asset
    return None
     

def get_selected_level_actors() -> List[unreal.Actor]:
    """Returns a list of selected actors in the level."""
    return unreal.EditorLevelLibrary.get_selected_level_actors()

def get_unreal_version() -> Tuple[int, int, int]:
    """Returns the Unreal Engine version as a tuple of (major, minor, patch)."""
    version_info = unreal.SystemLibrary.get_engine_version().split('-')[0]
    major, minor, patch = map(int, version_info.split('.'))
    return major, minor, patch

def is_unreal_version_greater_or_equal(target_major: int, target_minor: int = 0, target_patch: int = 0) -> bool:
    """Checks if the Unreal Engine version is greater than or equal to the target version."""
    major, minor, patch = get_unreal_version()
    return (
        major > target_major or 
        (major == target_major and minor > target_minor) or 
        (major == target_major and minor == target_minor and patch >= target_patch)
    )


def clean_filename_for_unreal(filename):
    """
    Returns a valid Unreal asset name by replacing invalid characters.
    Normalizes string, removes non-alpha characters
    """

    filename = filename.replace('.', '_')
    filename = filename.replace('(', '_')
    filename = filename.replace(')', '_')
    filename = filename.replace(' ', '_')
    valid_chars = "-_%s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename

def show_simple_message(title: str, message: str) -> unreal.AppReturnType:
    """Displays a simple message dialog in Unreal Editor."""
    if hasattr(unreal, 'EditorDialog'):
        return unreal.EditorDialog.show_message(title, message, unreal.AppMsgType.OK)
    else:
        print('--------------------------------------------------')
        print(message)

def show_warning_message(title: str, message: str) -> unreal.AppReturnType:
    """Displays a warning message in Unreal Editor and prints it to the console."""
    if hasattr(unreal, 'EditorDialog'):
        unreal.EditorDialog.show_message(title, message, unreal.AppMsgType.OK)
    else:
        print('--------------------------------------------------')
        print(message)

def get_support_interchange() -> bool:
    return import_module_unreal_utils.is_unreal_version_greater_or_equal(5, 1)

def editor_scripting_utilities_active() -> bool:
    if is_unreal_version_greater_or_equal(4,20):
        if hasattr(unreal, 'EditorAssetLibrary'):
            return True
    return False

def alembic_importer_active() -> bool:
    return hasattr(unreal, 'AbcImportSettings')

def sequencer_scripting_active() -> bool:
    return hasattr(unreal.MovieSceneSequence, 'set_display_rate')
