import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import nigga
import os


class FirstForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 800, 600)

        self.btn = QPushButton("ОК", self)
        self.btn.move(150, 0)
        self.btn.resize(80, 52)
        self.btn.clicked.connect(self.show_map)

        self.edit = QLineEdit(self)
        self.edit.setText("55.02131,30.23123")
        self.edit.move(0, 0)

        self.edit2 = QLineEdit(self)
        self.edit2.setText("4")
        self.edit2.move(0, 30)

        self.label = QLabel(self)
        self.label.move(0, 100)

    def show_map(self):
        image = nigga.give_me_an_image(self.edit.text(), self.edit2.text())
        self.label.setPixmap(QPixmap(image))
        self.label.resize(self.label.sizeHint())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.edit2.setText(str(max(0, int(self.edit2.text()) - 1)))
            self.show_map()
        elif event.key() == Qt.Key_PageUp:
            self.edit2.setText(str(min(17, int(self.edit2.text()) + 1)))
            self.show_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FirstForm()
    form.show()
    sys.exit(app.exec())
