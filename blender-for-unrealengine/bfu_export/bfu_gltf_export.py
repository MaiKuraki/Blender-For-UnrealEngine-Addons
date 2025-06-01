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


# This handle all FBX Export version of Blender.
# Better to look about an class that amange all export type in future?

import traceback
import bpy
from mathutils import Matrix
from .. import bpl


debug_show_arguments = False


def export_scene_gltf(
        filepath='', 
        check_existing=True, 
        filter_glob: str = "*.glb",
        use_selection=False, 
        use_visible=False, 
        use_armature_deform_only=False,
        use_active_collection=False, 
        use_mesh_edges=False, 
        bake_anim=True,
    ):
    print("s2")
    # Base parameters for all versions
    params = {
        'filepath': filepath,
        'check_existing': check_existing,
        'filter_glob': filter_glob,
        'use_selection': use_selection,
        'use_visible': use_visible,
        'use_active_collection': use_active_collection,
        'use_mesh_edges': use_mesh_edges,
        'export_def_bones': use_armature_deform_only,
        'export_bake_animation': bake_anim,
    }

    try:
        # Call the FBX export operator with the appropriate parameters
        print("s3")
        if (debug_show_arguments):
            print("(Blender) EXPORT PARMS:", params)
        bpy.ops.export_scene.gltf(**params)
        print("s4")
    except Exception as e:
        # Capture and print the detailed error information
        error_message = traceback.format_exc()
        print(bpl.color_set.red(error_message))
