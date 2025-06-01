import bpy

def get_static_export_procedure_enum_property_list():
    items=[
        ("custom_fbx_export",
            "UE Standard (FBX)",
            "Modified fbx I/O for Unreal Engine",
            "OUTLINER_OB_GROUP_INSTANCE",
            1),
        ("standard_fbx",
            "Blender Standard (FBX)",
            "Standard fbx I/O.",
            "OUTLINER_OB_GROUP_INSTANCE",
            2),
        ("standard_gltf",
            "Blender Standard (glTF 2.0)",
            "Standard glTF 2.0.",
            "OUTLINER_OB_GROUP_INSTANCE",
            3),
        ]
    return items

def get_default_static_export_procedure():
    return "standard_fbx"

def get_obj_export_type(obj: bpy.types.Object):
    return get_export_type(obj.bfu_static_export_procedure)

def get_export_type(procedure: str): # Object.bfu_static_export_procedure
    if procedure == "custom_fbx_export":
        return "FBX"

    elif procedure == "standard_fbx":
        return "FBX"
    
    elif procedure == "standard_gltf":
        return "GLTF"
    return None

def get_obj_static_fbx_procedure_preset(obj: bpy.types.Object):
    return get_static_fbx_procedure_preset(obj.bfu_static_export_procedure)

def get_static_fbx_procedure_preset(procedure: str): # Object.bfu_static_export_procedure
    preset = {}
    if procedure == "custom_fbx_export":
        preset["use_space_transform"]=True
        preset["axis_forward"]='-Z'
        preset["axis_up"]='Y'
        return preset

    else:
        preset["use_space_transform"]=True
        preset["axis_forward"]='-Z'
        preset["axis_up"]='Y'

    return preset

def get_obj_can_edit_scale(obj: bpy.types.Object)-> bool:
    return get_can_edit_scale(obj.bfu_static_export_procedure)

def get_can_edit_scale(procedure: str)-> bool: # Object.bfu_static_export_procedure
    if procedure == "standard_gltf":
        # bpy.ops.export_scene.gltf() don't have global_scale
        return False

    return True

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.bfu_static_export_procedure = bpy.props.EnumProperty(
        name="Export Procedure",
        description=(
            "This will define how a skeletal mesh should be exported."
            ),
        override={'LIBRARY_OVERRIDABLE'},
        items=get_static_export_procedure_enum_property_list(),
        default=get_default_static_export_procedure()
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)