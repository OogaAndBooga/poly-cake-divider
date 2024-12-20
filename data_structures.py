import copy
from math import pi
from functools import cmp_to_key

total_calculations = [0]

def toTuple(vec):
    return (vec.x, vec.y)

def seg_ray_intersection_math(segment, ray):
    a = segment.a - ray.origin
    b = segment.b - ray.origin
    c = segment.c
    r = ray.direction

    #TODO increase speed of computations
    #FIXME divide by zero potential error

    k = (abs(b) ** 2 - c @ b - (abs(a) ** 2) * (r @ b) / (a @ r)) / ((b @ r) * (a @ c) / (a @ r) - (b @ c))
    d = (abs(a) ** 2 + k * (a @ c)) / (a @ r)
    solution = {'d':float(d), 'k':float(k)}

    global total_calculations
    total_calculations[0] += 1
    # print(total_calculations[0], solution)
    return solution

class Segment :
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = b - a

    def ray_intersection_math(self, ray):
        solution = seg_ray_intersection_math(self, ray)
        return solution

class Intersection:
    def __init__(self, point, segment, origin = None):
        self.point = point
        self.segment = segment
        if origin is not None:
            self.origin = origin

class Ray :
    intersections = []
    def __init__(self, origin, poly_vertex):
        self.origin = origin
        self.direction = poly_vertex - origin # vector with ray direction
        self.poly_vertex = poly_vertex

        self.sorting_angle = self.direction.phi
        if self.sorting_angle < 0:
            self.sorting_angle += pi


    def intersect_polygon(self, poly):
        self.intersections = []
        for seg in poly.segments:
            ray_on_segment_edge = self.poly_vertex is seg.a or self.poly_vertex is seg.b

            if ray_on_segment_edge:
                self.intersections += [Intersection(self.poly_vertex, seg)]
            else:
                sol = seg.ray_intersection_math(self)
                d = sol['d']
                k = sol['k']

                if 0 <= k <= 1:
                    self.intersections.append( Intersection(self.origin + self.direction * d, seg, self.origin))

    def gen_line_tuple(self):
        r = copy.deepcopy(self)
        r.direction *= 100
        r.poly_vertex = r.origin + r.direction
        r.origin  = r.origin - r.direction
        return (toTuple(r.origin), toTuple(r.poly_vertex))

    def export(self):
        return {
            'origin': toTuple(self.origin),
            'direction' : toTuple(self.direction),
            'intersections' : [toTuple(i.point) for i in self.intersections]
        }

class Rung:
    def __init__(self, origin, a, b):
        self.ray1 = Ray(origin, a)
        self.ray2 = Ray(origin, b)
        self.origin = origin
        self.a = a
        self.b = b
    #a, b and __iter__ are for backwards compatibility, with 1 use case in Quadrilateral
    def generator(self):
        yield self.ray1.poly_vertex
        yield self.ray2.poly_vertex

    def __iter__(self):
        return self.generator


class Quadrilateral:
    def __init__(self, rung1, rung2):
        self.rung1 = rung1
        self.rung2 = rung2
        self.tup = [toTuple(p) for p in[rung1.a, rung1.b, rung2.b, rung2.a]]

class Triangle:
    def __init__(self, rung1, rung2):
        self.rung

class Bowtie :
    # self.rungs = None
    def __init__(self, origin, ray1, ray2):
        self.origin = origin
        self.ray1 = ray1
        self.ray2 = ray2

        self.gen_ladder_rungs()
        self.gen_shapes()

    #assuming polyline does not intersect itself, neither will the ladder rungs
    def gen_ladder_rungs(self):
        self.rungs = []
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

            self.rungs += [Rung(self.origin, int1.point, int2.point)]

        #compare 2 rungs to see which is closer to origin
        def compare_seg(rung1, rung2):
            if rung1.ray1.poly_vertex is rung2.ray1.poly_vertex:
                return abs(rung1.ray2.direction) > abs(rung2.ray2.direction)
            else:
                return abs(rung1.ray1.direction) > abs(rung2.ray1.direction)
                # pass

        self.rungs = sorted(self.rungs, key = cmp_to_key(compare_seg), reverse = True)
        #TODO verify that rungs are sorted

    #TODO triangle shapes, origin shape, points not outside of polygon
    def gen_shapes(self):
        self.shapes = []
        for i in range(0,len(self.rungs), 2):
            self.shapes += [Quadrilateral(self.rungs[i], self.rungs[i+1])]

