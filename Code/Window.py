import sys
import cv2
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QImageReader


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('window.ui', self)

if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()