# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'poly_database_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget, QSpacerItem)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        # Frame.resize(249, 106)
        self.verticalLayout = QVBoxLayout(Frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.load_poly_button = QPushButton(Frame)
        self.load_poly_button.setObjectName(u"load_poly_button")

        self.verticalLayout.addWidget(self.load_poly_button)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.save_poly_button = QPushButton(Frame)
        self.save_poly_button.setObjectName(u"save_poly_button")

        self.horizontalLayout_2.addWidget(self.save_poly_button)

        self.poly_name_line_edit = QLineEdit(Frame)
        self.poly_name_line_edit.setObjectName(u"poly_name_line_edit")

        self.horizontalLayout_2.addWidget(self.poly_name_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        #TODO DO NOT DELETE!!!

        # self.save_point_button = QPushButton(Frame)
        # self.save_point_button.setObjectName(u"save_point_button")

        # self.horizontalLayout.addWidget(self.save_point_button)

        # self.save_point_line_edit = QLineEdit(Frame)
        # self.save_point_line_edit.setObjectName(u"save_point_line_edit")

        # self.horizontalLayout.addWidget(self.save_point_line_edit)


        # self.verticalLayout.addLayout(self.horizontalLayout)

        #TODO DO NOT DELETE

        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)

    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.load_poly_button.setText(QCoreApplication.translate("Frame", u"Load Polygon From Database", None))
        self.save_poly_button.setText(QCoreApplication.translate("Frame", u"Save Polygon To Database", None))
        # self.save_point_button.setText(QCoreApplication.translate("Frame", u"Save Point", None))
    # retranslateUi

    def connect_signals(self, program_logic):
        self.load_poly_button.clicked.connect(program_logic.show_load_poly_ui)
        self.poly_name_line_edit.editingFinished.connect(self.save_poly_button.animateClick)
        def save_poly():
            name = self.poly_name_line_edit.text()
            program_logic.save_poly(name)
        self.save_poly_button.clicked.connect(save_poly)

    def get_poly_name(self):
        return self.poly_name_line_edit.text()

