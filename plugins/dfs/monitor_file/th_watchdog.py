# -*- coding: utf-8 -*-
import os
import threading
import time
from folder_api.dbinfo import *
from folder_api.interface import dfs_folder

#继承Thread，需要实现folder方法
class watchdog_folder(threading.Thread):
    def __init__(self,vaule,src_path,dest_path):
        get_management_configurations = get_management_configuration()
        self.domain = get_management_configurations.get('domain', '')  # 域名
        self.Basic_authority = get_management_configurations.get('Basic_authority', '')  # 默认文件夹权限
        self.DFS_distinguishedName = get_management_configurations.get('dfs_group', '')  # AD 文件权限组的位置
        self.dfs_manager = get_management_configurations.get('dfs_manager', '')  # AD 文件权限组的位置
        self.AD_time = get_management_configurations.get('AD_time', '')  # AD组新建完成后的缓冲时间，（文件夹无法实时获取到新建组）
        self.vaule = vaule
        self.src_path = src_path
        self.dest_path = dest_path
        threading.Thread.__init__(self)#异步调用
        
    def creat_folder(self):
        try:
            time.sleep(self.AD_time)
            exists_src_path = os.path.exists(self.src_path) #判断这个文件路径还存不存在
            if exists_src_path:
                get_folder_first_chiices = get_folder_first_chiice()
                for i in get_folder_first_chiices:
                    if i['watchdog'] == 1 and i['folder_path'] in self.src_path:
                        if i["folder_level"]==1 or i["folder_level"]==0:
                            level_path_list = self.src_path.replace(i['folder_path'],'').split('\\')
                            level_path_len = len(level_path_list)+i["folder_level"]-1
                            if level_path_len==1:
                                dfs_folder().level1_folder(self.src_path)
                                insert_watchdog_log("True", 'creat_folder', self.src_path, "", "插入一层文件夹数据")
                            elif level_path_len==2:
                                dfs_folder().level2_folder(self.src_path)
                                insert_watchdog_log("True", 'creat_folder', self.src_path, "", "插入二层文件夹数据")
                            elif level_path_len==3:
                                get_management_configurations = get_management_configuration()
                                if get_management_configurations:
                                    domain = get_management_configurations['domain']
                                    dfs_folder().level3_folder(self.src_path,domain,'10087')
                                    insert_watchdog_log("True", 'creat_folder', self.src_path, "", "插入三层文件夹数据")
            elif os.path.exists(self.dest_path):
                get_folder_first_chiices = get_folder_first_chiice()
                for i in get_folder_first_chiices:
                    if i['watchdog'] == 1 and i['folder_path'] in self.dest_path:
                        if i["folder_level"] == 1 or i["folder_level"] == 0:
                            level_path_list = self.dest_path.replace(i['folder_path'], '').split('\\')
                            level_path_len = len(level_path_list) + i["folder_level"] - 1
                            if level_path_len == 1:
                                dfs_folder().level1_folder(self.dest_path)
                                insert_watchdog_log("True", 'creat_folder', self.dest_path, "", "插入一层文件夹数据")
                            elif level_path_len == 2:
                                dfs_folder().level2_folder(self.dest_path)
                                insert_watchdog_log("True", 'creat_folder', self.dest_path, "", "插入二层文件夹数据")
                            elif level_path_len == 3:
                                get_management_configurations = get_management_configuration()
                                if get_management_configurations:
                                    domain = get_management_configurations['domain']
                                    dfs_folder().level3_folder(self.dest_path, domain, '10087')
                                    insert_watchdog_log("True", 'creat_folder', self.dest_path, "", "插入三层文件夹数据")
            return True
        except Exception as e:
            insert_watchdog_log("False", 'creat_folder', self.src_path, self.domain, str(e))
            return False
        
    def deleta_folder(self):
        try:
            if self.domain:
                show_folder_level1s = show_folder_level1(self.src_path)
                if show_folder_level1s:
                    level1_id = show_folder_level1s[0]['level1_id']
                    dfs_folder().delete_level1(level1_id,self.domain,'10087')
                    insert_watchdog_log("True", 'deleta_folder', self.src_path, self.domain, "删除一层文件夹数据")
                elif show_folder_level2(self.src_path):
                    show_folder_level2s = show_folder_level2(self.src_path)
                    level2_id = show_folder_level2s[0]['level2_id']
                    dfs_folder().delete_level2(level2_id, self.domain, '10087')
                    insert_watchdog_log("True", 'deleta_folder', self.src_path, self.domain, "删除二层文件夹数据")
                elif show_folder_level3(self.src_path):
                    show_folder_level3s = show_folder_level3(self.src_path)
                    level3_id = show_folder_level3s[0]['level3_id']
                    dfs_folder().delete_level3(level3_id, self.domain, '10087')
                    insert_watchdog_log("True", 'deleta_folder', self.src_path, self.domain, "删除三层文件夹数据")
            return True
        except Exception as e:
            insert_watchdog_log("False", 'deleta_folder', self.src_path, self.domain,str(e))
            return False

    def move_folder(self):
        try:
            if self.domain:
                show_folder_level1s = show_folder_level1(self.src_path)
                if show_folder_level1s:
                    level1_id = show_folder_level1s[0]['level1_id']
                    dfs_folder().rename_level1(level1_id,self.dest_path,self.domain,'10087')
                    insert_watchdog_log("True", 'move_folder', self.src_path, self.dest_path, self.domain+":重命名一层文件夹数据")
                elif show_folder_level2(self.src_path):
                    show_folder_level2s = show_folder_level2(self.src_path)
                    level2_id = show_folder_level2s[0]['level2_id']
                    dfs_folder().rename_level2(level2_id,self.dest_path, self.domain, '10087')
                    insert_watchdog_log("True", 'move_folder', self.src_path, self.dest_path, self.domain+":重命名二层文件夹数据")
                elif show_folder_level3(self.src_path):
                    show_folder_level3s = show_folder_level3(self.src_path)
                    level3_id = show_folder_level3s[0]['level3_id']
                    dfs_folder().rename_level3(level3_id,self.dest_path, self.domain, '10087')
                    insert_watchdog_log("True", 'move_folder', self.src_path, self.dest_path, self.domain+":重命名三层文件夹数据")
                else:
                    self.creat_folder()
            return True
        except Exception as e:
            insert_watchdog_log("False", 'move_folder', self.src_path, self.dest_path,self.domain+":"+str(e))
            return False

    def run(self):
        if self.vaule =="deleted":
            self.deleta_folder()
        elif self.vaule =="created":
            self.creat_folder()
        elif self.vaule =='moved':
            self.move_folder()
        return 1

def thr_watchdog_folder(vaule,src_path,dest_path):
    watch_Exc = watchdog_folder(vaule,src_path,dest_path)
    watch_Exc.start()