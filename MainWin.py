# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import os
import sys
import pymysql

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog ,QWidget, QFrame, QCheckBox, QLineEdit, QLabel, QPushButton, QTextBrowser, QTableWidget,  QAbstractItemView, QTableWidgetItem, QMenuBar
from NewConnDialog import NewConnDialog


class Ui_MainWindow(QtWidgets.QMainWindow):        
    def __init__(self,parent=None):
        super(Ui_MainWindow,self).__init__()
        # QtWidgets.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #新建菜单
        self.action_new = QtWidgets.QAction(MainWindow)
        self.action_new.setObjectName("action_new")
        self.menu.addAction(self.action_new)
        self.action_new.triggered.connect(self.newConn)

        #导入
        self.action_import = QtWidgets.QAction(MainWindow)
        self.action_import.setObjectName("action_import")
        self.menu.addAction(self.action_import)
        self.action_import.triggered.connect(self.importConn)

        #打开
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.menu.addAction(self.action_open)
        self.action_open.triggered.connect(self.openConn)


        self.menubar.addAction(self.menu.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "新建Mysql连接"))
        self.menu.setTitle(_translate("MainWindow", "文件(&F)"))

        self.action_new.setText(_translate("MainWindow", "新建"))
        self.action_new.setShortcut(_translate("MainWindow", "Ctrl+N"))

        self.action_import.setText(_translate("MainWindow", "导入"))
        self.action_import.setShortcut(_translate("MainWindow", "Ctrl+I"))

        self.action_open.setText(_translate("MainWindow", "打开(&O)"))
        self.action_open.setShortcut(_translate("MainWindow", "Ctrl+O"))

    def newConn(self):
        self.conn=NewConnDialog()
        self.conn.Signal_OpenDb.connect(self.openDb)
        resutl=self.conn.exec_()
        # self.conn.raise_()

    def importConn(self):
        file,ok=QFileDialog.getOpenFileName(None, 'Save File', os.getenv('HOME'))
    
    def openConn(self):
        pass
    
    def openDb(self,data):
        print(data) 


if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/ji.ico"))
    ui=Ui_MainWindow()
    ui.show()

    sys.exit(app.exec_())
