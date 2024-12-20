import copy
from math import pi

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
    # print(total_calculations[0], solution)


    total_calculations[0] += 1
    return solution

class Segment :
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = b - a

    def ray_intersection_math(self, ray):
        solution = seg_ray_intersection_math(self, ray)
        return solution
        #     #this "solution" is slow
        #     d, k = symbols('d, k') #d scales ray and k scales c  up to intersection point
        #     eq1 = Eq(d * float(a @ ray.direction) - k * (a @ c), abs(a) ** 2)
        #     eq2 = Eq(d * float(b @ ray.direction) - k * (b @ c), abs(b) ** 2 - c @ b)
        #
        #     solution = solve([eq1, eq2], [d, k], particular = True, quick=True)
        #     print(solution)
        #     solution = {'d' : solution[d], 'k' : solution[k]}
        #
        # return solution

class Intersection:
    def __init__(self, point, segment):
        self.point = point
        self.segment = segment

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

                #TODO REMOVE d > 0 AFTER DEBUGGING
                if 0 <= k <= 1:
                    self.intersections.append( Intersection(self.origin + self.direction * d, seg))

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

class Bowtie :
    # self.rungs = None
    def __init__(self, origin, ray1, ray2):
        self.origin = origin
        self.ray1 = ray1
        self.ray2 = ray2

        self.gen_ladder_rungs()

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

            self.rungs += [Segment(int1.point, int2.point)]


        #TODO sort rungs
        # self.rungs.sort(key = lambda a: a.)
