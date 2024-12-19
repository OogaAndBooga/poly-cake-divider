from math import dist
from polygon import Polygon
from data_structures import total_calculations

class Program_Logic():
    stage = 0
    polyline = [] # before creation of polygon
    mouse_near = False # mouse within a certain distance to polyline origin
    origin = None #one of the defining points for division
    origin_is_set = False
    MOUSENEARDIST = 10
    tempbowtiedata = None
    # points = []

    def __init__(self):
        pass

    def pass_render_area_instance(self, r_area_instance):
        self.render_area = r_area_instance

    def advance_stage(self):
        self.stage += 1
    # def update_stage(self):
    #     self.stage += 1

    def set_mouse_near(self, value):
        must_update = (value != self.mouse_near)
        self.mouse_near = value
        if must_update:
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
            # if not self.origin_is_set:
                #TODO better way of handling origin of rays
                print(f"ORIGIN POSITION: {pos}")
                self.origin = pos
                self.origin_is_set = True

                total_calculations[0] = 0
                self.tempbowtiedata = self.poly.gen_bowties(self.origin)

                self.update_screen()

    def update_screen(self):
        primitives = {'points' : [],
                      'polyline' : [],
                      'polygon' : []
                      }

        redlines = []

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
                redlines += self.tempbowtiedata

        print('PRIMITIVES SENT TO RENDERAREA', primitives)
        print(f'NUMBER OF RED ELEMENTS: {len(redlines)}')
        self.render_area.primitives = primitives
        self.render_area.redlines = redlines
        self.render_area.update()

            # drawP(self.origin, 5)
            # for p in self.int:
            #     drawP(p, 6)















