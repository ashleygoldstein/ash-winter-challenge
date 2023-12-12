from pxr import Gf, Sdf, UsdGeom
import omni.kit.commands
import omni.usd
from .utils import *
import math


class MeshGenerator():
    def __init__(self)-> None:
        self.instancer_path = ""
        self.points = []
        self.instancer = None
        self.curve = None
        self.selected_prim_path = ""
        
    def get_selection(self):
        context = get_current_context()
        selection = context.get_selection()
        self.selected_prim_path = selection.get_selected_prim_paths()[0]
        #return True

    def get_points_along_curve(self):
        stage = get_current_stage()
        prim = stage.GetPrimAtPath(str(self.selected_prim_path))
        type_name = prim.GetTypeName()
        self.curve = prim
        
        self.points = self.curve.GetAttribute("points").Get()
        return True

        

    def create_instancer(self):
        stage = get_current_stage()
        if self.instancer is None:
            self.instancer_path = Sdf.Path(omni.usd.get_stage_next_free_path(stage, "/World/CurveInstancer", False))
            self.instancer = UsdGeom.PointInstancer.Define(stage, self.instancer_path)

    def create_prototype(self):
        stage = get_current_stage()
        lights_path = "/World/holiday_light_red"
        if not stage.GetPrimAtPath(lights_path).IsValid():
                omni.kit.commands.execute('CreatePayloadCommand',
                    usd_context=get_current_context(),
                    path_to=Sdf.Path(lights_path),
                    asset_path='C:/Users/agoldstein/OneDrive - NVIDIA Corporation/Documents/Assets_USD//holiday_light_red.usd',
                    instanceable=True)
                omni.kit.commands.execute('TransformMultiPrimsSRTCpp',
                    count=1,
                    paths=[lights_path],
                    new_translations=[0.0, 0.0, 0.0],
                    new_rotation_eulers=[0.0, 0.0, 0.0],
                    new_rotation_orders=[0, 1, 2],
                    new_scales=[0.2, 0.2, 0.2])
                

        self.instancer.CreatePrototypesRel().SetTargets([lights_path])
    


    def create_positions(self):
        if len(self.points) > 0:
            world_pos_attr = self.curve.GetAttribute('xformOp:translate')
            world_pos = world_pos_attr.Get()
            ids = [0] * (len(self.points) - 1)
            new_points = []
            i = 0
            while i < len(self.points):
                new_x = self.points[i][0] + world_pos[0]
                new_y = self.points[i][1] + world_pos[1]
                new_z = self.points[i][2] + world_pos[2]
                new_points.append((new_x, new_y, new_z))
                i += 1
            print(new_points)
            self.instancer.CreatePositionsAttr().Set(new_points)
            self.instancer.CreateProtoIndicesAttr().Set(ids)


    def generate_lights(self):
        self.create_instancer()
        self.create_prototype()
        self.create_positions()        
                

        