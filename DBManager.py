from PyQt5.QtSql import QSqlQuery,QSqlDatabase

class DBManager():
    def __init__(self,conname='default',hostname='localhost',port='3306',user='root',password='qqdyw',table='',**kw):
        if (QSqlDatabase.contains(conname)):
            self.db = QSqlDatabase.database(conname)  
        else:
            self.db = QSqlDatabase.addDatabase("QMYSQL",conname)  
        self.db.setHostName(hostname)  
        self.db.setUserName(user);
        if port is '':
            port=3306
        self.db.setPort(int(port));
        self.db.setPassword(password); 
        for k,w in kw.items():
            setattr(self,k,w)

        # self.query = QSqlQuery()
        # ## create database
        # self.query.exec_("CREATE DATABASE test1")

        # ## Choose database
        # self.db.setDatabaseName("test1")
        # self._trytoConnect()
        # #also can be :self.query.exec_("USE test1")

    ## Connect and check connection state
    def _trytoConnect(self):
        if (self.db.open()):   
            re="Success"  
        else:
            re="Failed !\n"
            re+=QSqlDatabase.lastError(self.db).text()
            # ldd /home/ji/.local/lib/python3.6/site-packages/PyQt5/Qt/plugins/sqldrivers/libqsqlmysql.so
            # if error == 'QSqlDatabase: QMYSQL driver not loaded QSqlDatabase: available drivers: QSQLITE QMYSQL QMYSQL3 QPSQL QPSQL7':
            #     sudo apt-get install libmysqlclient18

        self.db.close()
        return re



if __name__ == "__main__":
    db=DBManager();
    db._trytoConnect()
    