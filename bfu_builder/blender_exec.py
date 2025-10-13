import subprocess
from . import bpl
from .config import BlenderVersionDetails
from pathlib import Path


def test_blender_installation(blender_detail: BlenderVersionDetails) -> bool:
    blender_executable_path = blender_detail.path
    if not blender_executable_path.exists():
        print(f"Blender executable not found at {blender_executable_path}")
        return False

    # Get the addon path from the current build file path
    # Get the current file path
    current_file_path = Path(__file__).resolve()
    # Le dossier blender_for_unrealengine est au niveau parent de bfu_builder
    addon_path: Path = current_file_path.parent.parent / "blender_for_unrealengine"
    
    # Path to the install script
    install_script_path = current_file_path.parent / "install_addon.py"

    command = [
        str(blender_executable_path),
        '--background',
        '--factory-startup',
        '--python', str(install_script_path),
        '--',  # Separator to indicate that the following arguments are for the Python script
        '--addon_path', str(addon_path)  # Pass addon_path as a named argument
    ]
    

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Blender script executed successfully")
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(bpl.color_set.red(f"Error executing Blender script: {e}"))
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False