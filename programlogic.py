from math import dist
from polygon import Polygon
from data_structures import total_calculations
import time
from data_structures import Segment

from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import  Qt

def toTuple(vec):
    if type(vec) == Segment:
        return (toTuple(vec.a), toTuple(vec.b))
    return (vec.x, vec.y)

#TODO detect intersection of polyline while inputing

class Program_Logic():
    bts = 2
    btindex = 0
    rayindex = 0
    sindex = 0
    dvindex = 0
    # stage = 0
    polyline = [] # before creation of polygon
    mouse_near = False # mouse within a certain distance to polyline origin
    origin = None #one of the defining points for division
    origin_is_set = False
    MOUSENEARDIST = 10
    display_socialised_division = False
    # tempbowtiedata = []
    # tempbowtielines = []
    # tempbowtieshapes = []
    # redpoints = []
    def __init__(self):
        pass

    def pass_render_area_instance(self, r_area_instance):
        self.render_area = r_area_instance

    def pass_plot_widget_instance(self, plot_widget):
        self.plot_widget = plot_widget

    # 0 = input polyline
    # 1 = set origin
    # 2 = cycle polygon divisions
    stage = 0

    def advance_stage(self):
        self.stage += 1

    def reset_to_stage(self, stage):
        if stage == 0:
            self.stage = 0
            self.polyline = []

    def set_mouse_near(self, value):
        must_update = (value != self.mouse_near)
        self.mouse_near = value
        if must_update:
            self.update_screen()

    def key_press_event(self, key):
        if key != 'reset':
            if key == 'up':
                self.sindex += 1
            elif key == 'down':
                self.sindex -= 1
            # elif key == 'toggle':
            #     self.bts += 1
            #     self.bts %= 3

            if self.stage == 2:
                if 0 > self.sindex or self.sindex >= len(self.poly.slices):
                    self.sindex %= len(self.poly.slices)
                
                print(f'Slice Index: {self.sindex}/{len(self.poly.slices) - 1}')
                self.plot_widget.set_btindex(self.sindex)
        else :
            self.reset_to_stage(0)
        self.update_screen()

    def mouse_move_event(self, pos):
        if self.stage == 0:
            if len(self.polyline) > 2 and dist(self.polyline[0], pos) < self.MOUSENEARDIST:
                self.set_mouse_near(True)
            else :
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
        # elif self.stage == 1:
        elif self.stage in [1, 2]:
            print(f"ORIGIN POSITION: {pos}")
            self.origin = pos
            self.origin_is_set = True
            self.btindex = 0

            total_calculations[0] = 0

            t1 = time.time()
            self.poly.set_origin_and_calculate_divisions(self.origin)
            t2 = time.time()
            print(f'POLY STATS --------------- ')
            print(f'CALCULATED {total_calculations[0]} INTERSECTIONS IN {round(t2-t1,2)} seconds')
            print(f'POLYGON AREA: {self.poly.area}')
            print(f'NUMBER OF SLICES: {len(self.poly.slices)}')
            print(f'INDEXES OF SOCIALSIT DIVISIONS: {[d.index for d in self.poly.future_socialist_divisions]}')
            sd = self.poly.socialised_divisions[0]
            print(f'area1: {sd.area1}')
            print(f'area2 = {sd.area2}')
            if self.stage == 1:
                self.advance_stage()
            self.update_screen()

    def load_poly_and_origin(self, data):
        poly = data[0]
        origin = data[1]
        self.polyline = poly
        self.mouse_near = True
        self.stage = 0
        self.click_event(poly[0])
        self.click_event(origin)


    def toggle_div_display(self):
        self.display_socialised_division = not self.display_socialised_division
        self.update_render_area()

    def display_ray_data_gen(self):
        if(len(self.poly.rays) == 0):
            return

        ray = self.poly.rays[self.rayindex]

        segments = [toTuple(i.segment) for i in ray.intersections]
        points = [toTuple(i.point) for i in ray.intersections]

        rl = [ray.gen_line_tuple()]

        self.tempbowtielines = rl + segments
        print(self.tempbowtielines)
        self.redpoints = points

    def gen_slice_display(self):
        if self.poly.slices == []:
            return
        sl = self.poly.slices[self.sindex]
        lines = [toTuple(r.segment) for r in sl.rungs]
        rays = [sl.ray1.gen_line_tuple(), sl.ray2.gen_line_tuple()]
        shapes = [s.tup for s in sl.shapes]

        self.tempbowtielines = lines + rays
        self.tempbowtieshapes = shapes

    def display_division(self):
        if self.poly.divisions == []:
            return
        div = self.poly.divisions[self.sindex]
        divshp1 = [shape.tup for shape in div.shapes1]
        divshp2 = [shape.tup for shape in div.shapes2]

        self.division_shapes_1 = divshp1
        self.division_shapes_2 = divshp2

        self.pink_center_shapes = [shape.tup for shape in div.slices1[0].shapes] + [s.tup for s in div.slices2[0].shapes]

        ray = div.ray
        self.division_ray = ray.gen_line_tuple()

    def update_screen(self):
        if self.stage == 2:
            # self.display_bowtie_data_gen()
            # self.display_ray_data_gen()
            # self.gen_slice_display()
            self.display_division()
            self.update_graph()
        self.update_render_area()

    def update_graph(self):
        indexes = range(len(self.poly.slices))

        a1 = [d.area1 for d in self.poly.divisions]
        a2 = [d.area2 for d in self.poly.divisions]
        a3 = [d.total_area for d in self.poly.divisions]

        self.plot_widget.plot1.setData(indexes, a1)
        self.plot_widget.plot2.setData(indexes, a2)
        self.plot_widget.plot3.setData(indexes, a3)

        self.plot_widget.set_line2(self.poly.future_socialist_divisions[0].index)
        self.plot_widget.update()

    def update_render_area(self):
        class Paint_Kit:
            def __init__(self, pen = QPen(), brush = QBrush()):
                self.pen = pen
                self.brush = brush
                self.points = []
                self.lines = []
                self.polylines = []
                self.polygons = []

        draw_packets = []

        if self.stage == 0:
            #BUG if no points added and mouse near
            elements = Paint_Kit()
            if self.polyline != []:
                if len(self.polyline) == 1 or self.mouse_near:
                    elements.points.append(self.polyline[0])
                if len(self.polyline) > 1:
                    elements.polylines.append(self.polyline)
                draw_packets.append(elements)
        elif self.stage == 1:
            elements = Paint_Kit()
            elements.polygons.append(self.polyline)
            draw_packets.append(elements)
        elif self.stage == 2:
            black = Paint_Kit()
            black.polygons.append(self.polyline)

            green = Paint_Kit(QPen(Qt.PenStyle.NoPen), QBrush(Qt.green, Qt.CrossPattern))
            red = Paint_Kit(QPen(Qt.PenStyle.NoPen), QBrush(Qt.red, Qt.CrossPattern))
            purple = Paint_Kit(QPen('blue'))
            pink = Paint_Kit(QPen(Qt.PenStyle.NoPen), QBrush('pink', Qt.CrossPattern))
            orange = Paint_Kit(QPen('orange'))

            if self.origin_is_set:
                black.points.append(self.origin)

                if not self.display_socialised_division:
                    green.polygons += self.division_shapes_1
                    red.polygons += self.division_shapes_2
                    purple.lines.append(self.division_ray)
                    pink.polygons += self.pink_center_shapes
                else:
                    sd = self.poly.socialised_divisions[0]
                    green.polygons += [s.tup for s in sd.shapes1]
                    red.polygons += [s.tup for s in sd.shapes2]

                s = [a.gen_line_tuple() for a in self.poly.rlist]
                # print(s)
                # orange.lines += s
                orange.lines += [s[-1]]

            for color in [black, red, green, purple, pink, orange]:
                draw_packets.append(color)

        self.render_area.draw_packets = draw_packets
        self.render_area.update()