# ASSUMPTION rung1 is closer to the origin than rung2

from math import dist, sqrt
from sympy import symbols, solve
from data_structures import Segment
from rung import Rung
def toTuple(vec):
    return vec.tolist()

#points as tuples
def heron_area(p1, p2, p3):
    a = dist(p1, p2)
    b = dist(p2, p3)
    c = dist(p3, p1)
    s = (a + b + c) / 2
    # try:
    return sqrt(s * (s - a) * (s - b) * (s - c))
    # except:
    #     print('shapes.py  heron_area() sqrt math domain error(sqr root of neg number)')
    #     breakpoint()

def two_rungs_sympy_expression(r1, r2, origin, rung1, rung2):
    a = dist(rung1.a, rung2.a) / dist(origin, rung1.a)
    b = dist(rung1.b, rung2.b) / dist(origin, rung1.b)

    e = (a+1) / (1-1/((b+1)/(1-r2)-b)) - a - 1/r1
    return e

class Quadrilateral:
    def __init__(self, rung1, rung2):
        self.rung1 = rung1
        self.rung2 = rung2
        self.tup = [toTuple(p) for p in[rung1.a, rung1.b, rung2.b, rung2.a]]
        # try:
        self.area = (
            heron_area(*[toTuple(p) for p in[*rung1, rung2.a]]) +
            heron_area(*[toTuple(p) for p in[*rung2, rung1.b]])
        )
    def gen_sympy_area_expression(self, r0, origin, rung0):
        rung_mid = Rung(origin, Segment(self.rung1.a, self.rung2.b))
        tr1 = Triangle(self.rung1, rung_mid)
        tr2 = Triangle(rung_mid, self.rung2)

        self.sympy_area_expresssion = (
            tr1.gen_sympy_area_expression(r0, origin, rung0) +
            tr2.gen_sympy_area_expression(r0, origin, rung0)
        )

        return self.sympy_area_expresssion
        # except:
        #     breakpoint()

#TODO store data for future calculations
#assumes rungs have 1 point in common
class Triangle:
    def __init__(self, rung1, rung2):
        self.rung1 = rung1
        self.rung2 = rung2
        comp = rung1.segment & rung2.segment
        
        self.common_point_on_ray1 = comp is rung1.a
        
        points = [*rung1.segment] + [*rung2.segment]
        self.tup = [comp.tolist()] + [p.tolist() for p in points if p is not comp]
        self.area = heron_area(*self.tup)
        # print(self.tup)
    def gen_sympy_area_expression(self, r0, origin, rung0):
        r2 = symbols('r2')
        r1 = symbols('r1')
        e0 = two_rungs_sympy_expression(r0, r1, origin, rung0, self.rung1)
        r1_of_r0 = solve(e0, r1)[0]

        if not self.common_point_on_ray1:
            a = dist(self.rung1.a, self.rung2.a) / dist(origin, self.rung1.a)
            e1 = (a+1)/r2 - a - 1/r1
            r2_of_r1 = solve(e1, r2)[0]
            r2_of_r0 = r2_of_r1.subs(r1, r1_of_r0)

            ar1 = heron_area(origin, *self.rung1)
            ar2 = heron_area(origin, *self.rung2)
            self.sympy_area_expression = ar2 * r2_of_r0 - ar1 * r1_of_r0
        else :
            a = dist(self.rung1.b, self.rung2.b) / dist(origin, self.rung1.b)
            e1 = (a+1)/(1-r2) - a - 1/(1-r1)
            r2_of_r1 = solve(e1, r2)[0]
            r2_of_r0 = r2_of_r1.subs(r1, r1_of_r0)

            ar1 = heron_area(origin, *self.rung1)
            ar2 = heron_area(origin, *self.rung2)
            self.sympy_area_expression = ar2 * r2_of_r0 - ar1 * r1_of_r0
            # inv_triangle = Triangle()
        return self.sympy_area_expression
    

class Origin_Triangle:
    def __init__(self, origin, rung):
        self.origin = origin
        self.rung = rung
        self.tup = [toTuple(p) for p in [origin, *rung]]
        self.area = heron_area(*self.tup)

    def sp_area_expression(self, r0, origin = None, rung0 = None):
        return self.area * r0