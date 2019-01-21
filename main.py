# -*- coding: utf-8 -*-


import os
import sys
import pymysql

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from NewConnDialog import NewConnDialog
from DBManager import DBManager
from Config import Config


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()
        # QtWidgets.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setupDb()

    def setupDb(self):
        self.conf = Config()  # 当前数据库的配置
        self.currentDB = ''  # 当前数据库类
        self.currentDBIndex = ''  # 当前数据库类 序号
        self.openDBs = []  # 所有打开的数据库
        self.currentTable = ''  # 当前打开的表
        self.openTables = []  # 所有打开的表
        self.currentLine = ''  # 当前行
        self.treeWidget=[]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

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
        MainWindow.setWindowTitle(_translate("MainWindow", "Mysql数据库管理工具"))
        self.menu.setTitle(_translate("MainWindow", "文件(&F)"))

        self.action_new.setText(_translate("MainWindow", "新建"))
        self.action_new.setShortcut(_translate("MainWindow", "Ctrl+N"))

        self.action_import.setText(_translate("MainWindow", "导入"))
        self.action_import.setShortcut(_translate("MainWindow", "Ctrl+I"))

        self.action_open.setText(_translate("MainWindow", "打开(&O)"))
        self.action_open.setShortcut(_translate("MainWindow", "Ctrl+O"))

    def newConn(self):
        self.conn = NewConnDialog()
        self.conn.Signal_OpenDb.connect(self.openConn)
        resutl = self.conn.exec_()
        # self.conn.raise_()

    def importConn(self):
        file, ok = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Save File', os.getenv('HOME'))


    def openConn(self, conname):
        conf = self.conf.cfg_get(conname)
        self.currentDB = DBManager(
            conf['conname'], conf['hostname'], conf['port'], conf['user'], conf['password'])
        re = self.currentDB.testConnect()
        if(re != 'Success'):
            self.conn.closeDialog()
            QMessageBox.information(self, '链接失败', re)
            return
        index = len(self.openDBs)
        if(index == 0):
            self.setupTabWidget()
        self.addTab(conname)
        self.currentDBIndex = index
        self.openDBs.append(self.currentDB)
        self.tabWidget.setCurrentIndex(index)
        dbList=self.currentDB.showDBs()        
        self.setupDbTree(index,dbList)

    def setupTabWidget(self):
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tabWidget.show()
    
    def addTab(self,tabName):
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab_"+tabName)
        self.tabWidget.addTab(self.tab, tabName)

    def setupDbTree(self, tabIndex,dbList):
        self.treeWidget.append("treeWidget_"+str(tabIndex))
        thisItem=self.treeWidget.index("treeWidget_"+str(tabIndex))
        thisItem = QtWidgets.QTreeWidget(self.tab)
        thisItem.setGeometry(QtCore.QRect(-1, 0, 181, 521))
        thisItem.setObjectName("treeWidget_"+str(tabIndex))
        thisItem.setHeaderHidden(True)
        item=[]
        for x in dbList:            
            i=QtWidgets.QTreeWidgetItem(thisItem)
            i.setText(0,x)
            item.append(i)
        thisItem.addTopLevelItems(item)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(thisItem.sizePolicy().hasHeightForWidth())
        thisItem.show()
        # thisItem.doubleClicked['QModelIndex'].connect(self.openItems())
    
    def openItems(self):
        print(11)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/ji.ico"))
    ui = Ui_MainWindow()
    ui.show()

    sys.exit(app.exec_())
