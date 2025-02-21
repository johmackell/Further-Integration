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


class HistoryOfIntegration(Scene):
    def construct(self):
        self.my_scene()
    
    def my_scene(self):
        self.wait(2)
        self.pol_v = ValueTracker(8)
        pol5 = RegularPolygon(5, color=BLUE).scale(2)
        pol5s = pol5.copy().set_fill(BLUE_C, 0.8).scale(0.8).shift(DOWN*0.1)
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
        self.play(cir5.animate.shift(LEFT*3).scale(0.5).shift(UP*0.1), pol5.animate.shift(LEFT*3).scale(0.5), pol5s.animate.shift(LEFT*3).scale(0.5), pol5t.animate.shift(LEFT*3).shift(UP*0.8), rate_func=linear)

        self.play(FadeIn(self.pol_vg))

        self.play(self.pol_v.animate.set_value(20), run_time=5, rate_func=linear)

        self.wait(5)
        self.play(FadeOut(self.pol_vg, pol5, pol5s, pol5t, cir5))

        #



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



