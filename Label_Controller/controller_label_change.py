from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSettings
import time
from PyQt5.QtCore import QThread
import logging

class ChangeLabel_Thread(QThread):
    def __init__(self,contrl, model, view):
        super().__init__()
        self.contrl = contrl
        self.CGl_model = model
        self.CGl_view = view

    def run(self):
        time.sleep(1)
        while True:
            
            if self.CGl_model.thread_flag == 1:
                #self.CGl_view.button4.setDisabled(True)
                if self.CGl_view.lineEdit2.text() == '':
                    self.CGl_view.lineEdit2.setText("可不选择转化后文件夹")


                selected_option1 = self.CGl_view.combo1.currentText() #转换前的标签
                selected_option2 = self.CGl_view.combo2.currentText() #转换前的标签

                # # 1. 检测所有参数是否正确
                rtv = self.CGl_model.check_info_label(selected_option1, selected_option2, self.CGl_view.label_text.text(),self.CGl_view.lineEdit_image.text(), self.CGl_view.lineEdit1.text())
                if rtv < 0:
                    QtWidgets.QMessageBox.warning(None, "警告", self.CGl_model.error_messages[rtv])
                    self.CGl_model.thread_flag = 0
                    self.CGl_view.button4.setEnabled(True)
                    self.CGl_model.jdt_flag = 0
                    continue

                my_dict = { 'class_type': self.CGl_view.label_text.text(), 
                            'combo1': selected_option1, 
                            'combo2': selected_option2,
                            'label_1': self.CGl_view.lineEdit1.text(),
                            'label_2': self.CGl_view.lineEdit2.text(),
                            'label_3': self.CGl_view.lineEdit_image.text(),
                        }

                # 2. 记录所有值
                self.CGl_model.Write_Record_Pyqt_info(str(my_dict))

                #传入标签名，和图片路径，和转换路径和class
                rtv = self.CGl_model.change_label(selected_option1, selected_option2, self.CGl_view.label_text.text().split(","),self.CGl_view.lineEdit_image.text(), self.CGl_view.lineEdit1.text(), self.CGl_view.lineEdit2.text())
                #print(rtv)
                if rtv is None:
                    QtWidgets.QMessageBox.warning(None, "警告", "未知错误")
                #self.CGl_view.button4.setEnabled(True)

                self.CGl_model.thread_flag = 2

            time.sleep(1)


class JDT_Thread(QThread):
    def __init__(self, model, view):
        super().__init__()
        
        self.Jdt_model = model
        self.Jdt_view = view
        self.cnt = 0

    def run(self):
        while True:
            if self.Jdt_model.jdt_flag == 1:
                self.cnt = self.cnt + 1
                self.Jdt_view.progress_bar.setValue(self.cnt)
            
            if self.cnt == 99:
                self.cnt = 99

            if self.Jdt_model.thread_flag == 2:
                self.Jdt_view.progress_bar.setValue(100)
                self.Jdt_model.jdt_flag = 0
                self.cnt = 0
                self.Jdt_view.button4.setEnabled(True)

            if  self.Jdt_model.thread_flag == 0:
                self.cnt = 0
                self.Jdt_view.progress_bar.setValue(self.cnt)
                
            time.sleep(1)

# 创建控制器
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.init_PYqt_View() #读取配置文件中的默认配置，每次转换都会记录下来
        self.ctflag = 0

        self.setSlot()

    def setSlot(self):
        # 绑定选择文件夹槽函数
        self.view.before_label_pushButton.clicked.connect(lambda: self.select_folder(self.view.before_label_lineEdit, 'folder_path1'))
        self.view.before_pic_pushButton.clicked.connect(lambda: self.select_folder(self.view.before_pic_lineEdit, 'folder_path2'))
        self.view.after_label_pushButton.clicked.connect(lambda: self.select_folder(self.view.after_label_lineEdit, 'folder_path3'))


        # #校验
        self.view.jy_pushButton.clicked.connect(self.check_folder_data)

    #读取配置config.json中的数据
    def init_PYqt_View(self):
        dist_info = self.model.Read_Record_Pyqt_info()
        if dist_info != -1:
            #print(dist_info)
            self.view.labelname_lineEdit.setText(dist_info["class_type"])
            self.view.before_comboBox.setCurrentText(dist_info["combo1"])
            self.view.after_comboBox.setCurrentText(dist_info["combo2"])
            self.view.before_label_lineEdit.setText(dist_info["label_1"])
            self.view.before_pic_lineEdit.setText(dist_info["label_2"])
            self.view.after_label_lineEdit.setText(dist_info["label_3"])
            if self.view.after_label_lineEdit.text() == '':
                self.view.after_label_lineEdit.setText("可不选择转化后文件夹")


        # #转换
        # self.view.button4.clicked.connect(self.Label_change)

        # self.ChangeLabel_t = ChangeLabel_Thread(self, model, view)
        # self.ChangeLabel_t.start()

        # # 进度条
        # self.JDT_Thread = JDT_Thread(model, view)
        # self.JDT_Thread.start()

        #logging.info("This is an info message...........")
        # self.view.logging.info("Controller")
        # self.view.logging.info("This is an info message.")
        # self.view.logging.warning("This is a warning message.")
        # self.view.logging.error("This is an error message.")






    def select_folder(self, target_widget, target_attribute):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly)

        if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
            folder_path = dialog.selectedFiles()[0]
            target_widget.setText(folder_path)
            setattr(self, target_attribute, folder_path)
            print(f"选择了文件夹路径为 {folder_path}")





    #检测两个文件夹中的数据是否相同
    def check_folder_data(self):
        # self.view.logger.warning("This is a debug message")
        # 1. 两个文件夹是否为空
        self.before_label_path = self.view.before_label_lineEdit.text()
        self.before_pic_path  = self.view.before_pic_lineEdit.text()


        if self.before_label_path == '' or self.before_pic_path == '':
            QtWidgets.QMessageBox.warning(None, "警告", "请选择文件夹")

        elif self.model.check_folder_for_jpg_images(self.before_pic_path) == -2:
            QtWidgets.QMessageBox.warning(None, "警告", "图片文件夹中存在非jpg格式的图片")
        else:
            # 检测两个文件夹是否有相同的文件夹数据，并且名字是否一一对应
            selected_option = self.view.before_comboBox.currentText()
            if self.model.compare_and_move_files(self.before_pic_path, self.before_label_path, self.model.alias_mapping[selected_option]) == 0:
                QtWidgets.QMessageBox.information(None, "消息", f"{self.before_pic_path}和{self.before_label_path}目前具有相同的文件数目，并且名字都相同")
            else:
                QtWidgets.QMessageBox.warning(None, "警告", "文件错误，确保图片为jpg图片")




    
    def Label_change(self):  # sourcery skip: lift-duplicated-conditional
        self.view.button4.setDisabled(True)
        self.model.thread_flag = 1
        self.model.jdt_flag = 1
        # self.view.button4.setDisabled(True)

        # selected_option1 = self.view.combo1.currentText() #转换前的标签
        # selected_option2 = self.view.combo2.currentText() #转换前的标签
        # # 1. 检测所有参数是否正确
        # rtv = self.model.check_info_label(selected_option1, selected_option2, self.view.label_text.text(),self.view.lineEdit_image.text(), self.view.lineEdit1.text())
        # if rtv < 0:
        #     QtWidgets.QMessageBox.warning(None, "警告", self.model.error_messages[rtv])
        
        # my_dict = { 'class_type': self.view.label_text.text(), 
        #             'combo1': selected_option1, 
        #             'combo2': selected_option2,
        #             'label_1': self.view.lineEdit1.text(),
        #             'label_2': self.view.lineEdit2.text(),
        #             'label_3': self.view.lineEdit_image.text(),
        #         }

        # # 2. 记录所有值
        # self.model.Write_Record_Pyqt_info(str(my_dict))

        # #传入标签名，和图片路径，和转换路径和class
        # self.model.change_label(selected_option1, selected_option2, self.view.label_text.text(),self.view.lineEdit_image.text(), self.view.lineEdit1.text(), self.view.lineEdit2.text())
        # self.view.button4.setEnabled(True)

