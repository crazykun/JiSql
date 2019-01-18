# -*- codeding: utf-8 -*-
 
import sys
import os
import configparser
 
class Config(object):
    def __init__(self,file='connect.ini'):
        self.file = file
        self.cfg = configparser.ConfigParser()                 #创建一个 管理对象。
        self.cfg.read(self.file)
 
    def cfg_list(self):
        return self.cfg.sections()

    def cfg_get(self,se):
        return self.cfg[se]
    
    def cfg_has(self,se):
        return self.cfg.has_section(se)
 
    def cfg_dump(self):
        se_list = self.cfg.sections()                          #cfg.sections()显示文件中的所有 section
        print('==================>')
        for se in se_list:
            print(se)
            print(self.cfg.items(se))
        print('==================>')
 
    def delete_item(self,se,key):
        self.cfg.remove_option(se,key)                          #在 section 中删除一个 item
 
    def delete_section(self,se):
        self.cfg.remove_section(se)                             #删除一个 section
 
    def add_section(self,se):
        self.cfg.add_section(se)                                #添加一个 section
 
    def set_item(self,se,key,value):
        self.cfg.set(se,key,value)                             #往 section 中 添加一个 item（一个item由key和value构成）
 
    def save(self):
        fd = open(self.file,'w')
        self.cfg.write(fd)                                      #在内存中修改的内容写回文件中，相当于保存
        fd.close()
    
 
if __name__== '__main__':
    info = Config()
    info.add_section('default')
    info.set_item('default','conname','本地链接')
    info.set_item('default','hostname','127.0.0.1')
    info.set_item('default','port','3306')
    info.set_item('default','user','root')
    info.set_item('default','password','qqdyw')
    info.cfg_dump()
    info.save()
