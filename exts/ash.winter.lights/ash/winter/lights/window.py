import omni.usd
import omni.ui as ui
import omni.ext
from omni.ui import color as cl
from pxr import Sdf, UsdGeom
import random


class WinterLightsWindow(ui.Window):

    def __init__(self, title, width, height):
        super().__init__(title, width=width, height=height)
        self._build_fn = self._build
        #self.frame.set_build_fn(self._build_fn)
        

        with self.frame:
            with ui.ScrollingFrame():
                with ui.VStack(height=10):
                    self._points = None
                    self.instancer = None
                    
                def get_points():
                    ctx = omni.usd.get_context()
                    stage = ctx.get_stage()
                    selection = ctx.get_selection()
                    if selection and len(selection.get_selected_prim_paths()) > 0:
                        prim_path = selection.get_selected_prim_paths()[0]
                        prim = stage.GetPrimAtPath(prim_path)
                        self._points = prim.GetAttribute("points").Get()
                        self.create_instancer(prim_path)
            
                def create_instancer(self, prim_path):
                    stage = omni.usd.get_context().get_stage()
                    instancer_path = Sdf.Path(omni.usd.get_stage_next_free_path(stage, prim_path + "/LightInstancer", False))
                    self.instancer = UsdGeom.PointInstancer.Define(stage, instancer_path)
                    self.instancer.CreatePrototypesRel().SetTargets(["/World/Lights/holiday_light_red", "/World/Lights/holiday_light_green", "/World/Lights/holiday_light_blue"])
                    self.place_lights()
                
                def place_lights(self):
                    if len(self._points) > 0:
                        new_points = [self._points[i] for i in range(0, len(self._points)) if i % 21 == 0]
                        print(len(self._points))
                        print(len(new_points))
                        ids = []
                        for i in new_points:
                            ids.append(random.randint(0,1000)%3)
                        self.instancer.CreatePositionsAttr().Set(new_points)
                        self.instancer.CreateProtoIndicesAttr().Set(ids)


                with ui.VStack():
                    with ui.HStack():
                        button_style = {"Button":{"background_color": cl.cyan,
                                                "border_color": cl.white,
                                                "border_width": 2.0,
                                                "padding": 10,
                                                "margin_height": 40,
                                                "border_radius": 10,
                                                "margin_width":15},
                                                "Button.Label":{"color": cl.black},
                                                "Button:hovered":{"background_color": cl("#E5F1FB")}}
                        ui.Button("Grab Points", style=button_style, clicked_fn=get_points)

                    with ui.HStack():
                        pass
                        #ui.Button("Generate Winter Lights", style=button_style, clicked_fn=place_lights)
                        
                    

    def destroy(self):
        super().destroy()
