# -*- coding: utf-8 -*- 
import sys
from MainWin import Ui_MainWindow;

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow ,QDesktopWidget,QApplication,QPushButton,QHBoxLayout,QWidget
from PyQt5.QtGui import QIcon
    
           
         
if __name__ == '__main__':    
    app=QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/ji.ico"))
    widget=QtWidgets.QMainWindow()
    form=Ui_MainWindow()
    form.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())