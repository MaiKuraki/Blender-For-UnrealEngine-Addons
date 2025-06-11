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
from pathlib import Path
from typing import List, TYPE_CHECKING
from .. import bbpl
from .. import bfu_utils
from ..bfu_assets_manager.bfu_asset_manager_type import AssetPackage
from .. import bfu_export
from ..bfu_export.bfu_export_utils import SavedSceneSimplfy
from ..bfu_export_logs.bfu_process_time_logs_types import SafeTimeGroup
from . import bfu_export_procedure
from .bfu_export_procedure import BFU_GroomExportProcedure

def process_groom_simulation_export_from_package(
    op: bpy.types.Operator,
    package: AssetPackage,
) -> bool:

    if package.file:
        return export_single_groom_simulation(
            op=op,
            fullpath=package.file.get_full_path(),
            objs=package.objects
        )
    else:
        return False


def export_single_groom_simulation(
    op: bpy.types.Operator,
    fullpath: Path,
    objs: List[bpy.types.Object]
) -> bool:

    '''
    #####################################################
            #GROOM SIMULATION
    #####################################################
    '''

    if bpy.context is None:
        return False

    # Export a single groom simulation
    my_timer_group = SafeTimeGroup(2)
    my_timer_group.start_timer(f"Prepare export")
    scene = bpy.context.scene

    # [SAVE ASSET DATA]
    # Save asset data before export like transforms, animation data, etc.
    # So can be restored after export.
    saved_simplify: SavedSceneSimplfy = SavedSceneSimplfy()
    saved_selection_names = bfu_export.bfu_export_utils.SavedObjectNames()
    saved_selection_names.save_new_names(objs)
    saved_base_transforms = bfu_export.bfu_export_utils.SaveTransformObjects(objs[0])


    # [SELECT ONLY] 
    # Select objects for export
    bbpl.utils.safe_mode_set('OBJECT')
    bbpl.utils.select_specific_object_list(objs[0], objs)

    # Selected active that should be used for export.
    if bpy.context.active_object is None:
        raise ValueError("No active object found after duplicate!")
    active: bpy.types.Object = bpy.context.active_object
    bfu_export.bfu_export_utils.set_object_export_name(obj=active, is_skeletal=False)

    if TYPE_CHECKING:
        class FakeObject(bpy.types.Object):
            bfu_groom_export_procedure: str
            bfu_convert_geometry_node_attribute_to_uv: bool
            bfu_convert_geometry_node_attribute_to_uv_name: str
            bfu_fbx_export_with_custom_props: bool
            bfu_export_deform_only: bool
            bfu_export_with_meta_data: bool
            bfu_mirror_symmetry_right_side_bones: bool
            bfu_use_ue_mannequin_bone_alignment: bool
            bfu_disable_free_scale_animation: bool
            bfu_fbx_export_with_custom_props: bool
        active = FakeObject()  # type: ignore

    frame = bpy.context.scene.frame_current = 1
    
    bfu_utils.apply_export_transform(active, "Object")

    # [PREPARE SCENE]
    # Prepare scene for export (frame range, simplefying, etc.)
    saved_simplify.symplify_scene()

    my_timer_group.end_last_timer()

    # Process export
    my_timer_group.start_timer(f"Process export")
    groom_simulation_export_procedure: BFU_GroomExportProcedure = bfu_export_procedure.get_object_export_procedure(active)
    if (groom_simulation_export_procedure.value == BFU_GroomExportProcedure.STANDARD_ALEMBIC.value):
        bpy.ops.wm.alembic_export(  # type: ignore
            filepath=str(fullpath),
            check_existing=False,
            selected=True,
            visible_objects_only=True,
            global_scale=1,
            start=frame,
            end=frame,
            uvs=False,
            normals=False,
            vcolors=True
            )
    else:
        print(f"Error: The export procedure '{groom_simulation_export_procedure.value}' was not found!")
    my_timer_group.end_last_timer()

    # [RESTORE ASSET DATA]
    # Restore asset data after export like transforms, animation data, etc.
    my_timer_group.start_timer(f"Clean after export")
    saved_base_transforms.reset_object_transforms()
    saved_selection_names.restore_names()
    saved_simplify.reset_scene()


    for obj in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(obj)
    my_timer_group.end_last_timer()
    return True