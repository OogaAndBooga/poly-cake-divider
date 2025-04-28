

def seg_ray_intersection_math(segment, ray):
    a = segment.a - ray.origin
    b = segment.b - ray.origin
    c = segment.c
    r = ray.direction

    #TODO increase speed of computations
    #FIXME divide by zero potential error

    #division ray (0, 1) or (1, 0)
    if r[0] == 0:
        k = - a[0] / c[0]
        d = (k * c[1] + a[1]) / r[1]
    elif r[1] == 0:
        k = - a[1] / c[1]
        d = (c[0] * k + a[0]) / r[0]
    #division ray paralell with c
    elif r[0] * c[1] == r[1] * c[0]:
    # elif r[0] / r[1] == c[0] / c[1]:
        return None
    else:
        # try:
        k = (a[0] - a[1] / r[1] * r[0]) / (r[0] * c[1] / r[1] - c[0])
        # except :
        #     breakpoint()
        d = c[0] * k / r[0] + a[0] / r[0]

    solution = {'d':d, 'k':k}

    # global total_calculations
    # total_calculations[0] += 1
    return solution

    # k = (modulo(b) ** 2 - c @ b - (modulo(a) ** 2) * (r @ b) / (a @ r)) / ((b @ r) * (a @ c) / (a @ r) - (b @ c))
    # d = (modulo(a) ** 2 + k * (a @ c)) / (a @ r)
    # print(f'k: {k}\nkn: {kn}\nd: {d}\ndn: {dn}\n')


class Segment :
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = b - a

    def ray_intersection_math(self, ray):
        solution = seg_ray_intersection_math(self, ray)
        return solution
    
    def gen_tuple(self):
        return (self.a.tolist(), self.b.tolist())

    def generator(self):
        yield self.a
        yield self.b

    def __iter__(self):
        return self.generator()

    def __contains__(self, key):
        return key is self.a or key is self.b

    #not a full implementation of & operator
    #2 identical segments will not return a iterable with both points
    def __and__(self, other):
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