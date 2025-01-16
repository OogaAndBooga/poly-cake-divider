import vector
import copy
from data_structures import Ray,Segment,Division,Slice

def toTuple(vec):
    return (vec.x, vec.y)

class Polygon :
    #TODO leave uncommented for clarity?
    # bowties = []
    # rays = []
    # slices = [] #quick fix, update_screen is called with stage = 1 before poly.set_origin_and... is called
    # divisions = [] #quick fix
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

    def set_origin_and_calculate_divisions(self, origin):
        self.origin = vector.obj(x = origin[0], y = origin[1])
        self.gen_rays()
        self.gen_slices()
        self.gen_divisions()
        self.calculate_area()
        self.determine_equal_division_slices()
        self.socialise_possible_divisions()

        # print()

        # print(self.future_socialist_divisions)

    #TODO 2 rays have the same angle or are very close
    def gen_rays(self):
        self.rays = []
        for vertex in self.vec_points:
            ray = Ray(self.origin, vertex)
            ray_opposite = ray.gen_opposite()

            ray.intersect_segments(self.segments)
            ray_opposite.intersect_segments(self.segments)

            self.rays.append(ray)
            self.rays.append(ray_opposite)

        self.rays.sort(key=lambda r: r.angle)

    def gen_slices(self):
        self.slices = []
        for ray1, ray2 in zip(self.rays, self.rays[1:]):
            self.slices.append(Slice(ray1, ray2))
        self.slices.append(Slice(self.rays[-1], self.rays[0]))

    def calculate_area(self):
        self.area = 0
        for slice in self.slices:
            self.area += slice.area
        self.half_area = self.area / 2

    def gen_divisions(self):
        self.divisions = []
        slices_len = len(self.slices)
        half_len = slices_len // 2
        # breakpo
        # TODO
        for slice_index in range(0, slices_len):
            if slice_index + half_len < slices_len:
                # breakpoint()
                slices1 = self.slices[slice_index : slice_index + half_len]
                slices2 = self.slices[slice_index + half_len:] + self.slices[:slice_index]
            else:
                #TODO check this part with pen and paper, i just tried something and it worked
                slices1 = self.slices[slice_index:] + self.slices[:slice_index - half_len]
                slices2 = self.slices[slice_index - half_len : slice_index]

            self.divisions.append(Division(self.slices[slice_index].ray1, slices1, slices2, index = len(self.divisions)))

    #FIXME WORK FOR CASES WITH MORE THAN 1 SOLUTION
    def determine_equal_division_slices(self):
        self.future_socialist_divisions = []
        division_pairs = [(self.divisions[-1], self.divisions[0])] + list(zip(self.divisions, self.divisions[1:]))
        for d1, d2 in division_pairs:
            if d1.area1 > self.half_area and d2.area1 < self.half_area:
                self.future_socialist_divisions.append(d1)

    #TODO implement case with more than 1 solution, origin within the polygon
    def socialise_possible_divisions(self):
        self.socialised_divisions = []
        for div in self.future_socialist_divisions:
            slice = div.slices1[0]
            r = (self.half_area - div.area2) / slice.area
            sub_slice1, sub_slice2 = slice.divide_using_ratio(r)
            socialised_div = Division(None, div.slices1[1:] + [sub_slice2], div.slices2 + [sub_slice1] , None)
            self.socialised_divisions.append(socialised_div)
            self.rlist = slice.rlist