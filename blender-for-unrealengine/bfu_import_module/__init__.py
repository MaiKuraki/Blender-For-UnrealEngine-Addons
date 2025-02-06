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

from . import bpl
from . import config
from . import import_module_utils
from . import import_module_unreal_utils
from . import import_module_post_treatment
from . import asset_import
from . import asset_import
from . import sequencer_import
from . import sequencer_utils
from . import bfu_import_animations
from . import bfu_import_materials
from . import bfu_import_vertex_color
from . import bfu_import_light_map
from . import bfu_import_sequencer
from . import import_module_tasks_class
from . import import_module_tasks_helper

if "bpl" in locals():
    importlib.reload(bpl)
if "config" in locals():
    importlib.reload(config)
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
if "bfu_import_materials" in locals():
    importlib.reload(bfu_import_materials)
if "bfu_import_vertex_color" in locals():
    importlib.reload(bfu_import_vertex_color)
if "bfu_import_light_map" in locals():
    importlib.reload(bfu_import_light_map)
if "bfu_import_sequencer" in locals():
    importlib.reload(bfu_import_sequencer)
if "import_module_tasks_class" in locals():
    importlib.reload(import_module_tasks_class)
if "import_module_tasks_helper" in locals():
    importlib.reload(import_module_tasks_helper)

def run_asset_import(assets_data, show_finished_popup=False):
    if asset_import.ready_for_asset_import():
        return asset_import.ImportAllAssets(assets_data, show_finished_popup)

def run_sequencer_import(sequence_data, show_finished_popup=False):
    if sequencer_import.ready_for_sequence_import():
        return sequencer_import.CreateSequencer(sequence_data, show_finished_popup)
    
