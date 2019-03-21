import sys
from functools import partial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import nigga
import os


class FirstForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layer_type = 'map'
        self.point = None

        self.setGeometry(300, 300, 800, 600)
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

        self.btn = QPushButton("ОК", self)
        self.btn.move(150, 40)
        self.btn.resize(80, 52)
        self.btn.clicked.connect(self.show_map)

        self.edit = QLineEdit(self)
        self.edit.setText("55.02131,30.23123")
        self.edit.move(20, 40)

        self.edit2 = QLineEdit(self)
        self.edit2.setText("4")
        self.edit2.move(20, 90)

        self.edit3 = QLineEdit(self)
        self.edit3.move(240, 40)

        self.btn3 = QPushButton("Искать", self)
        self.btn3.move(350, 40)
        self.btn3.clicked.connect(self.search)

        self.label = QLabel(self)
        self.label.move(0, 140)

    def show_map(self):
        image = nigga.give_me_an_image(self.edit.text(), self.edit2.text(), self.layer_type, point=self.point)
        self.label.setPixmap(QPixmap(image))
        self.label.resize(self.label.sizeHint())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.edit2.setText(str(min(17, int(self.edit2.text()) + 1)))
            self.show_map()
        elif event.key() == Qt.Key_PageUp:
            self.edit2.setText(str(max(0, int(self.edit2.text()) - 1)))
            self.show_map()
        elif event.key() == Qt.Key_S:
            z = float(self.edit2.text())
            x, y = map(float, self.edit.text().split(','))
            y -= 178.25792 / (2 ** (z - 1))
            y = max(-85, y)
            self.edit.setText(f'{x},{y}')
            self.show_map()
        elif event.key() == Qt.Key_W:
            z = float(self.edit2.text())
            x, y = map(float, self.edit.text().split(','))
            y += 178.25792 / (2 ** (z - 1))
            y = min(85, y)
            self.edit.setText(f'{x},{y}')
            self.show_map()
        elif event.key() == Qt.Key_A:
            z = float(self.edit2.text())
            x, y = map(float, self.edit.text().split(','))
            x -= 422.4 / (2 ** (z - 1))
            x = max(-180, x)
            self.edit.setText(f'{x},{y}')
            self.show_map()
        elif event.key() == Qt.Key_D:
            z = float(self.edit2.text())
            x, y = map(float, self.edit.text().split(','))
            x += 422.4 / (2 ** (z - 1))
            x = min(180, x)
            self.edit.setText(f'{x},{y}')
            self.show_map()

    def change_layer(self, type):
        self.layer_type = type
        self.show_map()

    def search(self):
        search = self.edit3.text()
        image, coords = nigga.find_object(search)
        self.point = coords
        self.edit.setText(coords)
        self.label.setPixmap(QPixmap(image))
        self.label.resize(self.label.sizeHint())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FirstForm()
    form.show()
    sys.exit(app.exec())
