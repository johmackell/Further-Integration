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

FOURIER_TRANSFORM = r"F(\omega)=\int_{-\infty}^{\infty}f(t)e^{-i\omega t} \ dt"
INVERSE_FOURIER   = r"f(t)=\int_{-\infty}^{\infty}F(\nu)e^{i\omega t} d\omega"

EULERS_FORMULA = r"e^{i\theta }=\cos{\theta }+i\sin{\theta }"

C7_CHORD = lambda x: np.sin(262*x) + np.sin(330*x) + np.sin(392*x) + np.sin(494*x)
FSM7_CHORD = lambda x: np.sin(370*x) + np.sin(466*x) + np.sin(554*x) + np.sin(698*x)
C_NOISE = lambda x: np.sin(262*x) + np.sin(330*x) + np.sin(392*x) + np.sin(1100*x)

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

class Sinewave(Scene):
    def construct(self):
        self.play_scene()
    
    def play_scene(self):
        Title = MathTex(r"V(t) = Acos(\omega t + \phi)")
        self.play(Write(Title))
        self.play(Title.animate.shift(UP*3))


        # Create the axes
        axes = Axes(x_range=[0, 15, 1.57], y_range=[-2, 2])
        axis_labels = axes.get_axis_labels(x_label = "t", y_label = "V")

        # This is the value you use for the shift.
        # On the last line, I use .animate to animate the change in value.
        # Changing the 'shift' value invokes a change in 'always_redraw'
        shift = ValueTracker(0)
        yline = always_redraw(
            lambda: axes.get_line_from_axis_to_point(
                0, # 0 indicates that the line comes FROM the x-axis
                axes.c2p(PI-shift.get_value(), -1),
                color=RED
            )
        )
        xline = always_redraw(
            lambda: axes.get_line_from_axis_to_point(
                1, # 1 indicates that the line come FROM the y-axis
                axes.c2p(PI-shift.get_value(), -1),
                line_func=Arrow,
                line_config={'buff': 0}
            )
        )
        
        xline_label = Variable(shift.get_value(), r"\phi", color=YELLOW).next_to(xline, DOWN)

        self.play(DrawBorderThenFill(axes))
        self.play(DrawBorderThenFill(axis_labels))

        # Create the waves
        # always_redraw makes it so that it replots the line *every* frame. This is the correct way to animate a curve plotted on the axes.
        graph = always_redraw(
            lambda: axes.plot(lambda x: np.cos(x+shift.get_value()), color=RED)
        )
        self.play(Create(graph), run_time = 4)
        self.wait(4)

        graph2 = axes.plot(lambda x: 0.5*np.cos(x), color=BLUE)

        self.add(graph2)
        self.wait()

        self.play(Create(yline), Create(xline), Write(xline_label))
        self.wait()
        self.play(shift.animate.set_value(-PI), xline_label.tracker.animate.set_value(-PI))

        self.wait(5)


### Done in high quality
class HistoryOfIntegration(Scene):
    def construct(self):
        self.wait(3)
        self.my_scene()
        self.wait(3)
    
    def my_scene(self):
        arc = ImageMobject("src/archimedes.png").scale(0.5).shift(LEFT*4.5)
        self.play(FadeIn(arc, shift=LEFT*3), run_time=2)
        self.wait()

        self.pol_v = ValueTracker(8)
        pol5 = RegularPolygon(5, color=BLUE).scale(2)
        pol5s = pol5.copy().set_fill(BLUE_C, 0.8).scale(0.8).shift(DOWN*0.05)
        pol5t = Text("n = 5").next_to(pol5, DOWN)

        pol6 = RegularPolygon(6, color=GREEN)
        pol6s = pol6.copy().set_fill(GREEN_C, 0.8)
        pol6s.scale(0.8)
        pol6t = Text("n = 6").next_to(pol6, DOWN)

        poln = always_redraw(lambda:
            RegularPolygon(int(self.pol_v.get_value()), color=RED).shift(RIGHT*3)
        )
        polns = always_redraw(lambda:
            RegularPolygon(int(self.pol_v.get_value()), color=RED).shift(RIGHT*3).scale(0.8).set_fill(RED_C, 0.8)
        )
        polnt = always_redraw(
            lambda: Text(f"n = {int(self.pol_v.get_value())}").next_to(poln, DOWN)
        )


        cir5 = Circle(color=WHITE).scale(1.6).shift(DOWN*0.1)
        cir6 = Circle(color=WHITE).scale(0.8)
        cirn = Circle(color=WHITE).shift(RIGHT*3).scale(0.8)

        self.pol_vg = VGroup(pol6, poln, pol6s, polns, cir6, cirn, pol6t, polnt)

        self.play(FadeIn(cir5))
        self.wait(3)
        self.play(FadeIn(pol5), FadeIn(pol5t))
        self.wait(3)
        self.play(FadeIn(pol5s))
        self.wait(10)
        self.play(FadeOut(arc, shift=LEFT*2), cir5.animate.shift(LEFT*3).scale(0.5).shift(UP*0.1), pol5.animate.shift(LEFT*3).scale(0.5), pol5s.animate.shift(LEFT*3).scale(0.5), pol5t.animate.shift(LEFT*3).shift(UP*0.8), rate_func=linear)

        self.play(FadeIn(self.pol_vg))

        self.play(self.pol_v.animate.set_value(20), run_time=5, rate_func=linear)

        self.wait(5)
        self.play(FadeOut(self.pol_vg, pol5, pol5s, pol5t, cir5))

        self.wait(3)

        ee = MathTex(r"f(t)&=2x+5 \\", r"f'(t)&=2", color=YELLOW)
        self.play(FadeIn(ee[0]))
        self.wait()
        self.play(FadeIn(ee[1], shift=UP))
        
        self.wait(5)
        self.play(FadeOut(ee))

        eq = MathTex(r"y=x^{2}", color=YELLOW).shift(LEFT*3)
        eqd = MathTex(r"\frac{dy}{dx}=2x", color=RED).shift(RIGHT*3)
        _sax = NumberPlane(
            (0, 2.5, 0.5), (0, 5, 1),
            5, 4,
            background_line_style={
                "stroke_opacity": 0.3
            }
        ).shift(DOWN).shift(LEFT*3)
        sylabel = _sax.get_y_axis_label(
            Tex("Displacement").rotate(90*DEGREES),
            edge=LEFT,
            direction=LEFT,

        )
        sxlabel = _sax.get_x_axis_label(
            Tex("Time"),
            edge=DOWN,
            direction=DOWN
        )
        _vax = NumberPlane(
            (0, 2.5, 0.5), (0, 5, 1),
            5, 4,
            background_line_style={
                "stroke_opacity": 0.3
            }
        ).shift(DOWN).shift(RIGHT*3)
        vylabel = _vax.get_y_axis_label(
            Tex("Velocity").rotate(90*DEGREES),
            edge=LEFT,
            direction=LEFT,

        )
        vxlabel = _vax.get_x_axis_label(
            Tex("Time"),
            edge=DOWN,
            direction=DOWN
        )
        
        ax_eq = _sax.plot(lambda x: x**2, x_range=(0, 2.5), color=YELLOW)
        ax_eqd = _vax.plot(lambda x: 2*x, x_range=(0, 2.5), color=RED)
        sax = VGroup(_sax, sylabel, sxlabel)
        vax = VGroup(_vax, vylabel, vxlabel)
        self.play(Write(eq), Write(eqd))
        self.wait(5)
        self.play(eq.animate.shift(UP*3), eqd.animate.shift(UP*3))
        self.play(Create(sax), Create(vax), rate_func=linear, run_time=2)
        self.play(Create(ax_eq), Create(ax_eqd))

        self.wait(5)
        self.play(FadeOut(sax, vax, ax_eq, ax_eqd, eq, eqd))

        eq = MathTex(r"v&=5t \\", r"s&=?", color=YELLOW)
        self.play(Write(eq[0]))
        self.wait()
        self.play(FadeIn(eq[1], shift=UP*2), run_time=2)

        self.wait(5)
        self.play(FadeOut(eq))

        _vax = NumberPlane(
            (0, 6, 0.5), (0, 3, 0.5),
            8, 4,
            background_line_style={
                "stroke_opacity": 0.3
            }
        ).shift(DOWN)
        vylabel = _vax.get_y_axis_label(
            Tex("Velocity").rotate(90*DEGREES),
            #edge=LEFT,
            direction=LEFT,

        )
        vxlabel = _vax.get_x_axis_label(
            Tex("Time"),
            #edge=DOWN,
            direction=DOWN
        )

        ax_eqd = _vax.plot(lambda x: np.sin(x)+1.5, x_range=(0, 6), color=RED)
        vax = VGroup(_vax, vylabel, vxlabel)
        self.play(Create(vax), rate_func=linear, run_time=2)
        self.play(Create(ax_eqd))
        self.wait(10)

        a = _vax.get_area(ax_eqd, (0, 6), color=YELLOW_B)
        #self.play(Write(a))
        r = _vax.get_riemann_rectangles(
            ax_eqd,
            x_range=(0, 6),
            dx=0.4,
            fill_opacity=0.6
        )
        self.play(Write(r))
        v = Tex(r"\textbf{v} \ \ \ ", r"\{").set_color_by_tex("v", RED).shift(LEFT*2.5).shift(DOWN*1.4)
        t = MathTex(r"\underbrace{} \\", r"\Delta t").set_color_by_tex("t", RED).shift(DOWN*3.4).shift(LEFT*1.1)
        self.play(Write(v), v[1].animate.scale(6.8))
        self.wait(2)
        self.play(Write(t), t[0].animate.scale(0.6))

        aeqq = MathTex(r"Area\approx\sum", r" \ ", r" \ ", color=YELLOW).shift(UP).shift(RIGHT)
        self.wait(2)
        self.play(Write(aeqq))
        self.play(FadeOut(v[1]), v[0].animate.move_to(aeqq[1]).shift(RIGHT*2.5).shift(UP), run_time=0.5)
        self.play(FadeOut(t[0]), t[1].animate.move_to(aeqq[2]).shift(RIGHT*3).shift(UP), run_time=0.5)

        self.wait(5)
        rn = _vax.get_riemann_rectangles(
            ax_eqd,
            x_range=(0, 6),
            dx=0.2,
            fill_opacity=0.6
        )
        self.play(ReplacementTransform(r, rn), run_time=2)
        self.wait(3)

        ri = _vax.get_riemann_rectangles(
            ax_eqd,
            x_range=(0, 6),
            dx=0.05,
            fill_opacity=0.6
        )
        self.play(ReplacementTransform(rn, ri), run_time=2)

        a = _vax.get_area(ax_eqd, (1, 5), opacity=0.8)
        self.wait(3)
        aa = _vax.get_area(ax_eqd, opacity=0.8)
        #self.play(ReplacementTransform(ri, a), FadeOut(t[0], scale=0.1))

        aeq = MathTex(r"Area&=\lim_{\Delta t\to 0} (\sum v \ \Delta t", r") \\ &=\int v \ dt", color=YELLOW).shift(RIGHT).shift(UP*2.5)
        self.play(Write(aeq), FadeOut(aeqq, v[0], t[1], ri))
        self.play(Write(aa))

        self.wait(3)
        self.play(FadeOut(aeq, aa))

        i = MathTex(r"\int f(x) \ dx", color=YELLOW).shift(LEFT*3).shift(UP*2.5)
        iab = MathTex(r"\int_{a}^{b} f(x) \ dx", color=YELLOW).shift(RIGHT*3).shift(UP*2.5)
        at = Tex("a", color=YELLOW).move_to(_vax.c2p(1, 0)).shift(DOWN*0.3)
        bt = Tex("b", color=YELLOW).move_to(_vax.c2p(5, 0)).shift(DOWN*0.3)
        self.wait(10)
        self.play(Write(i), run_time=2)
        self.wait(10)
        self.play(Write(iab), Write(a), FadeIn(at, bt), run_time=2)

        self.wait(5)
        ft = ImageMobject("src/fund_theo.png")
        self.play(FadeIn(ft))

        self.wait(30)
        self.play(FadeOut(ft, vax, i, iab, at, bt, ax_eqd, a))
        


### Done in high quality
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
        big_signal = big_axes.plot(C7_CHORD, color=BLUE)

        small_axes = Axes(
            x_range=(0, 6, 1), y_range=(-4, 4, 2),
            x_length=10, y_length=1.5,
            tips=False
        )
        small_text = Text("Cmaj7", font_size=24, color=YELLOW)
        small_text.next_to(small_axes, RIGHT*5)
        small_signal = small_axes.plot(C7_CHORD, color=BLUE)

        self.big_vert_line = Line(start=np.array([-6., -2., 0.]), end=np.array([-6., 2., 0.]), color=GOLD)
        self.small_vert_line = Line(start=np.array([-6., -0.5, 0.]), end=np.array([-6., 0.5, 0.]), color=GOLD)

        ax1_t = Text("f(t)", font_size=42, color=YELLOW)
        ax1_t.move_to(DOWN*3)
        self.ax1 = VGroup(
            Axes(x_range=(0, 6, 1), y_range=(-4, 4, 2), y_length=4, tips=False),
            big_axes.plot(FSM7_CHORD, color=GREEN),
            ax1_t,
            Line(start=np.array([-6., -2., 0.]), end=np.array([-6., 2., 0.]), color=GOLD)
        )

        ax2_t = Text("f(t)", font_size=42, color=MAROON)
        ax2_t.move_to(DOWN*3)
        self.ax2 = VGroup(
            Axes(x_range=(0, 6, 1), y_range=(-4, 4, 2), y_length=4, tips=False),
            big_axes.plot(C_NOISE, color=MAROON),
            ax2_t,
            Line(start=np.array([-6., -2., 0.]), end=np.array([-6., 2., 0.]), color=GOLD)
        )



        # ----- -----
        # Vgroup objects are generally formatted as follows:
        #       [Axes, ParametricFunction, Text, Line]
        #
        self.big_plot = VGroup(big_axes, big_signal, big_text)
        self.small_plot = VGroup(small_axes, small_signal, small_text)
        self.small_plot.shift(LEFT)

        self.notes = [
            ('C4', 262, YELLOW),
            ('E4', 330, GREEN),
            ('G4', 392, RED),
            ('B5', 494, PINK)
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
        print(f"\n\n===========\n{self.notes}\n\n================\n\n")

    
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

        self.play(ReplacementTransform(self.small_plot[1].copy(), self.notes[0][1]))
        self.play(FadeIn(self.notes[0][2]))
        self.play(self.notes[0][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[0][3]))

        self.play(ReplacementTransform(self.small_plot[1].copy(), self.notes[1][1]))
        self.play(FadeIn(self.notes[1][2]))
        self.play(self.notes[1][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[1][3]))

        self.play(ReplacementTransform(self.small_plot[1].copy(), self.notes[2][1]))
        self.play(FadeIn(self.notes[2][2]))
        self.play(self.notes[2][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[2][3]))

        self.play(ReplacementTransform(self.small_plot[1].copy(), self.notes[3][1]))
        self.play(FadeIn(self.notes[3][2]))
        self.play(self.notes[3][3].animate.shift(RIGHT*10), run_time=3, rate_func=linear)
        self.play(FadeOut(self.notes[3][3]))

        self.wait(3)

        sq = Square()
        sq.shift(UP*20)
        self.play(ReplacementTransform(self.big_plot, sq), ReplacementTransform(self.small_plot, sq), *[ReplacementTransform(i, sq) for i in self.notes])

        self.play(Create(self.ax1[0]), run_time=2)
        self.play(Create(self.ax1[1]), run_time=4)
        self.play(FadeIn(self.ax1[2]), run_time=0.5)
        self.play(self.ax1[3].animate.shift(RIGHT*12), run_time=2, rate_func=linear)
        self.play(FadeOut(self.ax1[3]))
        self.ax1[3].shift(LEFT*12)
        
        self.wait(2)

        self.play(ReplacementTransform(self.ax1[1], self.ax2[1]), ReplacementTransform(self.ax1[2], self.ax2[2]))
        self.play(Create(self.ax1[1]), run_time=4)
        self.play(FadeIn(self.ax1[2]), run_time=0.5)
        self.play(self.ax1[3].animate.shift(RIGHT*12), run_time=2, rate_func=linear)
        self.play(FadeOut(self.ax1[3]))

        self.wait(2)



### Done in high quality
class IntroducingFT(Scene):
    def construct(self):
        self.wait(5)
        self.initialise_objects()
        self.play_scene()
        self.unit_circle()
        self.wait(5)
    
    def initialise_objects(self):
        self.tt = MathTex(r"\begin{array}{c} Time \\ f(t) \end{array}", color=YELLOW).shift(LEFT*3)
        self.tar = MathTex(r"\Longleftrightarrow", color=YELLOW)
        self.ft = MathTex(r"\begin{array}{c} Frequency \\ F(\omega) \end{array}", color=YELLOW).shift(RIGHT*3)

        self.t2 = MathTex(
            r"F(\omega )",
            r"=\int_{-\infty}^{\infty}",
            r"f(t)",
            r"e^{-i\omega t}",
            r"\ dt",
            color=YELLOW
        )

        ax1 = Axes(
            x_range=(0, 2, 1), y_range=(-2, 2, 2),
            x_length=5, y_length=4,
            tips=False,
            x_axis_config={"include_numbers": True}
        )
        axs1 = ax1.plot(lambda x: np.sin(2*2*PI*x), color=RED)
        self.vg1 = VGroup(ax1, axs1)
        self.vg1.shift(LEFT*4)

        ax2 = Axes(
            x_range=(0, 3, 1), y_range=(-2, 2, 2),
            x_length=5, y_length=4,
            tips=False,
            x_axis_config={"include_numbers": True}
        )
        axs2 = Arrow(start=np.array([0.835, -0.3, 0]), end=np.array([0.835, 2, 0]), color=RED, tip_shape=StealthTip)
        self.vg2 = VGroup(ax2, axs2)
        self.vg2.shift(RIGHT*4)
        self.axs2l = MathTex("\\infty", color=RED).next_to(axs2, UP, buff=0.2)

    def play_scene(self):
        self.wait()

        t = Title("Introducing the Fourier Transform", color=RED)
        self.play(Write(t))
        self.wait()

        self.play(FadeIn(self.tt, self.ft, self.tar))
        self.wait()
        self.play(self.tt.animate.shift(DL).shift(DOWN*2), self.ft.animate.shift(DR).shift(DOWN*2), self.tar.animate.shift(DOWN*3))

        self.play(Write(self.t2), run_time=2)
        self.play(FadeOut(t), self.t2.animate.shift(UP*3))

        self.play(Create(self.vg1[0]), Create(self.vg2[0]))
        self.play(Create(self.vg1[1]), Create(self.vg2[1]), Write(self.axs2l))

        self.wait(15)

        ft_image = ImageMobject("src/td_to_fd.png")
        self.play(FadeIn(ft_image))
        self.wait(8)
        self.remove(ft_image)
        self.play(FadeOut(self.tt, self.ft, self.tar, self.vg1, self.vg2, self.axs2l))

        jf_image = ImageMobject("src/jf.png").scale(0.5)
        self.play(FadeIn(jf_image))
        self.wait(4)
        self.play(jf_image.animate.shift(LEFT*5))

        ax1 = Axes(
            x_range=(0, 2, 1), y_range=(-2, 2, 2),
            x_length=5, y_length=4,
            tips=False,
            x_axis_config={"include_numbers": True}
        )
        axs1 = ax1.plot(lambda x: np.sin(2*2*PI*x - 0.5*PI), color=RED)
        vg1 = VGroup(ax1, axs1)

        vg1.shift(RIGHT*2).shift(DOWN*0.6).scale(1.5)
        self.play(Create(ax1))
        self.play(Create(axs1))

        self.wait(3)

        dot1 = Dot(ax1.c2p(0.25, 1), color=BLUE)
        dot1l = ax1.get_line_from_axis_to_point(0, ax1.c2p(0.25, 1))
        dot2 = Dot(ax1.c2p(0.75, 1), color=BLUE)
        dot2l = ax1.get_line_from_axis_to_point(0, ax1.c2p(0.75, 1))

        self.play(Create(dot1), Create(dot1l))
        self.play(Create(dot2), Create(dot2l))

        tl = Line(ax1.c2p(0.25, 1), ax1.c2p(0.75, 1), color=BLUE)
        tlt = MathTex("T", color=BLUE).next_to(tl, UP, buff=0.1)
        al = Arrow(ax1.c2p(1.25, -0.17), ax1.c2p(1.25, 1.15), color=BLUE)
        alt = MathTex("A", color=BLUE).next_to(al, RIGHT, buff=0.2)
        pll = ax1.get_line_from_axis_to_point(0, ax1.c2p(0.25, -1))
        pl = Arrow(ax1.c2p(-0.07, -1), ax1.c2p(0.3, -1), color=BLUE)
        plt = MathTex("\\theta", color=BLUE).next_to(pl, DOWN, buff=0.1)

        self.play(Create(al), Write(alt))
        self.play(Create(tl), Write(tlt))
        self.play(Create(pl), Create(pll), Write(plt))

        self.wait(5)

        self.play(FadeOut(jf_image, shift=LEFT*2), FadeOut(dot1, dot1l, dot2, dot2l, vg1, tl, tlt, al, alt, pl, pll, plt, shift=RIGHT*4))

        self.wait()

        ef = MathTex(EULERS_FORMULA, color=BLUE)
        efr = SurroundingRectangle(ef, color=YELLOW)
        evg = VGroup(ef, efr)

        self.play(Write(ef), Create(efr), run_time=2)
        self.play(evg.animate.shift(UR*3).shift(RIGHT), self.t2.animate.shift(LEFT*4))
        
        ftr = SurroundingRectangle(self.t2[3], color=RED)
        self.play(Create(ftr))

        e = self.t2[3].copy().set_color(WHITE)
        eff = MathTex(r"&=\cos{(-\omega t)}+i\sin{(-\omega t)} \\", r"&= \cos{(\omega t)}-i\sin{(\omega t)}").shift(UP*0.6)
        self.play(e.animate.shift(LEFT*2).shift(DOWN*2))
        self.play(Write(eff), run_time=4)

        self.wait(2)

        ec = MathTex(r"e^{-i\omega t}", r"=\cos{(\omega t)}-i\sin{(\omega t)}").shift(UR*2).shift(RIGHT)
        self.play(FadeOut(eff[0]), ReplacementTransform(e, ec[0]), ReplacementTransform(eff[1], ec[1]))
        ecr = SurroundingRectangle(ec, color=YELLOW)
        self.play(Create(ecr))
        self.play(Uncreate(ftr))

        #

        ftr1 = SurroundingRectangle(self.t2[2:-1], color=RED)
        self.play(Create(ftr1))

        f2 = MathTex(
            r"F(\omega)&=\int_{-\infty}^{\infty}f(t)[\cos({\omega})-i\sin({\omega t})] \ dt \\",
            r"F(\omega)&=\int_{-\infty}^{\infty}f(t)\cos({\omega}) \ dt-i\int_{-\infty}^{\infty}f(t)\sin({\omega t}) \ dt"
        )
        self.play(Write(f2[0]), run_time=3)
        self.play(Write(f2[1]), run_time=3)
        
        self.wait(3)

        self.play(FadeOut(f2, ec, ecr, shift=UP*3))
        self.play(Uncreate(ftr1))

        arg_dia = NumberPlane(
            (-20, 20, 1), (-20, 20, 1),
            background_line_style={
                "stroke_opacity": 0.3
            }
        ).add_coordinates().shift(DL*3).shift(UP*1.5)
        y_label = arg_dia.get_y_axis_label(Tex("Im", color=RED)).shift(DL*1.5)
        x_label = arg_dia.get_x_axis_label(Tex("Re", color=RED))
        labels = VGroup(y_label, x_label)

        self.play(Create(arg_dia), Create(labels), run_time=2)

        yl = Line(arg_dia.c2p(5, 0), arg_dia.c2p(5, 3))
        ylt = MathTex(r"\int_{-\infty}^{\infty}f(t)\sin({\omega t})", color=YELLOW).next_to(yl, RIGHT, buff=0.3)
        xl = Line(arg_dia.c2p(0, 0), arg_dia.c2p(5, 3))
        xlt = MathTex(r"\int_{-\infty}^{\infty}f(t)\cos({\omega})", color=YELLOW).next_to(yl, DOWN, buff=0.3).shift(LEFT*2.2)
        theta = MathTex(r"\theta", color=BLUE).shift(DL*1.1).shift(LEFT*0.7)
        fmag = MathTex(r"|f(\omega)|", color=YELLOW).next_to(xl, UP, buff=0.3).shift(DOWN)
        
        self.play(Create(yl), Create(xl), Create(ylt), Create(xlt), Write(theta), Write(fmag))

        self.wait(5)

        mod_arg_image = ImageMobject("src/mod_arg.png").scale(0.8).shift(RIGHT*3).shift(DOWN*2)
        imgsr = SurroundingRectangle(mod_arg_image, color=YELLOW)
        self.play(FadeIn(mod_arg_image), Create(imgsr))

        self.wait(8)

        self.play(FadeOut(arg_dia, imgsr, mod_arg_image, theta, fmag, yl, ylt, xl, xlt, labels, self.t2, ef, efr))

        self.wait()

        # ===== =====   ===== =====
    
    def unit_circle(self):
        n = ValueTracker(0)

        unit_circle = Circle(1, color=WHITE)
        point = always_redraw(
            lambda: Dot(color=BLUE, radius=.1, stroke_width=0).move_to(unit_circle.point_at_angle(n.get_value()*DEGREES))
        )
        hline = always_redraw(
            lambda: Line(unit_circle.get_center(), point)
        )
        yline = always_redraw(
            lambda: Line((point.get_x(), unit_circle.get_y(), 0), point, color=YELLOW)
        )
        xline = always_redraw(
            lambda: Line(unit_circle.get_center(), (point.get_x(), unit_circle.get_y(), 0), color=RED)
        )

        self.play(Create(unit_circle), Create(point), Create(hline), Create(yline), Create(xline))
        eulers = MathTex(r"e^{i\theta}", color=YELLOW).next_to(unit_circle, UP)
        self.play(FadeIn(eulers, shift=UP))
        circ = VGroup(unit_circle, eulers)

        self.play(circ.animate.shift(LEFT*5).shift(UP*2))
        self.wait(5)


        sin_ax = Axes(
            x_range=(0, 2*PI, PI), y_range=(-1, 1, 1),
            x_length=5, y_length=2,
            tips=False,
        ).shift(UP*2)
        sin_gr = sin_ax.plot(lambda x: np.sin(x), color=RED)
        sin_ogr = sin_ax.plot(lambda x: np.sin(-x), color=RED)

        cos_ax = Axes(
            x_range=(0, 2*PI, PI), y_range=(-1, 1, 1),
            x_length=5, y_length=2,
            tips=False,
        ).shift(DOWN*1.5).shift(LEFT*5).rotate(-90*DEGREES)
        cos_gr = cos_ax.plot(lambda x: np.cos(x), color=YELLOW)


        self.play(Create(sin_ax), Create(cos_ax))
        self.play(n.animate.set_value(360), Create(sin_gr), Create(cos_gr), rate_func=linear, run_time=10)
        self.wait(3)
        self.play(FadeOut(sin_gr, cos_gr))
        self.play(n.animate.set_value(0), Create(sin_ogr), Create(cos_gr), rate_func=linear, run_time=10)

        st = MathTex(r"\sin({-\theta})&=-\sin({\theta}) \\", r"\cos({\theta})&=\cos({-\theta})", color=BLUE).shift(RIGHT).shift(DOWN)
        sr = SurroundingRectangle(st, color=YELLOW, buff=MED_LARGE_BUFF)

        self.play(Write(st[0]), run_time=2)
        self.wait()
        self.play(Write(st[1]), run_time=2)
        self.wait()
        self.play(Create(sr), rate_func=rate_functions.ease_in_out_quint, run_time=3)



### Done in high quality
class ApplyingFT(Scene):
    def construct(self):
        self.wait(3)
        self.play_scene()
        self.wait(3)
    
    def play_scene(self):
        t = Title("Applying the Fourier Transform", color=RED)
        self.play(Write(t))
        self.wait(3)

        ft = MathTex(r"f(t)&=\cos{(5\pi t)}", color=YELLOW)
        self.play(Write(ft))
        self.play(ft.animate.shift(UP*3).shift(LEFT*3), FadeOut(t, shift=UP*2))
        ftt = MathTex(FOURIER_TRANSFORM, color=BLUE)
        fttr = SurroundingRectangle(ftt, color=YELLOW)
        ftt = VGroup(ftt, fttr)
        self.play(Write(ftt))
        self.play(ftt.animate.shift(UP*3).shift(RIGHT*3))
        fft = MathTex(
            r"F(\omega)&= \int_{-\infty}^{\infty} \cos{(5\pi t)}e^{-i\omega t} \ dt \\",
            r"&= \int_{-\infty}^{\infty} \cos{(5\pi t)}\cos{(\omega t)}-i\cos{(5\pi t)}\sin{(\omega t)} \ dt \\",
            r"&=\int_{-\infty}^{\infty} \cos{(5\pi t)}\cos{(\omega t)} \ dt - i\int_{-\infty}^{\infty} \cos{(5\pi t)}\sin{(\omega t)} \ dt \\ ",
            r"F_{r}(\omega)&=\int_{-\infty}^{\infty} \cos{(5\pi t)}\cos{(\omega t)} \ dt"
        ).scale(0.7)
        fft[3].set_color(YELLOW).set_z_index(2)
        self.play(Write(fft[0]), run_time=2)
        self.play(Write(fft[1]), run_time=2)
        self.play(Write(fft[2]), run_time=2)
        self.wait(1.5)
        self.play(Write(fft[3]), run_time=2)
        _rft = SurroundingRectangle(fft[3], color=RED, z_index=1)
        _rfb = BackgroundRectangle(fft[3], fill_opacity=1, buff=0.1, z_index=1)
        self.play(Create(_rft))
        self.wait(5)
        rft = VGroup(fft[3], _rft, _rfb)
        self.play(rft.animate.shift(UP*4.8).shift(LEFT*2), FadeOut(ft, ftt, fft[0:3], shift=UP*2))

        self.wait(5)

        n = ValueTracker(1)
        dn = r"2\pi"
        a = "0"

        #_nt = always_redraw(
        #    lambda: MathTex(rf"\omega={dn}", color=RED).shift(RIGHT*3).shift(DOWN*3).#set_z_index(3)
        #)
        _nt = Variable(1, r"\omega", num_decimal_places=2).shift(RIGHT*3).shift(UP*3.5)
        _nt_pi = always_redraw(
            lambda: MathTex(f"{dn}", color=RED).set_z_index(3).move_to(_nt).shift(RIGHT*0.6)
        )
        _a = always_redraw(
            lambda: MathTex(f"Area\\approx{a}", color=RED).set_z_index(3).shift(UP*3.5)
        )
        _nt.label.set_color(YELLOW)
        _nt.value.set_color(RED)
        nt_tracker = _nt.tracker
        _ntb = BackgroundRectangle(_nt_pi, fill_opacity=1, buff=0.4, z_index=1)

        _ax = NumberPlane(
            (-3*PI, 3*PI, 1), (-1.5, 1.5, 0.25),
            16, 8,
            background_line_style={
                "stroke_opacity": 0.3
            }
        ).shift(DOWN)
        xlabel = _ax.get_x_axis_label(
            MathTex(r"\omega"),
            direction=DOWN
        )
        ax_eq = always_redraw(
            lambda: _ax.plot(lambda x: np.cos(5*x)*np.cos((n.get_value()/PI)*x))
        )
        ax_ar = always_redraw(
            lambda: _ax.get_area(ax_eq, color=YELLOW_B)
        )

        ax = VGroup(_ax, xlabel)

        self.play(Create(ax), Write(_nt), Write(_a), FadeIn(_rfb), run_time=2)
        self.play(Create(ax_eq), run_time=2)
        self.play(Write(ax_ar))

        self.wait(5)

        self.play(Uncreate(_nt_pi), run_time=0.0000001)
        self.play(n.animate.set_value(2*PI), nt_tracker.animate.set_value(2*PI), run_time=5)
        self.play(FadeIn(_nt_pi, _ntb))
        self.wait(2)
        self.play(FadeOut(_nt_pi, _ntb))
        dn = r"3\pi"
        self.play(Uncreate(_nt_pi), run_time=0.0000001)
        self.play(n.animate.set_value(3*PI), nt_tracker.animate.set_value(3*PI), run_time=5)
        self.play(FadeIn(_nt_pi, _ntb))
        self.wait(2)
        self.play(FadeOut(_nt_pi, _ntb))
        dn = r"5\pi"
        self.play(Uncreate(_nt_pi), run_time=0.0000001)
        self.play(n.animate.set_value(5*PI), nt_tracker.animate.set_value(5*PI), run_time=5)
        a = r"\infty"
        self.play(FadeIn(_nt_pi, _ntb))
        self.wait(10)
        self.play(FadeOut(_nt_pi, _ntb))
        dn = r"6\pi"
        self.play(Uncreate(_nt_pi), run_time=0.0000001)
        a = "0"
        self.play(n.animate.set_value(6*PI), nt_tracker.animate.set_value(6*PI), run_time=2)
        self.play(FadeIn(_nt_pi, _ntb))
        
        self.wait(5)
        self.play(FadeOut(ax, _a, _nt, _rfb, ax_eq, ax_ar, _nt_pi, _ntb, _rft, fft[3]))

        _fi = MathTex(r"F_{r}(\omega)&=\int_{-\infty}^{\infty} \cos{(5\pi t)}\sin{(\omega t)} dt", color=YELLOW).scale(0.7)
        fib = SurroundingRectangle(_fi, color=RED)
        self.play(Write(_fi), Create(fib))
        fi = VGroup(_fi, fib)
        self.play(fi.animate.shift(UP*3.2).shift(LEFT*4))

        n.set_value(1)
        nt_tracker.set_value(1.00)

        ax_eq = always_redraw(
            lambda: _ax.plot(lambda x: np.cos(5*x)*np.sin((n.get_value()/PI)*x))
        )
        ax_ar = always_redraw(
            lambda: _ax.get_area(ax_eq, color=YELLOW_B)
        )
        
        self.play(Create(ax), Create(_nt), Write(_a), run_time=2)
        self.play(Create(ax_eq), run_time=2)
        self.play(Write(ax_ar))

        self.wait(5)

        self.play(n.animate.set_value(2*PI), nt_tracker.animate.set_value(2*PI), run_time=5)
        self.play(n.animate.set_value(3*PI), nt_tracker.animate.set_value(3*PI), run_time=5)
        self.play(n.animate.set_value(5*PI), nt_tracker.animate.set_value(5*PI), run_time=5)
        self.wait(3)
        self.play(n.animate.set_value(6*PI), nt_tracker.animate.set_value(6*PI), run_time=5)

        self.wait(10)
        self.play(FadeOut(fi, ax_eq, ax_ar, ax, _nt, _a))

        fft = MathTex(
            r"F(\omega)&= \int_{-\infty}^{\infty} \cos{(5\pi t)}e^{-i\omega t} dt \\",
            r"&= \int_{-\infty}^{\infty} \cos{(5\pi t)}\cos{(\omega t)}-i\cos{(5\pi t)}\sin{(\omega t)} \ dt \\",
            r"&=\int_{-\infty}^{\infty} \cos{(5\pi t)}\cos{(\omega t)} \ dt - i\int_{-\infty}^{\infty} \cos{(5\pi t)}\sin{(\omega t)} \ dt \\ \\",
            r"F(\omega)&=F_{r}(\omega)-iF_{i}(\omega) \quad \textrm{since} \quad F_{i}=0 ; \\ ",
            r"F(\omega)&=\int_{-\infty}^{\infty} \cos{(5\pi t)}\cos{(\omega t)} \ dt \\ ",
            r"\textrm{When} \quad \omega&=5\pi ; \\",
            r"F(5\pi)&=\int_{-\infty}^{\infty} \cos{(5\pi t)}\cos{(5\pi t)} \ dt \\ ",
            r"&=\int_{-\infty}^{\infty} \cos^{2}{(5\pi t)} \ dt \\ ",
            r"F(5\pi)&=\infty"
        ).scale(0.7)
        fft[-1].set_color(YELLOW)
        _ftr = SurroundingRectangle(fft[-1], color=RED)
        ftr = VGroup(fft[-1], _ftr)

        for i in fft:
            self.play(Write(i), run_time=3)
        
        self.wait(5)
        self.play(Create(_ftr))
        self.play(FadeOut(fft[0:-1]), ftr.animate.shift(UP*7.2))
        
        ax = Axes(
            (-3, 3, 1), (-1, 5, 1),
            8, 6,
            tips=False
        )
        xlabel = ax.get_x_axis_label(r"\omega")
        pline = ax.get_line_from_axis_to_point(
            0, ax.c2p(2, 4),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        pline_t = MathTex(r"\infty", color=RED).next_to(pline, UP)
        pline_l = MathTex(r"+5\pi").next_to(pline, DOWN*1.3)
        nline = ax.get_line_from_axis_to_point(
            0, ax.c2p(-2, 4),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        nline_t = pline_t.copy().next_to(nline, UP)
        nline_l = MathTex(r"-5\pi").next_to(nline, DOWN*1.3)

        self.play(Create(ax), Create(xlabel), run_time=2)
        self.play(
            Create(pline), Create(nline),
            Write(pline_t), Write(nline_t),
            Write(pline_l), Write(nline_l),
            run_time=2
        )

        self.wait(10)
        self.play(FadeOut(ftr, ax, xlabel, pline, pline_t, pline_l, nline, nline_t, nline_l))

        fft = MathTex(
            r"F_{r}(\omega)=\int_{-\infty}^{\infty}[",
            r"\cos{( 1.4 t)}", '+',
            r"\cos{( 2.2 t)}", '+',
            r"\cos{( \pi t)}", '+',
            r"\cos{( 3\pi t)}",
            r"]\cos{( \quad \omega \quad t)} \ dt",
            substrings_to_isolate=(r"\omega",),
            color=YELLOW
        ).scale(0.8).set_color_by_tex(r"\omega", RED)
        
        dn = DecimalNumber(1, color=RED).scale(0.8).next_to(fft, RIGHT).shift(LEFT*1.75)

        self.play(Write(fft), run_time=2)
        
        ul = Underline(fft[3], color=RED)

        self.play(FadeOut(fft[-2]), FadeIn(dn))

        self.play(Create(ul))
        self.play(dn.animate.set_value(1.4))
        self.wait(2)
        self.play(
            ul.animate.next_to(fft[4], DOWN, buff=0.2).shift(RIGHT),
            dn.animate.set_value(2.2)
        )
        self.wait(2)
        self.play(
            ul.animate.next_to(fft[5], DOWN, buff=0.2).shift(RIGHT*2),
            dn.animate.set_value(PI)
        )
        self.wait(2)
        self.play(
            ul.animate.next_to(fft[6], DOWN, buff=0.2).shift(RIGHT*2.8),
            dn.animate.set_value(3*PI)
        )
        self.wait(2)
        
        self.wait(5)
        self.play(FadeOut(ul, fft, dn))
        
        ft = MathTex(r"f(t)=\sin{(5\pi t)}", color=YELLOW).shift(UP*3)
        self.play(Write(ft), run_time=2)
        self.wait(3)
        fft = MathTex(
            r"F(\omega)&=\int_{-\infty}^{\infty}\sin(5\pi t)e^{-i\omega t} \ dt \\",
            r"&=\int_{-\infty}^{\infty}\sin(5\pi t)\cos{(\omega t) \ dt-i\int_{-\infty}^{\infty}\sin(5\pi t)}\sin{(\omega t)} \ dt \\ \\",
            r"F_{r}(\omega)&=\int_{-\infty}^{\infty}\sin(5\pi t)\cos{(\omega t) \ dt"
        )
        self.play(Write(fft[0:2]), run_time=3)
        self.play(Write(fft[2]), run_time=2)
        self.play(FadeOut(ft, fft[0:2]), fft[2].animate.set_color(YELLOW), fft[2].animate.shift(UP*5).scale(0.7).shift(LEFT))

        # ===== =====
        n = ValueTracker(1)
        nt_tracker.set_value(1.00)

        _ax = NumberPlane(
            (-3*PI, 3*PI, 1), (-1.5, 1.5, 0.25),
            16, 8,
            background_line_style={
                "stroke_opacity": 0.3
            }
        ).shift(DOWN)
        xlabel = _ax.get_x_axis_label(
            MathTex(r"\omega"),
            direction=DOWN
        )
        ax_eq = always_redraw(
            lambda: _ax.plot(lambda x: np.sin(5*x)*np.cos((n.get_value()/PI)*x))
        )
        ax_ar = always_redraw(
            lambda: _ax.get_area(ax_eq, color=YELLOW_B)
        )
        a = "0"
        _a = always_redraw(
            lambda: MathTex(f"Area\\approx{a}", color=RED).set_z_index(3).shift(UP*3.5)
        )

        ax = VGroup(_ax, xlabel)

        self.play(Create(ax), Write(_nt), Write(_a), run_time=2)
        self.play(Create(ax_eq), run_time=2)
        self.play(Write(ax_ar))

        self.play(n.animate.set_value(2*PI), nt_tracker.animate.set_value(2*PI), run_time=2)
        self.wait(2)
        self.play(n.animate.set_value(5*PI), nt_tracker.animate.set_value(5*PI), run_time=4)
        self.wait(5)
        self.play(FadeOut(ax, _a, _nt, ax_eq, ax_ar, fft[2]))
        # ===== =====

        fti = MathTex(r"F_{i}(\omega)&=\int_{-\infty}^{\infty}\sin{(5\pi t)}\sin{(\omega t)} \ dt", color=YELLOW)
        self.play(Write(fti), run_time=2)
        self.play(fti.animate.scale(0.7).shift(UP*2.5).shift(LEFT*3))
        # ===== =====
        n = ValueTracker(1)
        nt_tracker.set_value(1.00)

        _ax = NumberPlane(
            (-3*PI, 3*PI, 1), (-1.5, 1.5, 0.25),
            16, 8,
            background_line_style={
                "stroke_opacity": 0.3
            }
        ).shift(DOWN)
        xlabel = _ax.get_x_axis_label(
            MathTex(r"\omega"),
            direction=DOWN
        )
        ax_eq = always_redraw(
            lambda: _ax.plot(lambda x: np.sin(5*x)*np.sin((n.get_value()/PI)*x))
        )
        ax_ar = always_redraw(
            lambda: _ax.get_area(ax_eq, color=YELLOW_B)
        )
        a = "0"
        _a = always_redraw(
            lambda: MathTex(f"Area\\approx{a}", color=RED).set_z_index(3).shift(UP*3.5)
        )

        ax = VGroup(_ax, xlabel)

        self.play(Create(ax), Write(_nt), Write(_a), run_time=2)
        self.play(Create(ax_eq), run_time=2)
        self.play(Write(ax_ar))

        mft = MathTex(
            r"F_{i}(\omega)&=\int_{-\infty}^{\infty}\sin{(5\pi t)}\sin{(5\pi t)} \ dt \\",
            r"&=\int_{-\infty}^{\infty}\sin^{2}{(5\pi t)} \ dt",
            color=BLUE
        ).shift(DOWN*2.5).scale(0.7)

        self.play(n.animate.set_value(2*PI), nt_tracker.animate.set_value(2*PI), run_time=2)
        self.wait(2)
        self.play(n.animate.set_value(5*PI), nt_tracker.animate.set_value(5*PI), run_time=4)
        a = r"\infty"
        self.play(Write(mft), run_time=2)
        self.wait(5)
        self.play(FadeOut(mft))
        a = "0"
        self.play(n.animate.set_value(-5*PI), nt_tracker.animate.set_value(-5*PI), run_time=6)
        a = r"-\infty"
        nmft = MathTex(
            r"F_{i}(\omega)&=\int_{-\infty}^{\infty}\sin{(5\pi t)}\sin{(-5\pi t)} \ dt \\",
            r"&=-\int_{-\infty}^{\infty}\sin^{2}{(5\pi t)} \ dt",
            color=BLUE
        ).shift(UP).scale(0.7)
        self.play(Write(nmft), run_time=2)
        self.wait(5)

        self.play(FadeOut(ax, _a, _nt, ax_eq, ax_ar, nmft, nmft, fti))
        # ===== =====

        ft = MathTex(r"\therefore F(5\pi)&=\pm i\int_{-\infty}^{\infty}\sin^{2}{(5\pi t)} \ dt", color=YELLOW)
        self.play(Write(ft))
        self.play(ft.animate.shift(UP*3.5).shift(LEFT*3).scale(0.7))

        ax = Axes(
            (-3, 3, 1), (-5, 5, 1),
            8, 6,
            tips=False
        )
        xlabel = ax.get_x_axis_label(r"\omega")
        pline = ax.get_line_from_axis_to_point(
            0, ax.c2p(2, -4),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        pline_t = MathTex(r"-\infty", color=RED).next_to(pline, DOWN)
        pline_l = MathTex(r"+5\pi").next_to(pline, UP*1.3)
        nline = ax.get_line_from_axis_to_point(
            0, ax.c2p(-2, 4),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        nline_t = MathTex(r"\infty", color=RED).next_to(nline, UP)
        nline_l = MathTex(r"-5\pi").next_to(nline, DOWN*1.3)

        self.play(Create(ax), Create(xlabel), run_time=2)
        self.play(
            Create(pline), Create(nline),
            Write(pline_t), Write(nline_t),
            Write(pline_l), Write(nline_l),
            run_time=2
        )

        self.wait(15)
        self.play(FadeOut(ft, ax, xlabel, pline, pline_t, pline_l, nline, nline_t, nline_l))



### Done in high quality
class IntegrationByParts(Scene):
    def construct(self):
        self.wait(3)
        self.play_scene()
        self.wait(3)
    
    def play_scene(self):
        t = Title("Integration by Parts", color=RED)
        self.play(Write(t))
        
        self.wait(5)

        ibp_img = ImageMobject("src/int_by_parts.png").scale(1.5).shift(RIGHT)
        self.play(FadeIn(ibp_img))

        self.wait(5)
        self.play(ibp_img.animate.shift(RIGHT*3))

        liate_img = ImageMobject("src/liate_rule.png").shift(LEFT*3)
        self.play(FadeIn(liate_img, shift=RIGHT*2))

        self.wait(5)
        self.play(FadeOut(t, ibp_img, liate_img))

        tri = MathTex(
            r"\Lambda(t)=\left\{\begin{array}{rcl}1+t & \textrm{for} & -1\leq t<0 \\ 1-t & \textrm{for} & 0\leq t \leq +1 \\ 0 & & otherwise \end{array}\right.",
            color=BLUE
        )
        tri_sr = SurroundingRectangle(tri, color=YELLOW)
        tri = VGroup(tri, tri_sr)
        self.play(Write(tri), run_time=2)
        self.play(tri.animate.scale(0.7).shift(LEFT*4).shift(UP*2))

        ax = Axes(
            (-3, 3, 1), (-0.5, 1.5, 0.5),
            12, 6
        )
        label1 = Text("1").next_to(ax.c2p(0, 1), LEFT, buff=0.2)
        labelp1 = Text("1").next_to(ax.c2p(1, 0), DOWN, buff=0.2)
        labeln1 = Text("-1").next_to(ax.c2p(-1, 0), DOWN, buff=0.2)
        label0 = Text("0").next_to(ax.c2p(0, 0), DL, buff=0.2)
        def tri_func(x):
            if -1 <= x and x < 0: return 1+x
            if 0 <= x and x <= 1: return 1-x
            # otherwise
            return 0
        ax_eq = ax.plot(lambda x: tri_func(x), color=BLUE)

        self.play(Create(ax), Create(label1), Create(labelp1), Create(labeln1), Create(label0))
        self.play(Create(ax_eq), run_time=2)

        self.wait(5)
        self.play(FadeOut(ax, label1, label0, labelp1, labeln1, ax_eq))
        self.play(tri.animate.shift(RIGHT*8).shift(UP))

        ft = MathTex(
            r"\textrm{For} \quad f(t)&=\Lambda(t) \\ \\",
            r"F(\omega)&=\int_{-\infty}^{\infty}\Lambda(t)e^{-i\omega t} \ dt \\",
            r"F(\omega)&=\int_{-1}^{0}(1+t)e^{-i\omega t} \ dt+\int_{0}^{+1}(1-t)e^{-i\omega t} \ dt \\",
            r"&={{ \int_{-1}^{0}1\cdot e^{-i\omega t} \ dt }}+\int_{-1}^{0}t\cdot e^{-i\omega t} \ dt+{{ \int_{0}^{+1}1\cdot e^{-i\omega t} \ dt }}-\int_{0}^{+1}t\cdot e^{-i\omega t} \ dt \\",
            r"&={{ \int_{-1}^{+1}e^{-i\omega t} \ dt }}+\int_{-1}^{0}t e^{-i\omega t} \ dt-\int_{0}^{+1}t e^{-i\omega t} \ dt"
        ).scale(0.7)
        ft[0].set_color(YELLOW)
        self.play(Write(ft[0]))
        self.wait(3)
        self.play(Write(ft[1]), run_time=2)
        self.play(Write(ft[2:]))
        sr1 = SurroundingRectangle(ft[4], color=RED)
        sr2 = SurroundingRectangle(ft[6], color=RED)
        self.play(Create(sr1), Create(sr2))

        self.wait(5)

        sr = SurroundingRectangle(ft[9], color=YELLOW)
        self.play(Create(sr), FadeOut(sr1, sr2))

        self.wait()

        t1 = MathTex(
            r"T_{1}&=", r"\int_{-1}^{+1}e^{-i\omega t} \ dt \\ ",
            r"&=\left[\frac{-1}{i\omega}\cdot e^{-i\omega t}\right]_{-1}^{+1} \\",
            r"&=\frac{-1}{i\omega}\left[e^{-i\omega\cdot 1}-e^{-i\omega\cdot -1}\right] \\ ",
            r"&=", r"\frac{i(e^{-i\omega}-e^{i\omega})}{\omega}"
        ).shift(LEFT*4).shift(UP).scale(0.7)
        t1[0:2].set_color(YELLOW)
        t1_sr = SurroundingRectangle(t1[-1], color=YELLOW)

        self.play(FadeOut(ft[1:9], ft[10:11], sr), ft[0].animate.shift(UP), Write(t1[0]), ReplacementTransform(ft[9], t1[1]), run_time=2)
        self.wait()
        self.play(Write(t1[2:]), run_time=4)
        self.wait(5)
        self.play(Create(t1_sr))
        self.wait(3)
        self.play(FadeOut(t1[1:-1], ft[9]), Uncreate(t1_sr), t1[0].animate.shift(RIGHT*9.5).shift(DOWN))
        self.play(t1[-1].animate.next_to(t1[0], RIGHT))
        t1[-1].set_color(YELLOW)
        t1 = VGroup(t1[0], t1[-1])
        t1_sr = SurroundingRectangle(t1, color=RED)
        self.play(Create(t1_sr), FadeOut(ft[0]))

        self.wait(5)

        fpe = MathTex(
            r"F(\omega)&=\int_{-1}^{+1}e^{-i\omega t} \ dt+\int_{-1}^{0}",
            r"t e^{-i\omega t}",
            r" \ dt-\int_{0}^{+1}",
            r"t e^{-i\omega t}",
            r"\ dt \\ \\ \\ ",
            r"\int t e^{-i\omega t} \ dt"
        ).scale(0.7).shift(LEFT*3).shift(UP)
        fpe[-1].set_color(YELLOW).shift(RIGHT*2)

        f1_ul = Underline(fpe[1], color=RED)
        f2_ul = Underline(fpe[3], color=RED)
        self.play(Write(fpe[0:-1]))
        self.wait(2)
        self.play(Create(f1_ul), Create(f2_ul))
        self.wait(2)
        self.play(Write(fpe[-1]))
        self.wait(5)
        self.play(Uncreate(f1_ul), Uncreate(f2_ul), FadeOut(fpe[0:-1]), fpe[-1].animate.shift(UP*3.5))

        _t23 = MathTex(
            r"T_{2,3}&=",
            r"\textrm{Let} \quad \begin{array}{rl}u=t & v'=e^{-i\omega t} \\ u'=1 & v=\frac{-1}{i\omega}\cdot e^{-i\omega t} \end{array} \\ \\ ",
            r"T_{2,3}&=t\cdot \frac{-1}{i\omega}\cdot e^{-i\omega t}-\int 1\cdot \frac{-1}{i\omega t}\cdot e^{-i\omega t} \ dt \\",
            r"&=\frac{ite^{-i\omega t}}{\omega}+\frac{1}{i\omega}\int e^{-i\omega t} \ dt \\",
            r"&=\frac{ite^{-i\omega t}}{\omega}+\frac{1}{i\omega}\left(\frac{-1}{i\omega}\cdot e^{-i\omega t}\right) \\",
            r"&=\frac{ite^{-i\omega t}}{\omega}-\frac{1}{i^{2}\omega^{2}}\cdot e^{-i\omega t} \\",
            r"&=\frac{ite^{-i\omega t}}{\omega}+\frac{e^{-i\omega t}}{\omega^{2}}",
            r"=\frac{i\omega t e^{-i\omega t}+e^{-i\omega t}}{\omega^{2}}",
            r"=", r"\frac{e^{-i\omega t}(1+i\omega t)}{\omega^{2}}"
        ).scale(0.7).shift(LEFT)
        _t23[0].set_color(YELLOW).next_to(fpe[-1], LEFT)
        _t23[1].set_color(BLUE).shift(DL*0.3).shift(LEFT)
        self.play(Write(_t23[0]))
        for i in range(1, 9):
            self.play(Write(_t23[i]), run_time=3)
            self.wait()
        self.play(Write(_t23[9], run_time=3))
        
        l_sr = SurroundingRectangle(_t23[-1], color=YELLOW)
        self.play(Create(l_sr))
        self.wait(3)
        self.play(Uncreate(l_sr))
        self.play(_t23[0].animate.next_to(t1, DOWN*2).shift(LEFT))
        self.play(_t23[-1].animate.next_to(_t23[0], RIGHT))
        _t23[-1].set_color(YELLOW)
        t23 = VGroup(_t23[0], _t23[-1])
        t23_sr = SurroundingRectangle(t23, color=RED)
        t23 += t23_sr
        self.play(Create(t23_sr))

        self.wait(5)

        self.play(Unwrite(_t23[1:-1]), Unwrite(fpe[-1]), run_time=3)
        self.play(Write(fpe[0:-1].set_color(YELLOW).shift(UP).shift(LEFT*0.4)))
        self.wait(2)
        f1_ul = Underline(fpe[1], color=RED).scale(2).shift(DOWN*0.35)
        self.play(Create(f1_ul))

        _t2 = MathTex(
            r"T_{2}&=",
            r"\int_{-1}^{0}t e^{-i\omega t} \ dt \\",
            r"&=\left[\frac{e^{-i\omega t}(1+i\omega t)}{\omega^{2}}\right]_{-1}^{0} \\",
            r"&=\frac{e^{-i\omega\cdot 0}(1+i\omega\cdot 0)}{\omega^{2}}-\frac{e^{-i\omega\cdot -1}(1+i\omega\cdot -1)}{\omega^{2}} \\",
            r"&=\frac{1(1+0)-e^{i\omega}(1-i\omega)}{\omega^{2}} \\",
            r"&=",
            r"\frac{1-e^{i\omega}(1-i\omega)}{\omega^{2}}"
        ).scale(0.7).shift(LEFT*2)
        _t2[0:2].set_color(YELLOW)
        _t2_sr = SurroundingRectangle(_t2[-1], color=YELLOW)
        self.play(Write(_t2[0:2]))
        for i in range(2, 5):
            self.play(Write(_t2[i]), run_time=3)
            self.wait()
        self.play(Write(_t2[-2:]), run_time=3)
        self.play(Create(_t2_sr))

        self.wait(2)
        self.play(Uncreate(_t2_sr), _t2[0].animate.next_to(t1, DOWN*2).shift(LEFT*1.1), t23.animate.shift(DOWN))
        _t2[-1].set_color(YELLOW)
        self.play(_t2[-1].animate.next_to(_t2[0], RIGHT))
        t2 = VGroup(_t2[0], _t2[-1])
        t2_sr = SurroundingRectangle(t2, color=RED)
        t2 += t2_sr
        self.play(Create(t2_sr))

        self.wait(5)

        self.play(Unwrite(_t2[1:-1]), run_time=3)
        self.wait()
        self.play(f1_ul.animate.shift(RIGHT*2))

        _t3 = MathTex(
            r"T_{3}&=",
            r"\int_{0}^{+1}t e^{-i\omega t} \ dt \\",
            r"&=\left[\frac{e^{-i\omega t}(1+i\omega t)}{\omega^{2}}\right]_{0}^{+1} \\",
            r"&=\frac{e^{-i\omega\cdot 1}(1+i\omega\cdot 1)}{\omega^{2}}-\frac{e^{-i\omega\cdot 0}(1+i\omega\cdot 0)}{\omega^{2}} \\",
            r"&=\frac{e^{-i\omega}(1+i\omega)-1(1+0)}{\omega^{2}} \\",
            r"&=",
            r"\frac{e^{-i\omega}(1+i\omega)-1}{\omega^{2}}"
        ).scale(0.7).shift(LEFT*2)
        _t3[0:2].set_color(YELLOW)
        _t3_sr = SurroundingRectangle(_t3[-1], color=YELLOW)
        self.play(Write(_t3[0:2]))
        for i in range(2, 5):
            self.play(Write(_t3[i]), run_time=3)
            self.wait()
        self.play(Write(_t3[-2:]), run_time=3)
        self.play(Create(_t3_sr))

        self.wait(2)
        self.play(Uncreate(_t3_sr), _t3[0].animate.next_to(t2, DOWN*1.7).shift(LEFT*1.25), t23.animate.shift(DOWN*1.4))
        _t3[-1].set_color(YELLOW)
        self.play(_t3[-1].animate.next_to(_t3[0], RIGHT))
        t3 = VGroup(_t3[0], _t3[-1])
        t3 += SurroundingRectangle(t3, color=RED)
        self.play(Create(t3[2]))
        self.play(FadeOut(t23, shift=DOWN*5))

        self.wait(5)
        self.play(FadeOut(_t3[1:-1], fpe[:-1], f1_ul))

        ttt = MathTex(
            r"F(\omega)&=T_{1}+T_{2}-T_{3} \\",
            r"&=\frac{i(e^{-i\omega}-e^{i\omega})}{\omega}+\frac{1-e^{i\omega}(1-i\omega)}{\omega^{2}}-\frac{e^{-i\omega}(1+i\omega)-1}{\omega^{2}} \\",
            r"&=\frac{i\omega(e^{-i\omega}-e^{i\omega})+1-e^{i\omega}(1-i\omega)-e^{-i\omega}(1+i\omega)+1}{\omega^{2}} \\",
            r"&=\frac{i\omega e^{-i\omega}-i\omega e^{i\omega}+1-e^{i\omega}+i\omega e^{i\omega}-e^{-i\omega}-i\omega e^{-i\omega}+1}{\omega^{2}} \\",
            r"&=\frac{2-e^{i\omega} - e^{-i\omega}}{\omega^{2}} \\",
            r"&=\frac{2-(e^{i\omega}+e^{-i\omega})}{\omega^{2}} \quad \\",
            r"\textrm{Using}& \quad 2\cos{\theta}=e^{i\theta}+e^{-i\theta} \ ; \\",
            r"&=\frac{2-2\cos{(\omega)}}{\omega^{2}} = 2\left[\frac{1-\cos{(\omega)}}{\omega^{2}}\right] \\",
            r"\textrm{Using}& \quad 1-\cos{\theta}=2\sin^{2}{\left( \frac{\theta}{2} \right) } \ ; \\",
            r"&=4\left\{ \frac{\sin^{2}{\left[ \pi \left( \frac{\omega}{2\pi} \right) \right]}}{4\left[ \pi \left( \frac{\omega}{2\pi} \right) \right]^{2} } \right\} \\",
            r"\textrm{Using}& \quad \textrm{sinc}^{2}(x)=\frac{\sin^{2}{(\pi x)}}{\pi x} \ ;\\",
            r"\therefore F(\omega)&=\textrm{sinc}^{2}\left( \frac{\omega}{2\pi} \right)"
        ).scale(0.7).shift(LEFT*2).shift(DOWN*2.5)
        ttt[0].shift(UP*0.8)
        ttt[0].set_color(YELLOW)

        self.play(Write(ttt[0], run_time=2))
        for i in range(1, 6):
            self.play(Write(ttt[i]), run_time=2)
        self.wait(3)
        self.play(FadeOut(ttt[1:5]), ttt[5].animate.shift(UP*4))
        ttt[6:].shift(UP*4)
        for i in range(6, 12):
            self.play(Write(ttt[i]), run_time=2)
        
        self.wait(3)

        fw_sr = SurroundingRectangle(ttt[-1], color=YELLOW)
        self.play(Create(fw_sr))

        self.wait(5)
        fw = VGroup(ttt[-1], fw_sr)
        self.play(FadeOut(ttt[0], ttt[5:-1], t1_sr, t1, t2, t3), fw.animate.shift(UP*6).shift(RIGHT))

        ax = Axes(
            (-12*PI, 12*PI, 2*PI), (-0.2, 1.2, 1),
            12, 6
        )
        xlabel = ax.get_x_axis_label(
            MathTex(r"\omega"),
            direction=DOWN,
            buff=1
        )
        label1 = Text("1").next_to(ax.c2p(0, 1), LEFT, buff=0.2)
        labelp1 = MathTex(r"2\pi").next_to(ax.c2p(2*PI, 0), DOWN, buff=0.2)
        labeln1 = MathTex(r"-2\pi").next_to(ax.c2p(-2*PI, 0), DOWN, buff=0.2)
        sinc_eq = ax.plot(lambda x: np.sinc(x/(2*PI))**2, color=BLUE)

        self.play(Create(ax), run_time=2)
        self.play(Write(sinc_eq), Write(xlabel), Write(label1), Write(labelp1), Write(labeln1), run_time=2)

        self.wait(10)
        self.play(FadeOut(ax, xlabel, label1, labelp1, labeln1, sinc_eq, fw))

        ft_pairs_img = ImageMobject("src/ft_pairs.png").shift(LEFT*2)
        self.play(FadeIn(ft_pairs_img), run_time=3)

        self.wait(10)
        self.play(FadeOut(tri, ft_pairs_img))



### Done in high quality
class UnitImpulse(Scene):
    def construct(self):
        self.wait(3)
        self.play_scene()
        self.wait(3)
    
    def play_scene(self):
        t = Title().shift(UP*3)
        mt = MathTex(r"\textrm{The Unit Impulse} \ - \ \delta (t)", color=RED).next_to(t, UP)
        t = VGroup(t, mt)

        self.play(Write(t))

        self.wait(5)

        ft = MathTex(
            r"F(\omega)&=\int_{-\infty}^{\infty} f(t)",
            r"e^{-i\omega t}",
            r"\ dt",
            color=YELLOW
        ).shift(UP)
        sc = MathTex(
            r"\cos{(\omega t)}-i\sin{(\omega t)}",
            color=RED
        )
        e = ft[1].copy()
        self.play(Write(ft), run_time=2)
        sr = SurroundingRectangle(ft[1], RED)
        self.play(Create(sr))
        self.play(ReplacementTransform(e, sc))

        self.wait(5)
        self.play(FadeOut(t, ft, sc, sr, e, shift=UP*3))
        
        _ddf = MathTex(
            r"\int_{a}^{b} \delta(\omega) \ d\omega &=\left\{ \begin{array}{rcl} 1 & \textrm{for} & a<0<b \\ 0 & & \textrm{otherwise} \end{array} \right.",
            color=BLUE
        )
        ddf_sr = SurroundingRectangle(_ddf, YELLOW)
        self.play(Write(_ddf), run_time=4)
        self.wait()
        self.play(Create(ddf_sr))
        ddf = VGroup(_ddf, ddf_sr)

        self.wait(5)
        self.play(ddf.animate.scale(0.7).shift(UP*3))

        ldt = NumberPlane(
            (-1, 1, 0.5), (0, 1.2, 1),
            5, 4,
            background_line_style={
                "stroke_opacity": 0.3
            },
            x_axis_config={
                "include_numbers": True
            }
        ).shift(DOWN*0.5).shift(LEFT*3.5)
        lylabel = ldt.get_y_axis_label(
            MathTex(r"\delta(\omega)", color=YELLOW).rotate(90*DEGREES),
            edge=LEFT,
            direction=LEFT*1.5,
        ).shift(LEFT*2)
        lxlabel = ldt.get_x_axis_label(
            MathTex(r"\textrm{Frequency} \ (\omega)", color=YELLOW),
            edge=DOWN,
            direction=DOWN*1.2
        )
        ldd_line = ldt.get_line_from_axis_to_point(
            0, ldt.c2p(0, 1),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        ldd_line_t = MathTex(r"\infty", color=RED).next_to(ldd_line, UP)
        lylabel1 = Tex("1").next_to(ldd_line, LEFT).shift(UP*1.7)


        rdt = NumberPlane(
            (-0.5, 1.5, 0.5), (0, 1.2, 1),
            5, 4,
            background_line_style={
                "stroke_opacity": 0.3
            },
            x_axis_config={
                "include_numbers": True
            }
        ).shift(DOWN*0.5).shift(RIGHT*4)
        rylabel = rdt.get_y_axis_label(
            MathTex(r"A\cdot \delta(\omega-0.5)", color=YELLOW).rotate(90*DEGREES),
            edge=LEFT,
            direction=LEFT*0.1,
        ).shift(LEFT*2)
        rxlabel = rdt.get_x_axis_label(
            MathTex(r"\textrm{Frequency} \ (\omega)", color=YELLOW),
            edge=DOWN,
            direction=DOWN*1.2
        )
        rdd_line = rdt.get_line_from_axis_to_point(
            0, rdt.c2p(0.5, 1),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        rdd_line_t = MathTex(r"\infty", color=RED).next_to(rdd_line, UP)
        rylabel1 = MathTex("A").next_to(rdd_line, LEFT*4.5).shift(UP*1.7)
        
        
        self.play(
            Create(ldt), Write(lylabel), Write(lxlabel),
            Create(rdt), Write(rylabel), Write(rxlabel),
            run_time=2
        )
        self.play(
            Create(ldd_line), Write(ldd_line_t),
            Create(rdd_line), Write(rdd_line_t),
            Write(lylabel1), Write(rylabel1),
            run_time=2
        )

        self.wait()
        note = MathTex(r"\textrm{*Values shown on y-axis are area.} \\ \textrm{Height}=\infty \quad \textrm{for both lines.}", color=YELLOW).scale(0.7).shift(RIGHT*3).shift(UP*3)
        note_sr = SurroundingRectangle(note, RED)
        note = VGroup(note, note_sr)

        self.play(ddf.animate.shift(LEFT*3.5), FadeIn(note), run_time=2)

        self.wait(10)
        self.play(FadeOut(note, ldt, lylabel, lylabel1, lxlabel, ldd_line, ldd_line_t, rdt, rylabel, rylabel1, rdd_line, rdd_line_t, ddf, rxlabel))

        ft = MathTex(r"f(t)=\cos{(5\pi t)} \quad \Longleftrightarrow \quad F(\pm5\pi)=\infty", color=YELLOW).scale(0.7)
        self.play(Write(ft))
        self.wait(5)
        self.play(ft.animate.shift(UP*3))

        fw = MathTex(
            r"F(\omega)&=\int_{-\infty}^{\infty} \cos{(5\pi t)} e^{-i\omega t} \ dt \\",
            r"\textrm{Using}& \quad \cos{x}=\frac{e^{i\omega}+e^{-ix}}{2} \ ; \\",
            r"F(\omega)&=\int_{-\infty}^{\infty}\left[ \frac{e^{i5\pi t}+e^{-i5\pi t}}{2}\right] e^{-i\omega t} \ dt \\",
            r"&=\int_{-\infty}^{\infty} \frac{1}{2} (e^{i5\pi t}+e^{-i5\pi t})e^{-i\omega t} \ dt \\",
            r"&=\frac{1}{2}\cdot \int_{-\infty}^{\infty}(e^{i5\pi t}\cdot e^{-i\omega t}+e^{-i5\pi t}\cdot e^{-i\omega t}) \ dt \\",
            r"&=\frac{1}{2}\left[ \int_{-\infty}^{\infty}e^{i5\pi t}\cdot e^{-i\omega t} \ dt+\int_{-\infty}^{\infty} e^{-i5\pi t}\cdot e^{-i\omega t} \ dt \right] \\ \\",
            r"\textrm{Using}& \quad e^{i\omega t} \quad \underleftrightarrow{ \ \ F \ \ } \quad 2\pi \delta(\omega - \omega_{0}) \ ; \\",
            r"F(\omega)&=\frac{1}{2}\left[ 2\pi \delta(\omega-5\pi)+2\pi\delta(\omega+5\pi) \right] \\ \\",
            r"&=\pi\left[\delta(\omega-5\pi)+\delta(\omega+5\pi)\right]"
        ).scale(0.7).shift(LEFT*2.5).shift(DOWN*2)
        fw[1].set_color(BLUE)
        fw[6].set_color(BLUE)

        for i in range(0, 6):
            self.play(Write(fw[i]), run_time=3)
            self.wait(0.5)
        self.wait(3)
        self.play(FadeOut(fw[1:5]), fw[5].animate.shift(UP*3.5))
        fw[6:].shift(UP*3.5)
        for i in range(6, 9):
            self.play(Write(fw[i]), run_time=3)
            self.wait(0.5)
        
        note = Tex(r"*The $F$ over the double arrow \\ denotes a Fourier Transform pair.", color=YELLOW).scale(0.7).shift(DOWN).shift(RIGHT*3)
        note_sr = SurroundingRectangle(note, RED)
        note = VGroup(note, note_sr)

        self.play(FadeIn(note))

        self.wait(5)
        self.play(FadeOut(fw[0], fw[5:-1], ft, note))
        ftr = MathTex(r"F(\omega)=\pi\left[\delta(\omega-5\pi)+\delta(\omega+5\pi)\right]", color=YELLOW).scale(0.7).shift(UP*3.5)
        self.play(ReplacementTransform(fw[-1], ftr))

        ax = NumberPlane(
            (-5, 5, 1), (-1, 4, 1),
            16, 8,
            tips=False,
            background_line_style={
                "stroke_opacity": 0.3
            },
            axis_config={
                "include_ticks": True
            }
        )
        xlabel = ax.get_x_axis_label(r"\omega")
        ylabel_pi = MathTex(r"\pi").next_to(ax.c2p(0, 3), LEFT)
        pline = ax.get_line_from_axis_to_point(
            0, ax.c2p(2, 3),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        pline_t = MathTex(r"\infty", color=RED).next_to(pline, UP)
        pline_l = MathTex(r"5\pi").next_to(pline, DOWN*1.3)
        nline = ax.get_line_from_axis_to_point(
            0, ax.c2p(-2, 3),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        nline_t = pline_t.copy().next_to(nline, UP)
        nline_l = MathTex(r"-5\pi").next_to(nline, DOWN*1.3)

        self.play(Create(ax), Write(xlabel), Write(ylabel_pi), run_time=2)
        self.play(
            Create(pline), Create(nline),
            Write(pline_t), Write(nline_t),
            Write(pline_l), Write(nline_l),
            run_time=2
        )

        self.wait(10)
        self.play(FadeOut(ftr, ax, xlabel, ylabel_pi, pline, pline_t, pline_l, nline, nline_t, nline_l))

        # ===== =====
        ftr1 = MathTex(r"f(t)=\sin{(5\pi t)}", color=BLUE).scale(0.7).shift(UP*3.5).shift(LEFT*5)
        ftr2 = MathTex(r"F(\omega)=i\pi\left[\delta(\omega+5\pi)-\delta(\omega-5\pi)\right]", color=YELLOW).scale(0.7).shift(UP*3.5).shift(RIGHT*3.5)
        self.play(FadeIn(ftr1, ftr2, shift=UP*3), run_time=2)

        ax = NumberPlane(
            (-7, 7, 1), (-4, 4, 1),
            16, 8,
            tips=False,
            background_line_style={
                "stroke_opacity": 0.3
            },
            axis_config={
                "include_ticks": True
            }
        )
        xlabel = ax.get_x_axis_label(r"\omega")
        pline = ax.get_line_from_axis_to_point(
            0, ax.c2p(2, -3),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        pline_t = MathTex(r"-\infty", color=RED).next_to(pline, DOWN)
        pline_l = MathTex(r"5\pi").next_to(pline, UP*1.3)
        nline = ax.get_line_from_axis_to_point(
            0, ax.c2p(-2, 3),
            color=RED,
            line_func=Arrow,
            line_config={
                'buff': 0
            }
        )
        nline_t = MathTex(r"\infty", color=RED).next_to(nline, UP)
        nline_l = MathTex(r"-5\pi").next_to(nline, DOWN*1.3)

        ylabel_ppi = MathTex(r"\pi").next_to(ax.c2p(0, 3), LEFT)
        ylabel_npi = MathTex(r"-\pi").next_to(ax.c2p(0, -3), LEFT)

        self.play(Create(ax), Write(xlabel), Write(ylabel_ppi), Write(ylabel_npi), run_time=2)
        self.play(
            Create(pline), Create(nline),
            Write(pline_t), Write(nline_t),
            Write(pline_l), Write(nline_l),
            run_time=2
        )

        self.wait(15)
        self.play(FadeOut(ftr1, ftr2, ax, xlabel, pline, pline_t, pline_l, nline, nline_t, nline_l, ylabel_ppi, ylabel_npi))




class FilteringSound(Scene):
    def construct(self):
        self.wait(3)
        self.play_scene()
        self.wait(3)

    def play_scene(self):
        t = Title("Filtering Sound", color=RED)
        self.play(Write(t), run_time=2)

        #