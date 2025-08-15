# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

### Version 4.4.1

- Changes: Optimized armature action export search.
    Test file:
    - Export Auto Search: from 32.0 ms to 24.0 ms
    - Export Specific List: from 33.0 ms to 0.09 ms
    - Export Specific Prefix: from 32.0 ms to 0.10 ms
    - Export Current: from 32.0 ms to 0.005 ms
- Changes: Improved translation support and performance.
- Fixed: Exporting scene collection produces script fail.
- Fixed: Default path export at disc root instead of relative to .blend file.
- Fixed: AxisPropertys in FBX export are not visible in UI.