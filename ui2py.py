#!/usr/bin/python3
import os
import os.path

### ui 文件转 py文件   

#列出目录下所有的ui文件
def listUiFile(dir='./'):
    list=[]
    files=os.listdir(dir) 
    for i in range(0,len(files)):
        path = os.path.join(dir,files[i])
        if os.path.isdir(path):
           list.extend(listUiFile(path))
        if os.path.isfile(path):
            if os.path.splitext(files[i])[1]=='.ui':
                print(path)
                list.append(path)
    return list

#把扩展名为ui的文件改成.py文件
def transPyFile(filename):
    return os.path.splitext(filename)[0]+'.py'


#调用系统命令把ui文件转换为python文件
def runMain():
    list=listUiFile()
    for uifile in list:
        pyfile=transPyFile(uifile)
        cmd='pyuic5 -o {pyfile} {uifile}'.format(pyfile=pyfile,uifile=uifile)
        os.system(cmd)

#入口
if __name__=="__main__":
        
    runMain()