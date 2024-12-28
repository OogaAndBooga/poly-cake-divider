import copy
from math import pi
from functools import cmp_to_key
from math import dist, sqrt

total_calculations = [0]

def toTuple(vec):
    return (vec.x, vec.y)

#TODO case in which segment is parallel to ray
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

    def generator(self):
        yield self.a
        yield self.b

    def __iter__(self):
        return self.generator()

    #not a full implementation of & operator
    #2 identical segments will not return a iterable with both points
    def __and__(self, other):
        # breakpoint()
        if not (self.a in other or self.b in other or other.a in self or other.b in self):
            return None
        else:
            if self.a in other:
                return self.a
            if self.b in other:
                return self.b
            if other.a in self:
                return other.a
            if other.b in self:
                return other.b

class Intersection:
    def __init__(self, point, segment):
        self.point = point
        self.segment = segment

class Ray :
    intersections = []
    flipped = False
    def __init__(self, origin, poly_vertex = None, direction = None):
        self.origin = origin
        self.poly_vertex = poly_vertex
        
        if poly_vertex is None and direction is None:
            raise TypeError('either a direction or a poly_vertex must be provided')
        
        if poly_vertex is not None and direction is not None:
            raise TypeError('do not provide both poly_vertex and direction')
        
        if poly_vertex:
            self.direction = poly_vertex - origin # vector with ray direction
        if direction:
            self.direction = direction
        
        # self.sorting_angle = self.direction.phi
        self.angle = self.direction.phi

    def gen_opposite(self):
        o_ray = Ray(self.origin, direction = -self.direction)
        return o_ray
        

    #TODO create self.intersections_opposite for clearer code?
    def intersect_polygon(self, poly):
        self.intersections = []
        for seg in poly.segments:
            if self.poly_vertex is not None:
                ray_on_segment_edge = self.poly_vertex in seg
            else:
                ray_on_segment_edge = False

            if ray_on_segment_edge:
                self.intersections += [Intersection(self.poly_vertex, seg)]
            else:
                sol = seg.ray_intersection_math(self)
                d = sol['d']
                k = sol['k']

                dpos = (d >= 0)
                if not self.flipped:
                    section = dpos
                else:
                    section = not dpos

                if 0 <= k <= 1 and 0 < d:
                    self.intersections.append(
                        Intersection(self.origin + self.direction * d, seg)
                    )

    def gen_oriented_line_tuple(self):
        r = self
        dir = r.direction * 100
        a = r.origin + dir
        b = r.origin
        # b = r.origin - dir
        return (toTuple(a), toTuple(b))
    
    def gen_line_tuple(self):
        r = self
        dir = r.direction * 100
        a = r.origin + dir
        b = r.origin - dir
        return (toTuple(a), toTuple(b))

class Rung:
    def __init__(self, origin, a, b):
        self.segment = Segment(a, b)
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
        return self.generator()

#points as tuples
def heron_area(p1, p2, p3):
    a = dist(p1, p2)
    b = dist(p2, p3)
    c = dist(p3, p1)
    s = (a + b + c) / 2
    return sqrt(s * (s - a) * (s - b) * (s - c))

class Quadrilateral:
    def __init__(self, rung1, rung2):
        self.rung1 = rung1
        self.rung2 = rung2
        self.tup = [toTuple(p) for p in[rung1.a, rung1.b, rung2.b, rung2.a]]
        self.area = (
            heron_area(*[toTuple(p) for p in[*rung1, rung2.a]]) +
            heron_area(*[toTuple(p) for p in[*rung2, rung1.b]])
        )

#TODO store data for future calculations
#assumes rungs have 1 point in common
class Triangle:
    def __init__(self, rung1, rung2):
        comp = rung1.segment & rung2.segment
        points = [*rung1.segment] + [*rung2.segment]
        self.tup = [toTuple(comp)] + [toTuple(p) for p in points if p is not comp]
        self.area = heron_area(*self.tup)
        # print(self.tup)

class Origin_Triangle:
    def __init__(self, origin, rung):
        self.origin = origin
        self.rung = rung
        self.tup = [toTuple(p) for p in [origin, *rung]]
        self.area = heron_area(*self.tup)

class Slice():
    opposite = None
    next = None
    previous = None

    def __init__(self, ray1, ray2):
        self.origin = ray1.origin
        self.ray1 = ray1
        self.ray2 = ray2

        self.gen_rungs()
        self.origin_inside_poly = (len(self.rungs) % 2 == 1)
        self.gen_shapes()
        self.is_empty = (self.shapes == [])
        self.calculate_area()

    def gen_rungs(self):
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

        def compare_seg_origin_distance(rung1, rung2):
            if rung1 is rung2:
                return 0
            
            # True -> 1
            # False -> -1
            l = lambda b: int(b) * 2 - 1
            
            if rung1.ray1.poly_vertex is rung2.ray1.poly_vertex:
                return l(abs(rung1.ray2.direction) > abs(rung2.ray2.direction))
            elif rung1.ray2.poly_vertex is rung2.ray2.poly_vertex:
                return l(abs(rung1.ray1.direction) > abs(rung2.ray1.direction))
            else:
                return l(abs(rung1.ray1.direction) > abs(rung2.ray1.direction))

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

class Division:
    def __init__(self, ray, slices1, slices2):
        self.ray = ray
        self.slices1 = slices1
        self.slices2 = slices2

        self.shapes1 = [shape for slice in slices1 for shape in slice.shapes]
        self.shapes2 = [shape for slice in slices2 for shape in slice.shapes]

        self.area1 = sum([slice.area for slice in slices1])
        self.area2 = sum([slice.area for slice in slices2])
        self.total_area = self.area1 + self.area2