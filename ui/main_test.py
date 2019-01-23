# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from main import Ui_MainWindow 
import sys


class main_test(Ui_MainWindow):
    def __init__(self, parent=None):
        # super(main_test, self).__init__()
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = main_test()
    ui.show()

    sys.exit(app.exec_())
