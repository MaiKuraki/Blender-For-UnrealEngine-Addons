from typing import Optional
from . import bpl
from . import config
from . import blender_exec
from .blender_version_manager import BlenderVersionList


def run_blender_test_build(blender_detail: config.BlenderVersionDetails, note: Optional[str] = None):
    print(f"Testing Blender {blender_detail.version} at {blender_detail.path}")
    if note:
        print(note)
    print("#" * 50)
    print()
    blender_exec.test_blender_installation(blender_detail)

def main():
    bpl.console_utils.clear_console()
    bpl.advprint.print_simple_title("Blender For Unreal Engine Addons Builder")
    print("-" * 50)

    blender_version = BlenderVersionList()
    blender_version.add_blender_versions(config.blender_version_and_path)
    print("Checking Blender installations...")
    blender_version.check_blender_path()

    print("What you want to do?")
    print("1. Build all addons for all Blender versions")
    for x, blender_detail in enumerate(blender_version.blender_versions.values()):
        print(f"{x + 2}. Test build only for Blender {blender_detail.version} at {blender_detail.path}")
    choice = input("Enter your choice: ")
    

    if choice == "1":
        # Build for all Blender versions
        version_length = len(blender_version.blender_versions)
        # reversed loop
        for x, blender_detail in enumerate(reversed(list(blender_version.blender_versions.values()))):
            step = f"Step {x + 1} of {version_length}:"
            run_blender_test_build(blender_detail, step)
    else:
        try:
            index = int(choice) - 2
            if 0 <= index < len(blender_version.blender_versions):
                blender_detail = list(blender_version.blender_versions.values())[index]
                run_blender_test_build(blender_detail)
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")


