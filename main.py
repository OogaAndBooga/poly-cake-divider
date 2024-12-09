# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the widgets/painting/basicdrawing example from Qt v5.x, originating from PyQt"""

# from PySide6 import QMath
# import PySide6
from PySide6.QtCore import QPoint, QRect, QSize, Qt, qVersion
from PySide6.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
                           QPainterPath, QPalette, QPen, QPixmap, QPolygon,
                           QRadialGradient)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QLabel, QSpinBox, QWidget)

# import basicdrawing_rc  # noqa: F401
# noqa: 1234
from polygon import Polygon
from programlogic import Program_Logic

from time import time
from math import dist

class RenderArea(QWidget):

    points = [QPoint(103, 186),
              QPoint(164, 84),
              QPoint(294, 89),
              QPoint(292, 235),
              QPoint(242, 320),
              QPoint(112, 311),
              QPoint(111, 249)]

    points = []

    primitives = {'points' : [],
                      'polyline' : [],
                      'polygon' : []
                      }

    # points = QPolygon([
    #     QPoint(40, 80),
    #     QPoint(50, 70),
    #     QPoint(90, 70)
    # ])


    def __init__(self, parent=None):
        super().__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()
        # self.pixmap = QPixmap()

        # self.shape = RenderArea.Polygon
        self.antialiased = False
        self.transformed = True
        # self.pixmap.load(':/image?s/qt-logo.png')

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

        self.setMouseTracking(True)

    def minimumSizeHint(self):
        return QSize(400, 400)

    #draw window size
    def sizeHint(self):
        return QSize(400, 400)

    def pass_program_logic_instance(self, program_instance):
        self.program = program_instance

    def mouseMoveEvent(self, event):
        self.program.mouse_move_event(event.pos().toTuple())

    def mousePressEvent(self, event):
        self.program.click_event(event.pos().toTuple())


    def paintEvent(self, event):

        print(event,self.primitives)

        def drawP(pos, r = 6):
            painter.drawEllipse(pos, r, r)


        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)

            painter.save()

            if self.primitives['points'] != []:
                for p in self.primitives['points']:
                    drawP(QPoint(*p))

            if self.primitives['polyline'] != []:
                painter.drawPolyline( [QPoint(*p) for p in self.primitives['polyline']])

            if self.primitives['polygon'] != []:
                painter.drawPolygon([QPoint(*p) for p in self.primitives['polygon']])

            painter.restore()

            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(0, 0, self.width() - 10, self.height() - 1))

id_role = Qt.ItemDataRole.UserRole
# print(id_role)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.render_area = RenderArea()
        self.program_logic = Program_Logic()

        self.render_area.pass_program_logic_instance(self.program_logic)
        self.program_logic.pass_render_area_instance(self.render_area)


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
