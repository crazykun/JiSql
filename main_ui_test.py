# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.Ui_MainWindow import Ui_MainWindow


class main_ui_test(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(main_ui_test, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        # self.show()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = main_ui_test()
    ui.show()

    sys.exit(app.exec_())
