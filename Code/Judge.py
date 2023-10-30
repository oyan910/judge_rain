from Window import Window
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFileDialog, QListWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QImageReader
import cv2
from PyQt5 import QtCore

class Judge:
    def __init__(self):
        self.has_rain = 0
        self.has_flog = 0
        pass

    def _judge_flog(self, image):
        # 分析状态
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        me = cv2.mean(gray)
        #print(f'图像平均数据:{me}')
        # 计算透射率（Transmission）
        mean_gray = me[0]  # 计算图像的平均亮度
        transmission = 1 - mean_gray / 255.0  # 计算透射率

        #print(f'当前透射率：{transmission}')
        # 阈值化透射率以判断是否有雾
        threshold = 0.4  # 设置透射率阈值
        has_haze = transmission <= threshold
        return has_haze



    def _dispose_rain(self):
        if self.has_rain:
            pass
        # 去雨
        pass

    def _dispose_flog(self):
        if self.has_flog:
            pass
        # 去雾
        pass