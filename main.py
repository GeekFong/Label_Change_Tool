from PyQt5 import QtWidgets
import sys
from qt_material import apply_stylesheet
from Label_View import View_Labels_Change
from Label_Model import Model_labels_change
from Label_Controller import controller_label_change



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='light_red.xml')
    model = Model_labels_change.Model()
    view = View_Labels_Change.Ui_Label_Change_Tool_window()
    view_window = QtWidgets.QMainWindow()
    view.setupUi(view_window)
    controller = controller_label_change.Controller(model, view)
    view_window.show()
    sys.exit(app.exec_())