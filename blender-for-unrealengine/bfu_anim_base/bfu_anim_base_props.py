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
        'obj.bfu_disable_free_scale_animation',
        'obj.bfu_export_animation_without_mesh',
        'obj.bfu_export_animation_without_materials',
        'obj.bfu_export_animation_without_textures',
        'obj.bfu_sample_anim_for_export',
        'obj.bfu_simplify_anim_for_export',
    ]
    return preset_values



# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_animation_advanced_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Animation Advanced Properties")

    bpy.types.Object.bfu_sample_anim_for_export = bpy.props.FloatProperty(
        name="Sampling Rate",
        description="How often to evaluate animated values (in frames)",
        override={'LIBRARY_OVERRIDABLE'},
        min=0.01, max=100.0,
        soft_min=0.01, soft_max=100.0,
        default=1.0,
        )

    bpy.types.Object.bfu_simplify_anim_for_export = bpy.props.FloatProperty(
        name="Simplify animations",
        description=(
            "How much to simplify baked values" +
            " (0.0 to disable, the higher the more simplified)"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        # No simplification to up to 10% of current magnitude tolerance.
        min=0.0, max=100.0,
        soft_min=0.0, soft_max=10.0,
        default=0.0,
        )
    
    bpy.types.Object.bfu_disable_free_scale_animation = bpy.props.BoolProperty(
        name="Disable non-uniform scale animation.",
        description=(
            "If checked, scale animation track's elements always have same value. " + 
            "This applies basic bones only."
        ),
        override={'LIBRARY_OVERRIDABLE'},
        default=False
    )

    bpy.types.Object.bfu_export_animation_without_mesh = bpy.props.BoolProperty(
        name="Export animation without mesh",
        description="If checked, When exporting animation, do not include mesh data in the animation exported files. \n"
        "(False by default because don't work with shape keys animation.)",
        override={'LIBRARY_OVERRIDABLE'},
        default=False
        )
    
    bpy.types.Object.bfu_export_animation_without_materials = bpy.props.BoolProperty(
        name="Export animation without materials",
        description="If checked, When exporting animation, do not include materials in the animation exported files.",
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )
    
    bpy.types.Object.bfu_export_animation_without_textures = bpy.props.BoolProperty(
        name="Export animation without textures",
        description="If checked, When exporting animation, do not include textures in the animation exported files.",
        override={'LIBRARY_OVERRIDABLE'},
        default=True
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_export_animation_without_textures
    del bpy.types.Object.bfu_export_animation_without_materials
    del bpy.types.Object.bfu_export_animation_without_mesh
    del bpy.types.Object.bfu_disable_free_scale_animation
    del bpy.types.Object.bfu_simplify_anim_for_export
    del bpy.types.Object.bfu_sample_anim_for_export
    del bpy.types.Scene.bfu_animation_advanced_properties_expanded