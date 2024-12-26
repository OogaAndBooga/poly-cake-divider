import copy
from math import pi
from functools import cmp_to_key
from math import dist, sqrt

#TODO use same naming convention as Bowtie.area ...

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
    def __init__(self, point, segment, section : bool):
        self.point = point
        self.segment = segment
        self.section = section

class Ray :
    intersections = []
    flipped = False
    def __init__(self, origin, poly_vertex):
        self.origin = origin
        self.direction = poly_vertex - origin # vector with ray direction
        self.poly_vertex = poly_vertex

        self.sorting_angle = self.direction.phi
        if self.sorting_angle < 0:
            self.sorting_angle += pi
            self.flipped = True

    #TODO create self.intersections_opposite for clearer code?
    def intersect_polygon(self, poly):
        self.intersections = []
        for seg in poly.segments:
            ray_on_segment_edge = self.poly_vertex in seg

            if ray_on_segment_edge:
                self.intersections += [Intersection(self.poly_vertex, seg, not self.flipped)]
            else:
                sol = seg.ray_intersection_math(self)
                d = sol['d']
                k = sol['k']

                dpos = (d >= 0)
                if not self.flipped:
                    section = dpos
                else:
                    section = not dpos
                if 0 <= k <= 1:
                    self.intersections.append(
                        Intersection(self.origin + self.direction * d, seg, section)
                    )

    def gen_line_tuple(self):
        r = copy.deepcopy(self)
        r.direction *= 100
        r.poly_vertex = r.origin + r.direction
        r.origin  = r.origin - r.direction
        return (toTuple(r.origin), toTuple(r.poly_vertex))

    # def export(self):
    #     return {
    #         'origin': toTuple(self.origin),
    #         'direction' : toTuple(self.direction),
    #         'intersections' : [toTuple(i.point) for i in self.intersections]
    #     }

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

    def __init__(self, origin, ray1, ray2, shapes, area):
        self.origin = origin
        self.ray1 = ray1
        self.ray2 = ray2
        self.shapes = shapes
        self.area = area

    def set_opposites(self, other):
        self.opposite = other
        other.opposite = self

    def link_elements(first, second):
        first.next = second
        second.previous = first

    def get_next(self):
        return self.next

    def get_previous(self):
        return self.previous

class Bowtie :
    def __init__(self, origin, ray1, ray2):
        self.origin = origin
        self.ray1 = ray1
        self.ray2 = ray2

        self.gen_ladder_rungs()
        self.gen_shapes()
        self.gen_areas()
        self.gen_slices()

        self.is_empty = (len(self.rungs + self.rungs_opposite) == 0)

    #assuming polyline does not intersect itself, neither will the ladder rungs
    def gen_ladder_rungs(self):
        self.rungs = []
        self.rungs_opposite = []

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

            #for any two rungs, r1.a and r2.a are intersected by a ray
            if int1.section :
                self.rungs += [Rung(self.origin, int1.point, int2.point)]
            else:
                self.rungs_opposite += [Rung(self.origin, int1.point, int2.point)]

        #compare function for 2 rungs on distance to origin
        def compare_seg_origin_distance(rung1, rung2):
            if rung1 is rung2:
                return 0
            l = lambda b: int(b) * 2 - 1
            if rung1.ray1.poly_vertex is rung2.ray1.poly_vertex:
                return l(abs(rung1.ray2.direction) > abs(rung2.ray2.direction))
            elif rung1.ray2.poly_vertex is rung2.ray2.poly_vertex:
                return l(abs(rung1.ray1.direction) > abs(rung2.ray1.direction))
            else:
                return l(abs(rung1.ray1.direction) > abs(rung2.ray1.direction))

        self.rungs.sort(key = cmp_to_key(compare_seg_origin_distance))
        self.rungs_opposite.sort(key = cmp_to_key(compare_seg_origin_distance))
        #TODO verify that rungs are sorted + sort order

    def shape_from_rungs(self, rung1, rung2):
        common = rung1.segment & rung2.segment
        if common is None:
            return Quadrilateral(rung1, rung2)
        else:
            return Triangle(rung1, rung2)

    #TODO implement for origin on polygon
    def gen_shapes(self):
        self.shapes = []
        self.shapes_opposite = []

        def gen_shapes(rungs, shapes):
            if len(rungs) % 2 == 1: #origin inside polygon
                self.shapes += [Origin_Triangle(self.origin, rungs[0])]
                for rung1, rung2 in zip(rungs[1::2], rungs[2::2]):
                    shapes += [self.shape_from_rungs(rung1, rung2)]
            else: #origin outside polygon
                if len(rungs) < 2:
                    return
                for i in range(1, len(rungs), 2):
                    rung1 = rungs[i]
                    rung2 = rungs[i-1]
                    shapes += [self.shape_from_rungs(rung1, rung2)]

        gen_shapes(self.rungs, self.shapes)
        gen_shapes(self.rungs_opposite, self.shapes_opposite)

    def gen_areas(self):
        self.positive_area = sum(shape.area for shape in self.shapes)
        self.negative_area = sum(shape.area for shape in self.shapes_opposite)
        self.delta_area = self.positive_area - self.negative_area
        self.total_area = self.positive_area + self.negative_area

    def gen_slices(self):
        self.positive_slice = Slice(self.origin, self.ray1, self.ray2, self.shapes, self.positive_area)
        self.negative_slice = Slice(self.origin, self.ray1, self.ray2, self.shapes_opposite, self.negative_area)
        self.positive_slice.set_opposites(self.negative_slice)

    def link_bowties(first, second):
        Slice.link_elements(first.positive_slice, second.positive_slice)
        Slice.link_elements(first.negative_slice, second.negative_slice)