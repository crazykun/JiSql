#!/usr/bin/python3
import os
import os.path

### ui 文件转 py文件   

#列出所有路径下的ui文件
dir= './'

#列出目录下所有的ui文件
def listUiFile():
    list=[]
    files=os.listdir(dir)
    for filename in files:
        #print(dir + os.sep +f)
        #print(filename)
        if os.path.splitext(filename)[1]=='.ui':
            list.append(filename)
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
        #print(cmd)
        os.system(cmd)

#入口
if __name__=="__main__":
        
    runMain()