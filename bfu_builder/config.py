from typing import List, Tuple
from pathlib import Path


class BlenderVersionDetails:
    def __init__(self, version: Tuple[int, int, int]):
        self.version: Tuple[int, int, int] = version
        self.path:Path = Path()

        # Disable TBB malloc replacement to avoid issues with Blender 4.2+ More details: https://projects.blender.org/blender/blender/issues/126109
        self.fix_allocation_functions_replacement: bool = False


blender_version_and_path: List[BlenderVersionDetails] = []

def add_blender_version(version: Tuple[int, int, int], path: Path) -> BlenderVersionDetails:
    details = BlenderVersionDetails(version)
    details.path = path
    blender_version_and_path.append(details)
    details.fix_allocation_functions_replacement = version == (4, 2, 0)
    return details

# Use default installation paths on Windows, adjust it for Linux or MacOS
add_blender_version((4, 5, 0), Path("C:/Program Files/Blender Foundation/Blender 4.5/blender.exe"))
add_blender_version((4, 4, 0), Path("C:/Program Files/Blender Foundation/Blender 4.4/blender.exe"))
add_blender_version((4, 3, 0), Path("C:/Program Files/Blender Foundation/Blender 4.3/blender.exe"))
add_blender_version((4, 2, 0), Path("C:/Program Files/Blender Foundation/Blender 4.2/blender.exe"))
add_blender_version((4, 1, 0), Path("C:/Program Files/Blender Foundation/Blender 4.1/blender.exe"))
add_blender_version((4, 0, 0), Path("C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"))
add_blender_version((3, 6, 0), Path("C:/Program Files/Blender Foundation/Blender 3.6/blender.exe"))
add_blender_version((3, 5, 0), Path("C:/Program Files/Blender Foundation/Blender 3.5/blender.exe"))
add_blender_version((3, 4, 0), Path("C:/Program Files/Blender Foundation/Blender 3.4/blender.exe"))
add_blender_version((3, 3, 0), Path("C:/Program Files/Blender Foundation/Blender 3.3/blender.exe"))
add_blender_version((3, 2, 0), Path("C:/Program Files/Blender Foundation/Blender 3.2/blender.exe"))
add_blender_version((3, 1, 0), Path("C:/Program Files/Blender Foundation/Blender 3.1/blender.exe"))
add_blender_version((3, 0, 0), Path("C:/Program Files/Blender Foundation/Blender 3.0/blender.exe"))
add_blender_version((2, 93, 0), Path("C:/Program Files/Blender Foundation/Blender 2.93/blender.exe"))
add_blender_version((2, 92, 0), Path("C:/Program Files/Blender Foundation/Blender 2.92/blender.exe"))
add_blender_version((2, 91, 0), Path("C:/Program Files/Blender Foundation/Blender 2.91/blender.exe"))
add_blender_version((2, 90, 0), Path("C:/Program Files/Blender Foundation/Blender 2.90/blender.exe"))
add_blender_version((2, 83, 0), Path("C:/Program Files/Blender Foundation/Blender 2.83/blender.exe"))
add_blender_version((2, 82, 0), Path("C:/Program Files/Blender Foundation/Blender 2.82/blender.exe"))
add_blender_version((2, 81, 0), Path("C:/Program Files/Blender Foundation/Blender 2.81/blender.exe"))
add_blender_version((2, 80, 0), Path("C:/Program Files/Blender Foundation/Blender/blender.exe"))

blender_download_page = "https://download.blender.org/release/"