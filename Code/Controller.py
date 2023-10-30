from Window import Window
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5 import QtCore
from Judge import Judge
_translate = QtCore.QCoreApplication.translate  # 翻译函数
class Controller:
    def __init__(self):

        self.View = Window()
        self.J = Judge()
        self.playing = 0            # 是否开始输入标识
        self.judging = 0
        self.selected_camera = None     # 摄像头

        self.Time = QTimer()
        self.Time.timeout.connect(self.update_input)

        self.view_to_controller()
        self.btn_to_connect()
        self.get_camera_list()
        self.Cameralist.currentIndexChanged.connect(self.change_camera)


        pass

    def get_camera_list(self):
        # 获取摄像头列表
        self.camera_list = [f'摄像头 {i}' for i in range(10) if cv2.VideoCapture(i).isOpened()]
        self.Cameralist.addItem("选择摄像头")
        if self.camera_list:
            self.Cameralist.addItems(self.camera_list)

    def view_to_controller(self):
        # 将View 中的控件转到controller中
        self.btn_Camera = self.View.Camera
        self.State = self.View.State
        self.Input = self.View.Input
        self.Output = self.View.Output
        self.Judge  = self.View.Judge
        self.Addfile = self.View.Addfile
        self.Start = self.View.Start
        self.Cameralist = self.View.CameraList


    def change_camera(self, index):
        if index > 0:
            self.selected_camera = cv2.VideoCapture(index - 1)
            # self.Time.start(10)  # 50ms 更新一次摄像头画面
        else:
            self.selected_camera = None
            self.Time.stop()
            self.Input.clear()

    def btn_to_connect(self):
        # 一些按钮功能连接
        self.View.Camera.clicked.connect(self.btn_change_open)
        self.Addfile.clicked.connect(self.open_video)
        self.Judge.clicked.connect(self.to_judge)
        pass

    def btn_change_open(self):
        # 点击后打开摄像头
        if self.playing == 1:
            self.Time.stop()
            self.View.Camera.setText("开启摄像头")
            self.playing = 0
            self.State.setText("未开启")
        else:
            self.Time.start(1)
            self.View.Camera.setText("关闭摄像头")
            self.State.setText("<font color = 'red'>摄像头开启</font>")
            self.playing = 1
        pass


    def show_input(self):
        # 输入框展示
        pass

    def to_judge(self):
        # 开始分析按钮
        if self.judging == 0:
            self.Judge.setText("停止分析")
            self.judging = 1
        else:
            self.Judge.setText("开始分析")
            self.judging = 0
        pass

    def change_img(self):
        # 处理功能
        pass

    def show_output(self):
        # 显示输出结果
        pass

    def update_input(self):
        # 更新输入摄像头用的
        if self.selected_camera and self.selected_camera.isOpened():
            if self.playing != 0:
                ret, frame = self.selected_camera.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = QPixmap.fromImage(QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888))
                    self.Input.setPixmap(image)
                    if self.judging == 1:
                        is_flog = self.J._judge_flog(frame)
                        if is_flog:
                            print("有雾")
                        else:
                            print("没有")




    pass

    def win_to_show(self):
        self.View.show()

    def open_video(self):
        # 打开文件目录选择视频文件
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        video_file, _ = QFileDialog.getOpenFileName(self.View, "选择视频文件", "", "Video Files (*.avi *.mp4 *.mov *.mkv)", options=options)

        if video_file:
            try:
                print(type(video_file))
            #     # 添加选定的视频文件路径到播放列表

                self.playing = 2
                self.selected_camera = cv2.VideoCapture(video_file)
                self.Time.start(20)
            except Exception as e:
                print(f"Error opening video: {e}")

if __name__ == '__main__':
    app = QApplication([])
    win = Controller()
    win.win_to_show()
    app.exec_()