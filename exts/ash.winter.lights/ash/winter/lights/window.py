import omni.usd
import omni.ui as ui
from omni.ui import color as cl
from .mesh_generator import MeshGenerator
import math


class WinterLightsWindow(ui.Window):

    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(title, **kwargs)
        self.generator: MeshGenerator = None

        self.frame.set_build_fn(self._build_fn)
        
    def _build_window(self):
        with self.frame:
            with ui.VStack():
                curve_label = None
                points_label = None


            def get_selection():
                #Get curve selected from stage
                #if self.generator is None:
                self.generator = MeshGenerator()
                if self.generator.get_selection():
                    curve_label.text = self.generator.selected_prim_path
                else:
                    curve_label.text = "No Selection"

                #Get points along curve selected
                if self.generator is not None:
                    if self.generator.get_points_along_curve():
                        points_label.text = "Points Stored"
                    else:
                        points_label.text = "Could not store points"

            def generate_lights():
                if self.generator is not None:
                    self.generator.generate_lights()


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
                    ui.Button("Grab Curve", style=button_style, clicked_fn=get_selection)
                    curve_label = ui.Label("No Selection")
                    with ui.ZStack():
                        points_label = ui.Label("No Points Stored")

                with ui.HStack():
                    ui.Button("Generate Winter Lights", style=button_style, clicked_fn=generate_lights)
                    

    def _build_fn(self):
        with ui.ScrollingFrame():
            with ui.VStack(height=10):
                self._build_window()
                

    def destroy(self):
        super().destroy()
