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


import os.path
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import unreal
from . import bpl
from . import import_module_utils
from . import import_module_unreal_utils
from . import import_module_post_treatment
from . import import_module_tasks_class
from . import import_module_tasks_helper
from . import bfu_import_animations
from . import bfu_import_lods
from . import bfu_import_materials
from . import bfu_import_vertex_color
from . import bfu_import_light_map
from . import bfu_import_nanite
from . import config
from .asset_types import ExportAssetType





def ready_for_asset_import():
    if not import_module_unreal_utils.alembic_importer_active():
        message = 'WARNING: Alembic Importer Plugin should be activated.' + "\n"
        message += 'Edit > Plugin > Importer > Alembic Importer.'
        import_module_unreal_utils.show_warning_message("Alembic Importer not activated.", message)
        return False

    if not import_module_unreal_utils.editor_scripting_utilities_active():
        message = 'WARNING: Editor Scripting Utilities Plugin should be activated.' + "\n"
        message += 'Edit > Plugin > Scripting > Editor Scripting Utilities.'
        import_module_unreal_utils.show_warning_message("Editor Scripting Utilities not activated.", message)
        return False
    return True




def ImportTask(asset_data: Dict[str, Any]) -> (str, Optional[List[unreal.AssetData]]):
    asset_type = ExportAssetType.get_asset_type_from_string(asset_data["asset_type"])

    if asset_type in [ExportAssetType.STATIC_MESH, ExportAssetType.SKELETAL_MESH]:
        if "import_as_lod_mesh" in asset_data:
            if asset_data["import_as_lod_mesh"] == True:  # Lod should not be imported here so return if lod is not 0.
                return "FAIL", None

    def found_additional_data():
        files: List[Dict[str, Any]] = asset_data["files"]
        for file in files:
            if file["content_type"] == "ADDITIONAL_DATA":
                return import_module_utils.json_load_file(Path(file["file_path"]))
        return None

    asset_additional_data = found_additional_data()

    if asset_type.is_skeletal():
        origin_skeleton = None
        origin_skeletal_mesh = None


        if "target_skeleton_search_ref" in asset_data:
            find_sk_asset = import_module_unreal_utils.load_asset(asset_data["target_skeleton_search_ref"])
            if isinstance(find_sk_asset, unreal.Skeleton):
                origin_skeleton = find_sk_asset
            elif isinstance(find_sk_asset, unreal.SkeletalMesh):
                origin_skeleton = find_sk_asset.skeleton
                origin_skeletal_mesh = find_sk_asset

        if "target_skeletal_mesh_search_ref" in asset_data:
            find_skm_asset = import_module_unreal_utils.load_asset(asset_data["target_skeletal_mesh_search_ref"])
            if isinstance(find_skm_asset, unreal.SkeletalMesh):
                origin_skeleton = find_skm_asset.skeleton
                origin_skeletal_mesh = find_skm_asset
            elif isinstance(find_skm_asset, unreal.Skeleton):
                origin_skeletal_mesh = find_skm_asset
                
        if asset_type in [ExportAssetType.ANIM_ACTION, ExportAssetType.ANIM_POSE, ExportAssetType.ANIM_NLA]:
            skeleton_search_str = f'"target_skeleton_search_ref": {asset_data["target_skeleton_search_ref"]}'
            skeletal_mesh_search_str = f'"target_skeletal_mesh_search_ref": {asset_data["target_skeletal_mesh_search_ref"]}'
    
            if origin_skeleton:
                print(f'{skeleton_search_str} and "{skeletal_mesh_search_str} "was found for animation immport:" {str(origin_skeleton)}')
            else:
                message = "WARNING: Could not find skeleton for animation import." + "\n"
                message += f" -{skeleton_search_str}" + "\n"
                message += f" -{skeletal_mesh_search_str}" + "\n"
                import_module_unreal_utils.show_warning_message("Skeleton not found.", message)

    print("######################################### origin_skeleton ->", origin_skeleton)

    itask = import_module_tasks_class.ImportTask()

    def get_file_from_types(file_types: List[str]) -> Tuple[str, str]:
        for file in asset_data["files"]:
            if file["type"] in file_types:
                return file["file_path"], file["type"]
        return "", ""

    # Search for the file to import
    if asset_type == ExportAssetType.ANIM_ALEMBIC:
        filename, filetype = get_file_from_types(["ABC"])
        if not filename:
            return "FAIL", None
        itask.set_filename(filename)
        print("Target Alembic file:", filename)
    else:
        filename, filetype = get_file_from_types(["GLTF", "FBX"])
        if not filename:
            return "FAIL", None
        itask.set_filename(filename)
        print("Target file:", filename)

    itask.get_task().destination_path = "/" + os.path.normpath(asset_data["asset_import_path"])
    itask.get_task().automated = config.automated_import_tasks
    itask.get_task().save = False
    itask.get_task().replace_existing = True
    task_option = import_module_tasks_helper.init_options_data(asset_type, filetype)
    itask.set_task_option(task_option)



    # Alembic
    if asset_type == ExportAssetType.ANIM_ALEMBIC:
        import_module_utils.print_debug_step("Process Alembic")
        alembic_import_data = itask.get_abc_import_settings()
        alembic_import_data.static_mesh_settings.set_editor_property("merge_meshes", True)
        alembic_import_data.set_editor_property("import_type", unreal.AlembicImportType.SKELETAL)
        alembic_import_data.conversion_settings.set_editor_property("flip_u", False)
        alembic_import_data.conversion_settings.set_editor_property("flip_v", True)
        scale = asset_data["scene_unit_scale"] * asset_data["asset_global_scale"]
        ue_scale = unreal.Vector(scale * 100, scale * -100, scale * 100) # Unit scale * object scale * 100
        rotation = unreal.Vector(90, 0, 0)
        alembic_import_data.conversion_settings.set_editor_property("scale", ue_scale) 
        alembic_import_data.conversion_settings.set_editor_property("rotation", rotation)

    # #################################[Change]

    # unreal.FbxImportUI
    # https://docs.unrealengine.com/4.26/en-US/PythonAPI/class/FbxImportUI.html

    import_module_utils.print_debug_step("Process transform and curve")
    # Import transform and curve
    if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
        animation_pipeline = itask.get_igap_animation()
        if "do_not_import_curve_with_zero" in asset_data:
            animation_pipeline.set_editor_property('do_not_import_curve_with_zero', asset_data["do_not_import_curve_with_zero"]) 

    else:
        anim_sequence_import_data = itask.get_animation_import_data()
        anim_sequence_import_data.import_translation = unreal.Vector(0, 0, 0)
        if "do_not_import_curve_with_zero" in asset_data:
            anim_sequence_import_data.set_editor_property('do_not_import_curve_with_zero', asset_data["do_not_import_curve_with_zero"]) 

    if asset_type == ExportAssetType.ANIM_ALEMBIC:
        itask.get_abc_import_settings().set_editor_property('import_type', unreal.AlembicImportType.SKELETAL)
        
    else:
        if asset_type.is_skeletal_animation():
            if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
                if origin_skeleton:
                    itask.get_igap_skeletal_mesh().set_editor_property('skeleton', origin_skeleton)
                    itask.get_igap_skeletal_mesh().set_editor_property('import_only_animations', True)

            else:
                if origin_skeleton:
                    itask.get_fbx_import_ui().set_editor_property('skeleton', origin_skeleton)

        if asset_type == ExportAssetType.SKELETAL_MESH:
            if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
                if origin_skeleton:
                    itask.get_igap_skeletal_mesh().set_editor_property('skeleton', origin_skeleton)
                    
                    # From Unreal Engine 5.1 to 5.4, the interchange pipeline still creates a new skeleton asset. #Look like a bug.
                    # May do a replace reference after import?
                    print("Skeleton set, ", origin_skeleton.get_path_name())
                    unreal_version = import_module_unreal_utils.get_unreal_version()
                    if unreal_version >= (5, 1, 0) and unreal_version <= (5, 4, 0):
                        print("Skeleton is set, but a new skeleton asset will be created. This is a bug with the Interchange Generic Assets Pipeline in Unreal Engine 5.1 to 5.4.")
                        
                else:
                    # Unreal Engine may randomly select a skeleton asset because it thinks it could be used for the skeletal mesh.
                    # This is a big issue and the Python API does not allow to avoid that...
                    # Even when I set the skeleton to None, Unreal Engine may still select a skeleton without letting the import create a new one.
                    itask.get_igap_skeletal_mesh().set_editor_property('skeleton', None)
                    print("Skeleton is not set, a new skeleton asset will be created...")
                    
            elif isinstance(itask.task_option, unreal.FbxImportUI):
                if origin_skeleton:
                    itask.get_fbx_import_ui().set_editor_property('skeleton', origin_skeleton)
                    print("Skeleton set, ", origin_skeleton.get_path_name())
                else:
                    itask.get_fbx_import_ui().set_editor_property('skeleton', None)
                    print("Skeleton is not set, a new skeleton asset will be created...")                  
   
        import_module_utils.print_debug_step("Set Asset Type")
        # Set Asset Type
        if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
            if asset_type == ExportAssetType.STATIC_MESH:
                itask.get_igap_common_mesh().set_editor_property('force_all_mesh_as_type', unreal.InterchangeForceMeshType.IFMT_STATIC_MESH)
            if asset_type == ExportAssetType.SKELETAL_MESH:
                itask.get_igap_common_mesh().set_editor_property('force_all_mesh_as_type', unreal.InterchangeForceMeshType.IFMT_SKELETAL_MESH)
            if asset_type.is_skeletal_animation():
                itask.get_igap_common_mesh().set_editor_property('force_all_mesh_as_type', unreal.InterchangeForceMeshType.IFMT_NONE)
            else:
                itask.get_igap_common_mesh().set_editor_property('force_all_mesh_as_type', unreal.InterchangeForceMeshType.IFMT_NONE)

        else:
            if asset_type == ExportAssetType.STATIC_MESH:
                itask.get_fbx_import_ui().set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_STATIC_MESH)
            elif asset_type.is_skeletal_animation():
                itask.get_fbx_import_ui().set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_ANIMATION)
            else:
                itask.get_fbx_import_ui().set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        
        import_module_utils.print_debug_step("Set Material Use")
        # Set Material Use
        if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
            if asset_type.is_skeletal_animation():
                itask.get_igap_material().set_editor_property('import_materials', False)
            else:
                itask.get_igap_material().set_editor_property('import_materials', True)
        else:
            if asset_type.is_skeletal_animation():
                itask.get_fbx_import_ui().set_editor_property('import_materials', False)
            else:
                itask.get_fbx_import_ui().set_editor_property('import_materials', True)
        
        import_module_utils.print_debug_step("Set Texture Type")
        # Set Texture Use
        if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
            itask.get_igap_texture().set_editor_property('import_textures', False)
        else:
            itask.get_fbx_import_ui().set_editor_property('import_textures', False)

        if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
            if asset_type.is_skeletal_animation():
                itask.get_igap_animation().set_editor_property('import_animations', True)
                itask.get_igap_mesh().set_editor_property('import_skeletal_meshes', False)
                itask.get_igap_mesh().set_editor_property('import_static_meshes', False)
                itask.get_igap_mesh().set_editor_property('create_physics_asset',False)
            else:
                itask.get_igap_animation().set_editor_property('import_animations', False)
                itask.get_igap_mesh().set_editor_property('import_skeletal_meshes', True)
                itask.get_igap_mesh().set_editor_property('import_static_meshes', True)
                if "create_physics_asset" in asset_data:
                    itask.get_igap_mesh().set_editor_property('create_physics_asset', asset_data["create_physics_asset"])
        else:
            if asset_type.is_skeletal_animation():
                itask.get_fbx_import_ui().set_editor_property('import_as_skeletal',True)
                itask.get_fbx_import_ui().set_editor_property('import_animations', True)
                itask.get_fbx_import_ui().set_editor_property('import_mesh', False)
                itask.get_fbx_import_ui().set_editor_property('create_physics_asset',False)
            else:
                itask.get_fbx_import_ui().set_editor_property('import_animations', False)
                itask.get_fbx_import_ui().set_editor_property('import_mesh', True)
                if "create_physics_asset" in asset_data:
                    itask.get_fbx_import_ui().set_editor_property('create_physics_asset', asset_data["create_physics_asset"])

        import_module_utils.print_debug_step("Process per-modules changes")
        # Vertex color
        bfu_import_vertex_color.bfu_import_vertex_color_utils.apply_import_settings(itask, asset_data, asset_additional_data)

        # Lods
        bfu_import_lods.bfu_import_lods_utils.apply_import_settings(itask, asset_data, asset_additional_data)

        # Materials
        bfu_import_materials.bfu_import_materials_utils.apply_import_settings(itask, asset_data, asset_additional_data)

        # Light Maps
        bfu_import_light_map.bfu_import_light_map_utils.apply_import_settings(itask, asset_data, asset_additional_data)

        # Nanite
        bfu_import_nanite.bfu_import_nanite_utils.apply_import_settings(itask, asset_data, asset_additional_data)

        if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
            itask.get_igap_mesh().set_editor_property('combine_static_meshes', True)
            itask.get_igap_mesh().set_editor_property('combine_skeletal_meshes', True)
            # @TODO auto_generate_collision Removed with InterchangeGenericAssetsPipeline? 
            # I yes need also remove auto_generate_collision from the addon propertys.
            itask.get_igap_mesh().set_editor_property('import_morph_targets', True)

            itask.get_igap_common_mesh().set_editor_property('recompute_normals', False)
            itask.get_igap_common_mesh().set_editor_property('recompute_tangents', False)

        else:
            if asset_type == ExportAssetType.STATIC_MESH:
                # unreal.FbxStaticMeshImportData
                itask.get_static_mesh_import_data().set_editor_property('combine_meshes', True)
                if "auto_generate_collision" in asset_data:
                    itask.get_static_mesh_import_data().set_editor_property('auto_generate_collision', asset_data["auto_generate_collision"])

            if asset_type.is_skeletal():
                # unreal.FbxSkeletalMeshImportData
                itask.get_skeletal_mesh_import_data().set_editor_property('import_morph_targets', True)
                itask.get_skeletal_mesh_import_data().set_editor_property('convert_scene', True)
                itask.get_skeletal_mesh_import_data().set_editor_property('normal_import_method', unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS)

    # ###############[ pre import ]################
    import_module_utils.print_debug_step("Process pre import")
    # Check is the file alredy exit
    if asset_additional_data:
        task_asset_full_path = itask.get_preview_import_refs()
        find_target_asset = import_module_unreal_utils.load_asset(task_asset_full_path)
        if find_target_asset:
            # Vertex color
            bfu_import_vertex_color.bfu_import_vertex_color_utils.apply_one_asset_settings(itask, find_target_asset, asset_additional_data)

    # ###############[ import asset ]################
    import_module_utils.print_debug_step("Process import asset")
    if asset_type.is_skeletal_animation():
        # For animation the script will import a skeletal mesh and remove after.
        # If the skeletal mesh already exists, try to remove it.

        asset_name = import_module_unreal_utils.clean_filename_for_unreal(asset_data["asset_name"])
        asset_import_path = asset_data['asset_import_path']
        asset_path = f"SkeletalMesh'/{asset_import_path}/{asset_name}.{asset_name}'"

        if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            old_asset = unreal.EditorAssetLibrary.find_asset_data(asset_path)
            if old_asset.asset_class == "SkeletalMesh":
                unreal.EditorAssetLibrary.delete_asset(asset_path)

    import_module_utils.print_debug_step("Process import...")
    itask.import_asset_task()
    import_module_utils.print_debug_step("Import asset done!")
    
    if len(itask.get_imported_assets()) == 0:
        fail_reason = 'Error zero imported object for: ' + asset_data["asset_name"]
        return fail_reason, None
    

    # ###############[ Post treatment ]################

    import_module_utils.print_debug_step("Process Post treatment")
    if asset_type.is_skeletal_animation():
        bfu_import_animations.bfu_import_animations_utils.apply_post_import_assets_changes(itask, asset_data)

    if asset_type == ExportAssetType.STATIC_MESH:

        if "collision_trace_flag" in asset_data:
            collision_data = itask.get_imported_static_mesh().get_editor_property('body_setup')
            if collision_data:
                if asset_data["collision_trace_flag"] == "CTF_UseDefault":
                    collision_data.set_editor_property('collision_trace_flag', unreal.CollisionTraceFlag.CTF_USE_DEFAULT)
                elif asset_data["collision_trace_flag"] == "CTF_UseSimpleAndComplex":
                    collision_data.set_editor_property('collision_trace_flag', unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX)
                elif asset_data["collision_trace_flag"] == "CTF_UseSimpleAsComplex":
                    collision_data.set_editor_property('collision_trace_flag', unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AS_COMPLEX)
                elif asset_data["collision_trace_flag"] == "CTF_UseComplexAsSimple":
                    collision_data.set_editor_property('collision_trace_flag', unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)

    if asset_type == ExportAssetType.SKELETAL_MESH:
        if origin_skeleton is None:
            # Unreal create a new skeleton when no skeleton was selected, so addon rename it.
            if import_module_unreal_utils.get_unreal_version() >= (5, 5, 0):
                skeleton = itask.get_imported_skeleton()
            else:
                # Before Unreal Engine 5.5, the skeleton is not included in the imported assets but still created.
                # So try to find using skeletal mesh name.
                skeletal_mesh = itask.get_imported_skeletal_mesh()
                if skeletal_mesh:
                    skeletal_mesh_name = skeletal_mesh.get_name()
                    skeletal_mesh_path = skeletal_mesh.get_path_name()
                    skeleton_path = skeletal_mesh_path.replace(skeletal_mesh_name, skeletal_mesh_name + "_Skeleton")
                    skeleton = unreal.EditorAssetLibrary.find_asset_data(skeleton_path).get_asset()
                else:
                    skeleton = None

            if skeleton:
                if "target_skeleton_import_ref" in asset_data:
                    print("Start rename skeleton...")
                    unreal.EditorAssetLibrary.rename_asset(skeleton.get_path_name(), asset_data["target_skeleton_import_ref"])
            else:
                print("Error: export skeleton not found after import!")
                print("Imported object paths:")
                for path in itask.task.imported_object_paths:
                    print(" -", path)

    if isinstance(itask.task_option, unreal.InterchangeGenericAssetsPipeline):
        if asset_type == ExportAssetType.STATIC_MESH:
            itask.get_igap_common_mesh().set_editor_property('recompute_normals', False)
            itask.get_igap_common_mesh().set_editor_property('recompute_tangents', False)

        if asset_type == ExportAssetType.SKELETAL_MESH:
            itask.get_igap_common_mesh().set_editor_property('recompute_normals', False)
            itask.get_igap_common_mesh().set_editor_property('recompute_tangents', False)

            if "enable_skeletal_mesh_per_poly_collision" in asset_data:
                itask.get_imported_skeletal_mesh().set_editor_property('enable_per_poly_collision', asset_data["enable_skeletal_mesh_per_poly_collision"])
        
    else:
        if asset_type == ExportAssetType.STATIC_MESH:
            static_mesh = itask.get_imported_static_mesh()
            if static_mesh:
                asset_import_data = static_mesh.get_editor_property('asset_import_data')
                asset_import_data.set_editor_property('normal_import_method', unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS)
            else:
                print("Error: Static Mesh not found after import!")

        elif asset_type == ExportAssetType.SKELETAL_MESH:
            skeletal_mesh = itask.get_imported_skeletal_mesh()
            if skeletal_mesh:
                asset_import_data = skeletal_mesh.get_editor_property('asset_import_data')
                asset_import_data.set_editor_property('normal_import_method', unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS)
            
                if "enable_skeletal_mesh_per_poly_collision" in asset_data:
                    skeletal_mesh.set_editor_property('enable_per_poly_collision', asset_data["enable_skeletal_mesh_per_poly_collision"])
                
            else:
                print("Error: Skeletal Mesh not found after import!")


    # Socket
    if asset_type == ExportAssetType.SKELETAL_MESH:
        # Import the SkeletalMesh socket(s)
        sockets_to_add = asset_additional_data["Sockets"]
        for socket in sockets_to_add:
            old_socket = itask.get_imported_skeletal_mesh().find_socket(socket["SocketName"])
            if old_socket:
                # Edit socket
                pass
                # old_socket.relative_location = socket["Location"]
                # old_socket.relative_rotation = socket["Rotation"]
                # old_socket.relative_scale = socket["Scale"]

            else:
                # Create socket
                pass
                # new_socket = unreal.SkeletalMeshSocket(asset)
                # new_socket.socket_name = socket["SocketName"]
                # new_socket.bone_name = socket["BoneName"]
                # new_socket.relative_location = socket["Location"]
                # new_socket.relative_rotation = socket["Rotation"]
                # new_socket.relative_scale = socket["Scale"]
                # NEED UNREAL ENGINE IMPLEMENTATION IN PYTHON API.
                # skeleton.add_socket(new_socket)

    # Preview mesh
    if asset_type.is_skeletal_animation():
        import_module_post_treatment.set_sequence_preview_skeletal_mesh(itask.get_imported_anim_sequence(), origin_skeletal_mesh)

    import_module_utils.print_debug_step("Process per-modules apply asset settings")
    # Vertex color
    bfu_import_vertex_color.bfu_import_vertex_color_utils.apply_asset_settings(itask, asset_additional_data)

    # Lods
    bfu_import_lods.bfu_import_lods_utils.apply_asset_settings(itask, asset_additional_data)

    # Materials
    bfu_import_materials.bfu_import_materials_utils.apply_asset_settings(itask, asset_additional_data)

    # Light maps
    bfu_import_light_map.bfu_import_light_map_utils.apply_asset_settings(itask, asset_additional_data)

    # Nanite
    bfu_import_nanite.bfu_import_nanite_utils.apply_asset_settings(itask, asset_additional_data)

    if asset_type == ExportAssetType.ANIM_ALEMBIC:
        pass
        # @TODO Need to found how create an physical asset, generate bodies, and assign it.
        """
        skeletal_mesh_path = itask.GetImportedSkeletalMeshAsset().get_path_name()
        path = skeletal_mesh_path.rsplit('/', 1)[0]
        name = skeletal_mesh_path.rsplit('/', 1)[1] + "_Physics"

        physical_asset_factory = unreal.PhysicsAssetFactory()
        physical_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name=name,
            package_path=path,
            asset_class=unreal.PhysicsAsset,
            factory=physical_asset_factory
        )
        """


    # #################################[EndChange]
    return "SUCCESS", itask.get_imported_assets()

def ImportAllAssets(assets_data, show_finished_popup=True):
    import_counter = 0
    ImportedList = []
    ImportFailList = []

    def GetAssetByType(types: List[str]):
        target_assets = []
        for asset in assets_data["assets"]:
            if asset["asset_type"] in types:
                target_assets.append(asset)
        return target_assets

    def PrepareImportTask(asset_data):
        nonlocal import_counter
        bpl.advprint.print_separator()
        counter = str(import_counter + 1) + "/" + str(len(assets_data["assets"]))
        asset_name = asset_data["asset_name"]
        import_task_message = f"Import asset {counter}: '{asset_name}'"
        print("###", import_task_message)

        result, assets = ImportTask(asset_data)

        if result == "SUCCESS":
            ImportedList.append([assets, asset_data["asset_type"]])
        else:
            ImportFailList.append(result)
        import_counter += 1

        bpl.advprint.print_separator()



    # Process import
    bpl.advprint.print_simple_title("Import started !")
    counter = bpl.utils.CounterTimer()

    # Import assets with a specific order

    for asset_data in GetAssetByType(["AlembicAnimation", "GroomSimulation", "Spline", "Camera"]):
        PrepareImportTask(asset_data)
    for asset_data in GetAssetByType(["StaticMesh", "CollectionStaticMesh"]):
        PrepareImportTask(asset_data)
    for asset_data in GetAssetByType(["SkeletalMesh"]):
        PrepareImportTask(asset_data)
    for asset_data in GetAssetByType(["SkeletalAnimation", "Action", "Pose", "NonLinearAnimation"]):
        PrepareImportTask(asset_data)

    bpl.advprint.print_simple_title("Full import completed !")

    # import result
    StaticMesh_ImportedList = []
    SkeletalMesh_ImportedList = []
    Alembic_ImportedList = []
    Animation_ImportedList = []
    for inport_data in ImportedList:
        assets = inport_data[0]
        source_asset_type = ExportAssetType.get_asset_type_from_string(inport_data[1])
        if source_asset_type == ExportAssetType.STATIC_MESH:
            StaticMesh_ImportedList.append(assets)
        elif source_asset_type == ExportAssetType.SKELETAL_MESH:
            SkeletalMesh_ImportedList.append(assets)
        elif source_asset_type == ExportAssetType.ANIM_ALEMBIC:
            Alembic_ImportedList.append(assets)
        else:
            Animation_ImportedList.append(assets)

    import_log = []
    import_log.append('Imported StaticMesh: '+str(len(StaticMesh_ImportedList)))
    import_log.append('Imported SkeletalMesh: '+str(len(SkeletalMesh_ImportedList)))
    import_log.append('Imported Alembic: '+str(len(Alembic_ImportedList)))
    import_log.append('Imported Animation: '+str(len(Animation_ImportedList)))
    import_log.append('Import failled: '+str(len(ImportFailList)))

    for import_row in import_log:
        print(import_row)
        
    for error in ImportFailList:
        print(error)

    asset_paths = []
    for assets in (StaticMesh_ImportedList + SkeletalMesh_ImportedList + Alembic_ImportedList + Animation_ImportedList):
        for asset in assets:
            asset_paths.append(asset.get_path_name())

    if config.save_assets_after_import:
        # Save asset(s) after import
        for path in asset_paths:
            unreal.EditorAssetLibrary.save_asset(path)

    if config.select_assets_after_import:
        # Select asset(s) in content browser
        unreal.EditorAssetLibrary.sync_browser_to_objects(asset_paths)
    
    title = "Import finished!"
    if show_finished_popup:
        if len(ImportFailList) > 0:
            message = 'Some asset(s) could not be imported.' + "\n"
        else:
            message = 'All assets imported with success!' + "\n"

        message += "Import finished in " + counter.get_str_time() + "\n"
        message += "\n"
        for import_row in import_log:
            message += import_row + "\n"

        if len(ImportFailList) > 0:
            message += "\n"
            for error in ImportFailList:
                message += error + "\n"

        import_module_unreal_utils.show_simple_message(title, message)
    else:
        bpl.advprint.print_simple_title(title)
    bpl.advprint.print_separator()

    return True
