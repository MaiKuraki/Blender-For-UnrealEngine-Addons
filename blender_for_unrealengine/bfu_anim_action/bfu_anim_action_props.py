# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

from enum import Enum
from typing import List, Tuple, TYPE_CHECKING, Any, Set, Optional
import bpy
from .. import bbpl

class BFU_AnimActionExportEnum(str, Enum):
    EXPORT_AUTO = "export_auto"
    EXPORT_SPECIFIC_LIST = "export_specific_list"
    EXPORT_SPECIFIC_PREFIX = "export_specific_prefix"
    EXPORT_CURRENT = "export_current"
    DONT_EXPORT = "dont_export"

    @staticmethod
    def default() -> "BFU_AnimActionExportEnum":
        return BFU_AnimActionExportEnum.EXPORT_AUTO

def get_anim_action_export_enum_list() -> List[Tuple[str, str, str, str, int]]:
    return [
        (BFU_AnimActionExportEnum.EXPORT_AUTO.value,
            "Export auto",
            "Export all actions connected to the bones names.",
            "FILE_SCRIPT",
            1),
        (BFU_AnimActionExportEnum.EXPORT_SPECIFIC_LIST.value,
            "Export specific list",
            "Export only actions that are checked in the list.",
            "LINENUMBERS_ON",
            3),
        (BFU_AnimActionExportEnum.EXPORT_SPECIFIC_PREFIX.value,
            "Export specific prefix",
            "Export only actions with a specific prefix" +
            " or the beginning of the actions names.",
            "SYNTAX_ON",
            4),
        (BFU_AnimActionExportEnum.DONT_EXPORT.value,
            "Not exported",
            "No action will be exported.",
            "MATPLANE",
            5),
        (BFU_AnimActionExportEnum.EXPORT_CURRENT.value,
            "Export Current",
            "Export only the current actions.",
            "FILE_SCRIPT",
            6),
    ]

def get_default_anim_action_export_enum() -> str:
    return BFU_AnimActionExportEnum.default().value

class BFU_AnimNamingTypeEnum(str, Enum):
    ACTION_NAME = "action_name"
    INCLUDE_ARMATURE_NAME = "include_armature_name"
    INCLUDE_CUSTOM_NAME = "include_custom_name"

    @staticmethod
    def default() -> "BFU_AnimNamingTypeEnum":
        return BFU_AnimNamingTypeEnum.ACTION_NAME
    
def get_anim_naming_type_enum_list() -> List[Tuple[str, str, str]]:
    return [
        (BFU_AnimNamingTypeEnum.ACTION_NAME.value,
            "Action name",
            'Exemple: "Anim_MyAction"'),
        (BFU_AnimNamingTypeEnum.INCLUDE_ARMATURE_NAME.value,
            "Include Armature Name",
            'Include armature name in animation export file name.' +
            ' Exemple: "Anim_MyArmature_MyAction"'),
        (BFU_AnimNamingTypeEnum.INCLUDE_CUSTOM_NAME.value,
            "Include custom name",
            'Include custom name in animation export file name.' +
            ' Exemple: "Anim_MyCustomName_MyAction"'),
    ]

def get_default_anim_naming_type_enum() -> str:
    return BFU_AnimNamingTypeEnum.default().value

class BFU_AnimActionStartEndTimeEnum(str, Enum):
    WITH_KEYFRAMES = "with_keyframes"
    WITH_SCENEFRAMES = "with_sceneframes"
    WITH_CUSTOMFRAMES = "with_customframes"

    @staticmethod
    def default() -> "BFU_AnimActionStartEndTimeEnum":
        return BFU_AnimActionStartEndTimeEnum.WITH_KEYFRAMES
    
def get_anim_action_start_end_time_enum_list() -> List[Tuple[str, str, str]]:
    return [
        (BFU_AnimActionStartEndTimeEnum.WITH_KEYFRAMES.value,
            "Auto",
            "The time will be defined according" +
            " to the first and the last frame"),
        (BFU_AnimActionStartEndTimeEnum.WITH_SCENEFRAMES.value,
            "Scene time",
            "Time will be equal to the scene time"),
        (BFU_AnimActionStartEndTimeEnum.WITH_CUSTOMFRAMES.value,
            "Custom time",
            'The time of all the animations of this object' +
            ' is defined by you.' +
            ' Use "bfu_anim_action_custom_start_frame" and "bfu_anim_action_custom_end_frame"'),
    ]

def get_default_anim_action_start_end_time_enum() -> str:
    return BFU_AnimActionStartEndTimeEnum.default().value


def get_preset_values() -> List[str]:
    preset_values: List[str] = [
        'obj.bfu_anim_action_export_enum',
        'obj.bfu_prefix_name_to_export',
        'obj.bfu_anim_action_start_end_time_enum',
        'obj.bfu_anim_action_start_frame_offset',
        'obj.bfu_anim_action_end_frame_offset',
        'obj.bfu_anim_action_custom_start_frame',
        'obj.bfu_anim_action_custom_end_frame',
        'obj.bfu_anim_naming_type',
        'obj.bfu_anim_naming_custom',
    ]
    return preset_values



class BFU_OT_ObjExportAction(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Action data name", default="Unknown", override={'LIBRARY_OVERRIDABLE'}) # type: ignore
    use: bpy.props.BoolProperty(name="use this action", default=False, override={'LIBRARY_OVERRIDABLE'}) # type: ignore

    if TYPE_CHECKING:
        name: str
        use: bool

def object_action_asset_list(obj: bpy.types.Object) -> List[BFU_OT_ObjExportAction]:
    return obj.bfu_action_asset_list #  type: ignore

def object_prefix_name_to_export(obj: bpy.types.Object) -> str:
    return obj.bfu_prefix_name_to_export #  type: ignore

class BFU_UL_ActionExportTarget(bpy.types.UIList):
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
        action_is_valid = False
        if item.name in bpy.data.actions:  # type: ignore
            action_is_valid = True

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if action_is_valid:  # If action is valid
                layout.prop(
                    bpy.data.actions[item.name],  # type: ignore
                    "name",
                    text="",
                    emboss=False,
                    icon="ACTION"
                )
                layout.prop(item, "use", text="")
            else:
                dataText = ('Action data named "' + item.name + '" Not Found. Please click on update')  # type: ignore
                layout.label(text=dataText, icon="ERROR")
        # Not optimized for 'GRID' layout type.
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class BFU_OT_UpdateObjActionListButton(bpy.types.Operator):
    bl_label = "Update action list"
    bl_idname = "object.updateobjactionlist"
    bl_description = "Update action list"

    def execute(self, context: bpy.types.Context) -> Set[Any]:
        def update_export_action_list(obj: bpy.types.Object):
            # Update the provisional action list known by the object

            def set_use_from_last(anim_list: List[Tuple[str, bool]], action_name: str) -> bool:
                for item in anim_list:
                    if item[0] == action_name:
                        if item[1]:
                            return True
                return False

            action_list_save: List[Tuple[str, bool]] = [("", False)]
            for action_asset in object_action_asset_list(obj):
                name = action_asset.name
                use = action_asset.use
                action_list_save.append((name, use))

            obj.bfu_action_asset_list.clear()  # type: ignore
            for action in bpy.data.actions:
                obj.bfu_action_asset_list.add().name = action.name  # type: ignore
                use_from_last: bool = set_use_from_last(action_list_save, action.name)
                obj.bfu_action_asset_list[action.name].use = use_from_last  # type: ignore
        
        obj = context.object
        if obj:
            update_export_action_list(obj)
        return {'FINISHED'}

class BFU_OT_SelectAllObjActionListButton(bpy.types.Operator):
    bl_label = "Select All"
    bl_idname = "object.selectallobjactionlist"
    bl_description = "Select all action list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context) -> Set[Any]:
        obj = context.object
        if obj:
            action_list = object_action_asset_list(obj)
            for item in action_list:
                item.use = True
        return {'FINISHED'}

class BFU_OT_DeselectAllObjActionListButton(bpy.types.Operator):
    bl_label = "Deselect All"
    bl_idname = "object.deselectallobjactionlist"
    bl_description = "Deselect all action list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context) -> Set[Any]:
        obj = context.object
        if obj:
            for action_asset in object_action_asset_list(obj):
                action_asset.use = False
        return {'FINISHED'}


def get_object_active_action_asset_list(obj: bpy.types.Object) -> int:
    return obj.bfu_active_action_asset_list  # type: ignore

def get_object_anim_action_export_enum(obj: bpy.types.Object) -> BFU_AnimActionExportEnum:
    for enum in BFU_AnimActionExportEnum:
        if obj.bfu_anim_action_export_enum == enum.value:  # type: ignore
            return enum

    print(f"Warning: Object {obj.name} has unknown export procedure '{obj.bfu_anim_action_export_enum}'. Falling back to default export procedure...")  # type: ignore
    return BFU_AnimActionExportEnum.default()

def get_object_prefix_name_to_export(obj: bpy.types.Object) -> str:
    return obj.bfu_prefix_name_to_export  # type: ignore

def has_object_with_export_enum(objects: List[bpy.types.Object], export_enum: BFU_AnimActionExportEnum) -> bool:
    for obj in objects:
        if get_object_anim_action_export_enum(obj) == export_enum:
            return True
    return False

def get_object_anim_action_start_end_time_enum(obj: bpy.types.Object) -> BFU_AnimActionStartEndTimeEnum:
    for enum in BFU_AnimActionStartEndTimeEnum:
        if obj.bfu_anim_action_start_end_time_enum == enum.value:  # type: ignore
            return enum

    print(f"Warning: Object {obj.name} has unknown start/end time '{obj.bfu_anim_action_start_end_time_enum}'. Falling back to default start/end time...")  # type: ignore
    return BFU_AnimActionStartEndTimeEnum.default()

def get_object_anim_action_start_frame_offset(obj: bpy.types.Object) -> int:
    return obj.bfu_anim_action_start_frame_offset  # type: ignore

def get_object_anim_action_end_frame_offset(obj: bpy.types.Object) -> int:
    return obj.bfu_anim_action_end_frame_offset  # type: ignore

def get_object_anim_action_custom_start_frame(obj: bpy.types.Object) -> int:
    return obj.bfu_anim_action_custom_start_frame  # type: ignore

def get_object_anim_action_custom_end_frame(obj: bpy.types.Object) -> int:
    return obj.bfu_anim_action_custom_end_frame  # type: ignore

def get_object_anim_naming_type_enum(obj: bpy.types.Object) -> BFU_AnimNamingTypeEnum:
    for enum in BFU_AnimNamingTypeEnum:
        if obj.bfu_anim_naming_type == enum.value:  # type: ignore
            return enum

    print(f"Warning: Object {obj.name} has unknown naming type '{obj.bfu_anim_naming_type}'. Falling back to default naming type...")  # type: ignore
    return BFU_AnimNamingTypeEnum.default()

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_ObjExportAction,
    BFU_UL_ActionExportTarget,
    BFU_OT_UpdateObjActionListButton,
    BFU_OT_SelectAllObjActionListButton,
    BFU_OT_DeselectAllObjActionListButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_animation_action_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Actions Properties")   # type: ignore[attr-defined]

    bpy.types.Object.bfu_action_asset_list = bpy.props.CollectionProperty(   # type: ignore[attr-defined]
        type=BFU_OT_ObjExportAction,
        options={'LIBRARY_EDITABLE'},
        override={'LIBRARY_OVERRIDABLE', 'USE_INSERTION'},
        )

    bpy.types.Object.bfu_active_action_asset_list = bpy.props.IntProperty(   # type: ignore[attr-defined]
        name="Active Scene Action",
        description="Index of the currently active object action",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
        )
    
    bpy.types.Object.bfu_anim_action_export_enum = bpy.props.EnumProperty(   # type: ignore[attr-defined]
        name="Action to export",
        description="Export procedure for actions (Animations and poses)",
        override={'LIBRARY_OVERRIDABLE'},
        items=get_anim_action_export_enum_list(),
        default=get_default_anim_action_export_enum()
    )

    bpy.types.Object.bfu_prefix_name_to_export = bpy.props.StringProperty(   # type: ignore[attr-defined]
        # properties used with ""export_specific_prefix" on bfu_anim_action_export_enum
        name="Prefix name",
        description="Indicate the prefix of the actions that must be exported",
        override={'LIBRARY_OVERRIDABLE'},
        maxlen=32,
        default="Example_",
        )

    bpy.types.Object.bfu_anim_action_start_end_time_enum = bpy.props.EnumProperty(   # type: ignore[attr-defined]
        name="Action Start/End Time",
        description="Set when animation starts and end",
        override={'LIBRARY_OVERRIDABLE'},
        items=get_anim_action_start_end_time_enum_list(),
        default=get_default_anim_action_start_end_time_enum()
        )

    bpy.types.Object.bfu_anim_action_start_frame_offset = bpy.props.IntProperty(   # type: ignore[attr-defined]
        name="Offset at start frame",
        description="Offset for the start frame.",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
    )

    bpy.types.Object.bfu_anim_action_end_frame_offset = bpy.props.IntProperty(   # type: ignore[attr-defined]
        name="Offset at end frame",
        description=(
            "Offset for the end frame. +1" +
            " is recommended for the sequences | 0 is recommended" +
            " for UnrealEngine cycles | -1 is recommended for Sketchfab cycles"
            ),
        override={'LIBRARY_OVERRIDABLE'},
        default=0
    )


    bpy.types.Object.bfu_anim_action_custom_start_frame = bpy.props.IntProperty(   # type: ignore[attr-defined]
        name="Custom start time",
        description="Set when animation start",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
        )

    bpy.types.Object.bfu_anim_action_custom_end_frame = bpy.props.IntProperty(   # type: ignore[attr-defined]
        name="Custom end time",
        description="Set when animation end",
        override={'LIBRARY_OVERRIDABLE'},
        default=1
        )
    

    bpy.types.Object.bfu_anim_naming_type = bpy.props.EnumProperty(   # type: ignore[attr-defined]
        name="Naming type",
        override={'LIBRARY_OVERRIDABLE'},
        items=get_anim_naming_type_enum_list(),
        default=get_default_anim_naming_type_enum()
        )

    bpy.types.Object.bfu_anim_naming_custom = bpy.props.StringProperty(   # type: ignore[attr-defined]
        name="Export name",
        override={'LIBRARY_OVERRIDABLE'},
        default='MyCustomName'
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.bfu_anim_naming_custom   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_anim_naming_type   # type: ignore[attr-defined]

    del bpy.types.Object.bfu_anim_action_custom_end_frame   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_anim_action_custom_start_frame   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_anim_action_end_frame_offset   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_anim_action_start_frame_offset   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_anim_action_start_end_time_enum   # type: ignore[attr-defined]

    del bpy.types.Object.bfu_prefix_name_to_export   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_anim_action_export_enum   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_active_action_asset_list   # type: ignore[attr-defined]
    del bpy.types.Object.bfu_action_asset_list   # type: ignore[attr-defined]
    del bpy.types.Scene.bfu_animation_action_properties_expanded   # type: ignore[attr-defined]