from PySide6.QtCore import QLine, QPoint, QRect, QSize, Qt
from PySide6.QtGui import (QBrush, QPainter,
                           QPalette, QPen)

from PySide6.QtWidgets import QWidget

import sys

#TODO process keyboard inputs in Window widget

class RenderArea(QWidget):
    draw_packets = []
    black_background = False

    def __init__(self, parent=None):
        super().__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()

        self.antialiased = False
        self.transformed = True

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

        self.setFocusPolicy(Qt.NoFocus)
        self.setMouseTracking(True)

    def minimumSizeHint(self):
        return QSize(600, 600)

    #draw window size
    def sizeHint(self):
        return QSize(400, 400)

    def pass_program_logic_instance(self, program_instance):
        self.program = program_instance

    def mouseMoveEvent(self, event):
        self.program.mouse_move_event(event.pos().toTuple())

    def mousePressEvent(self, event):
        self.program.click_event(event.pos().toTuple())

    # def keyPressEvent(self, event):
            # self.keysel = 0
        # if key == Qt.Key_T:
        #     pressed = 'toggle'
        #     self.keysel = 999
        # if key == Qt.Key_Z:
        #     self.keysel += 1
        #     self.keysel %= len(self.redpolys)
        # if key == Qt.Key_R:
        #     pressed = 'reset'
            # print(f'KEYSEL: {self.keysel}')
        # print(f'\nKEYPRESS EVENT: {event}\n')

    def paintEvent(self, event):
        with QPainter(self) as painter:
            if self.black_background:
                b = QBrush(Qt.black)
                painter.fillRect(QRect(QPoint(0, 0), self.size()), b)

            def drawP(pos, r = 6):
                painter.drawEllipse(pos, r, r)
            for draw_packet in self.draw_packets:
                dp = draw_packet #TODO bad variable name
                painter.setPen(draw_packet.pen)
                painter.setBrush(draw_packet.brush)

                for p in dp.points:
                    drawP(QPoint(*p))
                for l in dp.lines:
                    painter.drawLine(QLine(*l[0], *l[1]))
                for plne in dp.polylines:
                    painter.drawPolyline( [QPoint(*p) for p in plne])
                for poly in dp.polygons:
                    painter.drawPolygon([QPoint(*p) for p in poly])

            # border
            if not self.black_background:
                painter.setPen(self.palette().dark().color())
                painter.setBrush(Qt.NoBrush)
                painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

            # # for poly in self.redpolys:
            # #     test = [QPoint(*p) for p in poly]
            # #     print('_', end = '')
            # #     if i == self.keysel:
            #         print(f'\b{i}',end='')
            #         painter.drawPolygon(test)
            #     if self.keysel == 999:
            #         painter.drawPolygon(test)
            #     i += 1
            # print()