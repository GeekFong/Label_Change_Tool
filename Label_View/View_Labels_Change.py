# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\View_Labels_Change.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Label_Change_Tool_window(object):
    def setupUi(self, Label_Change_Tool_window):
        Label_Change_Tool_window.setObjectName("Label_Change_Tool_window")
        Label_Change_Tool_window.resize(858, 213)
        Label_Change_Tool_window.setMinimumSize(QtCore.QSize(858, 213))
        Label_Change_Tool_window.setMaximumSize(QtCore.QSize(858, 213))
        font = QtGui.QFont()
        font.setPointSize(10)

        # 创建主窗口对象
        self.main_window = Label_Change_Tool_window
        
        font = QtGui.QFont()
        font.setPointSize(10)
        
        # 设置窗口图标
        icon = QtGui.QIcon("./config/icon/icon.ico")
        self.main_window.setWindowIcon(icon)

        Label_Change_Tool_window.setFont(font)
        self.centralwidget = QtWidgets.QWidget(Label_Change_Tool_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 851, 211))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.all_verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.all_verticalLayout.setContentsMargins(2, 2, 2, 5)
        self.all_verticalLayout.setObjectName("all_verticalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget_3)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.all_verticalLayout.addWidget(self.progressBar)
        self.labelname_horizontalLayout = QtWidgets.QHBoxLayout()
        self.labelname_horizontalLayout.setObjectName("labelname_horizontalLayout")
        self.labelname_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.labelname_label.setObjectName("labelname_label")
        self.labelname_horizontalLayout.addWidget(self.labelname_label)
        self.labelname_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.labelname_lineEdit.setObjectName("labelname_lineEdit")
        self.labelname_horizontalLayout.addWidget(self.labelname_lineEdit)
        self.all_verticalLayout.addLayout(self.labelname_horizontalLayout)
        self.select_horizontalLayout = QtWidgets.QHBoxLayout()
        self.select_horizontalLayout.setContentsMargins(1, 1, 1, 3)
        self.select_horizontalLayout.setObjectName("select_horizontalLayout")
        self.before_verticalLayout = QtWidgets.QVBoxLayout()
        self.before_verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.before_verticalLayout.setContentsMargins(2, 2, 2, 5)
        self.before_verticalLayout.setSpacing(0)
        self.before_verticalLayout.setObjectName("before_verticalLayout")
        self.before_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.before_comboBox.setFont(font)
        self.before_comboBox.setObjectName("before_comboBox")
        self.before_comboBox.addItem("")
        self.before_comboBox.addItem("")
        self.before_comboBox.addItem("")
        self.before_verticalLayout.addWidget(self.before_comboBox)
        self.before_label_horizontalLayout = QtWidgets.QHBoxLayout()
        self.before_label_horizontalLayout.setObjectName("before_label_horizontalLayout")
        self.before_label_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.before_label_lineEdit.setObjectName("before_label_lineEdit")
        self.before_label_horizontalLayout.addWidget(self.before_label_lineEdit)
        self.before_label_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.before_label_pushButton.setObjectName("before_label_pushButton")
        self.before_label_horizontalLayout.addWidget(self.before_label_pushButton)
        self.before_verticalLayout.addLayout(self.before_label_horizontalLayout)
        self.before_pic_horizontalLayout = QtWidgets.QHBoxLayout()
        self.before_pic_horizontalLayout.setObjectName("before_pic_horizontalLayout")
        self.before_pic_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.before_pic_lineEdit.setObjectName("before_pic_lineEdit")
        self.before_pic_horizontalLayout.addWidget(self.before_pic_lineEdit)
        self.before_pic_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.before_pic_pushButton.setObjectName("pushButton")
        self.before_pic_horizontalLayout.addWidget(self.before_pic_pushButton)
        self.before_verticalLayout.addLayout(self.before_pic_horizontalLayout)
        self.before_verticalLayout.setStretch(0, 3)
        self.before_verticalLayout.setStretch(1, 1)
        self.before_verticalLayout.setStretch(2, 1)
        self.select_horizontalLayout.addLayout(self.before_verticalLayout)
        self.after_verticalLayout = QtWidgets.QVBoxLayout()
        self.after_verticalLayout.setContentsMargins(2, 2, 2, 5)
        self.after_verticalLayout.setObjectName("after_verticalLayout")
        self.after_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.after_comboBox.setFont(font)
        self.after_comboBox.setObjectName("after_comboBox")
        self.after_comboBox.addItem("")
        self.after_comboBox.addItem("")
        self.after_comboBox.addItem("")
        self.after_verticalLayout.addWidget(self.after_comboBox)
        self.after_label_horizontalLayout = QtWidgets.QHBoxLayout()
        self.after_label_horizontalLayout.setObjectName("after_label_horizontalLayout")
        self.after_label_lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.after_label_lineEdit.setObjectName("after_label_lineEdit")
        self.after_label_horizontalLayout.addWidget(self.after_label_lineEdit)
        self.after_label_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.after_label_pushButton.setObjectName("after_label_pushButton")
        self.after_label_horizontalLayout.addWidget(self.after_label_pushButton)
        self.after_verticalLayout.addLayout(self.after_label_horizontalLayout)
        self.select_horizontalLayout.addLayout(self.after_verticalLayout)
        self.all_verticalLayout.addLayout(self.select_horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.jy_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.jy_pushButton.setObjectName("jy_pushButton")
        self.horizontalLayout_2.addWidget(self.jy_pushButton)
        self.zh_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.zh_pushButton.setObjectName("zh_pushButton")
        self.horizontalLayout_2.addWidget(self.zh_pushButton)
        self.all_verticalLayout.addLayout(self.horizontalLayout_2)
        Label_Change_Tool_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(Label_Change_Tool_window)
        QtCore.QMetaObject.connectSlotsByName(Label_Change_Tool_window)

    def retranslateUi(self, Label_Change_Tool_window):
        _translate = QtCore.QCoreApplication.translate
        Label_Change_Tool_window.setWindowTitle(_translate("Label_Change_Tool_window", "Label_Change_Tool"))
        self.labelname_label.setText(_translate("Label_Change_Tool_window", "标签名"))
        self.before_comboBox.setItemText(0, _translate("Label_Change_Tool_window", "yolo-txt"))
        self.before_comboBox.setItemText(1, _translate("Label_Change_Tool_window", "pascal-voc"))
        self.before_comboBox.setItemText(2, _translate("Label_Change_Tool_window", "精灵标注助手-xml"))
        self.before_label_pushButton.setText(_translate("Label_Change_Tool_window", "选择标签路径"))
        self.before_pic_pushButton.setText(_translate("Label_Change_Tool_window", "选择图片路径"))
        self.after_comboBox.setItemText(0, _translate("Label_Change_Tool_window", "yolo-txt"))
        self.after_comboBox.setItemText(1, _translate("Label_Change_Tool_window", "pascal-voc"))
        self.after_comboBox.setItemText(2, _translate("Label_Change_Tool_window", "精灵标注助手-xml"))
        self.after_label_pushButton.setText(_translate("Label_Change_Tool_window", "选择输出标签路径"))
        self.jy_pushButton.setText(_translate("Label_Change_Tool_window", "校验"))
        self.zh_pushButton.setText(_translate("Label_Change_Tool_window", "转换"))
