import vector
from sympy import Eq, symbols, solve, linsolve
import copy
from data_structures import Ray,Segment,Bowtie

def toTuple(vec):
    return (vec.x, vec.y)


class Polygon :
    bowties = []
    rays = []
    def __init__(self, points):
        self.points = points
        self.vec_points = [vector.obj(x=p[0], y=p[1]) for p in self.points]

        print('POLY INIT '+30*'-')
        print(self.vec_points)

        self.segments = []
        for i in range(len(self.vec_points) - 1):
            self.segments.append(Segment(*self.vec_points[i:i+2]))

        self.segments.append(Segment(self.vec_points[-1], self.vec_points[0]))

    #TODO 2 rays have the same angle or are very close
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

        temp_bowties = []
        for i in range(len(self.rays) - 1):
            temp_bowties.append(Bowtie(self.origin, self.rays[i], self.rays[i+1]))
        temp_bowties.append(Bowtie(self.origin, self.rays[-1], self.rays[0]))

        #removes bowtie that contains the whole polygon
        self.bowties = [bt for bt in temp_bowties if not bt.is_empty]

    def display_ray(self, index):
        ray = self.rays[index]

        l = lambda a:a.segment
        fb = [(toTuple(l(i).a), toTuple(l(i).b)) for i in ray.intersections]

        rl = [ray.gen_line_tuple()]

        return fb + rl
