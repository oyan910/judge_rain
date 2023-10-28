import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QListWidget, QFileDialog, QWidget
from PyQt5.QtCore import Qt

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("视频播放器")
        self.setGeometry(100, 100, 800, 600)

        self.play_button = QPushButton("选择并播放视频")
        self.play_button.clicked.connect(self.open_video)

        self.video_list = QListWidget()
        self.video_list.setFlow(QListWidget.TopToBottom)

        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        layout.addWidget(self.video_list)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.video_capture = None

    def open_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        video_file, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "Video Files (*.avi *.mp4 *.mov *.mkv)", options=options)

        if video_file:
            # 添加选定的视频文件路径到播放列表
            self.video_list.addItem(video_file)

    def play_video(self, video_path):
        if self.video_capture is not None:
            self.video_capture.release()
        self.video_capture = cv2.VideoCapture(video_path)

        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if not ret:
                break

            # 在这里将帧(frame)显示在你的播放区域，这部分需要根据你的界面布局来实现

            # 更新界面以显示下一帧
            QApplication.processEvents()
            # 添加适当的等待时间，以控制视频的帧率
            cv2.waitKey(30)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())
