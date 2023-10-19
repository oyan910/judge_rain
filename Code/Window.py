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
        self.playing = False    # 播放状态
        self.Time = QTimer(self)
        self.Time.timeout.connect(self.update_frame)
        self.Time.start(1)
        self.cap = cv2.VideoCapture(0)
        self.Input = self.Win1      # 输入摄像头/原始视频展示帧
        self.Output = self.Win2     # 输出画面
        self.Camera = self.btn_ca   # 开启摄像头
        self.Judge = self.judge     # 开始分析
        self.Addfile = self.add_to_file  # 加入视频文件
        self.State = self.state          # 状态显示
        self.Start = self.btn_start  # 开始播放(视频)
        self.State.setText("未开启")
        self.to_connect()
    def to_connect(self):
        self.Camera.clicked.connect(self.res_btn_camera)
    def res_btn_camera(self):
        if self.playing:
            self.Time.stop()
            self.Camera.setText("开启摄像头")

            self.State.setText("未开启")
        else:
            self.Time.start(1)
            self.Camera.setText("关闭摄像头")
            self.State.setText("<font color = 'red'>摄像头开启</font>")
        self.playing = not self.playing
    def update_frame(self):
        ret, frame = self.cap.read()
        if self.playing:
            if ret:
                # 转换为RGB格式
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame_rgb.shape
                bytes_per_line = 3 * width

                # 创建Qt图像
                q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)

                # 显示视频帧
                self.Input.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec_()