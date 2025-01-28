from __future__ import annotations

from PySide6.QtWidgets import (QApplication, QGridLayout,
                               QLabel, QWidget, QPushButton)
from PySide6.QtCore import Qt

# from polygon import Polygon   
from programlogic import Program_Logic
from render_area import RenderArea
from graph_widget import Plot_Widget
from poly_ui_pyside6 import Ui_Form

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
        premade_polys = {
            1:[poly1, (236, 367)],
            2:[poly2, (398, 375)],#(209, 314)(398, 375)
            3:[poly3, origin3],
            4:[poly4, origin4],
            5:[poly5, origin5]
        }
        n = 2
        if n:
            self.program_logic.load_poly_and_origin(premade_polys[n])

        main_layout = QGridLayout()

        Form = QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        ui.set_combobox_options(premade_polys)
        ui.connect_signals(self.program_logic)

        #what does this do?
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(3, 1)

        main_layout.addWidget(self.render_area, 0, 0, 1, 4)
        main_layout.addWidget(self.plot_widget, 1, 1, 1, 1)
        main_layout.addWidget(Form, 1, 0, 1, 1)
        main_layout.setRowMinimumHeight(1, 6)
        self.setLayout(main_layout)

        self.setWindowTitle("Cake Sharer")

        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
            key = event.key()
            pressed = None
            if key == Qt.Key_Q:
                sys.exit()
                pressed = None
            if key == Qt.Key_K:
                pressed = 'up'
                self.keysel = 999
            if key == Qt.Key_M:
                pressed = 'down'

            self.program_logic.key_press_event(pressed)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
