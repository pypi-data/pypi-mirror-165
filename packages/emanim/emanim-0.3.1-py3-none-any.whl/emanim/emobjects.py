from manim import *

class RoundedTriangle(Triangle):
    def __init__(self, corner_radius=0.18, **kwargs):
        super().__init__(**kwargs)
        self.corner_radius = corner_radius

class Preview(VGroup):
    def __init__(self, num, type, name, logo, colors, stroke=False, **kwargs):
        super().__init__(**kwargs)
        num = str(num)
        types = {
            "exp" : "Выпуск $e^{" + num + "}$",
            "spec" : "Спецвыпуск",
            "compx" : "Выпуск $" + num + "i$",
            "expcompx" : "Выпуск $e^{" + num + "i}$"
        }

        if len(name) <= 13:
            scale_factor = 4
        else:
            scale_factor = 3
            name = name.replace(" ", r"\\")

        title = Tex(types[type], color=colors[0]).scale(4)
        subtitle = Tex(name, color=colors[1]).scale(scale_factor).next_to(title, DOWN)
        self.add(title, subtitle)
        self.move_to(ORIGIN)
        logo.to_edge(UL)
        self.add(logo)
        if stroke:
            rect = RoundedRectangle(corner_radius=1, height=8, width=14)
            self.add(rect)
