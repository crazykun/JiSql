#!/usr/bin/python3

from PyQt5.QtSql import QSqlQuery,QSqlDatabase,QSqlQueryModel
from PyQt5.QtCore import Qt


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

    def showTables(self,database):
        tables_list=[]
        self.openDB()
        self.query.exec("use "+database)   
        re=self.query.exec("show tables")   
        if(re):
            while(self.query.next()):
                tables_list.append(self.query.value(0))
        return tables_list

    def showColumns(self,table):
        columns=[]
        self.openDB()
        re=self.query.exec("select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s';" % (table))   
        if(re):
            while(self.query.next()):
                columns.append(self.query.value(0))
        return columns

    def getList(self,table,header,where='1=1',page=1,pagesize=100):
        model=QSqlQueryModel()
        # model.setTable(table)
        model.setQuery('select * from %s where %s limit %s , %s' % (table,where,(page-1)*pagesize,pagesize),self.db)
        i=0
        for h in header:
            model.setHeaderData(i,Qt.Horizontal,h)
            i+=1
        return model
    
    def getCount(self,table,where='1=1'):
        model=QSqlQueryModel()
        model.setQuery('count * from %s where %s ' % (table,where),self.db)
        return model


    def execSql(self,sql):
        self.openDB()
        return self.query.exec(sql)   


if __name__ == "__main__":
    my_db=DBManager();
    my_db.testConnect()
    re=my_db.showTables('test')
    print(re)
    