from PyQt5.QtSql import QSqlQuery,QSqlDatabase

class DBManager():
    def __init__(self,conname='default',hostname='localhost',port='3306',user='root',password='qqdyw',table='',**kw):
        if (QSqlDatabase.contains(conname)):
            self.db = QSqlDatabase.database(conname)  
        else:
            self.db = QSqlDatabase.addDatabase("QMYSQL",conname)  
        self.db.setHostName(hostname)  
        self.db.setUserName(user);
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
            re="Failed to connect to mysql"
        print(re)
        return re
        self.db.close()



if __name__ == "__main__":
    db=DBManager();
    db._trytoConnect()
    