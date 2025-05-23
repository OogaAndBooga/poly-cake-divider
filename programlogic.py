from math import dist
from polygon import Polygon
from data_structures import total_calculations
import time
from data_structures import Segment

from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import  Qt

import cv2 as cv
import numpy as np

from select_poly_dialog import Select_poly_dialog_creator
from database import DataBase

def toTuple(vec):
    if type(vec) == Segment:
        return (toTuple(vec.a), toTuple(vec.b))
    return (vec.x, vec.y)

#TODO detect intersection of polyline while inputing

class Program_Logic():
    is_counting_pixels = False
    is_dragging = False
    live_translation_amount = np.array((0, 0))
    translation_amount = np.array((0, 0))
    total_wheel_delta = 0
    scale_amount = 1
    SCALE_FACTOR = 0.003
    MIN_SCALE_AMOUNT = 0.3
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
    display_socialised_division = True

    def __init__(self):
        self.database = DataBase()

    def pass_render_area_instance(self, r_area_instance):
        self.render_area = r_area_instance

    def pass_plot_widget_instance(self, plot_widget):
        self.plot_widget = plot_widget

    def pass_database_ui(self, db_ui):
        self.database_ui = db_ui

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
            if self.stage == 2 and not self.display_socialised_division:
                if key == 'up':
                    self.sindex += 1
                elif key == 'down':
                    self.sindex -= 1

                if 0 > self.sindex or self.sindex >= len(self.poly.slices):
                    self.sindex %= len(self.poly.slices)
                
                # print(f'Slice Index: {self.sindex}/{len(self.poly.slices) - 1}')
                self.plot_widget.set_btindex(self.sindex)
        else :
            self.reset_to_stage(0)
        self.update_screen()

    def input_origin_as_string(self, sorigin : str):
        origin = eval(sorigin)
        self.click_event_poly_coords(origin)
        # self.click_event(origin)

    def wheel_event(self, scrpos, angle_delta):
        initial_scale = self.scale_amount

        self.total_wheel_delta += angle_delta
        self.scale_amount = 1 + self.total_wheel_delta * self.SCALE_FACTOR
        if self.scale_amount < self.MIN_SCALE_AMOUNT:
            self.scale_amount = self.MIN_SCALE_AMOUNT
            self.total_wheel_delta = (self.MIN_SCALE_AMOUNT - 1)/ self.SCALE_FACTOR

        d = scrpos + self.scale_amount / initial_scale * (self.live_translation_amount - scrpos)
        self.translation_amount = d
        self.live_translation_amount = self.translation_amount

        self.update_render_area()

    def reset_pan_and_zoom(self):
        self.live_translation_amount = np.array((0, 0))
        self.translation_amount = np.array((0, 0))
        self.total_wheel_delta = 0
        self.scale_amount = 1
        self.update_render_area()

    def screen_pos_to_poly_pos(self, scrpos):
        return (scrpos - self.live_translation_amount) / self.scale_amount

    def mouse_move_event(self, pos):
        if self.is_dragging:
            delta = np.array(pos) - self.drag_start_pos
            self.live_translation_amount = self.translation_amount + delta
            self.update_render_area()

        if self.stage == 0:
            pos = self.screen_pos_to_poly_pos(pos)
            if len(self.polyline) > 2 and dist(self.polyline[0], pos) < self.MOUSENEARDIST:
                self.set_mouse_near(True)
            else :
                self.set_mouse_near(False)

    def mouse_release_event(self, pos, button):
        if button == Qt.RightButton:
            self.is_dragging = False
            delta = np.array(pos) - self.drag_start_pos
            self.translation_amount += delta
            self.live_translation_amount = self.translation_amount
            self.update_render_area()

    def click_event(self, pos, button = None):
        if button == Qt.RightButton:
            self.is_dragging = True
            self.drag_start_pos = np.array(pos)
            return

        # take scale and translation into account
        pos = self.screen_pos_to_poly_pos(pos)
        pos = pos.tolist()
        self.click_event_poly_coords(pos)

    def click_event_poly_coords(self, poly_pos):
        pos = poly_pos
        if self.stage == 0:
            if not self.mouse_near:
                self.polyline.append(pos)
            else:
                self.advance_stage()
                self.poly = Polygon(self.polyline)
                print('POLY INIT '+30*'-')
                print(self.polyline)
            self.update_screen()
        # elif self.stage == 1:
        elif self.stage in [1, 2]:
            print('\n')
            print(f"ORIGIN POSITION: {pos}")
            self.origin = pos
            self.origin_is_set = True
            self.btindex = 0

            total_calculations[0] = 0

            t1 = time.time()
            self.poly.set_origin_and_calculate_divisions(self.origin)
            t2 = time.time()
            print(f'\nPOLY STATS --------------- ')
            print(f'TIME: {round(t2-t1,3)} seconds')
            # print(f'CALCULATED {total_calculations[0]} INTERSECTIONS IN {round(t2-t1,2)} seconds')
            # print(f'CALLED MODULO {total_calculations[1]} times')
            print(f'POLYGON AREA: {self.poly.area}')
            print(f'NUMBER OF SLICES: {len(self.poly.slices)}')
            # print(f'INDEXES OF SOCIALSIT DIVISIONS: {[d.index for d in self.poly.future_socialist_divisions]}')
            sd = self.poly.socialised_divisions[0]

            print(f'area1: {sd.area1}')
            print(f'area2 = {sd.area2}')
            # print(f'case 2 potential div: {len(self.poly.potential_socialist_divisions_case_2)}')
            if self.stage == 1:
                self.advance_stage()
            self.update_screen()


    def show_load_poly_ui(self):
        #vfetch and prepare data for dialot
        poly_data = self.database.load_polygons()
        # print(poly_data)
        id_names = []
        for id in range(len(poly_data)):
            name = poly_data[id]["name"]
            id_names.append({"id" : id + 1, "name" : name})

        # run dialog
        select_poly_dialog = Select_poly_dialog_creator(id_names)
        selected_id = select_poly_dialog.exec()
        print(selected_id)
        if selected_id != 0:
            polyline = poly_data[selected_id - 1]['points']
            self.set_poly(polyline)

        # print(selected)
        # print('exexutes')

    def set_poly(self, polyline, origin = (50, 50)):
        self.polyline = polyline
        self.mouse_near = True
        self.stage = 0
        self.click_event(polyline[0])
        # self.click_event(origin)

    def load_poly_and_origin_from_local_file(self, data):
        poly = data[0]
        origin = data[1]
        self.polyline = poly
        self.mouse_near = True
        self.stage = 0
        self.click_event(poly[0])
        self.click_event(origin)

    def save_poly(self, name):
        print(name)
        # name = self.database_ui.poly_name_line_edit.text()
        self.database.save_poly(name, self.poly.points)

    def count_pixels(self):
        self.display_socialised_division = True
        self.is_counting_pixels = True
        self.render_area.is_counting_pixels = True
        self.update_render_area()

        pm = self.render_area.grab()

        self.is_counting_pixels = False
        self.render_area.is_counting_pixels = False
        self.update_render_area()

        fname = 'temp_r_area.tif'
        pm.save(fname, 'tif')
        img = cv.imread(fname)

        blue = np.sum(img[:,:,0] == 255)
        green = np.sum(img[:,:,1] == 255)
        red = np.sum(img[:,:,2] == 255)

        print()
        print('COUNTING PIXELS' + '-'*10)
        print(f'red PIXELS: {red}')
        print(f'green PIXELS: {green}')
        print(f'TOTAL PIXELS = {red + green}')
        d = abs(red - green)
        print(f'abs delta: {d}')
        print(f'rel delta: {round(d / (red + green) * 100, 2)}%')

        cv.imshow('Counting Pixels', img)
        # k = cv.waitKey(0)

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

        ds = div.slices1[0]
        self.division_rays = [ds.ray1.gen_line_tuple(), ds.ray2.gen_line_tuple()]

    def update_screen(self):
        if self.stage == 2:
            # self.display_bowtie_data_gen()
            # self.display_ray_data_gen()
            # self.gen_slice_display()
            self.display_division()
            self.update_graph()
        self.update_render_area()

    def update_graph(self):
        return
        try:
            sd = self.poly.potential_socialist_divisions_case_2[0]
            data = sd.bowtie.area_per_vec
            # data = []
            # print(data)
            ind = range(len(data))
            print(f'indexes: {ind}')
            print(len(sd.bowtie.area_per_vec))
            self.plot_widget.plot1.setData(ind, data)
        except:
            print('the rgraph widget did not update!! 281 programlogic.py')
            self.plot_widget.plot1.setData([], [])
            pass

        # self.po
        # indexes = range(len(self.poly.slices))

        # a1 = [d.area1 for d in self.poly.divisions]
        # a2 = [d.area2 for d in self.poly.divisions]
        # a3 = [d.total_area for d in self.poly.divisions]

        # self.plot_widget.plot1.setData(indexes, a1)
        # self.plot_widget.plot2.setData(indexes, a2)
        # self.plot_widget.plot3.setData(indexes, a3)

        # self.plot_widget.set_line2(self.poly.future_socialist_divisions[0].index)
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
            blue = Paint_Kit(QPen('blue'))
            purple = Paint_Kit(QPen('purple'))
            pink = Paint_Kit(QPen(Qt.PenStyle.NoPen), QBrush('pink', Qt.CrossPattern))
            orange = Paint_Kit(QPen('orange'))

            blackfill = Paint_Kit(brush = QBrush(Qt.black))

            # redfill = Paint_Kit(QPen(Qt.PenStyle.NoPen), brush = QBrush(Qt.red))
            # greenfill = Paint_Kit(QPen(Qt.PenStyle.NoPen), brush = QBrush(Qt.green))

            redfill = Paint_Kit(QPen(Qt.red), brush = QBrush(Qt.red))
            greenfill = Paint_Kit(QPen(Qt.green), brush = QBrush(Qt.green))

            if self.origin_is_set:
                black.points.append(self.origin)

                if not self.display_socialised_division:
                    green.polygons += self.division_shapes_1
                    red.polygons += self.division_shapes_2
                    blue.lines.append(self.division_rays[0])
                    blue.lines.append(self.division_rays[1])
                    pink.polygons += self.pink_center_shapes
                else:
                    sd = self.poly.socialised_divisions[0]
                    green.polygons += [s.tup for s in sd.shapes1]
                    red.polygons += [s.tup for s in sd.shapes2]

                blackfill.polygons.append(self.polyline)

                s = [a.gen_line_tuple() for a in self.poly.rlist]
                # print(s)
                # orange.lines += s
                if self.display_socialised_division:
                    orange.lines += [s[-1]]
                    purple.lines += [a.gen_line_tuple() for a in self.poly.math_ray_list]
                    if self.poly.rung0 is not None:
                        purple.lines.append(self.poly.rung0.segment.gen_tuple())

            for color in [black, red, green, blue, pink, orange, purple]:
                draw_packets.append(color)

            if self.is_counting_pixels:
                redfill.polygons = red.polygons
                greenfill.polygons = green.polygons
                draw_packets = [redfill, greenfill]

        self.render_area.draw_packets = draw_packets
        self.render_area.translation = self.live_translation_amount.tolist()
        self.render_area.view_scale = self.scale_amount
        self.render_area.update()