import bpy
import importlib

from . import bfu_export_correct_and_improv_panel

if "bfu_export_correct_and_improv_panel" in locals():
    importlib.reload(bfu_export_correct_and_improv_panel)

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bfu_export_correct_and_improv_panel.register()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bfu_export_correct_and_improv_panel.unregister()
