import vector
from sympy import Eq, symbols, solve, linsolve
import copy
from data_structures import Ray,Segment,Bowtie

def toTuple(vec):
    return (vec.x, vec.y)


class Polygon :

    def __init__(self, points):
        self.points = points
        self.vec_points = [vector.obj(x=p[0], y=p[1]) for p in self.points]

        print('POLY INIT '+30*'-')
        print(self.vec_points)

        self.segments = []
        for i in range(len(self.vec_points) - 1):
            self.segments.append(Segment(*self.vec_points[i:i+2]))

        self.segments.append(Segment(self.vec_points[-1], self.vec_points[0]))

    def gen_rays(self):
        self.rays = []
        for vertex in self.vec_points:
            ray = Ray(self.origin, vertex)
            ray.intersect_polygon(self)

            self.rays.append(ray)

        self.rays.sort(key=lambda a: a.key)

    #tuple for input
    def set_origin(self, origin):
        self.origin = vector.obj(x = origin[0], y = origin[1])

    def gen_bowties(self, origin):
        self.set_origin(origin)
        self.gen_rays()

        self.bowties = []
        for i in range(len(self.rays) - 1):
            self.bowties.append(Bowtie(self.origin, self.rays[i], self.rays[i+1]))
        self.bowties.append(Bowtie(self.origin, self.rays[-1], self.rays[1]))



        # breakpoint()
        # print("NUMBER OF BOWTIES{len(self.bowties)}")
        bt = self.bowties[0]
        fb = self.bowties[0].rungs
        # breakpoint()
        # prin


        fb = [(toTuple(seg.a), toTuple(seg.b)) for seg in fb]

        rys = [self.bowties[0].ray1.gen_line_tuple(), self.bowties[0].ray2.gen_line_tuple()]
        print(f"FB, RED DATA:{fb}")
        print(f"RED DATA LENGTH(rys):{len(rys)}")
        return fb + rys

        # for ray in self.rays:
        #     for seg in self.segments:
        #
        #         ray_on_segment_edge = ray.poly_vertex is seg.a or ray.poly_vertex is seg.b
        #
        #         if ray_on_segment_edge:
        #             ray.intersections.append( Intersection(ray.poly_vertex, seg))
        #         else:
        #             sol = seg.ray_intersection(ray)
        #             d = sol['d']
        #             k = sol['k']
        #
        #             if not_in_seg and d > 0 and 0 <= k <= 1:
        #                 ray.intersections.append( Intersection(ray.origin + ray.direction * d, seg))



        # for i in range(len(self.rays) - 1):
        #     self.bowties.append(Bowtie(self.rays[i], self.rays[i+1]))
