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
        self.currentConname = ''  # 当前链接名字
        self.currentTabWidget=''
        self.openDBClassList = []  # 所有打开的数据库db
        self.openConNameList = []  # 所有打开的数据名字列表
        self.currentTable = ''  # 当前打开的表
        self.openTables = []  # 所有打开的表
        self.currentLine = ''  # 当前行
        self.currentTreeWidgets=''
        self.pagesDataDict={} #分页组件 {'链接名_数据库1_表1':1,'链接名_数据库2_表1':2}

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
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setObjectName("verticalLayout_main")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabsClosable(True)
        self.verticalLayout_main.addWidget(self.tabWidget)

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

        self.tabWidget.tabCloseRequested['int'].connect(self.closeDbTab)
        self.tabWidget.currentChanged['int'].connect(self.changeDbTab)
        
        MainWindow.setCentralWidget(self.centralwidget)

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
        self.conn = NewConnDialog(self.conf)
        self.conn.Signal_OpenDb.connect(self.openConn)
        self.conn.exec_()
        self.conn.raise_()

    def importConn(self):
        file, ok = QtWidgets.QFileDialog.getOpenFileName(None, 'Save File', os.getenv('HOME'))


    def openConn(self, conname):
        self.currentConname=conname
        if conname in self.openConNameList:
            self.currentDBIndex=self.openConNameList.index(conname)
            self.tabWidget.setCurrentIndex( self.currentDBIndex)
        else:
            conf = self.conf.cfg_get(conname)
            try:
                self.currentDB = DBManager(conf['conname'], conf['hostname'], conf['port'], conf['user'], conf['password'])
            except:
                self.conn.closeDialog()
                QMessageBox.warning(self, '提醒','配置参数有误')
                return
            re = self.currentDB.testConnect()
            if(re != 'Success'):
                self.conn.closeDialog()
                QMessageBox.information(self, '链接失败', re)
                return            
            dbList=self.currentDB.showDBs()  
            #初始化界面
            self.setupBaseUi(dbList)   
            index = len(self.openDBClassList)
            self.currentDBIndex = index            
            self.openDBClassList.append(self.currentDB)
            self.openConNameList.append(conname)
            self.tabWidget.setTabText(index,conname)
            self.tabWidget.setCurrentIndex(index)
       

    def setupBaseUi(self,dbList):
        tab_index=len(self.openDBClassList)
        if  tab_index is 0:
            self.pushButton_open.hide()       
        #大tab页
        tab_new = QtWidgets.QWidget()
        tab_new.setObjectName("tab"+str(tab_index))        
        horizontalLayout_tab_body = QtWidgets.QHBoxLayout(tab_new)
        horizontalLayout_tab_body.setObjectName("horizontalLayout_tab_body"+str(tab_index))
        horizontalLayout_tab_main = QtWidgets.QHBoxLayout()
        horizontalLayout_tab_main.setObjectName("horizontalLayout_tab_main"+str(tab_index))

        #添加tree
        tree=self.setupDbTree(tab_index,dbList)
        horizontalLayout_tab_main.addWidget(tree)
        
        #右侧
        verticalLayout_right_main = QtWidgets.QVBoxLayout()
        verticalLayout_right_main.setObjectName("verticalLayout_right_main"+str(tab_index))
        horizontalLayout_search_bar = QtWidgets.QHBoxLayout()
        horizontalLayout_search_bar.setObjectName("horizontalLayout_search_bar"+str(tab_index))
        textEdit_search_input = QtWidgets.QTextEdit(tab_new)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(textEdit_search_input.sizePolicy().hasHeightForWidth())
        textEdit_search_input.setSizePolicy(sizePolicy)
        textEdit_search_input.setMinimumSize(QtCore.QSize(0, 60))
        textEdit_search_input.setObjectName("textEdit"+str(tab_index))
        horizontalLayout_search_bar.addWidget(textEdit_search_input)
        pushButton_search_btn = QtWidgets.QPushButton(tab_new)
        pushButton_search_btn.setText("执行")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pushButton_search_btn.sizePolicy().hasHeightForWidth())
        pushButton_search_btn.setSizePolicy(sizePolicy)
        pushButton_search_btn.setMinimumSize(QtCore.QSize(60, 60))
        pushButton_search_btn.setObjectName("pushButton"+str(tab_index))
        # pushButton_search_btn.setStyleSheet("background:qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))")
        horizontalLayout_search_bar.addWidget(pushButton_search_btn)
        verticalLayout_right_main.addLayout(horizontalLayout_search_bar)
        tabWidget_tableslist = QtWidgets.QTabWidget(tab_new)
        tabWidget_tableslist.setObjectName("tabWidget_tableslist"+str(tab_index))
        tabWidget_tableslist.setTabsClosable(True)

        verticalLayout_right_main.addWidget(tabWidget_tableslist)   
        horizontalLayout_tab_main.addLayout(verticalLayout_right_main)
        horizontalLayout_tab_body.addLayout(horizontalLayout_tab_main)

        self.tabWidget.addTab(tab_new, "")      
        self.currentTabWidget=tabWidget_tableslist
        
        tabWidget_tableslist.tabCloseRequested['int'].connect(self.closeTablesTab)



    
    def closeDbTab(self,index):
        self.tabWidget.removeTab(index)
        del self.openDBClassList[index]
        del self.openConNameList[index]
        if len(self.openDBClassList) is 0:
            self.tabWidget.hide()
            self.pushButton_open.show()   

    def changeDbTab(self,index):
        tab=self.tabWidget.tabText(index)
        self.currentConname=tab
        print(self.tabWidget.widget(0))

    #左侧树
    def setupDbTree(self, tabIndex,dbList):
        thisItem = QtWidgets.QTreeWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(thisItem.sizePolicy().hasHeightForWidth())
        thisItem.setSizePolicy(sizePolicy)
        thisItem.setMinimumSize(QtCore.QSize(200, 0))
        thisItem.setObjectName("treeWidget_"+str(tabIndex))
        thisItem.setHeaderHidden(True)
        items=[]
        for x in dbList:            
            i=QtWidgets.QTreeWidgetItem(thisItem)
            i.setText(0,x)
            items.append(i)
        thisItem.addTopLevelItems(items)

        thisItem.itemDoubleClicked['QTreeWidgetItem*','int'].connect(self.clickTreeItem)
        self.currentTreeWidgets=thisItem
        return thisItem
        

    #点击左侧树
    def clickTreeItem(self,item,column):
        if(item.parent() is  None):
            #database 展开表
            database=item.text(column)
            tables=self.currentDB.showTables(database)
            items=[]
            for x in tables:            
                i=QtWidgets.QTreeWidgetItem(item)
                i.setText(0,x)
                items.append(i)
            item.addChildren(items)
        else:
            #打开表
            database=item.parent().text(0)
            table=item.text(column)
            self.currentTable=self.currentConname+'.'+database+'.'+table
            self.pagesDataDict.get(self.currentConname+'.'+database+'.'+table, 1)
            columns=self.currentDB.showColumns(table)
            dataModel=self.currentDB.getList(table,columns)
            self.setupTableData(table,dataModel)
    
    #初始化表数据
    def setupTableData(self,table,dataModel):
        if table in self.openTables:
            self.currentTabWidget.setCurrentIndex(self.openTables.index(table))
        else:
            this = self.__dict__
            table_index=len(self.openTables) 
            tab_tmp = QtWidgets.QWidget()
            tab_tmp.setObjectName("tab_tmp")
            verticalLayout_table = QtWidgets.QVBoxLayout(tab_tmp)
            verticalLayout_table.setObjectName("verticalLayout_table_"+str(table_index))
            tableView = QtWidgets.QTableView(tab_tmp)
            tableView.setObjectName("tableView_"+str(table_index))
            tableView.setModel(dataModel)
            verticalLayout_table.addWidget(tableView)
            
            self.currentTabWidget.addTab(tab_tmp, "")
            self.currentTabWidget.setTabText(table_index,table)
            this['table_'+str(table_index)]=tab_tmp
            self.openTables.append(table)
            self.currentTabWidget.setCurrentIndex(table_index)
            
            #初始化分页
            horizontalLayout_page = QtWidgets.QHBoxLayout()
            horizontalLayout_page.setObjectName("horizontalLayout_page_"+str(table_index))
            spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            horizontalLayout_page.addItem(spacerItem)           
            label_page = QtWidgets.QLabel(tab_tmp)
            label_page.setObjectName("label_page")
            horizontalLayout_page.addWidget(label_page)
            toolButton_page_first = QtWidgets.QToolButton(tab_tmp)
            toolButton_page_first.setObjectName("toolButton_page_first_"+str(table_index))
            horizontalLayout_page.addWidget(toolButton_page_first)
            toolButton_page_before = QtWidgets.QToolButton(tab_tmp)
            toolButton_page_before.setObjectName("toolButton_page_before_"+str(table_index))
            horizontalLayout_page.addWidget(toolButton_page_before)
            toolButton_page_next = QtWidgets.QToolButton(tab_tmp)
            toolButton_page_next.setObjectName("toolButton_page_next_"+str(table_index))
            horizontalLayout_page.addWidget(toolButton_page_next)
            toolButton_page_end = QtWidgets.QToolButton(tab_tmp)
            toolButton_page_end.setObjectName("toolButton_page_end_"+str(table_index))
            horizontalLayout_page.addWidget(toolButton_page_end)
            label_page.setText("共1000条,共10页,当前第1页")
            toolButton_page_first.setText("|<")
            toolButton_page_before.setText("<")
            toolButton_page_next.setText(">")
            toolButton_page_end.setText(">|")
            toolButton_page_first.clicked.connect(lambda: self.search(page=1))
            toolButton_page_before.clicked.connect(lambda: self.search(pagetype='-1'))
            toolButton_page_next.clicked.connect(lambda: self.search(pagetype='+1'))
            toolButton_page_end.clicked.connect(lambda: self.search(pagetype='end'))
            verticalLayout_table.addLayout(horizontalLayout_page)
    

    def search(self,where='',page=1,pagetype='',pagesize=100):
        print(dir(self.currentTreeWidgets))
        

    #添加表
    def addTablesTab(self,tabName):
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab_"+tabName)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.addTab(self.tab, tabName)

    #关闭表
    def closeTablesTab(self,index):
        # table=self.currentTabWidget.tabText(index)
        # self.openTables.remove(table)
        del self.openTables[index]
        self.currentTabWidget.removeTab(index)

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
