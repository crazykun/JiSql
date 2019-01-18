# -*- codeding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from DBManager import DBManager
from Config import Config

class NewConnDialog(QtWidgets.QDialog):
    
    Signal_OpenDb=QtCore.pyqtSignal(str)
    
    def __init__(self,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)    
        self.cursor='';
        self.conf = Config()
        self.listWidget_conn.addItems(self.conf.cfg_list())


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(522, 284)
        self.pushButton_test = QtWidgets.QPushButton(Dialog)
        self.pushButton_test.setGeometry(QtCore.QRect(238, 220, 80, 27))
        self.pushButton_test.setObjectName("pushButton_test")
        self.pushButton_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_save.setGeometry(QtCore.QRect(324, 220, 80, 27))
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_cancle = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancle.setGeometry(QtCore.QRect(410, 220, 80, 27))
        self.pushButton_cancle.setObjectName("pushButton_cancle")
        self.pushButton_open = QtWidgets.QPushButton(Dialog)
        self.pushButton_open.setGeometry(QtCore.QRect(117, 219, 80, 27))
        self.pushButton_open.setObjectName("pushButton_open")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 477, 194))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_conname = QtWidgets.QLabel(self.widget)
        self.label_conname.setObjectName("label_conname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_conname)
        self.lineEdit_conname = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_conname.setObjectName("lineEdit_conname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_conname)
        self.label_hostname = QtWidgets.QLabel(self.widget)
        self.label_hostname.setObjectName("label_hostname")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_hostname)
        self.lineEdit_hostname = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_hostname.setObjectName("lineEdit_hostname")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_hostname)
        self.label_port = QtWidgets.QLabel(self.widget)
        self.label_port.setObjectName("label_port")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_port)
        self.lineEdit_port = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_port)
        self.label_user = QtWidgets.QLabel(self.widget)
        self.label_user.setObjectName("label_user")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_user)
        self.lineEdit_user = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_user)
        self.label_password = QtWidgets.QLabel(self.widget)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_password = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.gridLayout.addLayout(self.formLayout, 0, 2, 1, 1)
        self.listWidget_conn = QtWidgets.QListWidget(self.widget)
        self.listWidget_conn.setObjectName("listWidget_conn")
        self.gridLayout.addWidget(self.listWidget_conn, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)

        self.retranslateUi(Dialog)

        self.pushButton_cancle.clicked.connect(Dialog.reject)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_test.clicked.connect(self.testConnect)
        self.pushButton_open.clicked.connect(self.openDb)
        self.listWidget_conn.itemClicked.connect(self.editConn)
        self.listWidget_conn.itemDoubleClicked.connect(self.openDbFast)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "打开链接"))
        self.pushButton_test.setText(_translate("Dialog", "连接测试"))
        self.pushButton_save.setText(_translate("Dialog", "保存"))
        self.pushButton_cancle.setText(_translate("Dialog", "取消"))
        self.pushButton_open.setText(_translate("Dialog", "打开"))
        self.label_conname.setText(_translate("Dialog", "链接名:"))
        self.lineEdit_conname.setPlaceholderText(_translate("Dialog", "本地链接"))
        self.label_hostname.setText(_translate("Dialog", "主机名或者IP:"))
        self.lineEdit_hostname.setPlaceholderText(_translate("Dialog", "127.0.0.1"))
        self.label_port.setText(_translate("Dialog", "端口:"))
        self.lineEdit_port.setPlaceholderText(_translate("Dialog", "3306"))
        self.label_user.setText(_translate("Dialog", "用户名:"))
        self.lineEdit_user.setPlaceholderText(_translate("Dialog", "root"))
        self.label_password.setText(_translate("Dialog", "密码:"))
        self.lineEdit_password.setPlaceholderText(_translate("Dialog", "root"))
    
    def testConnect(self):
        conname=self.lineEdit_conname.text()
        hostname=self.lineEdit_hostname.text()
        port=self.lineEdit_port.text()
        user=self.lineEdit_user.text()
        password=self.lineEdit_password.text()
        if hostname=='' or user=='':
            QMessageBox.warning(self,'链接测试','主机名,用户名不能为空')  
            return 
        db=DBManager(conname,hostname,port,user,password)
        re=db._trytoConnect()
        QMessageBox.information(self,'链接测试',re)        
    
    def editConn(self,item):
        self.cursor=item.text()
        db=self.conf.cfg_get(self.cursor)
        self.lineEdit_conname.setText(db['conname'])
        self.lineEdit_hostname.setText(db['hostname'])
        self.lineEdit_port.setText(db['port'])
        self.lineEdit_user.setText(db['user'])
        self.lineEdit_password.setText(db['password'])
    
    def save(self): 
        conname=self.lineEdit_conname.text()
        hostname=self.lineEdit_hostname.text()
        port=self.lineEdit_port.text()
        user=self.lineEdit_user.text()
        password=self.lineEdit_password.text()
        if self.cursor is '':
            print(self.conf.cfg_list())
            if conname in self.conf.cfg_list():
                QMessageBox.about(self,'提示','链接名已存在')
                return ''
            else:
                self.conf.add_section(conname)    
                self.cursor=conname    
        else:
            if self.cursor != conname:
                self.conf.delete_section(self.cursor) 
                self.conf.add_section(conname)    
                self.cursor=conname 
        self.conf.set_item(self.cursor,'conname',conname)
        self.conf.set_item(self.cursor,'hostname',hostname)
        self.conf.set_item(self.cursor,'port',port)
        self.conf.set_item(self.cursor,'user',user)
        self.conf.set_item(self.cursor,'password',password)
        self.conf.save() 
        #重置list widget
        self.listWidget_conn.clear()
        self.listWidget_conn.addItems(self.conf.cfg_list())


    def _translate(self,context, text, disambig=None):
        sys.stdout.encoding
        return QtWidgets.QApplication.translate(context, text, disambig)


    def openDbFast(self,item):
        self.cursor=item.text()
        self.openDb()
        
    def openDb(self):
        if self.cursor is '':
            QMessageBox.about(self,'提示','请选择要打开的链接')
        else:
            self.Signal_OpenDb.emit(self.cursor)
            self.accept()
        


if __name__=="__main__":
    
    app=QtWidgets.QApplication(sys.argv)

    form=Ui_NewConnDialog()
    form.show()
    sys.exit(app.exec_())


