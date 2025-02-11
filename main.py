# How to render animation:
#
#   manim -pql main.py Integral
#
#   manim [options] FILE [class_name (to render)]
#         -p, --preview
#         -q, --quality [l|m|h|p|k] (use 'h' for final render, otherwise 'l')
#
#



from manim import *

FOURIER_TRANSFORM = r"F(\nu)=\int_{-\infty}^{\infty}f(t)e^{-2\pi it\nu} dt"
INVERSE_FOURIER   = r"f(t)=\int_{-\infty}^{\infty}F(\nu)e^{2\pi it\nu} d\nu"

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
        title = Text("Exploring the Fourier Transform")
        title.to_edge(UP)
        #equation = MathTex(r"\hat{f} (\xi)=\int_{-\infty}^{\infty}f(x)e^{-2\pi ix\xi}dx")
        fourier = MathTex(FOURIER_TRANSFORM)
        fourier.set_color_by_tex("f", YELLOW)
        inverse = MathTex(INVERSE_FOURIER)
        inverse.set_color_by_tex("f", GREEN)

        self.play(Write(title))
        self.play(Write(fourier, run_time=3))
        self.play(ReplacementTransform(fourier, inverse, run_time=3))
        small_dot = Dot()
        small_dot.add_updater(lambda mob: mob.next_to(inverse, DOWN))
        self.play(Create(small_dot))
        self.play(inverse.animate.shift(RIGHT))
        self.wait()
        self.play(FadeOut(inverse, small_dot))


        ax=Axes(x_range=[-5,5,0.5], y_range=[-3,3,0.5], 
                x_axis_config={"numbers_to_include": np.arange(-5,5,1)}, 
                y_axis_config={"numbers_to_include": [1]})
        #ax_labels=ax.get_axis_labels(x_label="Time (t)", y_label=Tex(r"y=sin(x)"))
        ax_labels=ax.get_axis_labels()


        e = ValueTracker(0.04)


        sin_graph = always_redraw(
            lambda: FunctionGraph(

                # Sin wave goes here
                lambda x: np.sin(2*x) + np.sin(5*x),

                color=DARK_BLUE,
                x_range = (-10, e.get_value()),
            )
        )

        
        sin_label=ax.get_graph_label(sin_graph, label="\\sin(x)", 
                                     x_val=-4.5, direction=UP*4)

        ax_group = VGroup(ax, ax_labels)
        #labels=VGroup(sin_label, cos_label)
        
        self.play(Create(ax_group), Write(sin_label), run_time=3)
        self.wait()
        #self.play(Create(sin_graph), run_time=2)
        self.add(sin_graph)
        self.play(e.animate.set_value(PI), run_time=5, rate_func=linear)
        self.play(sin_graph.animate.shift(RIGHT), run_time=2)
        self.wait()

