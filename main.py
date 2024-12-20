from manim import *
import numpy as np

# Develop the graph and integration area under the curve
class Integral(Scene):
    CONFIG = {
        "y_max": 8,
        "y_axis_height": 5
    }

    # Define construction
    def construct(self):
        self.show_function_graph()
    
    # Define functions
    def show_function_graph(self):
        equation = MathTex(r"\hat{f} (\xi)=\int_{-\infty}^{\infty}f(x)e^{-2\pi ix\xi}dx")
        equation.set_color_by_tex("x", YELLOW)

        blue_circle = Circle(color=BLUE, fill_opacity=0.5)

        self.add(equation)
        self.wait(duration=3)
        self.play(ReplacementTransform(equation, blue_circle, run_time=3))
        small_dot = Dot()
        small_dot.add_updater(lambda mob: mob.next_to(blue_circle, DOWN))
        self.play(Create(small_dot))
        self.play(blue_circle.animate.shift(RIGHT))
        self.wait()
        self.play(FadeOut(blue_circle, small_dot))

