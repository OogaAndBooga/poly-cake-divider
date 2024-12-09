import vector
from sympy import Eq, symbols, solve, linsolve

def toTuple(vec):
    return (vec.x, vec.y)

class Segment :
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = b - a

    def ray_intersection_math(self, ray, sp = False):
        a = self.a - ray.origin
        b = self.b - ray.origin
        c = self.c
        r = ray.direction

        if not sp:
            #TODO fix the bug
            # r = ray.direction
            k = (abs(b) ** 2 - c @ b - (abs(a) ** 2) * (r @ b) / (a @ r)) / ((b @ r) * (a @ c) / (a @ r) - (b @ c))
            d = (abs(a) ** 2 + k * (a @ c)) / (a @ r)
            solution = {'d':float(d), 'k':float(k)}
            print(solution)
        else:
            d, k = symbols('d, k') #d scales ray and k scales c  up to intersection point
            eq1 = Eq(d * float(a @ ray.direction) - k * (a @ c), abs(a) ** 2)
            eq2 = Eq(d * float(b @ ray.direction) - k * (b @ c), abs(b) ** 2 - c @ b)

            solution = solve([eq1, eq2], [d, k], particular = True, quick=True)
            print(solution)
            solution = {'d' : solution[d], 'k' : solution[k]}

        return solution

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

    def export(self):
        return {
            'origin':toTuple(self.origin),
                'direction' : toTuple(self.direction),
                'inter' : [toTuple(i.point) for i in self.intersections]
                }
    #
    # def

class Bowtie :
    def __init__(self, origin, ray1, ray2):
        self.origin = origin
        self.ray1 = ray1
        self.ray2 = ray2

    #removes intersections not in common
    def prune(self):
        for s1 in [inter.segment for inter in ray1.intersections]:
            for i in range(len(ray2.intersections)):
                if(id(s1) != id(ray2.indersections[i].segment)):
                    del ray2.indersections[i]

class Polygon :

    vpts = [] #vector form of points

    def __init__(self, points):
        self.points = points
        self.vec_points = [vector.obj(x=p[0], y=p[1]) for p in self.points]

        print('POLY INIY '+30*'-')
        print(self.vec_points)

        self.segments = []
        for i in range(len(self.vec_points) - 1):
            self.segments.append(Segment(*self.vec_points[i:i+2]))

        self.segments.append(Segment(self.vec_points[-1], self.vec_points[0]))

    #tuple as input
    def set_origin(self, origin):
        self.origin = vector.obj(x = origin[0], y = origin[1])

    def gen_bowties(self):
        # origin = vector.obj(x = origin.x(), y = origin.y()) #TODO code assuems orifin is a QPoint
        # print('ORIGIN'+'4'*40)
        # print(origin)

        # self.rays = [Ray(origin, vertex - origin) for vertex in self.vec_points]

        self.rays = []
        for vertex in self.vec_points:
            self.rays.append(Ray(origin, vertex))

        # ray = Ray(origin, self.vec_points[0] - origin)
        inter = []

        for ray in self.rays:
            for seg in self.segments:

                ray_on_segment_edge = ray.poly_vertex is seg.a or ray.poly_vertex is seg.b

                if ray_on_segment_edge:
                    ray.intersections.append( Intersection(ray.poly_vertex, seg))
                else:
                    sol = seg.ray_intersection(ray)
                    d = sol['d']
                    k = sol['k']

                    if not_in_seg and d > 0 and 0 <= k <= 1:
                        ray.intersections.append( Intersection(ray.origin + ray.direction * d, seg))



        # for i in range(len(self.rays) - 1):
        #     self.bowties.append(Bowtie(self.rays[i], self.rays[i+1]))

    def get_bowtie(self, index):
        b = self.bowties[index]


    # def
        # for each ray:
        #     for each seg
        #         check intersection
        #         if so remember intereesection point and seg index/instance


