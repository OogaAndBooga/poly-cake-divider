# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the widgets/painting/basicdrawing example from Qt v5.x, originating from PyQt"""

# from PySide6 import QMath
# import PySide6
from PySide6.QtCore import QLine, QPoint, QRect, QSize, Qt, qVersion
from PySide6.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
                           QPainterPath, QPalette, QPen, QPixmap, QPolygon,
                           QRadialGradient)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QLabel, QSpinBox, QWidget)

from polygon import Polygon
from programlogic import Program_Logic
from render_area import RenderArea

from time import time
from math import dist

from test_polygons import *

id_role = Qt.ItemDataRole.UserRole
# print(id_role)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.render_area = RenderArea()
        self.program_logic = Program_Logic()

        self.render_area.pass_program_logic_instance(self.program_logic)
        self.program_logic.pass_render_area_instance(self.render_area)

        self.program_logic.polyline = poly1
        # self.program_logic.polyline = [(116, 206), (191, 75), (311, 149), (219, 344), (140, 359), (247, 227)]
        # self.program_logic.stage = 1

        main_layout = QGridLayout()
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(3, 1)
        main_layout.addWidget(self.render_area, 0, 0, 1, 4)
        main_layout.setRowMinimumHeight(1, 6)
        self.setLayout(main_layout)


        self.setWindowTitle("Basic Drawing")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
