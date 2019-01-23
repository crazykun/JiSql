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
        self.treeWidgets=[]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.pushButton_open = QtWidgets.QPushButton(MainWindow)
        self.pushButton_open.setText("打开")
        self.pushButton_open.setGeometry(QtCore.QRect(460, 350, 80, 27))
        self.pushButton_open.clicked.connect(self.newConn)


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

        #help
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.action_help.triggered.connect(self.aboutUs)
        self.menu_help.addAction(self.action_help)

        self.action_QT = QtWidgets.QAction(MainWindow)
        self.action_QT.setObjectName("action_QT")
        self.menu_help.addAction(self.action_QT)
        self.action_QT.triggered.connect(self.aboutQT)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mysql数据库管理工具"))
        self.menu.setTitle(_translate("MainWindow", "文件(&F)"))
        self.menu_help.setTitle(_translate("MainWindow", "帮助(H)"))

        self.action_new.setText(_translate("MainWindow", "新建"))
        self.action_new.setShortcut(_translate("MainWindow", "Ctrl+N"))

        self.action_import.setText(_translate("MainWindow", "导入"))
        self.action_import.setShortcut(_translate("MainWindow", "Ctrl+I"))

        self.action_open.setText(_translate("MainWindow", "打开(&O)"))
        self.action_open.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.action_help.setText(_translate("MainWindow", "关于我们"))
        self.action_QT.setText(_translate("MainWindow", "关于QT"))



    def newConn(self):
        self.conn = NewConnDialog()
        self.conn.Signal_OpenDb.connect(self.openConn)
        self.conn.exec_()
        # self.conn.raise_()

    def importConn(self):
        file, ok = QtWidgets.QFileDialog.getOpenFileName(None, 'Save File', os.getenv('HOME'))


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
        self.currentDBIndex = index
        self.openDBs.append(self.currentDB)
        dbList=self.currentDB.showDBs()  

        if(index == 0):
            self.setupBaseUi(self,dbList)
        else:
            self.addTab(conname)
            self.setupDbTree(index,dbList)
        self.tabWidget.setTabText(index,conname)
        self.tabWidget.setCurrentIndex(index)
       

    def setupBaseUi(self,MainWindow,dbList):
        self.pushButton_open.hide()
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        #大tab页
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")        
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        #添加tree
        self.setupDbTree(0,dbList)
        
        #右侧
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 60))
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setText("执行")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButton.setObjectName("pushButton")
        # self.pushButton.setStyleSheet("background:qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.verticalLayout.addWidget(self.tabWidget_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.tabWidget.tabCloseRequested['int'].connect(self.closeDbTab)
        self.tabWidget_2.tabCloseRequested['int'].connect(self.closeTablesTab)

        MainWindow.setCentralWidget(self.centralwidget)


    
    def addTab(self,tabName):
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab_"+tabName)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.addTab(self.tab, tabName)

    def closeDbTab(self,index):
        self.tabWidget.removeTab(index)

    def setupDbTree(self, tabIndex,dbList):
        self.treeWidgets.append("treeWidget_"+str(tabIndex))
        thisItem = QtWidgets.QTreeWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(thisItem.sizePolicy().hasHeightForWidth())
        thisItem.setSizePolicy(sizePolicy)
        thisItem.setMinimumSize(QtCore.QSize(200, 0))
        thisItem.setObjectName("treeWidget_"+str(tabIndex))
        thisItem.setHeaderHidden(True)
        self.horizontalLayout_4.addWidget(thisItem)

        items=[]
        for x in dbList:            
            i=QtWidgets.QTreeWidgetItem(thisItem)
            i.setText(0,x)
            items.append(i)
        thisItem.addTopLevelItems(items)

        thisItem.itemDoubleClicked['QTreeWidgetItem*','int'].connect(self.clickTreeItem)
        # thisItem.show()
        self.setCentralWidget(thisItem)
        
    def clickTreeItem(self,item,column):
        if(item.parent() is  None):
            database=item.text(column)
            tables=self.currentDB.showTables(database)
            items=[]
            for x in tables:            
                i=QtWidgets.QTreeWidgetItem(item)
                i.setText(0,x)
                items.append(i)
            item.addChildren(items)
        else:
            table=item.text(column)
            columns=self.currentDB.showColumns(table)
            dataModel=self.currentDB.getList(table,columns)
            self.setupTableData(table,dataModel)
    
    def setupTableData(self,table,dataModel):
        if table in self.openTables:
            print(self.openTables.index(table))
            self.tabWidget_2.setCurrentIndex(self.openTables.index(table))
        else:
            this = self.__dict__
            num=len(self.openTables) 
            tab_tmp = QtWidgets.QWidget()
            tab_tmp.setObjectName("tab_tmp")
            self.verticalLayout_3 = QtWidgets.QVBoxLayout(tab_tmp)
            self.verticalLayout_3.setObjectName("verticalLayout_3")
            self.tableView = QtWidgets.QTableView(tab_tmp)
            self.tableView.setObjectName("tableView")
            self.tableView.setModel(dataModel)
            self.verticalLayout_3.addWidget(self.tableView)
            self.tabWidget_2.setTabsClosable(True)
            self.tabWidget_2.addTab(tab_tmp, "")
            self.tabWidget_2.setTabText(num,table)
            this['tab_'+str(num)]=tab_tmp
            self.openTables.append(table)
            self.tabWidget_2.setCurrentIndex(num)

            self.label_page = QtWidgets.QLabel(tab_tmp)
            self.label_page.setObjectName("label_page")
            self.horizontalLayout.addWidget(self.label_page)
            self.toolButton_page_first = QtWidgets.QToolButton(tab_tmp)
            self.toolButton_page_first.setObjectName("toolButton_page_first")
            self.horizontalLayout.addWidget(self.toolButton_page_first)
            self.toolButton_page_before = QtWidgets.QToolButton(tab_tmp)
            self.toolButton_page_before.setObjectName("toolButton_page_before")
            self.horizontalLayout.addWidget(self.toolButton_page_before)
            self.toolButton_page_next = QtWidgets.QToolButton(tab_tmp)
            self.toolButton_page_next.setObjectName("toolButton_page_next")
            self.horizontalLayout.addWidget(self.toolButton_page_next)
            self.toolButton_page_end = QtWidgets.QToolButton(tab_tmp)
            self.toolButton_page_end.setObjectName("toolButton_page_end")
            self.horizontalLayout.addWidget(self.toolButton_page_end)

    def closeTablesTab(self,index):
        table=self.tabWidget_2.tabText(index)
        self.openTables.remove(table)
        self.tabWidget_2.removeTab(index)

    def aboutQT(self):
        QMessageBox.aboutQt(self,'关于QT')

    def aboutUs(self):
        QMessageBox.about(self,'关于JiSql','使用Pyqt5编写的跨平台mysql工具')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/ji.ico"))
    ui = Ui_MainWindow()
    ui.show()

    sys.exit(app.exec_())
