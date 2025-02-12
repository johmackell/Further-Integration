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

C7_CHORD = lambda x: np.sin(262*x) + np.sin(330*x) + np.sin(392*x) + np.sin(494*x)

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

        self.play(Unwrite(title))


        ax=Axes(x_range=[0,5,0.5], y_range=[-2,2,0.5],
                x_axis_config={"numbers_to_include": np.arange(0,5,1)}, 
                y_axis_config={"numbers_to_include": [1]})
        #ax_labels=ax.get_axis_labels(x_label="Time (t)", y_label=Tex(r"y=sin(x)"))
        ax_labels=ax.get_axis_labels(x_label="t", y_label="f(t)")


        e = ValueTracker(0.02)


        sin_graph = always_redraw(
            lambda: FunctionGraph(

                # Sin wave goes here
                lambda x: np.sin(2*x) + np.sin(5*x),

                color=DARK_BLUE,
                x_range = (0, e.get_value()),
            )
        )


        ax_group = VGroup(ax, ax_labels)
        #labels=VGroup(sin_label, cos_label)
        
        

        self.play(Create(ax_group), run_time=3)
        self.wait()
        #self.play(Create(sin_graph), run_time=2)
        self.add(sin_graph)
        self.play(e.animate.set_value(PI), run_time=5, rate_func=linear)
        self.play(sin_graph.animate.shift(RIGHT), run_time=2)
        self.wait()

        sin_label = ax.get_graph_label(sin_graph, label="\\sin(2x) + \\sin(5x)", x_val=3, direction=UP*4, dot=True)
        self.play(Write(sin_label))

class SineWave(Scene):
    def construct(self):
        self.show_graphs()
    
    def show_graphs(self):
        y = ValueTracker(4)

        axes = always_redraw(
            lambda: Axes(
                x_range=(0, 40, 1), y_range=(-y.get_value(), y.get_value(), 1),
                                    y_length=2,
                x_axis_config = {
                    "numbers_to_include": np.arange(0, 10.01, 2),
                    "numbers_with_elongated_ticks": np.arange(0, 10.01, 2)
                },
                y_axis_config = {
                    "numbers_to_include": np.arange(-4, 4.01, 2)
                },
                tips=False
            )
        )
        axes_labels = axes.get_axis_labels(x_label="t", y_label="f(t)")

        signal = axes.plot(C7_CHORD, color=BLUE)
        signal_label = axes.get_graph_label(signal, "f(t)", x_val=0, direction=UP / 2)

        t = ValueTracker(0.01)
        vert_line = always_redraw(
            lambda: axes.get_vertical_line(axes.c2p(t.get_value(), 3), color=YELLOW, line_func=Line)
        )

        line_label = axes.get_graph_label(signal, r"x=2\pi", x_val=TAU, direction=UR*5, color=WHITE)
        


        labels = VGroup(axes_labels, signal_label, line_label)
        plot = VGroup(axes, signal, labels)


        self.play(Create(axes), run_time=2)
        self.play(Create(signal), run_time=6)
        self.play(Create(labels), run_time=3)

        self.add(vert_line)
        self.play(t.animate.set_value(10), run_time=2, rate_func=linear)

        self.play(plot.animate.shift(UP*3))
        self.play(signal.animate.stretch_to_fit_height(4))
        self.play(y.animate.set_value(8))

        area = axes.get_area(signal, color=(GOLD_D, GOLD_A))
        self.play(FadeIn(area), run_time=2)

        self.wait(2)



class DecomposingSound(Scene):
    def construct(self):
        self.initialise_objects()
        self.play_scene()
    
    def initialise_objects(self):
        big_axes = Axes(
            x_range=(0, 6, 1), y_range=(-4, 4, 2),
                                y_length=4,
            tips=False
        )
        big_text = Text("Cmaj7", font_size=42, color=YELLOW)
        big_text.move_to(DOWN*3)
        small_axes = Axes(
            x_range=(0, 6, 1), y_range=(-4, 4, 2),
            x_length=10, y_length=1.5,
            tips=False
        )
        small_text = Text("Cmaj7", font_size=24, color=YELLOW)
        small_text.next_to(small_axes, RIGHT*5)

        big_signal = big_axes.plot(C7_CHORD, color=BLUE)
        small_signal = small_axes.plot(C7_CHORD, color=BLUE)

        self.big_vert_line = Line(start=np.array([-6., -2., 0.]), end=np.array([-6., 2., 0.]), color=GOLD)
        self.small_vert_line = Line(start=np.array([-6., -0.5, 0.]), end=np.array([-6., 0.5, 0.]), color=GOLD)



        # ----- -----
        # Vgroup objects are generally formatted as follows:
        #       [Axes, ParametricFunction, Text]
        #
        self.big_plot = VGroup(big_axes, big_signal, big_text)
        self.small_plot = VGroup(small_axes, small_signal, small_text)
        self.small_plot.shift(LEFT)

        self.notes = [
            ('C4', 262, YELLOW),
            ('E4', 330, GREEN),
            ('G4', 392, RED),
            ('B5', 494, GOLD)
        ]
        offset = 1.5
        for i in range(len(self.notes)):
            t = self.notes[i]

            ax = Axes(
                x_range=(0, 6, 1), y_range=(-4, 4, 2),
                x_length=10, y_length=1,
                tips=False
            )
            ax.shift(LEFT)
            tx = Text(f"{t[0]} - {t[1]} Hz", color=t[2], font_size=24)
            tx.next_to(ax, RIGHT*4)
            sg = ax.plot(lambda x: np.sin(t[1]*x), color=t[2])
            ln = Line(start=np.array([-6., -0.5, 0.]), end=np.array([-6., 0.5, 0.]), color=GOLD)
            vg = VGroup(ax, sg, tx, ln)
            vg.shift(UP*(3-offset))

            self.notes[i] = vg
            offset += 1.5
    
    def play_scene(self):
        self.wait()
        
        self.play(Create(self.big_plot[0]), run_time=2)
        self.play(Create(self.big_plot[1]), run_time=6)
        self.play(FadeIn(self.big_plot[2]), run_time=0.5)
        self.play(self.big_vert_line.animate.shift(RIGHT*12), run_time=3, rate_func=linear)
        self.wait(2)
        self.play(FadeOut(self.big_vert_line))
        self.play(ReplacementTransform(self.big_plot, self.small_plot, run_time=2))
        self.play(self.small_plot.animate.shift(UP*3.2))



        self.play(Create(self.notes[0][0]), Create(self.notes[1][0]), Create(self.notes[2][0]), Create(self.notes[3][0]), run_time=2)

        self.play(Transform(self.small_plot[1].copy(), self.notes[0][1]))
        self.play(FadeIn(self.notes[0][2]))
        self.play(self.notes[0][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[0][3]))

        self.play(Transform(self.small_plot[1].copy(), self.notes[1][1]))
        self.play(FadeIn(self.notes[1][2]))
        self.play(self.notes[1][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[1][3]))

        self.play(Transform(self.small_plot[1].copy(), self.notes[2][1]))
        self.play(FadeIn(self.notes[2][2]))
        self.play(self.notes[2][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[2][3]))

        self.play(Transform(self.small_plot[1].copy(), self.notes[3][1]))
        self.play(FadeIn(self.notes[3][2]))
        self.play(self.notes[3][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[3][3]))
        

        self.wait(2)