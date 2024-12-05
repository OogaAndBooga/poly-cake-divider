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

from time import time
from math import dist
# def qpToTup(qpoint):
#     return (qpoint)


# class Program:
    # def __init__(self, render_area):



class RenderArea(QWidget):

    points = [QPoint(103, 186),
              QPoint(164, 84),
              QPoint(294, 89),
              QPoint(292, 235),
              QPoint(242, 320),
              QPoint(112, 311),
              QPoint(111, 249)]

    points = []

    origin = QPoint(0, 0)
    int = []
    stage = 0
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

    MouseNear = False
    finishedInput = False

    def setMouseNear(self, value):
        if value != self.MouseNear:
            self.update()
        self.MouseNear = value

    def mouseMoveEvent(self, event):
        if len(self.points) > 2 and dist(self.points[0].toTuple(), event.pos().toTuple()) < 10:
            self.setMouseNear(True)
        else:
            self.setMouseNear(False)

    def mousePressEvent(self, event):
        if self.stage == 0:
            if not self.MouseNear:
                self.points.append(event.pos())
            else:
                self.stage += 1
                self.poly = Polygon([p.toTuple() for p in self.points])
                print(self.points)
                # self.points.append(self.points[0])
                # self.finishedInput = True
        elif self.stage == 1:
            self.origin = event.pos()
            self.int = self.poly.gen_bowties(self.origin)
            self.int = [QPoint(*p) for p in self.int]
        self.update()
        #trigers a redraw of screen

    def paintEvent(self, event):

        def drawP(pos, r):
            painter.drawEllipse(pos, r, r)

        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)

            painter.save()
            # if self.finishedInput:
            #     # painter.translate(-200, -200)
            #     painter.rotate(time()*2)
            if self.stage == 0:
                painter.drawPolyline(RenderArea.points)
            elif self.stage == 1:
                painter.drawPolygon(self.points)
                drawP(self.origin, 5)
                for p in self.int:
                    drawP(p, 6)

            r = 4
            if self.MouseNear:
                painter.drawEllipse(self.points[0], r, r)

            if len(self.points) == 1:
                painter.drawEllipse(self.points[0], r, r)

            painter.restore()

            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(0, 0, self.width() - 10, self.height() - 1))

id_role = Qt.ItemDataRole.UserRole
# print(id_role)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self._render_area = RenderArea()

        main_layout = QGridLayout()
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(3, 1)
        main_layout.addWidget(self._render_area, 0, 0, 1, 4)
        main_layout.setRowMinimumHeight(1, 6)
        self.setLayout(main_layout)


        self.setWindowTitle("Basic Drawing")


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
