import os
import platform
import shutil
import re
from typing import List, Tuple, Optional
from pathlib import Path
from . import edit_files
from . import edit_fbx_utils
from . import edit_export_fbx_bin

# Detect the current operating system
current_system = platform.system()
if current_system == "Windows":
    blender_install_folder = r"U:\\BlenderBuilds"
elif current_system == "Linux":
    blender_install_folder = r"/media/bleuraven/Game Engines/BlenderBuilds"


io_scene_fbx_prefix = "io_scene_fbx_"

export_fbx_files = [
    'data_types.py',
    'encode_bin.py',
    'export_fbx_bin.py',
    'fbx_utils.py',
]

export_fbx_files_with_threading = [
    'data_types.py',
    'encode_bin.py',
    'export_fbx_bin.py',
    'fbx_utils_threading.py',
    'fbx_utils.py',
]

all_export_fbx_files = [
    'data_types.py',
    'encode_bin.py',
    'export_fbx_bin.py',
    'fbx_utils_threading.py',
    'fbx_utils.py',
    'fbx2json.py',
    'import_fbx.py',
    'json2fbx.py',
    'parse_fbx.py',
]

all_export_fbx_files_with_init = [
    '__init__.py',
    'data_types.py',
    'encode_bin.py',
    'export_fbx_bin.py',
    'fbx_utils_threading.py',
    'fbx_utils.py',
    'fbx2json.py',
    'import_fbx.py',
    'json2fbx.py',
    'parse_fbx.py',
]



# Get the directory of the current script
current_script_directory: Path = Path(__file__).resolve().parent
# Define the parent directory (one level up from the current script directory)
parent_directory: Path = current_script_directory.parent

class FBXExporterGenerate:
    def __init__(self, version: Tuple[int, int, int], folder: str, files: List[str], new_io_fbx: Optional[str] = None):
        self.version: Tuple[int, int, int] = version
        self.folder: str = folder
        self.files: List[str] = files
        self.fbx_addon_version: Tuple[int, int, int] = (0, 0, 0)  # Default version
        if new_io_fbx:
            self.io_fbx: str = new_io_fbx
        else:
            self.io_fbx: str = r"scripts/addons/io_scene_fbx"

        self.run_init_check()

    def run_init_check(self):
        def print_red(message: str):
            print(f"\033[91m{message}\033[0m")
        if not self.get_addon_path().exists():
            print_red(f"Addon path does not exist: {self.get_addon_path()}")
            return False
        if not self.get_addon_init_path().exists():
            print_red(f"Addon init path does not exist: {self.get_addon_init_path()}")
            return False
        return True

    def get_str_version(self):
        return str(self.version[0])+"_"+str(self.version[1])
    
    def get_folder_str_version(self):
        return str(self.version[0])+"."+str(self.version[1])

    def get_addon_path(self) -> Path:
        addon_path = Path(blender_install_folder) / self.folder / self.io_fbx
        return addon_path.resolve()
    
    def get_addon_init_path(self) -> Path:
        addon_path = Path(blender_install_folder) / self.folder / self.io_fbx / '__init__.py'
        return addon_path.resolve()

    def run_generate(self) -> Tuple[Tuple[int, int, int], str]:
        # Create the destination folder in the parent directory
        self.update_fbx_addon_version()
        version_as_module: str = self.get_str_version()
        print("Start Generate ", version_as_module)
        dest_folder: Path = parent_directory / (io_scene_fbx_prefix + version_as_module)
        if not dest_folder.exists():
            dest_folder.mkdir(parents=True)

        new_files: List[Path] = self.copy_export_files(dest_folder)
        new_files.append(self.create_init_file(dest_folder))

        for new_file in new_files:
            print("Process file:", new_file)
            edit_files.add_header_to_file(new_file)
            if str(new_file).endswith('export_fbx_bin.py'):
                edit_export_fbx_bin.update_export_fbx_bin(new_file, self.version, self.fbx_addon_version)
            if str(new_file).endswith('fbx_utils.py'):
                edit_fbx_utils.update_fbx_utils(new_file, self.version)
        return (self.version, version_as_module)
    
    def update_fbx_addon_version(self):
        source_file = Path(self.get_addon_init_path())

        with open(source_file, 'r') as file:
            file_content = file.read()
            
            # Utiliser les expressions régulières pour trouver bl_info et la version
            bl_info_match = re.search(r'bl_info\s*=\s*\{([^}]*)\}', file_content, re.DOTALL)
            bl_info_lines = bl_info_match.group(1).split('\n')
            
            # Analyser chaque ligne pour trouver la version
            for line in bl_info_lines:
                if 'version' in line:
                    match = re.search(r'\(([^)]+)\)', line)
                    elements = match.group(1).replace(' ', '').split(',')
                    self.fbx_addon_version = tuple(map(int, elements))
                    return

    def copy_export_files(self, dest_folder: Path) -> List[Path]:
        addon_folder = self.get_addon_path()
        new_files = []
        # Verify if the source folder exists
        if not addon_folder.exists():
            print(f"Source folder does not exist: {addon_folder}")
            return

        # Copy only specified files from the source to the destination
        for file_name in self.files:
            source_file = addon_folder / file_name
            destination_file = dest_folder / file_name
            if source_file.exists():
                shutil.copy2(source_file, destination_file)
                new_files.append(destination_file)
            else:
                print(f"File does not exist: {source_file}")

        print(f"Copied specified FBX exporter files.")
        print(f"Source: {source_file}")
        print(f"Target: {dest_folder}")
        return new_files


    def create_init_file(self, dest_folder: Path) -> Path:
        files = self.files
        init_file_path = dest_folder / '__init__.py'
        with open(init_file_path, 'w') as init_file:
            # Write imports
            for file_name in files:
                module_name = os.path.splitext(file_name)[0]
                init_file.write(f"from . import {module_name}\n")
            
            
            init_file.write('\nif "bpy" in locals():\n')
            init_file.write("\timport importlib\n")
            
            # Write reloads
            for file_name in files:
                module_name = os.path.splitext(file_name)[0]
                if module_name in ["import_fbx", "fbx_utils"]:
                    
                    init_file.write(f"# import_fbx and fbx_utils should not be reload or the export will produce StructRNA errors. \n")
                    init_file.write(f"#\tif \"{module_name}\" in locals():\n")
                    init_file.write(f"#\t\timportlib.reload({module_name})\n")
                else:
                    init_file.write(f"\tif \"{module_name}\" in locals():\n")
                    init_file.write(f"\t\timportlib.reload({module_name})\n")

        print(f"Created __init__.py in {dest_folder}")
        return init_file_path

def run_all_generate():
    os.system('cls' if os.name == 'nt' else 'clear')
    clean_previous_exports()

    # generated var needs to be ordered from new to older.
    generator_list: List[FBXExporterGenerate] = []
    generated_list: List[Tuple[Tuple[int, int, int], str]] = []

    generator_list.append(FBXExporterGenerate((4, 5, 0), r"Blender_v4.5", export_fbx_files_with_threading, r"scripts/addons_core/io_scene_fbx/"))
    generator_list.append(FBXExporterGenerate((4, 4, 0), r"Blender_v4.4", export_fbx_files_with_threading, r"scripts/addons_core/io_scene_fbx/"))
    generator_list.append(FBXExporterGenerate((4, 3, 0), r"Blender_v4.3", export_fbx_files_with_threading, r"scripts/addons_core/io_scene_fbx/"))
    generator_list.append(FBXExporterGenerate((4, 2, 0), r"Blender_v4.2", export_fbx_files_with_threading, r"scripts/addons_core/io_scene_fbx/"))
    generator_list.append(FBXExporterGenerate((4, 1, 0), r"Blender 4.1/4.1", export_fbx_files_with_threading))
    generator_list.append(FBXExporterGenerate((4, 0, 0), r"Blender 4.0/4.0", export_fbx_files))
    generator_list.append(FBXExporterGenerate((3, 6, 0), r"Blender 3.6/3.6", export_fbx_files))
    generator_list.append(FBXExporterGenerate((3, 5, 0), r"Blender 3.5/3.5", export_fbx_files))
    generator_list.append(FBXExporterGenerate((3, 4, 0), r"Blender 3.4/3.4", export_fbx_files))
    generator_list.append(FBXExporterGenerate((3, 3, 0), r"Blender 3.3/3.3", export_fbx_files))
    generator_list.append(FBXExporterGenerate((3, 2, 0), r"Blender 3.2/3.2", export_fbx_files))
    generator_list.append(FBXExporterGenerate((3, 1, 0), r"Blender 3.1/3.1", export_fbx_files))
    generator_list.append(FBXExporterGenerate((2, 93, 0), r"Blender 2.93/2.93", export_fbx_files))
    generator_list.append(FBXExporterGenerate((2, 83, 0), r"Blender 2.83/2.83", export_fbx_files))

    for generator in generator_list:
        generated_list.append(generator.run_generate())

    root_init_file = create_root_init_file(generated_list)
    edit_files.add_header_to_file(root_init_file)


def create_root_init_file(generated_list: List[Tuple[Tuple[int, int, int], str]]) -> Path:
    init_file_path: Path = Path(parent_directory) / '__init__.py'
    with open(init_file_path, 'w') as init_file:
        init_file.write("import bpy\n")
        init_file.write("import importlib\n")
        init_file.write("blender_version = bpy.app.version\n\n")

        # Write conditional imports
        for x, generate in enumerate(generated_list):
            version = generate[0]
            str_version = generate[1]
            if x == 0:
                init_file.write(f"if blender_version >= {version}:\n")
            else:
                init_file.write(f"elif blender_version >= {version}:\n")
            init_file.write(f"    from . import {io_scene_fbx_prefix}{str_version} as current_fbxio \n")
            
        init_file.write(f"else:\n")
        init_file.write(f"    print('ERROR, no fbx exporter found for this version of Blender!') \n")

        init_file.write("\n")
        
        # Write reloads
        init_file.write(f"if \"current_fbxio\" in locals():\n")
        init_file.write(f"    importlib.reload(current_fbxio)\n")

    print(f"Created root __init__.py in {parent_directory}")
    return init_file_path

def clean_previous_exports():
    for item in os.listdir(parent_directory):
        if item.startswith(io_scene_fbx_prefix):
            folder_path: Path = Path(parent_directory) / item
            if folder_path.is_dir():
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}")


