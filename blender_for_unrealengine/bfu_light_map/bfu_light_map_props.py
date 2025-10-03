# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


from typing import List
import bpy
from .. import bfu_utils
from .. import bbpl
from . import bfu_light_map_utils


def get_preset_values() -> List[str]:
    preset_values = [
            'obj.bfu_static_mesh_light_map_mode',
            'obj.bfu_static_mesh_custom_light_map_res',
            'obj.bfu_static_mesh_light_map_surface_scale',
            'obj.bfu_static_mesh_light_map_round_power_of_two',
            'obj.bfu_use_static_mesh_light_map_world_scale',
            'obj.bfu_generate_light_map_uvs',
        ]
    return preset_values

class BFU_OT_ComputLightMap(bpy.types.Operator):
    bl_label = "Calculate surface area"
    bl_idname = "object.comput_lightmap"
    bl_description = "Click to calculate the surface of the object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        obj.computedStaticMeshLightMapRes = bfu_utils.GetExportRealSurfaceArea(obj)
        self.report(
            {'INFO'},
            "Light map area updated to " + str(round(obj.computedStaticMeshLightMapRes)) + ". " +
            "Compunted Light map: " + str(bfu_light_map_utils.GetCompuntedLightMap(obj)))
        return {'FINISHED'}

class BFU_OT_ComputAllLightMap(bpy.types.Operator):
    bl_label = "Calculate all surface area"
    bl_idname = "object.comput_all_lightmap"
    bl_description = (
        "Click to calculate the surface of the all object in the scene"
        )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context):
        scene = context.scene
        if scene:
            updated = bfu_light_map_utils.update_area_light_map_list(scene)
            self.report({'INFO'}, "The light maps of " + str(updated) + " object(s) have been updated.")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No objects found to update.")
            return {'CANCELLED'}


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_ComputLightMap,
    BFU_OT_ComputAllLightMap
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_object_light_map_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Light map")
    bpy.types.Scene.bfu_tools_light_map_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Light Map")


    # StaticMeshImportData
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxStaticMeshImportData/index.html


    bpy.types.Object.bfu_static_mesh_light_map_mode = bpy.props.EnumProperty(
        name="Light Map",
        description='Specify how the light map resolution will be generated',
        override={'LIBRARY_OVERRIDABLE'},
        items=[
            ("Default",
                "Default",
                "Has no effect on light maps",
                1),
            ("CustomMap",
                "Custom map",
                "Set the custom light map resolution",
                2),
            ("SurfaceArea",
                "Surface Area",
                "Set light map resolution depending on the surface Area",
                3)
            ]
        )

    bpy.types.Object.bfu_static_mesh_custom_light_map_res = bpy.props.IntProperty(
        name="Light Map Resolution",
        description="This is the resolution of the light map",
        override={'LIBRARY_OVERRIDABLE'},
        soft_max=2048,
        soft_min=16,
        max=4096,  # Max for unreal
        min=4,  # Min for unreal
        default=64
        )

    bpy.types.Object.computedStaticMeshLightMapRes = bpy.props.FloatProperty(
        name="Computed Light Map Resolution",
        description="This is the computed resolution of the light map",
        override={'LIBRARY_OVERRIDABLE'},
        default=64.0
        )

    bpy.types.Object.bfu_static_mesh_light_map_surface_scale = bpy.props.FloatProperty(
        name="Surface scale",
        description="This is for resacle the surface Area value",
        override={'LIBRARY_OVERRIDABLE'},
        min=0.00001,  # Min for unreal
        default=64
        )

    bpy.types.Object.bfu_static_mesh_light_map_round_power_of_two = bpy.props.BoolProperty(
        name="Round power of 2",
        description=(
            "round Light Map resolution to nearest power of 2"
            ),
        default=True
        )

    bpy.types.Object.bfu_use_static_mesh_light_map_world_scale = bpy.props.BoolProperty(
        name="Use world scale",
        description=(
            "If not that will use the object scale."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )

    bpy.types.Object.bfu_generate_light_map_uvs = bpy.props.BoolProperty(
        name="Generate LightmapUVs",
        description=(
            "If checked, UVs for Lightmap will automatically be generated."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=True,
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_generate_light_map_uvs
    del bpy.types.Object.bfu_use_static_mesh_light_map_world_scale
    del bpy.types.Object.bfu_static_mesh_light_map_round_power_of_two
    del bpy.types.Object.bfu_static_mesh_light_map_surface_scale
    del bpy.types.Object.computedStaticMeshLightMapRes
    del bpy.types.Object.bfu_static_mesh_custom_light_map_res
    del bpy.types.Object.bfu_static_mesh_light_map_mode

    del bpy.types.Scene.bfu_tools_light_map_properties_expanded
    del bpy.types.Scene.bfu_object_light_map_properties_expanded