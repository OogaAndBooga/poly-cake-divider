# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the widgets/painting/basicdrawing example from Qt v5.x, originating from PyQt"""

from PySide6.QtCore import QPoint, QRect, QSize, Qt, qVersion
from PySide6.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
                           QPainterPath, QPalette, QPen, QPixmap, QPolygon,
                           QRadialGradient)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                               QLabel, QSpinBox, QWidget)

# import basicdrawing_rc  # noqa: F401

import time

class RenderArea(QWidget):
    points = []
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

    def minimumSizeHint(self):
        return QSize(400, 400)

    #draw window size
    def sizeHint(self):
        return QSize(300, 300)

    mclicks = 0
    def mousePressEvent(self, event):
        print(event.pos())
        # self.mclicks += 10
        self.points.append(event.pos())
        self.update()
        #trigers a redraw of schreen

    def paintEvent(self, event):

        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)

            painter.drawPolyline(RenderArea.points)

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
