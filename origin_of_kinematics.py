#######################################################
# special thanks : 3b1b/manim
# Author : Sanjeev
#######################################################

from big_ol_pile_of_manim_imports import *
import numpy as np
from scipy.integrate import odeint
class Intro_scene(Scene):
    def construct(self):
        background_square=Square(side_length=20,fill_color=WHITE, fill_opacity=1)
        self.add(background_square)

        example_text = TextMobject(
            "ORIGINS of KINEMATICS",color=BLUE,background_stroke_color=BLUE
        )
        example_tex = TextMobject(
            "Physics",color=RED,background_stroke_color=RED
        )
        group = VGroup(example_text,example_tex)
        group.arrange_submobjects(DOWN)
        group.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)
        group.move_to(2*UP)

        self.play(FadeIn(example_text))
        self.wait(1)
        self.play(FadeIn(example_tex))
        self.wait(2)
class SimplePendulum(VMobject):
    CONFIG = {
        "buff": 0.5,
        "start_angles": [PI / 6],
        "color1": RED,
    }

    def __init__(self,pos=ORIGIN,length=2,mass_of_bob=1,gravity=9.81,damping=0, **kwargs):
        VMobject.__init__(self, **kwargs)
        line1 = Line(ORIGIN, UP,stroke_width=1,stroke_color=BLACK)
        dot1 = Dot(color=self.color1).scale(1.5)
        dot1.add_updater(lambda d: d.move_to(line1.get_end()))

        self.add(line1, dot1)
        self.L1 = length
        self.m1 = mass_of_bob
        self.c = gravity/length
        self.b = damping
        self.g = gravity
        self.time=0
        self.time_list = []
        def update(group, dt):
            self.time+=dt
            y0 = [np.pi/12, 0.0]
            line1 = group.submobjects[0]
            self.time_list.append(self.time)
            sol = odeint(deriv, y0, self.time_list, args=(self.b, self.c))
            p1 = np.sin(sol[-1, 0])* RIGHT * 2 + np.cos(sol[-1, 0]) * DOWN * 2
            line1.put_start_and_end_on(pos, pos+p1)

        def deriv(y, t, b, c):
            theta, omega = y
            dydt = [omega, -b*omega - c*np.sin(theta)]
            return dydt
        self.add_updater(update)
