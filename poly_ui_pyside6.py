# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'poly_ui_v0.1.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,QLineEdit,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        # print('start------')
        if not Form.objectName():
            Form.setObjectName(u"Form")
        # Form.resize(152, 76)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMouseTracking(False)

        self.horizontalLayout.addWidget(self.comboBox)

        self.pb2 = QPushButton(text = 'count pixels')
        self.verticalLayout.addWidget(self.pb2)

        self.led = QLineEdit(text='(318, 276)')
        self.led.editingFinished.connect(self.led.clearFocus)
        self.verticalLayout.addWidget(self.led)

        self.pb3 = QPushButton(text = 'reset zoom')
        self.verticalLayout.addWidget(self.pb3)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Toggle poly display", None))
        self.label.setText(QCoreApplication.translate("Form", u"Load poly", None))
    # retranslateUi

    def set_combobox_options(self, options):
        for o in options:
            self.comboBox.addItem(str(o), (options[o]))

    def connect_signals(self, program_logic):
        self.pushButton.clicked.connect(program_logic.toggle_div_display)
        self.pb2.clicked.connect(program_logic.count_pixels)
        self.led.editingFinished.connect(lambda: program_logic.input_origin_as_string(str(self.led.text())))
        self.pb3.clicked.connect(program_logic.reset_pan_and_zoom)

        def load_poly():
            data = self.comboBox.itemData(self.comboBox.currentIndex())
            program_logic.load_poly_and_origin(data)
        self.comboBox.activated.connect(load_poly)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.connect_signals(lambda:print(1))
    Form.show()
    sys.exit(app.exec())