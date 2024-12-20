import vector
from sympy import Eq, symbols, solve, linsolve
import copy
from data_structures import Ray,Segment,Bowtie

def toTuple(vec):
    return (vec.x, vec.y)


class Polygon :
    bowties = []
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

        self.rays.sort(key=lambda a: a.sorting_angle)

    #tuple for input
    def set_origin(self, origin):
        self.origin = vector.obj(x = origin[0], y = origin[1])

    def gen_bowties(self, origin):
        self.set_origin(origin)
        self.gen_rays()

        #BUG when point outside of polygon, a bowtie containint the wholee polygon is generated
        self.bowties = []
        for i in range(len(self.rays) - 1):
            self.bowties.append(Bowtie(self.origin, self.rays[i], self.rays[i+1]))
        self.bowties.append(Bowtie(self.origin, self.rays[-1], self.rays[0]))


    def display_ray(self, index):
        ray = self.rays[index]

        l = lambda a:a.segment
        fb = [(toTuple(l(i).a), toTuple(l(i).b)) for i in ray.intersections]

        rl = [ray.gen_line_tuple()]

        return fb + rl

    # def display_bowtie(self, index):

        # bt = self.bowties[index]
        # fb = bt.rungs
        #
        #
        # fb = [(toTuple(seg.a), toTuple(seg.b)) for seg in fb]
        #
        # rys = [bt.ray1.gen_line_tuple(), bt.ray2.gen_line_tuple()]
        #
        # # print(f"FB, RED DATA:{fb}")
        # # print(f"RED DATA LENGTH(rys):{len(rys)}")
        # # print(f'BOWTIE INDEX {index}')
        # return fb + rys
