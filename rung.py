from ray import Ray
class Rung:
    def __init__(self, origin, segment):
        self.segment = segment
        a, b = segment
        # self.segment = Segment(a, b)
        self.ray1 = Ray(origin, a)
        self.ray2 = Ray(origin, b)
        self.origin = origin
        self.a = a
        self.b = b
    #a, b and __iter__ are for backwards compatibility, with 1 use case in Quadrilateral?
    def generator(self):
        yield self.ray1.poly_vertex
        yield self.ray2.poly_vertex

    def __iter__(self):
        return self.generator()