# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

### Version 4.3.13

- New: Sub folder support for modular skeletal meshs.
- New: Better and more checks for potential issue checker.
- Changed: "Check Potential Errors" renamed "Check Potential Issues".
- Changed: New wiki button for open Lods page.
- Changed: The default export folder "ExportedFbx" is now "ExportedAssets".
- Changed: The default export folder "ImportedFbx" is now "ImportedBlenderAssets".
- Changed: "Export animation without mesh" moved in animations tab and it now False by default.
- Fixed: Check Potential shape keys issues identify the wrong modifiers.
- Fixed: In Blender 4.4 the app crash with some constraint. (Removing constraints now also removes the driver's influence to avoid crashing.)
- Fixed: Import script do not use the the correct name for search and apply pre import setting.
- Fixed: All panel under a accordion contain a small space over it.
- Fixed: Import counter is wrong when an import fails.
- Fixed: Static Mesh Lod Groups is set at import but never apply.
- Fixed: Script when try to replace a read only file. (Happens when Unreal use it at the same time)
- Fixed: Asset number is None in the export logs.
- Fixed: Animation export may stay idle (NLA export fail, fixed with BBPL update)
- Fixed: Modifiers distances not updated wihe the rescale when the Unit Scale is not set to 0.01.
