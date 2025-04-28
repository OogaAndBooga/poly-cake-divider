from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,QLineEdit,QDialog,QListWidget,QListWidgetItem,
    QWidget)

class List_item_with_info(QListWidgetItem):
    def __init__(self, id, text):
        super().__init__('')
        self.id = id
        # self.data = data
        self.setText(text)

class Select_poly_dialog_creator(QDialog):
    def __init__(self, id_names):
        super().__init__()
        self.setWindowTitle('Select polygon')
        self.layout = QVBoxLayout()
        self.poly_list = QListWidget()
        self.set_polys(id_names)
        self.layout.addWidget(self.poly_list)
        self.setLayout(self.layout)
        
        self.poly_list.itemDoubleClicked.connect(self.item_selected)

    def set_polys(self, id_names):
        self.items = []
        for p in id_names:
            self.items.append(List_item_with_info(text = p['name'], id = p['id']))
        # self.items = [List_item_with_info(id, data.name, data) for data, id in zip(named_polygons, range(len(named_polygons)))]
        # breakpoint()

        # self.poly_list.clear()
        for i in self.items:
            self.poly_list.addItem(i)

    def item_selected(self, item):
        self.done(item.id)
        # print(item_id)
        # for data, id in self.items:
        #     if id == item_id:

        # print(item)
        # # breakpoint()
        # print(item.id)
        

    # def

    
