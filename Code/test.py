import cv2
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class CameraViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("摄像头查看器")
        self.layout = QVBoxLayout()

        self.camera_combo = QComboBox()
        self.camera_combo.addItem("选择摄像头")
        self.layout.addWidget(self.camera_combo)

        self.display_label = QLabel()
        self.layout.addWidget(self.display_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_camera)
        self.selected_camera = None

        # 使用 OpenCV 获取可用摄像头列表
        self.camera_list = [f'摄像头 {i}' for i in range(10) if cv2.VideoCapture(i).isOpened()]

        if self.camera_list:
            self.camera_combo.addItems(self.camera_list)

        self.camera_combo.currentIndexChanged.connect(self.change_camera)

        self.setLayout(self.layout)


    def change_camera(self, index):
        if index > 0:
            self.selected_camera = cv2.VideoCapture(index - 1)
            self.timer.start(10)  # 50ms 更新一次摄像头画面
        else:
            self.selected_camera = None
            self.timer.stop()
            self.display_label.clear()

    def show_camera(self):
        if self.selected_camera and self.selected_camera.isOpened():
            ret, frame = self.selected_camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QPixmap.fromImage(QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888))
                self.display_label.setPixmap(image)

def main():
    app = QApplication(sys.argv)
    viewer = CameraViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
