from PySide6.QtCore import QLine, QPoint, QRect, QSize, Qt
from PySide6.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
                           QPainterPath, QPalette, QPen, QPixmap, QPolygon,
                           QRadialGradient)

from PySide6.QtWidgets import QWidget

import sys

#TODO process keyboard inputs in Window widget

class RenderArea(QWidget):
    points = []

    redlines = []
    primitives = {'points' : [],
                      'polyline' : [],
                      'polygon' : []
                      }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()

        self.antialiased = False
        self.transformed = True

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

        self.setFocusPolicy(Qt.StrongFocus)
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

    def keyPressEvent(self, event):
        key = event.key()
        pressed = None
        if key == Qt.Key_Q:
            sys.exit()
        if key == Qt.Key_K:
            pressed = 'up'
        if key == Qt.Key_M:
            pressed = 'down'
        print(f'\nKEYPRESS EVENT: {event}')

        self.program.key_press_event(pressed)

    def paintEvent(self, event):
        # print(event,self.primitives)

        def drawP(pos, r = 6):
            painter.drawEllipse(pos, r, r)


        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)

            painter.save()

            p = QPen()
            p.setColor('red')
            p.setWidth(3)
            painter.setPen(p)
            if self.redlines != []:
                # painter.setPen(self.palette().light().color())
                for l in self.redlines:
                    painter.drawLine(QLine(*l[0], *l[1]))

            painter.restore()

            if self.primitives['points'] != []:
                for p in self.primitives['points']:
                    drawP(QPoint(*p))

            if self.primitives['polyline'] != []:
                painter.drawPolyline( [QPoint(*p) for p in self.primitives['polyline']])

            if self.primitives['polygon'] != []:
                painter.drawPolygon([QPoint(*p) for p in self.primitives['polygon']])



            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(0, 0, self.width() - 10, self.height() - 1))
