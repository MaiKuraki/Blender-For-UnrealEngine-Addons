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
from typing import List, TYPE_CHECKING, Tuple, Optional
from .. import bbpl
from .. import bfu_utils
from ..bfu_assets_manager.bfu_asset_manager_type import AssetPackage
from .. import bfu_export
from ..bfu_export_logs.bfu_process_time_logs_types import SafeTimeGroup


def process_alembic_animation_export_from_package(
    op: bpy.types.Operator,
    package: AssetPackage
) -> bool:

    if package.file:
        return export_alembic_animation(
            op=op,
            fullpath=package.file.get_full_path(),
            objs=package.objects,
            frame_range=package.frame_range
        )
    else:
        return False


def export_alembic_animation(
    op: bpy.types.Operator,
    fullpath: Path,
    objs: List[bpy.types.Object],
    frame_range: Optional[Tuple[float, float]]
) -> bool:

    '''
    #####################################################
            #ALEMBIC ANIMATION
    #####################################################
    '''

    if bpy.context is None:
        return False

    # Export a single alembic animation
    my_timer_group = SafeTimeGroup(2)
    my_timer_group.start_timer(f"Prepare export")
    scene = bpy.context.scene

    # [SAVE ASSET DATA]
    # Save asset data before export like transforms, animation data, etc.
    # So can be restored after export.
    save_use_simplify: bool = bpy.context.scene.render.use_simplify
    saved_selection_names = bfu_export.bfu_export_utils.SavedObjectNames()
    saved_selection_names.save_new_names(objs)
    saved_base_transforms = bfu_export.bfu_export_utils.SaveTransformObjects(objs[0])
    saved_frame_range: Tuple[int, int] = (scene.frame_start, scene.frame_end)


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
            bfu_alembic_export_procedure: str
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

    bfu_utils.apply_export_transform(active, "Object")

    # [PREPARE SCENE]
    # Prepare scene for export (frame range, simplefying, etc.)
    if frame_range:
        scene.frame_start = int(frame_range[0])
        scene.frame_end = int(frame_range[1]) + 1
    scene.render.use_simplify = False

    my_timer_group.end_last_timer()

    # Process export
    my_timer_group.start_timer(f"Process export")
    alembic_animation_export_procedure = active.bfu_alembic_export_procedure
    if (alembic_animation_export_procedure == "blender-standard"):
        bpy.ops.wm.alembic_export(  # type: ignore
            filepath=str(fullpath),
            check_existing=False,
            selected=True,
            triangulate=True,
            global_scale=1,
            )
    else:
        print(f"Error: The export procedure '{alembic_animation_export_procedure}' was not found!")
    my_timer_group.end_last_timer()

    # [RESTORE ASSET DATA]
    # Restore asset data after export like transforms, animation data, etc.
    my_timer_group.start_timer(f"Clean after export")
    saved_base_transforms.reset_object_transforms()
    saved_selection_names.restore_names()
    scene.render.use_simplify = save_use_simplify
    scene.frame_start = saved_frame_range[0]
    scene.frame_end = saved_frame_range[1]


    for obj in scene.objects:
        bfu_utils.clear_all_bfu_temp_vars(obj)
    my_timer_group.end_last_timer()
    return True