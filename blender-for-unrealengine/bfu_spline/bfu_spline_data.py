import bpy
import math
import mathutils
from typing import Dict, Any, List, Union, TYPE_CHECKING
from .. import bfu_utils
from . import bfu_spline_utils
from . import bfu_spline_unreal_utils

def float_as_ue(my_float: float) -> str:
    return "{:.6f}".format(my_float)

def vector_as_ue(vector_data: mathutils.Vector) -> Dict[str, str]:
    vector: Dict[str, str] = {}        
    vector["X"] = "{:.6f}".format(vector_data.x)
    vector["Y"] = "{:.6f}".format(vector_data.y)
    vector["Z"] = "{:.6f}".format(vector_data.z)
    return vector

def quad_as_ue(quad_data: mathutils.Quaternion) -> Dict[str, str]:
    quad: Dict[str, str] = {}
    quad["X"] = "{:.6f}".format(quad_data.x)
    quad["Y"] = "{:.6f}".format(quad_data.y)
    quad["Z"] = "{:.6f}".format(quad_data.z)
    quad["W"] = "{:.6f}".format(quad_data.w)
    return quad

class BFU_SimpleSplinePoint():

    def __init__(self, spline_obj: bpy.types.Object, point_data: Union[bpy.types.SplinePoint, bpy.types.BezierSplinePoint], point_type: str):
        # Context stats

        self.position: mathutils.Vector = mathutils.Vector((0,0,0))
        self.handle_left: mathutils.Vector = mathutils.Vector((0,0,0)) # Handle left is the "Arrive Tangent" in UE
        self.handle_left_type = "FREE"
        self.handle_right: mathutils.Vector = mathutils.Vector((0,0,0)) # Handle right is the "Leave Tangent" in UE
        self.handle_right_type = "FREE"
        self.curve_roll: float = self.get_curve_roll(spline_obj, point_data)
        self.curve_radius: float = point_data.radius

        self.point_type = point_type

        if point_type in ["BEZIER"]:
            if isinstance(point_data, bpy.types.BezierSplinePoint):
                self.set_point_from_bezier(point_data)
        elif point_type in ["NURBS"]:
            print("NURBS curves need to be resampled!")
        elif point_type in ["POLY"]:
            if isinstance(point_data, bpy.types.SplinePoint):
                self.set_point_from_poly(point_data)

    def get_curve_roll(self, spline_obj: bpy.types.Object, point_data: Union[bpy.types.SplinePoint, bpy.types.BezierSplinePoint]) -> float:
        if isinstance(point_data, bpy.types.BezierSplinePoint):
            if isinstance(spline_obj.data, bpy.types.Curve):
                # For the momment roll work only with Z_UP mode.
                # Need a way to evaluate the roll at spline points.
                # It possible to brut force using a PathDummy with Follow Path constraint but that very heavy...
                # Please.
                if spline_obj.data.twist_mode == 'Z_UP':
                    return point_data.tilt
        else:
            return point_data.tilt
            
        return 0.0
    
    def set_point_from_bezier(self, point_data: bpy.types.BezierSplinePoint):
        self.handle_left_type = "VECTOR"
        self.handle_right_type = "VECTOR"
        self.position = point_data.co.copy()
        self.handle_left = point_data.handle_left.copy()
        self.handle_right = point_data.handle_right.copy()

    def set_point_from_poly(self, point_data: bpy.types.SplinePoint):
        self.handle_left_type = "VECTOR"
        self.handle_right_type = "VECTOR"
        real_position = mathutils.Vector((0,0,0))
        real_position.x = point_data.co.x
        real_position.y = point_data.co.y
        real_position.z = point_data.co.z
        self.position = real_position
        self.handle_left = real_position
        self.handle_right = real_position

    def get_ue_position(self) -> mathutils.Vector:
        ue_position = self.position.copy()
        ue_position *= mathutils.Vector((1,-1,1))
        if TYPE_CHECKING:
            vector_scale = mathutils.Vector((1, 1, 1))
        else:
            vector_scale = mathutils.Vector(bpy.context.scene.bfu_spline_vector_scale)
        ue_position *= vector_scale

        return ue_position

    def get_ue_handle_left(self) -> mathutils.Vector:
        ue_handle_left = self.handle_left.copy()
        ue_handle_left -= self.position
        ue_handle_left *= mathutils.Vector((-3,3,-3))
        if TYPE_CHECKING:
            vector_scale = mathutils.Vector((1, 1, 1))
        else:
            vector_scale = mathutils.Vector(bpy.context.scene.bfu_spline_vector_scale)
        ue_handle_left *= vector_scale

        return ue_handle_left

    def get_ue_handle_right(self) -> mathutils.Vector:
        ue_handle_right = self.handle_right.copy()
        ue_handle_right -= self.position
        ue_handle_right *= mathutils.Vector((3,-3,3))
        if TYPE_CHECKING:
            vector_scale = mathutils.Vector((1, 1, 1))
        else:
            vector_scale = mathutils.Vector(bpy.context.scene.bfu_spline_vector_scale)
        ue_handle_right *= vector_scale

        return ue_handle_right

    """
    -------------
    position: <Vector (-20.0000, 20.0000, 0.0000)>
    left_handle: <Vector (-30.0000, 20.0000, -0.0000)>
    right_handle: <Vector (-30.0000, 20.0000, -0.0000)>
    true_roll: 0.0
    Target -> Roll: 0.00, Pitch: 0.00, Yaw: 0.00
    -------------
    position: <Vector (0.0000, 20.0000, 0.0000)>
    left_handle: <Vector (-9.3969, 16.5798, -0.0000)>
    right_handle: <Vector (-9.3969, 16.5798, -0.0000)>
    true_roll: 0.0
    Target -> Roll: 0.00, Pitch: 0.00, Yaw: -20.00
    -------------
    position: <Vector (20.0000, 20.0000, 0.0000)>
    left_handle: <Vector (10.6031, 20.0000, 3.4202)>
    right_handle: <Vector (10.6031, 20.0000, 3.4202)>
    true_roll: 0.0
    Target -> Roll: 0.00, Pitch: -20.00, Yaw: 0.00
    -------------
    position: <Vector (40.0000, 20.0000, 0.0000)>
    left_handle: <Vector (30.0000, 20.0000, -0.0000)>
    right_handle: <Vector (30.0000, 20.0000, -0.0000)>
    true_roll: 45.0
    Target -> Roll: 45.00, Pitch: 0.00, Yaw: 0.00
    """

    def convert_blender_quat_to_unreal(self, quat: mathutils.Quaternion) -> mathutils.Quaternion:
        # Convert quaternion to matrix
        mat = quat.to_matrix().to_4x4()

        # Blender (X=Right, Y=Forward, Z=Up)
        # Unreal  (X=Forward, Y=Right, Z=Up)
        # So remap axes: [X,Y,Z] => [Y,X,Z]
        remap = mathutils.Matrix((
            (0, 1, 0, 0),  # X = Blender Y
            (1, 0, 0, 0),  # Y = Blender X
            (0, 0, 1, 0),  # Z unchanged
            (0, 0, 0, 1)
        ))

        # Apply the axis remap
        mat_unreal = remap @ mat
        return mat_unreal.to_quaternion()

    def get_ue_rotation(self, start: mathutils.Vector, end: mathutils.Vector) -> mathutils.Quaternion:
        direction = (self.position - self.handle_right).normalized()

        # Yaw (horizontal angle)
        yaw = -math.degrees(math.atan2(direction.y, direction.x))
        yaw = (yaw + 180) % 360
        if yaw > 180:
            yaw -= 360

        # Pitch (elevation)
        xy_len = math.sqrt(direction.x ** 2 + direction.y ** 2)
        pitch = math.degrees(math.atan2(direction.z, xy_len))

        # Roll = tilt (from curve tilt)
        roll = math.degrees(self.curve_roll)

        # Create Euler in Unreal order: Z = Yaw, X = Roll, Y = Pitch
        euler = mathutils.Euler((
            math.radians(roll),
            math.radians(pitch),
            math.radians(yaw)
        ), 'ZXY')

        return euler.to_quaternion()
    
    def get_out_val_rotation(self) -> mathutils.Quaternion:
        # The rotation seam controlled by the leave tangent in UE. (handle_right in Blender)
        return self.get_ue_rotation(self.position, self.handle_right)

    @staticmethod
    def scale_quaternion(q: mathutils.Quaternion, target_w: float = 0.5) -> mathutils.Quaternion:
        scale = target_w / q.w
        return mathutils.Quaternion((q.x * scale, q.y * scale, q.z * scale, q.w * scale))

    def get_out_left_handle_rotation(self) -> mathutils.Quaternion:
        quat = self.get_ue_rotation(self.position, self.handle_right)
        return self.scale_quaternion(quat, 0.2)

    def get_out_right_handle_rotation(self) -> mathutils.Quaternion:
        quat = self.get_ue_rotation(self.handle_left, self.position)
        return self.scale_quaternion(quat, 0.2)

    def get_human_readable_rotation(self, unreal_format: bool=False) -> str:
        ue_rotation = self.get_out_val_rotation()
        
        # Conversion à l'ordre Unreal: XYZ → Roll=X, Pitch=Y, Yaw=Z
        euler_rotation = ue_rotation.to_euler('XYZ')
        if unreal_format:
            euler_rotation.y = -euler_rotation.y  # Invert Y for Unreal format
        
        str_roll = "{:.2f}".format(math.degrees(euler_rotation.x))
        str_pitch = "{:.2f}".format(math.degrees(euler_rotation.y)) 
        str_yaw = "{:.2f}".format(math.degrees(euler_rotation.z))
        
        return f"Roll: {str_roll}, Pitch: {str_pitch}, Yaw: {str_yaw}"

    def get_ue_scale(self) -> mathutils.Vector:
        radius = self.curve_radius
        ue_scale = mathutils.Vector((radius, radius, radius))
        return ue_scale

    def get_ue_interp_curve_mode(self) -> str:
        if self.point_type in ["BEZIER"]:
            return "CIM_CurveUser"
        elif self.point_type in ["NURBS"]:
            return "CIM_CurveAuto"
        elif self.point_type in ["POLY"]:
            return "CIM_Linear" 
        return "CIM_CurveAuto"

    def get_spline_point_as_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        # Static data
        data["position"] = vector_as_ue(self.position)
        data["point_type"] = self.point_type
        return data



class BFU_SimpleSpline():

    def __init__(self, spline_data: bpy.types.Spline):
        # Context stats
        self.spline_type = spline_data.type
        self.closed_loop = spline_data.use_cyclic_u
        self.spline_length = spline_data.calc_length(resolution=512) #512 is the res used in UE5 to calculate length.
        self.spline_points: List[BFU_SimpleSplinePoint] = []

        # Blender Spline Data
        # ...

        # Formated data for Unreal Engine
        # ...

        # Formated data for ArchVis Tools in Unreal Engine
        # ...

    def get_simple_spline_values_as_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        # Static data
        data["spline_type"] = self.spline_type
        data["closed_loop"] = self.closed_loop
        points: List[Any] = []
        for spline_point in self.spline_points:
            points.append(spline_point.get_spline_point_as_dict())
        data["points"] = points

        return data
    

    def get_ue_format_spline(self) -> str:
        # handle right is leave Tangent in UE
        # handle left is arive Tangent in UE

        Position: Dict[str, Any] = {}
        Rotation: Dict[str, Any] = {}
        Scale: Dict[str, Any] = {}
        ReparamTable: Dict[str, Any] = {}
        Position["Points"] = []
        Rotation["Points"] = []
        Scale["Points"] = []
        ReparamTable["Points"] = []
        reparam_table_sample = 10

        spline_num = len(self.spline_points)
        spline_length = self.spline_length


        Position_Points: List[Any] = []
        Rotation_Points: List[Any] = []
        Scale_Points: List[Any] = []
        ReparamTable_Points: List[Any] = []

        for x, spline_point in enumerate(self.spline_points):
            spline_point: BFU_SimpleSplinePoint
            point_location = {}
            point_rotation = {}
            point_scale = {}

            point_location["InVal"] = "{:.6f}".format(x)
            point_location["OutVal"] = vector_as_ue(spline_point.get_ue_position())
            point_location["ArriveTangent"] = vector_as_ue(spline_point.get_ue_handle_left())
            point_location["LeaveTangent"] = vector_as_ue(spline_point.get_ue_handle_right())
            point_location["InterpMode"] = spline_point.get_ue_interp_curve_mode()

            point_rotation["InVal"] = float_as_ue(x)
            point_rotation["OutVal"] = quad_as_ue(spline_point.get_out_val_rotation())
            point_rotation["ArriveTangent"] = quad_as_ue(spline_point.get_out_left_handle_rotation())
            point_rotation["LeaveTangent"] = quad_as_ue(spline_point.get_out_right_handle_rotation())
            point_rotation["InterpMode"] = spline_point.get_ue_interp_curve_mode()

            point_scale["InVal"] = float_as_ue(x)
            point_scale["OutVal"] = vector_as_ue(spline_point.get_ue_scale())
            point_scale["ArriveTangent"] = vector_as_ue(mathutils.Vector((1, 1, 1)))
            point_scale["LeaveTangent"] = vector_as_ue(mathutils.Vector((1, 1, 1)))
            point_scale["InterpMode"] = spline_point.get_ue_interp_curve_mode()
           
            Position_Points.append(point_location)
            Position["bIsLooped"] = self.closed_loop
            Position["LoopKeyOffset"] = float_as_ue(1)
            Rotation_Points.append(point_rotation)
            Rotation["bIsLooped"] = self.closed_loop
            Rotation["LoopKeyOffset"] = float_as_ue(spline_num)
            Scale_Points.append(point_scale)
            Scale["bIsLooped"] = self.closed_loop
            Scale["LoopKeyOffset"] = float_as_ue(spline_num)

            for reparam_index in range(0, reparam_table_sample):
                reparam_table = {}
                spline_position_at_time = (reparam_index + reparam_table_sample*x + 1)/reparam_table_sample
                spline_length_at_time = spline_length*(reparam_index + reparam_table_sample*x + 1)/(reparam_table_sample*spline_num)
                InVal = spline_length_at_time
                OutVal = spline_position_at_time
                #print(float_as_ue(InVal), "->", float_as_ue(OutVal))
                reparam_table["InVal"] = float_as_ue(InVal)
                reparam_table["OutVal"] = float_as_ue(OutVal)
                ReparamTable_Points.append(reparam_table)

        Position["Points"] = Position_Points
        Rotation["Points"] = Rotation_Points
        Scale["Points"] = Scale_Points
        ReparamTable["Points"] = ReparamTable_Points

        data: Dict[str, Any] = {}
        data["SplineCurves"] = {}
        data["SplineCurves"]["Position"] = Position
        data["SplineCurves"]["Rotation"] = Rotation
        data["SplineCurves"]["Scale"] = Scale
        data["SplineCurves"]["ReparamTable"] = ReparamTable
        str_data = bfu_spline_utils.json_to_ue_format(data)
        return str_data
    

    def evaluate_spline_data(self, spline_obj: bpy.types.Object, spline_data: bpy.types.Spline, index: int = 0):
        
        if spline_data.type in ["POLY"]:
            for point in spline_data.points:
                point: bpy.types.SplinePoint
                self.spline_points.append(BFU_SimpleSplinePoint(spline_obj, point, spline_data.type))

        if spline_data.type in ["NURBS"]:
            
            # Duplicate and resample spline
            resampled_spline_obj: bpy.types.Object = bfu_spline_utils.create_resampled_spline(spline_data, spline_obj.bfu_spline_resample_resolution)
            new_spline_data = resampled_spline_obj.data.splines[0]
            for point in new_spline_data.bezier_points:
                point: bpy.types.BezierSplinePoint
                self.spline_points.append(BFU_SimpleSplinePoint(spline_obj, point, new_spline_data.type))

            # Clear
            objects_to_remove: List[bpy.types.Object] = [resampled_spline_obj]
            data_to_remove: List[bpy.types.ID] = [resampled_spline_obj.data]
            bpy.data.batch_remove(objects_to_remove)
            bpy.data.batch_remove(data_to_remove)
            
        elif spline_data.type in ["BEZIER"]:
            for bezier_point in spline_data.bezier_points:
                bezier_point: bpy.types.BezierSplinePoint
                self.spline_points.append(BFU_SimpleSplinePoint(spline_obj, bezier_point, spline_data.type))

        #print("Evaluate index " + str(index) + " finished in " + counter.get_str_time())
        #print("-----")
        return

class BFU_SplinesList():

    def __init__(self, spline: bpy.types.Object):
        # Context stats
        scene = bpy.context.scene

        self.spline_name = spline.name
        self.desired_spline_type = spline.bfu_desired_spline_type
        self.ue_spline_component_class = bfu_spline_unreal_utils.get_spline_unreal_component(spline)
        self.simple_splines: Dict[int, BFU_SimpleSpline] = {}

    def get_spline_list_values_as_dict(self) -> Dict[str, Any]:
        data = {}
        # Static data
        data["spline_name"] = self.spline_name
        data["desired_spline_type"] = self.desired_spline_type
        data["ue_spline_component_class"] = self.ue_spline_component_class

        data["simple_splines"] = {}
        for x, simple_spline_key in enumerate(self.simple_splines):
            simple_spline: BFU_SimpleSpline = self.simple_splines[simple_spline_key]
            data["simple_splines"][x] = simple_spline.get_simple_spline_values_as_dict()

        return data

    def get_ue_format_spline_list(self) -> List[str]:
        data: List[str] = []
        for simple_spline_key in self.simple_splines:
            simple_spline: BFU_SimpleSpline = self.simple_splines[simple_spline_key]
            data.append(simple_spline.get_ue_format_spline())
        return data
    

    def evaluate_spline_obj_data(self, spline_obj: bpy.types.Object):
        
        for x, spline_data in enumerate(spline_obj.data.splines):
            simple_spline = self.simple_splines[x] = BFU_SimpleSpline(spline_data)
            simple_spline.evaluate_spline_data(spline_obj, spline_data, x)

        #print("Evaluate " + spline_obj.name + " finished in " + counter.get_str_time())
        #print("-----")
        return

 
class BFU_MultiSplineTracks():

    def __init__(self):
        self.splines_to_evaluate: List[bpy.types.Object] = []
        self.evaluate_splines: Dict[str, BFU_SplinesList] = {}

    def add_spline_to_evaluate(self, obj: bpy.types.Object):
        self.splines_to_evaluate.append(obj)


    def evaluate_all_splines(self, preview: bool = False):
        # Evaluate all splines at same time will avoid frame switch

        scene = bpy.context.scene
        if scene is None:
            return

        # Save scene data
        save_current_frame = scene.frame_current
        if not preview:
            save_use_simplify = bpy.context.scene.render.use_simplify
            bpy.context.scene.render.use_simplify = True

        for spline in self.splines_to_evaluate:
            self.evaluate_splines[spline.name] = BFU_SplinesList(spline)

        print(f"Start evaluate {str(len(self.splines_to_evaluate))} spline(s).")
        for spline in self.splines_to_evaluate:
            evaluate = self.evaluate_splines[spline.name]
            evaluate.evaluate_spline_obj_data(spline)

        if not preview:
            scene.frame_current = save_current_frame
            bpy.context.scene.render.use_simplify = save_use_simplify

    def get_evaluate_spline_data(self, obj: bpy.types.Object):
        return self.evaluate_splines[obj.name]
    
    def get_evaluate_spline_data_as_dict(self, obj: bpy.types.Object) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        data.update(self.evaluate_splines[obj.name].get_spline_list_values_as_dict())
        data.update(self.evaluate_splines[obj.name].get_spline_list_values_as_dict())
        return data