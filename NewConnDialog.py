# -*- codeding: utf-8 -*-

# Form implementation generated from reading ui file 'ui4.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from DBManager import DBManager
from Config import Config
from ui.Ui_NewConnDialog import Ui_ConnDialog

class NewConnDialog(QtWidgets.QDialog,Ui_ConnDialog):
    
    Signal_OpenDb=QtCore.pyqtSignal(str)
    
    def __init__(self,conf=None):
        super(NewConnDialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)      

        #当前打开的配置游标
        self.cursor=''
        if conf is not None:
            self.conf=conf
        else:
            self.conf = Config()
        self.listWidget_conn.addItems(self.conf.cfg_list())
        self.listWidget_conn.setContextMenuPolicy(Qt.CustomContextMenu)



    def newConn(self):
        self.lineEdit_conname.setText('')
        self.lineEdit_hostname.setText('')
        self.lineEdit_port.setText('3306')
        self.lineEdit_user.setText('')
        self.lineEdit_password.setText('')
        self.cursor=''
    
    def testConnect(self):
        conname=self.lineEdit_conname.text()
        hostname=self.lineEdit_hostname.text()
        port=self.lineEdit_port.text()
        user=self.lineEdit_user.text()
        password=self.lineEdit_password.text()
        if hostname=='' or user=='':
            QMessageBox.warning(self,'链接测试','主机名,用户名不能为空')  
            return 
        try:
            newDB=DBManager(conname,hostname,port,user,password)
        except:
            QMessageBox.warning(self,'链接测试','配置参数有误!')  
        else:
            QMessageBox.information(self,'链接测试',newDB.testConnect())        
    
    def editConn(self,item):
        self.cursor=item.text()
        db=self.conf.cfg_get(self.cursor)
        self.lineEdit_conname.setText(db['conname'])
        self.lineEdit_hostname.setText(db['hostname'])
        self.lineEdit_port.setText(db['port'])
        self.lineEdit_user.setText(db['user'])
        self.lineEdit_password.setText(db['password'])
    
    def saveConn(self): 
        conname=self.lineEdit_conname.text()
        hostname=self.lineEdit_hostname.text()
        port=self.lineEdit_port.text()
        user=self.lineEdit_user.text()
        password=self.lineEdit_password.text()
        if conname is '':
            QMessageBox.warning(self,'提示','请输入链接名')
            return 
        if self.cursor is '':
            # print(self.conf.cfg_list())
            if conname in self.conf.cfg_list():
                QMessageBox.about(self,'提示','链接名已存在')
                return ''
            else:
                self.conf.add_section(conname)    
                self.cursor=conname    
        else:
            if self.cursor != conname:
                if conname in self.conf.cfg_list():
                    QMessageBox.about(self,'提示','链接名已存在')
                    return ''
                else:
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
        QMessageBox.information(self,'提示','保存成功')
        


    #双击直接打开数据库
    def openDbFast(self,item):
        self.cursor=item.text()
        self.openDb()
        
    def openDb(self):
        if self.cursor is '':
            QMessageBox.about(self,'提示','请选择要打开的链接')
        else:
            print(self.cursor)
            self.Signal_OpenDb.emit(self.cursor)
            self.accept()

    def rightClick(self,point):      
        item=self.listWidget_conn.itemAt(point)
        if item is None:
            return
        self.rightItem=item
        popMenu = QtWidgets.QMenu(self.listWidget_conn) 
        popMenu.addAction(QtWidgets.QAction('修改',self.listWidget_conn))
        popMenu.addAction(QtWidgets.QAction('删除',self.listWidget_conn))
        popMenu.triggered['QAction*'].connect(self.rightMenu)
        popMenu.exec_(QtGui.QCursor.pos())

    def rightMenu(self,action):
        # print(self.rightItem)
        if action.text()=='修改':
            self.editConn(self.rightItem)
        elif action.text()=='删除':
            self.delConn(self.rightItem)
        else:
            pass

    def delConn(self,item):
        self.listWidget_conn.takeItem(self.listWidget_conn.row(item))
        self.listWidget_conn.removeItemWidget(item)
        self.conf.cfg_get(item.text())
        self.conf.delete_section(item.text())
    
    def closeDialog(self):
        self.close()
        


if __name__=="__main__":
    
    app=QtWidgets.QApplication(sys.argv)

    form=NewConnDialog()
    form.show()
    sys.exit(app.exec_())


