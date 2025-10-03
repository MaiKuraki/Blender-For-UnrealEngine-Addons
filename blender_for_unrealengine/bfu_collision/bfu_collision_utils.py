# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Blender For UnrealEngine
#  https://github.com/xavier150/Blender-For-UnrealEngine-Addons
# ----------------------------------------------

import bpy
from typing import List
from .bfu_collision_types import CollisionShapeType
from .. import bfu_basics
from .. import bfu_unreal_utils
from .. import bfu_export_control
from .. import bfu_addon_prefs


name_for_collision_material = "UE_Collision"

def is_a_collision(obj: bpy.types.Object) -> bool:
    '''
    Return True is object is an Collision.
    https://docs.unrealengine.com/en-US/WorkingWithContent/Importing/FBX/StaticMeshes/#collision
    '''
    prefix_list: List[str] = CollisionShapeType.get_prefix_list()

    if isinstance(obj.data, bpy.types.Mesh):
        if obj.name.startswith(tuple(prefix_list)):
            return True
    return False

def get_all_scene_collision_objs() -> List[bpy.types.Object]:
    # Get any collision objects from bpy.context.scene.objects or List if valid.
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")
    
    objs = scene.objects
    prefix_list: List[str] = CollisionShapeType.get_prefix_list()

    collision_objs: List[bpy.types.Object] = []
    for obj in objs:
        if isinstance(obj.data, bpy.types.Mesh):
            if obj.name.startswith(tuple(prefix_list)):
                collision_objs.append(obj)

    return collision_objs

def fix_scene_collision_export_type() -> int:
    # Corrects bad properties
    objs = get_all_scene_collision_objs()
    return fix_collision_export_type(objs)

def fix_collision_export_type(obj_list: List[bpy.types.Object]) -> int:
    # Corrects bad properties
    fixed_collisions = 0
    for obj in obj_list:
        if bfu_export_control.bfu_export_control_utils.is_export_recursive(obj):
            bfu_export_control.bfu_export_control_utils.set_auto(obj)
            fixed_collisions += 1
    return fixed_collisions

def fix_scene_collision_names() -> int:
    # Updates hierarchy names
    objs: List[bpy.types.Object] = get_all_scene_collision_objs()
    return fix_collision_names(objs)

def fix_collision_names(obj_list: List[bpy.types.Object]) -> int:
    # Updates hierarchy names
    fixed_collision_names = 0
    
    for obj in obj_list:
        for member in CollisionShapeType:
            if obj.name.startswith(member.get_unreal_engine_prefix()):
                update_length = update_collision_names(member, [obj])
                fixed_collision_names += update_length
                
    return fixed_collision_names

def fix_scene_collision_materials() -> int:
    # Updates hierarchy names
    objs = get_all_scene_collision_objs()
    return fix_collision_materials(objs)

def fix_collision_materials(obj_list: List[bpy.types.Object]) -> int:
    fixed_collision_materials: int = 0

    # Force material update
    create_collision_material()

    for obj in obj_list:
        if check_need_apply_collision_material(obj):
            apply_collision_material_to_object(obj)
            fixed_collision_materials += 1
    return fixed_collision_materials



def update_collision_names(collision_shape: CollisionShapeType, obj_list: List[bpy.types.Object]) -> int:
    # Update collision names for Unreal Engine.

    update_length: int = 0
    for obj in obj_list:
        ownerObj = obj.parent

        if ownerObj is not None:
            if obj != ownerObj:

                if isinstance(obj.data, bpy.types.Mesh):
                    prefix_name: str = collision_shape.get_unreal_engine_prefix()

                    new_name = bfu_unreal_utils.generate_name_for_unreal_engine(prefix_name+ownerObj.name, obj.name)
                    if new_name != obj.name:
                        obj.name = new_name 
                        update_length += 1
    return update_length

def convert_to_unrealengine_collision(
    collision_owner: bpy.types.Object, 
    objs_to_convert: List[bpy.types.Object], 
    collision_shape: CollisionShapeType
) -> List[bpy.types.Object]:
    # Convert objects to Unreal Engine Collisions Shapes
    
    def deselect_all_except_active() -> None:
        for obj in bpy.context.selected_objects:
            if obj != bpy.context.active_object:
                obj.select_set(False)


    converted_objs: List[bpy.types.Object] = []

    for obj in objs_to_convert:
        deselect_all_except_active()
        obj.select_set(True)
        if obj != collision_owner:

            if isinstance(obj.data, bpy.types.Mesh):
                if collision_shape.value == CollisionShapeType.BOX.value:
                    bfu_basics.convert_to_box_shape(obj)
                else:
                    bfu_basics.convert_to_convex_hull_shape(obj)
                obj.modifiers.clear()
                apply_collision_material_to_object(obj)

                prefix_name: str = collision_shape.get_unreal_engine_prefix()

                if is_a_collision(obj):
                    # Update the name if needed
                    obj.name = bfu_unreal_utils.generate_name_for_unreal_engine(obj.name, obj.name)
                else:
                    # Set a new name using the owner name as reference
                    obj.name = bfu_unreal_utils.generate_name_for_unreal_engine(prefix_name+collision_owner.name, obj.name)
                obj.show_wire = True
                obj.show_transparent = True
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                converted_objs.append(obj)

    deselect_all_except_active()
    for obj in objs_to_convert:
        obj.select_set(True)  # Resets previous selected object
    return converted_objs


def convert_select_to_unrealengine_collision(collision_shape: CollisionShapeType) -> List[bpy.types.Object]:
    # Convert selected objects to Unreal Engine Collisions Shapes

    collision_owner = bpy.context.active_object
    objs_to_convert = bpy.context.selected_objects
    if collision_owner is None:
        print("No active object found!")
        return []
    if len(objs_to_convert) < 2:
        print("Please select two objects. (Active object is the owner of the collision)")
        return []

    return convert_to_unrealengine_collision(collision_owner, objs_to_convert, collision_shape)

def get_or_create_collision_material() -> bpy.types.Material:
    mat = bpy.data.materials.get(name_for_collision_material)
    if mat is None:
        mat = create_collision_material()
    return mat

def create_collision_material() -> bpy.types.Material:
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")

    mat = bpy.data.materials.get(name_for_collision_material)
    if mat is None:
        mat = bpy.data.materials.new(name=name_for_collision_material)
    update_collision_material(mat)
    return mat

def update_collision_material(mat: bpy.types.Material) -> None:
    addon_prefs = bfu_addon_prefs.get_addon_prefs()

    # Viewport display settings
    mat.diffuse_color = addon_prefs.collisionColor
    mat.metallic = 0.0
    mat.roughness = 0.5
    mat.specular_intensity = 0.5
    
    # sets up the nodes to create a transparent material
    # with GLSL mat in Cycle
    mat.use_nodes = True
    node_tree = mat.node_tree
    if node_tree:
        nodes = node_tree.nodes

        # Clear and create the output node
        nodes.clear()
        out = nodes.new('ShaderNodeOutputMaterial')
        out.location = (0, 0)

        # Add a mix shader node and connect it to the output
        mix = nodes.new('ShaderNodeMixShader')
        mix.location = (-200, 0)
        fac_input = mix.inputs[0]
        if isinstance(fac_input, bpy.types.NodeSocketFloatFactor):
            fac_input.default_value = addon_prefs.collisionColor[3]  # Alpha value
        node_tree.links.new(mix.outputs['Shader'], out.inputs[0])

        # Add transparent shader for Cycles use
        trans = nodes.new('ShaderNodeBsdfTransparent')
        trans.location = (-400, 100)
        node_tree.links.new(trans.outputs['BSDF'], mix.inputs[1])

        # Add diffuse and transparent shaders and connect them to the mix shader
        diff = nodes.new('ShaderNodeBsdfDiffuse')
        diff.location = (-400, -100)
        colour_input = diff.inputs[0]
        if isinstance(colour_input, bpy.types.NodeSocketColor):
            colour_input.default_value = addon_prefs.collisionColor
        node_tree.links.new(diff.outputs['BSDF'], mix.inputs[2])

def get_current_visibility_state() -> bool:
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")

    # Get the current visibility state of all collision objects in the scene
    prefix_list: List[str] = CollisionShapeType.get_prefix_list()
    visibility_states: List[bool] = [obj.hide_viewport for obj in scene.objects if obj.name.startswith(tuple(prefix_list))]
    if not visibility_states:
        return False  # No collision objects found, default to False

    if all(visibility_states):
        return True  # All collision objects are hidden

    if not any(visibility_states):
        return False  # All collision objects are visible

    # Mixed visibility states, return False as a default
    return False

def apply_collision_material_to_objects(obj_list: List[bpy.types.Object]) -> None:
    # Apply the collision material to a List of objects
    mat = get_or_create_collision_material()
    for obj in obj_list:
        if isinstance(obj.data, bpy.types.Mesh):
            obj.data.materials.clear()
            obj.active_material_index = 0
            obj.data.materials.append(mat)

def apply_collision_material_to_object(obj: bpy.types.Object) -> None:
    if isinstance(obj.data, bpy.types.Mesh):
        obj.data.materials.clear()
        obj.active_material_index = 0
        obj.data.materials.append(get_or_create_collision_material())

def check_need_apply_collision_material(obj: bpy.types.Object) -> bool:
    # Check if the object needs to have the collision material applied
    if isinstance(obj.data, bpy.types.Mesh):
        if len(obj.data.materials) != 1:
            return True
        if obj.data.materials[0] is None:
            return True
        current_mat = obj.data.materials[0]
        if current_mat is None:
            return True
        if current_mat.name != name_for_collision_material:
            return True
    return False

def toggle_collision_visibility():
    scene = bpy.context.scene
    if scene is None:
        raise ValueError("No active scene found!")

    new_visibility: bool = not get_current_visibility_state()

    prefix_list: List[str] = CollisionShapeType.get_prefix_list()
    for obj in scene.objects:
        if isinstance(obj.data, bpy.types.Mesh):
            if obj.name.startswith(tuple(prefix_list)):
                obj.hide_viewport = new_visibility