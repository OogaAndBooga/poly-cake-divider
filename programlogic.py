from math import dist
from polygon import Polygon
from data_structures import total_calculations
import time

def toTuple(vec):
    return (vec.x, vec.y)

class Program_Logic():
    bts = 2
    btindex = 0
    stage = 0
    polyline = [] # before creation of polygon
    mouse_near = False # mouse within a certain distance to polyline origin
    origin = None #one of the defining points for division
    origin_is_set = False
    MOUSENEARDIST = 10
    tempbowtiedata = []
    tempbowtielines = []
    tempbowtieshapes = []
    redpoints = []
    # points = []

    def __init__(self):
        pass

    def pass_render_area_instance(self, r_area_instance):
        self.render_area = r_area_instance

    def pass_plot_widget_instance(self, plot_widget):
        self.plot_widget = plot_widget

    def advance_stage(self):
        self.stage += 1

    def set_mouse_near(self, value):
        must_update = (value != self.mouse_near)
        self.mouse_near = value
        if must_update:
            self.update_screen()

    def key_press_event(self, key):
        # if key in ['up','down']:
        if key == 'up':
            self.btindex += 1
        elif key == 'down':
            self.btindex -= 1
        # elif key == 'toggle':
        #     self.bts += 1
        #     self.bts %= 3
        # print(f'BTS: {self.bts}')

        if abs(self.btindex) >= len(self.poly.bowties):
            self.btindex = 0

        self.update_screen()


    def mouse_move_event(self, pos):
        if self.stage == 0:
            if len(self.polyline) > 2 and dist(self.polyline[0], pos) < self.MOUSENEARDIST:
                self.set_mouse_near(True)
            else:
                self.set_mouse_near(False)

    def click_event(self, pos):
        print(pos)
        if self.stage == 0:
            if not self.mouse_near:
                self.polyline.append(pos)
            else:
                self.advance_stage()
                self.poly = Polygon(self.polyline)
                print(self.polyline)
            self.update_screen()
        elif self.stage == 1:
            if True:
                print(f"ORIGIN POSITION: {pos}")
                self.origin = pos
                self.origin_is_set = True

                total_calculations[0] = 0

                t1 = time.time()
                self.poly.gen_bowties(self.origin)
                t2 = time.time()
                print(f'CALCULATED {total_calculations[0]} INTERSECTIONS IN {round(t2-t1,2)} seconds')

                # self.tempbowtiedata = self.poly.display_ray(self.btindex)
                # self.display_bowtie()
                # self.tempbowtiedata = self.poly.display_bowtie(self.btindex)

                self.update_screen()

    def display_ray_data_gen(self):
        if(len(self.poly.rays) == 0):
            return

        ray = self.poly.rays[self.btindex]

        # l = lambda a:a.segment
        if self.bts == 0:
            points = [toTuple(i.point) for i in ray.intersections if i.section]
        elif self.bts == 1:
            points = [toTuple(i.point) for i in ray.intersections if not i.section]
        else:
            points = [toTuple(i.point) for i in ray.intersections]
        # points = [toTuple(i.point) for i in ray.intersections if i.section == t]

        rl = [ray.gen_line_tuple()]

        # return fb + rl
        self.tempbowtielines = rl
        self.redpoints = points

    def display_bowtie_data_gen(self):
        if(len(self.poly.bowties) == 0):
            return

        bt = self.poly.bowties[self.btindex]

        fb = bt.rungs
        fb = [(toTuple(seg.a), toTuple(seg.b)) for seg in fb]

        rys = [bt.ray1.gen_line_tuple(), bt.ray2.gen_line_tuple()]

        self.redlines = fb
        self.tempbowtielines = rys
        a = [s.tup for s in bt.shapes]
        b = [s.tup for s in bt.shapes_opposite]
        if self.bts == 0:
            c = a
        elif self.bts == 1:
            c = b
        else:
            c = a + b

        self.tempbowtieshapes = c

    def update_screen(self):
        # self.display_ray_data_gen()
        self.display_bowtie_data_gen()
        self.update_render_area()
        self.update_graph()

    def update_graph(self):
        l1 = [i for i in range(len(self.poly.bowties))]
        l2 = [len(bt.rungs) for bt in self.poly.bowties]
        self.plot_widget.p.setData(l1,l2)

        self.plot_widget.update()

    def update_render_area(self):
        primitives = {'points' : [],
                      'polyline' : [],
                      'polygon' : []
                      }

        redlines = []
        redpolys = []
        redpoints = []

        if self.stage == 0:
            #BUG if no points added and mouse near
            if len(self.polyline) == 1 or self.mouse_near:
                primitives['points'].append(self.polyline[0])
            if len(self.polyline) > 1:
                primitives['polyline'] = self.polyline
        elif self.stage == 1:
            primitives['polygon'] = self.polyline
            if self.origin_is_set:
                primitives['points'] += [self.origin]
                redlines += self.tempbowtielines
                redpolys = self.tempbowtieshapes
                redpoints = self.redpoints

        # print('PRIMITIVES SENT TO RENDERAREA', primitives)
        # print(f'NUMBER OF BLACK PRIMITIVES {len(primitives)}')
        # print(f'NUMBER OF RED RUNGS: {len(redlines) - 2}')
        self.render_area.primitives = primitives
        self.render_area.redlines = redlines
        self.render_area.redpolys = redpolys
        self.render_area.redpoints = redpoints
        self.render_area.update()
