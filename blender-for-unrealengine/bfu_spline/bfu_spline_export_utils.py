import bpy

from . import bfu_spline_write_text
from . import bfu_spline_data
from .. import bfu_basics
from .. import bfu_export_text_files

def ExportSingleAdditionalTrackSpline(dirpath, filename, obj, pre_bake_spline: bfu_spline_data.BFU_SplinesList = None):
    # Export additional spline track for Unreal Engine
    # FocalLength
    # FocusDistance
    # Aperture

    absdirpath = bpy.path.abspath(dirpath)
    bfu_basics.verifi_dirs(absdirpath)
    AdditionalTrack = bfu_spline_write_text.write_spline_points_data(obj, pre_bake_spline=pre_bake_spline)
    return bfu_export_text_files.bfu_export_text_files_utils.export_single_json_file(
        AdditionalTrack,
        absdirpath,
        filename
        )