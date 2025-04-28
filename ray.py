import numpy as np

np.seterr(all='raise')

def toTuple(vec):
    return vec.tolist()

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
        
        if poly_vertex is not None:
            self.direction = poly_vertex - origin # vector with ray direction
        if direction is not None:
            self.direction = direction
        
        self.angle = np.angle(complex(*self.direction))

    def gen_opposite(self):
        o_ray = Ray(self.origin, direction = -self.direction)
        return o_ray

    #TODO create self.intersections_opposite for clearer code?
    def intersect_segments(self, segments):
        self.intersections = []
        for seg in segments:
            if self.poly_vertex is not None:
                ray_on_segment_edge = self.poly_vertex is seg.a or self.poly_vertex is seg.b
            else:
                ray_on_segment_edge = False

            if ray_on_segment_edge:
                self.intersections += [Intersection(self.poly_vertex, seg)]
            else:
                sol = seg.ray_intersection_math(self)
                if sol is not None:
                    d = sol['d']
                    k = sol['k']

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
        dir = r.direction * 6100
        a = r.origin + dir
        b = r.origin - dir
        return (toTuple(a), toTuple(b))