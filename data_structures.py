
from math import pi
from functools import cmp_to_key
# 
import numpy as np

np.seterr(all='raise')


from segment import Segment
from ray import Ray
from shapes import Origin_Triangle, Quadrilateral, Triangle
from rung import Rung

from sympy import symbols, solve, solveset, Interval, init_printing

init_printing(use_unicode=True)

total_calculations = [0, 0]

def toTuple(vec):
    return vec.tolist()

##TODO perhaps a faster solution exists
# py-spy total time is not constant, depends on some other factor
# length of vector
def modulo(a):
    # global total_calculations
    # total_calculations[1] += 1
    return np.linalg.norm(a)

def unit(a):
    return a / modulo(a)


class Slice():
    opposite = None
    next = None
    previous = None
    _is_empty = None

    def __init__(self, ray1, ray2):
        self.origin = ray1.origin
        self.ray1 = ray1
        self.ray2 = ray2

        self.gen_rungs()
        self.origin_inside_poly = (len(self.rungs) % 2 == 1)
        self.gen_shapes()
        self._is_empty = (self.shapes == [])
        self.calculate_area()
        # self.segments = [r.segment for r in self.rungs]

    @property
    def is_empty(self):
        return self._is_empty
    
    def gen_rungs(self):
        self.rungs = []
        self.original_poly_segments = []

        r1int = self.ray1.intersections
        r2int = self.ray2.intersections

        r1seg = {i.segment for i in self.ray1.intersections}
        r2seg = {i.segment for i in self.ray2.intersections}

        common_segments = r1seg & r2seg

        for cseg in common_segments:
            for i in r1int:
                if i.segment is cseg:
                    int1 = i
                    break
            for i in r2int:
                if i.segment is cseg:
                    int2 = i
                    break

            self.rungs.append(Rung(self.origin, Segment(int1.point, int2.point)))
            self.original_poly_segments += [cseg]


        def compare_seg_origin_distance(rung1, rung2):
            if rung1 is rung2:
                return 0
            
            # l(True) -> 1
            # l(False) -> -1
            l = lambda b: int(b) * 2 - 1
            
            if rung1.ray1.poly_vertex is rung2.ray1.poly_vertex:
                return l(modulo(rung1.ray2.direction) > modulo(rung2.ray2.direction))
            elif rung1.ray2.poly_vertex is rung2.ray2.poly_vertex:
                return l(modulo(rung1.ray1.direction) > modulo(rung2.ray1.direction))
            else:
                return l(modulo(rung1.ray1.direction) > modulo(rung2.ray1.direction))
            

        self.rungs.sort(key = cmp_to_key(compare_seg_origin_distance))

    def shape_from_rungs(self, rung1, rung2):
        common = rung1.segment & rung2.segment
        if common is None:
            return Quadrilateral(rung1, rung2)
        else:
            return Triangle(rung1, rung2)

    #TODO implement for origin on polygon
    def gen_shapes(self):
        self.shapes = []

        rungs = self.rungs
        if self.origin_inside_poly:
            self.shapes.append(Origin_Triangle(self.origin, rungs[0]))
            for rung1, rung2 in zip(rungs[1::2], rungs[2::2]):
                self.shapes += [self.shape_from_rungs(rung1, rung2)]
        else:
            for rung1, rung2 in zip(rungs[0::2], rungs[1::2]):
                self.shapes += [self.shape_from_rungs(rung1, rung2)]

    def calculate_area(self):
        self.area = 0
        for shape in self.shapes:
            self.area += shape.area

    def divide_using_vector(self, v):
        div_ray = Ray(self.origin, direction = v)
        div_ray.intersect_segments(self.original_poly_segments)
        
        sub_slice1 = Slice(self.ray1, div_ray)
        sub_slice2 = Slice(div_ray, self.ray2)
        return sub_slice1, sub_slice2

    def divide_using_ratio(self, ratio):
        # print('\ndivide by ratio ---------------- ')
        # print(f'slice area: {self.area}')
        # print(f'r: {ratio}')

        self.rlist = []
        r = ratio
        ACCURACY = 0.0000000001
        bound2_vec = unit(self.ray2.direction)
        bound1_vec = unit(self.ray1.direction)
        div_vector = unit(bound1_vec + bound2_vec)
        sub_slice1, sub_slice2 = self.divide_using_vector(div_vector)
        cy = 0
        while abs(self.area * r - sub_slice1.area) >= ACCURACY:
            self.rlist.append(Ray(self.origin, direction = div_vector))
            cy += 1
            if r * self.area > sub_slice1.area:
                bound1_vec = div_vector
            else:
                bound2_vec = div_vector
            div_vector = unit(unit(bound1_vec) + unit(bound2_vec))
            div_ray = Ray(self.origin, direction = div_vector)
            div_ray.intersect_segments(self.original_poly_segments)
            sub_slice1, sub_slice2 = self.divide_using_vector(div_vector)

        # print(f'max error: {ACCURACY}')
        # print(f'iterations to converge: {cy}')

        return sub_slice1, sub_slice2, div_vector

    def gen_rung_0(self):
        if type(self.shapes[0]) == Origin_Triangle:
            self.rung0 = self.shapes[0].rung
        else:
            self.rung0 = self.shapes[0].rung1

    def divide_using_ratio_expression(self, ratio):
        self.math_ray_list = []

        r0 = symbols('r0')
        self.gen_rung_0()
        
        e = 0
        for shape in self.shapes:
            e += shape.gen_sympy_area_expression(r0, self.origin, self.rung0)
            # print(shape)

        e = e - self.area * ratio
        # print(e)
        solutions = solveset(e, r0, Interval(0, 1))
        solutions = list(solutions)
        # print(f'r0 solutions: {solutions}')
        direction_vector = self.direction_vector_from_r0(solutions[0])
        self.math_ray_list.append(Ray(self.origin, direction=direction_vector))

        sub_slice1, sub_slice2 = self.divide_using_vector(direction_vector)
        return sub_slice1, sub_slice2, direction_vector

    def direction_vector_from_r0(self, r0):
        # print(f'r0passed: {r0}')
        self.gen_rung_0()
        dir = self.rung0.segment.c * float(r0) + self.rung0.a - self.origin
        # print(unit(self.rung0.segment.c * float(1-r0) + self.rung0.a))
        return unit(dir)


# ??? why did i make this
class UncutPizzaSlices :
    def __init__(self, slices):
        self.slices = slices
        self.shapes = [shape for slice in slices for shape in slice.shapes]
        self.area = sum([slice.area for slice in slices])

    def does_ray_intersect(self, ray):
        for slice in self.slices:
            if ray.intersects_slice(slice):
                return True
        return False

class Bowtie :
    def __init__(self, slice1, slice2):
        if not (slice1.origin == slice2.origin).all():
            raise RuntimeError('the origins must be the same')
        self.area = slice1.area + slice2.area
        self.area1 = slice1.area
        self.area2 = slice2.area
        self.slice2 = slice2
        self.slice1 = slice1
        self.origin = slice1.origin

    def divide_using_vector(self, vec):
        s1a, s1b = self.slice1.divide_using_vector(vec)
        s2a, s2b = self.slice2.divide_using_vector(-vec)

        b1 = Bowtie(s1a, s2a)
        b2 = Bowtie(s1b, s2b)
        return b1, b2

class Division:
    rung0 = None
    def __init__(self, ray, slices1, slices2, index):
        self.ray = ray # ray is only used for display purposes
        self.index = index

        self.slices1 = slices1
        self.slices2 = slices2

        self.cut_slice_1 = slices1[0]
        self.cut_slice_2 = slices2[0] #TODO is this correct?

        self.pizza1 = UncutPizzaSlices(slices1)
        self.pizza2 = UncutPizzaSlices(slices2)

        self.shapes1 = self.pizza1.shapes
        self.shapes2 = self.pizza2.shapes

        self.area1 = self.pizza1.area
        self.area2 = self.pizza2.area

        self.total_area = self.area1 + self.area2
        self.half_area = self.total_area / 2

        self.bowtie = Bowtie(self.cut_slice_1, self.cut_slice_2)

        self.math_ray_list = []

    def gen_socialised_division(self):
        # print (self.cut_slice_1.is_empty, self.cut_slice_2.is_empty)
        
        if self.cut_slice_1.is_empty + self.cut_slice_2.is_empty == 1:
            if self.cut_slice_1.is_empty:
                return None
            slice = self.slices1[0]
            # try:
            r = (self.half_area - self.area2) / slice.area
            # except:
            #     breakpoint(0)
            sub_slice1, sub_slice2, d_1 = slice.divide_using_ratio(r)
            _, _, d_2 = slice.divide_using_ratio_expression(r)
            # print('2 division vectors!!! '+'-'*10)
            print('\ndivision ray orientation')
            print(f'solution 1: {d_1}')
            print(f'solution 2: {d_2}')
            # print(d_1, d_2)
            socialised_div = Division(
                None,
                self.slices1[1:] + [sub_slice2],
                self.slices2 + [sub_slice1],
                self.index
            )
            socialised_div.rlist = slice.rlist #list of division ray iterations
            socialised_div.math_ray_list = slice.math_ray_list
            socialised_div.rung0 = slice.rung0

            return socialised_div
        else:
            s1 = self.cut_slice_1
            s2 = self.cut_slice_2
            sbowtie = self.bowtie

            def vector_fan(v1, v2, exp2):
                mid = unit(v1 + v2)
                if exp2 <= 0:
                    return [mid]
                return vector_fan(v1, mid, exp2 - 1) + vector_fan(mid, v2, exp2 - 1)

            exp2 = 6
            vec_fan = vector_fan(unit(s1.ray1.direction), unit(s1.ray2.direction), exp2)
            
            area_per_vec = []
            for v in vec_fan:
                b1, b2 = sbowtie.divide_using_vector(v)
                area_per_vec.append(b2.area1 + b1.area2)

            self.bowtie.area_per_vec = area_per_vec

            self.rlist = [self.cut_slice_1.ray1]
            return self
            # raise NotImplemented
