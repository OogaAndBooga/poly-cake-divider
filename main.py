from __future__ import annotations

from PySide6.QtWidgets import (QApplication, QGridLayout,
                               QLabel, QWidget, QPushButton)

from polygon import Polygon
from programlogic import Program_Logic
from render_area import RenderArea
from graph_widget import Plot_Widget

from test_polygons import *

# id_role = Qt.ItemDataRole.UserRole
# print('IDROLEEEEEEEEEEEEEEE',id_role)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.plot_widget = Plot_Widget()
        self.render_area = RenderArea()
        self.program_logic = Program_Logic()

        self.render_area.pass_program_logic_instance(self.program_logic)
        self.program_logic.pass_render_area_instance(self.render_area)
        self.program_logic.pass_plot_widget_instance(self.plot_widget)

        #simulate user input
        l = {
            1:[poly1, (236, 367)],
            2:[poly2, (398, 375)],#(209, 314)(398, 375)
            4:[poly4, origin4] 
        }
        n = 4
        if n:
            poly = l[n][0]
            origin = l[n][1]
            self.program_logic.polyline = poly
            self.program_logic.mouse_near = True
            self.program_logic.click_event(poly[0])
            self.program_logic.click_event(origin)

        main_layout = QGridLayout()

        #what does this do?
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(3, 1)

        main_layout.addWidget(self.render_area, 0, 0, 1, 4)
        main_layout.addWidget(self.plot_widget, 1, 1, 1, 1)
        main_layout.setRowMinimumHeight(1, 6)
        self.setLayout(main_layout)

        self.setWindowTitle("Basic Drawing")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
