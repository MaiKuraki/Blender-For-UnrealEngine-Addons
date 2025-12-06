# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------


from typing import List, Tuple, TYPE_CHECKING, Optional, Any, Set
import bpy

def get_preset_values() -> List[str]:
    preset_values: List[str] = [
        ]
    return preset_values

class BFU_OT_SceneStaticCollectionExport(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="collection data name", default="Unknown", override={'LIBRARY_OVERRIDABLE'}) # type: ignore
    use: bpy.props.BoolProperty(name="export this collection", default=False, override={'LIBRARY_OVERRIDABLE'}) # type: ignore

    if TYPE_CHECKING:
        name: str
        use: bool

class BFU_UL_StaticCollectionExportTarget(bpy.types.UIList):

    def draw_item(
            self, 
            context: bpy.types.Context, 
            layout: bpy.types.UILayout, 
            data: Optional[Any], 
            item: Optional[Any], 
            icon: Optional[int], 
            active_data: Any, 
            active_property: Optional[str], 
            index: Optional[int],
            flt_flag: Optional[int]
        ):

        collection_is_valid = False
        if item.name in bpy.data.collections:  # type: ignore
            collection_is_valid = True

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if collection_is_valid:  # If action is valid
                layout.prop(
                    bpy.data.collections[item.name],  # type: ignore
                    "name",
                    text="",
                    emboss=False,
                    icon="OUTLINER_COLLECTION")
                layout.prop(item, "use", text="")
            else:
                dataText = ('Collection named "' + item.name + '" Not Found. Please clic on update')  # type: ignore
                layout.label(text=dataText, icon="ERROR")
        # Not optimised for 'GRID' layout type.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


def scene_static_collection_asset_list(scene: bpy.types.Scene) -> List[BFU_OT_SceneStaticCollectionExport]:
    return scene.bfu_static_collection_asset_list # type: ignore

class BFU_OT_UpdateStaticCollectionButton(bpy.types.Operator):
    bl_label = "Update collection list"
    bl_idname = "object.updatecollectionlist"
    bl_description = "Update collection list"

    def execute(self, context: bpy.types.Context) -> Set[Any]:
        def update_export_collection_list(scene: bpy.types.Scene):
            # Update the provisional collection list known by the object

            def set_use_from_last(col_list: List[Tuple[str, bool]], CollectionName: str) -> bool:
                for item in col_list:
                    if item[0] == CollectionName:
                        if item[1]:
                            return True
                return False

            col_list_save: List[Tuple[str, bool]] = [("", False)]
            for col in scene_static_collection_asset_list(scene):  # CollectionProperty
                name = col.name
                use = col.use
                col_list_save.append((name, use))
            scene.bfu_static_collection_asset_list.clear() # type: ignore
            for col in bpy.data.collections:
                scene.bfu_static_collection_asset_list.add().name = col.name # type: ignore
                use_from_last = set_use_from_last(col_list_save, col.name)
                scene.bfu_static_collection_asset_list[col.name].use = use_from_last # type: ignore
        scene = context.scene
        if scene:
            update_export_collection_list(scene)
        return {'FINISHED'}


def get_scene_static_collection_asset_list(scene: bpy.types.Scene) -> List[BFU_OT_SceneStaticCollectionExport]:
    return scene.bfu_static_collection_asset_list  # type: ignore

def get_scene_active_static_collection_asset_list(scene: bpy.types.Scene) -> int:
    return scene.bfu_active_static_collection_asset_list  # type: ignore

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_SceneStaticCollectionExport,
    BFU_UL_StaticCollectionExportTarget,
    BFU_OT_UpdateStaticCollectionButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_static_collection_asset_list = bpy.props.CollectionProperty( # type: ignore
        type=BFU_OT_SceneStaticCollectionExport,
        options={'LIBRARY_EDITABLE'},
        override={'LIBRARY_OVERRIDABLE', 'USE_INSERTION'},
        )
    
    bpy.types.Scene.bfu_active_static_collection_asset_list = bpy.props.IntProperty( # type: ignore
        name="Active Collection",
        description="Index of the currently active collection",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_active_static_collection_asset_list # type: ignore
    del bpy.types.Scene.bfu_static_collection_asset_list # type: ignore