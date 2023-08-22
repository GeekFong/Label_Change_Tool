from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QCompleter, QProgressBar, QPlainTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import io


class View(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("标注文件转换工具")
        self.setGeometry(100, 100, 800, 300)  # 调整窗口高度以容纳日志布局

        # 设置窗口图标
        icon = QtGui.QIcon("./config/icon/icon.ico")
        self.setWindowIcon(icon)
        

        main_layout = QHBoxLayout()  # 使用水平布局
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

        # 左侧布局
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # 添加进度条和标签布局
        progress_layout = QHBoxLayout()
        left_layout.addLayout(progress_layout)

        self.label_progress = QLabel("转换进度条:", self)
        progress_layout.addWidget(self.label_progress)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)  # 设置进度条范围
        progress_layout.addWidget(self.progress_bar)

        # 标签输入框布局
        self.label_layout = QHBoxLayout()
        self.left_layout.addLayout(self.label_layout)

        self.label = QLabel("标签名:", self)
        self.label_layout.addWidget(self.label)

        self.label_text = QLineEdit(self)
        self.label_layout.addWidget(self.label_text)



        #--------------------------------------------

        # 文件夹选择框布局
        self.folder_layout1 = QHBoxLayout()
        self.left_layout.addLayout(self.folder_layout1)

        self.combo1 = QComboBox()
        self.combo1.addItems(["yolo-txt", "pascal-voc", "精灵标注助手-xml"])
        self.folder_layout1.addWidget(self.combo1)
        
        # 图片路径选择
        self.lineEdit_image = QLineEdit(self)
        self.folder_layout1.addWidget(self.lineEdit_image)

        self.button_image = QPushButton("选择图片路径", self)
        self.folder_layout1.addWidget(self.button_image)


        self.label_layout.addWidget(self.folder_layout1)


        #--------------------------------------------



        # folder_layout2 = QHBoxLayout()
        # left_layout.addLayout(folder_layout2)

        # self.combo2 = QComboBox()
        # self.combo2.addItems(["yolo-txt", "pascal-voc", "精灵标注助手-xml"])
        # folder_layout2.addWidget(self.combo2)

        # self.lineEdit1 = QLineEdit(self)
        # folder_layout2.addWidget(self.lineEdit1)

        # self.button1 = QPushButton("选择标注路径", self)
        # folder_layout2.addWidget(self.button1)

        # label_layout.addWidget(folder_layout2)



        # 图片路径选择布局
        image_layout = QHBoxLayout()
        left_layout.addLayout(image_layout)


        self.label2 = QLabel("存放转换后标注文件的路径:", self)
        image_layout.addWidget(self.label2)

        self.lineEdit2 = QLineEdit(self)
        image_layout.addWidget(self.lineEdit2)

        self.button2 = QPushButton("选择", self)
        image_layout.addWidget(self.button2)



        # 校验和转换按钮布局
        action_layout = QHBoxLayout()
        left_layout.addLayout(action_layout)

        self.button3 = QPushButton("校验", self)
        action_layout.addWidget(self.button3)

        self.button4 = QPushButton("转换", self)
        action_layout.addWidget(self.button4)
