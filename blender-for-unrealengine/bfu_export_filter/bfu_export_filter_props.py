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


from typing import List
import bpy
from .. import bbpl


def get_preset_values() -> List[str]:
    preset_values = [
        # Filter Categories
        'scene.bfu_use_static_export',
        'scene.bfu_use_static_collection_export',
        'scene.bfu_use_skeletal_export',
        'scene.bfu_use_animation_export',
        'scene.bfu_use_alembic_export',
        'scene.bfu_use_groom_simulation_export',
        'scene.bfu_use_camera_export',
        'scene.bfu_use_spline_export',

        # Additional Files
        'scene.bfu_use_text_export_log',
        'scene.bfu_use_text_import_asset_script',
        'scene.bfu_use_text_import_sequence_script',
        'scene.bfu_use_text_additional_data',

        # Export Filter
        'scene.bfu_export_selection_filter',
        ]
    return preset_values


def scene_use_static_export(scene: bpy.types.Scene) -> bool: 
    return scene.bfu_use_static_export # type: ignore

def scene_use_static_collection_export(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_static_collection_export # type: ignore

def scene_use_skeletal_export(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_skeletal_export # type: ignore

def scene_use_animation_export(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_animation_export # type: ignore

def scene_use_alembic_export(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_alembic_export # type: ignore

def scene_use_groom_simulation_export(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_groom_simulation_export # type: ignore

def scene_use_camera_export(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_camera_export # type: ignore

def scene_use_spline_export(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_spline_export # type: ignore

def scene_use_text_export_log(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_text_export_log # type: ignore

def scene_use_text_import_asset_script(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_text_import_asset_script # type: ignore

def scene_use_text_import_sequence_script(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_text_import_sequence_script # type: ignore

def scene_use_text_additional_data(scene: bpy.types.Scene) -> bool:
    return scene.bfu_use_text_additional_data # type: ignore

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_export_filter_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Export filters") #  type: ignore

    # Filter Categories
    bpy.types.Scene.bfu_use_static_export = bpy.props.BoolProperty( # type: ignore
        name="StaticMesh(s)",
        description="Check mark to export StaticMesh(s)",
        default=True
        )

    bpy.types.Scene.bfu_use_static_collection_export = bpy.props.BoolProperty( # type: ignore
        name="Collection(s) ",
        description="Check mark to export Collection(s)",
        default=True
        )

    bpy.types.Scene.bfu_use_skeletal_export = bpy.props.BoolProperty( # type: ignore
        name="SkeletalMesh(s)",
        description="Check mark to export SkeletalMesh(s)",
        default=True
        )

    bpy.types.Scene.bfu_use_animation_export = bpy.props.BoolProperty( # type: ignore
        name="Animation(s)",
        description="Check mark to export Animation(s)",
        default=True
        )

    bpy.types.Scene.bfu_use_alembic_export = bpy.props.BoolProperty( # type: ignore
        name="Alembic Animation(s)",
        description="Check mark to export Alembic animation(s)",
        default=True
        )

    bpy.types.Scene.bfu_use_groom_simulation_export = bpy.props.BoolProperty( # type: ignore
        name="Groom Simulation(s)",
        description="Check mark to export Groom Simulation(s)",
        default=True
        )

    bpy.types.Scene.bfu_use_camera_export = bpy.props.BoolProperty( # type: ignore
        name="Camera(s)",
        description="Check mark to export Camera(s)",
        default=True
        )

    bpy.types.Scene.bfu_use_spline_export = bpy.props.BoolProperty( # type: ignore
        name="Spline(s)",
        description="Check mark to export Spline(s)",
        default=True
        )
    
    # Additional Files
    bpy.types.Scene.bfu_use_text_export_log = bpy.props.BoolProperty( # type: ignore
        name="Export Log",
        description="Check mark to write export log file",
        default=True
        )

    bpy.types.Scene.bfu_use_text_import_asset_script = bpy.props.BoolProperty( # type: ignore
        name="Import assets script",
        description="Check mark to write import asset script file",
        default=True
        )

    bpy.types.Scene.bfu_use_text_import_sequence_script = bpy.props.BoolProperty( # type: ignore
        name="Import sequence script",
        description="Check mark to write import sequencer script file",
        default=True
        )

    bpy.types.Scene.bfu_use_text_additional_data = bpy.props.BoolProperty( # type: ignore
        name="Additional data",
        description=(
            "Check mark to write additional data" +
            " like parameter or anim tracks"),
        default=True
        )
    
    # Export Filter
    bpy.types.Scene.bfu_export_selection_filter = bpy.props.EnumProperty( # type: ignore
        name="Selection filter",
        items=[
            ('default', "No Filter", "Export as normal all objects with the recursive export option.", 0),
            ('only_object', "Only selected", "Export only the selected and visible object(s)", 1),
            ('only_object_and_active', "Only selected, active action / part",
                "Export only the selected and visible object(s) and active action on this object or part for modular skeletal mesh", 2),
            ],
        description=(
            "Choose what need be export from asset list."),
        default="default"
        )

def unregister():
    del bpy.types.Scene.bfu_export_selection_filter # type: ignore

    del bpy.types.Scene.bfu_use_text_additional_data # type: ignore
    del bpy.types.Scene.bfu_use_text_import_sequence_script # type: ignore
    del bpy.types.Scene.bfu_use_text_import_asset_script # type: ignore
    del bpy.types.Scene.bfu_use_text_export_log # type: ignore

    del bpy.types.Scene.bfu_use_spline_export # type: ignore
    del bpy.types.Scene.bfu_use_camera_export # type: ignore
    del bpy.types.Scene.bfu_use_groom_simulation_export # type: ignore
    del bpy.types.Scene.bfu_use_alembic_export # type: ignore
    del bpy.types.Scene.bfu_use_animation_export # type: ignore
    del bpy.types.Scene.bfu_use_skeletal_export # type: ignore
    del bpy.types.Scene.bfu_use_static_collection_export # type: ignore
    del bpy.types.Scene.bfu_use_static_export # type: ignore

    del bpy.types.Scene.bfu_export_filter_properties_expanded # type: ignore

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)