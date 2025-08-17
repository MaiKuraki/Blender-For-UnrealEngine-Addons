# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


import bpy
from .. import bfu_addon_prefs
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl
from .. import bfu_assets_manager
from .. import bfu_static_mesh
from .. import bfu_export_control


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context, obj: bpy.types.Object):

    if obj is None:
        return
    
    scene = bpy.context.scene 
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Hide filters
    if obj is None:
        return
    if not bfu_utils.draw_proxy_propertys(obj):
        return
    if addon_prefs.useGeneratedScripts is False:
        return
    if bfu_export_control.bfu_export_control_utils.is_not_export_recursive(obj):
        return
    
    # Draw UI
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "MISC"):   
        accordion = bbpl.blender_layout.layout_accordion.get_accordion(scene, "bfu_lod_properties_expanded")
        _, panel = accordion.draw(layout)
        if accordion.is_expend():

            # Wiki page
            bbpl.blender_layout.layout_doc_button.add_doc_page_operator(panel, text="About Level of details (Lods)", url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Level-of-details")

            # Unreal python no longer support Skeletal mesh LODS import.
            asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_primary_supported_asset_class(obj)
            if asset_class and asset_class.use_lods == True:
                LodProp = panel.column()
                LodProp.prop(obj, 'bfu_export_as_lod_mesh')

            #Static only because Unreal python not support Skeletal mesh LODS import.
            if (bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj)):

                # Lod Groups
                bfu_static_mesh_lod_group = panel.row()
                bfu_static_mesh_lod_group.prop(obj, 'bfu_use_static_mesh_lod_group', text="")
                SMLODGroupChild = bfu_static_mesh_lod_group.column()
                SMLODGroupChild.enabled = obj.bfu_use_static_mesh_lod_group
                SMLODGroupChild.prop(obj, 'bfu_static_mesh_lod_group')
                bfu_static_mesh_lod_group.enabled = obj.bfu_export_as_lod_mesh is False

                # Lod Slots 
                LodList = panel.column()
                LodList.prop(obj, 'bfu_lod_target1')
                LodList.prop(obj, 'bfu_lod_target2')
                LodList.prop(obj, 'bfu_lod_target3')
                LodList.prop(obj, 'bfu_lod_target4')
                LodList.prop(obj, 'bfu_lod_target5')
                LodList.enabled = obj.bfu_export_as_lod_mesh is False and obj.bfu_use_static_mesh_lod_group is False

