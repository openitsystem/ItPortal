# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 20:33
# @Author  :
import threading
from datetime import datetime
#继承Thread，需要实现run方法
# 申请权限的多线程
from adapi.ad_api import adapi
from admin_account.Profile import readprofile
from dfs.dbinfo import get_manager_dfs_group_from
from dfs.folder import dfs_api


class thr_creat_folder(threading.Thread):
    def __init__(self,username,level3_path):
        self.username = username     #当前登陆用户的AD
        self.level3_path = level3_path   # 3层文件夹 路径
        threading.Thread.__init__(self)
    def run(self):
        try:
            Level3Folder = dfs_api().postapi("Level3Folder", path=self.level3_path)
            if Level3Folder['isSuccess']:
                get_manager_dfs_group_froms = get_manager_dfs_group_from(self.level3_path)
                if get_manager_dfs_group_froms:
                    for manager_dfs_group in get_manager_dfs_group_froms:
                        group_name = manager_dfs_group.get("group_name", '')
                        AddUserToGroups = adapi().Initialapi("AddUserToGroup", sAMAccountName=self.username, groupname=group_name)
                        # if AddUserToGroups['isSuccess'] or "对象已存在" in AddUserToGroups['message']:
        except Exception as e:
            print(e)

#新建 3层文件夹 创建数据库，新建AD权限组，添加权限
def thr_creat_folder_level3(username,level3_path):
    updateauthority = thr_creat_folder(username,level3_path)
    updateauthority.start()


class thr_set_file_mysql(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        try:
            mysql_host = readprofile('mysql', 'ip')
            mysql_user = readprofile('mysql', 'username')
            mysql_port = readprofile('mysql', 'Port')
            mysql_password = (readprofile('mysql', 'Password'))
            mysql_database = 'itdev-portal'
            dfs_api_mysqlconfig = dfs_api().postapi("dfs_api_mysqlconfig", mysql_host=mysql_host, mysql_user=mysql_user, mysql_port=mysql_port, mysql_password=mysql_password,
                                                    mysql_database=mysql_database)
            if dfs_api_mysqlconfig['isSuccess']:
                result = {'isSuccess': True, 'message': '数据更新成功'}
            else:
                result = {'isSuccess': False, 'message': '数据库连接失败'}
            return result
        except Exception as e:
            print(e)

#修改文件服务器连接的数据库
def set_file_mysql():
    updateau = thr_set_file_mysql()
    updateau.start()


class thr_set_file_FirstFolderAuthority(threading.Thread):
    def __init__(self,domain):
        self.domain = domain
        threading.Thread.__init__(self)

    def run(self):
        try:
            dfs_api().postapi("FirstFolderAuthority", domain=self.domain, tokenid='102')
        except Exception as e:
            print(e)

#异步文件夹权限权限初始化
def set_file_FirstFolderAuthority(domain):
    updateau = thr_set_file_FirstFolderAuthority(domain)
    updateau.start()