import omni.usd
import omni.ext
import omni.ui as ui
from omni.ui import color as cl
from pxr import Sdf, UsdGeom
import random

WINDOW_STYLE = {"Window": {"background_color": cl.white}}

# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[ash.winter.lights] some_public_function was called with x: ", x)
    return x ** x


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class AshWinterLightsExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[ash.winter.lights] ash winter lights startup")
        self._points = None
        self.instancer = None
        self._window = ui.Window("Holiday Lights", width=300, height=300)
        frame_style ={"ScrollingFrame": {"background_color": cl("#097eff90"), "border_color": cl.white}}
        with self._window.frame:
            with ui.ScrollingFrame(style=frame_style):
                with ui.VStack(spacing=0):
                    button_style = {"Button":{"background_color": cl("#097eff"),
                                                    "border_color": cl.white,
                                                    "border_width": 2.0,
                                                    "padding": 10,
                                                    "margin_height": 40,
                                                    "border_radius": 10,
                                                    "margin_width":15},
                                                    "Button.Label":{"color": cl.white},
                                                    "Button:hovered":{"background_color": cl("#E5F1FB")}}
                    ui.Button("DECORATE", clicked_fn=self.get_points, style=button_style)
                    # ui.Button("Place Lights", clicked_fn=self.place_lights)
    
    def get_points(self):
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

    def on_shutdown(self):
        self._window.destroy()
        self._window = None
