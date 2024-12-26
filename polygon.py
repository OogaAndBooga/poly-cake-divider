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
        self.gen_segments()

        print('POLY INIT '+30*'-')
        print(self.vec_points)

    def gen_segments(self):
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

        empty_bowtie_list = [bt for bt in temp_bowties if bt.is_empty]        

        if empty_bowtie_list == []:
            self.bowties = temp_bowties
            for bts in zip(self.bowties, self.bowties[1:]):
                Bowtie.link_bowties(bts[0], bts[1])
            Bowtie.link_bowties(self.bowties[-1], self.bowties[0])

        else:
            empty_bowtie = empty_bowtie_list[0]
            empty_bowtie_index = temp_bowties.index(empty_bowtie)
            del temp_bowties[empty_bowtie_index]
            i = empty_bowtie_index
            # self.bowties[0] and self.bowties[-1] are on opposide sides of polygon
            self.bowties = temp_bowties[i:] + temp_bowties[0:i]

            for bts in zip(self.bowties, self.bowties[1:]):
                Bowtie.link_bowties(bts[0], bts[1])

    def divide_with_slice(self, slice):
        positive_area = 0
        negative_area = 0
        start_slice = slice
        end_slice = slice.opposite
        while slice is not end_slice:
            positive_area += slice.area
            negative_area += slice.opposite.area
            slice = slice.next

        return [positive_area, negative_area]
