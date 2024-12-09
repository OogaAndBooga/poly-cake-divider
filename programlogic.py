from math import dist

class Program_Logic():
    stage = 0
    polyline = [] # before creation of polygon
    mouse_near = False # mouse within a certain distance to polyline origin
    origin = (0, 0)
    MOUSENEARDIST = 10

    # points = []

    def __init__(self):
        pass

    def pass_render_area_instance(self, r_area_instance):
        self.render_area = r_area_instance

    # def update_stage(self):
    #     self.stage += 1

    def set_mouse_near(self, value):
        must_update = value != self.mouse_near
        self.mouse_near = value
        if must_update:
            self.draw()

    def mouse_move_event(self, pos):
        if len(self.polyline) > 2 and dist(self.polyline[0], pos) < self.MOUSENEARDIST:
            self.set_mouse_near(True)
        else:
            self.set_mouse_near(False)

    def click_event(self, pos):
        print(pos)
        if self.stage == 0:
            if not self.mouse_near:
                self.polyline.append(pos)
                self.draw() #function to send data to be displayed
            else:
                self.stage += 1
                self.poly = Polygon([p.toTuple() for p in self.polyline])
                print(self.polyline)
        elif self.stage == 1:
            self.origin = pos

    def draw(self):
        primitives = {'points' : [],
                      'polyline' : [],
                      'polygon' : []
                      }

        if self.stage == 0:
            #TODO bug if no points added and mouse near
            if len(self.polyline) == 1 or self.mouse_near:
                primitives['points'].append(self.polyline[0])
            if len(self.polyline) > 1:
                primitives['polyline'] = self.polyline
        elif self.stage == 1:
            primitives['polygon'] = self.polyline

        print('pcalssprim', primitives)
        self.render_area.primitives = primitives
        self.render_area.update()

            # drawP(self.origin, 5)
            # for p in self.int:
            #     drawP(p, 6)















