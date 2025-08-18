# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

Please note: I changed the work folder name so when installing the addon, be sure to uninstall the previous version first. 
If not you will have both versions installed, conflicts may occur.

### Version 4.4.1
- New: New collection asset preview. ("Show Assets" button)
- New: New asset cache management system for actions.
- Changes: Optimized armature action export search.
    Test file without caching:
    - Action Auto Search: from 32.0 ms to 24.0 ms
    - Action Specific List: from 33.0 ms to 0.09 ms
    - Action Specific Prefix: from 32.0 ms to 0.1 ms
    - Action Current: from 32.0 ms to 0.005 ms
    Draw with caching:
    - Any: from 32.0 ms to 0.6 ms
- Changes: Improved translation support and performance.
- Changes: General code cleanup and optimization.
- Fixed: Exporting scene collection produces script fail.
- Fixed: Default path export at disc root instead of relative to .blend file.
- Fixed: AxisPropertys in FBX export are not visible in UI.
- Fixed: Can't access collection properties in the UI if no active object.
- Fixed: "Calculate all surface area" produce script error.
- Fixed: FBX export produces script error on Blender 2.8 (Backwards compatibility issues).