import bpy
from typing import Any, Optional, Dict
from . import bfu_spline_data
from .. import languages
from .. import bfu_export_text_files

def WriteSplinePointsData(obj: bpy.types.Object, pre_bake_spline: bfu_spline_data.BFU_SplinesList) -> Dict[str, Any]:
    # Write as data spline animation tracks


    data: Dict[str, Any] = {}
    bfu_export_text_files.bfu_export_text_files_utils.add_generated_json_header(data, languages.ti('write_text_additional_track_spline'))
    bfu_export_text_files.bfu_export_text_files_utils.add_generated_json_meta_data(data)

 
    if pre_bake_spline:
        spline_tracks = pre_bake_spline.get_spline_list_values_as_dict()
    else:
        multi_spline_tracks = bfu_spline_data.BFU_MultiSplineTracks()
        multi_spline_tracks.add_spline_to_evaluate(obj)
        multi_spline_tracks.evaluate_all_splines()
        spline_tracks = multi_spline_tracks.get_evaluate_spline_data_as_dict(obj)
    data.update(spline_tracks)

    bfu_export_text_files.bfu_export_text_files_utils.add_generated_json_footer(data)
    return data

