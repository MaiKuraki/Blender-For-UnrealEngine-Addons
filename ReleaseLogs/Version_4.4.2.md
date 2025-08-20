# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

### Version 4.4.2
- New: Added `bfu_export_skeletal_animation_file_path` to support custom skeletal animations path
- Changed: Renamed `bfu_export_static_file_path` to `bfu_export_static_mesh_file_path` for clarity
- Changed: Renamed `bfu_export_skeletal_file_path` to `bfu_export_skeletal_mesh_file_path` for clarity
- Fixed: Cached action system may reference and use removed StructRNA. Add checks to avoid script fails.
- Fixed: Old Interchange check function produce script errors at import.
