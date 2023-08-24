# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets
import sys
from qt_material import apply_stylesheet
from Label_View import View_Labels_Change
from Label_Model import Model_labels_change
from Label_Controller import controller_label_change



if __name__ == "__main__":
    # 创建应用程序实例
    app = QtWidgets.QApplication(sys.argv)
    
    # 应用样式
    apply_stylesheet(app, theme='light_red.xml')
    
    # 创建Model实例
    model = Model_labels_change.Model()
    
    # 创建主窗口视图实例
    view = View_Labels_Change.Ui_Label_Change_Tool_window()
    
    # 在主窗口上设置UI
    view_window = QtWidgets.QMainWindow()
    view.setupUi(view_window)
    
    # 创建控制器实例
    controller = controller_label_change.Controller(model, view)
    
    # 显示主窗口
    view_window.show()
    
    # 启动应用程序事件循环
    sys.exit(app.exec_())