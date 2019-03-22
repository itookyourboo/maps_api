import sys
from functools import partial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMainWindow, \
    QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import nigga
import os

Y_RATIO, X_RATIO = 178.25792, 422.4


class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_size = (600, 600)
        self.map_pos = (0, 140)
        self.map_size = (600, 450)
        self.layer_type = 'map'
        self.point = None

        self.setGeometry(300, 300, *self.window_size)
        self.setWindowTitle('maps api')

        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))

        # self.settings = QtWidgets.QMenu(self.menubar)
        # self.settings.setTitle('Настройки')

        self.layer = QtWidgets.QMenu(self)
        self.layer.setTitle("Слой карты")

        self.shema = QtWidgets.QAction(self)
        self.shema.setText("Схема")
        self.layer.addAction(self.shema)

        self.sputnik = QtWidgets.QAction(self)
        self.sputnik.setText("Спутник")
        self.layer.addAction(self.sputnik)

        self.gibrid = QtWidgets.QAction(self)
        self.gibrid.setText("Гибрид")
        self.layer.addAction(self.gibrid)

        self.shema.triggered.connect(partial(self.change_layer, 'map'))
        self.sputnik.triggered.connect(partial(self.change_layer, 'sat'))
        self.gibrid.triggered.connect(partial(self.change_layer, 'skl'))

        # self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.layer.menuAction())

        ok_x, search_x = 170, 260

        self.btn = QPushButton("ОК", self)
        self.btn.move(ok_x, 40)
        self.btn.resize(80, 52)
        self.btn.clicked.connect(self.show_map)

        self.edit = QLineEdit(self)
        self.edit.setText("55.02131,30.23123")
        self.edit.move(20, 40)
        self.edit.resize(140, 40)

        self.edit2 = QLineEdit(self)
        self.edit2.setText("4")
        self.edit2.move(20, 90)

        self.edit3 = QLineEdit(self)
        self.edit3.move(search_x, 40)

        self.btn3 = QPushButton("Искать", self)
        self.btn3.move(search_x + 110, 40)
        self.btn3.clicked.connect(self.search)

        self.btn4 = QPushButton("Сброс поискового результата", self)
        self.btn4.move(search_x, 70)
        self.btn4.resize(210, 30)
        self.btn4.clicked.connect(self.reset)

        self.cb = QCheckBox('Почтовый индекс', self)
        self.cb.resize(self.cb.sizeHint())
        self.cb.move(search_x + 215, 40)
        self.cb.stateChanged.connect(self.display_address)
        self.address_text = self.index_text = ''

        self.address = QLabel(self)
        self.address.move(search_x, 105)
        self.address.setText("")

        self.label = QLabel(self)
        self.label.move(*self.map_pos)

    def show_map(self):
        image = nigga.give_me_an_image(self.edit.text(), self.edit2.text(), self.layer_type,
                                       point=self.point)
        self.label.setPixmap(QPixmap(image))
        self.label.resize(self.label.sizeHint())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.edit2.setText(str(min(19, int(self.edit2.text()) + 1)))
        elif event.key() == Qt.Key_PageUp:
            self.edit2.setText(str(max(0, int(self.edit2.text()) - 1)))
        else:
            z = float(self.edit2.text())
            x, y = map(float, self.edit.text().split(','))
            scale = (2 ** (z - 1))
            if event.key() == Qt.Key_S:
                y = max(-85, y - Y_RATIO / scale)
            elif event.key() == Qt.Key_W:
                y = min(85, y + Y_RATIO / scale)
            elif event.key() == Qt.Key_A:
                x = max(-180, x - X_RATIO / scale)
            elif event.key() == Qt.Key_D:
                x = min(180, x + X_RATIO / scale)
            else:
                return
            self.edit.setText(f'{x},{y}')
        self.show_map()

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        if not (self.map_pos[0] <= x <= self.map_pos[0] + self.map_size[0]) or \
                not (self.map_pos[1] <= y <= self.map_pos[1] + self.map_size[1]):
            return
        if event.buttons() in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton]:
            z = self.get_zoom()
            scale = (2 ** (z - 1))
            x_k = (X_RATIO / scale) / self.map_size[0]
            y_k = (Y_RATIO / scale) / self.map_size[1]

            x = self.map_pos[0] + x - self.map_size[0] / 2
            y = self.map_pos[1] - y + self.map_size[1] / 2
            lat, lon = self.get_lonlat()
            lat, lon = lat + x * x_k, lon + y * y_k
            self.edit3.setText(f'{lat},{lon}')
            self.search(org=(event.buttons() == QtCore.Qt.RightButton))

    def display_address(self):
        if self.cb.isChecked() and self.index_text:
            self.address.setText(', '.join([self.address_text, self.index_text]))
        else:
            self.address.setText(self.address_text)
        self.address.resize(self.address.sizeHint())

    def change_layer(self, type):
        self.layer_type = type
        self.show_map()

    def search(self, org=False):
        search = self.edit3.text()
        if org:
            coords, self.address_text, self.index_text = *nigga.find_orginization(search), ''
        else:
            coords, self.address_text, self.index_text = nigga.find_object(search)
        if coords:
            self.point = coords
        if self.sender() is not None:
            self.edit.setText(coords)
        self.display_address()
        self.show_map()

    def reset(self):
        self.point = None
        self.edit3.setText("")
        self.address.setText("")
        self.address_text = self.index_text = ''
        self.show_map()

    def get_zoom(self):
        return int(self.edit2.text())

    def get_lonlat(self):
        return tuple(map(float, self.edit.text().split(',')))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FirstForm()
    form.show()
    sys.exit(app.exec())
