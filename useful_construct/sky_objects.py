from big_ol_pile_of_manim_imports import *
import numpy as np
from scipy.integrate import odeint
from itertools import tee

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
        self.count=0
        def update(group, dt):
            self.time+=dt
            y0 = [np.pi/12, 0.0]
            line1 = group.submobjects[0]
            self.time_list.append(self.time)
            if self.count<3:
                self.count+=1
            sol = odeint(deriv, y0, self.time_list, args=(self.b, self.c))
            p1 = np.sin(sol[-1, 0])* RIGHT * 2 + np.cos(sol[-1, 0]) * DOWN * 2
            line1.put_start_and_end_on(pos, pos+p1)

        def deriv(y, t, b, c):
            theta, omega = y
            dydt = [omega, -b*omega - c*np.sin(theta)]
            return dydt
        self.add_updater(update)

class Satellite(VMobject):
    CONFIG = {
	"normal_vector_color":RED
	"tangent_vector_color":RED
	

    }

    def __init__(self,radius=2,planet_pos=ORIGIN,add_tangent=True, **kwargs):
        VMobject.__init__(self, **kwargs)
        Satellite = SVGMobject(file_name="satellite.svg").scale(0.25)
        Planet= ImageMobject("earth_2.png").scale(0.25)
        Planet.move_to(planet_pos)
        planet_center=Planet.get_center()
        Satellite.move_to(planet_center+UP)
        self.add(Satellite,Planet)

        if add_tangent:
            n=TexMobject()
            normal_vector=Line(LEFT,RIGHT,stroke_width=1,color=self.normal_vector_color)
            tangent_vector=Arrow(ORIGIN,RIGHT,stroke_width=0.25,color=self.tangent_vector_color)
            self.add(normal_vector,tangent_vector)
        self.count=0

        def perpendicular( a ) :
            b = np.empty_like(a)
            b[0] = -a[1]
            b[1] = a[0]
            return b

        def normalize(a):
            a = np.array(a)
            return a/np.linalg.norm(a)

        def update(group, dt):
            satellite_obj = group.submobjects[0]
            planet_obj = group.submobjects[1]
            self.count+=dt
            new_point=rotate(UP*radius, angle=TAU*0.2*self.count, axis=OUT)+planet_obj.get_center()
            if add_tangent:
                tan_vec,norm_vec=group.submobjects[-1],group.submobjects[-2]
                norm_vec.put_start_and_end_on(planet_obj.get_center(),new_point)
                tan_vec.put_start_and_end_on(new_point,new_point+normalize(perpendicular(new_point-planet_obj.get_center()))/2)
            satellite_obj.move_to(new_point)

        self.add_updater(update)

class Star_groups():
    def __init__(self,*points, **kwargs):
        self.points=[*points]

    def get_lines(self,start,end):
        return Line(start,end,stroke_width=0.3)

    def get_dots(self,point):
        return Dot().scale(0.5).move_to(point)

    def Aries(self,connecting_lines_check=False):
        self.points=[ORIGIN,RIGHT*1.25+0.15*UP,1.875*RIGHT+1.2*DOWN,1.9*RIGHT+1.725*DOWN,1.8*RIGHT+1.9*DOWN]
        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
            
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Tarus(self,connecting_lines_check=False):
        self.points=[np.array([3.28765832,5.30851252,0.]),
                     np.array([5.45932253,9.41054492,0.]),
                     np.array([ 6.1228866,10.40589102,0.]),
                     np.array([6.30385862,9.83281296,0.]),
                     np.array([6.36418262,9.1994109 ,0.]),
                     np.array([5.51964654,4.40365243,0.])]

        points_2=[np.array([6.36418262,9.1994109 ,0.]),
                  np.array([9.53119293,9.95346097,0.])]

        points_3=[np.array([ 6.1228866,10.40589102,0.]),
                  np.array([ 6.54515464,11.97431517,0.]),
                  np.array([ 7.93260677,14.11581738,0.])]

        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots).scale(2))
        for dots in points_2[1:]:
            stars.append(self.get_dots(dots).scale(2))
        for dots in points_3[1:]:
            stars.append(self.get_dots(dots).scale(2))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_2):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_3):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Gemini(self,connecting_lines_check=False):
        self.points=[np.array([2.63328424, 3.59351988, 0.]),
                     np.array([1.39027982, 3.15169367, 0.]),
                     np.array([1.23122239, 2.34462445, 0.]),
                     np.array([1.80265096, 2.48600884, 0.]),
                     np.array([2.81590574, 2.95729013, 0.])]

        points_2=[np.array([3.03976436, 2.33284242, 0.]),
                  np.array([2.40942563, 1.73195876, 0.]),
                  np.array([3.15758468, 1.95581738, 0.]),
                  np.array([3.42857143, 1.90279823, 0.]),
                  np.array([3.79381443, 1.71428571, 0.])]

        points_3=[np.array([0.34756996, 2.05007364, 0.]),
                  np.array([0.60677467, 1.65537555, 0.]),
                  np.array([0.97201767, 1.4904271 , 0.]),
                  np.array([1.40206186, 1.09572901, 0.]),
                  np.array([1.89690722, 0.45949926, 0.])]

        points_4=[np.array([0.28276878, 1.50220913, 0.]),
                  np.array([0.60677467, 1.65537555, 0.])]

        points_5=[np.array([0.60088365, 0.90721649, 0.]),
                  np.array([1.40206186, 1.09572901, 0.])]

        points_6=[np.array([1.23122239, 2.34462445, 0.]),
                  np.array([0.60677467, 1.65537555, 0.])]

        points_7=[np.array([2.40942563, 1.73195876, 0.]),
                  np.array([1.40206186, 1.09572901, 0.])]

        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots))
        for dots in points_2:
            stars.append(self.get_dots(dots))
        for dots in points_3:
            stars.append(self.get_dots(dots))
        for dots in points_4[:1]:
            stars.append(self.get_dots(dots))
        for dots in points_5[:1]:
            stars.append(self.get_dots(dots))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_2):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_3):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_4):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_5):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_6):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_7):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Cancer(self,connecting_lines_check=False):
        self.points=[np.array([3.34451613, 0.77419355, 0.]),
                     np.array([4.61419355, 2.35354839, 0.]),
                     np.array([5.07870968, 3.15870968, 0.]),
                     np.array([5.20258065, 5.14064516, 0.])]

        points_2=[np.array([4.61419355, 2.35354839, 0.]),
                  np.array([4.92387097, 0.21677419, 0.])]

        points_3=[np.array([5.07870968, 3.15870968, 0.]),
                  np.array([8.02064516, 4.14967742, 0.])]

        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots).scale(2))
        for dots in points_2[1:]:
            stars.append(self.get_dots(dots).scale(2))
        for dots in points_3[1:]:
            stars.append(self.get_dots(dots).scale(2))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_2):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_3):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Leo(self,connecting_lines_check=False):
        self.points=[np.array([1.56038095, 4.94120635, 0.]),
                     np.array([2.3568254 , 3.65714286, 0.]),
                     np.array([4.11225397, 2.95822222, 0.]),
                     np.array([4.71365079, 3.15326984, 0.]),
                     np.array([4.98996825, 3.83593651, 0.]),
                     np.array([2.66565079, 4.35606349, 0.]),
                     np.array([1.56038095, 4.94120635, 0.])]

        points_2=[np.array([4.11225397, 2.95822222, 0.]),
                  np.array([3.96596825, 2.4055873 , 0.]),
                  np.array([4.53485714, 1.64165079, 0.]),
                  np.array([4.90869841, 1.80419048, 0.])]

        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots))
        for dots in points_2[1:]:
            stars.append(self.get_dots(dots))

        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_2):
            connecting_lines.append(self.get_lines(*line))

        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Virgo(self,connecting_lines_check=False):
        self.points=[np.array([0.76393651, 4.42107937, 0.]),
                     np.array([1.77168254, 4.74615873, 0.]),
                     np.array([2.69815873, 5.46133333, 0.]),
                     np.array([3.72215873, 4.87619048, 0.]),
                     np.array([4.51860317, 4.77866667, 0.]),
                     np.array([5.60761905, 4.42107937, 0.])]

        points_2=[np.array([2.69815873, 5.46133333, 0.]),
                  np.array([2.13739683, 6.30653968, 0.])]

        points_3=[np.array([3.72215873,4.87619048,0.]),
                  np.array([3.2264127 ,4.19352381,0.]),
                  np.array([2.98260317,3.072,0.])]

        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots))
        for dots in points_2[1:]:
            stars.append(self.get_dots(dots))
        for dots in points_3[1:]:
            stars.append(self.get_dots(dots))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_2):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_3):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Libra(self,connecting_lines_check=False):
        self.points=[np.array([3.36571429, 4.95085714,0.]),
                     np.array([4.04428571, 3.11057143,0.]),
                     np.array([4.91828571, 2.584     ,0.]),
                     np.array([5.43942857, 3.82171429,0.]),
                     np.array([4.53828571, 4.90742857,0.])]

        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots))

        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise([self.points[1],self.points[3]]):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Scorpio(self,connecting_lines_check=False):
        self.points=[np.array([1.86813187, 1.68956044, 0.]),
                     np.array([1.71978022, 1.57142857, 0.]),
                     np.array([1.29120879, 1.76648352, 0.]),
                     np.array([0.87362637, 1.92032967, 0.]),
                     np.array([1.08791209, 2.4532967 , 0.]),
                     np.array([1.87637363, 2.85164835, 0.]),
                     np.array([2.54945055, 2.93131868, 0.]),
                     np.array([2.81318681, 2.3543956 , 0.]),
                     np.array([3.03571429, 1.78571429, 0.]),
                     np.array([3.76923077, 1.18681319, 0.]),
                     np.array([4.06593407, 0.9478022 , 0.]),
                     np.array([4.42032967, 0.9532967 , 0.]),
                     np.array([5.13186813, 0.2032967 , 0.]),]

        points_2=[np.array([4.42032967, 0.9532967 , 0.]),
                  np.array([5.3489011 , 0.35989011, 0.])]

        points_3=[np.array([4.42032967, 0.9532967 , 0.]),
                  np.array([5.32967033, 0.87912088, 0.])]
        
        points_4=[np.array([4.42032967, 0.9532967 , 0.]),
                  np.array([5.13461538, 1.40384615, 0.])]
        
        points_5=[np.array([4.42032967, 0.9532967 , 0.]),
                  np.array([4.98901099, 1.84065934, 0.])]
        
        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots))
        for dots in points_2[1:]:
            stars.append(self.get_dots(dots))
        for dots in points_3[1:]:
            stars.append(self.get_dots(dots))
        for dots in points_4[1:]:
            stars.append(self.get_dots(dots))
        for dots in points_5[1:]:
            stars.append(self.get_dots(dots))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_2):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_3):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_4):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_5):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Sagittarius(self,connecting_lines_check=False):
        self.points=[np.array([1.0707511 , 2.26592047, 0]),
                     np.array([1.21025037, 2.23952872, 0]),
                     np.array([1.28565538, 2.15281296, 0]),
                     np.array([1.41761414, 2.0057732 , 0]),
                     np.array([1.45908689, 1.91151694, 0]),
                     np.array([1.40253314, 1.79840943, 0]),
                     np.array([1.78332842, 1.71923417, 0]),
                     np.array([1.82103093, 1.5571134 , 0]),
                     np.array([1.68907216, 1.26680412, 0]),
                     np.array([2.0208542 , 1.13107511, 0]),
                     np.array([2.37148748, 1.18008837, 0]),
                     np.array([2.5524595, 1.0707511, 0])]

        points_2=[np.array([1.92282769, 2.77113402, 0.]),
                  np.array([1.75693667, 2.42050074, 0.]),
                  np.array([1.70415317, 2.23952872, 0.]),
                  np.array([1.73808542, 2.06232695, 0.]),
                  np.array([1.90397644, 1.90397644, 0.]),
                  np.array([2.0585567 , 1.82103093, 0.]),
                  np.array([2.88424153, 2.04724595, 0.]),
                  np.array([3.18209131, 1.99069219, 0.])]

        points_3=[np.array([1.78332842, 1.71923417, 0]),
                  np.array([1.90397644, 1.90397644, 0.])]
        
        points_4=[np.array([1.68907216, 1.26680412, 0]),
                  np.array([1.34597938, 1.01419735, 0.])]
        
        points_5=[np.array([2.0208542 , 1.13107511, 0]),
                  np.array([2.06986745, 0.87469809, 0.])]
        
        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots).scale(0.7))
        for dots in points_2:
            stars.append(self.get_dots(dots).scale(0.7))
        for dots in points_4[1:]:
            stars.append(self.get_dots(dots).scale(0.7))
        for dots in points_5[1:]:
            stars.append(self.get_dots(dots).scale(0.7))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_2):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_3):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_4):
            connecting_lines.append(self.get_lines(*line))
        for line in self.pairwise(points_5):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Capricorn(self,connecting_lines_check=False):
        self.points=[np.array([3.27645066, 1.25416789, 0.        ]),
                     np.array([3.17319588, 1.40275405, 0.        ]),
                     np.array([2.97172312, 1.59163476, 0.        ]),
                     np.array([2.53351988, 2.05502209, 0.        ]),
                     np.array([2.40759941, 2.13561119, 0.        ]),
                     np.array([2.18849779, 1.94421208, 0.        ]),
                     np.array([1.8963623 , 1.68733432, 0.        ]),
                     np.array([1.65963181, 1.37001473, 0.        ]),
                     np.array([1.61430044, 1.15343152, 0.        ]),
                     np.array([1.7377025 , 1.21639175, 0.        ]),
                     np.array([2.05502209, 1.28942563, 0.        ]),
                     np.array([2.33708395, 1.38008837, 0.        ]),
                     np.array([3.17319588, 1.40275405, 0.        ])]
        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots).scale(0.7))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
            
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def Aquarius(self,connecting_lines_check=False):
        self.points=[np.array([3.32159057, 2.14904271, 0.]),
                     np.array([2.88047128, 1.72300442, 0.]),
                     np.array([2.20559647, 1.38368189, 0.]),
                     np.array([1.91528719, 1.4967894 , 0.]),
                     np.array([1.77578792, 1.40630339, 0.]),
                     np.array([1.65136966, 1.43269514, 0.]),
                     np.array([1.40253314, 2.0208542 , 0.]),
                     np.array([0.96518409, 2.20559647, 0.]),
                     np.array([0.58815906, 2.66933726, 0.]),
                     np.array([0.65602356, 2.91063328, 0.]),
                     np.array([0.96141384, 3.0614433 , 0.]),
                     np.array([1.24795287, 3.0388218 , 0.]),
                     np.array([1.50810015, 2.45066274, 0.]),
                     np.array([2.04724595, 1.96430044, 0.]),
                     np.array([2.20559647, 1.38368189, 0.])]
        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots).scale(0.7))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
            
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
    def Pisces(self,connecting_lines_check=False):
        self.points=[ np.array([0.71634757, 1.19139912, 0.]),
                      np.array([0.55045655, 1.56842415, 0.]),
                      np.array([0.76159057, 1.75693667, 0.]),
                      np.array([1.17631811, 2.0359352 , 0.]),
                      np.array([1.56088365, 2.48836524, 0.]),
                      np.array([1.44023564, 3.63452135, 0.]),
                      np.array([1.51564065, 4.69019146, 0.]),
                      np.array([1.52318115, 5.78356406, 0.]),
                      np.array([1.73431517, 5.59505155, 0.]),
                      np.array([1.92282769, 5.074757  , 0.]),
                      np.array([2.22444772, 4.77313697, 0.]),
                      np.array([2.63163476, 4.35086892, 0.]),
                      np.array([2.91817378, 4.00400589, 0.]),
                      np.array([3.38568483, 3.74762887, 0.]),
                      np.array([4.98427099, 2.80506627, 0.]),
                      np.array([5.72324006, 2.52606775, 0.]),
                      np.array([6.07010309, 2.13396171, 0.]),
                      np.array([6.43204713, 2.0736377 , 0.]),
                      np.array([6.71104566, 2.27723122, 0.]),
                      np.array([6.54515464, 2.78998527, 0.]),
                      np.array([5.98715758, 3.0614433 , 0.]),
                      np.array([5.72324006, 2.52606775, 0.])]
        stars=[]
        connecting_lines=[]
        for dots in self.points:
            stars.append(self.get_dots(dots).scale(1.6))
        for line in self.pairwise(self.points):
            connecting_lines.append(self.get_lines(*line))
        if connecting_lines_check:
            return VGroup(*stars,*connecting_lines).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)
        else:
            return VGroup(*stars).move_to(ORIGIN).scale(0.5).rotate(180*DEGREES).flip(UP)

    def zodiac_group(self,connecting_lines_check=False):
        if connecting_lines_check:
            zodiacs=[self.Aries(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Tarus(connecting_lines_check=True).set_width(1.5).set_height(1.5),
                     self.Gemini(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Cancer(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Leo(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Virgo(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Libra(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Scorpio(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Sagittarius(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Capricorn(connecting_lines_check=True).set_width(0.5).set_height(0.5),
                     self.Aquarius(connecting_lines_check=True).set_width(1).set_height(1),
                     self.Pisces(connecting_lines_check=True).set_width(1).set_height(1)]
        else:
            zodiacs=[self.Aries().set_width(1).set_height(1),
                     self.Tarus().set_width(1.5).set_height(1.5),
                     self.Gemini().set_width(1).set_height(1),
                     self.Cancer().set_width(1).set_height(1),
                     self.Leo().set_width(1).set_height(1),
                     self.Virgo().set_width(1).set_height(1),
                     self.Libra().set_width(1).set_height(1),
                     self.Scorpio().set_width(1).set_height(1),
                     self.Sagittarius().set_width(1).set_height(1),
                     self.Capricorn().set_width(0.5).set_height(0.5),
                     self.Aquarius().set_width(1).set_height(1),
                     self.Pisces().set_width(1).set_height(1)]
        theta = np.radians(0)
        for cluster in zodiacs:
            theta+=np.radians(30)
            c, s = np.cos(theta), np.sin(theta)
            Rotation_Matrix = np.array(((c,-s, 0), (s, c, 0),(0,0,1)))
            cluster.move_to(np.matmul(Rotation_Matrix,3*UP.T))
        return VGroup(*zodiacs)

    def pairwise(self,iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

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
