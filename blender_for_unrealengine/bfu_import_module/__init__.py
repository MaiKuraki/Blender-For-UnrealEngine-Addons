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

import importlib
import traceback
from typing import Dict, Any, List, Tuple

# constrcut_config needs to be imported and reloaded first because it used to construct functions.
from . import constrcut_config
from . import constrcut_utils
if "constrcut_config" in locals():
    importlib.reload(constrcut_config)
if "constrcut_utils" in locals():
    importlib.reload(constrcut_utils)

from . import bpl
from . import config
from . import asset_types
from . import import_module_tasks_class
from . import import_module_utils
from . import import_module_unreal_utils
from . import import_module_post_treatment
from . import asset_import
from . import asset_import
from . import sequencer_import
from . import sequencer_utils
from . import bfu_import_animations
from . import bfu_import_lods
from . import bfu_import_materials
from . import bfu_import_vertex_color
from . import bfu_import_light_map
from . import bfu_import_nanite
from . import bfu_import_sequencer
from . import import_module_tasks_helper

if "bpl" in locals():
    importlib.reload(bpl)
if "config" in locals():
    importlib.reload(config)
if "asset_types" in locals():
    importlib.reload(asset_types)
if "import_module_tasks_class" in locals():
    importlib.reload(import_module_tasks_class)
if "import_module_utils" in locals():
    importlib.reload(import_module_utils)
if "import_module_unreal_utils" in locals():
    importlib.reload(import_module_unreal_utils)
if "import_module_post_treatment" in locals():
    importlib.reload(import_module_post_treatment)
if "asset_import" in locals():
    importlib.reload(asset_import)
if "sequencer_import" in locals():
    importlib.reload(sequencer_import)
if "sequencer_utils" in locals():
    importlib.reload(sequencer_utils)
if "bfu_import_animations" in locals():
    importlib.reload(bfu_import_animations)
if "bfu_import_lods" in locals():
    importlib.reload(bfu_import_lods)
if "bfu_import_materials" in locals():
    importlib.reload(bfu_import_materials)
if "bfu_import_vertex_color" in locals():
    importlib.reload(bfu_import_vertex_color)
if "bfu_import_light_map" in locals():
    importlib.reload(bfu_import_light_map)
if "bfu_import_nanite" in locals():
    importlib.reload(bfu_import_nanite)
if "bfu_import_sequencer" in locals():
    importlib.reload(bfu_import_sequencer)
if "import_module_tasks_helper" in locals():
    importlib.reload(import_module_tasks_helper)

def run_asset_import(assets_data: Dict[str, Any], show_finished_popup: bool = False):
    try:
        if asset_import.ready_for_asset_import():
            return asset_import.import_all_assets(assets_data, show_finished_popup)
        else:
            print("Error: Asset import is not ready.")
    except Exception as e:
        print(f"Error during asset import: {e}")
        traceback.print_exc()

def run_sequencer_import(sequence_data: Dict[str, Any], show_finished_popup: bool = False):
    try:
        if sequencer_import.ready_for_sequence_import():
            return sequencer_import.create_sequencer(sequence_data, show_finished_popup)
        else:
            print("Error: Sequencer import is not ready.")
    except Exception as e:
        print(f"Error during sequencer import: {e}")
        traceback.print_exc()
    
