import time
from PyQt5.QtCore import QThread
from logger.logging_utils import text_writer
from PyQt5 import QtWidgets

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

                #传入标签名，和图片路径，和转换路径和class,把进度条也传进去
                rtv = self.CGl_model.change_label(self.contrl.controls_view_value["before_comboBox"], self.contrl.controls_view_value["after_comboBox"],
                        self.contrl.controls_view_value["labelname_lineEdit"].split(","), self.contrl.controls_view_value["before_pic_lineEdit"], 
                        self.contrl.controls_view_value["before_label_lineEdit"], self.contrl.controls_view_value["after_label_lineEdit"], self.CGl_view.progressBar)
                #print(rtv)
                if rtv is None:
                    self.CGl_model.thread_flag = 0
                    QtWidgets.QMessageBox.warning(None, "警告", "未知错误")


                self.CGl_model.thread_flag = 0

            time.sleep(1)





# 创建控制器
class Controller:
    def __init__(self, model, view):

        self.model = model
        self.view = view
        self.init_PYqt_View() #读取配置文件中的默认配置，每次转换都会记录下来
        self.ctflag = 0

        self.setSlot()


        self.controls_view = {
            "labelname_lineEdit": self.view.labelname_lineEdit.text(),
            "before_comboBox": self.view.before_comboBox.currentText(),
            "after_comboBox": self.view.after_comboBox.currentText(),
            "before_label_lineEdit": self.view.before_label_lineEdit.text(),
            "before_pic_lineEdit": self.view.before_pic_lineEdit.text(),
            "after_label_lineEdit": self.view.after_label_lineEdit.text()
        }

        self.controls_view_alia = {
            "labelname_lineEdit": "类别标签为空",
            "before_comboBox": "转换标签为空",
            "after_comboBox": "转换标签为空",
            "before_label_lineEdit": "转换标签路径为空",
            "before_pic_lineEdit": "转换图片路径为空",
            "after_label_lineEdit": "转换后图片路径为空"
        }


        self.controls_view_value = {}  #最新的数据


    def update_controls_view(self):
                # 获取各个控件的值并赋给字典
        self.controls_view_value["labelname_lineEdit"] = self.view.labelname_lineEdit.text()
        self.controls_view_value["before_comboBox"] = self.view.before_comboBox.currentText()
        self.controls_view_value["after_comboBox"] = self.view.after_comboBox.currentText()
        self.controls_view_value["before_label_lineEdit"] = self.view.before_label_lineEdit.text()
        self.controls_view_value["before_pic_lineEdit"] = self.view.before_pic_lineEdit.text()
        self.controls_view_value["after_label_lineEdit"] = self.view.after_label_lineEdit.text()

        return self.controls_view_value


    def setSlot(self):
        # 绑定选择文件夹槽函数
        self.view.before_label_pushButton.clicked.connect(lambda: self.select_folder(self.view.before_label_lineEdit, 'folder_path1'))
        self.view.before_pic_pushButton.clicked.connect(lambda: self.select_folder(self.view.before_pic_lineEdit, 'folder_path2'))
        self.view.after_label_pushButton.clicked.connect(lambda: self.select_folder(self.view.after_label_lineEdit, 'folder_path3'))


        # 校验
        self.view.jy_pushButton.clicked.connect(self.check_folder_data)

        # 转换按钮
        self.view.zh_pushButton.clicked.connect(self.Label_change)
        # 转换线程
        self.ChangeLabel_t = ChangeLabel_Thread(self, self.model, self.view)
        self.ChangeLabel_t.start()


    #读取配置config.json中的数据
    def init_PYqt_View(self):
        dist_info = self.model.Read_Record_Pyqt_info()
        if dist_info != None:
            #print(dist_info)
            self.view.labelname_lineEdit.setText(dist_info["labelname_lineEdit"])
            self.view.before_comboBox.setCurrentText(dist_info["before_comboBox"])
            self.view.after_comboBox.setCurrentText(dist_info["after_comboBox"])
            self.view.before_label_lineEdit.setText(dist_info["before_label_lineEdit"])
            self.view.before_pic_lineEdit.setText(dist_info["before_pic_lineEdit"])
            self.view.after_label_lineEdit.setText(dist_info["after_label_lineEdit"])
            if self.view.after_label_lineEdit.text() == '':
                self.view.after_label_lineEdit.setText("可不选择转化后文件夹")




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


    def Label_change_init(self):

        # 1. 检测转换的标签，路径是否为空，转换后的标签是否为空
        update_data = self.update_controls_view() #更新数据
        print(update_data)
        # 找到值为空的键并打印出
        for key, value in update_data.items():
            if value == "":
                return (f"'{self.controls_view_alia[key]}' 的值为空")
        # 2. 检测是否为空并输出对应的控件名称


            

                

        return 0

    def Label_change(self):  # sourcery skip: lift-duplicated-conditional
        self.view.zh_pushButton.setDisabled(True)
        rtv = self.Label_change_init()
        if  rtv !=0:
            self.view.zh_pushButton.setEnabled(True)
            QtWidgets.QMessageBox.warning(None, "警告", rtv)
            return 0


        self.controls_view_value["labelname_lineEdit"] = self.view.labelname_lineEdit.text()
        self.controls_view_value["before_comboBox"] = self.view.before_comboBox.currentText()
        self.controls_view_value["after_comboBox"] = self.view.after_comboBox.currentText()
        self.controls_view_value["before_label_lineEdit"] = self.view.before_label_lineEdit.text()
        self.controls_view_value["before_pic_lineEdit"] = self.view.before_pic_lineEdit.text()
        self.controls_view_value["after_label_lineEdit"] = self.view.after_label_lineEdit.text()

        # # 1. 检测所有参数是否正确
        rtv = self.model.check_info_label(self.controls_view_value["before_comboBox"], self.controls_view_value["after_comboBox"], 
                    self.controls_view_value["labelname_lineEdit"],self.controls_view_value["before_pic_lineEdit"], self.controls_view_value["before_label_lineEdit"] )
        if rtv < 0:
            QtWidgets.QMessageBox.warning(None, "警告", self.model.error_messages[rtv])
        


        # # 2. 记录所有值
        self.model.Write_Record_Pyqt_info(str(self.update_controls_view()))


        self.model.thread_flag = 1  #启动线程工作


        self.view.zh_pushButton.setEnabled(True)

