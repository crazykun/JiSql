#!/usr/bin/python3

import pymysql
from PyQt5.QtSql import QSqlQuery,QSqlDatabase


class DBManager():
    def __init__(self,conname='default',hostname='localhost',port='3306',user='root',password='qqdyw'):
        self.conname=conname
        self.hostname=hostname
        if port is '':
            port=3306
        self.port=int(port)
        self.user=user
        self.password=password

        if (QSqlDatabase.contains(self.conname)):
            self.db = QSqlDatabase.database(self.conname)  
        else:
            self.db = QSqlDatabase.addDatabase("QMYSQL",self.conname)  
        self.query = QSqlQuery(self.db)
      

    #测试数据库链接是否成功
    # if error == 'QSqlDatabase: QMYSQL driver not loaded QSqlDatabase: available drivers: QSQLITE QMYSQL QMYSQL3 QPSQL QPSQL7':
    # ldd /home/ji/.local/lib/python3.6/site-packages/PyQt5/Qt/plugins/sqldrivers/libqsqlmysql.so
    #     sudo apt-get install libmysqlclient18
    def testConnect(self):
        if (self.openDB()):   
            re="Success"  
        else:
            re="Failed !\n"
            re+=self.db.lastError().text()
        return re

    def openDB(self):
        if(self.db.isOpen() is not True): 
            self.db.setHostName(self.hostname)  
            self.db.setUserName(self.user);        
            self.db.setPort(int(self.port));
            self.db.setPassword(self.password); 
            return self.db.open()
        return True

    def closeDB(self):
        if(self.db.isOpen()):
            self.db.close()
    
    def showDBs(self):
        databases_list=[]
        self.openDB()
        self.query = QSqlQuery(self.db)
        re=self.query.exec("show databases")   
        if(re):
            while(self.query.next()):
                databases_list.append(self.query.value(0))
        return databases_list



    def execSql(self,sql):
        self.openDB()
        return self.query.exec(sql)   


if __name__ == "__main__":
    db=DBManager();
    db.testConnect()
    re=db.showTables()
    print(re)
    