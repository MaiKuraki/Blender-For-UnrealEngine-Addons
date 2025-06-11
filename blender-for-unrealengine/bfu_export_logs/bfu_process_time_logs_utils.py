import bpy
from typing import List
from . import bfu_process_time_logs_types 


def get_process_time_logs() -> List[bfu_process_time_logs_types.BFU_OT_ExportProcessTimeLog]:
    if bpy.context is None:
        return []
    scene = bpy.context.scene
    return scene.bfu_export_process_time_logs  # type: ignore[attr-defined]

def start_time_log(process_info: str) -> bfu_process_time_logs_types.SafeTimeLogHandle:
    process_task_proxy = bfu_process_time_logs_types.SafeTimeLogHandle()
    process_task_proxy.start_timer(process_info)
    return process_task_proxy

def clear_process_time_logs():
    if bpy.context is None:
        return
    scene = bpy.context.scene
    scene.bfu_export_process_time_logs.clear()  # type: ignore[attr-defined]

def get_process_time_logs_details():
    export_log = ""
    for log in get_process_time_logs():
        export_log += f"- {log.get_process_detail()} \n"

    return export_log